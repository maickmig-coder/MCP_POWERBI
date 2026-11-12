# V10 — Estándar de diseño y catálogo de fuentes desde censos

Fecha: 2026-11-09
Base: V9.3 (auditoría profunda de Creación).
Insumos: mockups corporativos de diseño (header, segmentaciones, botones, gráficos, cards, datos relevantes,
mesa de trabajo, paletas, feedback, secundarios, tipografía), guía de color de Microsoft entregada por la compañía,
tablero de referencia "Cotizaciones" y censo `GC - Flotillas` (census_id 20261105T124212-gc-flotillas).

## Decisiones del usuario

| # | Tema | Decisión |
|---:|---|---|
| D1 | Segmentaciones | Estilo oscuro: fondo `#474747`, borde `#323131`, texto `#FFFFFF`, valores sobre `#474747`, 69 × 135 |
| D2 | Radio de botones | 6 px (se descarta 4 px) |
| D3 | Logo | Solo logo Nebula, como en el mockup |
| D4 | Fuentes | Si el usuario nombra una fuente ya censada (ej.: Athena Entregas Totales), la conexión se toma del censo |

## Cambios

| Archivo | Clasificación | Cambio |
|---|---|---|
| `02_diseno_corporativo.md` | REESCRITA | Aplica D1–D3. Corrige el botón menú (era texto azul sobre blanco; es fondo `#1A73E8` y texto blanco). Agrega variante botón texto, etiqueta de 10 px de "Última actualización", espacio de 10 px y fondo `#F5F5FA` en etiquetas de gráficos, lienzo y mesa de trabajo, orden de dataColors igual a `Tema_1_BI_Nebula`, escalas 50–900, colores de feedback, neutrales con niveles del tema, principios de color, tabla de contraste, valores mínimos del Theme JSON, equivalencia px/pt y tabla de decisiones pendientes. Renombra familias duplicadas (`teal`, `red-feedback`). |
| `16_catalogo_fuentes_desde_censos.md` | NUEVA | Regla obligatoria: consultar los censos como catálogo de fuentes; procedimiento encontrada / ambigua / no encontrada; verificación en conexión real; prohibido crear objetos en la base; no heredar filtros de carga sin aprobación. |
| `02_Plantillas/02_catalogo_fuentes.md` | NUEVA | Estructura del catálogo y primera entrada F-ATH-001 (`bi_materialized_data.entregas_totales`) tomada del censo de GC - Flotillas. |
| `03_creacion.md` | MODIFICADA | Sección 6.1 de catálogo; reutilización desde censos en 7; decisiones D1–D3 en 8; aclaración CENSO vs catálogo en 10. |
| `01_rutas_y_censo.md` | MODIFICADA | Separa "CENSO del BI nuevo = No aplica" de "consulta de censos como catálogo = obligatoria"; agrega rutas del catálogo. |
| `01_levantamiento_creacion.md` | MODIFICADA | Campo de catálogo consultado; tabla de fuentes con origen del dato y verificación; decisiones pendientes del estándar. |
| `flujo_operativo.md` | MODIFICADA | Paso de búsqueda en catálogo con tres salidas y paso de verificación. |
| `checklist_general.md` / `14_checklist_integral.md` | MODIFICADAS (sincronizadas) | Controles de catálogo, verificación, datos personales y nuevos controles de diseño. |
| `README.md` | MODIFICADA | Orden de lectura, inicio obligatorio y reglas de bloqueo actualizados. |

## Decisiones pendientes (no resueltas por la IA)

Ver `02_diseno_corporativo.md` sección 4.17: unidades px/pt, dataColors 6–8 repetidos, color de advertencia,
tono de KPI de feedback (contraste), jerarquía de filtros fuera de Leads, radio de segmentaciones, tamaño de ícono.

## Validaciones ejecutadas

- Revisión cruzada de valores contra los mockups (hex de escalas transcritos y contrastados contra las imágenes).
- Colores secundarios muestreados del mockup: `#323131`, `#898C93`, `#CDCDD1`, `#474747`, `#F6F6F5`, `#FFFFFF`.
- Búsqueda de reglas contradictorias (radio 4, selector blanco, logos de marca, botón menú): solo quedan como referencia a lo descartado.
- Checklists sincronizados.
- Revisión documental; no se probó contra un PBIP ni contra la conexión Athena.
