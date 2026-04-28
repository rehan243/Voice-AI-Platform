"""
Rolling sentiment: small transformer head + lexicon fallback. Good for dashboards, not therapy.
"""
from __future__ import annotations

import logging
import re
from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, List, Optional

import numpy as np
import torch
from pydantic import BaseModel, Field
from transformers import AutoModelForSequenceClassification, AutoTokenizer

logger = logging.getLogger(__name__)

_LEX_POS = {"good", "great", "thanks", "excellent", "love", "perfect"}
_LEX_NEG = {"bad", "terrible", "angry", "hate", "awful", "useless", "refund"}


@dataclass
class SentimentConfig:
    model_name: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    window_segments: int = 12
    transformer_weight: float = 0.72
    device: str = "cpu"
    clip: float = 1.0


class RollingSentimentAnalyzer:
    def __init__(self, cfg: Optional[SentimentConfig] = None) -> None:
        self._cfg = cfg or SentimentConfig()
        self._tok = AutoTokenizer.from_pretrained(self._cfg.model_name)
        self._model = AutoModelForSequenceClassification.from_pretrained(self._cfg.model_name)
        self._model.eval()
        self._device = torch.device(self._cfg.device)
        self._model.to(self._device)
        self._window: Deque[float] = deque(maxlen=self._cfg.window_segments)
        self._utter_scores: List[float] = []

    def _lexicon_score(self, text: str) -> float:
        tokens = re.findall(r"[A-Za-z']+", text.lower())
        if not tokens:
            return 0.0
        pos = sum(1 for t in tokens if t in _LEX_POS)
        neg = sum(1 for t in tokens if t in _LEX_NEG)
        if pos == neg == 0:
            return 0.0
        return float(pos - neg) / float(pos + neg + 1e-6)

    @torch.inference_mode()
    def _transformer_score(self, text: str) -> float:
        if not text.strip():
            return 0.0
        enc = self._tok(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=256,
            padding=True,
        )
        enc = {k: v.to(self._device) for k, v in enc.items()}
        logits = self._model(**enc).logits.float()
        probs = torch.softmax(logits, dim=-1)[0].cpu().numpy()
        # Map 3-class RoBERTa sentiment to [-1, 1] roughly: neg, neu, pos
        if probs.shape[0] == 3:
            return float(probs[2] - probs[0])
        return float(probs[-1] - probs[0])

    def score_utterance(self, text: str) -> Dict[str, float]:
        lex = self._lexicon_score(text)
        tr = self._transformer_score(text)
        w = self._cfg.transformer_weight
        combined = self._clamp(w * tr + (1.0 - w) * lex)
        self._window.append(combined)
        self._utter_scores.append(combined)
        rolling = float(np.mean(self._window)) if self._window else combined
        return {
            "utterance": combined,
            "rolling": rolling,
            "lexicon": lex,
            "transformer": tr,
        }

    @torch.inference_mode()
    def score_batch(self, texts: List[str]) -> List[Dict[str, float]]:
        """Batched path for backfilling analytics; not latency-optimized."""
        if not texts:
            return []
        enc = self._tok(
            texts,
            return_tensors="pt",
            truncation=True,
            max_length=256,
            padding=True,
        )
        enc = {k: v.to(self._device) for k, v in enc.items()}
        logits = self._model(**enc).logits.float()
        probs = torch.softmax(logits, dim=-1).cpu().numpy()
        out: List[Dict[str, float]] = []
        w = self._cfg.transformer_weight
        for i, text in enumerate(texts):
            row = probs[i]
            if row.shape[0] == 3:
                tr = float(row[2] - row[0])
            else:
                tr = float(row[-1] - row[0])
            lex = self._lexicon_score(text)
            combined = self._clamp(w * tr + (1.0 - w) * lex)
            out.append(
                {
                    "utterance": combined,
                    "rolling": combined,
                    "lexicon": lex,
                    "transformer": tr,
                }
            )
        return out

    @property
    def window_volatility(self) -> float:
        if len(self._window) < 2:
            return 0.0
        arr = np.array(self._window, dtype=np.float64)
        return float(arr.std())

    def reset(self) -> None:
        self._window.clear()
        self._utter_scores.clear()
