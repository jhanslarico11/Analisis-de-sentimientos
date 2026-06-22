const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, VerticalAlign, PageBreak, LevelFormat,
  TableOfContents, SimpleField
} = require('docx');
const fs = require('fs');

const DARK_BLUE = "1B3A6B";
const MID_BLUE  = "2E75B6";
const LIGHT_BLUE = "D6E4F5";
const ACCENT = "E8A020";
const TEXT = "1A1A2E";
const GRAY = "595959";

const border = { style: BorderStyle.SINGLE, size: 1, color: "B8CCE4" };
const borders = { top: border, bottom: border, left: border, right: border };
const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 180 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: MID_BLUE, space: 6 } },
    children: [new TextRun({ text, bold: true, size: 32, color: DARK_BLUE, font: "Arial" })]
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 140 },
    children: [new TextRun({ text, bold: true, size: 26, color: MID_BLUE, font: "Arial" })]
  });
}

function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 200, after: 100 },
    children: [new TextRun({ text, bold: true, size: 22, color: DARK_BLUE, font: "Arial" })]
  });
}

function body(text, opts = {}) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { before: 80, after: 80, line: 330 },
    children: [new TextRun({ text, size: 22, color: TEXT, font: "Arial", ...opts })]
  });
}

function bullet(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "bullets", level },
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text, size: 22, color: TEXT, font: "Arial" })]
  });
}

function numbered(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "numbers", level },
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text, size: 22, color: TEXT, font: "Arial" })]
  });
}

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

function spacer(n = 1) {
  return Array(n).fill(new Paragraph({ spacing: { before: 60, after: 60 }, children: [new TextRun("")] }));
}

function infoTable(rows) {
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [2800, 6560],
    rows: rows.map(([label, value], i) => new TableRow({
      children: [
        new TableCell({
          borders,
          width: { size: 2800, type: WidthType.DXA },
          shading: { fill: i === 0 ? DARK_BLUE : LIGHT_BLUE, type: ShadingType.CLEAR },
          margins: { top: 100, bottom: 100, left: 140, right: 140 },
          children: [new Paragraph({
            children: [new TextRun({ text: label, bold: true, size: 20, color: i === 0 ? "FFFFFF" : DARK_BLUE, font: "Arial" })]
          })]
        }),
        new TableCell({
          borders,
          width: { size: 6560, type: WidthType.DXA },
          shading: { fill: i === 0 ? MID_BLUE : "FFFFFF", type: ShadingType.CLEAR },
          margins: { top: 100, bottom: 100, left: 140, right: 140 },
          children: [new Paragraph({
            children: [new TextRun({ text: value, bold: i === 0, size: 20, color: i === 0 ? "FFFFFF" : TEXT, font: "Arial" })]
          })]
        })
      ]
    }))
  });
}

function headerTable(cols, rows) {
  const colW = Math.floor(9360 / cols.length);
  const colWidths = cols.map(() => colW);

  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [
      new TableRow({
        children: cols.map(c => new TableCell({
          borders,
          width: { size: colW, type: WidthType.DXA },
          shading: { fill: DARK_BLUE, type: ShadingType.CLEAR },
          margins: { top: 100, bottom: 100, left: 120, right: 120 },
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: c, bold: true, size: 20, color: "FFFFFF", font: "Arial" })]
          })]
        }))
      }),
      ...rows.map((row, ri) => new TableRow({
        children: row.map(cell => new TableCell({
          borders,
          width: { size: colW, type: WidthType.DXA },
          shading: { fill: ri % 2 === 0 ? "FFFFFF" : "EBF3FA", type: ShadingType.CLEAR },
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          children: [new Paragraph({
            children: [new TextRun({ text: cell, size: 20, color: TEXT, font: "Arial" })]
          })]
        }))
      }))
    ]
  });
}

const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }, {
          level: 1, format: LevelFormat.BULLET, text: "\u25E6",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 1080, hanging: 360 } } }
        }]
      },
      {
        reference: "numbers",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      }
    ]
  },
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial", color: DARK_BLUE },
        paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 0 }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Arial", color: MID_BLUE },
        paragraph: { spacing: { before: 280, after: 140 }, outlineLevel: 1 }
      },
      {
        id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 22, bold: true, font: "Arial", color: DARK_BLUE },
        paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 2 }
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1260, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({
        children: [
          new Paragraph({
            border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: MID_BLUE, space: 4 } },
            children: [
              new TextRun({ text: "PLAN DE AUDITORIA INTEGRAL - UNIVERSIDAD PERUANA UNION  |  ", bold: true, size: 18, color: DARK_BLUE, font: "Arial" }),
              new TextRun({ text: "Centro de Practicas Pre Profesionales", size: 18, color: GRAY, font: "Arial" })
            ]
          })
        ]
      })
    },
    footers: {
      default: new Footer({
        children: [
          new Paragraph({
            border: { top: { style: BorderStyle.SINGLE, size: 6, color: MID_BLUE, space: 4 } },
            tabStops: [{ type: "right", position: 9360 }],
            children: [
              new TextRun({ text: "Confidencial - Uso Interno  \t", size: 16, color: GRAY, font: "Arial" }),
              new TextRun({ text: "Pagina ", size: 16, color: GRAY, font: "Arial" }),
              new SimpleField("PAGE"),
              new TextRun({ text: " de ", size: 16, color: GRAY, font: "Arial" }),
              new SimpleField("NUMPAGES")
            ]
          })
        ]
      })
    },
    children: [
      // =========================================================
      // PORTADA
      // =========================================================
      new Paragraph({ spacing: { before: 800, after: 200 }, children: [new TextRun("")] }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 120 },
        children: [new TextRun({ text: "UNIVERSIDAD PERUANA UNION", bold: true, size: 44, color: DARK_BLUE, font: "Arial" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 60 },
        children: [new TextRun({ text: "Facultad de Ciencias Empresariales", size: 28, color: MID_BLUE, font: "Arial" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 400 },
        children: [new TextRun({ text: "Escuela Profesional de Contabilidad y Auditoria", size: 24, color: GRAY, font: "Arial" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 200, after: 200 },
        border: {
          top: { style: BorderStyle.SINGLE, size: 12, color: ACCENT, space: 8 },
          bottom: { style: BorderStyle.SINGLE, size: 12, color: ACCENT, space: 8 }
        },
        children: [
          new TextRun({ text: "PLAN DE AUDITORIA INTEGRAL", bold: true, size: 52, color: DARK_BLUE, font: "Arial" }),
          new TextRun({ break: 1 }),
          new TextRun({ text: "Centro de Practicas Pre Profesionales", bold: true, size: 32, color: MID_BLUE, font: "Arial" })
        ]
      }),
      new Paragraph({ spacing: { before: 400, after: 100 }, children: [new TextRun("")] }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 60 },
        children: [new TextRun({ text: "Elaborado por:", bold: true, size: 22, color: DARK_BLUE, font: "Arial" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 60 },
        children: [new TextRun({ text: "Equipo de Auditoria Interna", size: 22, color: TEXT, font: "Arial" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 60 },
        children: [new TextRun({ text: "Lima, Peru - 2025", size: 22, color: GRAY, font: "Arial" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 60 },
        children: [new TextRun({ text: "Version 1.0 - Confidencial", size: 20, color: GRAY, font: "Arial", italics: true })]
      }),

      pageBreak(),

      // =========================================================
      // TABLA DE INFORMACION GENERAL
      // =========================================================
      h1("INFORMACION GENERAL DEL PLAN"),
      ...spacer(1),
      infoTable([
        ["DOCUMENTO", "Plan de Auditoria Integral"],
        ["Entidad auditada", "Universidad Peruana Union (UPeU)"],
        ["Unidad auditada", "Centro de Practicas Pre Profesionales"],
        ["Tipo de auditoria", "Integral (Financiera, Operativa, Cumplimiento, Gestion)"],
        ["Periodo auditado", "Ejercicio 2024 - 2025"],
        ["Fecha de elaboracion", "Julio 2025"],
        ["Equipo auditor", "Auditoria Interna Institucional"],
        ["Responsable", "Jefe de Auditoria Interna"],
        ["Clasificacion", "Documento Confidencial - Uso Interno"],
        ["Version", "1.0 - Aprobado"],
      ]),

      pageBreak(),

      // =========================================================
      // 1. INTRODUCCION
      // =========================================================
      h1("1. INTRODUCCION"),
      body("La Universidad Peruana Union (UPeU) es una institucion de educacion superior privada de confesion adventista, con sede principal en Lima y campus en las ciudades de Juliaca y Tarapoto. Como parte de su compromiso con la excelencia academica y la transparencia institucional, la UPeU cuenta con el Centro de Practicas Pre Profesionales (CPPP), unidad academica-administrativa que articula la formacion practica de los estudiantes con el sector productivo y de servicios."),
      ...spacer(1),
      body("El presente Plan de Auditoria Integral constituye el documento rector que orienta, organiza y sistematiza el proceso de evaluacion independiente del Centro de Practicas Pre Profesionales. Este plan ha sido elaborado en concordancia con las Normas Internacionales para el Ejercicio Profesional de la Auditoria Interna (NIEPAI), las Normas de Auditoria Generalmente Aceptadas (NAGAS), la Ley Universitaria N.° 30220, el Estatuto de la Universidad Peruana Union, y los lineamientos emitidos por la Superintendencia Nacional de Educacion Superior Universitaria (SUNEDU)."),
      ...spacer(1),
      body("La auditoria integral tiene como proposito emitir una opinion tecnica y objetiva sobre la eficiencia, eficacia, economica, legalidad, y transparencia de las operaciones del CPPP, identificando areas de mejora, riesgos no controlados y oportunidades de fortalecimiento institucional."),

      h2("1.1 Antecedentes del Centro de Practicas Pre Profesionales"),
      body("El Centro de Practicas Pre Profesionales de la UPeU fue creado como respuesta a las exigencias de la Ley Universitaria N.° 30220 y las condiciones de licenciamiento de SUNEDU, que establecen que las universidades deben garantizar que sus estudiantes realicen practicas vinculadas a su formacion profesional. Desde su creacion, el CPPP ha articulado convenios con entidades publicas, privadas y organizaciones de la sociedad civil, facilitando la insercion temprana de los estudiantes al mercado laboral."),
      ...spacer(1),
      body("No obstante, el crecimiento acelerado de la demanda de plazas de practicas, el incremento del numero de convenios institucionales y la diversificacion de carreras que utilizan la plataforma han generado una complejidad operativa que requiere una evaluacion sistematica y rigorosa de sus procesos."),

      h2("1.2 Marco Normativo Aplicable"),
      bullet("Ley N.° 30220 - Ley Universitaria y sus modificatorias"),
      bullet("Ley N.° 28518 - Ley sobre modalidades formativas laborales"),
      bullet("Decreto Supremo N.° 007-2005-TR - Reglamento de la Ley N.° 28518"),
      bullet("Ley N.° 28716 - Ley de Control Interno de las Entidades del Estado (aplicacion referencial)"),
      bullet("Estatuto de la Universidad Peruana Union - Version vigente 2024"),
      bullet("Reglamento de Practicas Pre Profesionales UPeU"),
      bullet("Normas Internacionales para el Ejercicio Profesional de la Auditoria Interna (NIEPAI - IIA)"),
      bullet("Marco Integrado de Control Interno COSO 2013"),
      bullet("Normas de Auditoria Generalmente Aceptadas (NAGAS)"),
      bullet("Lineamientos SUNEDU para el licenciamiento institucional"),

      pageBreak(),

      // =========================================================
      // 2. OBJETIVOS
      // =========================================================
      h1("2. OBJETIVOS DE LA AUDITORIA"),

      h2("2.1 Objetivo General"),
      body("Realizar una auditoria integral al Centro de Practicas Pre Profesionales de la Universidad Peruana Union para evaluar de manera objetiva e independiente la gestion administrativa, financiera, operativa y el cumplimiento normativo de la unidad, con el proposito de emitir un informe tecnico que contribuya a la mejora continua, al fortalecimiento del control interno y a la transparencia institucional."),

      h2("2.2 Objetivos Especificos"),
      numbered("Evaluar la estructura organizacional y el modelo de gobierno del Centro de Practicas Pre Profesionales, identificando brechas en la definicion de roles, funciones y responsabilidades."),
      numbered("Verificar el cumplimiento de la normativa legal vigente aplicable a las practicas pre profesionales, incluyendo la Ley N.° 28518 y el Reglamento de Practicas de la UPeU."),
      numbered("Examinar la gestion de los convenios institucionales con empresas, entidades publicas y organizaciones aliadas, evaluando los procesos de suscripcion, seguimiento y renovacion."),
      numbered("Analizar los procesos de asignacion, supervision y evaluacion de practicantes, identificando controles existentes y deficiencias en la cadena de valor del servicio."),
      numbered("Revisar el manejo de los recursos financieros asignados al CPPP, verificando la correcta ejecucion presupuestal y la pertinencia de los gastos realizados."),
      numbered("Evaluar los sistemas de informacion utilizados para la gestion de practicas, identificando riesgos de integridad, disponibilidad y confidencialidad de los datos."),
      numbered("Identificar los principales riesgos operativos, de cumplimiento y estrategicos que afectan la continuidad y calidad del servicio prestado por el CPPP."),
      numbered("Formular recomendaciones de mejora orientadas al fortalecimiento del control interno, la eficiencia operativa y el alineamiento estrategico con el Plan Estrategico Institucional de la UPeU."),

      pageBreak(),

      // =========================================================
      // 3. ALCANCE
      // =========================================================
      h1("3. ALCANCE DE LA AUDITORIA"),

      h2("3.1 Ambito Organizacional"),
      body("La auditoria comprende la totalidad de las operaciones, procesos y actividades del Centro de Practicas Pre Profesionales de la UPeU, incluyendo sus interacciones con las Facultades, la Direccion de Bienestar Universitario, la Direccion de Recursos Humanos, la Oficina de Asesoria Legal y la Direccion General de Administracion y Finanzas."),

      h2("3.2 Periodo de la Auditoria"),
      body("El periodo objeto de evaluacion comprende los ejercicios academicos y administrativos 2024 y 2025, con enfasis en los procesos activos al momento de la intervencion auditora. Se podra extender el periodo de revision cuando sea necesario para establecer comparaciones, identificar tendencias o evaluar el cumplimiento de recomendaciones de auditorias anteriores."),

      h2("3.3 Areas y Procesos Auditados"),
      headerTable(
        ["N°", "Area / Proceso", "Tipo de Auditoria", "Prioridad"],
        [
          ["1", "Gestion Administrativa General del CPPP", "Operativa / Gestion", "Alta"],
          ["2", "Convenios con Empresas e Instituciones", "Cumplimiento / Legal", "Alta"],
          ["3", "Proceso de Asignacion de Practicantes", "Operativa", "Alta"],
          ["4", "Supervision y Evaluacion de Practicantes", "Operativa / Calidad", "Alta"],
          ["5", "Gestion Presupuestal y Financiera", "Financiera", "Alta"],
          ["6", "Sistemas de Informacion y Tecnologia", "TI / Seguridad", "Media"],
          ["7", "Recursos Humanos del CPPP", "Operativa", "Media"],
          ["8", "Comunicacion e Imagen Institucional", "Gestion", "Baja"],
          ["9", "Seguimiento a Egresados", "Gestion", "Media"],
          ["10", "Cumplimiento Normativo SUNEDU", "Cumplimiento", "Alta"],
        ]
      ),

      pageBreak(),

      // =========================================================
      // 4. METODOLOGIA
      // =========================================================
      h1("4. METODOLOGIA DE LA AUDITORIA"),

      h2("4.1 Enfoque Metodologico"),
      body("La auditoria integral se desarrollara bajo un enfoque mixto que combina metodologias cuantitativas y cualitativas. Se aplicara el Marco Integrado de Control Interno COSO 2013 como referente para la evaluacion de los componentes del control interno, y la metodologia de gestion de riesgos COSO ERM 2017 para la identificacion, evaluacion y respuesta a los riesgos identificados."),

      h2("4.2 Fases de la Auditoria"),

      h3("Fase I - Planificacion (Semanas 1-3)"),
      bullet("Reunion de apertura con la alta direccion del CPPP y autoridades universitarias"),
      bullet("Recopilacion y analisis de documentacion institucional (estatutos, manuales, reglamentos)"),
      bullet("Aplicacion de cuestionarios de evaluacion del control interno"),
      bullet("Elaboracion de la matriz de riesgos preliminar"),
      bullet("Definicion del programa de auditoria detallado y distribucion de responsabilidades"),
      bullet("Solicitud formal de informacion a las areas involucradas"),

      h3("Fase II - Trabajo de Campo (Semanas 4-9)"),
      bullet("Entrevistas estructuradas con directivos, coordinadores y personal operativo"),
      bullet("Observacion directa de procesos operativos criticos"),
      bullet("Revision y analisis de expedientes, contratos y convenios"),
      bullet("Pruebas de cumplimiento sobre controles seleccionados"),
      bullet("Pruebas sustantivas sobre transacciones financieras significativas"),
      bullet("Analisis de bases de datos e informes estadisticos del CPPP"),
      bullet("Aplicacion de tecnicas de muestreo estadistico y no estadistico"),
      bullet("Verificacion del cumplimiento de requisitos SUNEDU"),

      h3("Fase III - Evaluacion y Analisis (Semanas 10-12)"),
      bullet("Procesamiento y triangulacion de evidencias recopiladas"),
      bullet("Elaboracion de la matriz de hallazgos con causa, efecto y condicion"),
      bullet("Actualizacion de la matriz de riesgos con hallazgos identificados"),
      bullet("Reunion de avance con la gerencia del CPPP para comunicar hallazgos preliminares"),
      bullet("Revision de respuestas y comentarios de la administracion"),

      h3("Fase IV - Informe y Seguimiento (Semanas 13-16)"),
      bullet("Elaboracion del borrador del Informe de Auditoria Integral"),
      bullet("Reunion de cierre con autoridades del CPPP y la UPeU"),
      bullet("Emision del Informe Final de Auditoria"),
      bullet("Comunicacion de resultados a los organos de gobierno competentes"),
      bullet("Elaboracion del Plan de Implementacion de Recomendaciones"),
      bullet("Programacion del seguimiento a la implementacion de mejoras"),

      h2("4.3 Tecnicas de Auditoria a Emplear"),
      headerTable(
        ["Tecnica", "Descripcion", "Aplicacion"],
        [
          ["Entrevista", "Conversaciones estructuradas con funcionarios clave", "Todas las fases"],
          ["Cuestionario", "Instrumentos de evaluacion de control interno", "Fase I y II"],
          ["Observacion", "Verificacion directa de procesos y condiciones fisicas", "Fase II"],
          ["Revision documental", "Analisis de expedientes, contratos y registros", "Fase II"],
          ["Muestreo estadistico", "Seleccion representativa de transacciones", "Fase II"],
          ["Analisis de datos", "Procesamiento de bases de datos institucionales", "Fase II y III"],
          ["Conciliacion", "Verificacion cruzada de informacion entre fuentes", "Fase II y III"],
          ["Calculo y recalculo", "Verificacion de operaciones aritmeticas y formulas", "Fase II"],
          ["Confirmacion", "Verificacion con terceros (empresas, practicantes)", "Fase II"],
          ["Inspeccion fisica", "Verificacion de bienes, equipos e instalaciones", "Fase II"],
        ]
      ),

      pageBreak(),

      // =========================================================
      // 5. EVALUACION DE RIESGOS
      // =========================================================
      h1("5. EVALUACION DE RIESGOS"),

      h2("5.1 Metodologia de Evaluacion"),
      body("La identificacion y evaluacion de riesgos se realiza mediante una matriz biaxial que considera dos dimensiones: la Probabilidad de ocurrencia (P) y el Impacto potencial (I), ambas calificadas en una escala del 1 al 5. El nivel de riesgo inherente se calcula como el producto P x I, clasificandose en cuatro categorias: Bajo (1-4), Medio (5-9), Alto (10-15) y Critico (16-25)."),

      h2("5.2 Matriz de Riesgos Principales"),
      headerTable(
        ["Riesgo Identificado", "P", "I", "Nivel", "Control Sugerido"],
        [
          ["Convenios sin actualizacion legal", "4", "5", "CRITICO", "Auditoria legal periodica"],
          ["Incumplimiento Ley N.° 28518", "3", "5", "ALTO", "Comite de cumplimiento"],
          ["Practicantes sin supervision adecuada", "4", "4", "ALTO", "Sistema de monitoreo"],
          ["Perdida de datos de practicantes", "3", "4", "ALTO", "Backup y plan de contingencia"],
          ["Fraude en documentacion", "2", "5", "ALTO", "Control documental riguroso"],
          ["Incumplimiento SUNEDU", "2", "5", "ALTO", "Monitoreo de indicadores"],
          ["Rotacion alta de personal CPPP", "4", "3", "MEDIO", "Plan de retencion de talentos"],
          ["Deficit presupuestal", "3", "3", "MEDIO", "Presupuesto participativo"],
          ["Sistemas desactualizados", "3", "3", "MEDIO", "Plan de modernizacion TI"],
          ["Insatisfaccion de practicantes", "3", "2", "MEDIO", "Encuestas de satisfaccion"],
        ]
      ),
      ...spacer(1),
      body("Nota: P = Probabilidad (1-5), I = Impacto (1-5). Critico: 16-25 / Alto: 10-15 / Medio: 5-9 / Bajo: 1-4."),

      h2("5.3 Riesgos Emergentes"),
      body("Se han identificado los siguientes riesgos emergentes que, si bien pueden no tener una materializacion inmediata, requieren atencion preventiva dado el entorno cambiante en el que opera el CPPP:"),
      bullet("Riesgo de ciberseguridad: exposicion de datos personales de practicantes ante ataques informaticos o accesos no autorizados a los sistemas de informacion del CPPP."),
      bullet("Riesgo regulatorio: cambios en la normativa universitaria o laboral que puedan afectar los modelos de convenio vigentes o los requisitos de las practicas formativas."),
      bullet("Riesgo reputacional: impacto negativo en la imagen de la UPeU derivado de incidentes relacionados con el bienestar o la seguridad de los practicantes en las empresas aliadas."),
      bullet("Riesgo tecnologico: dependencia de plataformas digitales para la gestion de practicas que podrian presentar fallas de disponibilidad o interoperabilidad."),

      pageBreak(),

      // =========================================================
      // 6. PROGRAMA DE AUDITORIA
      // =========================================================
      h1("6. PROGRAMA DE AUDITORIA DETALLADO"),

      h2("6.1 Auditoria Financiera"),
      body("La auditoria financiera tendra como objetivo verificar que los estados financieros del CPPP reflejan razonablemente la situacion financiera de la unidad y que los recursos se han utilizado conforme a las normas y politicas institucionales."),
      ...spacer(1),
      headerTable(
        ["N°", "Procedimiento de Auditoria", "Objetivo", "Responsable"],
        [
          ["F01", "Revision del presupuesto asignado vs ejecutado", "Eficiencia presupuestal", "Auditor Senior"],
          ["F02", "Analisis de transferencias y fondos recibidos", "Legalidad financiera", "Auditor Senior"],
          ["F03", "Verificacion de facturas y comprobantes de pago", "Documentacion contable", "Auditor Junior"],
          ["F04", "Conciliacion bancaria de cuentas del CPPP", "Integridad financiera", "Auditor Senior"],
          ["F05", "Revision de planilla de personal y boletas", "Gestion de RRHH", "Auditor Junior"],
          ["F06", "Evaluacion de gastos por servicios de terceros", "Control de contratos", "Auditor Junior"],
          ["F07", "Verificacion de activos fijos asignados", "Salvaguarda de activos", "Auditor Junior"],
          ["F08", "Analisis de ingresos por convenios con empresas", "Integridad de ingresos", "Auditor Senior"],
        ]
      ),

      h2("6.2 Auditoria Operativa"),
      body("La auditoria operativa evaluara la eficiencia y efectividad de los procesos clave del CPPP, identificando oportunidades de mejora en la gestion operativa."),
      ...spacer(1),
      headerTable(
        ["N°", "Procedimiento de Auditoria", "Objetivo", "Responsable"],
        [
          ["O01", "Mapeo y analisis del proceso de asignacion de practicantes", "Eficiencia operativa", "Auditor Senior"],
          ["O02", "Revision de fichas de supervision de practicantes", "Calidad del seguimiento", "Auditor Junior"],
          ["O03", "Evaluacion del proceso de evaluacion final de practicantes", "Objetividad evaluativa", "Auditor Junior"],
          ["O04", "Analisis del proceso de gestion de convenios", "Control contractual", "Auditor Senior"],
          ["O05", "Revision de tiempos de respuesta en atencion al estudiante", "Eficiencia de servicio", "Auditor Junior"],
          ["O06", "Evaluacion del proceso de registro y certificacion", "Integridad documental", "Auditor Junior"],
          ["O07", "Observacion de procesos de induccion a practicantes", "Calidad formativa", "Auditor Junior"],
          ["O08", "Analisis de indicadores de gestion del CPPP", "Medicion de resultados", "Auditor Senior"],
        ]
      ),

      h2("6.3 Auditoria de Cumplimiento"),
      body("La auditoria de cumplimiento verificara que las operaciones del CPPP se ajustan a las disposiciones legales, reglamentarias e institucionales aplicables."),
      ...spacer(1),
      headerTable(
        ["N°", "Procedimiento de Auditoria", "Norma Aplicable", "Responsable"],
        [
          ["C01", "Verificacion cumplimiento Ley N.° 28518", "Ley 28518 y DS 007-2005-TR", "Auditor Senior"],
          ["C02", "Revision de condiciones minimas en convenios", "Ley Universitaria 30220", "Auditor Legal"],
          ["C03", "Verificacion de seguros de practicantes", "DS 007-2005-TR Art. 51", "Auditor Junior"],
          ["C04", "Cumplimiento de jornada maxima de practicas", "Ley 28518 Art. 45", "Auditor Junior"],
          ["C05", "Revision de subvencion economica minima", "Ley 28518 Art. 46", "Auditor Junior"],
          ["C06", "Verificacion de reportes a SUNEDU", "Condicion de licenciamiento", "Auditor Senior"],
          ["C07", "Revision de planes de practicas por carrera", "Reglamento UPeU", "Auditor Junior"],
          ["C08", "Cumplimiento del Reglamento Interno UPeU", "Estatuto UPeU", "Auditor Junior"],
        ]
      ),

      h2("6.4 Auditoria de Tecnologias de Informacion"),
      body("La auditoria de TI evaluara los controles sobre los sistemas de informacion utilizados en la gestion de practicas, incluyendo la integridad de los datos, la seguridad de acceso y la continuidad del servicio tecnologico."),
      ...spacer(1),
      bullet("Revision de la arquitectura del sistema de gestion de practicas"),
      bullet("Evaluacion de controles de acceso logico y perfiles de usuario"),
      bullet("Verificacion de politicas de respaldo y recuperacion de informacion"),
      bullet("Analisis de la integridad de los datos registrados en el sistema"),
      bullet("Evaluacion del cumplimiento de la Ley N.° 29733 - Ley de Proteccion de Datos Personales"),
      bullet("Revision de los controles de seguridad en la infraestructura tecnologica"),
      bullet("Evaluacion del plan de continuidad del negocio relacionado con TI"),

      pageBreak(),

      // =========================================================
      // 7. EQUIPO AUDITOR
      // =========================================================
      h1("7. EQUIPO AUDITOR Y RESPONSABILIDADES"),

      h2("7.1 Composicion del Equipo"),
      headerTable(
        ["Cargo", "Perfil Requerido", "Responsabilidades Principales"],
        [
          ["Jefe de Auditoria Interna", "CPC, CIA, 10+ anos experiencia", "Supervision general, aprobacion del informe final"],
          ["Auditor Senior Financiero", "CPC, 5+ anos auditoria financiera", "Pruebas financieras, analisis presupuestal"],
          ["Auditor Senior Operativo", "Lic. Admin./Ing. Industrial, 5 anos", "Mapeo de procesos, evaluacion operativa"],
          ["Auditor de Cumplimiento", "Abogado, 3+ anos derecho laboral/edu.", "Verificacion legal y normativa"],
          ["Auditor de TI", "Ing. de Sistemas, CISA o similar", "Auditoria de sistemas de informacion"],
          ["Auditor Junior 1", "CPC o Bachiller Contabilidad", "Apoyo en pruebas financieras"],
          ["Auditor Junior 2", "Bachiller Administracion", "Apoyo en trabajo de campo operativo"],
          ["Asistente Administrativo", "Tecnico en administracion", "Soporte logistico y documental"],
        ]
      ),

      h2("7.2 Cronograma de Trabajo"),
      headerTable(
        ["Fase", "Actividad Principal", "Semanas", "Responsable"],
        [
          ["Planificacion", "Levantamiento de informacion, matriz de riesgos", "1-3", "Jefe Auditoria + Seniors"],
          ["Trabajo de Campo - Financiero", "Pruebas financieras y presupuestales", "4-6", "Auditor Senior Financiero"],
          ["Trabajo de Campo - Operativo", "Revision de procesos y convenios", "4-7", "Auditor Senior Operativo"],
          ["Trabajo de Campo - Cumplimiento", "Revision normativa y legal", "5-8", "Auditor de Cumplimiento"],
          ["Trabajo de Campo - TI", "Auditoria de sistemas", "6-9", "Auditor de TI"],
          ["Evaluacion y Analisis", "Procesamiento de hallazgos", "10-12", "Todo el equipo"],
          ["Informe y Cierre", "Redaccion y emision del informe", "13-16", "Jefe Auditoria + Seniors"],
        ]
      ),

      pageBreak(),

      // =========================================================
      // 8. COMUNICACION Y REPORTES
      // =========================================================
      h1("8. COMUNICACION DE RESULTADOS"),

      h2("8.1 Estructura del Informe Final"),
      body("El Informe de Auditoria Integral sera estructurado conforme a los estandares del Instituto de Auditores Internos (IIA) y constara de las siguientes secciones:"),
      numbered("Carta de presentacion del Jefe de Auditoria"),
      numbered("Resumen ejecutivo con principales hallazgos y opinion de auditoria"),
      numbered("Descripcion del alcance, objetivos y metodologia"),
      numbered("Evaluacion del control interno (componentes COSO)"),
      numbered("Hallazgos detallados con condicion, criterio, causa, efecto y recomendacion"),
      numbered("Matriz de seguimiento de recomendaciones"),
      numbered("Respuestas de la administracion del CPPP"),
      numbered("Anexos: evidencias, cuestionarios, muestras y documentacion soporte"),

      h2("8.2 Clasificacion de Hallazgos"),
      headerTable(
        ["Categoria", "Descripcion", "Plazo de Atencion"],
        [
          ["Critico", "Riesgos que amenazan la continuidad o legalidad del CPPP", "Inmediato (30 dias)"],
          ["Alto", "Deficiencias significativas en controles clave", "Corto plazo (90 dias)"],
          ["Medio", "Oportunidades de mejora en procesos operativos", "Mediano plazo (180 dias)"],
          ["Bajo", "Recomendaciones de buenas practicas", "Largo plazo (360 dias)"],
        ]
      ),

      h2("8.3 Destinatarios del Informe"),
      bullet("Rector de la Universidad Peruana Union"),
      bullet("Vicerrector Academico"),
      bullet("Vicerrector de Administracion"),
      bullet("Director del Centro de Practicas Pre Profesionales"),
      bullet("Decanos de Facultades participantes"),
      bullet("Consejo Universitario (para conocimiento)"),
      bullet("Organo de Control Institucional (cuando corresponda)"),

      pageBreak(),

      // =========================================================
      // 9. CRITERIOS DE AUDITORIA
      // =========================================================
      h1("9. CRITERIOS Y ESTANDARES DE AUDITORIA"),

      h2("9.1 Criterios de Evaluacion"),
      body("Los criterios de auditoria son los parametros, estandares, normas, indicadores y principios utilizados para comparar la situacion encontrada (condicion) y determinar si existe o no una deficiencia (hallazgo). Para el presente plan se utilizaran los siguientes criterios:"),
      ...spacer(1),
      bullet("Criterios normativos: disposiciones legales y reglamentarias vigentes aplicables al CPPP"),
      bullet("Criterios institucionales: manuales de procedimientos, reglamentos internos y politicas de la UPeU"),
      bullet("Criterios tecnicos: estandares internacionales de gestion (ISO, COSO, COBIT)"),
      bullet("Criterios comparativos: mejores practicas de instituciones universitarias similares"),
      bullet("Criterios de eficiencia: metas e indicadores establecidos en el Plan Operativo del CPPP"),

      h2("9.2 Indicadores de Gestion Auditados"),
      headerTable(
        ["Indicador", "Formula", "Meta Esperada"],
        [
          ["Tasa de colocacion de practicantes", "(Practicantes colocados / Solicitudes) x 100", ">= 85%"],
          ["Convenios vigentes activos", "Convenios con vigencia >= 1 ano", ">= 80% del total"],
          ["Cumplimiento de evaluaciones", "(Evaluaciones realizadas / Programadas) x 100", "100%"],
          ["Satisfaccion de practicantes", "Encuesta de satisfaccion (escala 1-5)", ">= 4.0"],
          ["Satisfaccion de empresas aliadas", "Encuesta de satisfaccion (escala 1-5)", ">= 4.0"],
          ["Tasa de incidentes laborales", "(Incidentes / Total practicantes) x 1000", "< 5 por mil"],
          ["Practicantes con seguro vigente", "(Con seguro / Total practicantes) x 100", "100%"],
          ["Ejecucion presupuestal", "(Ejecutado / Aprobado) x 100", "90-100%"],
        ]
      ),

      pageBreak(),

      // =========================================================
      // 10. PRESUPUESTO DE LA AUDITORIA
      // =========================================================
      h1("10. PRESUPUESTO ESTIMADO DE LA AUDITORIA"),

      h2("10.1 Recursos Humanos"),
      headerTable(
        ["Cargo", "Horas estimadas", "Costo por hora (S/)", "Total estimado (S/)"],
        [
          ["Jefe de Auditoria Interna", "120", "S/ 150", "S/ 18,000"],
          ["Auditor Senior Financiero", "200", "S/ 90", "S/ 18,000"],
          ["Auditor Senior Operativo", "200", "S/ 90", "S/ 18,000"],
          ["Auditor de Cumplimiento Legal", "160", "S/ 90", "S/ 14,400"],
          ["Auditor de TI", "160", "S/ 90", "S/ 14,400"],
          ["Auditor Junior 1", "240", "S/ 50", "S/ 12,000"],
          ["Auditor Junior 2", "240", "S/ 50", "S/ 12,000"],
          ["Asistente Administrativo", "160", "S/ 35", "S/ 5,600"],
          ["TOTAL RECURSOS HUMANOS", "1,480", "-", "S/ 112,400"],
        ]
      ),

      h2("10.2 Recursos Materiales y Logisticos"),
      headerTable(
        ["Concepto", "Descripcion", "Monto estimado (S/)"],
        [
          ["Utiles de oficina", "Papel, impresion, archivadores", "S/ 800"],
          ["Software de auditoria", "Licencias IDEA o ACL (3 meses)", "S/ 2,500"],
          ["Transporte y viaticos", "Visitas a campus y empresas aliadas", "S/ 3,000"],
          ["Comunicaciones", "Telefono, internet, videoconferencias", "S/ 600"],
          ["Capacitacion del equipo", "Actualizacion en normas y tecnicas", "S/ 1,200"],
          ["Imprevistos (5%)", "Contingencias no previstas", "S/ 5,555"],
          ["TOTAL MATERIALES", "-", "S/ 13,655"],
        ]
      ),
      ...spacer(1),
      body("PRESUPUESTO TOTAL ESTIMADO: S/ 126,055 soles.", { bold: true, size: 24, color: DARK_BLUE }),

      pageBreak(),

      // =========================================================
      // 11. CONTROL DE CALIDAD
      // =========================================================
      h1("11. CONTROL DE CALIDAD DE LA AUDITORIA"),

      body("El proceso de auditoria estara sujeto a controles de calidad en cada una de sus fases, con el objetivo de garantizar que los procedimientos aplicados, las evidencias recopiladas, los hallazgos identificados y las recomendaciones formuladas cumplan con los estandares profesionales establecidos."),

      h2("11.1 Mecanismos de Control de Calidad"),
      bullet("Supervision continua por parte del Jefe de Auditoria en todas las fases del proceso"),
      bullet("Revision cruzada de papeles de trabajo entre miembros del equipo auditor"),
      bullet("Aplicacion de listas de verificacion (checklists) de cumplimiento metodologico"),
      bullet("Revision de la suficiencia y pertinencia de la evidencia de auditoria obtenida"),
      bullet("Validacion de los hallazgos con la administracion del CPPP antes del informe final"),
      bullet("Revision externa del borrador del informe por un auditor independiente senior"),
      bullet("Evaluacion post-auditoria del desempeno del equipo y calidad del proceso"),

      h2("11.2 Confidencialidad y Etica"),
      body("Todos los miembros del equipo auditor firmaran un acuerdo de confidencialidad y declaracion de independencia antes del inicio de los trabajos. La informacion obtenida durante la auditoria sera utilizada exclusivamente para los fines del presente encargo y no podra ser divulgada a terceros sin autorizacion expresa de las autoridades universitarias competentes."),
      ...spacer(1),
      body("El equipo auditor actuara en todo momento con objetividad, independencia y apego a las normas eticas del Instituto de Auditores Internos (IIA) y del Colegio de Contadores Publicos del Peru."),

      pageBreak(),

      // =========================================================
      // 12. SEGUIMIENTO A RECOMENDACIONES
      // =========================================================
      h1("12. PLAN DE SEGUIMIENTO A RECOMENDACIONES"),

      body("Una vez emitido el Informe Final de Auditoria, la Jefatura de Auditoria Interna realizara el seguimiento a la implementacion de las recomendaciones formuladas, conforme al siguiente esquema:"),

      h2("12.1 Proceso de Seguimiento"),
      numbered("Primera evaluacion de avance: 90 dias despues de la emision del informe final"),
      numbered("Segunda evaluacion de avance: 180 dias, con verificacion de implementacion de recomendaciones criticas"),
      numbered("Evaluacion final: 360 dias, con cierre de recomendaciones implementadas y reprogramacion de pendientes"),
      numbered("Informe de seguimiento: emitido al Consejo Universitario con el nivel de cumplimiento"),

      h2("12.2 Clasificacion del Estado de Implementacion"),
      headerTable(
        ["Estado", "Descripcion", "Accion"],
        [
          ["Implementada", "La recomendacion fue atendida en su totalidad", "Cierre del hallazgo"],
          ["En proceso", "Acciones iniciadas pero no concluidas aun", "Monitoreo continuo"],
          ["Pendiente", "Sin acciones de implementacion iniciadas", "Escalamiento a alta direccion"],
          ["No aplicable", "Condicion cambio, recomendacion ya no aplica", "Documentacion y cierre"],
          ["Rechazada", "Administracion no acepta la recomendacion", "Informe especial al Rector"],
        ]
      ),

      pageBreak(),

      // =========================================================
      // 13. CONCLUSIONES Y APROBACION
      // =========================================================
      h1("13. CONCLUSIONES PRELIMINARES Y APROBACION"),

      h2("13.1 Consideraciones Finales"),
      body("El presente Plan de Auditoria Integral ha sido elaborado considerando el analisis previo del entorno, la evaluacion de riesgos institucionales, la normativa vigente aplicable y los recursos disponibles. Su implementacion rigurosa permitira a la Universidad Peruana Union contar con una evaluacion objetiva, completa y oportuna del Centro de Practicas Pre Profesionales."),
      ...spacer(1),
      body("Se espera que los resultados de esta auditoria contribuyan significativamente al fortalecimiento del control interno, la mejora de la eficiencia operativa y el alineamiento del CPPP con los objetivos estrategicos de la UPeU. Asimismo, el proceso auditora promovera una cultura de transparencia y mejora continua en toda la organizacion."),
      ...spacer(1),
      body("La ejecucion exitosa de este plan requerira la colaboracion activa de todas las areas involucradas, el acceso oportuno a la informacion solicitada y el compromiso de la alta direccion con la implementacion de las mejoras recomendadas."),

      h2("13.2 Aprobacion del Plan"),
      ...spacer(1),
      headerTable(
        ["Rol", "Nombre", "Firma", "Fecha"],
        [
          ["Elaborado por", "Equipo de Auditoria Interna", "_________________", "____/____/2025"],
          ["Revisado por", "Auditor Senior Responsable", "_________________", "____/____/2025"],
          ["Aprobado por", "Jefe de Auditoria Interna", "_________________", "____/____/2025"],
          ["Conocimiento", "Rector - UPeU", "_________________", "____/____/2025"],
        ]
      ),
      ...spacer(2),
      body("Lima, Peru - 2025", { italics: true }),
      ...spacer(1),
      body("Este documento es de caracter confidencial y de uso exclusivo de la Universidad Peruana Union. Cualquier reproduccion o difusion no autorizada esta prohibida.", { italics: true, color: GRAY }),
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync('../Plan_Auditoria_Integral_UPeU.docx', buffer);
  console.log('Word document created successfully');
}).catch(err => console.error(err));
