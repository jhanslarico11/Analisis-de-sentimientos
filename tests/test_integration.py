"""Tests de integración."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pytest

from src.analytics.metrics import PoliticalAnalytics
from src.database.manager import DatabaseManager
from src.ml.pipeline import NLPipeline
from src.reporting.generator import ReportGenerator
from src.utils.seed_data import generate_sample_dataframe


class TestIntegration:
    def test_end_to_end_pipeline(self, tmp_path):
        raw = generate_sample_dataframe(15)
        pipeline = NLPipeline(sentiment_mode="TF-IDF + Logistic Regression")
        processed = pipeline.run(raw)

        db = DatabaseManager(str(tmp_path / "integration.db"))
        db.dataframe_to_db(processed)
        loaded = db.get_all_comments()
        assert len(loaded) == len(processed)

        analytics = PoliticalAnalytics(loaded)
        conclusions = analytics.generate_conclusions()
        assert "summary" in conclusions
        assert "debate_winner" in conclusions

        reporter = ReportGenerator(loaded, output_dir=tmp_path)
        paths = reporter.generate_all()
        assert all(Path(p).exists() for p in paths.values())

    def test_analytics_metrics(self):
        raw = generate_sample_dataframe(20)
        pipeline = NLPipeline(sentiment_mode="TF-IDF + Logistic Regression")
        processed = pipeline.run(raw)
        analytics = PoliticalAnalytics(processed)
        metrics = analytics.all_metrics()
        assert not metrics["share_of_voice"].empty
        assert isinstance(metrics["polarization"], float)
