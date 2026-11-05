# Catálogos de vocabulario del CENSO (v2.3)

Este archivo es la **única fuente de valores permitidos**. El ritual, las reglas, el checklist y `scripts/censo.py` usan exactamente estos valores, escritos igual (mayúsculas y tildes incluidas). Si se necesita un valor nuevo, se agrega aquí primero y se registra en `CHANGELOG.md`.

---

## CAT-01 — Certeza de una afirmación

| Valor | Significado |
|---|---|
| `Encontrado` | Existe evidencia directa en un archivo del PBIP. |
| `Inferido` | Inferencia razonable sin evidencia directa. Se debe explicar en qué se basa. |
| `Desconocido` | No hay información suficiente. |

## CAT-02 — Estado de uso de un objeto (columna, medida, tabla, consulta, visual, bookmark, recurso)

| Valor | Cuándo usarlo |
|---|---|
| `En uso` | Se encontró al menos una dependencia funcional: visual, slicer, filtro de página/informe/visual, medida o columna calculada consumida, bookmark válido. |
| `Uso técnico` | Solo sostiene funciones técnicas: relación, paso M posterior, filtro de carga, ordenamiento (`sortByColumn`), seguridad, tabla de fecha automática. |
| `Sin uso interno identificado` | Se revisaron **todas** las clases obligatorias de CAT-03 (V, F, D, M, PQ, BK; SQL y SEC cuando apliquen) con resultado `No encontrada en el alcance revisado` o `No aplica`. |
| `Uso desconocido` | Alguna clase obligatoria quedó `No verificable` o `Pendiente`, o la evidencia es ambigua. |
| `Referencia rota` | El objeto referencia una entidad, página, visual o bookmark que no existe en el PBIP analizado. |

Reglas de uso:
- `Candidata a depuración` **no es un estado de uso**: un objeto es candidato cuando su estado es `Sin uso interno identificado` o `Referencia rota`, y figura en la sección 17.2.
- `No eliminar` **no es un estado de uso**: los objetos `En uso` y `Uso técnico` se consideran protegidos.
- Un objeto oculto no es, por estar oculto, `Sin uso interno identificado`.

## CAT-03 — Clases de dependencia (códigos)

| Código | Clase | Obligatoria para clasificar columnas |
|---|---|---|
| `V` | Visuales (bindings en `visual.json`) | Sí |
| `F` | Filtros de informe, página y visual; slicers | Sí |
| `D` | DAX: medidas, columnas calculadas, tablas calculadas | Sí |
| `M` | Modelo: relaciones, jerarquías, `sortByColumn`, variaciones, propiedades | Sí |
| `PQ` | Power Query/M: pasos de la consulta | Sí |
| `BK` | Bookmarks, botones, navegación, tooltips, drillthrough | Sí |
| `SQL` | SQL/origen visible dentro del PBIP (consulta nativa, vista) | Solo si existe en el PBIP |
| `SEC` | Seguridad RLS/OLS, roles | Solo si existen roles |

## CAT-04 — Resultado de revisión por clase de dependencia

| Valor | Significado |
|---|---|
| `Encontrada` | Hay al menos una referencia concreta con evidencia. |
| `No encontrada en el alcance revisado` | Se revisó la clase completa y no hay referencias. No prueba ausencia de uso externo. |
| `No aplica` | La clase no existe en este PBIP (ej.: no hay roles → `SEC`). |
| `No verificable` | La clase existe pero no se pudo inspeccionar (archivo inaccesible, formato opaco, origen externo). |
| `Pendiente` | La clase no se revisó todavía en esta ejecución. |

**Forma abreviada en la Matriz A (sección 6):** número = `Encontrada` (cantidad de referencias) · `0` = `No encontrada en el alcance revisado` · `NA` = `No aplica` · `NV` = `No verificable` · `P` = `Pendiente`. El validador acepta solo estos valores en esas celdas.

## CAT-05 — Estado de referencia de un binding, navegación o target

| Valor | Significado |
|---|---|
| `Válida` | La entidad/objeto referenciado existe en el PBIP. |
| `Rota` | La entidad/objeto referenciado no existe en el PBIP analizado. |
| `No determinada` | Coincidencia textual o contexto ambiguo; requiere verificación. |
| `Formato huérfano` | Una regla de formato (no un campo de datos) apunta a una entidad inexistente. El visual funciona. |
| `No aplica` | El objeto no tiene referencias (imagen, forma, cuadro de texto). |

## CAT-06 — Tipo de referencia

`Directa` · `Secundaria` · `No determinada`

## CAT-07 — Estado de la ejecución del CENSO

| Valor | Cuándo |
|---|---|
| `Completado y validado` | Cobertura total conciliada contra el PBIP, validador sin errores, sin pendientes. Las capas externas siguen declaradas como limitación. |
| `Completado pendiente de validación` | Documento completo pero con capas `No verificable`/`Pendiente`, o hallazgos que requieren confirmación del dueño. |
| `Revisión incompleta` | Faltan inventarios individuales o hay conteos sin conciliar. |
| `Interrumpido` | La ejecución se detuvo antes de terminar. |
| `Fallido` | La ejecución no produjo un resultado utilizable. |

El estado del encabezado del Markdown es el que `censo.py registrar` copia a `historial-censos.md`.

## CAT-08 — Tipo de CENSO

| Valor | Cuándo |
|---|---|
| `Inicial` | No existe censo previo del tablero. |
| `Actualización` | Hay una **versión nueva** del PBIP guardada en `01_versiones/<versión>/<BI>` (por ejemplo, después de un DLC de modificación o depuración). Se censa completa desde cero (R52, R54). |
| `Validación` | El PBIP no cambió (misma huella) y se registran respuestas del dueño a puntos pendientes. Se prepara con `censo.py iniciar-validacion` (R55). |

## CAT-09 — Tipo de registro en la tabla maestra de hallazgos

| Valor | Significado |
|---|---|
| `Hallazgo` | Condición encontrada con evidencia (ej.: métrica con binding incorrecto). |
| `Riesgo` | Condición que puede afectar la operación o un cambio futuro. |
| `Vacío` | Información necesaria que no pudo determinarse. |
| `Observación` | Dato informativo relevante para el DLC de modificación, sin problema identificado. |

Hallazgos y vacíos comparten la tabla de la sección 16; un `Vacío` no tiene sección propia. `Mejora propuesta` **ya no es un tipo válido**: el CENSO no prescribe cambios (ver `criterios-puntos-revision.md`).

## CAT-10 — Prioridad

`Alta` · `Media` · `Baja` (criterios en `criterios-puntos-revision.md`).

## CAT-11 — Estado de un punto de revisión

`Pendiente de validación` · `Confirmado por el dueño` · `Descartado por el dueño`

Se usan en la columna «Estado» de la sección 16 y en «Validación del dueño» de la sección 14. `Confirmado por el dueño` y `Descartado por el dueño` exigen la columna «Respuesta del dueño» con fecha y respuesta (R55). Si quien realiza el censo es el dueño, se registran en la misma ejecución; si no, en una de tipo `Validación`.

En la sección 14 se agrega el valor `No requerida`, solo para reglas con certeza `Encontrado` (se leen tal cual del PBIP). Una regla `Inferido` queda `Pendiente de validación` hasta que el dueño responda.

## CAT-12 — Visibilidad de un visual por estado

`Visible` · `Oculto físicamente` (`isHidden: true`) · `Oculto por bookmark` · `Visible en algún bookmark` · `Sin estado explícito` · `No verificable`

## CAT-12b — Efecto de un bookmark (sección 12.2)

| Valor | Significado |
|---|---|
| `Se aplica: muestra` / `Se aplica: oculta` | Target que existe; al activar el bookmark se muestra u oculta. |
| `Se aplica: sin estado guardado` | Target que existe pero sin estado guardado en el bookmark. |
| `Se aplica (toda la página): …` | Bookmark sin targets: el estado se aplica a todos los visuales guardados. |
| `Target inexistente` | El target no existe en el PBIP. |
| `Guardado sin efecto` | Estados guardados de visuales que no son targets; no se aplican por `applyOnlyToTargetVisuals`. En la 12.2 solo va la cantidad; el detalle visual por visual está en la matriz 12.3 (`O` oculto, `V` visible, `·` sin estado). |

## CAT-13 — Ámbito de filtro o interacción

`Informe` · `Página` · `Visual` · `Slicer` · `Interacción`

## CAT-14 — Valores para campos no completables

| Valor | Cuándo |
|---|---|
| `No aplica` | El atributo no existe para ese objeto. |
| `No disponible` | El formato fuente no expone el dato. |
| `No verificable` | El dato existe pero no se pudo comprobar. |

En las tablas del censo, `—` equivale a `No aplica` o `No disponible`. No se deja ningún campo vacío si el vacío puede leerse como “revisado sin hallazgos”.

## CAT-15 — Identificadores nativos por tipo de objeto (PBIP: PBIR + TMDL)

| Objeto | ID nativo | Dónde está |
|---|---|---|
| Tabla | `lineageTag` | `definition/tables/<tabla>.tmdl` |
| Columna | `lineageTag` | Bajo `column` en el `.tmdl` de la tabla |
| Medida | `lineageTag` | Bajo `measure` en el `.tmdl` de la tabla |
| Jerarquía | `lineageTag` | Bajo `hierarchy` |
| Relación | nombre de la relación (GUID completo) | `definition/relationships.tmdl` |
| Rol | nombre del rol | `definition/roles/<rol>.tmdl` |
| Consulta / partición | nombre de la partición + tabla | Bajo `partition` |
| Página | `name` (= nombre de la carpeta) | `definition/pages/<id>/page.json` |
| Visual | `name` (= nombre de la carpeta) | `definition/pages/<id>/visuals/<id>/visual.json` |
| Bookmark | `name` | `definition/bookmarks/<id>.bookmark.json` |
| Filtro | `name` del filtro | `filterConfig.filters[]` de `report.json`, `page.json` o `visual.json` |
| Recurso (imagen/tema) | nombre registrado en `resourcePackages` | `report.json` + `StaticResources/` |

Reglas:
- Los IDs se registran **completos**. Está prohibido truncarlos con `…`, `...` o recortes de 8 caracteres.
- Las claves compuestas (`compound_key`) se marcan siempre como **no nativas**.
