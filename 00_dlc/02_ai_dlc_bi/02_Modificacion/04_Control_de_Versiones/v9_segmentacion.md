# V9 — Segmentación del AI-DLC: MODIFICACIÓN

- Base de origen: V8 — Repositorio Kiro.
- Acción: reorganización de contenidos en tres DLC independientes.
- Reglas previas: conservadas mediante copia de las reglas transversales y específicas correspondientes.
- No se declara ninguna regla eliminada.
- Regla Kiro: conservada; toda copia de trabajo del agente debe estar en `01_kiro`.
- Próxima actualización: comparar contra V9 y clasificar cada regla como NUEVA, MODIFICADA, REEMPLAZADA, ELIMINADA o CONSERVADA, justificando cualquier cambio.


## Revisión correctiva de Modificación — V9.1

- **MODIFICADA:** secuencia operativa para conservar el PBIP original antes de gestionar el CENSO y crear/usar la copia Kiro solo después de validar el CENSO.
- **MODIFICADA:** ruta de plantilla del Registro de Cambio, ahora enlazada a `00_Base_Compartida/12_plantilla_registro_cambio.md`.
- **MODIFICADA:** ruta del árbol de fuentes, de `01_fuentes` a `00_fuentes`.
- **MODIFICADA:** README y plantilla de solicitud para eliminar instrucciones de Creación dentro de Modificación y registrar las rutas/email obligatorios.
- **ELIMINADA de los checklists de Modificación:** sección específica de bloqueo por CENSO para Depuración; esa regla se mantiene en el DLC de Depuración.
- **CONSERVADAS:** todas las reglas sustantivas de modificación, CENSO, original protegido, Kiro, trazabilidad, aprobaciones, validación y registro histórico.


## Auditoría de cierre de Modificación — V9.2

- **MODIFICADA:** checklist convertido en controles propios de modificación, con estados Cumple/No cumple/No aplica y puertas bloqueantes.
- **MODIFICADA:** rutas de CENSO, PBIP original, Kiro, README y Registro de Cambio unificadas.
- **MODIFICADA:** ruta del logo corporativo normalizada a la ruta relativa oficial bajo `MCP_POWERBI\00_dlc\02_ai_dlc_creacion_modificacion\00_fuentes`.
- **MODIFICADA:** se añadieron condiciones de parada cuando no se identifica el BI, no se puede preservar el original, no existe copia separada o faltan aprobaciones/validaciones.
- **MODIFICADA:** se explicitó el límite entre modificación y depuración general para evitar ampliación silenciosa del alcance.
- **CONSERVADAS:** reglas previas de CENSO obligatorio, PBIP protegido, copia Kiro, correos, README acumulativo, registro central, decisión del analista, diseño corporativo, integridad, visuales ocultos, validación antes/después, codificación y control de evolución de reglas.
- **VALIDACIONES AUTOMÁTICAS:** rutas internas comprobadas; se verificó ausencia de BOM en archivos Markdown; inventario actualizado.
