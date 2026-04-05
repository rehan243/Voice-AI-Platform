# Voice AI Latency Optimization

## Pipeline Stages & Targets
| Stage | Target | Technique |
|-------|--------|-----------|
| VAD | <50ms | WebRTC VAD, Silero |
| ASR | <200ms | Whisper streaming, chunked |
| NLU | <100ms | Intent cache, local model |
| LLM | <500ms | Streaming, KV cache |
| TTS | <150ms | Streaming synthesis |
| Total | <1000ms | End-to-end target |

## Key Optimizations
- Stream everything: Don't wait for full ASR before starting NLU
- Speculative execution: Start TTS on first sentence while LLM generates rest
- Connection pooling: Reuse WebSocket connections
- Edge caching: Cache common responses at CDN level