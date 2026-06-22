"""
Plataforma Profesional de Análisis de Sentimientos Electorales
Segunda Vuelta Presidencial Perú 2026 - Keiko Fujimori vs Roberto Sánchez
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd

import config
from src.analytics.metrics import PoliticalAnalytics
from src.dashboard.components import (
    render_bots_tab,
    render_candidate_analysis,
    render_emotion_tab,
    render_executive_summary,
    render_explorer_tab,
    render_general_dashboard,
    render_ml_tab,
    render_prediction_tab,
    render_reports_tab,
    render_sentiment_tab,
    render_timeline_tab,
    render_topic_tab,
)
from src.dashboard.styles import CUSTOM_CSS
from src.database.manager import DatabaseManager
from src.ml.pipeline import NLPipeline
from src.scraping.youtube_scraper import DataImporter, YouTubeScraper
from src.utils.helpers import logger
from src.utils.seed_data import generate_sample_dataframe

st.set_page_config(
    page_title="Electoral Intelligence Platform | Perú 2026",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


@st.cache_resource
def get_database() -> DatabaseManager:
    return DatabaseManager()


@st.cache_resource
def get_pipeline(sentiment_mode: str) -> NLPipeline:
    return NLPipeline(sentiment_mode=sentiment_mode)


@st.cache_data(ttl=300)
def load_comments() -> pd.DataFrame:
    db = get_database()
    return db.get_all_comments()


def process_and_save(df: pd.DataFrame, sentiment_mode: str) -> pd.DataFrame:
    if df.empty:
        return df
    pipeline = get_pipeline(sentiment_mode)
    processed = pipeline.run(df)
    db = get_database()
    db.dataframe_to_db(processed)
    load_comments.clear()
    return processed


def main():
    st.sidebar.markdown("## 🗳️ Electoral Intelligence")
    st.sidebar.markdown("**Segunda Vuelta Perú 2026**")
    st.sidebar.markdown("Keiko Fujimori vs Roberto Sánchez")
    st.sidebar.markdown("---")

    sentiment_mode = st.sidebar.selectbox(
        "Modo de Sentimiento",
        config.SENTIMENT_MODES,
        index=0,
    )

    st.sidebar.subheader("📥 Ingesta de Datos")
    data_source = st.sidebar.radio(
        "Fuente",
        ["Base de datos", "Demo", "YouTube URL", "Búsqueda YouTube", "CSV/Excel"],
    )

    if data_source == "Demo":
        if st.sidebar.button("Cargar datos demo"):
            raw = generate_sample_dataframe(30)
            with st.spinner("Procesando NLP..."):
                process_and_save(raw, sentiment_mode)
            st.sidebar.success(f"{len(raw)} comentarios demo cargados.")

    elif data_source == "YouTube URL":
        url = st.sidebar.text_input("URL de YouTube", placeholder="https://www.youtube.com/watch?v=...")
        if st.sidebar.button("Extraer comentarios"):
            scraper = YouTubeScraper()
            if not scraper.is_available:
                st.sidebar.error("Configure YOUTUBE_API_KEY en variables de entorno.")
            else:
                raw = scraper.scrape_url(url)
                if raw.empty:
                    st.sidebar.warning("No se obtuvieron comentarios.")
                else:
                    with st.spinner("Procesando..."):
                        process_and_save(raw, sentiment_mode)
                    st.sidebar.success(f"{len(raw)} comentarios extraídos.")

    elif data_source == "Búsqueda YouTube":
        keywords = st.sidebar.text_area("Palabras clave (una por línea)", "\n".join(config.DEFAULT_SEARCH_QUERIES[:3]))
        if st.sidebar.button("Buscar y extraer"):
            scraper = YouTubeScraper()
            if not scraper.is_available:
                st.sidebar.error("Configure YOUTUBE_API_KEY.")
            else:
                queries = [q.strip() for q in keywords.split("\n") if q.strip()]
                raw = scraper.scrape_keywords(queries)
                if raw.empty:
                    st.sidebar.warning("Sin resultados.")
                else:
                    with st.spinner("Procesando..."):
                        process_and_save(raw, sentiment_mode)
                    st.sidebar.success(f"{len(raw)} comentarios extraídos.")

    elif data_source == "CSV/Excel":
        uploaded = st.sidebar.file_uploader("Subir archivo", type=["csv", "xlsx"])
        if uploaded and st.sidebar.button("Importar"):
            if uploaded.name.endswith(".csv"):
                raw = pd.read_csv(uploaded)
            else:
                raw = pd.read_excel(uploaded)
            raw["source"] = "upload"
            with st.spinner("Procesando..."):
                process_and_save(raw, sentiment_mode)
            st.sidebar.success(f"{len(raw)} registros importados.")

    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Actualizar datos"):
        load_comments.clear()
        st.rerun()

    if st.sidebar.button("🗑️ Limpiar base de datos"):
        get_database().delete_all()
        load_comments.clear()
        st.sidebar.warning("Base de datos limpiada.")
        st.rerun()

    df = load_comments()

    st.markdown('<div class="hero-title">Electoral Intelligence Platform</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Análisis de sentimientos y analítica política digital · Segunda Vuelta Presidencial Perú 2026</div>',
        unsafe_allow_html=True,
    )

    if df.empty:
        st.info("👆 Cargue datos demo o conecte YouTube API desde la barra lateral para comenzar.")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Inicio rápido")
            st.markdown("""
            1. Seleccione **Demo** en la barra lateral
            2. Pulse **Cargar datos demo**
            3. Explore las 13 pestañas de análisis
            """)
        with col2:
            st.markdown("### YouTube API")
            st.markdown("""
            Configure la variable de entorno:
            ```
            YOUTUBE_API_KEY=su_clave_aqui
            ```
            """)
        return

    analytics = PoliticalAnalytics(df)
    pipeline = get_pipeline(sentiment_mode)

    tabs = st.tabs([
        "📋 Resumen Ejecutivo",
        "📊 Dashboard General",
        "🔴 Keiko Fujimori",
        "🔵 Roberto Sánchez",
        "💬 Sentimientos",
        "😊 Emociones",
        "📚 Temas",
        "📅 Timeline",
        "🤖 Bots",
        "🧠 Machine Learning",
        "🔍 Explorador",
        "⚡ Predicción",
        "📄 Reportes",
    ])

    with tabs[0]:
        render_executive_summary(analytics, df)
    with tabs[1]:
        render_general_dashboard(analytics, df)
    with tabs[2]:
        render_candidate_analysis(analytics, df, "Keiko Fujimori")
    with tabs[3]:
        render_candidate_analysis(analytics, df, "Roberto Sánchez")
    with tabs[4]:
        render_sentiment_tab(analytics, df)
    with tabs[5]:
        render_emotion_tab(analytics, df)
    with tabs[6]:
        render_topic_tab(analytics, df)
    with tabs[7]:
        render_timeline_tab(analytics, df)
    with tabs[8]:
        render_bots_tab(df)
    with tabs[9]:
        render_ml_tab(df)
    with tabs[10]:
        render_explorer_tab(df)
    with tabs[11]:
        render_prediction_tab(pipeline)
    with tabs[12]:
        render_reports_tab(df)

    st.sidebar.markdown("---")
    st.sidebar.metric("Comentarios en BD", len(df))
    st.sidebar.caption(f"Backend: {pipeline.sentiment.active_backend}")


if __name__ == "__main__":
    main()
