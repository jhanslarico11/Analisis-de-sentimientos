"""Tests unitarios."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pandas as pd
import pytest

from src.database.manager import DatabaseManager
from src.ml.pipeline import NLPipeline
from src.preprocessing.text_cleaner import TextPreprocessor
from src.sentiment.candidate_detector import detect_candidate, classify_political
from src.sentiment.analyzer import SentimentAnalyzer
from src.utils.seed_data import generate_sample_dataframe


@pytest.fixture
def sample_df():
    return generate_sample_dataframe(10)


@pytest.fixture
def temp_db(tmp_path):
    db_path = tmp_path / "test.db"
    return DatabaseManager(str(db_path))


class TestPreprocessor:
    def test_clean_removes_urls(self):
        p = TextPreprocessor(use_lemma=False)
        text = "Visita https://example.com #hashtag @user excelente"
        clean = p.clean(text)
        assert "https" not in clean
        assert "#" not in clean
        assert "@" not in clean

    def test_lowercase(self):
        p = TextPreprocessor(use_lemma=False)
        assert p.clean("MAYUSCULAS") == "mayusculas"


class TestCandidateDetector:
    def test_detect_keiko(self):
        assert detect_candidate("Apoyo a Keiko Fujimori") == "Keiko Fujimori"

    def test_detect_roberto(self):
        assert detect_candidate("Roberto Sánchez es mejor") == "Roberto Sánchez"

    def test_detect_both(self):
        assert detect_candidate("Keiko vs Roberto debate") == "Ambos"

    def test_political_classification(self):
        assert classify_political("text", "Keiko Fujimori", "Positivo") == "Apoya a Keiko"
        assert classify_political("text", "Roberto Sánchez", "Negativo") == "Critica a Roberto"


class TestSentiment:
    def test_positive(self):
        analyzer = SentimentAnalyzer(mode="TF-IDF + Logistic Regression")
        result = analyzer.predict("excelente propuesta economica apoyo total")
        assert result.label in ["Positivo", "Neutral"]

    def test_negative(self):
        analyzer = SentimentAnalyzer(mode="TF-IDF + Logistic Regression")
        result = analyzer.predict("corrupto ladron pesimo odio")
        assert result.label in ["Negativo", "Neutral"]


class TestDatabase:
    def test_insert_and_query(self, temp_db, sample_df):
        pipeline = NLPipeline(sentiment_mode="TF-IDF + Logistic Regression")
        processed = pipeline.run(sample_df)
        count = temp_db.dataframe_to_db(processed)
        assert count > 0
        loaded = temp_db.get_all_comments()
        assert len(loaded) >= count

    def test_delete(self, temp_db, sample_df):
        pipeline = NLPipeline(sentiment_mode="TF-IDF + Logistic Regression")
        processed = pipeline.run(sample_df)
        temp_db.dataframe_to_db(processed)
        deleted = temp_db.delete_all()
        assert deleted > 0
        assert temp_db.count() == 0


class TestPipeline:
    def test_full_pipeline(self, sample_df):
        pipeline = NLPipeline(sentiment_mode="TF-IDF + Logistic Regression")
        result = pipeline.run(sample_df)
        assert "sentiment" in result.columns
        assert "candidate" in result.columns
        assert "emotion" in result.columns
        assert len(result) == len(sample_df)

    def test_predict_single(self):
        pipeline = NLPipeline(sentiment_mode="TF-IDF + Logistic Regression")
        result = pipeline.predict_single("Keiko propuesta economica excelente")
        assert "sentiment" in result
        assert "candidate" in result
