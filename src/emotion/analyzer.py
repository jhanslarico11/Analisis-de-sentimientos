"""Análisis de emociones en comentarios políticos."""

from __future__ import annotations

import pandas as pd

import config

EMOTION_LEXICON = {
    "Alegría": [
        "feliz", "alegre", "genial", "excelente", "amo", "me encanta", "bravo", "victoria",
        "ganó", "gano", "orgullo", "celebrar", "bien", "positivo", "esperanza",
    ],
    "Ira": [
        "odio", "rabia", "enojado", "furioso", "indignado", "asco", "corrupto", "ladron",
        "ladrón", "mentiroso", "vergüenza", "verguenza", "inaceptable", "harto",
    ],
    "Tristeza": [
        "triste", "decepcion", "decepción", "pena", "llorar", "desilusion", "desilusión",
        "fracaso", "perdimos", "perdió", "perdio", "nostalgia", "abandono",
    ],
    "Miedo": [
        "miedo", "temor", "terror", "inseguro", "inseguridad", "peligro", "riesgo",
        "preocupa", "preocupado", "incertidumbre", "incertidumbre", "zozobra",
    ],
    "Sorpresa": [
        "sorprende", "sorprendente", "increible", "increíble", "wow", "impresionante",
        "inesperado", "no lo creo", "impactante", "shock", "asombro",
    ],
}


class EmotionAnalyzer:
    """Detector de emociones por léxico con scoring ponderado."""

    def predict(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return "Neutral" if "Neutral" in config.EMOTIONS else config.EMOTIONS[0]
        text_lower = text.lower()
        scores = {}
        for emotion, keywords in EMOTION_LEXICON.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            scores[emotion] = score
        best = max(scores, key=scores.get)
        if scores[best] == 0:
            return "Sorpresa" if "Sorpresa" in config.EMOTIONS else list(config.EMOTIONS)[-1]
        return best

    def predict_with_scores(self, text: str) -> dict[str, float]:
        text_lower = (text or "").lower()
        scores = {}
        total = 0
        for emotion, keywords in EMOTION_LEXICON.items():
            val = sum(1 for kw in keywords if kw in text_lower)
            scores[emotion] = val
            total += val
        if total == 0:
            return {e: 1 / len(config.EMOTIONS) for e in config.EMOTIONS}
        return {e: scores[e] / total for e in config.EMOTIONS}

    def process_dataframe(self, df: pd.DataFrame, text_col: str = "text") -> pd.DataFrame:
        out = df.copy()
        out["emotion"] = out[text_col].fillna("").astype(str).apply(self.predict)
        return out

    def emotion_summary_by_candidate(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or "candidate" not in df.columns:
            return pd.DataFrame()
        filtered = df[df["candidate"].isin(["Keiko Fujimori", "Roberto Sánchez"])]
        if filtered.empty:
            return pd.DataFrame()
        return (
            filtered.groupby(["candidate", "emotion"])
            .size()
            .reset_index(name="count")
        )
