"""Pipeline completo de Machine Learning."""

from __future__ import annotations

import pandas as pd

from src.emotion.analyzer import EmotionAnalyzer
from src.ml.bot_detector import BotDetector
from src.ml.influence import InfluenceCalculator
from src.preprocessing.text_cleaner import TextPreprocessor
from src.sentiment.analyzer import SentimentAnalyzer
from src.sentiment.candidate_detector import CandidateDetector, classify_political
from src.topic_modeling.analyzer import TopicAnalyzer
from src.utils.helpers import ensure_columns, logger, normalize_dates


class NLPipeline:
    """Pipeline end-to-end de procesamiento NLP."""

    REQUIRED_COLUMNS = [
        "id", "source", "text", "author", "date", "likes", "replies",
        "video_id", "video_title", "channel", "url",
    ]

    def __init__(self, sentiment_mode: str = "Automático"):
        self.preprocessor = TextPreprocessor(use_lemma=False, use_stem=False)
        self.sentiment = SentimentAnalyzer(mode=sentiment_mode)
        self.candidates = CandidateDetector()
        self.emotions = EmotionAnalyzer()
        self.topics = TopicAnalyzer()
        self.influence = InfluenceCalculator()
        self.bots = BotDetector()

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        if df is None or df.empty:
            logger.warning("DataFrame vacío en pipeline.")
            return pd.DataFrame()

        out = ensure_columns(df, self.REQUIRED_COLUMNS)
        out = normalize_dates(out, "date")
        out["text"] = out["text"].fillna("").astype(str)
        out["likes"] = pd.to_numeric(out["likes"], errors="coerce").fillna(0).astype(int)
        out["replies"] = pd.to_numeric(out["replies"], errors="coerce").fillna(0).astype(int)

        out = self.preprocessor.process_dataframe(out)
        out = self.sentiment.process_dataframe(out)
        out = self.candidates.process_dataframe(out)
        out = self.emotions.process_dataframe(out)
        out = self.topics.analyze(out)
        out = self.influence.process_dataframe(out)
        out = self.bots.process_dataframe(out)

        out["political_classification"] = out.apply(
            lambda r: classify_political(
                str(r.get("text", "")),
                str(r.get("candidate", "Ninguno")),
                str(r.get("sentiment", "Neutral")),
            ),
            axis=1,
        )
        return out

    def predict_single(self, text: str) -> dict:
        clean = self.preprocessor.clean(text)
        sentiment = self.sentiment.predict(clean)
        candidate = self.candidates.predict(text)
        emotion = self.emotions.predict(text)
        topic = self.topics.classifier.predict(clean)
        political = classify_political(text, candidate, sentiment.label)
        return {
            "text": text,
            "clean_text": clean,
            "sentiment": sentiment.label,
            "sentiment_score": sentiment.score,
            "candidate": candidate,
            "emotion": emotion,
            "topic": topic,
            "political_classification": political,
        }
