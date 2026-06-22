"""Detección automática de candidatos en comentarios."""

from __future__ import annotations

import re
import unicodedata
from typing import Optional

import pandas as pd

import config


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    return text.encode("ascii", "ignore").decode("utf-8")


def _contains_alias(text: str, alias: str) -> bool:
    alias_norm = _normalize(alias)
    if " " in alias_norm:
        return alias_norm in text
    return re.search(rf"\b{re.escape(alias_norm)}\b", text) is not None


def detect_candidate(text: Optional[str]) -> str:
    """Clasifica comentario: Keiko Fujimori, Roberto Sánchez, Ambos o Ninguno."""
    if not text or not isinstance(text, str):
        return "Ninguno"

    normalized = _normalize(text)
    keiko_match = any(_contains_alias(normalized, a) for a in config.CANDIDATES["keiko"]["aliases"])
    roberto_match = any(_contains_alias(normalized, a) for a in config.CANDIDATES["roberto"]["aliases"])

    if keiko_match and roberto_match:
        return "Ambos"
    if keiko_match:
        return "Keiko Fujimori"
    if roberto_match:
        return "Roberto Sánchez"
    return "Ninguno"


def classify_political(text: str, candidate: str, sentiment: str) -> str:
    """Clasificación política basada en candidato + sentimiento."""
    if candidate == "Ninguno" or sentiment == "Neutral":
        return "Neutral"
    if candidate == "Ambos":
        return "Neutral"

    if candidate == "Keiko Fujimori":
        if sentiment == "Positivo":
            return "Apoya a Keiko"
        if sentiment == "Negativo":
            return "Critica a Keiko"
    elif candidate == "Roberto Sánchez":
        if sentiment == "Positivo":
            return "Apoya a Roberto"
        if sentiment == "Negativo":
            return "Critica a Roberto"
    return "Neutral"


class CandidateDetector:
    """Detector batch para DataFrames."""

    def predict(self, text: str) -> str:
        return detect_candidate(text)

    def process_dataframe(self, df: pd.DataFrame, text_col: str = "text") -> pd.DataFrame:
        out = df.copy()
        out["candidate"] = out[text_col].fillna("").astype(str).apply(detect_candidate)
        if "sentiment" in out.columns:
            out["political_classification"] = out.apply(
                lambda r: classify_political(
                    str(r.get(text_col, "")),
                    str(r.get("candidate", "Ninguno")),
                    str(r.get("sentiment", "Neutral")),
                ),
                axis=1,
            )
        return out
