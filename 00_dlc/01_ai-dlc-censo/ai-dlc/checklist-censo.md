# Checklist del CENSO BI (v2.3)

**[S]** = lo genera `censo.py borrador`. **[V]** = lo comprueba `censo.py validar`. Sin marca = lo revisa la IA o una persona. Un punto con [S] no debe rehacerse a mano.

## Antes de empezar

- [ ] **[V]** Correo de quien realiza el CENSO y correo del dueño/responsable del tablero registrados; sin ellos el script no se ejecuta.
- [ ] Tipo de censo decidido con la tabla de la Fase 0 del ritual (Inicial, Actualización o Validación).
- [ ] **[V]** En `Actualización`: el usuario confirmó que guardó el PBIP de la versión nueva en `01_versiones/<versión>/<BI>` (`--pbip-guardado-confirmado`), la carpeta coincide con `--version` y la huella es distinta a la del censo vigente (R54).

## Borrador (fase 1)

- [ ] **[S][V]** Secciones 0–18 en orden.
- [ ] **[S][V]** census_id, fecha y hora con zona horaria, tipo de CAT-08.
- [ ] **[S][V]** IDs nativos completos (CAT-15), sin `…`.
- [ ] **[S]** Código M completo una sola vez (sección 4) y expresiones DAX una sola vez (6.1 y 7).
- [ ] **[S][V]** Una fila por columna de cada tabla, con resultado por clase y estado de uso; conciliada contra el PBIP.
- [ ] **[S][V]** Una fila por medida, página, visual, filtro, interacción, bookmark y recurso; conciliadas contra el PBIP.
- [ ] **[S]** Posición, tamaño y bindings de cada visual; resumen por clase que suma el total de la página.
- [ ] **[S]** Archivos de recursos con ruta, peso y tamaño original; ubicación por página de banners, logos, formas y textos con escala de cada imagen; tema y metadatos.
- [ ] **[S]** Visuales con «Formato huérfano» separados de los que tienen referencia rota de datos.
- [ ] **[S]** Bookmarks con targets (existen / funcionan), efecto real (12.2) y matriz de estados guardados sin efecto (12.3).
- [ ] **[S]** Hallazgos detectables (H-A*), vacíos estándar (V-A*) y candidatas (17.2).
- [ ] Si ya existía un censo, el script escribió `… - censo.borrador.md` y se integraron los hallazgos previos (R35).

## Interpretación (fase 2)

- [ ] **[V]** Ningún marcador `[IA: …]` pendiente (`censo.py pendientes`).
- [ ] Estado del encabezado elegido según CAT-07 y justificado en 18.2.
- [ ] Área, objetivo y pregunta central con certeza `Encontrado`, `Inferido` o `Desconocido`.
- [ ] Rol y granularidad de cada tabla de la 5.1.
- [ ] Interpretación funcional de cada KPI (sección 10); los títulos que no coinciden con lo calculado están en la 17.
- [ ] Interpretación y certeza de cada regla de negocio (14).
- [ ] Mapa de arquitectura de 5–12 líneas en la 15, sin repetir inventarios.
- [ ] Vacíos y limitaciones propios agregados o declarados como «Sin … adicionales».
- [ ] Filas H-A* y V-A* revisadas: certeza, prioridad e impacto ajustados; ningún asunto repetido en otra fila o sección.
- [ ] Todo ID agregado por la IA lleva su nombre (R48).
- [ ] **[V]** Las filas de la IA en la sección 16 no citan filas H-A/V-A y usan prefijos H01/V01 (R50).
- [ ] **[V]** Las limitaciones agregadas por la IA no citan hallazgos ni vacíos (error) ni repiten una estándar (advertencia) (R49).
- [ ] 2.1, 10, 14 y 15 no afirman lo que un vacío declara desconocido, ni siquiera citándolo (R50).
- [ ] **[V]** Sección 14: cada columna calculada se interpreta desde su expresión (6.1) y su estado de uso; certeza «Inferido» (R51).
- [ ] **[V]** Sin verbos de cambio en la columna «Punto de revisión» (R47).
- [ ] **[V]** Valores de catálogo en tipo, prioridad, certeza y estado de la sección 16.
- [ ] No se reescribieron tablas mecánicas ni se crearon scripts propios (R36).

## Versiones y validación con el dueño

- [ ] **[V]** En `Actualización` o `Validación`: `comparar` ejecutado con el origen correcto; existe `[BI] - cambios.borrador.md` (R52).
- [ ] **[V]** Sección 14: «Validación del dueño» = `No requerida` solo en reglas `Encontrado`; las `Inferido` quedan `Pendiente de validación` hasta la respuesta (R55).
- [ ] **[V]** Todo punto `Confirmado por el dueño` o `Descartado por el dueño` (14 y 16) tiene «Respuesta del dueño» con fecha (R55).
- [ ] **[V]** Si el ejecutor es el dueño: cada punto pendiente tiene respuesta o constancia de que se preguntó (R55).

## Cierre (fases 3 a 5)

- [ ] **[V]** `censo.py validar --pbip` sin errores.
- [ ] **[V]** Sin conteos aproximados (`≈`, “aprox.”).
- [ ] **[V]** Ninguna columna `Sin uso interno identificado` con referencias en V, F, D, M, PQ o BK (R22).
- [ ] **[V]** `Completado y validado` solo con validación contra el PBIP.
- [ ] **[V]** La huella del PBIP coincide con la del encabezado (R53).
- [ ] **[V]** `Completado y validado` sin puntos `Pendiente de validación` en 14 y 16 (R56).
- [ ] `censo.py registrar` archivó el censo anterior en `versiones/`, agregó el bloque a `[BI] - cambios.md` y la fila a `historial-censos.md`; lo anterior sigue intacto.
- [ ] `censo.py vigencia` ejecutado: su resultado (APTO / NO APTO) se informa al usuario (R56).
