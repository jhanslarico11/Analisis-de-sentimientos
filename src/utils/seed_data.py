"""Datos de demostración para la plataforma."""

from __future__ import annotations

from datetime import datetime, timedelta
import random

import pandas as pd

from src.utils.helpers import generate_comment_id

SAMPLE_COMMENTS = [
    ("Keiko Fujimori presentó excelentes propuestas económicas en el debate", "Positivo", "Keiko Fujimori", "Economía"),
    ("Roberto Sánchez demostró honestidad y propuestas claras de empleo", "Positivo", "Roberto Sánchez", "Empleo"),
    ("No vuelve Keiko, corrupta como siempre, vergüenza nacional", "Negativo", "Keiko Fujimori", "Corrupción"),
    ("Roberto Sánchez no convence, propuestas vacías e incompetentes", "Negativo", "Roberto Sánchez", "General"),
    ("El debate fue transmitido anoche por Willax", "Neutral", "Ambos", "General"),
    ("Keiko propone seguridad y mano dura contra la delincuencia", "Positivo", "Keiko Fujimori", "Seguridad"),
    ("Roberto habló de salud universal y hospitales", "Positivo", "Roberto Sánchez", "Salud"),
    ("Fuerza Popular no aprende, misma corrupción de siempre", "Negativo", "Keiko Fujimori", "Corrupción"),
    ("Juntos por el Perú tiene mejores ideas para la educación", "Positivo", "Roberto Sánchez", "Educación"),
    ("Roberto Sánchez ganó el debate con propuestas de infraestructura", "Positivo", "Roberto Sánchez", "Infraestructura"),
    ("Keiko mintió sobre la economía, datos falsos", "Negativo", "Keiko Fujimori", "Economía"),
    ("Ambos candidatos hablaron de minería y medio ambiente", "Neutral", "Ambos", "Minería"),
    ("Apoyo total a Keiko, la única con experiencia", "Positivo", "Keiko Fujimori", "General"),
    ("Roberto es la esperanza del cambio verdadero", "Positivo", "Roberto Sánchez", "General"),
    ("Odio a los fujimoristas, nunca más", "Negativo", "Keiko Fujimori", "Corrupción"),
    ("Roberto no tiene plan de seguridad concreto", "Negativo", "Roberto Sánchez", "Seguridad"),
    ("Keiko y Roberto debaten sobre empleo juvenil", "Neutral", "Ambos", "Empleo"),
    ("Gran propuesta de Keiko sobre infraestructura vial", "Positivo", "Keiko Fujimori", "Infraestructura"),
    ("Roberto Sánchez propone reforma educativa seria", "Positivo", "Roberto Sánchez", "Educación"),
    ("Los comentarios del debate reflejan polarización extrema", "Neutral", "Ninguno", "General"),
    ("Keiko domina en menciones pero también en rechazo", "Negativo", "Keiko Fujimori", "General"),
    ("Roberto genera más engagement positivo en YouTube", "Positivo", "Roberto Sánchez", "General"),
    ("Propuesta económica de Roberto es la más sensata", "Positivo", "Roberto Sánchez", "Economía"),
    ("Keiko evade preguntas sobre corrupción", "Negativo", "Keiko Fujimori", "Corrupción"),
    ("Segunda vuelta presidencial Perú 2026 análisis completo", "Neutral", "Ninguno", "General"),
    ("Roberto Sánchez habló de lucha contra la corrupción", "Positivo", "Roberto Sánchez", "Corrupción"),
    ("Keiko promete seguridad en las calles", "Positivo", "Keiko Fujimori", "Seguridad"),
    ("No confío en ninguno de los dos candidatos", "Negativo", "Ambos", "General"),
    ("Excelente moderación del debate electoral", "Positivo", "Ninguno", "General"),
    ("Roberto propone empleo formal para jóvenes", "Positivo", "Roberto Sánchez", "Empleo"),
]

AUTHORS = [
    "AnalistaPolitico_PE", "ObservadorElectoral", "CiudadanoLima", "Votante2026",
    "PeriodistaDigital", "OpinionPublica", "ElectoralWatch", "PeruDecide",
    "DebatePeru", "ComentaristaPE", "UsuarioReal123", "PoliticaHoy",
]

VIDEO_TITLES = [
    "Debate Presidencial Segunda Vuelta Perú 2026 | Completo",
    "Análisis post-debate: Keiko vs Roberto Sánchez",
    "Entrevista exclusiva Roberto Sánchez - Propuestas 2026",
    "Keiko Fujimori en Ampliación de Noticias - Debate",
    "Resumen debate presidencial Perú 2026",
]

CHANNELS = ["Willax Televisión", "Latina Noticias", "América Noticias", "RPP Noticias", "Panamericana"]


def generate_sample_dataframe(n: int = 30) -> pd.DataFrame:
    """Genera DataFrame de demostración con comentarios simulados."""
    random.seed(42)
    base_date = datetime(2026, 6, 1, 20, 0, 0)
    rows = []
    for i in range(min(n, len(SAMPLE_COMMENTS) * 3)):
        text, _, _, _ = SAMPLE_COMMENTS[i % len(SAMPLE_COMMENTS)]
        author = random.choice(AUTHORS)
        video_idx = i % len(VIDEO_TITLES)
        video_id = f"demo_vid_{video_idx}"
        dt = base_date + timedelta(hours=i * 2, minutes=random.randint(0, 59))
        rows.append({
            "id": generate_comment_id(text, author, video_id),
            "source": "demo",
            "text": text,
            "author": author,
            "date": dt.isoformat(),
            "likes": random.randint(0, 500),
            "replies": random.randint(0, 50),
            "video_id": video_id,
            "video_title": VIDEO_TITLES[video_idx],
            "channel": CHANNELS[video_idx % len(CHANNELS)],
            "url": f"https://www.youtube.com/watch?v={video_id}",
        })
    return pd.DataFrame(rows)
