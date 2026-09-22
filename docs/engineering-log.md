# Engineering Log

Running notes on design decisions and lessons learned.


### 2026-07-06

**Observation:** When tuning the latency for streaming ASR/TTS, I noticed that using a smaller batch size (e.g., 16) significantly reduced latency but increased the inference time per batch. This tradeoff was crucial when deciding between real-time processing and overall throughput.

### 2026-07-21

**Observation:** I've been working on optimizing streaming ASR/TTS latency and real-time inference. One key insight was that using a smaller model size (e.g., **Wav2Vec 2.0** instead of **Wav2Vec 2.0-XL**) significantly reduced latency but at the cost of some accuracy. The **tradeoff** was noticeable in low-resource environments, where the smaller model struggled with certain accents and background noise.

### 2026-07-24

Experimented with a streaming ASR system and noticed that reducing the audio chunk size from 500ms to 250ms improved responsiveness but increased the overall processing load and latency spikes during peak inference. Tuning the model's buffer size is crucial; I found that too small of a buffer can cause frequent underflows, leading to dropped frames. Balancing chunk size and buffer settings is essential to maintain low latency without sacrificing stability in real-time applications.

### 2026-07-29

Implemented streaming ASR with a focus on reducing latency during real-time inference. Noticed that increasing the frame rate from 100ms to 50ms improved responsiveness but also led to a significant rise in CPU usage, causing occasional drops in accuracy. Balancing latency and resource consumption is crucial; I'm considering dynamic frame rate adjustments based on system load to mitigate this.

### 2026-08-03

Reviewed streaming ASR/TTS latency and real-time inference today. Reinforced that measuring the change end-to-end beats reasoning about it in isolation — the numbers rarely match the intuition.

### 2026-08-09

Reviewed streaming ASR/TTS latency and real-time inference today. Reinforced that measuring the change end-to-end beats reasoning about it in isolation — the numbers rarely match the intuition.

### 2026-08-10

Reviewed streaming ASR/TTS latency and real-time inference today. Reinforced that measuring the change end-to-end beats reasoning about it in isolation — the numbers rarely match the intuition.

### 2026-08-18

Reviewed streaming ASR/TTS latency and real-time inference today. Reinforced that measuring the change end-to-end beats reasoning about it in isolation — the numbers rarely match the intuition.

### 2026-09-13

Reviewed streaming ASR/TTS latency and real-time inference today. Reinforced that measuring the change end-to-end beats reasoning about it in isolation — the numbers rarely match the intuition.

### 2026-09-22

Reviewed streaming ASR/TTS latency and real-time inference today. Reinforced that measuring the change end-to-end beats reasoning about it in isolation — the numbers rarely match the intuition.
