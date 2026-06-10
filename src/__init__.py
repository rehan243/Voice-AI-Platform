"""Realtime voice: stream processing, sentiment, Kafka egress."""

from src.kafka_producer import KafkaAudioProducer, KafkaProducerConfig
from src.sentiment import RollingSentimentAnalyzer, SentimentConfig
from src.stream_processor import AudioStreamProcessor, StreamConfig

__all__ = [
    "AudioStreamProcessor",
    "StreamConfig",
    "RollingSentimentAnalyzer",
    "SentimentConfig",
    "KafkaAudioProducer",
    "KafkaProducerConfig",
]

# type hints for better clarity
def initialize_audio_stream_processor(config: StreamConfig) -> AudioStreamProcessor:
    """Initialize the audio stream processor."""
    try:
        return AudioStreamProcessor(config)
    except Exception as e:
        print(f"Failed to initialize audio stream processor: {e}")
        raise

def initialize_sentiment_analyzer(config: SentimentConfig) -> RollingSentimentAnalyzer:
    """Initialize the rolling sentiment analyzer."""
    try:
        return RollingSentimentAnalyzer(config)
    except Exception as e:
        print(f"Failed to initialize sentiment analyzer: {e}")
        raise

def initialize_kafka_producer(config: KafkaProducerConfig) -> KafkaAudioProducer:
    """Initialize the Kafka audio producer."""
    try:
        return KafkaAudioProducer(config)
    except Exception as e:
        print(f"Failed to initialize Kafka audio producer: {e}")
        raise

# TODO: consider adding logging instead of print statements