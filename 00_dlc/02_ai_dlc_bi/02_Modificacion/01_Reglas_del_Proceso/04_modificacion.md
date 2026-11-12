# 6. REGLAS DE MODIFICACIÓN

1. Solicitar nombre exacto y los dos correos.
2. Verificar la puerta del censo (`vigencia` = VIGENTE y APTO).
3. Preparar la copia de trabajo desde la última versión guardada.
4. Analizar solicitud y alcance.
5. Identificar dependencias (y, si hay fuentes nuevas, el diccionario de datos).
6. Clasificar riesgo.
7. Registrar propuesta/decisión.
8. Modificar en `01_kiro`.
9. Validar.
10. Revisar integridad completa.
11. Guardar la versión nueva y censarla.

## Estética

Por defecto conservar:
- colores;
- tipografías;
- tamaños;
- posiciones;
- distribución;
- Header;
- filtros;
- tarjetas;
- gráficos;
- navegación.

Solo cambiar por:
- solicitud explícita;
- regla corporativa;
- necesidad técnica justificada.

## Alcance

No ampliar silenciosamente el alcance.

Si una dependencia requiere cambio adicional:
- explicarlo;
- justificarlo;
- clasificar riesgo;
- solicitar aprobación cuando no sea estrictamente necesario.

## Marcadores y estados

Si existen:
- identificar marcador;
- visuales controlados;
- estado;
- visibilidad;
- relación con botones;
- campos/medidas usados;
- errores.


## Registro de la modificación

Antes de modificar:

- abrir el README existente del tablero;
- registrar correo de quien trabaja/modifica y correo de quien solicita/es dueño;
- registrar fecha de inicio;
- agregar una nueva entrada al histórico;
- identificar la versión/referencia sobre la que se trabajará.

Al finalizar, registrar cambios, decisiones, validaciones, pendientes y cierre.

Si el tablero ya tiene un histórico por creaciones o modificaciones anteriores,
se debe continuar el mismo README.


## Control de identificación y trazabilidad por correo

Antes de iniciar cualquier modificación, registrar únicamente:

- **Correo de quien trabaja/modifica el tablero.**
- **Correo de quien solicita/es dueño del requerimiento.**

Esta identificación es obligatoria y debe quedar registrada en el README del
tablero y en el registro central cuando corresponda.

No se requieren nombres, cargos, teléfonos ni otros datos personales para este
control.

### Continuidad histórica

Si el mismo tablero vuelve a modificarse posteriormente, no se crea un nuevo
README. Se actualiza el correo de quien trabaja/modifica y se agrega una nueva
intervención al histórico, conservando las intervenciones anteriores.

### Secuencia obligatoria de modificación

```text
Solicitud
↓
Nombre exacto del BI
↓
Registrar correo de quien trabaja/modifica
↓
Registrar correo de quien solicita/es dueño
↓
censo.py vigencia
↓
¿VIGENTE y APTO?
├── No → Bloquear (censo requerido, desactualizado o sin validar)
└── Sí → Registrar census_id de partida
↓
Copia de trabajo desde la última versión guardada
↓
Analizar alcance y dependencias
↓
Evaluar riesgo
↓
Proponer/confirmar cambios
↓
Registrar decisión del analista
↓
Ejecutar modificación aprobada
↓
Validación del cambio
↓
Revisión integral de integridad
↓
Actualizar README e histórico
↓
Actualizar registro central
↓
Guardar versión nueva NN_modificacion_<ID> y censarla (Actualización)
↓
Listo para entrega
```


## Registro individual de cada cambio

Además del README histórico, cada modificación relevante debe documentarse
mediante `../../00_Base_Compartida/12_plantilla_registro_cambio.md`.

El registro debe permitir responder:

1. ¿Qué se solicitó?
2. ¿Cómo estaba antes?
3. ¿Qué se propuso?
4. ¿Qué dependencias estaban involucradas?
5. ¿Qué decidió el analista?
6. ¿Qué se modificó realmente?
7. ¿Cómo quedó después?
8. ¿Qué se validó antes/después?
9. ¿Cuál fue el beneficio o impacto?
10. ¿Qué alertas o pendientes quedaron?

El registro individual no reemplaza el README; ambos se complementan.


## Puerta del censo: solo un censo del tablero final (R53, R56)

Aplicar `../../00_Base_Compartida/01_rutas_y_censo.md`, sección «Entrada del censo según el proceso»:

1. Solicitar el **nombre exacto del BI** y los dos correos.
2. Ejecutar `censo.py vigencia` sobre `MCP_POWERBI\02_censo\[BI]\[BI] - censo.md`.
3. Según el resultado:
   - sin censo → `BLOQUEADO — CENSO REQUERIDO` (censo `Inicial` con el DLC del censo);
   - `DESACTUALIZADO` → `BLOQUEADO — CENSO DESACTUALIZADO` (el censo no describe el tablero final: censar la última
     versión guardada, tipo `Actualización`);
   - `VIGENTE` pero `NO APTO` → `BLOQUEADO — CENSO SIN VALIDAR` (validación con el dueño);
   - `VIGENTE` y `APTO` → continuar y registrar el `census_id` de partida en el README.
4. Preparar la copia de trabajo en `01_kiro\[BI]\` **desde la última versión guardada** que indica `vigencia`.

El AI-DLC no puede saltarse esta puerta ni reconstruir el estado del tablero por inferencia. Un bloqueo queda
registrado en el README (y en el Registro de Cambio cuando corresponda) con su causa y la fecha en que se habilitó.

## Cierre: versión nueva y censo

1. Con la aprobación de la entrega, guardar el resultado como **versión nueva**
   `MCP_POWERBI\01_bi\01_versiones\NN_modificacion_<ID>\[BI]\` (NN = siguiente número de ese tablero). Nunca sobrescribir
   una versión existente ni editar un PBIP dentro de `01_versiones`.
2. Censar esa versión con el DLC del censo: tipo `Actualización`, `--origen "DLC de modificación <ID>"`. Al registrarse,
   el censo actualiza el diccionario de datos (R60).
3. Registrar en el README el `census_id` de cierre y la ruta de la versión entregada.

El trabajo no se declara cerrado hasta que ese censo esté registrado.

## Fuentes nuevas: diccionario de datos

Si la modificación agrega una fuente, tabla o columna de origen, aplicar
`../../00_Base_Compartida/16_diccionario_datos_y_simulacion.md` igual que Creación: ubicarla en el diccionario
(tablas de los tableros y catálogo de Athena), decidir columnas y filtros con el dueño, construir con la versión de
práctica y verificar la conexión real antes de entregar. Si un cambio quita o renombra columnas que otros tableros
usan, consultar antes «¿qué tableros usan X?».

## Condiciones de parada adicionales

Además de la ausencia de CENSO, detener la ejecución (sin modificar archivos) si:
- no se puede identificar de forma inequívoca el BI;
- la última versión guardada del tablero no está disponible en `01_versiones`;
- no se puede preparar una copia de trabajo separada en `01_kiro`;
- faltan permisos o herramientas para validar un cambio que puede afectar resultados;
- hay una decisión obligatoria del analista pendiente.

Registrar el motivo, el estado, lo que falta y la condición necesaria para reanudar. No declarar `Listo para entrega` mientras exista un bloqueo.

## Límites de la modificación frente a depuración

La revisión integral de integridad forma parte de toda modificación. Sin embargo, una optimización general de consultas, reducción de columnas, refactorización amplia de DAX o eliminación de elementos que no sean necesarios para el cambio solicitado no se ejecuta como parte implícita de esta tarea. Documentar el hallazgo, explicar beneficio/riesgo y solicitar autorización para abrir un proceso separado de Depuración y Mejora.
