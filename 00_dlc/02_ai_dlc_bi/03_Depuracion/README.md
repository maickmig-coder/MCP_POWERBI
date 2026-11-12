# AI-DLC — Depuración y Mejora

## Propósito
Diagnosticar y corregir problemas de integridad, dependencias, consultas, modelo, DAX, procesos y rendimiento en un BI existente. No es un proceso de rediseño estético y **no agrega** fuentes, tablas, columnas de origen, páginas ni visuales: solo depura.

## Regla de independencia
Este DLC se ejecuta como proceso separado. Si la solicitud mezcla creación, modificación funcional/visual y depuración, registrar los procesos por separado y definir dependencias, orden y aprobaciones. No absorber cambios estéticos ni agregados dentro de Depuración.

## Orden de lectura
Las reglas comunes están en `../00_Base_Compartida/` (una sola base para Creación, Modificación y Depuración).

1. `../00_Base_Compartida/06_principios_y_controles.md`
2. `../00_Base_Compartida/01_rutas_y_censo.md` (puerta del censo y versiones)
3. `01_Reglas_del_Proceso/05_depuracion_mejora.md`, `controles_reforzados_depuracion.md` y `16_protocolo_integridad_visuales_eliminacion_segura.md`
4. `02_Plantillas/03_depuracion_mejora.md` y `04_inventario_visual_y_eliminacion_segura.md`
5. `../00_Base_Compartida/03_integridad_validacion.md`, `04_archivos_y_encoding.md`, `05_control_trazabilidad_tableros.md` y `15_rendimiento_y_DAX.md`
6. `03_Flujo_y_Checklists/flujo_operativo.md`, `checklist_general.md` y `checklist_integral.md`

## Inicio obligatorio
1. Confirmar nombre exacto del BI y objetivo medible.
2. Registrar únicamente el correo de quien trabaja/modifica y el correo de quien solicita/es dueño.
3. Abrir el README del tablero en `MCP_POWERBI\02_censo\[Nombre exacto BI]\README.md` y actualizar `MCP_POWERBI\02_censo\REGISTRO_CONTROL_TABLEROS.md`; no crear historial paralelo.
4. **Puerta del censo:** `censo.py vigencia` debe responder **VIGENTE** y **APTO**. Si no, bloquear según `01_rutas_y_censo.md`.
5. Preparar la copia de trabajo en `MCP_POWERBI\01_bi\01_versiones\01_kiro\[Nombre exacto BI]` desde la última versión guardada. El agente nunca trabaja dentro de `01_versiones`.
6. Capturar línea base, dependencias, riesgos, pruebas y rollback.
7. Detectar y documentar; proponer; obtener decisión del analista; ejecutar solo acciones aprobadas.
8. Comparar antes/después, guardar la versión nueva `01_versiones\NN_depuracion_<ID>\[Nombre exacto BI]\` y censarla (tipo `Actualización`, `--origen "DLC de depuración <ID>"`).
9. Actualizar trazabilidad y comunicar beneficios medidos, alertas y pendientes.

## Control adicional V9.5 — preservación de visuales

La V9.5 incorpora un protocolo obligatorio para evitar eliminaciones accidentales de visuales u objetos durante la depuración. Incluye inventario por ID, análisis semántico de referencias, lista positiva de acciones aprobadas, revisión separada de bookmarks/botones/estados, conciliación antes/después y bloqueo por desapariciones no autorizadas. La codificación y la integridad técnica se validan por separado de la integridad funcional.

## Estructura
- `../00_Base_Compartida/`: reglas transversales comunes a los tres procesos.
- `01_Reglas_del_Proceso/`: reglas de Depuración, controles reforzados y protocolo de eliminación segura.
- `02_Plantillas/`: plantilla de diagnóstico, decisiones, validación e inventario visual.
- `03_Flujo_y_Checklists/`: secuencia, checklist general y checklist integral.
- `04_Control_de_Versiones/`: auditoría de cambios del DLC.

## Bloqueos y límites
- Censo vigente y validado obligatorio (`vigencia` = VIGENTE y APTO).
- Trabajo exclusivamente en `01_kiro`; las versiones guardadas no se editan.
- No eliminar ni modificar automáticamente elementos por parecer no usados.
- No agregar fuentes, tablas, columnas de origen, páginas ni visuales (eso es Modificación).
- No ejecutar propuestas rechazadas o pendientes.
- No declarar beneficio sin medición/evidencia.
- No declarar `Listo para entrega` con bloqueantes, pruebas críticas fallidas o sin censo de la versión entregada.

## Lección técnica conservada
Un caso del proyecto redujo una carga aproximada de 20 millones de filas a 1,3 millones mediante optimización SQL y eliminación de columnas no utilizadas. Es un ejemplo histórico, no una promesa de resultado para otros tableros. La regla general es evaluar la optimización en origen antes de cargar, validando que no cambien los resultados funcionales.
