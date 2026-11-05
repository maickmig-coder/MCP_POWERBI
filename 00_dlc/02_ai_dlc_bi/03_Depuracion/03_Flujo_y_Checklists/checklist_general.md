# Checklist operativo — Depuración y Mejora

Marcar cada control como `Cumple`, `No cumple`, `No aplica` o `Pendiente`, adjuntando evidencia. No dejar casillas ambiguas.

## A. Ingreso y clasificación
- [ ] Se confirmó el nombre exacto del BI.
- [ ] Se confirmó que la solicitud corresponde a Depuración/Mejora y no a creación, modificación funcional o rediseño estético.
- [ ] Si mezcla procesos, se separaron las solicitudes, dependencias, responsables y orden de ejecución.
- [ ] Se registró únicamente el correo de quien trabaja y el correo de quien solicita/es dueño.
- [ ] Se abrió el README histórico existente; no se creó un historial paralelo para el mismo BI.
- [ ] Se actualizó el registro central.
- [ ] Se documentó objetivo, alcance, exclusiones, criterios de aceptación y fecha.

## B. Bloqueos previos obligatorios
- [ ] Se buscó el CENSO en `MCP_POWERBI\02_censo`.
- [ ] El CENSO corresponde al nombre exacto del BI y refleja un estado útil para el análisis.
- [ ] Si no existe/no corresponde/no está accesible, el estado es `BLOQUEADO — CENSO REQUERIDO`; no se ejecutaron cambios.
- [ ] El PBIP original está preservado en `MCP_POWERBI\01_bi\01_versiones\00_original\[Nombre exacto BI]`.
- [ ] Existe copia de trabajo en `MCP_POWERBI\01_bi\01_versiones\01_kiro\[Nombre exacto BI]`.
- [ ] Se verificó que el trabajo se realiza sobre `01_kiro`, nunca sobre `00_original`.
- [ ] Se registraron versión/commit/referencia, rutas y mecanismo de reversión.

## C. Línea base antes de cambios
- [ ] Se registraron tamaño del PBIP/modelo y volumen de filas/columnas cuando estén disponibles.
- [ ] Se registraron tiempos de actualización/refresh y consultas relevantes cuando puedan medirse.
- [ ] Se capturaron resultados de referencia para KPIs, totales, conteos y filtros afectados.
- [ ] Se documentaron errores existentes, limitaciones de acceso y métricas no disponibles.
- [ ] Se creó matriz de dependencias para cada elemento candidato a cambio.
- [ ] Se asignó riesgo bajo/medio/alto y se definió rollback para cambios de riesgo medio/alto.

## D. Fuentes, SQL y consultas
- [ ] Se identificaron todas las fuentes conocidas y credenciales/puertas de enlace relevantes sin exponer secretos.
- [ ] Se revisó SQL, vistas, joins, filtros, columnas seleccionadas y predicados cuando el acceso lo permita.
- [ ] Se revisó Power Query, pasos redundantes, tipos, conversiones y filtros.
- [ ] Se evaluó si las operaciones pueden ejecutarse en origen y si se conserva query folding cuando aplique.
- [ ] Se identificaron filas/columnas cargadas y luego descartadas.
- [ ] Se evaluaron cambios de origen y sus impactos en permisos, actualización y resultados.
- [ ] Se preguntó al analista si desea revisión de consultas/fuentes cuando esa revisión no esté incluida explícitamente en el alcance.

## E. Modelo y campos
- [ ] Se revisaron tablas, columnas, medidas, relaciones, cardinalidad, dirección de filtro, claves y granularidad.
- [ ] Se verificaron columnas candidatas a no uso contra visuales, filtros, relaciones, jerarquías, medidas, cálculos y transformaciones conocidas.
- [ ] Se consideraron dependencias externas conocidas, exportaciones, paginated reports, Excel u otros consumidores cuando aplique.
- [ ] Ningún elemento fue eliminado por la sola ausencia de uso visible.
- [ ] Se revisaron duplicidades, cardinalidad alta, tablas/columnas redundantes y tipos de datos.

## F. DAX y cálculo
- [ ] Se revisaron fórmulas relevantes o se dejó constancia de que no estaban en alcance.
- [ ] Se evaluaron lógica duplicada, filtros repetidos, conversiones, cadenas de medidas y reutilización.
- [ ] Cada simplificación propuesta conserva semántica, contexto de filtro, tratamiento de BLANK/null y límites temporales.
- [ ] Se compararon resultados de la fórmula anterior y la propuesta con casos representativos y límites.
- [ ] No se cambió una regla de negocio por una optimización técnica sin aprobación funcional.

## G. Integridad del reporte
- [ ] Se revisaron visuales rotos y referencias a tablas/columnas/medidas inexistentes.
- [ ] Se revisaron visuales ocultos, panel Selección, marcadores, botones, estados alternativos, tooltips y navegación.
- [ ] Se revisaron objetos heredados de copias y páginas ocultas.
- [ ] Se verificó que los cambios no dañaran filtros, interacciones, drill-through, RLS ni navegación afectados.
- [ ] No se realizó rediseño estético fuera del alcance.

## G2. Inventario y protección de visuales (V9.5)
- [ ] Existe inventario antes de cambios con página, ID de página, título, tipo, ID técnico, ruta y visibilidad cuando esté disponible.
- [ ] Campos/medidas activos se distinguen de filtros, metadatos y referencias secundarias.
- [ ] Coincidencias de texto/regex se tratan solo como candidatos y se revisó su contexto semántico.
- [ ] Existe lista positiva con IDs exactos y acciones aprobadas antes de borrar/reparar.
- [ ] Ningún objeto no enumerado fue afectado por una aprobación grupal.
- [ ] Bookmarks, botones y estados alternativos se analizaron por separado y no se borraron colecciones completas por defecto.
- [ ] Existe inventario posterior y comparación por ID y página.
- [ ] Toda desaparición no aprobada o diferencia no explicada se resolvió/revirtió; de lo contrario el caso está bloqueado.
- [ ] La integridad técnica y la funcional se reportan por separado.
- [ ] Las pruebas no ejecutadas se marcaron `No validado`; no se afirmaron como exitosas.

## H. Aprobación y ejecución
- [ ] Cada hallazgo tiene evidencia, causa probable, impacto, propuesta y beneficio esperado.
- [ ] El analista aprobó/rechazó/dejó pendiente cada acción.
- [ ] No se ejecutó ninguna acción rechazada o pendiente.
- [ ] Se aplicaron cambios en unidades pequeñas y rastreables cuando fue posible.
- [ ] Cada etapa se validó antes de ejecutar el siguiente grupo; ante un fallo se detuvo la secuencia.
- [ ] Se registró cómo revertir cada cambio de riesgo medio/alto.

## I. Validación después del cambio
- [ ] Se compararon KPIs, totales, conteos, filtros y resultados antes/después.
- [ ] Se investigaron diferencias no esperadas; las diferencias esperadas tienen explicación.
- [ ] Se validó refresh y conexión a las fuentes afectadas.
- [ ] Se midieron de nuevo tamaño, volumen, duración o rendimiento cuando era parte del objetivo y se pudo medir.
- [ ] Se revisaron visuales, medidas, relaciones y dependencias afectadas.
- [ ] Se validó que la solución no haya creado errores funcionales o técnicos nuevos.
- [ ] Se verificó codificación UTF-8/BOM de los archivos de texto modificados cuando corresponda.
- [ ] Se registró evidencia de prueba y limitaciones.

## J. Cierre y reversibilidad
- [ ] Se actualizó README histórico con hallazgos, decisiones, cambios y rutas.
- [ ] Se actualizó Registro de Cambio cuando corresponda.
- [ ] Se actualizó `REGISTRO_CONTROL_TABLEROS.md`.
- [ ] Se registraron beneficios esperados y observados, sin atribuir beneficios no medidos.
- [ ] Alertas, riesgos residuales y pendientes fueron comunicados.
- [ ] Se confirmó rollback disponible o se documentó por qué no aplica.
- [ ] El estado `Listo para entrega` solo se asignó si no hay bloqueantes abiertos y las pruebas aplicables pasaron.

## Reglas de no cierre
No cerrar como listo si falta CENSO válido, el original no está protegido, no existe copia Kiro, hay diferencias no explicadas, fallan pruebas críticas, existe un bloqueante abierto, se ejecutó un cambio no aprobado, desapareció un objeto sin autorización exacta o hay diferencias de inventario no conciliadas.
