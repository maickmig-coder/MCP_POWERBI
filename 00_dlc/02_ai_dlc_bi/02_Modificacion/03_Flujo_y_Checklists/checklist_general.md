# CHECKLIST DE MODIFICACIÓN DE BI EXISTENTE

Marcar cada punto como **Cumple / No cumple / No aplica**, con evidencia cuando corresponda. Un punto obligatorio no cumplido impide declarar el trabajo listo para entrega.

## A. Inicio y trazabilidad
- [ ] Nombre exacto del BI confirmado.
- [ ] Solicitud y resultado esperado documentados.
- [ ] Correo de quien trabaja/modifica registrado.
- [ ] Correo de quien solicita/es dueño registrado.
- [ ] README histórico localizado o creado en la carpeta del BI.
- [ ] Registro central actualizado.
- [ ] Fecha de inicio y versión/referencia registradas.
- [ ] Alcance incluido y excluido definido.
- [ ] Criterios de aceptación acordados.
- [ ] Riesgo inicial clasificado (bajo/medio/alto) y justificado.

## B. CENSO y control del original — BLOQUEANTES
- [ ] CENSO localizado en `MCP_POWERBI\02_censo`.
- [ ] CENSO corresponde al nombre exacto del BI y está disponible/legible.
- [ ] Si falta/no corresponde/no se puede validar, estado `BLOQUEADO — CENSO REQUERIDO` registrado y no se ejecutan cambios.
- [ ] PBIP original preservado en `MCP_POWERBI\01_bi\01_versiones\00_original\[Nombre exacto BI]\`.
- [ ] El original no fue utilizado como destino de edición.
- [ ] Solo después de validar el CENSO, copia de trabajo preparada en `MCP_POWERBI\01_bi\01_versiones\01_kiro\[Nombre exacto BI]\`.
- [ ] Rutas de original y copia Kiro registradas en el README y en el Registro de Cambio cuando corresponda.

## C. Análisis de impacto de la solicitud
- [ ] Estado anterior documentado y evidencia disponible cuando sea posible.
- [ ] Visuales/páginas afectados identificados.
- [ ] Campos, columnas, medidas y tablas afectadas identificados.
- [ ] Relaciones, granularidad y filtros relacionados evaluados cuando aplique.
- [ ] Fuentes y consultas evaluadas cuando la solicitud las afecte.
- [ ] Marcadores, botones, navegación y estados alternativos evaluados cuando aplique.
- [ ] Dependencias e impactos indirectos registrados.
- [ ] Diferenciados requisito del solicitante, necesidad técnica y propuesta de IA.
- [ ] Propuesta con alcance, exclusiones, riesgo y beneficio esperado presentada.
- [ ] Decisión del analista registrada antes de ejecutar todo cambio que requiera aprobación.

## D. Ejecución controlada
- [ ] Se trabaja exclusivamente sobre la copia Kiro.
- [ ] Solo se ejecutaron cambios aprobados y dentro del alcance.
- [ ] Cambios técnicos adicionales justificados y aprobados cuando correspondía.
- [ ] Estética existente conservada salvo solicitud explícita, regla corporativa o necesidad técnica justificada.
- [ ] No se eliminaron campos, medidas, visuales ni elementos automáticamente por considerarlos innecesarios.
- [ ] Diferencias frente a la propuesta documentadas.

## E. Validación del cambio
- [ ] Criterios de aceptación revisados.
- [ ] Visuales afectados revisados.
- [ ] Filtros e interacciones relacionados probados.
- [ ] Medidas/DAX afectadas validadas.
- [ ] Relaciones/modelo validados cuando aplique.
- [ ] Resultados antes/después comparados cuando el cambio pueda alterar datos o comportamiento.
- [ ] Diferencias inesperadas investigadas y explicadas.
- [ ] Marcadores, botones, estados alternativos y visuales ocultos revisados cuando aplique.
- [ ] Referencias a campos, medidas o entidades inexistentes revisadas.
- [ ] Consistencia de diseño revisada para evitar cambios colaterales.
- [ ] Rendimiento validado cuando el cambio pueda afectarlo.
- [ ] Codificación y BOM validados en archivos de texto creados/modificados cuando aplique.

## F. Documentación y cierre
- [ ] Registro de Cambio completado para el cambio relevante.
- [ ] Estado anterior, propuesta, decisión, ejecución y estado posterior documentados.
- [ ] Validaciones, evidencia, beneficio/impacto y riesgo registrados.
- [ ] Alertas clasificadas como bloqueante/advertencia/información y comunicadas.
- [ ] Pendientes asignados o declarados explícitamente.
- [ ] README histórico actualizado sin borrar intervenciones anteriores.
- [ ] Registro central actualizado con estado y correos actuales.
- [ ] No existen bloqueantes abiertos para la entrega.
- [ ] Estado `Listo para entrega` declarado solo cuando se completaron los controles aplicables.

## Exclusión de alcance
Este checklist no autoriza una depuración general del BI. Si se detectan oportunidades de optimización no necesarias para la modificación solicitada, documentarlas como hallazgo/propuesta y pedir al analista si desea abrir un trabajo separado de Depuración y Mejora.
