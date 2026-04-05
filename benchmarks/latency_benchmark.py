"""Voice AI Latency Benchmark - Rehan Malik"""

import time
import statistics
from dataclasses import dataclass


@dataclass
class LatencyReport:
    component: str
    p50_ms: float
    p95_ms: float
    p99_ms: float
    mean_ms: float
    samples: int


def measure_latency(fn, iterations=100):
    """Measure function latency with percentile reporting."""
    latencies = []
    for _ in range(iterations):
        start = time.perf_counter()
        fn()
        latencies.append((time.perf_counter() - start) * 1000)

    latencies.sort()
    n = len(latencies)
    return LatencyReport(
        component=fn.__name__,
        p50_ms=round(latencies[n // 2], 2),
        p95_ms=round(latencies[int(n * 0.95)], 2),
        p99_ms=round(latencies[int(n * 0.99)], 2),
        mean_ms=round(statistics.mean(latencies), 2),
        samples=n,
    )


def simulate_asr():
    """Simulated ASR processing."""
    time.sleep(0.001)

def simulate_llm():
    """Simulated LLM inference."""
    time.sleep(0.002)

def simulate_tts():
    """Simulated TTS synthesis."""
    time.sleep(0.001)


if __name__ == "__main__":
    components = [simulate_asr, simulate_llm, simulate_tts]
    total_p99 = 0
    for fn in components:
        report = measure_latency(fn, 50)
        print(f"{report.component}: p50={report.p50_ms}ms p95={report.p95_ms}ms p99={report.p99_ms}ms")
        total_p99 += report.p99_ms
    print(f"\nEnd-to-end p99 estimate: {total_p99:.1f}ms")
