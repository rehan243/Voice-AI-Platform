# Engineering Log

Running notes on design decisions and lessons learned.


### 2026-07-06

**Observation:** When tuning the latency for streaming ASR/TTS, I noticed that using a smaller batch size (e.g., 16) significantly reduced latency but increased the inference time per batch. This tradeoff was crucial when deciding between real-time processing and overall throughput.
