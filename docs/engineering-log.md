# Engineering Log

Running notes on design decisions and lessons learned.


### 2026-07-06

**Observation:** When tuning the latency for streaming ASR/TTS, I noticed that using a smaller batch size (e.g., 16) significantly reduced latency but increased the inference time per batch. This tradeoff was crucial when deciding between real-time processing and overall throughput.

### 2026-07-21

**Observation:** I've been working on optimizing streaming ASR/TTS latency and real-time inference. One key insight was that using a smaller model size (e.g., **Wav2Vec 2.0** instead of **Wav2Vec 2.0-XL**) significantly reduced latency but at the cost of some accuracy. The **tradeoff** was noticeable in low-resource environments, where the smaller model struggled with certain accents and background noise.
