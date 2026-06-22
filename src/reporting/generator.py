"""Generación automática de reportes."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

import config
from src.analytics.metrics import PoliticalAnalytics
from src.utils.helpers import logger, now_str


class ReportGenerator:
    """Generador de reportes PDF, Excel, CSV y Markdown."""

    def __init__(self, df: pd.DataFrame, output_dir: Path = None):
        self.df = df
        self.analytics = PoliticalAnalytics(df)
        self.output_dir = output_dir or config.REPORTS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metrics = self.analytics.all_metrics()
        self.conclusions = self.metrics["conclusions"]

    def to_csv(self, filename: str = None) -> str:
        filename = filename or f"report_comments_{datetime.now():%Y%m%d_%H%M%S}.csv"
        path = self.output_dir / filename
        self.df.to_csv(path, index=False, encoding="utf-8-sig")
        logger.info("Reporte CSV generado: %s", path)
        return str(path)

    def to_excel(self, filename: str = None) -> str:
        filename = filename or f"report_analytics_{datetime.now():%Y%m%d_%H%M%S}.xlsx"
        path = self.output_dir / filename
        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            self.df.to_excel(writer, sheet_name="Comentarios", index=False)
            for name, data in [
                ("ShareOfVoice", self.metrics["share_of_voice"]),
                ("Popularidad", self.metrics["popularity"]),
                ("Rechazo", self.metrics["rejection"]),
                ("Engagement", self.metrics["engagement"]),
                ("ImpactoPropuestas", self.metrics["proposal_impact"]),
            ]:
                if isinstance(data, pd.DataFrame) and not data.empty:
                    data.to_excel(writer, sheet_name=name[:31], index=False)
            pd.DataFrame([self.conclusions]).to_excel(writer, sheet_name="Conclusiones", index=False)
        logger.info("Reporte Excel generado: %s", path)
        return str(path)

    def _df_to_markdown(self, df: pd.DataFrame) -> str:
        if df.empty:
            return "Sin datos."
        try:
            return df.to_markdown(index=False)
        except ImportError:
            header = " | ".join(df.columns)
            sep = " | ".join(["---"] * len(df.columns))
            rows = [" | ".join(str(v) for v in row) for row in df.values]
            return "\n".join([header, sep] + rows)

    def to_markdown(self, filename: str = None) -> str:
        filename = filename or f"report_{datetime.now():%Y%m%d_%H%M%S}.md"
        path = self.output_dir / filename
        c = self.conclusions
        content = f"""# Reporte de Análisis Electoral Digital

**Generado:** {now_str()}  
**Total comentarios:** {len(self.df)}

## Conclusiones Ejecutivas

- **Candidato más mencionado:** {c.get('most_mentioned', 'N/A')}
- **Mejor valoración digital:** {c.get('best_valued', 'N/A')}
- **Mayor rechazo:** {c.get('most_rejected', 'N/A')}
- **Emoción dominante:** {c.get('dominant_emotion', 'N/A')}
- **Tema predominante:** {c.get('dominant_topic', 'N/A')}
- **Ganador digital del debate:** {c.get('debate_winner', 'N/A')}
- **Polarización:** {c.get('polarization', 'N/A')}%

## Resumen

{c.get('summary', '')}

## Métricas de Engagement

{self._df_to_markdown(self.metrics['engagement'])}

## Share of Voice

{self._df_to_markdown(self.metrics['share_of_voice'])}
"""
        path.write_text(content, encoding="utf-8")
        logger.info("Reporte Markdown generado: %s", path)
        return str(path)

    def to_pdf(self, filename: str = None) -> str:
        filename = filename or f"report_{datetime.now():%Y%m%d_%H%M%S}.pdf"
        path = self.output_dir / filename
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

            doc = SimpleDocTemplate(str(path), pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            story.append(Paragraph("Reporte de Análisis Electoral Digital", styles["Title"]))
            story.append(Spacer(1, 12))
            story.append(Paragraph(f"Generado: {now_str()}", styles["Normal"]))
            story.append(Spacer(1, 12))
            for key, label in [
                ("most_mentioned", "Candidato más mencionado"),
                ("best_valued", "Mejor valorado"),
                ("most_rejected", "Más rechazado"),
                ("dominant_emotion", "Emoción dominante"),
                ("dominant_topic", "Tema dominante"),
                ("debate_winner", "Ganador digital del debate"),
            ]:
                story.append(Paragraph(f"<b>{label}:</b> {self.conclusions.get(key, 'N/A')}", styles["Normal"]))
            story.append(Spacer(1, 12))
            story.append(Paragraph(self.conclusions.get("summary", ""), styles["Normal"]))
            if not self.metrics["share_of_voice"].empty:
                story.append(Spacer(1, 12))
                data = [self.metrics["share_of_voice"].columns.tolist()] + self.metrics["share_of_voice"].values.tolist()
                table = Table(data)
                table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3b82f6")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ]))
                story.append(table)
            doc.build(story)
            logger.info("Reporte PDF generado: %s", path)
            return str(path)
        except ImportError:
            md_path = self.to_markdown(filename.replace(".pdf", ".md"))
            logger.warning("reportlab no disponible. Se generó Markdown: %s", md_path)
            return md_path

    def generate_all(self) -> dict[str, str]:
        return {
            "csv": self.to_csv(),
            "excel": self.to_excel(),
            "markdown": self.to_markdown(),
            "pdf": self.to_pdf(),
        }
