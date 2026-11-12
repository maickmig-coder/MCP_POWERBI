# V10.1 — Fuentes desde el diccionario de datos (sustituye el catálogo de V10)

Fecha: 2026-11-09
Base: V10.

## Decisión del usuario

Creación no toma las conexiones de un censo en particular (antes: censo de GC - Flotillas sembrado en un catálogo),
sino de un **diccionario de datos** que consolida todos los censos, generado por un DLC aparte:
`MCP_POWERBI\00_dlc\01b_ai-dlc-diccionario-datos` → `MCP_POWERBI\03_diccionario_datos`.

## Cambios

| Archivo | Clasificación | Cambio |
|---|---|---|
| `16_catalogo_fuentes_desde_censos.md` | ELIMINADA | Sustituida por la regla 16 nueva. |
| `02_Plantillas/02_catalogo_fuentes.md` | ELIMINADA | El catálogo sembrado con Flotillas deja de existir; lo reemplaza el diccionario. |
| `16_diccionario_datos_y_simulacion.md` | NUEVA | Validar vigencia del diccionario; ubicar la fuente; decidir columnas, filtros y puntos abiertos; construir en modo simulación (`ModoSimulacion`, `Sim_` / `Real_` / `Src_`); cambiar a conexión real y verificar antes de liberar; fuentes nuevas fuera del diccionario. |
| `03_creacion.md` | MODIFICADA | Sección 6.1 apunta al diccionario y al modo simulación. |
| `01_rutas_y_censo.md` | MODIFICADA | Rutas del DLC y de `03_diccionario_datos`; Creación no lee censos individuales para conexiones. |
| `01_levantamiento_creacion.md` | MODIFICADA | `diccionario_id` usado; origen `Diccionario (objeto_id)` o fuente nueva; decisiones sobre filtros y puntos abiertos. |
| `flujo_operativo.md` | MODIFICADA | Pasos de vigencia del diccionario, simulación y cambio a conexión real. |
| `checklist_general.md` / `14_checklist_integral.md` | MODIFICADAS (sincronizadas) | Controles del diccionario y de la simulación. |
| `02_diseno_corporativo.md` | MODIFICADA | Referencias al catálogo cambiadas por diccionario / censos. |
| `README.md` | MODIFICADA | Orden de lectura, inicio y reglas de bloqueo. |

## Validaciones

- Búsqueda de referencias al catálogo, `CATALOGO_FUENTES`, `F-ATH`, `C-ATH`: ninguna fuera del control de versiones.
- Checklists sincronizados.
- El DLC del diccionario se probó con censos de prueba (no incluidos en el paquete final); Creación no se probó contra un PBIP.

## Ajuste posterior (2026-11-09) — disparadores

- `16_diccionario_datos_y_simulacion.md`, paso 1: la vigencia se comprueba con el disparador DD-02 «consulta diccionario»
  (`diccionario.py estado`); si hay censos nuevos, modificados o eliminados se ejecuta DD-01 (`actualizar`) antes de seguir.
  La ubicación de la fuente usa DD-04 (`buscar`) y las consultas de simulación DD-06 (`simulacion`).

## Ajuste posterior (2026-11-09) — ubicación del diccionario

- La salida del diccionario de datos se aloja en `C:\dev\MCP_POWERBI\00_dlc\00_diccionario_datos`
  (antes `MCP_POWERBI\03_diccionario_datos`). Actualizadas las rutas en `01_rutas_y_censo.md`, `03_creacion.md`,
  `16_diccionario_datos_y_simulacion.md` y `README.md`. El repositorio del DLC sigue en `00_dlc\01b_ai-dlc-diccionario-datos`.

## Ajuste posterior (2026-11-10) — ubicaciones reales en el equipo

- DLC del diccionario y diccionario generado: `C:\dev\MCP_POWERBI\00_dlc\00_diccionario_datos` (antes `00_dlc\01b_ai-dlc-diccionario-datos`).
- Creación: `C:\dev\MCP_POWERBI\00_dlc\02_ai_dlc_bi\01_Creacion` (antes `00_dlc\02_ai_dlc_creacion_modificacion`).
- Logo oficial: `MCP_POWERBI\00_dlc\02_ai_dlc_bi\00_fuentes\Logo_Nebula.png`.
