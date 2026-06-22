"""Estilos CSS premium para dashboard oscuro."""

import config

CUSTOM_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background: linear-gradient(135deg, {config.THEME['background']} 0%, #0f172a 50%, {config.THEME['background']} 100%);
    color: {config.THEME['text']};
}}

.block-container {{
    padding-top: 1.5rem;
    max-width: 1400px;
}}

section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {config.THEME['card']} 0%, {config.THEME['background']} 100%);
    border-right: 1px solid {config.THEME['border']};
}}

section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {{
    color: {config.THEME['cyan']};
}}

.kpi-card {{
    background: rgba(21, 28, 44, 0.85);
    backdrop-filter: blur(12px);
    border: 1px solid {config.THEME['border']};
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.kpi-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(59, 130, 246, 0.15);
}}

.kpi-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: {config.THEME['muted']};
    margin-bottom: 0.5rem;
}}

.kpi-value {{
    font-size: 2rem;
    font-weight: 700;
    color: {config.THEME['text']};
    line-height: 1.2;
}}

.kpi-delta {{
    font-size: 0.85rem;
    margin-top: 0.25rem;
}}

.kpi-positive {{ color: {config.THEME['green']}; }}
.kpi-negative {{ color: {config.THEME['red']}; }}
.kpi-neutral {{ color: {config.THEME['cyan']}; }}

.glass-panel {{
    background: rgba(21, 28, 44, 0.7);
    backdrop-filter: blur(10px);
    border: 1px solid {config.THEME['border']};
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin: 0.5rem 0 1rem 0;
}}

.hero-title {{
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(90deg, {config.THEME['cyan']}, {config.THEME['blue']});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.25rem;
}}

.hero-subtitle {{
    color: {config.THEME['muted']};
    font-size: 1rem;
    margin-bottom: 1.5rem;
}}

.conclusion-box {{
    background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(0,229,255,0.08));
    border-left: 4px solid {config.THEME['cyan']};
    padding: 1rem 1.25rem;
    border-radius: 0 12px 12px 0;
    margin: 1rem 0;
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
    background: transparent;
}}

.stTabs [data-baseweb="tab"] {{
    background: {config.THEME['card']};
    border-radius: 8px;
    padding: 8px 16px;
    border: 1px solid {config.THEME['border']};
}}

.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, {config.THEME['blue']}, #2563eb) !important;
    color: white !important;
}}

div[data-testid="stMetric"] {{
    background: rgba(21, 28, 44, 0.85);
    border: 1px solid {config.THEME['border']};
    border-radius: 12px;
    padding: 1rem;
}}

.stDataFrame {{
    border-radius: 12px;
    overflow: hidden;
}}
</style>
"""


def render_kpi_card(label: str, value: str, delta: str = "", delta_type: str = "neutral"):
    css_class = f"kpi-{delta_type}"
    delta_html = f'<div class="kpi-delta {css_class}">{delta}</div>' if delta else ""
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """
