# Checklist integral — Depuración y Mejora

Este checklist es específico de Depuración. Para los controles transversales de trazabilidad se apoya en las plantillas incluidas, pero no incorpora los pasos de Creación ni los bloqueos propios de Modificación. Cada control se marca `Cumple`, `No cumple`, `No aplica` o `Pendiente`, con evidencia cuando corresponda.

## 1. Preparación y bloqueos
- [ ] Nombre exacto y objetivo de depuración confirmados.
- [ ] Correo de quien trabaja/modifica registrado.
- [ ] Correo de quien solicita/es dueño registrado.
- [ ] README histórico y registro central abiertos/actualizados.
- [ ] CENSO existente, correspondiente y utilizable verificado en `MCP_POWERBI\02_censo`.
- [ ] Si falta/no corresponde/no es utilizable, estado `BLOQUEADO — CENSO REQUERIDO` y ningún cambio ejecutado.
- [ ] Original PBIP protegido en `00_original`.
- [ ] Copia de trabajo preparada en `01_kiro`.
- [ ] Alcance, exclusiones, criterios de aceptación, riesgo y rollback documentados.

## 2. Línea base y evidencia
- [ ] Estado anterior documentado con evidencia.
- [ ] Volumen, columnas, tamaño y tiempos capturados cuando se puedan medir.
- [ ] KPIs, totales, conteos y filtros afectados capturados.
- [ ] Limitaciones y métricas no disponibles declaradas.
- [ ] Matriz de dependencias completada para cambios relevantes.

## 3. Revisión técnica
- [ ] Fuentes, SQL, vistas, Power Query y Dataflows revisados cuando estén en alcance.
- [ ] Se evaluaron filtros en origen, columnas, joins y transformaciones redundantes.
- [ ] Query folding evaluado cuando aplique.
- [ ] Tablas, columnas, claves, granularidad, relaciones, cardinalidad y medidas revisadas.
- [ ] Elementos aparentemente no usados comprobados contra dependencias internas y externas conocidas.
- [ ] DAX revisado cuando esté en alcance; equivalencia semántica comprobada.
- [ ] Visuales rotos/ocultos, marcadores, botones, estados alternativos y objetos heredados revisados.
- [ ] Seguridad/RLS, actualización, navegación, filtros e interacciones afectados probados cuando aplique.

## 3.1 Control de visuales y eliminaciones (V9.5)
- [ ] Inventario previo de visuales/objetos por ID, página y ruta generado cuando aplica.
- [ ] Regex/búsquedas textuales solo localizaron candidatos; cada candidato fue verificado semánticamente.
- [ ] Lista positiva de IDs y acciones exactas aprobadas disponible antes de ejecutar.
- [ ] Bookmarks, botones y estados se analizaron por separado.
- [ ] Inventario posterior comparado por ID y página; cada diferencia está conciliada.
- [ ] No existen desapariciones no autorizadas; si existen, estado bloqueado y reversión documentada.
- [ ] Integridad técnica y funcional registradas por separado.

## 4. Decisiones y ejecución
- [ ] Cada hallazgo contiene evidencia, causa probable, impacto y severidad.
- [ ] Cada propuesta contiene beneficio esperado, riesgo y decisión del analista.
- [ ] Solo se ejecutaron propuestas aprobadas.
- [ ] No hubo cambios estéticos ni ampliaciones de alcance no aprobadas.
- [ ] Cambios de riesgo medio/alto tienen rollback documentado.

## 5. Validación y cierre
- [ ] Se compararon resultados antes/después.
- [ ] Diferencias no esperadas investigadas y resueltas o registradas como bloqueantes.
- [ ] Refresh, conexiones y resultados de negocio afectados validados.
- [ ] Beneficio observado medido o declarado explícitamente como no medido.
- [ ] Codificación/BOM revisados en archivos modificados cuando corresponda.
- [ ] README histórico, Registro de Cambio y registro central actualizados.
- [ ] Alertas, riesgos residuales y pendientes comunicados.
- [ ] No hay bloqueantes abiertos antes de declarar `Listo para entrega`.
