"""Topic modeling: diccionario temático + LDA."""

from __future__ import annotations

from typing import Optional

import pandas as pd

import config
from src.utils.helpers import logger


class TopicClassifier:
    """Clasificación temática por diccionario de palabras clave."""

    def predict(self, text: str) -> str:
        if not text:
            return "General"
        text_lower = text.lower()
        scores = {}
        for topic, keywords in config.TOPIC_KEYWORDS.items():
            scores[topic] = sum(1 for kw in keywords if kw in text_lower)
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else "General"

    def process_dataframe(self, df: pd.DataFrame, text_col: str = "clean_text") -> pd.DataFrame:
        out = df.copy()
        out["topic"] = out[text_col].fillna("").astype(str).apply(self.predict)
        return out


class LDATopicModel:
    """Modelado de temas con LDA para detectar temas emergentes."""

    def __init__(self, n_topics: int = 8):
        self.n_topics = n_topics
        self.vectorizer = None
        self.lda = None
        self.feature_names: list[str] = []

    def fit(self, texts: list[str]) -> bool:
        if len(texts) < 5:
            logger.warning("Insuficientes textos para LDA.")
            return False
        try:
            from sklearn.decomposition import LatentDirichletAllocation
            from sklearn.feature_extraction.text import CountVectorizer

            self.vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=1000)
            X = self.vectorizer.fit_transform(texts)
            self.lda = LatentDirichletAllocation(
                n_components=min(self.n_topics, max(2, len(texts) // 3)),
                random_state=42,
                max_iter=15,
            )
            self.lda.fit(X)
            self.feature_names = self.vectorizer.get_feature_names_out().tolist()
            return True
        except Exception as exc:
            logger.warning("Error en LDA: %s", exc)
            return False

    def get_top_words(self, n_words: int = 8) -> list[dict]:
        if self.lda is None:
            return []
        topics = []
        for idx, topic in enumerate(self.lda.components_):
            top_indices = topic.argsort()[-n_words:][::-1]
            words = [self.feature_names[i] for i in top_indices]
            topics.append({"topic_id": idx, "keywords": words, "label": self._map_to_theme(words)})
        return topics

    @staticmethod
    def _map_to_theme(words: list[str]) -> str:
        joined = " ".join(words)
        classifier = TopicClassifier()
        mapped = classifier.predict(joined)
        return mapped

    def predict_topics(self, texts: list[str]) -> list[int]:
        if self.lda is None or self.vectorizer is None:
            return [0] * len(texts)
        X = self.vectorizer.transform(texts)
        return self.lda.transform(X).argmax(axis=1).tolist()

    def emergent_topics(self, df: pd.DataFrame, text_col: str = "clean_text") -> pd.DataFrame:
        texts = df[text_col].fillna("").astype(str).tolist()
        if not self.fit(texts):
            return pd.DataFrame(columns=["topic_id", "keywords", "label", "count"])
        topics = self.get_top_words()
        topic_ids = self.predict_topics(texts)
        counts = pd.Series(topic_ids).value_counts()
        rows = []
        for t in topics:
            rows.append({
                "topic_id": t["topic_id"],
                "keywords": ", ".join(t["keywords"]),
                "label": t["label"],
                "count": int(counts.get(t["topic_id"], 0)),
            })
        return pd.DataFrame(rows).sort_values("count", ascending=False)


class TopicAnalyzer:
    """Orquestador de análisis temático."""

    def __init__(self):
        self.classifier = TopicClassifier()
        self.lda = LDATopicModel()

    def analyze(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.classifier.process_dataframe(df)

    def get_emergent(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.lda.emergent_topics(df)
