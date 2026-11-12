# AI-DLC — CREACIÓN

## Propósito
Construir un BI nuevo con requerimientos, reglas de negocio, fuentes, modelo semántico, KPIs, visualizaciones, seguridad, operación, validaciones y documentación trazables.

## Uso autónomo
Este DLC se usa solo para crear un BI nuevo. Si el trabajo parte de un BI existente, detenerse y clasificarlo como Modificación o Depuración/Mejora según el objetivo. No usar este proceso para evadir el CENSO requerido en trabajos sobre BI existentes.

## Orden de lectura obligatorio
Las reglas comunes están en `../00_Base_Compartida/` (una sola base para Creación, Modificación y Depuración).

1. `../00_Base_Compartida/06_principios_y_controles.md`
2. `../00_Base_Compartida/01_rutas_y_censo.md`
3. `01_Reglas_del_Proceso/03_creacion.md`
4. `02_Plantillas/01_levantamiento_creacion.md`
5. `../00_Base_Compartida/16_diccionario_datos_y_simulacion.md` (requiere el diccionario de `MCP_POWERBI\00_dlc\00_diccionario_datos`)
6. `../00_Base_Compartida/02_diseno_corporativo.md`
7. `../00_Base_Compartida/03_integridad_validacion.md`
8. `../00_Base_Compartida/04_archivos_y_encoding.md`
9. `../00_Base_Compartida/05_control_trazabilidad_tableros.md`
10. Plantillas `../00_Base_Compartida/10_plantilla_readme_tablero.md`, `11_plantilla_registro_central.md` y `12_plantilla_registro_cambio.md`.
11. `../00_Base_Compartida/15_rendimiento_y_DAX.md` cuando aplique.
12. `03_Flujo_y_Checklists/flujo_operativo.md`, `checklist_general.md` y `checklist_integral.md`.

## Inicio obligatorio
1. Confirmar que se trata de un BI nuevo.
2. Confirmar nombre exacto y solicitar únicamente los dos correos de trazabilidad: quien trabaja/modifica y quien solicita/es dueño.
3. Crear la carpeta del tablero y su README en `MCP_POWERBI\02_censo\[Nombre exacto BI]\README.md` (el censo se agregará al liberar).
4. Actualizar `MCP_POWERBI\02_censo\REGISTRO_CONTROL_TABLEROS.md`.
5. Crear y utilizar la copia de trabajo en `MCP_POWERBI\01_bi\01_versiones\01_kiro\[Nombre exacto BI]\`.
6. Validar el diccionario de datos, ubicar la fuente pedida y construir en modo simulación; verificar la conexión real antes de liberar.
7. Completar levantamiento, decisiones, diseño, construcción y validaciones.
8. Tras aprobación, guardar la versión base en `MCP_POWERBI\01_bi\01_versiones\00_original\[Nombre exacto BI]\` y censarla (tipo `Inicial`); al registrarse, el censo lleva sus fuentes al diccionario.
9. Actualizar documentación (incluidas las diferencias encontradas contra el diccionario) y cerrar solo con evidencia.

## Reglas de bloqueo
- No construir como creación si la solicitud realmente es modificación/depuración de un BI existente.
- No desarrollar en `01_versiones` (ni en `00_original`); el trabajo ocurre en `01_kiro`.
- No ejecutar decisiones de negocio propuestas por IA sin aprobación explícita.
- No declarar listo si existen bloqueantes críticos o validaciones requeridas sin ejecutar.
- No guardar secretos/credenciales en documentos o código.
- No definir una conexión fuera del diccionario de datos vigente (salvo fuente nueva declarada); no liberar sin verificar la conexión real.
- No crear tablas ni vistas en la base de datos.

## Estructura
- `../00_Base_Compartida/`: reglas transversales comunes a los tres procesos.
- `01_Reglas_del_Proceso/`: reglas específicas de creación.
- `02_Plantillas/`: levantamiento inicial.
- `03_Flujo_y_Checklists/`: secuencia, checklist general y checklist integral.
- `04_Control_de_Versiones/`: historial de auditoría y evolución.

## Alcance de diseño
El estándar visual corporativo (V10) aplica a Creación: solo logo Nebula, segmentaciones oscuras y botones con radio 6 px. Deben mantenerse la ruta oficial del logo, jerarquía de filtros, header, colores, tipografía, botones, cards, tablas, navegación y consistencia entre páginas según el documento de diseño vigente.
