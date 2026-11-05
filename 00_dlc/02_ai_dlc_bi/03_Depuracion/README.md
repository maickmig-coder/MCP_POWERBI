# AI-DLC — Depuración y Mejora

## Propósito
Diagnosticar y corregir problemas de integridad, dependencias, fuentes, consultas, modelo, DAX, procesos y rendimiento en un BI existente. No es un proceso de rediseño estético.

## Regla de independencia
Este DLC se ejecuta como proceso separado. Si la solicitud mezcla creación, modificación funcional/visual y depuración, registrar los procesos por separado y definir dependencias, orden y aprobaciones. No absorber cambios estéticos dentro de Depuración.

## Inicio obligatorio
1. Confirmar nombre exacto del BI y objetivo medible.
2. Registrar únicamente el correo de quien trabaja/modifica y el correo de quien solicita/es dueño.
3. Abrir el README histórico existente y actualizar el registro central; no crear historial paralelo.
4. Buscar y validar el CENSO en `MCP_POWERBI\02_censo`. Si falta, no corresponde o no es utilizable, bloquear como `BLOQUEADO — CENSO REQUERIDO`.
5. Preservar el original PBIP en `MCP_POWERBI\01_bi\01_versiones\00_original\[Nombre exacto BI]`.
6. Preparar la copia de trabajo en `MCP_POWERBI\01_bi\01_versiones\01_kiro\[Nombre exacto BI]`. El agente nunca trabaja sobre el original.
7. Capturar línea base, dependencias, riesgos, pruebas y rollback.
8. Detectar y documentar; proponer; obtener decisión del analista; ejecutar solo acciones aprobadas.
9. Comparar antes/después, actualizar trazabilidad y comunicar beneficios medidos, alertas y pendientes.

## Control adicional V9.5 — preservación de visuales

La V9.5 incorpora un protocolo obligatorio para evitar eliminaciones accidentales de visuales u objetos durante la depuración. Incluye inventario por ID, análisis semántico de referencias, lista positiva de acciones aprobadas, revisión separada de bookmarks/botones/estados, conciliación antes/después y bloqueo por desapariciones no autorizadas. La codificación y la integridad técnica se validan por separado de la integridad funcional.

La incidencia de `GC - Flotillas` se registra como lección preventiva dentro de este DLC. **No se modifica el DLC de CENSO ni su ritual**; esta versión solo actualiza `03_Depuracion` y conserva la consulta del CENSO como condición operativa ya existente.

## Estructura
- `00_Base_Compartida/`: controles transversales necesarios para operar este DLC.
- `01_Reglas_del_Proceso/`: reglas específicas de Depuración y Mejora.
- `02_Plantillas/`: plantilla de diagnóstico, decisiones y validación.
- `03_Flujo_y_Checklists/`: secuencia operativa y controles específicos.
- `04_Control_de_Versiones/`: auditoría de cambios del DLC.

## Bloqueos y límites
- CENSO válido obligatorio para depurar un BI existente.
- Original protegido en `00_original`; trabajo exclusivamente en `01_kiro`.
- No eliminar ni modificar automáticamente elementos por parecer no usados.
- No ejecutar propuestas rechazadas o pendientes.
- No declarar beneficio sin medición/evidencia.
- No declarar `Listo para entrega` con bloqueantes o pruebas críticas fallidas.

## Lección técnica conservada
Un caso del proyecto redujo una carga aproximada de 20 millones de filas a 1,3 millones mediante optimización SQL y eliminación de columnas no utilizadas. Es un ejemplo histórico, no una promesa de resultado para otros tableros. La regla general es evaluar la optimización en origen antes de cargar, validando que no cambien los resultados funcionales.
