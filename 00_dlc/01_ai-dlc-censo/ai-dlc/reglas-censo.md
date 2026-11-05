# Reglas del CENSO AI-DLC (v2.3.2)

Reglas obligatorias en todo CENSO. Están numeradas de corrido y agrupadas por tema; cada número existe una sola vez. Los valores permitidos están en `catalogos.md`; la secuencia de trabajo, en `ritual-censo-bi.md`.

La equivalencia con la numeración de v1 está en `CHANGELOG.md`. En v2.1 cambiaron R16, R18, R19, R26 y R32–R38; en v2.2, R25, R29, R33, R45 y se agregó R48; en v2.2.1 se agregaron R49 y R50; en v2.2.2 se precisaron R49 y R50; en v2.2.3 se retiró R03; en v2.2.4 se agregó R51; en v2.3 cambiaron R35, R39 y R41 y se agregaron R52–R56; en v2.3.1 se agregaron R57 y R58; en v2.3.2, R59.

---

## A. Gobierno y alcance

**R01 — Solo lectura.** El CENSO no modifica, borra, reconstruye ni publica el PBIP, el modelo, las consultas ni los visuales.

**R02 — Correos antes de empezar.** Sin el correo de quien realiza el CENSO y el del dueño/responsable del tablero no se lee el PBIP ni se produce ninguna conclusión. No se aceptan nombres ni `Pendiente de confirmar` como sustitutos.

**R03 — Retirada en v2.2.3.** El censo no registra responsables funcional y técnico: el dueño/responsable del tablero (R02) responde por ambos papeles.

**R04 — El CENSO describe, no prescribe.** Los hallazgos dicen qué condición existe, dónde, con qué evidencia y qué objetos afecta. No dicen cómo corregirla. La modificación, creación y depuración pertenecen a su propio DLC (ver `criterios-puntos-revision.md`).

**R05 — Alcance = el PBIP.** La evidencia válida son los archivos del PBIP. Documentos externos solo como contexto marcado `Inferido` y listados como fuente inspeccionada. Las dependencias fuera del PBIP (consumidores, procesos de carga) se declaran `No verificable`.

**R06 — Sin secretos.** No se registran contraseñas, tokens, llaves ni cadenas de conexión con credenciales en ninguna salida.

## B. Evidencia y certeza

**R07 — No asumir.** Toda afirmación lleva certeza `Encontrado`, `Inferido` o `Desconocido` (CAT-01).

**R08 — Evidencia localizable.** Cada hallazgo, dependencia y clasificación indica archivo, ruta y propiedad o expresión observada, de forma que se pueda volver al archivo.

**R09 — Lectura estructural, no textual.** Una coincidencia de texto en el JSON o el TMDL no prueba una dependencia. Se interpreta el contexto (binding, expresión DAX, paso M). Lo ambiguo queda `No determinada`.

**R10 — Declarar lo no revisado.** Lo que no se pudo abrir o verificar se registra `No verificable` o `Pendiente` y aparece en limitaciones. Nunca se declara revisada una capa que no se recorrió.

**R11 — Técnico y funcional separados.** Cuando sea posible, cada regla y KPI indica qué hace técnicamente y qué significa funcionalmente. Una regla solo inferida se marca `Inferido`.

## C. Identificadores

**R12 — IDs nativos completos.** Se usan los identificadores de CAT-15 tal como aparecen en el archivo, completos. Prohibido truncar con `…`, `...` o recortes. Prohibido usar el título visible como ID.

**R13 — Claves compuestas marcadas.** `compound_key` (versión + `page_id` + `visual_id`) y `column_compound_key` (versión + tabla + columna) sirven para comparar versiones y se marcan siempre como no nativas.

**R14 — Rutas exactas.** `page_path`, `visual_path`, rutas de `.tmdl`, bookmarks y recursos se escriben completas desde la raíz del PBIP.

**R15 — No inventar IDs.** Si un objeto no tiene ID nativo (por ejemplo, un filtro de página sin visual), el campo es `No aplica` o `No disponible`.

## D. Granularidad y conciliación

**R16 — Una fila por objeto.** Columnas, pasos M, medidas, páginas, visuales, bindings, filtros, segmentaciones, interacciones, bookmarks, botones y recursos tienen fila propia. Excepciones permitidas porque no pierden trazabilidad: los estados de un bookmark se agrupan por página y estado, listando cada `visual_id` (12.2); las tablas de fecha automáticas se listan una por fila con el `column_id` de cada columna (6.2).

**R17 — Conteos exactos.** Todo conteo sale de un inventario individual. Prohibido `≈`, “aprox.”, “unos”. Las sumas de un resumen deben dar el total.

**R18 — Conciliación contra el PBIP.** `censo.py validar --pbip` compara objeto por objeto (por ID) visuales, páginas, tablas, columnas, medidas, relaciones, bookmarks y recursos, y cuenta filtros e interacciones. Toda diferencia es un error que se corrige antes de cerrar.

**R19 — Expresiones completas, una sola vez.** El código M va completo en la sección 4; las expresiones DAX, en 6.1 y 7. Los literales de más de 300 caracteres (por ejemplo, tablas embebidas en base64) se reemplazan por un aviso con la ruta del archivo.

**R20 — Tipos por etapa.** Si una columna cambia de tipo en M, se registran el tipo anterior y el posterior en el paso que lo cambia.

## E. Clasificación del uso

**R21 — Estados del catálogo.** El estado de uso es uno de CAT-02. `Candidata a depuración` y `No eliminar` son marcas aparte, no estados.

**R22 — Mínimo para “Sin uso”.** Una columna solo es `Sin uso interno identificado` si las clases V, F, D, M, PQ y BK tienen resultado `No encontrada en el alcance revisado` o `No aplica`. Si alguna queda `No verificable` o `Pendiente`, el estado es `Uso desconocido`.

**R23 — Resultado por clase.** Cada columna registra un resultado de CAT-04 para cada clase de CAT-03.

**R24 — No visuales ≠ sin uso.** La ausencia en visuales no basta. Una columna puede alimentar DAX, relaciones, filtros, ordenamiento, seguridad o pasos M.

**R25 — Oculto ≠ sin uso; formato huérfano ≠ roto.** Un visual oculto físicamente o por bookmark no es, por eso, inexistente ni sin uso. Un visual cuyos datos son válidos pero que conserva reglas de formato que apuntan a entidades inexistentes funciona: se registra como «Formato huérfano», no como «Referencia rota», y no es candidato a depuración.

**R26 — Candidatas completas.** Toda columna, medida, visual, bookmark o recurso con estado `Sin uso interno identificado` o `Referencia rota` aparece en la sección 17.2 (las columnas de tablas de fecha automáticas se tratan en el hallazgo de inteligencia de tiempo automática).

**R27 — Aprobación pendiente.** La aprobación de toda candidata es `Pendiente; el CENSO no autoriza eliminar`. El impacto que no se puede medir es `No estimable con la evidencia disponible`.

## F. Bookmarks, estados y navegación

**R28 — Página física vs. estado.** Una página puede tener varias vistas según el bookmark activo. Se mantienen dos inventarios: físico (`page_id + visual_id`) y de estados (`page_id + visual_id + bookmark_id`). Una aparición en un bookmark no es un visual nuevo.

**R29 — Inspección individual y efecto real.** Cada bookmark se documenta con sus targets (si existen y si funcionan), el efecto que realmente aplica al activarse y los estados guardados sin efecto. No se extrapola un bookmark a otros.

**R30 — Botón → bookmark solo si está escrito.** La relación se registra solo si el `visualLink` del botón la declara. Si no, `No verificable`.

**R31 — Referencia rota confirmada.** Antes de marcar `Rota`, se contrasta contra todas las tablas, columnas, medidas, páginas, visuales y bookmarks del PBIP.

## G. Salidas

**R32 — Una sola salida.** El resultado es un único Markdown, `[Nombre exacto del BI] - censo.md`, más `historial-censos.md`. No se generan Excel ni JSON.

**R33 — Estructura fija.** El Markdown tiene las secciones 0–18 del ritual, en orden y con numeración continua. Se pueden añadir subsecciones.

**R34 — Un dato, un lugar.** Cada dato se escribe en una sola sección; las demás lo citan por su ID. La Matriz A muestra cuántas referencias hay por clase; el detalle está en la sección de origen (V → 9, F → 11, D → 6.1 y 7, M → 5, BK → 12). Las rutas de evidencia se escriben una vez por tabla. No se agregan matrices que repitan otras tablas.

**R35 — El censo muestra el estado actual.** Cada versión nueva del PBIP se censa completa desde cero. Si ya existe un censo, `borrador` escribe `[BI] - censo.borrador.md`; `comparar` traslada lo que el censo vigente ya resolvió (interpretaciones y validaciones de las secciones 14 y 16 cuyos objetos siguen existiendo) y `registrar` archiva el censo anterior en `versiones/` y deja el borrador como censo vigente. Nunca se edita a mano un censo archivado.

**R36 — Lo mecánico lo hace el script.** Inventarios, IDs, posiciones, bindings, expresiones, clasificación de uso y conciliación los genera `censo.py`. La IA completa solo los marcadores `[IA: …]` y la revisión de la sección 16; no reescribe tablas mecánicas ni crea scripts propios para generarlas. Si detecta un error del script, lo registra en la sección 17.

## H. Historial y estado

**R37 — Historial por tablero.** Cada BI tiene su `historial-censos.md` en su carpeta de salida. Un `historial-censos.xlsx` de v2.0 se conserva sin cambios.

**R38 — Append-only.** Cada ejecución agrega una fila mediante `censo.py registrar`. Prohibido borrar o reescribir filas anteriores. Generar un borrador no es una ejecución registrada.

**R39 — Contenido de la fila.** `census_id`, fecha y hora reales con zona horaria, tipo (CAT-08), versión analizada, huella del PBIP, `census_id` anterior, alcance, ambos correos, estado (CAT-07), cantidad de puntos pendientes de validación, archivo, versión del ritual, resultado del validador y observaciones. Si el historial existe con otras columnas, se conservan las suyas (R38).

**R40 — Historial de CENSO, no de cambios.** El historial no registra cambios al BI.

**R41 — Estado honesto.** No queda ningún punto «Pendiente de validación» en las secciones 14 y 16 (R56). `Completado y validado` solo si `censo.py validar --pbip` no tiene errores y no quedan clases `NV` o `P` ni hallazgos que requieran confirmación. El estado del encabezado es el que se registra en el historial.

**R42 — Registro después de validar.** La fila del historial se agrega solo después de que el validador de contenido termina sin errores.

## I. Hallazgos y puntos de revisión

**R43 — Basados en evidencia.** Cada registro de la tabla maestra responde: ¿qué encontraste que te llevó a registrar esto?

**R44 — Sin genéricos.** No se incluyen recomendaciones estándar sin relación con la evidencia del BI.

**R45 — Una fila por asunto.** Hallazgos, riesgos, vacíos y observaciones van en una sola tabla maestra (sección 16). Ninguna otra sección repite un asunto que ya tiene fila allí. Un mismo asunto que afecta varios objetos lista todos sus IDs en esa fila; el detalle de cada objeto está en su sección de origen.

**R46 — Localización completa.** Un hallazgo sobre un visual incluye página (nombre), `page_id`, `visual_id`, título, campo o medida que realmente usa y la diferencia entre lo que el visual comunica y lo que calcula.

**R47 — Sin verbos de cambio.** La tabla maestra no usa “cambiar”, “eliminar”, “reemplazar”, “corregir”, “usar X en lugar de Y” ni “desactivar”. Usa “revisar”, “confirmar con el dueño”, “validar visualmente”.

## J. Identificación

**R48 — Nombre junto a cada ID.** Todo ID que relaciona objetos (visual, página, bookmark, medida, tabla) se escribe con su nombre legible (`ID · nombre`), para que se pueda identificar sin abrir el PBIP. El nombre de un visual es su título; si no tiene, su texto; si tampoco, su tipo y el campo o la imagen que muestra.

**R49 — Limitaciones solo del proceso.** La sección 17.1 describe qué no pudo revisar el censo y por qué. Los problemas del tablero (métricas, referencias rotas, vacíos de negocio) van solo en la sección 16; una limitación no cita filas H o V ni repite con otras palabras una de las 5 estándar. El validador da error si cita filas y advertencia si se parece a una estándar.

**R50 — Sin agrupadores ni contradicciones.** Una fila agregada por la IA en la sección 16 no cita filas `H-A`/`V-A` (si es el mismo asunto, se ajusta esa fila; el validador lo comprueba) y usa los prefijos `H01`, `V01`…. Ningún texto interpretativo (2.1, 10, 14, 15) afirma lo que un vacío declara desconocido: lo cita sin adjetivarlo (no «valor facturado (ver V01)», sino «valor, definición pendiente: V01»).

**R51 — Interpretar desde la evidencia.** Una columna calculada se interpreta desde su expresión en 6.1, no desde su nombre («DIVISION S» es el semestre S1/S2 según el mes, no una «división»), y la interpretación respeta su «Estado de uso»: si es «Sin uso interno identificado», lo dice y no le atribuye segmentaciones ni separaciones que el censo no encontró. La expresión está Encontrada, pero su significado de negocio es «Inferido» salvo que el PBIP lo documente. Aplica a las secciones 2, 10, 14 y 15. El validador avisa en la sección 14.

## K. Versiones, validación con el dueño y paso al DLC

**R52 — Registro de cambios entre versiones.** Cada ejecución registrada agrega un bloque a `[BI] - cambios.md` (append-only): versión y censo anterior, origen del cambio, huella anterior y nueva, objetos agregados, eliminados y modificados (ID y nombre) y cambios de estado de la validación del dueño. Lo genera `censo.py comparar`; la IA no lo redacta. El origen es obligatorio: «DLC de modificación <ID>», «DLC de depuración <ID>», «Validación con el dueño» o «No informado». Si el tablero cambió y el origen es «No informado», el bloque lleva una alerta: el PBIP se modificó fuera del DLC.

**R53 — Huella y vigencia.** El encabezado del censo lleva la huella del PBIP (SHA-256 de sus archivos, sin `.pbi` ni caché). `validar --pbip` da error si la huella no coincide: el tablero se guardó después del borrador. `censo.py vigencia` dice si el censo es de la última versión guardada en `01_versiones` y si su huella coincide; si no, el censo está **desactualizado** y no describe el tablero final. Quien revise un censo empieza por `vigencia`.

**R54 — Versión nueva guardada antes del censo.** Antes de un censo de tipo `Actualización`, la IA pregunta al usuario si guardó el PBIP de la versión nueva en `01_bi/01_versiones/<versión>/<BI>` y, solo con su confirmación, ejecuta `borrador` con `--pbip-guardado-confirmado`. El script bloquea si falta la confirmación, si no hay archivo `.pbip`, si la carpeta no coincide con `--version`, si esa versión ya está censada o si la huella es idéntica a la del censo vigente (el cambio no se guardó en la ruta nueva). Cada cambio al tablero se guarda como una versión nueva; no se sobrescribe una versión ya censada.

**R55 — Validación con el dueño.** Requieren respuesta del dueño los puntos de la sección 16 y las reglas de la sección 14 con certeza `Inferido` («Validación del dueño» = `Pendiente de validación`); las reglas `Encontrado` van con `No requerida`. Cada respuesta se escribe en «Respuesta del dueño» con fecha y texto, y el estado pasa a `Confirmado por el dueño` o `Descartado por el dueño`.
- **Si quien realiza el censo es el dueño** (los dos correos coinciden): la IA le presenta los puntos pendientes en la misma ejecución y registra cada respuesta. Si el dueño no sabe una respuesta, el punto queda `Pendiente de validación` con la constancia («fecha: se preguntó; el dueño no lo sabe»). El validador da error si un punto pendiente no tiene respuesta ni constancia.
- **Si es otra persona:** el censo cierra como `Completado pendiente de validación`. Después se ejecuta `censo.py iniciar-validacion` (mismo PBIP, misma huella): si quien la inicia es el dueño, valida directamente; si no, aplica R58. Se registran las respuestas y se cierra con `comparar --origen "Validación con el dueño"` y `registrar`.

**R56 — Bloqueo del DLC de modificación y depuración.** El DLC de modificación, creación o depuración solo parte de un censo que `censo.py vigencia` declare **APTO**: censo vigente (última versión, huella coincidente, sin borrador abierto), estado `Completado y validado` y ningún punto `Pendiente de validación` en las secciones 14 y 16. Un punto que el dueño no sabe responder mantiene el bloqueo hasta que se confirme. El DLC cita el `census_id` del censo con el que parte.

**R57 — Correo de quien revisa.** Toda consulta o revisión de un censo existente (vigencia, pendientes, validación, inicio de una validación) empieza pidiendo el correo de quien revisa; no se aceptan nombres. Los comandos `vigencia`, `pendientes`, `validar` e `iniciar-validacion` lo exigen (`--correo-revisor`) y agregan una fila a `revisiones-censo.md` de la carpeta del BI (append-only): fecha y hora, correo, rol (dueño del tablero o no), comando, census_id y resultado. Así se sabe quién trabajó sobre cada censo.

**R58 — Validación por alguien que no es el dueño.** Si quien pide iniciar la validación tiene el correo del dueño (sección 0), la validación la hace el dueño y se inicia sin más preguntas. Si no, la IA le pregunta si conoce las respuestas de los puntos pendientes y si acepta iniciar la validación sin ser el dueño. Solo con su aceptación explícita se ejecuta `iniciar-validacion --acepta-validar-sin-ser-dueno`, que deja en la sección 0 su correo como ejecutor y la línea «Validación sin ser el dueño: Sí», con la fecha de la aceptación. Sin aceptación, el script bloquea y lo registra. En toda Validación, cada punto pendiente lleva respuesta o constancia (R55). El historial muestra que ejecutor y dueño son distintos, y el dueño puede revisar ese registro.

**R59 — Presentación punto por punto.** La validación con el dueño (o con quien aceptó validar, R58) se conduce un punto a la vez, en el orden de `censo.py guia-validacion` (prioridad alta, reglas inferidas, media y baja). Cada punto se presenta en lenguaje de negocio, sin IDs, código ni términos técnicos sin traducir, con cuatro partes: qué se encontró (página y título del gráfico), por qué importa (impacto concreto en la lectura o en las decisiones), qué se necesita confirmar (una pregunta concreta) y cómo puede responder. Cada respuesta se registra apenas se recibe, con fecha, correo y las palabras de quien responde, y se confirma en una línea antes de pasar al siguiente punto. La plantilla, el glosario y un ejemplo están en `kiro/steering-censo-bi.md`.
