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

---

> **Source Code**: The production source code for this project is maintained in a private repository due to proprietary and client confidentiality requirements. This repository documents the architecture, design decisions, and technical approach. For code-level discussions or collaboration inquiries, feel free to reach out.


## Author

**Rehan Malik** - CTO @ Reallytics.ai

- [LinkedIn](https://linkedin.com/in/rehan-malik-cto)
- [GitHub](https://github.com/rehan243)
- [Email](mailto:rehanmalil99@gmail.com)