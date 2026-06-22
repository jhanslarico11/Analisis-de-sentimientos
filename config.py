"""Configuración central de la plataforma de análisis electoral."""

from __future__ import annotations

import os
from pathlib import Path

# Rutas base
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"
DB_PATH = DATA_DIR / "sentiment_platform.db"

# Crear directorios necesarios
for _dir in (DATA_DIR, MODELS_DIR, REPORTS_DIR, PROJECT_ROOT / "tests", PROJECT_ROOT / "notebooks"):
    _dir.mkdir(parents=True, exist_ok=True)

# YouTube API
YOUTUBE_API_KEY = "AIzaSyDdhkGkx7hDn8MWsaVFr4S1hqrCNyDg_Yo"

# Candidatos
CANDIDATES = {
    "keiko": {
        "name": "Keiko Fujimori",
        "aliases": ["keiko", "fujimori", "fuerza popular", "fp", "la hija del dictador"],
        "color": "#ff4444",
    },
    "roberto": {
        "name": "Roberto Sánchez",
        "aliases": ["roberto", "sanchez", "sánchez", "roberto sanchez", "roberto sánchez", "juntos por el peru", "jpp"],
        "color": "#3b82f6",
    },
}

CANDIDATE_LABELS = ["Keiko Fujimori", "Roberto Sánchez", "Ambos", "Ninguno"]

# Sentimientos y emociones
SENTIMENTS = ["Positivo", "Negativo", "Neutral"]
EMOTIONS = ["Alegría", "Ira", "Tristeza", "Miedo", "Sorpresa"]
POLITICAL_CLASSES = [
    "Apoya a Keiko",
    "Critica a Keiko",
    "Apoya a Roberto",
    "Critica a Roberto",
    "Neutral",
]

# Temas políticos
TOPICS = [
    "Economía",
    "Seguridad",
    "Corrupción",
    "Educación",
    "Salud",
    "Empleo",
    "Minería",
    "Infraestructura",
    "General",
]

TOPIC_KEYWORDS = {
    "Economía": ["economía", "economia", "inflación", "inflacion", "impuestos", "pib", "fiscal", "precios", "dolar", "dólar"],
    "Seguridad": ["seguridad", "delincuencia", "policía", "policia", "crimen", "violencia", "narco"],
    "Corrupción": ["corrupción", "corrupcion", "ladron", "ladrón", "robo", "soborno", "odebrecht", "fujimorismo"],
    "Educación": ["educación", "educacion", "universidad", "colegio", "profesor", "estudiante"],
    "Salud": ["salud", "hospital", "medicina", "sis", "essalud", "covid", "vacuna"],
    "Empleo": ["empleo", "trabajo", "desempleo", "sueldo", "salario", "jovenes", "jóvenes"],
    "Minería": ["minería", "mineria", "minero", "conga", "antamina", "extractivismo"],
    "Infraestructura": ["infraestructura", "carretera", "obras", "transporte", "metro", "agua", "saneamiento"],
}

# Búsqueda YouTube
DEFAULT_SEARCH_QUERIES = [
    "debate presidencial Perú 2026 segunda vuelta",
    "Keiko Fujimori Roberto Sánchez debate",
    "segunda vuelta presidencial Perú 2026",
    "entrevista Keiko Fujimori 2026",
    "entrevista Roberto Sánchez 2026",
    "análisis debate presidencial Perú",
    "resumen debate segunda vuelta Perú",
]

# UI Theme
THEME = {
    "background": "#0b0f19",
    "card": "#151c2c",
    "blue": "#3b82f6",
    "cyan": "#00E5FF",
    "green": "#00C851",
    "red": "#ff4444",
    "text": "#e2e8f0",
    "muted": "#94a3b8",
    "border": "rgba(59, 130, 246, 0.25)",
}

# Modelos
SENTIMENT_MODES = ["Automático", "TF-IDF + Logistic Regression", "BETO", "RoBERTa Español"]
DEFAULT_SENTIMENT_MODE = "Automático"
LR_MODEL_PATH = MODELS_DIR / "sentiment_lr.joblib"
TFIDF_PATH = MODELS_DIR / "tfidf_vectorizer.joblib"

# SQLite
SQLITE_TIMEOUT = 30.0

# Scraping
MAX_VIDEOS_PER_SEARCH = 10
MAX_COMMENTS_PER_VIDEO = 200
