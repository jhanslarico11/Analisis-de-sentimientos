"""Métricas políticas y analítica avanzada."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

import config
from src.utils.helpers import normalize_dates


class PoliticalAnalytics:
    """Calculadora de KPIs políticos y conclusiones automáticas."""

    CANDIDATES = ["Keiko Fujimori", "Roberto Sánchez"]

    def __init__(self, df: pd.DataFrame):
        self.df = normalize_dates(df.copy() if df is not None else pd.DataFrame(), "date")

    def _candidate_df(self, candidate: str) -> pd.DataFrame:
        if self.df.empty:
            return self.df
        return self.df[self.df["candidate"] == candidate]

    def share_of_voice(self) -> pd.DataFrame:
        if self.df.empty:
            return pd.DataFrame({"candidate": self.CANDIDATES, "mentions": [0, 0], "share_pct": [0.0, 0.0]})
        counts = self.df["candidate"].value_counts()
        keiko = int(counts.get("Keiko Fujimori", 0))
        roberto = int(counts.get("Roberto Sánchez", 0))
        both = int(counts.get("Ambos", 0))
        keiko += both // 2
        roberto += both // 2
        total = keiko + roberto or 1
        return pd.DataFrame({
            "candidate": self.CANDIDATES,
            "mentions": [keiko, roberto],
            "share_pct": [round(keiko / total * 100, 1), round(roberto / total * 100, 1)],
        })

    def popularity(self) -> pd.DataFrame:
        rows = []
        for cand in self.CANDIDATES:
            sub = self._candidate_df(cand)
            total = len(sub) or 1
            positive = len(sub[sub["sentiment"] == "Positivo"])
            rows.append({
                "candidate": cand,
                "popularity_pct": round(positive / total * 100, 1),
                "positive_count": positive,
                "total": len(sub),
            })
        return pd.DataFrame(rows)

    def rejection(self) -> pd.DataFrame:
        rows = []
        for cand in self.CANDIDATES:
            sub = self._candidate_df(cand)
            total = len(sub) or 1
            negative = len(sub[sub["sentiment"] == "Negativo"])
            rows.append({
                "candidate": cand,
                "rejection_pct": round(negative / total * 100, 1),
                "negative_count": negative,
                "total": len(sub),
            })
        return pd.DataFrame(rows)

    def engagement_score(self) -> pd.DataFrame:
        rows = []
        for cand in self.CANDIDATES:
            sub = self._candidate_df(cand)
            likes = sub["likes"].sum() if not sub.empty else 0
            replies = sub["replies"].sum() if not sub.empty else 0
            score = np.log1p(likes) + np.log1p(replies) * 1.5
            rows.append({
                "candidate": cand,
                "total_likes": int(likes),
                "total_replies": int(replies),
                "engagement_score": round(float(score), 2),
            })
        return pd.DataFrame(rows)

    def polarization_index(self) -> float:
        if self.df.empty:
            return 0.0
        pos = len(self.df[self.df["sentiment"] == "Positivo"])
        neg = len(self.df[self.df["sentiment"] == "Negativo"])
        total = pos + neg or 1
        balance = abs(pos - neg) / total
        return round(balance * 100, 1)

    def proposal_impact_index(self) -> pd.DataFrame:
        if self.df.empty:
            return pd.DataFrame()
        proposal_keywords = ["propuesta", "plan", "programa", "promete", "ofrece", "medida"]
        mask = self.df["text"].fillna("").str.lower().apply(
            lambda t: any(k in t for k in proposal_keywords)
        )
        sub = self.df[mask]
        if sub.empty:
            return pd.DataFrame({"candidate": self.CANDIDATES, "impact_score": [0.0, 0.0]})
        rows = []
        for cand in self.CANDIDATES:
            csub = sub[sub["candidate"] == cand]
            impact = csub["influence_score"].sum() + csub["likes"].sum() * 0.01
            rows.append({"candidate": cand, "impact_score": round(float(impact), 2), "proposal_mentions": len(csub)})
        return pd.DataFrame(rows)

    def debate_winner_index(self) -> dict[str, Any]:
        pop = self.popularity()
        eng = self.engagement_score()
        rej = self.rejection()
        if pop.empty:
            return {"winner": "Sin datos", "scores": {}}
        scores = {}
        for cand in self.CANDIDATES:
            pop_val = pop.loc[pop["candidate"] == cand, "popularity_pct"].values
            eng_val = eng.loc[eng["candidate"] == cand, "engagement_score"].values
            rej_val = rej.loc[rej["candidate"] == cand, "rejection_pct"].values
            pop_v = pop_val[0] if len(pop_val) else 0
            eng_v = eng_val[0] if len(eng_val) else 0
            rej_v = rej_val[0] if len(rej_val) else 0
            scores[cand] = round(pop_v * 0.4 + eng_v * 0.3 - rej_v * 0.3, 2)
        winner = max(scores, key=scores.get)
        return {"winner": winner, "scores": scores}

    def influence_index(self) -> pd.DataFrame:
        if self.df.empty:
            return pd.DataFrame()
        return (
            self.df.groupby("candidate")["influence_score"]
            .agg(["mean", "sum", "max"])
            .reset_index()
            .rename(columns={"mean": "avg_influence", "sum": "total_influence", "max": "max_influence"})
        )

    def trend_index(self) -> pd.DataFrame:
        if self.df.empty or "date" not in self.df.columns:
            return pd.DataFrame()
        df = self.df.dropna(subset=["date"]).copy()
        if df.empty:
            return pd.DataFrame()
        df["week"] = df["date"].dt.to_period("W").astype(str)
        trend = df.groupby(["week", "candidate"]).size().reset_index(name="mentions")
        return trend

    def emotion_by_candidate(self) -> pd.DataFrame:
        if self.df.empty:
            return pd.DataFrame()
        return (
            self.df[self.df["candidate"].isin(self.CANDIDATES)]
            .groupby(["candidate", "emotion"])
            .size()
            .reset_index(name="count")
        )

    def topic_distribution(self) -> pd.DataFrame:
        if self.df.empty:
            return pd.DataFrame(columns=["topic", "count"])
        result = self.df["topic"].value_counts().reset_index()
        result.columns = ["topic", "count"]
        return result

    def temporal_analysis(self, freq: str = "D") -> pd.DataFrame:
        if self.df.empty or "date" not in self.df.columns:
            return pd.DataFrame()
        df = self.df.dropna(subset=["date"]).copy()
        if df.empty:
            return pd.DataFrame()
        grouped = df.set_index("date").groupby([pd.Grouper(freq=freq), "candidate"]).size()
        return grouped.reset_index(name="count")

    def top_influential(self, n: int = 10) -> pd.DataFrame:
        if self.df.empty:
            return pd.DataFrame()
        return self.df.nlargest(n, "influence_score")

    def generate_conclusions(self) -> dict[str, str]:
        if self.df.empty:
            return {"summary": "No hay datos disponibles para generar conclusiones."}

        sov = self.share_of_voice()
        pop = self.popularity()
        rej = self.rejection()
        debate = self.debate_winner_index()

        most_mentioned = sov.loc[sov["mentions"].idxmax(), "candidate"] if not sov.empty else "N/A"
        best_valued = pop.loc[pop["popularity_pct"].idxmax(), "candidate"] if not pop.empty else "N/A"
        most_rejected = rej.loc[rej["rejection_pct"].idxmax(), "candidate"] if not rej.empty else "N/A"

        dominant_emotion = self.df["emotion"].mode().iloc[0] if "emotion" in self.df.columns and not self.df.empty else "N/A"
        dominant_topic = self.df["topic"].mode().iloc[0] if "topic" in self.df.columns and not self.df.empty else "N/A"
        debate_winner = debate.get("winner", "N/A")
        polarization = self.polarization_index()

        summary = (
            f"Candidato más mencionado: {most_mentioned}. "
            f"Mejor valoración digital: {best_valued}. "
            f"Mayor rechazo: {most_rejected}. "
            f"Emoción dominante: {dominant_emotion}. "
            f"Tema predominante: {dominant_topic}. "
            f"Ganador digital del debate: {debate_winner}. "
            f"Índice de polarización: {polarization}%."
        )
        return {
            "most_mentioned": most_mentioned,
            "best_valued": best_valued,
            "most_rejected": most_rejected,
            "dominant_emotion": dominant_emotion,
            "dominant_topic": dominant_topic,
            "debate_winner": debate_winner,
            "polarization": str(polarization),
            "summary": summary,
        }

    def all_metrics(self) -> dict[str, Any]:
        return {
            "share_of_voice": self.share_of_voice(),
            "popularity": self.popularity(),
            "rejection": self.rejection(),
            "engagement": self.engagement_score(),
            "polarization": self.polarization_index(),
            "proposal_impact": self.proposal_impact_index(),
            "debate_winner": self.debate_winner_index(),
            "influence": self.influence_index(),
            "trend": self.trend_index(),
            "emotions": self.emotion_by_candidate(),
            "topics": self.topic_distribution(),
            "conclusions": self.generate_conclusions(),
        }
