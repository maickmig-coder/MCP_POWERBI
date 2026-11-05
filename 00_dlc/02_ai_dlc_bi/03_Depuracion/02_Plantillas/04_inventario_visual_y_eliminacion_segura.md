# Plantilla — Inventario de visuales y control de eliminación

Usar esta matriz durante Depuración cuando se analicen visuales, páginas, bookmarks o botones. No sustituye el inventario completo del proyecto; registra la evidencia necesaria para decisiones destructivas.

| ID hallazgo | Página | ID página | Título visible | Tipo | ID visual/objeto | Ruta del archivo | Visible/oculto | Referencia sospechosa y contexto | Campos/medidas activos | Dependencias revisadas | Clasificación | Evidencia | Acción propuesta | Riesgo | Decisión | Aprobación exacta | Resultado después |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H-VIS-001 | | | | | | | | | | | Candidato / Roto confirmado / Válido / Desconocido | | Conservar / Reparar / Eliminar / Pendiente | | Pendiente | | |

## Reglas de uso

1. El ID técnico y la ruta deben identificar inequívocamente el objeto; no usar solo el título visible.
2. Una coincidencia textual se registra como `Candidato` hasta demostrar su efecto real.
3. La columna `Aprobación exacta` debe referirse al objeto concreto y a la acción autorizada.
4. No ejecutar filas `Pendiente`, `Rechazado`, vacías o ambiguas.
5. Crear una matriz posterior y comparar IDs antes/después.
6. Registrar por separado bookmarks, botones y estados alternativos con sus dependencias.
7. Si un objeto desaparece sin aprobación, marcar bloqueante, detener y revertir/restaurar.

## Conciliación por página

| Página | ID página | Visuales antes | Conservados | Reparados/modificados | Eliminados aprobados | Nuevos | Desapariciones no autorizadas | Diferencia explicada | Estado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| | | | | | | | | | Pendiente |
