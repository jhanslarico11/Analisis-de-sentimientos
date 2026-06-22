"""Análisis de sentimientos con múltiples modos y fallback automático."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd

import config
from src.utils.helpers import logger

POSITIVE_WORDS = {
    "excelente", "bueno", "buena", "genial", "apoyo", "apoyar", "mejor", "positivo",
    "correcto", "acertado", "bravo", "felicito", "grande", "honesto", "capaz",
    "inteligente", "propuesta", "solucion", "solución", "victoria", "gano", "ganó",
    "convence", "claro", "coherente", "firme", "valiente", "admirable",
}
NEGATIVE_WORDS = {
    "malo", "mala", "horrible", "pésimo", "pesimo", "odio", "corrupto", "corrupta",
    "mentira", "mentiroso", "ladron", "ladrón", "robo", "vergüenza", "verguenza",
    "incompetente", "desastre", "fracaso", "rechazo", "critico", "critico", "critica",
    "critica", "no sirve", "peor", "basura", "asco", "falso", "falsa", "engaña",
    "engano", "engañó", "engano", "dictadura", "criminal", "delincuente",
}


@dataclass
class SentimentResult:
    label: str
    score: float


class LexiconSentimentAnalyzer:
    """Analizador léxico de respaldo."""

    def predict(self, text: str) -> SentimentResult:
        if not text:
            return SentimentResult("Neutral", 0.5)
        tokens = set(text.lower().split())
        pos = len(tokens & POSITIVE_WORDS)
        neg = len(tokens & NEGATIVE_WORDS)
        if pos > neg:
            score = min(0.95, 0.55 + pos * 0.08)
            return SentimentResult("Positivo", score)
        if neg > pos:
            score = max(0.05, 0.45 - neg * 0.08)
            return SentimentResult("Negativo", score)
        return SentimentResult("Neutral", 0.5)


class LogisticSentimentAnalyzer:
    """TF-IDF + Logistic Regression."""

    def __init__(self):
        self.vectorizer = None
        self.model = None
        self.lexicon = LexiconSentimentAnalyzer()
        self._load_or_train()

    def _load_or_train(self) -> None:
        try:
            import joblib
            if config.TFIDF_PATH.exists() and config.LR_MODEL_PATH.exists():
                self.vectorizer = joblib.load(config.TFIDF_PATH)
                self.model = joblib.load(config.LR_MODEL_PATH)
                logger.info("Modelo LR cargado desde disco.")
                return
        except Exception as exc:
            logger.warning("No se pudo cargar LR: %s", exc)

        self._train_default()

    def _train_default(self) -> None:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        import joblib

        samples = [
            ("keiko excelente propuesta economica apoyo total", "Positivo"),
            ("roberto muy buen candidato honesto y preparado", "Positivo"),
            ("gran debate roberto gano con propuestas claras", "Positivo"),
            ("keiko demostro liderazgo y experiencia positiva", "Positivo"),
            ("roberto Sanchez propone empleo y seguridad bien", "Positivo"),
            ("keiko corrupta no vuelve mas verguenza total", "Negativo"),
            ("roberto incompetente propuestas vacias pesimo", "Negativo"),
            ("odio a keiko fujimori ladrona mentirosa", "Negativo"),
            ("roberto no convence desastre total rechazo", "Negativo"),
            ("peor candidato roberto sanchez fracaso", "Negativo"),
            ("el debate fue transmitido ayer en la noche", "Neutral"),
            ("los candidatos hablaron de economia y salud", "Neutral"),
            ("segunda vuelta presidencial peru junio 2026", "Neutral"),
            ("programa periodistico analizo propuestas", "Neutral"),
            ("comentario sobre el formato del debate", "Neutral"),
        ]
        texts = [s[0] for s in samples]
        labels = [s[1] for s in samples]
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        X = self.vectorizer.fit_transform(texts)
        self.model = LogisticRegression(max_iter=1000, random_state=42)
        self.model.fit(X, labels)
        config.MODELS_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.vectorizer, config.TFIDF_PATH)
        joblib.dump(self.model, config.LR_MODEL_PATH)
        logger.info("Modelo LR entrenado y guardado.")

    def predict(self, text: str) -> SentimentResult:
        if not text.strip():
            return SentimentResult("Neutral", 0.5)
        try:
            X = self.vectorizer.transform([text])
            label = self.model.predict(X)[0]
            proba = self.model.predict_proba(X)[0]
            classes = list(self.model.classes_)
            idx = classes.index(label)
            score = float(proba[idx])
            if label == "Negativo":
                score = 1 - score
            elif label == "Neutral":
                score = 0.5
            return SentimentResult(str(label), score)
        except Exception:
            return self.lexicon.predict(text)


class TransformerSentimentAnalyzer:
    """Analizador basado en Transformers (BETO / RoBERTa)."""

    MODEL_MAP = {
        "BETO": "dccuchile/bert-base-spanish-wwm-uncased",
        "RoBERTa Español": "Recognai/bert-base-spanish-wwm-uncased-finetuned-ner",
    }

    def __init__(self, model_name: str = "BETO"):
        self.model_name = model_name
        self.pipeline = None
        self.lexicon = LexiconSentimentAnalyzer()
        self._loaded = False

    def _load(self) -> bool:
        if self._loaded:
            return self.pipeline is not None
        try:
            from transformers import pipeline
            import torch

            model_id = self.MODEL_MAP.get(self.model_name, self.MODEL_MAP["BETO"])
            device = 0 if torch.cuda.is_available() else -1
            self.pipeline = pipeline(
                "sentiment-analysis",
                model=model_id,
                tokenizer=model_id,
                device=device,
                truncation=True,
                max_length=256,
            )
            self._loaded = True
            return True
        except Exception as exc:
            logger.warning("Transformers no disponible (%s): %s", self.model_name, exc)
            self.pipeline = None
            self._loaded = True
            return False

    def predict(self, text: str) -> SentimentResult:
        if not text.strip():
            return SentimentResult("Neutral", 0.5)
        if not self._load() or self.pipeline is None:
            return self.lexicon.predict(text)
        try:
            result = self.pipeline(text[:512])[0]
            label_raw = result["label"].lower()
            score = float(result["score"])
            if "pos" in label_raw or label_raw in {"positive", "positivo", "label_2"}:
                return SentimentResult("Positivo", score)
            if "neg" in label_raw or label_raw in {"negative", "negativo", "label_0"}:
                return SentimentResult("Negativo", 1 - score)
            return SentimentResult("Neutral", 0.5)
        except Exception:
            return self.lexicon.predict(text)


class SentimentAnalyzer:
    """Orquestador con lazy loading y fallback automático."""

    def __init__(self, mode: str = "Automático"):
        self.mode = mode
        self._lr: Optional[LogisticSentimentAnalyzer] = None
        self._beto: Optional[TransformerSentimentAnalyzer] = None
        self._roberta: Optional[TransformerSentimentAnalyzer] = None
        self._lexicon = LexiconSentimentAnalyzer()
        self.active_backend = "Lexicon"

    @property
    def lr(self) -> LogisticSentimentAnalyzer:
        if self._lr is None:
            self._lr = LogisticSentimentAnalyzer()
        return self._lr

    @property
    def beto(self) -> TransformerSentimentAnalyzer:
        if self._beto is None:
            self._beto = TransformerSentimentAnalyzer("BETO")
        return self._beto

    @property
    def roberta(self) -> TransformerSentimentAnalyzer:
        if self._roberta is None:
            self._roberta = TransformerSentimentAnalyzer("RoBERTa Español")
        return self._roberta

    def _resolve_backend(self):
        if self.mode == "TF-IDF + Logistic Regression":
            self.active_backend = "Logistic Regression"
            return self.lr
        if self.mode == "BETO":
            self.active_backend = "BETO"
            return self.beto
        if self.mode == "RoBERTa Español":
            self.active_backend = "RoBERTa"
            return self.roberta
        # Automático
        try:
            import torch
            from transformers import pipeline  # noqa: F401
            if torch.cuda.is_available() or True:
                self.active_backend = "BETO (Auto)"
                return self.beto
        except Exception:
            pass
        self.active_backend = "Logistic Regression (Auto)"
        return self.lr

    def predict(self, text: str) -> SentimentResult:
        backend = self._resolve_backend()
        result = backend.predict(text)
        if result.label not in config.SENTIMENTS:
            result = SentimentResult("Neutral", 0.5)
        return result

    def process_dataframe(self, df: pd.DataFrame, text_col: str = "clean_text") -> pd.DataFrame:
        out = df.copy()
        sentiments = []
        scores = []
        for text in out[text_col].fillna("").astype(str):
            res = self.predict(text)
            sentiments.append(res.label)
            scores.append(res.score)
        out["sentiment"] = sentiments
        out["sentiment_score"] = scores
        return out


def evaluate_sentiment_models(texts: list[str], labels: list[str]) -> pd.DataFrame:
    """Evalúa y compara modelos de sentimiento."""
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

    modes = ["TF-IDF + Logistic Regression", "BETO", "RoBERTa Español"]
    rows = []
    for mode in modes:
        analyzer = SentimentAnalyzer(mode=mode)
        preds = [analyzer.predict(t).label for t in texts]
        report = classification_report(labels, preds, output_dict=True, zero_division=0)
        rows.append({
            "model": mode,
            "accuracy": accuracy_score(labels, preds),
            "precision": report["weighted avg"]["precision"],
            "recall": report["weighted avg"]["recall"],
            "f1": f1_score(labels, preds, average="weighted", zero_division=0),
            "support": len(labels),
            "confusion_matrix": confusion_matrix(labels, preds).tolist(),
            "classification_report": report,
        })
    result = pd.DataFrame(rows)
    if not result.empty:
        best = result.loc[result["f1"].idxmax(), "model"]
        result["is_best"] = result["model"] == best
    return result
