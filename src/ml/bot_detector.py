"""Detección de bots, spam y actividad sospechosa."""

from __future__ import annotations

import pandas as pd

from src.utils.helpers import clamp


class BotDetector:
    """Detector heurístico de bots y spam."""

    def compute_bot_probability(self, row: pd.Series, duplicate_ratio: float = 0.0) -> float:
        score = 0.0
        text = str(row.get("text", ""))
        author = str(row.get("author", ""))
        likes = int(row.get("likes", 0) or 0)
        replies = int(row.get("replies", 0) or 0)

        if len(text) < 10:
            score += 0.15
        if text == text.upper() and len(text) > 20:
            score += 0.2
        if "http" in text.lower():
            score += 0.15
        if likes == 0 and replies == 0 and len(text) > 50:
            score += 0.1
        if any(c in author.lower() for c in ["bot", "spam", "promo"]):
            score += 0.3
        if duplicate_ratio > 0.5:
            score += 0.25
        if text.count("!") > 5:
            score += 0.1
        return clamp(score)

    def detect_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        out = df.copy()
        text_counts = out["text"].fillna("").astype(str).value_counts()
        out["is_duplicate"] = out["text"].fillna("").astype(str).map(lambda t: text_counts.get(t, 0) > 1)
        return out

    def detect_repetitive_users(self, df: pd.DataFrame, threshold: int = 5) -> pd.DataFrame:
        if df.empty:
            return df
        out = df.copy()
        author_counts = out["author"].fillna("Anónimo").value_counts()
        out["is_repetitive_user"] = out["author"].fillna("Anónimo").map(lambda a: author_counts.get(a, 0) >= threshold)
        return out

    def process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        out = self.detect_duplicates(df)
        out = self.detect_repetitive_users(out)
        dup_ratio = out["is_duplicate"].mean() if "is_duplicate" in out.columns else 0
        out["bot_probability"] = out.apply(
            lambda r: self.compute_bot_probability(r, duplicate_ratio=dup_ratio),
            axis=1,
        )
        out["is_suspicious"] = out["bot_probability"] >= 0.6
        return out

    def activity_summary(self, df: pd.DataFrame) -> dict:
        if df.empty:
            return {"organic_pct": 100.0, "suspicious_pct": 0.0, "duplicates": 0, "repetitive_users": 0}
        processed = self.process_dataframe(df)
        suspicious = processed["is_suspicious"].sum()
        total = len(processed)
        return {
            "organic_pct": round((total - suspicious) / total * 100, 1) if total else 100.0,
            "suspicious_pct": round(suspicious / total * 100, 1) if total else 0.0,
            "duplicates": int(processed.get("is_duplicate", pd.Series(dtype=bool)).sum()),
            "repetitive_users": int(processed.get("is_repetitive_user", pd.Series(dtype=bool)).sum()),
            "suspicious_count": int(suspicious),
            "total": total,
        }
