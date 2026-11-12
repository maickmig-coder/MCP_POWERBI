# 16. DICCIONARIO DE DATOS Y SIMULACIÓN DE CONEXIÓN

## Propósito

Un BI nuevo casi siempre consume bases de datos que otros tableros ya usan. Esas conexiones no se toman de un
censo en particular: se toman del **diccionario de datos**, que consolida todos los censos y lo genera el
`AI-DLC Diccionario de datos` (`MCP_POWERBI\00_dlc\00_diccionario_datos`).

Con el diccionario, Creación **simula la conexión**: construye el modelo con el esquema exacto del origen
(nombres y tipos de columna), sin datos ni credenciales, y cambia a la conexión real al final sin rehacer nada.

**Quién la aplica:** Creación siempre; Modificación cuando el cambio agrega una fuente, tabla o columna de origen
(donde dice «BI nuevo», léase «la parte nueva del BI»). Depuración no agrega fuentes y no la aplica; puede consultar
«¿qué tableros usan X?» antes de tocar la carga de una tabla.

**Censos que no describen el tablero final:** si el diccionario marca un tablero con «NO describe el tablero final»,
sus filtros y columnas pueden estar desactualizados; tomarlos solo como referencia y verificar en la conexión real.

## Fuente oficial

| Archivo | Uso |
|---|---|
| `MCP_POWERBI\00_dlc\00_diccionario_datos\diccionario-datos.json` | Lectura por Kiro / MCP |
| `MCP_POWERBI\00_dlc\00_diccionario_datos\diccionario-datos.md` | Lectura humana y evidencia |
| `MCP_POWERBI\00_dlc\00_diccionario_datos\simulacion\Sim_<objeto>.m` / `Real_<objeto>.m` | Consultas M a copiar |

Creación **no lee censos individuales para obtener conexiones** y **no modifica el diccionario**.
El CENSO del BI que se crea sigue siendo `No aplica`.

## Paso 1 — Comprobar que el diccionario está vigente

Aplicar el disparador **DD-02 «consulta diccionario»** del DLC del diccionario
(`00_dlc/00_diccionario_datos/ai-dlc/disparadores.md`):

```bash
python 00_dlc/00_diccionario_datos/scripts/diccionario.py estado --censos 02_censo --salida 00_dlc/00_diccionario_datos
```

| ESTADO | Acción |
|---|---|
| `AL_DIA` | Continuar |
| `DESACTUALIZADO` / `SIN_DICCIONARIO` (censo nuevo, modificado o eliminado) | Ejecutar DD-01 (`actualizar`) antes de seguir |
| Error al actualizar | Detener la parte de fuentes; no construir sobre un diccionario desactualizado |

Para ubicar la fuente usar DD-04 (`buscar`) y para obtener las consultas DD-06 (`simulacion`).

Registrar en el levantamiento el `diccionario_id` usado.

## Paso 2 — Ubicar la fuente pedida

El usuario nombra la fuente en lenguaje natural (ej.: "Athena, Entregas Totales"). Buscar en el diccionario por:
nombre del objeto en origen, nombre en los modelos que lo usan, descripción y motor/destino.

La búsqueda revisa primero las tablas que ya usan los tableros y después **todo el catálogo de Athena**, incluidas
las tablas que ningún tablero usa todavía.

| Resultado | Acción |
|---|---|
| **Encontrada** en una tabla que ya usan tableros | Paso 3 |
| **Encontrada solo en el catálogo** (ningún tablero la usa) | Paso 3, sabiendo que: no hay filtros de otros BI que revisar, la estructura viene solo del catálogo y la conexión real se arma con el mismo DSN de Athena de los tableros (o se pide el DSN si no hay uno conocido). Registrar en el levantamiento «Origen: catálogo de Athena (sin uso previo)». |
| **Ambigua** (varias tablas) | Mostrar las opciones (esquema.tabla y tableros que las usan); el usuario elige |
| **No encontrada** en ninguno | Paso 6 |

## Paso 3 — Presentar la ficha y decidir con el usuario

Antes de construir, mostrar de la ficha del objeto:
- `objeto_id`, conexión y ruta de navegación;
- columnas con tipo, marcando las de **posible dato personal** y las de tipo **distinto entre tableros**;
- usos en otros BI con sus **filtros de carga** — son reglas de esos BI, no del origen.

Preguntar y registrar:
1. qué columnas se incluyen (datos personales solo con decisión registrada);
2. qué filtros de carga se aplican en el BI nuevo (ninguno se hereda en silencio);
3. si el significado de alguna columna usada en un KPI no está claro, preguntarlo al dueño; el censo del tablero
   que la usa puede tenerlo registrado como punto abierto.

## Paso 4 — Construir en modo simulación

En el PBIP de trabajo (`01_kiro`):

1. Crear el parámetro `ModoSimulacion = true` (lógico, obligatorio).
2. Por cada objeto, copiar del diccionario:
   - `Sim_<objeto>`: `#table` tipado con el esquema del origen, 0 filas;
   - `Real_<objeto>`: navegación real exacta;
   - `Src_<objeto>`: `if ModoSimulacion then Sim_<objeto> else Real_<objeto>`.
3. Las tablas del modelo parten **solo** de `Src_<objeto>` y aplican sus transformaciones (selección de columnas,
   filtros aprobados, renombres, tipos).
4. `Sim_`, `Real_` y `Src_` con carga deshabilitada (`enableLoad = false`); solo las tablas del modelo se cargan.
5. Construir relaciones, medidas y visuales normalmente. Con 0 filas, los visuales se ven vacíos: en simulación se
   valida estructura (bindings, DAX sin errores, relaciones, layout), no valores.

## Paso 5 — Cambiar a la conexión real y verificar

Antes de liberar:
1. `ModoSimulacion = false` y actualizar.
2. Comparar el esquema real con la ficha: columnas faltantes, nuevas o de otro tipo.
3. Si hay diferencias: registrarlas, ajustar el BI si es seguro y **reportarlas** para que se actualice el censo
   correspondiente y se regenere el diccionario. Creación no edita el diccionario.
4. Validar valores (totales, conteos, KPI) contra la fuente o contra el criterio del dueño.
5. Conservar `Sim_` y el parámetro (permiten trabajar sin credenciales en futuras modificaciones) o retirarlos según
   la decisión registrada; en ambos casos `ModoSimulacion = false` en la versión liberada.

Una conexión no verificada en el paso 5 bloquea la liberación.

## Paso 6 — Fuente que no está en el diccionario

1. Informar que la fuente no figura en el diccionario vigente ni en el catálogo de Athena (indicar el `diccionario_id`).
2. Si está en un destino conocido (mismo DSN/servidor del diccionario), proponer la navegación con el mismo conector.
3. Si es un destino nuevo, solicitar: motor, servidor/DSN, base o catálogo, esquema, tabla/vista y método de
   autenticación administrado. Nunca contraseñas, tokens ni cadenas con credenciales.
4. Para simular sin acceso, el usuario puede entregar el esquema (columnas y tipos); la simulación se marca
   `Esquema suministrado por [correo]`, no `Según diccionario`.
5. La IA no crea tablas ni vistas en la base de datos; un objeto inexistente es una dependencia externa.
6. La fuente entrará al diccionario cuando el BI liberado se cense y se regenere el diccionario.

## Reutilización adicional

Tablas auxiliares (ej.: la tabla de fecha de actualización que alimenta el header), medidas y temas de otros BI se
consultan en sus censos, previa aprobación y sin reutilizar objetos con referencia rota o hallazgos abiertos.

## Limitaciones que deben informarse

- El diccionario lista las tablas que algún BI censado consume; la búsqueda alcanza además todo el catálogo de
  Athena, pero no las fuentes que aún no se han migrado (SQL Server, archivos, etc.) si ningún BI censado las usa.
- Columnas y tipos son los reales del catálogo de Athena cuando la tabla está ahí; si la ficha dice «no verificado
  en catálogo», son los que tenía el tablero censado y pueden diferir de la base: fijar los tipos en la tabla del
  modelo, justo después de `Src_<objeto>`.
- El diccionario dice que una tabla existía en la fecha del censo, no que existe hoy: por eso el paso 5 es obligatorio.
