"""
WebSocket audio in, VAD-gated segments out. Designed for "it mostly works at 3am" ops.
"""
from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field
from typing import Awaitable, Callable, Dict, Optional

import webrtcvad
from fastapi import WebSocket

logger = logging.getLogger(__name__)

FrameCallback = Callable[[str, str, dict], Awaitable[None]]


@dataclass
class StreamConfig:
    sample_rate: int = 16_000
    frame_ms: int = 20
    vad_aggressiveness: int = 2
    max_segment_sec: float = 12.0
    queue_max_chunks: int = 400
    max_concurrent_ws: int = 600


class AudioStreamProcessor:
    def __init__(
        self,
        cfg: StreamConfig,
        stt_fn: Callable[[bytes, int], Awaitable[str]],
        on_transcript: Optional[FrameCallback] = None,
    ) -> None:
        self._cfg = cfg
        self._stt = stt_fn
        self._on_transcript = on_transcript
        self._vad = webrtcvad.Vad(cfg.vad_aggressiveness)
        self._bytes_per_frame = int(cfg.sample_rate * cfg.frame_ms / 1000) * 2
        self._connections: Dict[str, "_ConnState"] = {}
        self._lock = asyncio.Lock()
        self._accept_sem = asyncio.Semaphore(cfg.max_concurrent_ws)

    async def register(self, call_id: str) -> None:
        async with self._lock:
            self._connections[call_id] = _ConnState(self._cfg, self._vad, self._bytes_per_frame)

    async def unregister(self, call_id: str) -> None:
        async with self._lock:
            self._connections.pop(call_id, None)

    async def handle_ws(self, websocket: WebSocket, call_id: str) -> None:
        # Semaphore is coarse backpressure; still need per-call fairness in STT pools.
        async with self._accept_sem:
            await websocket.accept()
            await self.register(call_id)
            try:
                while True:
                    msg = await websocket.receive()
                    if msg.get("type") == "websocket.disconnect":
                        break
                    data = msg.get("bytes")
                    if not data:
                        continue
                    text = await self._feed(call_id, data)
                    if text:
                        await websocket.send_json(
                            {"type": "transcript", "text": text, "call_id": call_id}
                        )
                        if self._on_transcript:
                            await self._on_transcript(call_id, text, {"ts": time.time()})
            finally:
                await self.unregister(call_id)
                try:
                    await websocket.close()
                except Exception:
                    pass

    async def _feed(self, call_id: str, pcm_s16le: bytes) -> Optional[str]:
        async with self._lock:
            state = self._connections.get(call_id)
        if state is None:
            return None
        return await state.push(pcm_s16le, self._stt, self._cfg.sample_rate)


@dataclass
class _ConnState:
    cfg: StreamConfig
    vad: webrtcvad.Vad
    frame_bytes: int
    buffer: bytearray = field(default_factory=bytearray)
    speech_buf: bytearray = field(default_factory=bytearray)
    in_speech: bool = False
    segment_started: float = field(default_factory=time.monotonic)
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    async def push(
        self,
        chunk: bytes,
        stt_fn: Callable[[bytes, int], Awaitable[str]],
        sample_rate: int,
    ) -> Optional[str]:
        async with self.lock:
            self.buffer.extend(chunk)
            transcript: Optional[str] = None
            while len(self.buffer) >= self.frame_bytes:
                frame = bytes(self.buffer[: self.frame_bytes])
                del self.buffer[: self.frame_bytes]
                is_speech = self.vad.is_speech(frame, sample_rate)
                now = time.monotonic()
                if is_speech:
                    if not self.in_speech:
                        self.in_speech = True
                        self.segment_started = now
                        self.speech_buf.clear()
                    self.speech_buf.extend(frame)
                    if (now - self.segment_started) > self.cfg.max_segment_sec:
                        transcript = await self._flush_segment(stt_fn, sample_rate)
                else:
                    if self.in_speech and len(self.speech_buf) >= self.frame_bytes * 3:
                        transcript = await self._flush_segment(stt_fn, sample_rate)
                    self.in_speech = False
            return transcript

    async def _flush_segment(
        self,
        stt_fn: Callable[[bytes, int], Awaitable[str]],
        sample_rate: int,
    ) -> Optional[str]:
        if not self.speech_buf:
            return None
        audio = bytes(self.speech_buf)
        self.speech_buf.clear()
        self.in_speech = False
        try:
            return (await stt_fn(audio, sample_rate)).strip() or None
        except Exception as e:
            logger.warning("STT failed: %s", e)
            return None
