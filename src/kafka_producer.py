"""
Kafka egress with DLQ. If brokers are flapping, we at least don't silently drop audio metadata.
"""
from __future__ import annotations

import json
import logging
import threading
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

from kafka import KafkaProducer
from kafka.errors import KafkaError

logger = logging.getLogger(__name__)


@dataclass
class KafkaProducerConfig:
    bootstrap_servers: str
    audio_topic: str = "voice.audio.events"
    transcript_topic: str = "voice.transcripts"
    sentiment_topic: str = "voice.sentiment"
    dlq_topic: str = "voice.dlq"
    compression_type: str = "zstd"
    linger_ms: int = 20
    max_retries: int = 5
    request_timeout_ms: int = 30_000


class KafkaAudioProducer:
    def __init__(
        self,
        cfg: KafkaProducerConfig,
        on_delivery_ok: Optional[Callable[[str], None]] = None,
    ) -> None:
        self._cfg = cfg
        self._on_ok = on_delivery_ok
        self._producer = KafkaProducer(
            bootstrap_servers=[s.strip() for s in cfg.bootstrap_servers.split(",") if s.strip()],
            compression_type=cfg.compression_type,
            linger_ms=cfg.linger_ms,
            retries=cfg.max_retries,
            request_timeout_ms=cfg.request_timeout_ms,
            value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8"),
            key_serializer=lambda k: k.encode("utf-8") if k is not None else None,
        )
        self._send_lock = threading.Lock()
        self._metrics = {"sent": 0, "dlq": 0, "fail": 0}

    def _partition_key(self, call_id: str) -> str:
        return call_id or "unknown"

    def metrics_snapshot(self) -> Dict[str, int]:
        return dict(self._metrics)

    def publish_audio_event(self, call_id: str, payload: Dict[str, Any]) -> None:
        body = {"call_id": call_id, "type": "audio", "payload": payload, "ts": time.time()}
        self._send(self._cfg.audio_topic, self._partition_key(call_id), body)

    def publish_transcript(self, call_id: str, text: str, meta: Optional[dict] = None) -> None:
        body = {
            "call_id": call_id,
            "type": "transcript",
            "text": text,
            "meta": meta or {},
            "ts": time.time(),
        }
        self._send(self._cfg.transcript_topic, self._partition_key(call_id), body)

    def publish_sentiment(
        self,
        call_id: str,
        scores: Dict[str, float],
        utterance_idx: int,
    ) -> None:
        body = {
            "call_id": call_id,
            "type": "sentiment",
            "utterance_idx": utterance_idx,
            "scores": scores,
            "ts": time.time(),
        }
        self._send(self._cfg.sentiment_topic, self._partition_key(call_id), body)

    def _send(self, topic: str, key: str, value: Dict[str, Any]) -> None:
        try:
            with self._send_lock:
                fut = self._producer.send(topic, key=key, value=value)
            fut.get(timeout=10)
            self._metrics["sent"] += 1
            if self._on_ok:
                self._on_ok(topic)
        except KafkaError as e:
            logger.error("kafka send failed -> DLQ: %s", e)
            self._metrics["fail"] += 1
            self._dlq(topic, key, value, str(e))
        except Exception as e:
            logger.exception("unexpected kafka error")
            self._metrics["fail"] += 1
            self._dlq(topic, key, value, repr(e))

    def _dlq(self, original_topic: str, key: str, value: Dict[str, Any], err: str) -> None:
        dlq_body = {
            "original_topic": original_topic,
            "key": key,
            "value": value,
            "error": err,
            "ts": time.time(),
        }
        try:
            with self._send_lock:
                fut = self._producer.send(self._cfg.dlq_topic, key=key, value=dlq_body)
            fut.get(timeout=10)
            self._metrics["dlq"] += 1
        except Exception as e:
            logger.critical("DLQ publish failed, data lost: %s", e)

    def flush(self) -> None:
        self._producer.flush()

    def close(self) -> None:
        try:
            self.flush()
        finally:
            self._producer.close()
