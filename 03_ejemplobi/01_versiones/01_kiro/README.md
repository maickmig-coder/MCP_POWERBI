# GC - Leads MG v2

Tablero Power BI en formato **PBIP**. El diseño visual sigue el estándar **AI-DLC — Creación, Modificación y Estandarización de BI** (`00_dlc/02_ai_dlc_creacion_modificacion/AI-DLC-Creacion-Modificacion-Estandarizacion-BI.md`).

Ubicación: `C:\dev\NIGGA\03_ejemplobi\01_versiones\01_kiro`

## Estructura

```
01_kiro/
├─ GC - Leads MG v2.pbip                 # Archivo de proyecto (abrir este en Power BI Desktop)
├─ GC - Leads MG v2.Report/              # Reporte (PBIR)
│  ├─ definition.pbir                    # datasetReference.byPath → ../GC - Leads MG v2.SemanticModel
│  ├─ definition/report.json             # Tema Fluent2 + tema corporativo + logo estándar
│  ├─ definition/pages/                  # 2 páginas: Resumen, Análisis
│  └─ StaticResources/                   # Tema base, tema custom y logos
├─ GC - Leads MG v2.SemanticModel/       # Modelo clonado de la plantilla (TMDL)
└─ .gitignore
```

## Modelo semántico

Clon exacto del modelo de la plantilla. Reutiliza las mismas fuentes:

- **Orbi Leads** — Amazon Athena (DSN ODBC `Athena_ODBC2`), esquema `tatooine_prod_core`, tabla `materialized_leads_tracking`.
- **Atom** — Amazon Athena, esquema `atom_leads`, tablas `leads` + `nebula_tiempos_de_agentes`.
- Tabla central `General` (UNION Orbi + Atom deduplicado), dimensión `Calendario`, `Parametros` y `Medidas`.

### Medidas (KPIs base)

| Medida | Definición |
|---|---|
| `Leads` | `DISTINCTCOUNT(General[lead_id])` |
| `Total Leads sin nuevos` | Leads gestionados (Orbi ≠ "Nuevo" + Atom = "Atendido") |
| `%Gestionados` | `DIVIDE([Total Leads sin nuevos],[Leads])` |

## Estándar visual aplicado (AI-DLC)

**Header** (idéntico en ambas páginas, §5):
- Rectángulo `#323131`, alto 155, ancho 1279.
- Título "Leads" — Segoe UI, blanco `#FFFFFF`, tamaño 24, negrilla.
- Separador de línea con remate plano, borde blanco.
- Tarjeta "Última Actualización" — blanco, tamaño 12, negrilla (usa `Min(Parametros[Parametro])`).
- Logo **Nebula** en la esquina superior derecha (`Logo_Nebula.png`).

**Segmentaciones** (§6–§8): tipo desplegable, alto 69, ancho 135, fondo `#474747`, borde `#323131`, esquinas redondeadas, fuente blanca. Jerarquía estándar respetada, con el título = campo real:

1. Año · 2. Mes · 3. Campaña · 4. Categoría · 5. Centro · 6. Tipificación · 7. Fuente · 8. Gestión Leads

**Colores** (§11): fondo general `#F6F6F5`, tarjetas blancas, encabezados de matriz `#B8D4F8`. Colores de medida consistentes: **Leads → azul `#1A73E8`**, **Leads Gestionados → morado `#8943A7`**.

## Reporte (páginas y visuales)

**Página 1 — Resumen**
- 3 tarjetas KPI: Total Leads, Leads Gestionados, % Gestionados
- Leads por Centro (barras) · Leads por Medio (circular) · Leads por Mes (líneas)

**Página 2 — Análisis**
- 3 tarjetas KPI
- Total leads por días del mes (líneas) · Estado Actual por Campaña (matriz)

> Ambas páginas comparten el mismo header y la misma fila de 8 segmentaciones (regla de consistencia §17).
> No se arrastran reglas de color huérfanas (`VehiculosEntregados` / `Funnel Digital`) ni títulos de slicer incorrectos.

## Cómo abrir y refrescar

1. Abre `GC - Leads MG v2.pbip` en **Power BI Desktop** (versión con soporte PBIP/TMDL).
2. El reporte carga el modelo por ruta relativa (`byPath`), no requiere reconexión de dataset.
3. Para refrescar datos necesitas el **DSN ODBC `Athena_ODBC2`** configurado en tu equipo con credenciales válidas de Amazon Athena. El refresh se ejecuta desde Power BI Desktop; no está automatizado en el proyecto versionado.

## Pendientes sugeridos (del censo)

- Validar con negocio la definición de "gestionado" (difiere por fuente).
- Revisar el umbral de 120 min de la clasificación de gestión Orbi.
- Evaluar desactivar la fecha/hora automática (20 tablas `LocalDateTable` heredadas del modelo).
