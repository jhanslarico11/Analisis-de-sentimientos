"""Cálculo de influence score."""

from __future__ import annotations

import math

import pandas as pd

from src.utils.helpers import clamp


def compute_influence_score(row: pd.Series) -> float:
    likes = int(row.get("likes", 0) or 0)
    replies = int(row.get("replies", 0) or 0)
    text_len = len(str(row.get("text", "")))
    length_factor = min(1.0, text_len / 300)
    engagement = math.log1p(likes) * 2 + math.log1p(replies) * 3
    score = engagement * (0.5 + 0.5 * length_factor)
    return round(clamp(score / 20), 4)


class InfluenceCalculator:
    def process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out["influence_score"] = out.apply(compute_influence_score, axis=1)
        return out.sort_values("influence_score", ascending=False)
