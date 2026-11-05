# Plantilla — Solicitud, diagnóstico y registro de Depuración/Mejora

## 1. Identificación y control
- Nombre exacto del BI:
- Fecha de inicio:
- Correo de quien trabaja/modifica:
- Correo de quien solicita/es dueño:
- Objetivo medible de la intervención:
- Alcance incluido:
- Fuera de alcance:
- Criterios de aceptación:
- Versión/referencia analizada:
- Ruta del original PBIP (`00_original`):
- Ruta de la copia de trabajo (`01_kiro`):
- README histórico actualizado: Sí / No
- Registro central actualizado: Sí / No

## 2. CENSO y condiciones previas
- Ubicación del CENSO:
- Nombre exacto coincide: Sí / No
- Estado/fecha/versión del CENSO:
- CENSO utilizable: Sí / No
- Si falta o no coincide, estado: `BLOQUEADO — CENSO REQUERIDO`
- PBIP original protegido: Sí / No
- Copia Kiro preparada: Sí / No
- Referencia/commit de reversión:

## 3. Línea base (antes)
- Tamaño del modelo/proyecto:
- Filas/columnas relevantes:
- Duración de actualización:
- Duración/consulta de referencia:
- KPIs/totales/conteos de referencia:
- Errores conocidos:
- Evidencia (archivo, consulta, medida, visual, captura, log):
- Métricas no disponibles y motivo:

## 3.1 Inventario de visuales y objetos antes del cambio (cuando aplique)
- Archivo de inventario previo:
- Método de identificación (IDs/rutas):
- Objetos visibles/ocultos revisados:
- Referencias sospechosas verificadas semánticamente:
- Limitaciones de inspección:
- Matriz de eliminación segura: `02_Plantillas/04_inventario_visual_y_eliminacion_segura.md`
- Hash/commit o copia recuperable de referencia:

## 4. Hallazgos
| ID | Capa (fuente/SQL/Power Query/modelo/DAX/visual/archivo) | Elemento y ubicación | Evidencia | Encontrado/Inferido/Desconocido | Causa probable | Impacto | Riesgo |
|---|---|---|---|---|---|---|---|
| H-01 | | | | | | | |

## 5. Dependencias e impacto
| Hallazgo/elemento | Depende de | Consumido por | Impacto funcional | Impacto técnico | Impacto en refresh/seguridad | Prueba requerida | Rollback |
|---|---|---|---|---|---|---|---|
| H-01 | | | | | | | |

## 6. Propuestas y decisión del analista
| ID | Acción propuesta | Beneficio esperado | Riesgo/impacto | Evidencia | Decisión (Aprobado/Rechazado/Pendiente) | Correo/fecha de decisión |
|---|---|---|---|---|---|---|
| P-01 | | | | | | |

## 6.1 Lista positiva de acciones autorizadas
| ID propuesta | Página/ID página | Título/tipo | ID técnico/ruta | Acción exacta aprobada | Dependencias verificadas | Evidencia de aprobación |
|---|---|---|---|---|---|---|
| | | | | | | |

Regla: no ejecutar acciones ausentes de esta lista ni ampliar una aprobación a objetos encontrados después.

## 7. Ejecución aprobada
- ID de propuesta aprobada:
- Cambio ejecutado exactamente:
- Archivos/objetos afectados:
- Fecha y versión resultante:
- Diferencias respecto a lo aprobado:
- Si hubo desviación, justificación y autorización:
- Rollback ejecutado (si aplica):

## 8. Validación después
- KPIs/totales/conteos comparados:
- Resultados esperados y tolerancias aprobadas:
- Diferencias esperadas:
- Diferencias no esperadas e investigación:
- Pruebas de refresh/conexión:
- Pruebas de medidas, filtros, relaciones y visuales:
- Tamaño/filas/columnas después:
- Tiempo de actualización antes/después:
- Métricas de rendimiento antes/después:
- Evidencias de prueba:
- Resultado: Aprobado / Fallido / Parcial / Bloqueado

## 8.1 Conciliación del inventario posterior
- Archivo de inventario posterior:
- Elementos conservados:
- Elementos reparados/modificados:
- Elementos eliminados con aprobación exacta:
- Elementos nuevos:
- Desapariciones no autorizadas:
- Diferencias por página/ID y explicación:
- Resultado de conciliación: Aprobado / Fallido / Bloqueado

## 8.2 Validación técnica y funcional (separadas)
- Integridad técnica (JSON/TMDL/estructura/referencias/codificación): Aprobada / Fallida / No validada
- Integridad funcional (visuales/KPIs/filtros/navegación/bookmarks/refresh/RLS aplicable): Aprobada / Fallida / No validada
- Power BI Desktop abierto: Sí / No
- Refresh ejecutado: Sí / No / No aplica
- Pruebas no realizadas y motivo:

## 9. Beneficio e impacto observado
- Beneficio esperado:
- Beneficio observado y cómo se midió:
- Impacto funcional:
- Impacto técnico:
- Riesgos residuales:
- Limitaciones de medición:

## 10. Alertas y cierre
- Alertas por severidad (Bloqueante/Advertencia/Información):
- Pendientes y responsable por correo si aplica:
- Documentación actualizada:
- Estado final: Listo para entrega / Parcial / Bloqueado / Revertido
- Criterios de cierre cumplidos:
- Relación con README histórico y Registro de Cambio:
