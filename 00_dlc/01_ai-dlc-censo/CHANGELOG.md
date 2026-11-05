# CHANGELOG — AI-DLC-CENSO

## v2.3 — 2026-11-05

Versiones del tablero y validación con el dueño, acordados tras la revisión del censo de GC - Flotillas.

### Decisiones

| # | Decisión | Resultado |
|---|---|---|
| 1 | Cada versión del PBIP se censa completa; el censo muestra el estado actual | `[BI] - censo.md` siempre describe la última versión censada; los anteriores se archivan en `versiones/` (R35). |
| 2 | Los cambios entre versiones van en un archivo propio | Nuevo `[BI] - cambios.md`, append-only, con objetos agregados, eliminados y modificados, origen del cambio y cambios de validación (R52). Lo genera `censo.py comparar`. |
| 3 | Saber si un censo es el del tablero final | Huella del PBIP (SHA-256) en el encabezado; `validar --pbip` la comprueba y el nuevo comando `vigencia` responde VIGENTE o DESACTUALIZADO (R53). |
| 4 | Confirmar que la versión nueva se guardó en la ruta | `borrador --tipo Actualización` exige `--pbip-guardado-confirmado` y bloquea si no hay `.pbip`, si la carpeta no coincide con la versión, si la versión ya está censada o si la huella es igual a la del censo vigente (R54). |
| 5 | Validación con el dueño | Columnas «Validación del dueño» (14) y «Respuesta del dueño» (14 y 16). Si el ejecutor es el dueño, se le pregunta en la misma ejecución; si no, `iniciar-validacion` prepara una ejecución de tipo Validación (R55). En la 14 solo se validan las reglas Inferidas. |
| 6 | Bloqueo del DLC | El DLC de modificación o depuración solo parte de un censo APTO según `vigencia`: vigente, `Completado y validado` y sin pendientes; un punto que el dueño no sabe mantiene el bloqueo (R56). |

### Otros cambios

- `comparar` traslada al borrador las interpretaciones y validaciones de 14 y 16 que siguen aplicando, reabre las que citan objetos eliminados e indica a la IA qué texto del censo vigente puede reutilizar (menos tokens).
- `registrar` cierra la ejecución: archiva, reemplaza, agrega el bloque de cambios y la fila del historial (con huella y pendientes). Conserva las columnas de un historial existente.
- Limitación estándar 5: los cambios entre versiones están en `[BI] - cambios.md`.
- CAT-08 y CAT-11 precisados; R35, R39 y R41 actualizadas; ritual con fases 0–5 y Fase 2b; checklist, criterios, guía de Kiro y README al día.
- `examples/GC - Flotillas - censo.md` migrado al formato v2.3 (columnas de validación; sin huella hasta la próxima ejecución con el PBIP).

## v2.2.4 — 2026-11-05

Ajuste tras revisar la corrida limpia de Kiro con v2.2.3 (325 IDs, sin errores): la sección 14 interpretaba columnas calculadas por su nombre.

- **R51 (nueva):** una columna calculada se interpreta desde su expresión en 6.1 y su «Estado de uso»; su significado de negocio es «Inferido».
- **Validador:** advertencia si una regla de la sección 14 sobre una columna «Sin uso interno identificado» no lo dice, o si su certeza es «Encontrado».
- **Marcador de la 14, ritual, checklist y guía de Kiro:** instrucción y ejemplo (DIVISION S = semestre; RENTING sin uso).
- **README:** reglas R01–R51, lista de errores y advertencias del validador al día.
- **examples/:** incluye el censo de GC - Flotillas como referencia (325 IDs, validación sin errores); la guía de Kiro indica que no lo lea durante un censo.

## v2.2.3 — 2026-11-05

- **Sección 1:** se eliminan las filas «Responsable funcional» y «Responsable técnico»; el dueño/responsable del tablero (cabecera, R02) responde por ambos papeles. Se retiran los parámetros `--responsable-funcional` y `--responsable-tecnico`.
- **Sección 16:** desaparece el vacío «No se conoce: Responsables funcional y técnico»; los vacíos de gobierno del script quedan en V-A01 a V-A03 (actualización, ambiente y propietario de las fuentes).
- **Historial:** la fila nueva no lleva columnas de responsables; si `historial-censos.md` ya existía con esas columnas, se rellenan con `—` para no reescribir el encabezado (R38).
- R03 retirada (se conserva el número); R39, catálogo, criterios, checklist y ritual actualizados.

## v2.2.2 — 2026-11-05

Ajustes tras revisar el censo de GC - Flotillas generado con v2.2.1 (325 IDs, validación sin errores, parte mecánica idéntica a la versión depurada).

- **Validador:** advertencia cuando una limitación agregada por la IA se parece a una de las 5 estándar (comparten al menos la mitad de sus palabras significativas). En GC - Flotillas detecta la limitación 6, que repetía la 3 en un 78 %.
- **Validador:** la comprobación de limitaciones de la IA empieza después de las 5 estándar (antes empezaba en la 5).
- **Marcador de 2.1 y guía de Kiro:** ejemplo explícito; citar el vacío no basta si el texto sigue afirmando. No «valor facturado (ver V01)», sino «valor (`Entregas Totales[Valor]`, definición pendiente: V01)».
- R49 y R50 precisadas; checklist actualizado.

## v2.2.1 — 2026-11-04

Depuración tras revisar el censo v2.2 de GC - Flotillas, sin perder mapeo (los 325 IDs del censo se conservan).

- **12.2 / 12.3:** la 12.2 deja solo la cantidad de estados guardados sin efecto; el detalle pasa a una matriz por página (12.3) con una fila por visual y una columna por bookmark (`O`/`V`/`·`). Botones pasan a 12.4 y tooltips a 12.5.
- **H-A04:** solo lista los visuales con formato huérfano que funcionan; indica cuántos otros ya están rotos por sus datos (todos siguen marcados en la sección 9).
- **Limitaciones:** la 4 incluye que del contenido de tablas embebidas solo se documenta su efecto; nueva limitación estándar «se analiza una sola versión del PBIP». La IA solo agrega limitaciones del proceso (R49).
- **Validador:** error si una fila de la IA en la sección 16 cita filas H-A/V-A (R50) o si una limitación agregada por la IA cita un hallazgo o vacío (R49).
- **Guía de Kiro y ritual:** prefijos `H01`/`V01` para filas de la IA, sin filas agrupadoras, sin afirmar lo que un vacío declara desconocido.

## v2.2 — 2026-11-03

Ajustes acordados con el responsable tras revisar el primer censo v2.1 de GC - Flotillas.

### Decisiones

| # | Decisión | Resultado |
|---|---|---|
| 1 | Unir vacíos y hallazgos | La sección 16 es «Hallazgos, vacíos y puntos de revisión» (filas H-A*/V-A* del script y H/V de la IA). El documento queda con las secciones 0–18. Un asunto no se repite en otra fila ni en otra sección. |
| 2 | Limitaciones | Sin cambios. |
| 3 | Bookmarks | La 12.1 da la ficha (targets: total / existen / funcionan, invocado por, estado y motivo). La 12.2 detalla el efecto real: qué muestra u oculta al activarse, targets inexistentes y estados guardados sin efecto, con cada visual como `ID · nombre · funciona/roto`. Un bookmark cuyos targets están todos rotos o no existen pasa a «Referencia rota». |
| 4 | Visuales en dos tablas | Sin cambios (inventario y bindings). Se explica en la sección qué contiene cada una. |
| 5 | Estética | La sección 13 incluye la ubicación de cada elemento de diseño por página, agrupada en banners (forma de al menos 80 % del ancho y todo lo que cae en su franja) y cuerpo de página, con la escala de cada imagen (original → colocado) y la ruta del archivo. |
| 6 | Filtro de carga | Sin cambios. |
| 7 | Correcciones del script | Ver «Correcciones». |
| — | Nombres junto a los IDs | Nueva regla R48: todo ID que relaciona objetos va con su nombre. |

### Correcciones

- **Formato huérfano frente a fuente ausente:** una regla de formato (colores por categoría, formato condicional) que apunta a una entidad inexistente ya no marca el visual como «Referencia rota». El visual se clasifica por sus datos, la fila del binding dice «Formato huérfano» y se registra un hallazgo de tipo «Observación» aparte. En GC - Flotillas, «Participación por convenio (unidades año)» vuelve a ser válido; los visuales rotos pasan de 37 a 36.
- Posiciones y tamaños en píxeles enteros.
- Los filtros sin condición guardada siguen en 11.1, pero ya no se registran como reglas de negocio.
- La sección 3 muestra el conector y su DSN en vez de copiar la primera línea del código M.
- La 13.4 muestra solo el modelo referenciado y la versión PBIR, en lugar del JSON completo de `definition.pbir`.
- Las propiedades anidadas del modelo se leen con su ruta (`dataAccessOptions.legacyRedirects`).
- Las segmentaciones toman el nombre visible del campo (por ejemplo, «Tecnología» para `combustible`).

## v2.1 — 2026-11-03

Ajuste tras la primera ejecución de v2.0 con Kiro sobre GC - Flotillas: 66 créditos (el doble que v1), unos 90 mil caracteres de scripts generadores escritos por la IA, un Markdown de 330 KB y un validador que se colgó más de 10 minutos.

### Causas encontradas

| Problema | Causa |
|---|---|
| Validador colgado | Leía `matrices-censo.xlsx` celda por celda en modo de solo lectura de openpyxl, lo que crece de forma cuadrática con las filas. |
| Costo de tokens | La IA reconstruía en cada censo el cruce de bindings, filtros, DAX y relaciones, y lo escribía tres veces (JSON, Excel y Markdown). |
| Markdown de 330 KB | Matriz B (114 KB) repetía lo que ya estaba en bindings, filtros, medidas y relaciones; 313 de sus 372 filas eran referencias internas de tablas de fecha automáticas. La ruta de evidencia se repetía 731 veces; «No encontrada en el alcance revisado», 422 veces. Las matrices C y D repetían la A, y la matriz bookmark × visual tenía 80 filas de visuales inexistentes. |
| Datos erróneos | El extractor v2.0 perdía expresiones DAX multilínea (salían como «```»), no traducía las agregaciones (`Aggregation(2)` en vez de `Count`) y buscaba el tema base en una carpeta equivocada, lo que lo marcaba como «Referencia rota» y además lo duplicaba. |

### Cambios

- **Una sola salida:** el Markdown. Se retiraron `matrices-censo.xlsx`, `censo.json`, sus esquemas y plantillas. El historial pasa a `historial-censos.md`; un `historial-censos.xlsx` existente se conserva sin cambios.
- **`scripts/censo.py`** reemplaza a `validar_censo.py`. Comandos: `borrador`, `pendientes`, `validar`, `registrar`, `inventario`. No requiere paquetes externos.
- **El script genera el borrador completo:** IDs nativos, posiciones, bindings (incluidos cálculos visuales), expresiones completas, uso por clase de dependencia con propagación por DAX, clasificación de columnas, medidas, visuales, bookmarks y recursos, conciliación y hallazgos detectables. La IA completa unos 12 marcadores `[IA: …]`.
- **Un dato, un lugar (R34):** se eliminaron las matrices B, C y D como tablas aparte. La Matriz A muestra conteos por clase con códigos cortos (número, `0`, `NA`, `NV`, `P`); el detalle vive en su sección de origen. La evidencia se indica una vez por tabla. El código M y las expresiones DAX aparecen una sola vez. Los textos visibles solo están en la sección 9.
- **Estados de bookmark agrupados** por página y estado con la lista de `visual_id` (R16).
- **Tablas de fecha automáticas** en una fila por tabla, con el `column_id` de cada columna.
- **Candidatas (18.2)** en una tabla compacta que cubre columnas, medidas, visuales, bookmarks y recursos; riesgo y pruebas por tipo, escritos una vez.
- **Hallazgos detectables automáticos (H-A*)**, agrupados por asunto.
- **Validación en menos de un segundo,** conciliación por ID contra el PBIP.
- **`kiro/steering-censo-bi.md`:** guía de ejecución para Kiro.
- Reglas modificadas: R16, R18, R19, R26 y R32–R38. Checklist reescrito con marcas [S] (lo genera el script) y [V] (lo valida).

### Resultado con GC - Flotillas (PBIP reconstruido con los TMDL reales y las tablas del censo de Kiro)

| | v2.0 (Kiro) | v2.1 (borrador) |
|---|---:|---:|
| Tamaño | 330 KB | 112 KB |
| Líneas | 1.851 | 1.273 |
| Código escrito por la IA | ~90 mil caracteres | 0 |
| Validación | más de 10 min sin terminar | 0,1 s |
| Visuales: válidos / decorativos / botón / rotos | 41 / 15 / 1 / 36 | 41 / 15 / 1 / 36 |

## v2.0 — 2026-11-03

Consolidación completa del paquete. Los anexos acumulados de v1 se integraron en el cuerpo de cada documento; ya no existen bloques “complementarios que no reemplazan lo anterior”.

### Decisión de alcance

- El CENSO **describe y señala; no prescribe cambios**. La modificación, creación y depuración son un DLC aparte que usa el CENSO como base. Consecuencias: `criterios-propuestas.md` pasa a `criterios-puntos-revision.md`; el tipo `Mejora propuesta` desaparece; la matriz de regresión sale de las reglas del censo y queda para el DLC de modificación; la tabla maestra lleva “Objetos afectados y dependencias” y “Punto de revisión”.

### Contradicciones de v1 resueltas

| # | Contradicción v1 | Resolución v2 |
|---|---|---|
| C1 | 17 secciones (contrato) vs. 20 (README, reglas 34 y 29, checklist) vs. 23 (Consolidación); plantilla saltaba de 17 a 21 | Un solo contrato: sección 0 + secciones 1–19, numeración continua; el validador lo comprueba |
| C2 | Secciones “Elementos utilizados / no utilizados” obligatorias y eliminadas a la vez | Eliminadas; el uso vive en Matriz A y en el `estado_uso` de cada hoja |
| C3 | “Punto 13 — Elementos no utilizados” vs. sección 13 = Dependencias | Referencias renumeradas |
| C4 | “No crear un Excel independiente” vs. replicar en Excel | Se replica en Excel y en `censo.json` (R32) |
| C5 | Reglas 29, 30 y 31 duplicadas con contenido distinto | Reglas renumeradas R01–R47 sin repetidos |
| C6 | Anexo “Profundidad individual” A–H repetido casi literal | Integrado una vez en el ritual |
| C7 | Estados de uso distintos en ritual, reglas y hoja LEEME | Un catálogo (CAT-02); `Candidata a depuración` y `No eliminar` pasan a ser marcas, no estados |
| C8 | Resultados por clase con y sin `Pendiente` | CAT-04 con `Pendiente` |
| C9 | Estados del censo: 4 valores, más `Revisión incompleta`, más Borrador/En revisión/Validado | CAT-07 con 5 valores, iguales en las cuatro salidas |
| C10 | Tipo de censo libre en el validador | CAT-08 con 3 valores, validado |
| C11 | “No proponer modificaciones” vs. propuestas con matriz de regresión | Ver “Decisión de alcance” |
| C12 | Matriz C por tabla vs. por tabla × clase | Por tabla × clase |
| C13 | Hora del historial = hora del registro | `--fecha-hora-ejecucion` obligatorio |
| C14 | Ayuda de `--responsable-funcional` confusa sobre nombres | Eliminada la ambigüedad |
| C15 | Se citaba `GC - Flotillas - censo profundizado.md`, que no estaba en el paquete; el único ejemplo (GC - Leads MG) violaba las reglas | Ejemplo antiguo retirado; ver `examples/README.md` |
| C16 | Markdown autocontenido vs. “ver anexo técnico / ver Excel” | R32: ninguna salida remite a otra para un detalle obligatorio |
| C17 | Tablas de la plantilla con separadores de columnas incorrectos | Plantilla reescrita |
| C18 | `column_id` “No disponible” aunque TMDL expone `lineageTag` | CAT-15 fija `lineageTag` como ID de tabla, columna, medida y jerarquía |
| C19 | “No se evalúan dependencias fuera del PBIP” vs. uso de documentos externos | R05: externos solo como contexto `Inferido` y declarados |
| C20 | “Validar las 20 secciones” sin que el validador lo hiciera | El validador comprueba secciones 0–19 |
| C21 | La hoja LEEME del Excel tenía un tercer catálogo de estados | LEEME remite a `catalogos.md` |

### Agregado

- `ai-dlc/catalogos.md` con CAT-01 a CAT-15, incluida la tabla de IDs nativos por objeto.
- Sección 13 **Recursos, tema y presentación**: imágenes y logos con peso y dimensiones, tema, fuentes, textos visibles, metadatos del proyecto.
- Sección 12 separada para bookmarks, botones y navegación.
- Posición y tamaño obligatorios para cada visual.
- `censo.json` + `templates/censo.schema.json` como salida para agentes.
- Hojas nuevas: `Fuentes_conexiones`, `Columnas_afectadas_M`, `Tablas`, `Relaciones`, `Seguridad_roles`, `Medidas`, `Paginas`, `Bindings_visuales`, `Interacciones`, `Bookmarks`, `Botones_navegacion`, `Recursos_presentacion`, `Tema_textos`, `Hallazgos_revision`.
- Columnas `rev_V` … `rev_SEC`, `candidata_depuracion` y `proteccion` en `Inventario_columnas`.
- Columnas `census_id`, `Versión analizada`, `census_id anterior`, `Archivo de matrices`, `Archivo censo.json` y `Versión del ritual` en el historial.
- Validador: `--extraer-pbip`, `--pbip` (conciliación objeto por objeto), comprobación de secciones, IDs truncados, conteos aproximados, verbos de cambio, catálogos, coherencia Markdown–Excel–JSON, migración automática del historial v1.

### Retirado

- `ai-dlc/criterios-propuestas.md` (reemplazado).
- `examples/gc-leads-mg/censo.md` (formato v1 que contradecía las reglas).
- Hojas `Propuestas_IA` (→ `Hallazgos_revision`), `Tablas_relaciones` (→ `Tablas` + `Relaciones`), `Elementos_no_utilizados` y `Elementos_no_utilizados_detalle` (→ `estado_uso` en cada hoja + `Candidatas_depuracion`), `Fuentes_consultas_M_SQL` (→ `Fuentes_conexiones` + `Pasos_M_detallados`).

### Equivalencia de reglas v1 → v2

| v1 | v2 |
|---|---|
| 1 No asumir | R07 |
| 2 Evidencia | R08 |
| 3 No modificar | R01 |
| 4, 5 Uso y no uso | R21, R24 |
| 6 Vacíos | Ritual fase 4 |
| 7, 8 Propuestas | R43, R44 |
| 9 Técnico/funcional | R11 |
| 10 Inferencia | R11 |
| 11 Limitaciones | R10 |
| 12 Cierre | Checklist §19 |
| 13 IDs reales | R12 |
| 14 Rutas | R14 |
| 15 Clave compuesta | R13 |
| 16 Directa/secundaria | CAT-06 |
| 17 Conciliar por página | R18, R46 |
| Correos | R02 |
| 18 Responsables | R03 |
| 19–23 Historial y estado | R37–R41 |
| 24 Una columna por fila | R16 |
| 25 No inventar IDs | R15 |
| 26–28 Clases de dependencia | R22, R23 |
| 29 (1.ª) Clasificación | R21 |
| 30 (1.ª) Impacto sin inventar | R27 |
| 31 (1.ª) No autoriza eliminar | R27 |
| 32 Conciliar columnas | R18 |
| 33 Validación semántica | R09 |
| 34 Markdown autocontenido | R32, R33 |
| 35, 44 Preservar | R35 |
| 36 Inspección real | R10 |
| 37 Protección | R22, R24 |
| 29–31 (2.ª) Markdown + Excel | R32, R34, R36 |
| 38–43 Granularidad | R16–R20 |
| 45 Concordancia | R32 |
| 46–50 Validación y registro | R41, R42 |
| Anexo bookmarks | R28–R31 |
| Tabla maestra | R45, R46 |

## v1 — 2026-10

Versión inicial con anexos sucesivos.
