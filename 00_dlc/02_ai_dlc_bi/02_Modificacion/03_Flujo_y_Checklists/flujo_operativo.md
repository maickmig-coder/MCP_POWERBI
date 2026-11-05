# Flujo operativo — MODIFICACIÓN

1. Recibir solicitud de modificación.
2. Confirmar nombre exacto del BI existente.
3. Registrar correo de quien trabaja/modifica y correo de quien solicita/es dueño.
4. Abrir el README histórico y actualizar el registro central.
5. Identificar y conservar el PBIP original en `MCP_POWERBI\01_bi\01_versiones\00_original\[Nombre exacto BI]`. No sobrescribirlo.
6. Buscar el CENSO correspondiente en `MCP_POWERBI\02_censo`.
7. ¿Existe y corresponde al BI exacto?
   - **No:** estado `BLOQUEADO — CENSO REQUERIDO`; ejecutar `MCP_POWERBI\00_dlc\01_ai-dlc-censo`, guardar el resultado en `MCP_POWERBI\02_censo` y verificarlo. No avanzar con la modificación hasta completar esta validación.
   - **Sí:** cargarlo como contexto del estado actual.
8. Preparar la copia de trabajo en `MCP_POWERBI\01_bi\01_versiones\01_kiro\[Nombre exacto BI]`.
9. Analizar solicitud, alcance y criterios de aceptación.
10. Identificar dependencias: fuentes/consultas, tablas, columnas, relaciones, medidas/DAX, filtros, visuales, marcadores, botones, navegación y estados alternativos, cuando apliquen.
11. Evaluar riesgo y documentar el estado anterior.
12. Presentar propuesta, alcance incluido/no incluido y efectos esperados.
13. Registrar la decisión del analista.
14. Ejecutar únicamente lo aprobado, trabajando sobre la copia Kiro.
15. Validar el cambio y ejecutar pruebas antes/después.
16. Revisar integridad completa, incluyendo visuales ocultos, marcadores, botones y elementos heredados.
17. Registrar alertas, pendientes, evidencia y resultados.
18. Actualizar README histórico, Registro de Cambio y registro central.
19. Confirmar estado `Listo para entrega` solo si las validaciones requeridas se completaron; de lo contrario, dejar el estado y pendientes explícitos.

## Regla de copia de trabajo Kiro
La copia de `01_kiro` es el único destino de trabajo del agente. El original de `00_original` queda protegido. Documentar ambas rutas en el README y en el Registro de Cambio cuando corresponda.
