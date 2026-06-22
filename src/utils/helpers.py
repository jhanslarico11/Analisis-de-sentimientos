"""Utilidades generales de la plataforma."""

from __future__ import annotations

import hashlib
import logging
import re
from datetime import datetime
from typing import Any, Optional

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("sentiment_platform")


def safe_datetime(value: Any) -> Optional[pd.Timestamp]:
    """Convierte fechas de forma segura eliminando timezone."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    try:
        dt = pd.to_datetime(value, errors="coerce", utc=True)
        if pd.isna(dt):
            return None
        return dt.tz_localize(None) if dt.tzinfo else dt
    except Exception:
        return None


def normalize_dates(df: pd.DataFrame, column: str = "date") -> pd.DataFrame:
    """Normaliza columna de fechas evitando errores UTC."""
    if column not in df.columns or df.empty:
        return df
    out = df.copy()
    out[column] = pd.to_datetime(out[column], errors="coerce", utc=True)
    out[column] = out[column].dt.tz_localize(None)
    return out


def extract_youtube_video_id(url: str) -> Optional[str]:
    """Extrae video ID de una URL de YouTube."""
    if not url:
        return None
    patterns = [
        r"(?:v=|/videos/|embed/|youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def generate_comment_id(text: str, author: str, video_id: str) -> str:
    """Genera ID único para comentarios sin ID externo."""
    raw = f"{text}|{author}|{video_id}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def format_number(value: float, decimals: int = 1) -> str:
    if value >= 1_000_000:
        return f"{value / 1_000_000:.{decimals}f}M"
    if value >= 1_000:
        return f"{value / 1_000:.{decimals}f}K"
    return f"{value:.{decimals}f}"


def pct(value: float) -> str:
    return f"{value:.1f}%"


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in columns:
        if col not in out.columns:
            out[col] = None
    return out
