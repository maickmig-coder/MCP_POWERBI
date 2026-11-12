# CHECKLIST INTEGRAL DE INTEGRIDAD — MODIFICACIÓN

Este checklist complementa `03_Flujo_y_Checklists/checklist_general.md`. No sustituye los controles de inicio, aprobación, alcance, trazabilidad ni cierre. Marcar cada punto como **Cumple / No cumple / No aplica** y conservar evidencia de los hallazgos relevantes.

## 1. Estructura del archivo y modelo
- [ ] El proyecto PBIP de trabajo abre o puede analizarse con las herramientas disponibles.
- [ ] Se verificó que la copia analizada corresponde a la ruta Kiro del BI exacto.
- [ ] Referencias a tablas, columnas, medidas y entidades usadas por el cambio siguen siendo válidas.
- [ ] Relaciones afectadas siguen siendo válidas y coherentes.
- [ ] No se introdujeron referencias rotas ni objetos duplicados de manera involuntaria.
- [ ] Los cambios de modelo conservan la granularidad y el significado funcional esperado.

## 2. Visuales y páginas
- [ ] Los visuales afectados cargan sin errores.
- [ ] Títulos y campos de los visuales afectados corresponden a su contenido.
- [ ] No hay campos, medidas o entidades inexistentes en los elementos afectados.
- [ ] Páginas afectadas conservan navegación y distribución no incluida en el alcance.
- [ ] Elementos heredados relevantes se revisaron cuando el cambio los pueda afectar.

## 3. Marcadores, botones y estados
- [ ] Se revisaron marcadores que interactúan con páginas o visuales afectados.
- [ ] Se revisaron botones y acciones relacionados.
- [ ] Se validó visibilidad de elementos en estados alternativos.
- [ ] Se revisaron visuales ocultos relacionados con el cambio.
- [ ] Si se encontraron visuales ocultos con campos/medidas inexistentes, se generó alerta con ubicación e instrucciones de revisión.
- [ ] No se eliminaron elementos ocultos ni se modificaron estados fuera del alcance sin aprobación.

## 4. Filtros e interacciones
- [ ] Los filtros afectados funcionan y mantienen el comportamiento esperado.
- [ ] Se probaron interacciones relevantes entre visuales.
- [ ] Los cambios no alteraron filtros, segmentaciones o navegación no solicitados.
- [ ] Los marcadores/restablecimientos no introducen un estado incoherente.

## 5. Resultados y pruebas
- [ ] Se validó el criterio de aceptación de la solicitud.
- [ ] Se compararon KPIs, totales, conteos o resultados antes/después cuando el cambio pueda afectarlos.
- [ ] Se investigaron diferencias no esperadas.
- [ ] Las pruebas cubren los casos de uso impactados.
- [ ] Los límites de la validación se declaran si no fue posible probar en Power BI Desktop/Service o contra datos reales.

## 6. Diseño y consistencia
- [ ] Se conservó el diseño existente salvo autorización, regla corporativa o necesidad técnica justificada.
- [ ] Los componentes repetidos mantienen consistencia entre páginas.
- [ ] Si el cambio solicitado es visual, se validó el estándar corporativo aplicable.
- [ ] No se aplicaron rediseños adicionales fuera del alcance.

## 7. Archivos técnicos y codificación
- [ ] Los archivos creados/modificados conservan estructura y sintaxis válidas.
- [ ] Se validaron referencias internas de archivos cuando aplique.
- [ ] Se comprobó UTF-8 y ausencia de BOM cuando el formato lo requiera.
- [ ] No se declararon pruebas automáticas exitosas si no fueron ejecutadas.

## 8. Alertas y cierre técnico
- [ ] Cada hallazgo tiene descripción, ubicación, impacto, severidad y acción sugerida.
- [ ] Los hallazgos se clasificaron como Bloqueante, Advertencia o Información.
- [ ] Los bloqueantes están resueltos o la entrega queda bloqueada.
- [ ] Alertas y pendientes están reflejados en el Registro de Cambio/README.
- [ ] El resultado de esta revisión está documentado.

## Límites
Este checklist valida integridad relacionada con la modificación. No autoriza una depuración general, eliminación de columnas sin uso ni refactorización amplia de consultas/DAX. Si aparecen esas oportunidades, registrarlas como propuestas separadas para Depuración y Mejora, salvo que formen parte explícita del alcance aprobado.
