"""Visualizaciones Plotly con tema oscuro profesional."""

from __future__ import annotations

from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import config

COLORS = {
    "Positivo": config.THEME["green"],
    "Negativo": config.THEME["red"],
    "Neutral": "#94a3b8",
    "Keiko Fujimori": config.THEME["red"],
    "Roberto Sánchez": config.THEME["blue"],
    "Alegría": config.THEME["green"],
    "Ira": config.THEME["red"],
    "Tristeza": "#6366f1",
    "Miedo": "#f59e0b",
    "Sorpresa": config.THEME["cyan"],
}

LAYOUT_DEFAULTS = dict(
    paper_bgcolor=config.THEME["background"],
    plot_bgcolor=config.THEME["card"],
    font=dict(color=config.THEME["text"], family="Inter, Segoe UI, sans-serif"),
    margin=dict(l=40, r=40, t=60, b=40),
)


def apply_dark_theme(fig: go.Figure) -> go.Figure:
    fig.update_layout(**LAYOUT_DEFAULTS)
    fig.update_xaxes(gridcolor="rgba(148,163,184,0.15)", zerolinecolor="rgba(148,163,184,0.15)")
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.15)", zerolinecolor="rgba(148,163,184,0.15)")
    return fig


def pie_chart(df: pd.DataFrame, names: str, values: str, title: str) -> go.Figure:
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Sin datos", showarrow=False, font=dict(color=config.THEME["muted"]))
        return apply_dark_theme(fig.update_layout(title=title))
    color_map = {k: COLORS.get(k, config.THEME["cyan"]) for k in df[names].unique()}
    fig = px.pie(df, names=names, values=values, title=title, color=names, color_discrete_map=color_map, hole=0.45)
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return apply_dark_theme(fig)


def bar_chart(df: pd.DataFrame, x: str, y: str, title: str, color: Optional[str] = None) -> go.Figure:
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Sin datos", showarrow=False, font=dict(color=config.THEME["muted"]))
        return apply_dark_theme(fig.update_layout(title=title))
    if color and color in df.columns:
        fig = px.bar(df, x=x, y=y, color=color, title=title, color_discrete_map=COLORS, barmode="group")
    else:
        fig = px.bar(df, x=x, y=y, title=title, color_discrete_sequence=[config.THEME["blue"]])
    return apply_dark_theme(fig)


def timeline_chart(df: pd.DataFrame, date_col: str, value_col: str, color_col: str, title: str) -> go.Figure:
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Sin datos", showarrow=False)
        return apply_dark_theme(fig.update_layout(title=title))
    fig = px.line(df, x=date_col, y=value_col, color=color_col, title=title, color_discrete_map=COLORS, markers=True)
    return apply_dark_theme(fig)


def heatmap(df: pd.DataFrame, title: str) -> go.Figure:
    if df.empty:
        fig = go.Figure()
        return apply_dark_theme(fig.update_layout(title=title))
    fig = px.imshow(df, title=title, color_continuous_scale="Blues", aspect="auto")
    return apply_dark_theme(fig)


def radar_chart(categories: list[str], values: list[float], title: str, name: str = "Score") -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values, theta=categories, fill="toself", name=name, line_color=config.THEME["cyan"]))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, max(values + [100])])),
        title=title,
        **LAYOUT_DEFAULTS,
    )
    return fig


def correlation_matrix(df: pd.DataFrame, columns: list[str], title: str) -> go.Figure:
    if df.empty:
        return apply_dark_theme(go.Figure().update_layout(title=title))
    numeric = df[columns].select_dtypes(include="number")
    if numeric.empty:
        return apply_dark_theme(go.Figure().update_layout(title=title))
    corr = numeric.corr()
    fig = px.imshow(corr, text_auto=".2f", title=title, color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
    return apply_dark_theme(fig)


def sankey_candidate_sentiment(df: pd.DataFrame, title: str) -> go.Figure:
    if df.empty:
        return apply_dark_theme(go.Figure().update_layout(title=title))
    filtered = df[df["candidate"].isin(["Keiko Fujimori", "Roberto Sánchez"])]
    if filtered.empty:
        return apply_dark_theme(go.Figure().update_layout(title=title))
    flow = filtered.groupby(["candidate", "sentiment"]).size().reset_index(name="count")
    candidates = sorted(flow["candidate"].unique())
    sentiments = sorted(flow["sentiment"].unique())
    labels = candidates + sentiments
    source, target, value = [], [], []
    for _, row in flow.iterrows():
        source.append(labels.index(row["candidate"]))
        target.append(labels.index(row["sentiment"]))
        value.append(row["count"])
    fig = go.Figure(data=[go.Sankey(
        node=dict(pad=15, thickness=20, label=labels, color=[COLORS.get(l, config.THEME["blue"]) for l in labels]),
        link=dict(source=source, target=target, value=value, color="rgba(59,130,246,0.4)"),
    )])
    return apply_dark_theme(fig.update_layout(title=title))


def treemap_topics(df: pd.DataFrame, title: str) -> go.Figure:
    if df.empty or "topic" not in df.columns:
        return apply_dark_theme(go.Figure().update_layout(title=title))
    counts = df["topic"].value_counts().reset_index()
    counts.columns = ["topic", "count"]
    fig = px.treemap(counts, path=["topic"], values="count", title=title, color="count", color_continuous_scale="Blues")
    return apply_dark_theme(fig)


def scatter_engagement(df: pd.DataFrame, title: str) -> go.Figure:
    if df.empty:
        return apply_dark_theme(go.Figure().update_layout(title=title))
    fig = px.scatter(
        df, x="likes", y="replies", size="influence_score", color="candidate",
        hover_data=["author", "sentiment"], title=title, color_discrete_map=COLORS,
        size_max=30,
    )
    return apply_dark_theme(fig)


def word_frequency_bar(word_freq: pd.DataFrame, title: str = "Palabras frecuentes") -> go.Figure:
    if word_freq.empty:
        return apply_dark_theme(go.Figure().update_layout(title=title))
    top = word_freq.head(20)
    fig = px.bar(top, x="count", y="word", orientation="h", title=title, color="count", color_continuous_scale="Blues")
    return apply_dark_theme(fig)


def confusion_matrix_plot(matrix: list, labels: list[str], title: str) -> go.Figure:
    fig = px.imshow(matrix, x=labels, y=labels, text_auto=True, title=title, color_continuous_scale="Blues")
    fig.update_layout(xaxis_title="Predicción", yaxis_title="Real")
    return apply_dark_theme(fig)


def kpi_sparkline(dates: list, values: list, title: str) -> go.Figure:
    fig = go.Figure(go.Scatter(x=dates, y=values, mode="lines+markers", line=dict(color=config.THEME["cyan"], width=2)))
    fig.update_layout(title=title, height=200, showlegend=False, **LAYOUT_DEFAULTS)
    return fig
