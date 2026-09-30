# GC - Leads MG v2

Tablero Power BI en formato **PBIP** creado a partir de la plantilla `GC - Leads MG` (Opción C: mismo modelo semántico, reporte nuevo).

## Estructura

```
00_desarrollos_bi/
├─ GC - Leads MG v2.pbip                 # Archivo de proyecto (abrir este en Power BI Desktop)
├─ GC - Leads MG v2.Report/              # Reporte nuevo (PBIR)
│  ├─ definition.pbir                    # datasetReference.byPath → ../GC - Leads MG v2.SemanticModel
│  ├─ definition/report.json             # Tema Fluent2 + tema corporativo
│  ├─ definition/pages/                  # 2 páginas: Resumen, Análisis
│  └─ StaticResources/                   # Tema base, tema custom y logo
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

## Reporte (páginas y visuales)

**Página 1 — Resumen**
- 3 tarjetas KPI: Total Leads, Leads Gestionados, % Gestionados
- Leads por Centro (barras) · Leads por Medio (circular) · Leads por Mes (líneas)
- Segmentaciones: Año, Mes, Fuente

**Página 2 — Análisis**
- 3 tarjetas KPI
- Total leads por días del mes (líneas) · Estado Actual por Campaña (matriz)
- Segmentaciones: Centro, Categoría, Fuente

> Nota: A diferencia de la plantilla, este reporte no arrastra las reglas de color huérfanas
> (que apuntaban a tablas inexistentes `VehiculosEntregados` / `Funnel Digital`) ni los títulos
> de segmentación mal etiquetados como "Año". Cada segmentación muestra su campo real.

## Cómo abrir y refrescar

1. Abre `GC - Leads MG v2.pbip` en **Power BI Desktop** (versión con soporte PBIP/TMDL).
2. El reporte carga el modelo por ruta relativa (`byPath`), no requiere reconexión de dataset.
3. Para refrescar datos necesitas el **DSN ODBC `Athena_ODBC2`** configurado en tu equipo con credenciales válidas de Amazon Athena. El refresh se ejecuta desde Power BI Desktop; no está automatizado en el proyecto versionado.

## Pendientes sugeridos (del censo)

- Validar con negocio la definición de "gestionado" (difiere por fuente).
- Revisar el umbral de 120 min de la clasificación de gestión Orbi.
- Evaluar desactivar la fecha/hora automática (20 tablas `LocalDateTable` heredadas del modelo).
