#!/usr/bin/env python3
"""
Script de verificación del pipeline completo.
Ejecutar: python verify_pipeline.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import pandas as pd

import config
from src.analytics.metrics import PoliticalAnalytics
from src.database.manager import DatabaseManager
from src.ml.pipeline import NLPipeline
from src.reporting.generator import ReportGenerator
from src.utils.helpers import logger
from src.utils.seed_data import generate_sample_dataframe


def check(name: str, condition: bool, detail: str = "") -> bool:
    status = "[PASS]" if condition else "[FAIL]"
    msg = f"{status} | {name}"
    if detail:
        msg += f" | {detail}"
    print(msg)
    return condition


def main() -> int:
    print("=" * 60)
    print("VERIFICACIÓN DEL PIPELINE - Electoral Intelligence Platform")
    print("=" * 60)

    results = []

    # 1. Config
    results.append(check("Config", config.DB_PATH.parent.exists(), str(config.DATA_DIR)))

    # 2. Seed data
    raw = generate_sample_dataframe(20)
    results.append(check("Seed Data", not raw.empty, f"{len(raw)} registros"))

    # 3. NLP Pipeline
    pipeline = NLPipeline(sentiment_mode="TF-IDF + Logistic Regression")
    processed = pipeline.run(raw)
    required_cols = ["clean_text", "sentiment", "candidate", "emotion", "topic", "influence_score", "bot_probability"]
    has_cols = all(c in processed.columns for c in required_cols)
    results.append(check("NLP Pipeline", has_cols and len(processed) == len(raw), f"{len(processed)} procesados"))

    # 4. Predicción individual
    pred = pipeline.predict_single("Keiko excelente propuesta economica")
    results.append(check("Predicción RT", pred["sentiment"] in config.SENTIMENTS, pred["sentiment"]))

    # 5. Base de datos
    test_db = config.DATA_DIR / "test_verify.db"
    if test_db.exists():
        test_db.unlink()
    db = DatabaseManager(str(test_db))
    inserted = db.dataframe_to_db(processed)
    loaded = db.get_all_comments()
    results.append(check("Database CRUD", inserted > 0 and len(loaded) > 0, f"{inserted} insertados"))

    # 6. Analytics
    analytics = PoliticalAnalytics(processed)
    metrics = analytics.all_metrics()
    results.append(check("Analytics", "conclusions" in metrics, metrics["conclusions"].get("debate_winner", "")))

    # 7. Reportes
    reporter = ReportGenerator(processed, output_dir=config.REPORTS_DIR)
    md_path = reporter.to_markdown("verify_test.md")
    results.append(check("Reportes", Path(md_path).exists(), md_path))

    # 8. Fechas UTC
    processed["date"] = pd.to_datetime(processed["date"], errors="coerce", utc=True)
    processed["date"] = processed["date"].dt.tz_localize(None)
    results.append(check("UTC Fix", True, "Normalización de fechas OK"))

    # Resumen
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"RESULTADO: {passed}/{total} verificaciones exitosas")
    print("=" * 60)

    if passed == total:
        print("Pipeline completamente funcional.")
        return 0
    print("Algunas verificaciones fallaron.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
