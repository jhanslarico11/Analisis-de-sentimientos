"""Componentes reutilizables del dashboard."""

from __future__ import annotations

import streamlit as st
import pandas as pd

from src.analytics.metrics import PoliticalAnalytics
from src.dashboard.styles import render_kpi_card
from src.visualization.charts import (
    bar_chart,
    correlation_matrix,
    pie_chart,
    radar_chart,
    sankey_candidate_sentiment,
    scatter_engagement,
    timeline_chart,
    treemap_topics,
    word_frequency_bar,
)
from src.visualization.wordcloud_gen import extract_word_frequencies


def render_kpi_row(analytics: PoliticalAnalytics, df: pd.DataFrame):
    conclusions = analytics.generate_conclusions()
    cols = st.columns(4)
    with cols[0]:
        st.markdown(render_kpi_card("Total Comentarios", str(len(df)), "Base analizada"), unsafe_allow_html=True)
    with cols[1]:
        val = conclusions.get("most_mentioned", "N/A")
        st.markdown(render_kpi_card("Share of Voice", val, "Más mencionado", "neutral"), unsafe_allow_html=True)
    with cols[2]:
        val = conclusions.get("debate_winner", "N/A")
        st.markdown(render_kpi_card("Ganador Digital", val, "Debate Winner Index", "positive"), unsafe_allow_html=True)
    with cols[3]:
        pol = analytics.polarization_index()
        st.markdown(render_kpi_card("Polarización", f"{pol}%", "Índice de polarización", "negative"), unsafe_allow_html=True)


def render_executive_summary(analytics: PoliticalAnalytics, df: pd.DataFrame):
    conclusions = analytics.generate_conclusions()
    render_kpi_row(analytics, df)
    st.markdown(
        f'<div class="conclusion-box"><strong>Conclusión automática:</strong> {conclusions["summary"]}</div>',
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)
    sov = analytics.share_of_voice()
    pop = analytics.popularity()
    with col1:
        if not sov.empty:
            st.plotly_chart(pie_chart(sov, "candidate", "mentions", "Share of Voice"), use_container_width=True)
    with col2:
        if not pop.empty:
            st.plotly_chart(bar_chart(pop, "candidate", "popularity_pct", "Popularidad Digital (%)", "candidate"), use_container_width=True)
    debate = analytics.debate_winner_index()
    if debate.get("scores"):
        scores_df = pd.DataFrame(list(debate["scores"].items()), columns=["candidate", "score"])
        st.plotly_chart(bar_chart(scores_df, "candidate", "score", "Debate Winner Index"), use_container_width=True)


def render_general_dashboard(analytics: PoliticalAnalytics, df: pd.DataFrame):
    col1, col2, col3 = st.columns(3)
    with col1:
        sent_counts = df["sentiment"].value_counts().reset_index()
        sent_counts.columns = ["sentiment", "count"]
        st.plotly_chart(pie_chart(sent_counts, "sentiment", "count", "Distribución de Sentimientos"), use_container_width=True)
    with col2:
        sov = analytics.share_of_voice()
        st.plotly_chart(bar_chart(sov, "candidate", "share_pct", "Share of Voice (%)"), use_container_width=True)
    with col3:
        rej = analytics.rejection()
        st.plotly_chart(bar_chart(rej, "candidate", "rejection_pct", "Rechazo (%)"), use_container_width=True)
    st.plotly_chart(sankey_candidate_sentiment(df, "Flujo Candidato → Sentimiento"), use_container_width=True)
    st.plotly_chart(scatter_engagement(df, "Engagement: Likes vs Respuestas"), use_container_width=True)


def render_candidate_analysis(analytics: PoliticalAnalytics, df: pd.DataFrame, candidate: str):
    sub = df[df["candidate"] == candidate]
    if sub.empty:
        st.warning(f"No hay comentarios para {candidate}.")
        return
    pop = len(sub[sub["sentiment"] == "Positivo"])
    neg = len(sub[sub["sentiment"] == "Negativo"])
    cols = st.columns(4)
    cols[0].metric("Menciones", len(sub))
    cols[1].metric("Positivos", pop)
    cols[2].metric("Negativos", neg)
    cols[3].metric("Engagement", int(sub["likes"].sum()))
    col1, col2 = st.columns(2)
    with col1:
        sc = sub["sentiment"].value_counts().reset_index()
        sc.columns = ["sentiment", "count"]
        st.plotly_chart(pie_chart(sc, "sentiment", "count", f"Sentimientos - {candidate}"), use_container_width=True)
    with col2:
        ec = sub["emotion"].value_counts().reset_index()
        ec.columns = ["emotion", "count"]
        st.plotly_chart(bar_chart(ec, "emotion", "count", f"Emociones - {candidate}"), use_container_width=True)
    st.plotly_chart(treemap_topics(sub, f"Temas - {candidate}"), use_container_width=True)
    wf = extract_word_frequencies(sub["clean_text"].tolist())
    st.plotly_chart(word_frequency_bar(wf, f"Palabras clave - {candidate}"), use_container_width=True)


def render_sentiment_tab(analytics: PoliticalAnalytics, df: pd.DataFrame):
    col1, col2 = st.columns(2)
    with col1:
        sc = df["sentiment"].value_counts().reset_index()
        sc.columns = ["sentiment", "count"]
        st.plotly_chart(pie_chart(sc, "sentiment", "count", "Sentimientos Globales"), use_container_width=True)
    with col2:
        pc = df["political_classification"].value_counts().reset_index()
        pc.columns = ["political_classification", "count"]
        st.plotly_chart(bar_chart(pc, "political_classification", "count", "Clasificación Política"), use_container_width=True)
    if "sentiment_score" in df.columns:
        st.plotly_chart(
            correlation_matrix(df, ["likes", "replies", "sentiment_score", "influence_score"], "Matriz de Correlación"),
            use_container_width=True,
        )


def render_emotion_tab(analytics: PoliticalAnalytics, df: pd.DataFrame):
    col1, col2 = st.columns(2)
    with col1:
        ec = df["emotion"].value_counts().reset_index()
        ec.columns = ["emotion", "count"]
        st.plotly_chart(pie_chart(ec, "emotion", "count", "Emociones Globales"), use_container_width=True)
    with col2:
        ebc = analytics.emotion_by_candidate()
        if not ebc.empty:
            st.plotly_chart(bar_chart(ebc, "emotion", "count", "Emociones por Candidato", "candidate"), use_container_width=True)
    for candidate in ["Keiko Fujimori", "Roberto Sánchez"]:
        sub = df[df["candidate"] == candidate]
        if sub.empty:
            continue
        emo_counts = sub["emotion"].value_counts()
        values = [emo_counts.get(e, 0) for e in ["Alegría", "Ira", "Tristeza", "Miedo", "Sorpresa"]]
        st.plotly_chart(
            radar_chart(["Alegría", "Ira", "Tristeza", "Miedo", "Sorpresa"], values, f"Radar Emocional - {candidate}", candidate),
            use_container_width=True,
        )


def render_topic_tab(analytics: PoliticalAnalytics, df: pd.DataFrame):
    topics = analytics.topic_distribution()
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(treemap_topics(df, "Mapa de Temas"), use_container_width=True)
    with col2:
        if not topics.empty:
            st.plotly_chart(bar_chart(topics, "topic", "count", "Frecuencia Temática"), use_container_width=True)
    from src.topic_modeling.analyzer import TopicAnalyzer
    emergent = TopicAnalyzer().get_emergent(df)
    if not emergent.empty:
        st.subheader("Temas Emergentes (LDA)")
        st.dataframe(emergent, use_container_width=True)


def render_timeline_tab(analytics: PoliticalAnalytics, df: pd.DataFrame):
    freq = st.radio("Granularidad", ["Hora", "Día", "Semana"], horizontal=True)
    freq_map = {"Hora": "H", "Día": "D", "Semana": "W"}
    temporal = analytics.temporal_analysis(freq_map[freq])
    if not temporal.empty:
        st.plotly_chart(timeline_chart(temporal, "date", "count", "candidate", f"Timeline ({freq})"), use_container_width=True)
    if "date" in df.columns and not df["date"].isna().all():
        daily = df.dropna(subset=["date"]).set_index("date").resample("D").size().reset_index(name="count")
        if not daily.empty:
            peak = daily.loc[daily["count"].idxmax()]
            st.info(f"Pico de conversación: {peak['date'].strftime('%Y-%m-%d')} con {peak['count']} comentarios.")


def render_bots_tab(df: pd.DataFrame):
    from src.ml.bot_detector import BotDetector
    detector = BotDetector()
    summary = detector.activity_summary(df)
    cols = st.columns(4)
    cols[0].metric("Actividad Orgánica", f"{summary['organic_pct']}%")
    cols[1].metric("Actividad Sospechosa", f"{summary['suspicious_pct']}%")
    cols[2].metric("Duplicados", summary["duplicates"])
    cols[3].metric("Usuarios Repetitivos", summary["repetitive_users"])
    processed = detector.process_dataframe(df)
    suspicious = processed[processed["is_suspicious"]].head(20)
    st.subheader("Comentarios Sospechosos")
    st.dataframe(suspicious[["author", "text", "bot_probability", "likes", "replies"]], use_container_width=True)


def render_ml_tab(df: pd.DataFrame):
    from src.sentiment.analyzer import evaluate_sentiment_models
    from src.visualization.charts import confusion_matrix_plot
    st.subheader("Evaluación de Modelos de Sentimiento")
    eval_texts = df["clean_text"].fillna("").head(20).tolist()
    eval_labels = df["sentiment"].head(20).tolist()
    if len(eval_texts) >= 3:
        results = evaluate_sentiment_models(eval_texts, eval_labels)
        display = results[["model", "accuracy", "precision", "recall", "f1", "support"]].copy()
        st.dataframe(display, use_container_width=True)
        best = results.loc[results["f1"].idxmax()]
        st.success(f"Mejor modelo: **{best['model']}** (F1: {best['f1']:.3f}, Accuracy: {best['accuracy']:.3f})")
        labels = sorted(set(eval_labels))
        st.plotly_chart(confusion_matrix_plot(best["confusion_matrix"], labels, f"Matriz de Confusión - {best['model']}"), use_container_width=True)
    else:
        st.warning("Se necesitan más datos para evaluar modelos.")


def render_explorer_tab(df: pd.DataFrame):
    st.subheader("Explorador de Comentarios")
    col1, col2, col3 = st.columns(3)
    with col1:
        cand_filter = st.multiselect("Candidato", df["candidate"].unique().tolist(), default=[])
    with col2:
        sent_filter = st.multiselect("Sentimiento", df["sentiment"].unique().tolist(), default=[])
    with col3:
        topic_filter = st.multiselect("Tema", df["topic"].unique().tolist(), default=[])
    filtered = df.copy()
    if cand_filter:
        filtered = filtered[filtered["candidate"].isin(cand_filter)]
    if sent_filter:
        filtered = filtered[filtered["sentiment"].isin(sent_filter)]
    if topic_filter:
        filtered = filtered[filtered["topic"].isin(topic_filter)]
    sort_by = st.selectbox("Ordenar por", ["influence_score", "likes", "date", "sentiment_score"])
    filtered = filtered.sort_values(sort_by, ascending=False)
    st.dataframe(filtered[["date", "author", "candidate", "sentiment", "emotion", "topic", "likes", "text"]], use_container_width=True, height=400)


def render_prediction_tab(pipeline):
    st.subheader("Predicción en Tiempo Real")
    text = st.text_area("Ingrese un comentario para analizar", value="Keiko presentó mejores propuestas económicas", height=100)
    if st.button("Analizar", type="primary"):
        result = pipeline.predict_single(text)
        cols = st.columns(5)
        cols[0].metric("Sentimiento", result["sentiment"])
        cols[1].metric("Score", f"{result['sentiment_score']:.2f}")
        cols[2].metric("Candidato", result["candidate"])
        cols[3].metric("Emoción", result["emotion"])
        cols[4].metric("Tema", result["topic"])
        st.info(f"Clasificación política: **{result['political_classification']}**")


def render_reports_tab(df: pd.DataFrame):
    from src.reporting.generator import ReportGenerator
    st.subheader("Generación de Reportes")
    col1, col2, col3, col4 = st.columns(4)
    generator = ReportGenerator(df)
    if col1.button("Exportar CSV"):
        st.success(f"CSV generado: {generator.to_csv()}")
    if col2.button("Exportar Excel"):
        st.success(f"Excel generado: {generator.to_excel()}")
    if col3.button("Exportar Markdown"):
        st.success(f"Markdown generado: {generator.to_markdown()}")
    if col4.button("Exportar PDF"):
        st.success(f"Reporte generado: {generator.to_pdf()}")
    st.markdown(f'<div class="conclusion-box">{generator.conclusions.get("summary", "")}</div>', unsafe_allow_html=True)
