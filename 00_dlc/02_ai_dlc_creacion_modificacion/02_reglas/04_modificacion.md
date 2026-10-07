# 6. REGLAS DE MODIFICACIÓN

1. Solicitar nombre exacto.
2. Buscar CENSO.
3. Si no existe, bloquear y realizar CENSO.
4. Preservar PBIP original.
5. Analizar solicitud y alcance.
6. Identificar dependencias.
7. Clasificar riesgo.
8. Registrar propuesta/decisión.
9. Modificar.
10. Validar.
11. Revisar integridad completa.

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
Buscar CENSO
↓
¿Existe CENSO?
├── No → Bloquear modificación y solicitar CENSO
└── Sí → Continuar
↓
Identificar versión/original
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
Listo para entrega
```


## Registro individual de cada cambio

Además del README histórico, cada modificación relevante debe documentarse
mediante `03_plantillas/06_registro_de_cambio.md`.

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


# REGLA BLOQUEANTE — CENSO OBLIGATORIO Y CONSERVACIÓN DEL PBIP ORIGINAL

## Cuando no existe CENSO

Si se solicita modificar un BI existente y **no existe un CENSO del tablero en**:

```text
NIGGA\02_censo
```

la modificación **DEBE QUEDAR BLOQUEADA**.

No se debe modificar, depurar ni alterar el BI basándose únicamente en el
archivo actual.

### Procedimiento obligatorio

1. Solicitar el **nombre exacto del BI**.
2. Verificar la existencia del CENSO correspondiente en:

```text
NIGGA\02_censo
```

3. Si el CENSO no existe, informar que la modificación queda bloqueada.
4. Conservar el BI original como **PBIP** en:

```text
NIGGA\01_bi\01_versiones\00_original\[Nombre exacto BI]\
```

5. Ejecutar el ritual de CENSO definido en:

```text
NIGGA\00_dlc\01_ai-dlc-censo
```

6. Guardar el resultado del CENSO en:

```text
NIGGA\02_censo
```

7. Verificar que el CENSO quedó disponible y corresponde al BI exacto.
8. Solo después de esta verificación se puede continuar con la modificación.

### Ejemplo

Para:

```text
GC - Leads MG
```

el original debe conservarse en:

```text
NIGGA\01_bi\01_versiones\00_original\GC - Leads MG\
```

y el CENSO debe quedar registrado en:

```text
NIGGA\02_censo
```

### Prohibición

El AI-DLC **no puede saltarse el CENSO** para avanzar más rápido con una
modificación.

Si el CENSO no existe, el estado de la solicitud debe ser:

```text
BLOQUEADO — CENSO REQUERIDO
```

La modificación solo cambia a estado de ejecución cuando el CENSO ha sido
realizado, guardado y verificado.

## Cuando el CENSO sí existe

Si el CENSO existe:

1. cargarlo como contexto del estado actual del BI;
2. verificar que corresponde al nombre exacto del tablero;
3. conservar el PBIP original sin modificarlo;
4. continuar con el análisis de alcance, dependencias, riesgo y propuesta;
5. ejecutar únicamente los cambios aprobados;
6. realizar las validaciones correspondientes;
7. actualizar el README y el Registro de Cambio.

## Relación con el Registro de Cambio

Cuando la modificación estuvo inicialmente bloqueada por ausencia de CENSO,
esta situación debe quedar documentada en el Registro de Cambio o en el
histórico del README, indicando:

- CENSO no encontrado;
- modificación bloqueada;
- PBIP original conservado;
- CENSO solicitado/realizado;
- ruta donde quedó el CENSO;
- fecha en que se habilitó nuevamente la modificación.
