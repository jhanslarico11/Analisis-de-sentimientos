"""Paquete de análisis de sentimientos."""

from src.sentiment.analyzer import SentimentAnalyzer, evaluate_sentiment_models
from src.sentiment.candidate_detector import CandidateDetector, classify_political, detect_candidate

__all__ = [
    "SentimentAnalyzer",
    "CandidateDetector",
    "detect_candidate",
    "classify_political",
    "evaluate_sentiment_models",
]
