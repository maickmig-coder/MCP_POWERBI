# AI-DLC — MODIFICACIÓN

## Propósito
Aplicar cambios solicitados sobre un BI existente, partiendo de un CENSO que describe el tablero final, con una copia de trabajo Kiro, ejecución limitada al alcance aprobado y cierre con una versión nueva censada.

## Uso autónomo
Este DLC no requiere ejecutar el de Creación ni el de Depuración. Si la solicitud incluye un objetivo distinto de la modificación, registrar la necesidad y acordar un proceso separado antes de ejecutar ese alcance adicional.

## Archivos de referencia y orden de lectura
Las reglas comunes están en `../00_Base_Compartida/` (una sola base para Creación, Modificación y Depuración).

1. `../00_Base_Compartida/06_principios_y_controles.md`
2. `../00_Base_Compartida/01_rutas_y_censo.md` (puerta del censo y versiones)
3. `01_Reglas_del_Proceso/04_modificacion.md`
4. `02_Plantillas/02_solicitud_modificacion.md`
5. `../00_Base_Compartida/16_diccionario_datos_y_simulacion.md` si el cambio agrega fuentes, tablas o columnas de origen.
6. `../00_Base_Compartida/02_diseno_corporativo.md` (V10) cuando se afecte diseño o se deba validar que se conserva.
7. `../00_Base_Compartida/03_integridad_validacion.md`
8. `../00_Base_Compartida/04_archivos_y_encoding.md` cuando se creen/modifiquen archivos de texto.
9. `../00_Base_Compartida/05_control_trazabilidad_tableros.md`, `10_plantilla_readme_tablero.md`, `11_plantilla_registro_central.md` y `12_plantilla_registro_cambio.md`.
10. `../00_Base_Compartida/15_rendimiento_y_DAX.md` solo en la medida en que el cambio pueda afectar DAX, modelo o rendimiento; una optimización general se deriva a Depuración.
11. `03_Flujo_y_Checklists/flujo_operativo.md`, `checklist_general.md` y `checklist_integral.md`.

## Inicio obligatorio
1. Confirmar el nombre exacto del BI.
2. Registrar únicamente el correo de quien trabaja/modifica y el correo de quien solicita/es dueño.
3. Abrir el README del tablero en `MCP_POWERBI\02_censo\[Nombre exacto BI]\README.md` (crearlo si no existe) y actualizar `MCP_POWERBI\02_censo\REGISTRO_CONTROL_TABLEROS.md`.
4. **Puerta del censo:** `censo.py vigencia` debe responder **VIGENTE** (el censo describe la última versión guardada y su huella coincide) y **APTO** (validado por el dueño). Si no, bloquear según `01_rutas_y_censo.md`.
5. Preparar la copia de trabajo en `MCP_POWERBI\01_bi\01_versiones\01_kiro\[Nombre exacto BI]\` desde la última versión guardada.
6. Analizar alcance, dependencias y riesgo; presentar propuesta y registrar la decisión del analista.
7. Ejecutar únicamente cambios aprobados sobre Kiro. Fuentes nuevas solo desde el diccionario de datos.
8. Validar, documentar y guardar el resultado como versión nueva `01_versiones\NN_modificacion_<ID>\[Nombre exacto BI]\`.
9. Censar esa versión (tipo `Actualización`, `--origen "DLC de modificación <ID>"`) y cerrar con estado sustentado.

## Bloqueos
- Sin censo, censo desactualizado o censo sin validar: `BLOQUEADO — CENSO REQUERIDO / DESACTUALIZADO / SIN VALIDAR`.
- Sin copia de trabajo separada: no ejecutar cambios.
- Con aprobación obligatoria pendiente: no ejecutar la parte afectada.
- Con bloqueantes de validación abiertos o sin censo de la versión entregada: no declarar `Listo para entrega`.

## Estructura
- `../00_Base_Compartida/`: reglas transversales comunes a los tres procesos.
- `01_Reglas_del_Proceso/`: reglas específicas de Modificación.
- `02_Plantillas/`: formato de solicitud de modificación.
- `03_Flujo_y_Checklists/`: secuencia, checklist general y checklist integral.
- `04_Control_de_Versiones/`: registro de cambios de la segmentación.

## Principio de alcance
La validación integral de integridad es obligatoria. La depuración general, la eliminación de columnas/campos y la optimización amplia no se ejecutan automáticamente por estar modificando el BI; se registran como propuestas para un proceso separado, salvo que formen parte explícita del alcance aprobado. En diseño se conserva lo existente; el estándar V10 se aplica a lo que el cambio crea o rediseña con aprobación.
