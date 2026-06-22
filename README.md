# Electoral Intelligence Platform

Plataforma profesional de **análisis de sentimientos y analítica política digital** basada en NLP sobre comentarios de YouTube relacionados con la segunda vuelta presidencial del Perú 2026: **Keiko Fujimori** vs **Roberto Sánchez**.

---

## Características

- Extracción de comentarios vía **YouTube Data API v3**
- Importación desde **CSV**, **Excel** y fuentes demo
- Pipeline NLP completo en español (limpieza, lematización, stopwords)
- **4 modos de análisis de sentimiento**: TF-IDF+LR, BETO, RoBERTa, Automático
- Detección de candidatos, emociones, temas y clasificación política
- **13 KPIs políticos**: Share of Voice, Polarización, Debate Winner Index, etc.
- Dashboard Streamlit premium con tema oscuro estilo Bloomberg/TradingView
- Reportes automáticos en **PDF**, **Excel**, **CSV** y **Markdown**
- Detección de bots/spam y ranking de influencia
- Base de datos **SQLite** con CRUD completo

---

## Instalación

```bash
# Clonar o descomprimir el proyecto
cd analsisis-de-sentimientos

# Crear entorno virtual (recomendado)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Descargar recursos NLTK
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# (Opcional) Modelo spaCy español
python -m spacy download es_core_news_sm
```

---

## Configuración

### YouTube API

1. Crear proyecto en [Google Cloud Console](https://console.cloud.google.com/)
2. Habilitar **YouTube Data API v3**
3. Crear credencial de API Key
4. Configurar variable de entorno:

```bash
# Windows PowerShell
$env:YOUTUBE_API_KEY = "TU_API_KEY"

# Linux/Mac
export YOUTUBE_API_KEY="TU_API_KEY"
```

### Inicio rápido (sin API)

1. Ejecutar la aplicación
2. En la barra lateral seleccionar **Demo**
3. Clic en **Cargar datos demo**

---

## Ejecución

```bash
# Dashboard principal
streamlit run app.py

# Verificar pipeline completo
python verify_pipeline.py

# Tests
pytest tests/ -v
```

La aplicación estará disponible en `http://localhost:8501`

---

## Arquitectura

```
project_root/
├── app.py                  # Dashboard Streamlit principal
├── config.py               # Configuración central
├── requirements.txt
├── verify_pipeline.py      # Validación end-to-end
├── README.md
├── data/                   # SQLite + datasets
├── models/                 # Modelos entrenados (.joblib)
├── reports/                # Reportes generados
├── tests/                  # Unit + integration tests
├── notebooks/              # Jupyter notebooks
└── src/
    ├── database/           # CRUD SQLite
    ├── scraping/           # YouTube, Reddit, CSV
    ├── preprocessing/      # Limpieza NLP español
    ├── sentiment/          # Sentimiento + candidatos
    ├── emotion/            # 5 emociones
    ├── topic_modeling/     # Diccionario + LDA
    ├── ml/                 # Pipeline + bots + influencia
    ├── analytics/          # KPIs políticos
    ├── visualization/      # Plotly charts
    ├── dashboard/          # Componentes UI
    ├── reporting/          # PDF/Excel/CSV/MD
    └── utils/              # Helpers + seed data
```

---

## Pestañas del Dashboard

| # | Pestaña | Descripción |
|---|---------|-------------|
| 1 | Resumen Ejecutivo | KPIs y conclusiones automáticas |
| 2 | Dashboard General | Sentimientos, SOV, Sankey, scatter |
| 3 | Keiko Fujimori | Análisis dedicado |
| 4 | Roberto Sánchez | Análisis dedicado |
| 5 | Sentimientos | Distribución y correlaciones |
| 6 | Emociones | Radar charts por candidato |
| 7 | Temas | Treemap + LDA emergente |
| 8 | Timeline | Evolución temporal |
| 9 | Bots | Detección de spam/sospechosos |
| 10 | Machine Learning | Evaluación y comparación de modelos |
| 11 | Explorador | Filtros avanzados de comentarios |
| 12 | Predicción | Análisis en tiempo real |
| 13 | Reportes | Exportación multi-formato |

---

## Métricas Políticas

- **Share of Voice** — Proporción de menciones por candidato
- **Popularidad** — % comentarios positivos
- **Rechazo** — % comentarios negativos
- **Engagement Score** — Likes + respuestas ponderados
- **Polarización** — Balance positivo vs negativo
- **Proposal Impact Index** — Impacto de propuestas
- **Debate Winner Index** — Ganador digital del debate
- **Influence Index** — Score de influencia promedio
- **Trend Index** — Tendencia semanal

---

## Solución de Errores

| Error | Solución |
|-------|----------|
| `TypeError: Invalid comparison UTC` | Ya corregido con `dt.tz_localize(None)` |
| `database is locked` | Timeout SQLite configurado a 30s |
| `YOUTUBE_API_KEY` inválida | Verificar clave en Google Cloud |
| Modelos Transformers lentos | Usar modo "TF-IDF + Logistic Regression" |
| CSV vacío | Verificar encoding UTF-8 y columnas |
| spaCy no encontrado | `python -m spacy download es_core_news_sm` |

---

## Casos de Uso

- Consultoras políticas evaluando percepción digital post-debate
- Medios de comunicación midiendo reacción de audiencia
- Observatorios electorales detectando polarización
- Centros de investigación en opinión pública
- Proyectos académicos de NLP aplicado a política

---

## Dependencias Principales

| Paquete | Uso |
|---------|-----|
| streamlit | Dashboard interactivo |
| pandas / numpy | Manipulación de datos |
| plotly | Visualizaciones interactivas |
| scikit-learn | TF-IDF, LR, LDA |
| transformers / torch | BETO, RoBERTa (opcional) |
| google-api-python-client | YouTube Data API |
| nltk / spacy | Preprocesamiento NLP |
| reportlab / openpyxl | Reportes PDF/Excel |

---

## Licencia

Proyecto académico — Electivo II, Ciclo 10.
