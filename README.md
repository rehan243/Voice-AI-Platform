# Voice-AI-Platform

Real-time concurrent voice infrastructure processing 500+ simultaneous calls with zero-latency voice-to-data ingestion engines.

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazon-aws&logoColor=white)](https://aws.amazon.com)
[![Kafka](https://img.shields.io/badge/Kafka-231F20?style=flat-square&logo=apache-kafka&logoColor=white)](https://kafka.apache.org)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)

---

## Overview

Production-grade voice AI infrastructure designed for real-time, concurrent call processing at scale. Built to handle 500+ simultaneous voice streams with zero-latency ingestion, real-time transcription, and intelligent routing.

This system powers the voice AI capabilities at **Reallytics.ai**, processing live audio streams into structured business data for downstream analytics and AI-driven decision-making.

## Architecture

```
                    ┌─────────────────────────────────────────────┐
                    │              Load Balancer (ALB)             │
                    └────────────────────┬────────────────────────┘
                                         │
                    ┌────────────────────▼────────────────────────┐
                    │         WebSocket Gateway (FastAPI)          │
                    │         - Connection management              │
                    │         - Audio stream ingestion              │
                    │         - Session tracking                   │
                    └────────────────────┬────────────────────────┘
                                         │
                    ┌────────────────────▼────────────────────────┐
                    │           Apache Kafka Cluster               │
                    │         - Audio chunk streaming               │
                    │         - Event-driven processing             │
                    │         - Partition-based scaling             │
                    └──────┬─────────────┬──────────────┬─────────┘
                           │             │              │
              ┌────────────▼──┐  ┌───────▼───────┐  ┌──▼────────────┐
              │  STT Worker   │  │ Sentiment     │  │  Analytics    │
              │  (gRPC/C++)   │  │ Analyzer      │  │  Engine       │
              │  - Whisper    │  │ - Real-time   │  │  - Metrics    │
              │  - Custom ASR │  │ - Emotion     │  │  - Insights   │
              └───────┬───────┘  └───────┬───────┘  └──┬────────────┘
                      │                  │              │
              ┌───────▼──────────────────▼──────────────▼─────────┐
              │              Results Aggregator                     │
              │           - Structured output                      │
              │           - Real-time dashboard feed               │
              └──────────────────────┬────────────────────────────┘
                                     │
              ┌──────────────────────▼────────────────────────────┐
              │          Data Store (PostgreSQL + Redis)           │
              └───────────────────────────────────────────────────┘
```

## Key Features

- **Zero-Latency Ingestion**: WebSocket-based audio stream ingestion with sub-50ms processing latency
- **Massive Concurrency**: Handles 500+ simultaneous voice calls through Kafka partition-based scaling
- **High-Performance STT**: gRPC microservices with C++ modules (CUDA, Eigen) for speech-to-text inference, reducing latency by 25%
- **Real-Time Sentiment Analysis**: Live emotion and sentiment detection on voice streams
- **Streaming Architecture**: Apache Kafka for event-driven, fault-tolerant audio chunk processing
- **Cloud-Native Deployment**: AWS ECS/ECR with Docker containerization, auto-scaling, and health monitoring
- **Sales Insights Pipeline**: Real-time extraction of business signals from voice conversations

## Tech Stack

| Category | Technologies |
|---|---|
| **Core** | Python, C++ (CUDA, Eigen), FastAPI |
| **Streaming** | Apache Kafka, WebSockets, gRPC |
| **ML/AI** | Whisper, Custom ASR models, Sentiment models |
| **Cloud** | AWS (ECS, ECR, Lambda, S3, RDS), Docker |
| **Data** | PostgreSQL, Redis, Real-time streaming |
| **Monitoring** | Grafana, CloudWatch, Custom dashboards |

## Project Structure

```
voice-ai-platform/
├── gateway/
│   ├── websocket_handler.py       # WebSocket connection management
│   ├── session_manager.py         # Call session tracking
│   └── audio_ingestion.py         # Raw audio stream processing
├── kafka/
│   ├── producer.py                # Audio chunk producer
│   ├── consumer.py                # Stream consumers
│   └── config.py                  # Kafka cluster configuration
├── stt_engine/
│   ├── grpc_server.cpp            # High-performance gRPC STT service
│   ├── whisper_inference.py       # Whisper model inference
│   ├── cuda_kernels/              # Custom CUDA kernels for acceleration
│   └── proto/                     # gRPC protocol definitions
├── analytics/
│   ├── sentiment_analyzer.py      # Real-time sentiment pipeline
│   ├── emotion_detector.py        # Voice emotion recognition
│   └── insights_engine.py         # Business signal extraction
├── infrastructure/
│   ├── docker-compose.yml         # Local development setup
│   ├── Dockerfile                 # Production container
│   ├── ecs-task-definition.json   # AWS ECS deployment
│   └── kafka-setup.yml            # Kafka cluster config
├── tests/
│   ├── test_gateway.py
│   ├── test_stt_engine.py
│   └── test_analytics.py
├── requirements.txt
└── README.md
```

## Performance Benchmarks

| Metric | Value |
|---|---|
| Concurrent calls supported | 500+ |
| Audio ingestion latency | < 50ms |
| STT inference latency | < 200ms (with C++/CUDA) |
| Sentiment analysis latency | < 100ms |
| System uptime | 99.9% |
| Latency reduction (vs pure Python) | 25% |
| Additional concurrent users supported | +15% |

## Getting Started

```bash
# Clone the repository
git clone https://github.com/rehan243/Voice-AI-Platform.git
cd Voice-AI-Platform

# Set up environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start Kafka and dependencies
docker-compose up -d

# Run the gateway
uvicorn gateway.websocket_handler:app --host 0.0.0.0 --port 8000

# Run STT workers
python stt_engine/whisper_inference.py --workers 4
```

## Environment Variables

```bash
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
AWS_REGION=us-east-1
REDIS_URL=redis://localhost:6379
DATABASE_URL=postgresql://user:pass@localhost:5432/voiceai
STT_MODEL_PATH=/models/whisper-large-v3
CUDA_VISIBLE_DEVICES=0,1
```

## Author

**Rehan Malik** - CTO @ Reallytics.ai

- [LinkedIn](https://linkedin.com/in/rehan-malik-cto)
- [GitHub](https://github.com/rehan243)
- [Email](mailto:rehanmalil99@gmail.com)