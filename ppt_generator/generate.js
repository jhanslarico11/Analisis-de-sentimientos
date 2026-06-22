const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.title = 'Plan de Auditoria Integral - UPeU CPPP';

const DARK_BLUE = "1B3A6B";
const MID_BLUE  = "2E75B6";
const LIGHT_BLUE = "D6E4F5";
const WHITE = "FFFFFF";
const ACCENT = "E8A020";
const GRAY = "F2F6FC";
const TEXT_DARK = "1A1A2E";

// Helper: card
function card(slide, x, y, w, h, fill = WHITE) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h,
    fill: { color: fill },
    rectRadius: 0.08,
    shadow: { type: "outer", color: "000000", blur: 8, offset: 2, angle: 45, opacity: 0.10 }
  });
}

// Helper: section badge
function badge(slide, x, y, text, fill = MID_BLUE) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w: 2.2, h: 0.35,
    fill: { color: fill },
    rectRadius: 0.17,
    line: { color: fill }
  });
  slide.addText(text, {
    x, y, w: 2.2, h: 0.35,
    fontSize: 10, bold: true, color: WHITE, align: "center", valign: "middle",
    margin: 0, fontFace: "Calibri"
  });
}

// ====================================================
// SLIDE 1 - PORTADA
// ====================================================
{
  const s = pres.addSlide();
  s.background = { color: DARK_BLUE };

  // Top accent band
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.08,
    fill: { color: ACCENT }, line: { color: ACCENT }
  });

  // Left panel (dark overlay)
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0.08, w: 3.8, h: 5.545,
    fill: { color: "11244A" }, line: { color: "11244A" }
  });

  // Vertical label
  s.addText("AUDITORIA INTEGRAL", {
    x: 0.15, y: 0.5, w: 3.5, h: 4.0,
    fontSize: 11, color: "6899CC", fontFace: "Calibri", bold: true,
    charSpacing: 6, align: "center", rotate: 270
  });

  // Right panel content
  s.addText("PLAN DE AUDITORÍA INTEGRAL", {
    x: 4.1, y: 0.7, w: 5.6, h: 1.1,
    fontSize: 30, bold: true, color: WHITE, fontFace: "Calibri", align: "left", valign: "top"
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 4.1, y: 1.85, w: 5.6, h: 0.05,
    fill: { color: ACCENT }, line: { color: ACCENT }
  });

  s.addText("Centro de Prácticas Pre Profesionales", {
    x: 4.1, y: 1.95, w: 5.6, h: 0.6,
    fontSize: 18, color: "A8C8F0", fontFace: "Calibri", bold: false, align: "left"
  });

  s.addText("UNIVERSIDAD PERUANA UNIÓN", {
    x: 4.1, y: 2.65, w: 5.6, h: 0.4,
    fontSize: 13, color: ACCENT, fontFace: "Calibri", bold: true, align: "left", charSpacing: 2
  });

  // Info boxes at bottom
  const infos = [
    ["📅 Periodo", "2024 – 2025"],
    ["📋 Tipo", "Integral"],
    ["🏛️ Entidad", "UPeU – CPPP"],
  ];
  infos.forEach(([label, val], i) => {
    const bx = 4.1 + i * 1.95;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: bx, y: 3.7, w: 1.8, h: 0.9,
      fill: { color: "243B6B" }, rectRadius: 0.08, line: { color: "3B5FA0" }
    });
    s.addText(label, { x: bx, y: 3.75, w: 1.8, h: 0.3, fontSize: 9, color: "8BB8E8", fontFace: "Calibri", align: "center" });
    s.addText(val, { x: bx, y: 4.05, w: 1.8, h: 0.4, fontSize: 11, bold: true, color: WHITE, fontFace: "Calibri", align: "center" });
  });

  s.addText("Lima, Perú • 2025  |  Versión 1.0  |  Confidencial", {
    x: 4.1, y: 4.75, w: 5.6, h: 0.3,
    fontSize: 9, color: "6080A0", fontFace: "Calibri", align: "left"
  });
}

// ====================================================
// SLIDE 2 - AGENDA / CONTENIDO
// ====================================================
{
  const s = pres.addSlide();
  s.background = { color: GRAY };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 1.1, fill: { color: DARK_BLUE }, line: { color: DARK_BLUE } });
  s.addText("CONTENIDO DEL PLAN", { x: 0.4, y: 0, w: 9, h: 1.1, fontSize: 26, bold: true, color: WHITE, fontFace: "Calibri", valign: "middle" });
  badge(s, 8.3, 0.35, "AGENDA", ACCENT);

  const items = [
    ["01", "Introducción y Antecedentes", "Marco normativo y contexto institucional"],
    ["02", "Objetivos de la Auditoría", "General y específicos del encargo"],
    ["03", "Alcance y Áreas Auditadas", "Periodo, unidades y procesos incluidos"],
    ["04", "Metodología", "Fases, técnicas y herramientas"],
    ["05", "Evaluación de Riesgos", "Matriz de riesgos prioritarios"],
    ["06", "Programa de Auditoría", "Procedimientos financieros, operativos y de TI"],
    ["07", "Equipo Auditor", "Roles, responsabilidades y cronograma"],
    ["08", "Presupuesto e Informe Final", "Recursos y estructura de resultados"],
  ];

  items.forEach(([num, title, desc], i) => {
    const col = i < 4 ? 0 : 1;
    const row = i % 4;
    const x = col === 0 ? 0.3 : 5.2;
    const y = 1.3 + row * 1.0;

    card(s, x, y, 4.7, 0.85, WHITE);
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 0.55, h: 0.85,
      fill: { color: MID_BLUE }, rectRadius: 0.08, line: { color: MID_BLUE }
    });
    s.addText(num, { x, y, w: 0.55, h: 0.85, fontSize: 16, bold: true, color: WHITE, fontFace: "Calibri", align: "center", valign: "middle", margin: 0 });
    s.addText(title, { x: x + 0.65, y: y + 0.05, w: 3.9, h: 0.35, fontSize: 12, bold: true, color: DARK_BLUE, fontFace: "Calibri" });
    s.addText(desc, { x: x + 0.65, y: y + 0.42, w: 3.9, h: 0.3, fontSize: 9, color: "607090", fontFace: "Calibri" });
  });
}

// ====================================================
// SLIDE 3 - INTRODUCCION
// ====================================================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 1.1, fill: { color: DARK_BLUE }, line: { color: DARK_BLUE } });
  s.addText("01 | INTRODUCCIÓN", { x: 0.4, y: 0, w: 8, h: 1.1, fontSize: 26, bold: true, color: WHITE, fontFace: "Calibri", valign: "middle" });

  // Two columns
  card(s, 0.3, 1.25, 4.5, 3.9, "EBF3FB");
  s.addText("¿Qué es el CPPP?", { x: 0.5, y: 1.35, w: 4.1, h: 0.4, fontSize: 13, bold: true, color: DARK_BLUE, fontFace: "Calibri" });
  s.addText([
    { text: "El Centro de Prácticas Pre Profesionales de la UPeU articula la formación práctica de los estudiantes con el sector productivo y de servicios.", options: { breakLine: true } },
    { text: "\nCreado bajo exigencias de la Ley Universitaria N.° 30220 y los requisitos de licenciamiento SUNEDU.", options: { breakLine: true } },
    { text: "\nGestiona convenios con entidades públicas, privadas y organizaciones de la sociedad civil.", options: {} }
  ], { x: 0.5, y: 1.8, w: 4.1, h: 2.9, fontSize: 11, color: TEXT_DARK, fontFace: "Calibri", valign: "top" });

  card(s, 5.1, 1.25, 4.5, 3.9, "FFF8EC");
  s.addText("¿Por qué esta auditoría?", { x: 5.3, y: 1.35, w: 4.1, h: 0.4, fontSize: 13, bold: true, color: DARK_BLUE, fontFace: "Calibri" });
  const razones = [
    "Crecimiento acelerado de la demanda de plazas de prácticas",
    "Incremento del número de convenios institucionales",
    "Diversificación de carreras que utilizan la plataforma",
    "Necesidad de alineamiento con objetivos estratégicos UPeU",
    "Exigencias de transparencia y buen gobierno universitario",
  ];
  s.addText(
    razones.map((r, i) => ({ text: `• ${r}`, options: { breakLine: i < razones.length - 1 } })),
    { x: 5.3, y: 1.8, w: 4.1, h: 2.9, fontSize: 11, color: TEXT_DARK, fontFace: "Calibri", valign: "top" }
  );

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.25, w: 10, h: 0.375, fill: { color: ACCENT }, line: { color: ACCENT } });
  s.addText("Marco normativo: Ley N.° 30220 • Ley N.° 28518 • DS 007-2005-TR • NIEPAI • COSO 2013 • SUNEDU", {
    x: 0.3, y: 5.25, w: 9.4, h: 0.375, fontSize: 10, color: WHITE, fontFace: "Calibri", bold: true, align: "center", valign: "middle"
  });
}

// ====================================================
// SLIDE 4 - OBJETIVOS
// ====================================================
{
  const s = pres.addSlide();
  s.background = { color: GRAY };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 1.1, fill: { color: DARK_BLUE }, line: { color: DARK_BLUE } });
  s.addText("02 | OBJETIVOS DE LA AUDITORÍA", { x: 0.4, y: 0, w: 8, h: 1.1, fontSize: 26, bold: true, color: WHITE, fontFace: "Calibri", valign: "middle" });

  // Objetivo general box
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.3, y: 1.2, w: 9.4, h: 1.1,
    fill: { color: MID_BLUE }, rectRadius: 0.1,
    shadow: { type: "outer", color: "000000", blur: 6, offset: 2, angle: 45, opacity: 0.12 }
  });
  s.addText("OBJETIVO GENERAL", { x: 0.5, y: 1.2, w: 2.2, h: 0.4, fontSize: 10, bold: true, color: ACCENT, fontFace: "Calibri", valign: "bottom" });
  s.addText("Evaluar la gestión administrativa, financiera, operativa y el cumplimiento normativo del CPPP para emitir una opinión técnica objetiva que contribuya a la mejora continua y transparencia institucional.",
    { x: 0.5, y: 1.6, w: 9.0, h: 0.55, fontSize: 11, color: WHITE, fontFace: "Calibri" });

  const objs = [
    ["Estructura\nOrganizacional", "Evaluar roles, funciones y modelo de gobierno del CPPP"],
    ["Cumplimiento\nNormativo", "Verificar adherencia a Ley 28518, Reglamento UPeU y SUNEDU"],
    ["Gestión de\nConvenios", "Examinar suscripción, seguimiento y renovación de alianzas"],
    ["Gestión de\nPracticantes", "Analizar asignación, supervisión y evaluación de practicantes"],
    ["Gestión\nFinanciera", "Revisar ejecución presupuestal y pertinencia de gastos"],
    ["Sistemas de\nInformación", "Evaluar integridad, seguridad y disponibilidad de datos"],
  ];

  objs.forEach(([title, desc], i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = 0.3 + col * 3.15;
    const y = 2.5 + row * 1.4;
    card(s, x, y, 3.0, 1.25, WHITE);
    s.addText(`0${i+1}`, { x, y: y + 0.05, w: 3.0, h: 0.35, fontSize: 22, bold: true, color: LIGHT_BLUE, fontFace: "Calibri", align: "center" });
    s.addText(title, { x, y: y + 0.35, w: 3.0, h: 0.45, fontSize: 10, bold: true, color: DARK_BLUE, fontFace: "Calibri", align: "center" });
    s.addText(desc, { x: x + 0.15, y: y + 0.78, w: 2.7, h: 0.38, fontSize: 9, color: "607090", fontFace: "Calibri", align: "center" });
  });
}

// ====================================================
// SLIDE 5 - ALCANCE
// ====================================================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 1.1, fill: { color: DARK_BLUE }, line: { color: DARK_BLUE } });
  s.addText("03 | ALCANCE DE LA AUDITORÍA", { x: 0.4, y: 0, w: 8, h: 1.1, fontSize: 26, bold: true, color: WHITE, fontFace: "Calibri", valign: "middle" });

  // Period box
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.3, y: 1.2, w: 4.2, h: 1.0,
    fill: { color: "EBF3FB" }, rectRadius: 0.08,
    shadow: { type: "outer", color: "000000", blur: 4, offset: 1, angle: 45, opacity: 0.1 }
  });
  s.addText("📅  Período Auditado", { x: 0.5, y: 1.25, w: 3.8, h: 0.35, fontSize: 11, bold: true, color: DARK_BLUE, fontFace: "Calibri" });
  s.addText("Ejercicios académicos y administrativos 2024 – 2025", { x: 0.5, y: 1.6, w: 3.8, h: 0.45, fontSize: 10, color: "405080", fontFace: "Calibri" });

  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 4.8, y: 1.2, w: 4.9, h: 1.0,
    fill: { color: "FFF4E0" }, rectRadius: 0.08,
    shadow: { type: "outer", color: "000000", blur: 4, offset: 1, angle: 45, opacity: 0.1 }
  });
  s.addText("🏛️  Ámbito Organizacional", { x: 5.0, y: 1.25, w: 4.5, h: 0.35, fontSize: 11, bold: true, color: DARK_BLUE, fontFace: "Calibri" });
  s.addText("CPPP + Facultades + Bienestar + RRHH + Legal + Administración y Finanzas", { x: 5.0, y: 1.6, w: 4.5, h: 0.45, fontSize: 10, color: "405080", fontFace: "Calibri" });

  // Areas table header
  s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 2.4, w: 9.4, h: 0.4, fill: { color: DARK_BLUE }, line: { color: DARK_BLUE } });
  ["N°", "Área / Proceso Auditado", "Tipo de Auditoría", "Prioridad"].forEach((h, i) => {
    const wx = [0.3, 0.85, 6.1, 8.2];
    const ww = [0.55, 5.25, 2.1, 1.5];
    s.addText(h, { x: wx[i], y: 2.4, w: ww[i], h: 0.4, fontSize: 10, bold: true, color: WHITE, fontFace: "Calibri", align: i === 0 ? "center" : "left", valign: "middle" });
  });

  const rows = [
    ["1", "Gestión Administrativa del CPPP", "Operativa / Gestión", "ALTA"],
    ["2", "Convenios con Empresas e Instituciones", "Cumplimiento / Legal", "ALTA"],
    ["3", "Asignación y Supervisión de Practicantes", "Operativa", "ALTA"],
    ["4", "Gestión Presupuestal y Financiera", "Financiera", "ALTA"],
    ["5", "Sistemas de Información y TI", "TI / Seguridad", "MEDIA"],
    ["6", "Cumplimiento Normativo SUNEDU", "Cumplimiento", "ALTA"],
    ["7", "Recursos Humanos del CPPP", "Operativa", "MEDIA"],
  ];

  rows.forEach((row, ri) => {
    const y = 2.8 + ri * 0.37;
    const bg = ri % 2 === 0 ? WHITE : "EBF3FB";
    s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y, w: 9.4, h: 0.37, fill: { color: bg }, line: { color: "C8DCF0" } });
    const wx = [0.3, 0.85, 6.1, 8.2];
    const ww = [0.55, 5.25, 2.1, 1.5];
    row.forEach((cell, ci) => {
      const isAlta = cell === "ALTA";
      const isMedia = cell === "MEDIA";
      if ((isAlta || isMedia) && ci === 3) {
        s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: wx[ci] + 0.1, y: y + 0.05, w: 1.1, h: 0.27, fill: { color: isAlta ? "C8372D" : "E8A020" }, rectRadius: 0.05, line: { color: isAlta ? "C8372D" : "E8A020" } });
        s.addText(cell, { x: wx[ci] + 0.1, y: y + 0.05, w: 1.1, h: 0.27, fontSize: 9, bold: true, color: WHITE, fontFace: "Calibri", align: "center", valign: "middle", margin: 0 });
      } else {
        s.addText(cell, { x: wx[ci], y: y + 0.04, w: ww[ci], h: 0.3, fontSize: 10, color: TEXT_DARK, fontFace: "Calibri", align: ci === 0 ? "center" : "left" });
      }
    });
  });
}

// ====================================================
// SLIDE 6 - METODOLOGIA
// ====================================================
{
  const s = pres.addSlide();
  s.background = { color: GRAY };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 1.1, fill: { color: DARK_BLUE }, line: { color: DARK_BLUE } });
  s.addText("04 | METODOLOGÍA", { x: 0.4, y: 0, w: 8, h: 1.1, fontSize: 26, bold: true, color: WHITE, fontFace: "Calibri", valign: "middle" });

  const phases = [
    { num: "I", title: "Planificación", weeks: "Semanas 1-3", color: "1B4F8A", items: ["Reunión de apertura", "Evaluación de control interno", "Matriz de riesgos", "Programa de auditoría"] },
    { num: "II", title: "Trabajo de Campo", weeks: "Semanas 4-9", color: MID_BLUE, items: ["Entrevistas y cuestionarios", "Observación de procesos", "Pruebas sustantivas", "Análisis de datos"] },
    { num: "III", title: "Evaluación", weeks: "Semanas 10-12", color: "1B6A7F", items: ["Triangulación de evidencias", "Matriz de hallazgos", "Reunión de avance", "Respuestas de la admin."] },
    { num: "IV", title: "Informe y Cierre", weeks: "Semanas 13-16", color: "17567A", items: ["Borrador del informe", "Reunión de cierre", "Informe final", "Plan de seguimiento"] },
  ];

  phases.forEach((ph, i) => {
    const x = 0.25 + i * 2.4;
    // Phase card
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x, y: 1.2, w: 2.25, h: 4.1,
      fill: { color: WHITE }, rectRadius: 0.1,
      shadow: { type: "outer", color: "000000", blur: 8, offset: 2, angle: 45, opacity: 0.1 }
    });
    // Phase header
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x, y: 1.2, w: 2.25, h: 1.1,
      fill: { color: ph.color }, rectRadius: 0.1, line: { color: ph.color }
    });
    s.addText(`FASE ${ph.num}`, { x, y: 1.22, w: 2.25, h: 0.35, fontSize: 9, bold: true, color: ACCENT, fontFace: "Calibri", align: "center" });
    s.addText(ph.title, { x, y: 1.57, w: 2.25, h: 0.4, fontSize: 13, bold: true, color: WHITE, fontFace: "Calibri", align: "center" });
    s.addText(ph.weeks, { x, y: 1.97, w: 2.25, h: 0.3, fontSize: 9, color: "A0C8E8", fontFace: "Calibri", align: "center" });

    // Items
    ph.items.forEach((item, j) => {
      s.addShape(pres.shapes.OVAL, {
        x: x + 0.15, y: 2.42 + j * 0.47, w: 0.18, h: 0.18,
        fill: { color: ph.color }, line: { color: ph.color }
      });
      s.addText(item, {
        x: x + 0.38, y: 2.4 + j * 0.47, w: 1.78, h: 0.38,
        fontSize: 10, color: TEXT_DARK, fontFace: "Calibri", valign: "middle"
      });
    });

    // Arrow between phases
    if (i < 3) {
      s.addShape(pres.shapes.LINE, {
        x: x + 2.25, y: 3.3, w: 0.15, h: 0,
        line: { color: MID_BLUE, width: 2 }
      });
    }
  });

  // Framework badges
  s.addText("Marcos de referencia: COSO 2013 • COSO ERM 2017 • NIEPAI (IIA) • NAGAS • COBIT", {
    x: 0.3, y: 5.25, w: 9.4, h: 0.3,
    fontSize: 10, color: "405080", fontFace: "Calibri", align: "center",
    bold: true
  });
}

// ====================================================
// SLIDE 7 - EVALUACION DE RIESGOS
// ====================================================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 1.1, fill: { color: DARK_BLUE }, line: { color: DARK_BLUE } });
  s.addText("05 | EVALUACIÓN DE RIESGOS", { x: 0.4, y: 0, w: 8, h: 1.1, fontSize: 26, bold: true, color: WHITE, fontFace: "Calibri", valign: "middle" });

  // Risk matrix visual (simplified heat map)
  const matrixX = 0.3, matrixY = 1.25;
  const cellW = 0.6, cellH = 0.55;
  const impactColors = [
    ["D6E4F5","AED0EE","FDEBD0","F5B7B1","E74C3C"],
    ["AED0EE","7FB3DC","FDEBD0","F5B7B1","E74C3C"],
    ["FDEBD0","FDEBD0","F9E79F","F5B7B1","E74C3C"],
    ["A9DFBF","FDEBD0","F9E79F","F5B7B1","E74C3C"],
    ["A9DFBF","A9DFBF","FDEBD0","F9E79F","E74C3C"],
  ];

  // Y-axis label
  s.addText("PROBABILIDAD", { x: matrixX - 0.05, y: matrixY, w: 0.25, h: cellH * 5, fontSize: 8, bold: true, color: "607090", fontFace: "Calibri", rotate: 270, align: "center" });

  for (let row = 0; row < 5; row++) {
    for (let col = 0; col < 5; col++) {
      s.addShape(pres.shapes.RECTANGLE, {
        x: matrixX + 0.3 + col * cellW,
        y: matrixY + (4 - row) * cellH,
        w: cellW, h: cellH,
        fill: { color: impactColors[row][col] },
        line: { color: WHITE, width: 2 }
      });
      const val = (row + 1) * (col + 1);
      s.addText(String(val), {
        x: matrixX + 0.3 + col * cellW,
        y: matrixY + (4 - row) * cellH,
        w: cellW, h: cellH,
        fontSize: 10, bold: val >= 16, color: val >= 16 ? WHITE : "405080",
        fontFace: "Calibri", align: "center", valign: "middle", margin: 0
      });
    }
    s.addText(String(row + 1), { x: matrixX + 0.05, y: matrixY + (4 - row) * cellH, w: 0.25, h: cellH, fontSize: 9, color: "607090", fontFace: "Calibri", align: "center", valign: "middle" });
  }

  // X-axis
  for (let col = 0; col < 5; col++) {
    s.addText(String(col + 1), { x: matrixX + 0.3 + col * cellW, y: matrixY + 5 * cellH + 0.02, w: cellW, h: 0.25, fontSize: 9, color: "607090", fontFace: "Calibri", align: "center" });
  }
  s.addText("IMPACTO", { x: matrixX + 0.3, y: matrixY + 5 * cellH + 0.25, w: cellW * 5, h: 0.25, fontSize: 8, bold: true, color: "607090", fontFace: "Calibri", align: "center" });

  // Legend
  const legends = [{ c: "E74C3C", l: "Crítico (16-25)" }, { c: "F5B7B1", l: "Alto (10-15)" }, { c: "F9E79F", l: "Medio (5-9)" }, { c: "A9DFBF", l: "Bajo (1-4)" }];
  legends.forEach((leg, i) => {
    s.addShape(pres.shapes.RECTANGLE, { x: matrixX + 0.3, y: matrixY + 3.25 + i * 0.28, w: 0.2, h: 0.2, fill: { color: leg.c }, line: { color: leg.c } });
    s.addText(leg.l, { x: matrixX + 0.55, y: matrixY + 3.25 + i * 0.28, w: 2.5, h: 0.22, fontSize: 9, color: TEXT_DARK, fontFace: "Calibri" });
  });

  // Top risks table
  const risks = [
    ["Convenios sin actualización legal", "CRÍTICO", "E74C3C"],
    ["Incumplimiento Ley N.° 28518", "ALTO", "E67E22"],
    ["Practicantes sin supervisión adecuada", "ALTO", "E67E22"],
    ["Pérdida de datos de practicantes", "ALTO", "E67E22"],
    ["Incumplimiento condiciones SUNEDU", "ALTO", "E67E22"],
    ["Rotación alta de personal CPPP", "MEDIO", "2E86AB"],
  ];

  s.addText("RIESGOS PRIORITARIOS IDENTIFICADOS", { x: 4.0, y: 1.25, w: 5.7, h: 0.3, fontSize: 11, bold: true, color: DARK_BLUE, fontFace: "Calibri" });
  s.addShape(pres.shapes.RECTANGLE, { x: 4.0, y: 1.55, w: 5.7, h: 0.02, fill: { color: MID_BLUE }, line: { color: MID_BLUE } });

  risks.forEach((risk, i) => {
    const ry = 1.6 + i * 0.58;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 4.0, y: ry, w: 5.7, h: 0.5,
      fill: { color: "F8FBFF" }, rectRadius: 0.06,
      shadow: { type: "outer", color: "000000", blur: 4, offset: 1, angle: 45, opacity: 0.08 }
    });
    s.addText(risk[0], { x: 4.15, y: ry + 0.05, w: 4.0, h: 0.4, fontSize: 10, color: TEXT_DARK, fontFace: "Calibri", valign: "middle" });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 8.2, y: ry + 0.1, w: 1.3, h: 0.3, fill: { color: risk[2] }, rectRadius: 0.05, line: { color: risk[2] } });
    s.addText(risk[1], { x: 8.2, y: ry + 0.1, w: 1.3, h: 0.3, fontSize: 9, bold: true, color: WHITE, fontFace: "Calibri", align: "center", valign: "middle", margin: 0 });
  });
}

// ====================================================
// SLIDE 8 - PROGRAMA DE AUDITORIA
// ====================================================
{
  const s = pres.addSlide();
  s.background = { color: GRAY };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 1.1, fill: { color: DARK_BLUE }, line: { color: DARK_BLUE } });
  s.addText("06 | PROGRAMA DE AUDITORÍA", { x: 0.4, y: 0, w: 8, h: 1.1, fontSize: 26, bold: true, color: WHITE, fontFace: "Calibri", valign: "middle" });

  const programs = [
    {
      title: "Auditoría Financiera",
      color: "1B4F8A",
      icon: "💰",
      items: ["Presupuesto asignado vs ejecutado", "Transferencias y fondos recibidos", "Facturas y comprobantes de pago", "Conciliación bancaria", "Planilla de personal", "Ingresos por convenios"]
    },
    {
      title: "Auditoría Operativa",
      color: MID_BLUE,
      icon: "⚙️",
      items: ["Proceso de asignación de practicantes", "Fichas de supervisión", "Evaluación final de practicantes", "Gestión de convenios", "Tiempos de respuesta", "Indicadores de gestión"]
    },
    {
      title: "Auditoría de Cumplimiento",
      color: "16607A",
      icon: "📋",
      items: ["Cumplimiento Ley N.° 28518", "Condiciones mínimas en convenios", "Seguros de practicantes vigentes", "Jornada máxima de prácticas", "Subvención económica mínima", "Reportes a SUNEDU"]
    },
  ];

  programs.forEach((prog, i) => {
    const x = 0.3 + i * 3.25;
    card(s, x, 1.25, 3.1, 4.1, WHITE);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x, y: 1.25, w: 3.1, h: 0.7,
      fill: { color: prog.color }, rectRadius: 0.1, line: { color: prog.color }
    });
    s.addText(`${prog.icon}  ${prog.title}`, {
      x: x + 0.1, y: 1.25, w: 2.9, h: 0.7,
      fontSize: 12, bold: true, color: WHITE, fontFace: "Calibri", align: "center", valign: "middle"
    });
    prog.items.forEach((item, j) => {
      s.addShape(pres.shapes.OVAL, {
        x: x + 0.2, y: 2.07 + j * 0.52, w: 0.14, h: 0.14,
        fill: { color: prog.color }, line: { color: prog.color }
      });
      s.addText(item, {
        x: x + 0.4, y: 2.03 + j * 0.52, w: 2.55, h: 0.42,
        fontSize: 10, color: TEXT_DARK, fontFace: "Calibri", valign: "middle"
      });
    });
  });

  // TI badge
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.3, y: 5.2, w: 9.4, h: 0.3,
    fill: { color: "EBF3FB" }, rectRadius: 0.06, line: { color: "C8DCF0" }
  });
  s.addText("+ Auditoría de TI: Controles de acceso • Backups • Seguridad de datos • Ley N.° 29733 • Plan de continuidad", {
    x: 0.5, y: 5.2, w: 9.2, h: 0.3, fontSize: 10, color: DARK_BLUE, fontFace: "Calibri", bold: true, align: "center", valign: "middle"
  });
}

// ====================================================
// SLIDE 9 - EQUIPO AUDITOR
// ====================================================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 1.1, fill: { color: DARK_BLUE }, line: { color: DARK_BLUE } });
  s.addText("07 | EQUIPO AUDITOR", { x: 0.4, y: 0, w: 8, h: 1.1, fontSize: 26, bold: true, color: WHITE, fontFace: "Calibri", valign: "middle" });

  const team = [
    { role: "Jefe de\nAuditoría", profile: "CPC / CIA\n10+ años", color: DARK_BLUE },
    { role: "Auditor Sr.\nFinanciero", profile: "CPC\n5+ años", color: MID_BLUE },
    { role: "Auditor Sr.\nOperativo", profile: "Lic. Admin.\n5+ años", color: "16607A" },
    { role: "Auditor de\nCumplimiento", profile: "Abogado\n3+ años", color: "1B4F8A" },
    { role: "Auditor\nde TI", profile: "Ing. Sistemas\nCISA", color: "28618A" },
  ];

  team.forEach((m, i) => {
    const x = 0.5 + i * 1.82;
    s.addShape(pres.shapes.OVAL, {
      x: x + 0.35, y: 1.3, w: 1.1, h: 1.1,
      fill: { color: m.color }, line: { color: m.color }
    });
    s.addText(m.role.charAt(0), { x: x + 0.35, y: 1.3, w: 1.1, h: 1.1, fontSize: 28, bold: true, color: WHITE, fontFace: "Calibri", align: "center", valign: "middle", margin: 0 });
    s.addText(m.role, { x, y: 2.5, w: 1.8, h: 0.55, fontSize: 11, bold: true, color: DARK_BLUE, fontFace: "Calibri", align: "center" });
    s.addText(m.profile, { x, y: 3.05, w: 1.8, h: 0.45, fontSize: 10, color: "607090", fontFace: "Calibri", align: "center" });
  });

  // Cronograma
  s.addText("CRONOGRAMA RESUMIDO", { x: 0.3, y: 3.65, w: 9.4, h: 0.35, fontSize: 12, bold: true, color: DARK_BLUE, fontFace: "Calibri" });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 4.0, w: 9.4, h: 0.0, fill: { color: MID_BLUE }, line: { color: MID_BLUE } });

  const weeks = [
    { phase: "Planificación", start: 0, len: 3, color: DARK_BLUE },
    { phase: "Trabajo de Campo", start: 3, len: 6, color: MID_BLUE },
    { phase: "Evaluación", start: 9, len: 3, color: "16607A" },
    { phase: "Informe y Cierre", start: 12, len: 4, color: "1B4F8A" },
  ];

  const totalW = 19; // 16 weeks scale + margin
  weeks.forEach((w, i) => {
    const bx = 0.3 + (w.start / totalW) * 9.4;
    const bw = (w.len / totalW) * 9.4 - 0.05;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: bx, y: 4.05, w: bw, h: 0.55,
      fill: { color: w.color }, rectRadius: 0.04, line: { color: w.color }
    });
    s.addText(`${w.phase}\nSem. ${w.start + 1}–${w.start + w.len}`, {
      x: bx, y: 4.05, w: bw, h: 0.55,
      fontSize: 9, color: WHITE, fontFace: "Calibri", align: "center", valign: "middle"
    });
  });
  s.addText("16 Semanas de duración total", { x: 0.3, y: 4.68, w: 9.4, h: 0.25, fontSize: 9, color: "607090", fontFace: "Calibri", align: "center" });
}

// ====================================================
// SLIDE 10 - PRESUPUESTO E INFORME
// ====================================================
{
  const s = pres.addSlide();
  s.background = { color: GRAY };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 1.1, fill: { color: DARK_BLUE }, line: { color: DARK_BLUE } });
  s.addText("08 | PRESUPUESTO E INFORME FINAL", { x: 0.4, y: 0, w: 8, h: 1.1, fontSize: 26, bold: true, color: WHITE, fontFace: "Calibri", valign: "middle" });

  // Budget
  card(s, 0.3, 1.25, 4.5, 3.2, WHITE);
  s.addText("💰  PRESUPUESTO", { x: 0.5, y: 1.35, w: 4.1, h: 0.4, fontSize: 13, bold: true, color: DARK_BLUE, fontFace: "Calibri" });

  const budget = [
    ["Recursos Humanos", "S/ 112,400"],
    ["Software de Auditoría", "S/ 2,500"],
    ["Transporte y Viáticos", "S/ 3,000"],
    ["Materiales y Logística", "S/ 2,600"],
    ["Imprevistos (5%)", "S/ 5,555"],
  ];
  budget.forEach(([concept, amount], i) => {
    const by = 1.85 + i * 0.44;
    s.addText(concept, { x: 0.5, y: by, w: 3.0, h: 0.37, fontSize: 10, color: TEXT_DARK, fontFace: "Calibri", valign: "middle" });
    s.addText(amount, { x: 3.5, y: by, w: 1.1, h: 0.37, fontSize: 10, bold: true, color: MID_BLUE, fontFace: "Calibri", align: "right", valign: "middle" });
  });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 4.0, w: 4.1, h: 0.02, fill: { color: MID_BLUE }, line: { color: MID_BLUE } });
  s.addText("TOTAL ESTIMADO:", { x: 0.5, y: 4.07, w: 2.5, h: 0.35, fontSize: 12, bold: true, color: DARK_BLUE, fontFace: "Calibri" });
  s.addText("S/ 126,055", { x: 3.0, y: 4.07, w: 1.6, h: 0.35, fontSize: 14, bold: true, color: "C8372D", fontFace: "Calibri", align: "right" });

  // Informe
  card(s, 5.1, 1.25, 4.5, 3.2, WHITE);
  s.addText("📄  INFORME FINAL", { x: 5.3, y: 1.35, w: 4.1, h: 0.4, fontSize: 13, bold: true, color: DARK_BLUE, fontFace: "Calibri" });

  const sections = [
    "Resumen ejecutivo con opinión de auditoría",
    "Evaluación del control interno (COSO)",
    "Hallazgos: condición, criterio, causa, efecto",
    "Recomendaciones priorizadas",
    "Matriz de seguimiento",
    "Respuestas de la administración",
  ];
  sections.forEach((sec, i) => {
    s.addShape(pres.shapes.OVAL, { x: 5.3, y: 1.88 + i * 0.41, w: 0.15, h: 0.15, fill: { color: ACCENT }, line: { color: ACCENT } });
    s.addText(sec, { x: 5.5, y: 1.83 + i * 0.41, w: 3.9, h: 0.37, fontSize: 10, color: TEXT_DARK, fontFace: "Calibri", valign: "middle" });
  });

  // Clasificacion hallazgos
  card(s, 0.3, 4.55, 9.4, 0.75, WHITE);
  s.addText("CLASIFICACIÓN DE HALLAZGOS:", { x: 0.5, y: 4.6, w: 2.2, h: 0.6, fontSize: 10, bold: true, color: DARK_BLUE, fontFace: "Calibri", valign: "middle" });
  const cats = [["CRÍTICO", "E74C3C", "30 días"], ["ALTO", "E67E22", "90 días"], ["MEDIO", "F39C12", "180 días"], ["BAJO", "27AE60", "360 días"]];
  cats.forEach(([cat, color, plazo], i) => {
    const cx = 2.9 + i * 1.7;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: cx, y: 4.62, w: 1.5, h: 0.6, fill: { color }, rectRadius: 0.06, line: { color } });
    s.addText(`${cat}\n${plazo}`, { x: cx, y: 4.62, w: 1.5, h: 0.6, fontSize: 9, bold: true, color: WHITE, fontFace: "Calibri", align: "center", valign: "middle" });
  });
}

// ====================================================
// SLIDE 11 - CIERRE
// ====================================================
{
  const s = pres.addSlide();
  s.background = { color: DARK_BLUE };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.08, fill: { color: ACCENT }, line: { color: ACCENT } });

  s.addText("COMPROMISOS CLAVE DE LA AUDITORÍA", {
    x: 0.5, y: 0.5, w: 9, h: 0.6,
    fontSize: 18, bold: true, color: ACCENT, fontFace: "Calibri", align: "center"
  });

  const commitments = [
    { icon: "🔍", title: "Objetividad", desc: "Evaluación imparcial basada en evidencias" },
    { icon: "📊", title: "Rigor Técnico", desc: "NIEPAI, COSO, NAGAS aplicados" },
    { icon: "🤝", title: "Colaboración", desc: "Comunicación continua con el CPPP" },
    { icon: "💡", title: "Mejora Continua", desc: "Recomendaciones accionables y medibles" },
  ];

  commitments.forEach((c, i) => {
    const cx = 0.6 + i * 2.25;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: cx, y: 1.3, w: 2.1, h: 2.4,
      fill: { color: "243B6B" }, rectRadius: 0.1,
      shadow: { type: "outer", color: "000000", blur: 10, offset: 3, angle: 45, opacity: 0.2 }
    });
    s.addText(c.icon, { x: cx, y: 1.4, w: 2.1, h: 0.7, fontSize: 30, fontFace: "Calibri", align: "center" });
    s.addText(c.title, { x: cx + 0.1, y: 2.1, w: 1.9, h: 0.45, fontSize: 14, bold: true, color: WHITE, fontFace: "Calibri", align: "center" });
    s.addText(c.desc, { x: cx + 0.1, y: 2.6, w: 1.9, h: 0.8, fontSize: 10, color: "8BB8E8", fontFace: "Calibri", align: "center" });
  });

  s.addShape(pres.shapes.RECTANGLE, { x: 1, y: 4.0, w: 8, h: 0.03, fill: { color: ACCENT }, line: { color: ACCENT } });

  s.addText("\"La auditoría integral no es un fin en sí misma, sino el punto de partida para\n una gestión universitaria más transparente, eficiente y confiable.\"", {
    x: 0.5, y: 4.1, w: 9, h: 0.85,
    fontSize: 12, italics: true, color: "A8C8F0", fontFace: "Calibri", align: "center"
  });

  s.addText("Plan de Auditoría Integral  •  CPPP - Universidad Peruana Unión  •  Lima, Perú 2025", {
    x: 0.5, y: 5.1, w: 9, h: 0.3,
    fontSize: 10, color: "607090", fontFace: "Calibri", align: "center"
  });

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.545, w: 10, h: 0.08, fill: { color: ACCENT }, line: { color: ACCENT } });
}

// Modify the path to save directly in the workspace directory (parent of ppt_generator)
pres.writeFile({ fileName: "../Plan_Auditoria_Integral_UPeU.pptx" })
  .then(() => console.log("PPTX created successfully"))
  .catch(err => console.error(err));
