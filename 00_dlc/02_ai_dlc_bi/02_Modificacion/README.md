# AI-DLC — MODIFICACIÓN

## Propósito
Aplicar cambios solicitados sobre un BI existente, con el CENSO como condición de entrada, el original protegido, una copia de trabajo Kiro y ejecución limitada al alcance aprobado.

## Uso autónomo
Este DLC contiene las reglas transversales y las reglas específicas necesarias para modificar un BI. No requiere ejecutar el DLC de Creación ni el de Depuración. Si la solicitud incluye un objetivo distinto de la modificación, registrar la necesidad y acordar un proceso separado antes de ejecutar ese alcance adicional.

## Archivos de referencia y orden de lectura
1. `00_Base_Compartida/06_principios_y_controles.md`
2. `00_Base_Compartida/01_rutas_y_censo.md`
3. `01_Reglas_del_Proceso/04_modificacion.md`
4. `02_Plantillas/02_solicitud_modificacion.md`
5. `00_Base_Compartida/02_diseno_corporativo.md` cuando se afecte diseño o se deba validar que se conserva.
6. `00_Base_Compartida/03_integridad_validacion.md`
7. `00_Base_Compartida/04_archivos_y_encoding.md` cuando se creen/modifiquen archivos de texto.
8. `00_Base_Compartida/05_control_trazabilidad_tableros.md`, `10_plantilla_readme_tablero.md`, `11_plantilla_registro_central.md` y `12_plantilla_registro_cambio.md`.
9. `00_Base_Compartida/15_rendimiento_y_DAX.md` solo en la medida en que el cambio pueda afectar DAX, modelo o rendimiento; una optimización general se deriva a Depuración.
10. `03_Flujo_y_Checklists/flujo_operativo.md` y luego `checklist_general.md`.

## Inicio obligatorio
1. Confirmar el nombre exacto del BI.
2. Registrar únicamente el correo de quien trabaja/modifica y el correo de quien solicita/es dueño.
3. Localizar/crear el README histórico y actualizar el registro central.
4. Preservar el PBIP original en `MCP_POWERBI\01_bi\01_versiones\00_original\[Nombre exacto BI]\` sin sobrescribir originales existentes.
5. Buscar y validar el CENSO en `MCP_POWERBI\02_censo`.
6. Si el CENSO falta, no corresponde al BI o no puede validarse, registrar `BLOQUEADO — CENSO REQUERIDO`, ejecutar el ritual `MCP_POWERBI\00_dlc\01_ai-dlc-censo`, guardar el resultado en `MCP_POWERBI\02_censo` y volver a validarlo.
7. Solo después de validar el CENSO, preparar y usar la copia de trabajo en `MCP_POWERBI\01_bi\01_versiones\01_kiro\[Nombre exacto BI]\`.
8. Analizar alcance, dependencias y riesgo; presentar propuesta y registrar la decisión del analista.
9. Ejecutar únicamente cambios aprobados sobre Kiro.
10. Validar, documentar, actualizar historial y cerrar con estado sustentado.

## Bloqueos
- Sin CENSO válido: `BLOQUEADO — CENSO REQUERIDO`.
- Sin original PBIP preservado o sin copia de trabajo separada: no ejecutar cambios.
- Con aprobación obligatoria pendiente: no ejecutar la parte afectada.
- Con bloqueantes de validación abiertos: no declarar `Listo para entrega`.

## Estructura
- `00_Base_Compartida/`: reglas transversales requeridas por este proceso.
- `01_Reglas_del_Proceso/`: reglas específicas de Modificación.
- `02_Plantillas/`: formato de solicitud de modificación.
- `03_Flujo_y_Checklists/`: secuencia y controles de salida.
- `04_Control_de_Versiones/`: registro de cambios de la segmentación.

## Principio de alcance
La validación integral de integridad es obligatoria. La depuración general, la eliminación de columnas/campos y la optimización amplia no se ejecutan automáticamente por estar modificando el BI; se registran como propuestas para un proceso separado, salvo que formen parte explícita del alcance aprobado.
