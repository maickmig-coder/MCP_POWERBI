# AI-DLC — Ritual estándar para el CENSO de BI (v2.3.3)

> **Para agentes (Kiro u otros):** antes de cualquier acción sobre un censo —crear, revisar, validar, iniciar una validación, consultar vigencia o pendientes— pide el correo de quien lo solicita y no ejecutes nada hasta tenerlo (R57). Sigue `kiro/steering-censo-bi.md`: si quien inicia una validación no es el dueño, pregunta si acepta validar sin serlo (R58), y presenta los puntos uno por uno con `guia-validacion` (R59).

> **Qué es:** un proceso de **solo lectura** que documenta un tablero Power BI guardado en PBIP con el detalle suficiente para que cualquier cambio posterior (modificación, creación o depuración) se planifique a partir de él.
>
> **Qué no es:** no modifica el BI, no decide cambios y no redacta instrucciones de cambio. Eso pertenece al **DLC de modificación, creación y depuración**, que usa el CENSO como base de conocimiento.
>
> **Principio desde v2.1:** el script hace todo lo mecánico; la IA solo interpreta. La única salida es un Markdown, y cada dato aparece en un solo lugar.

Documentos relacionados: `reglas-censo.md` (obligaciones), `catalogos.md` (valores permitidos), `checklist-censo.md` (verificación), `criterios-puntos-revision.md` (redacción de hallazgos). Guía operativa para agentes: `kiro/steering-censo-bi.md`.

---

## 1. Contrato del resultado

En la carpeta de salida del tablero (`02_censo/[Nombre exacto del BI]`) quedan:

| Archivo | Quién lo escribe | Contenido |
|---|---|---|
| `[BI] - censo.md` | `censo.py borrador` + la IA en los marcadores `[IA: …]` | **Estado actual** del tablero: secciones 0–18 de la última versión censada (R35). |
| `[BI] - cambios.md` | `censo.py comparar` y `registrar` | Registro de cambios entre versiones, append-only: un bloque por ejecución (R52). |
| `versiones/[BI] - censo - <census_id>.md` | `censo.py registrar` | Censos anteriores archivados, para consulta. No se editan. |
| `historial-censos.md` | `censo.py registrar` | Una fila por ejecución validada, append-only. |
| `revisiones-censo.md` | `vigencia`, `pendientes`, `validar`, `iniciar-validacion` | Quién consultó o revisó cada censo, cuándo, con qué comando y con qué resultado; append-only (R57). |

Mientras una ejecución está abierta existen además `[BI] - censo.borrador.md` y `[BI] - cambios.borrador.md`; `registrar` los integra. `censo.py vigencia` responde si el censo es el de la versión final y si es apto para el DLC (R53, R56).

No se generan Excel ni JSON. Si un historial `historial-censos.xlsx` de v2.0 existe, se conserva sin tocarlo.

### Estructura del Markdown

Numeración fija y continua. El script crea todas las secciones; se pueden agregar subsecciones, pero no quitar ni renumerar.

| # | Sección | Lo genera el script | Completa la IA |
|---|---|---|---|
| 0 | Control obligatorio previo | Correos | — |
| — | Encabezado | census_id, fecha y hora, versión, huella del PBIP, tipo | Estado (CAT-07) |
| 1 | Identificación | Datos técnicos del BI y de la ejecución | Área |
| 2 | Objetivo y alcance | Alcance y fuentes inspeccionadas | Objetivo y pregunta central |
| 3 | Fuentes de datos y conexiones | Conector, navegación, modo y parámetros por partición | — |
| 4 | Transformaciones (Power Query/M) | Código M completo (una vez) y tabla de pasos | — |
| 5 | Modelo de datos | Tablas, relaciones, jerarquías, propiedades y roles | Rol y granularidad de las tablas |
| 6 | Columnas | Matriz A con resultado por clase y estado de uso; expresiones de columnas calculadas; tablas de fecha automáticas | — |
| 7 | Medidas | Medidas con referencias, uso y estado; expresiones completas (una vez) | — |
| 8 | Páginas | Páginas existentes y páginas referenciadas que no existen | — |
| 9 | Visuales | Por página: ficha con nombre, posición, tamaño, clase y formato huérfano; bindings con nombre del visual; conciliación | — |
| 10 | KPIs | Tarjetas e indicadores con lo que calculan | Interpretación funcional |
| 11 | Filtros, segmentaciones e interacciones | Todos los filtros, segmentaciones e interacciones | — |
| 12 | Bookmarks, botones y navegación | 12.1 ficha de cada bookmark (targets que existen y que funcionan); 12.2 efecto real al activarlo; 12.3 matriz de estados guardados sin efecto por página; 12.4 botones; 12.5 tooltips y drillthrough | — |
| 13 | Recursos, tema y presentación | Estética: archivos de recursos, ubicación de banners, logos, formas y textos por página (con escala de cada imagen), tema y metadatos | — |
| 14 | Reglas de negocio | Reglas detectadas, con puntero a su implementación | Interpretación, certeza y «Validación del dueño»; reglas adicionales; respuestas del dueño |
| 15 | Dependencias | Elementos centrales y aislados | Mapa de arquitectura |
| 16 | Hallazgos, vacíos y puntos de revisión | Hallazgos detectables (H-A*) y vacíos estándar (V-A*) en una sola tabla | Revisión, hallazgos o vacíos de negocio y respuestas del dueño |
| 17 | Limitaciones y control para DLC posteriores | Limitaciones estándar del proceso y candidatas | Limitaciones del proceso propias de la ejecución (nunca problemas del tablero) |
| 18 | Validación final | Conciliación contra el PBIP | Justificación del estado |

### Un dato, un lugar

Para que el documento sea compacto y no haya contradicciones entre copias:

- El código M está solo en la sección 4; las expresiones DAX, solo en 6.1 (columnas calculadas) y 7 (medidas).
- El detalle de cada referencia vive en su sección de origen: visuales en 9, filtros y segmentaciones en 11, relaciones en 5, bookmarks en 12. La Matriz A solo muestra cuántas referencias hay por clase.
- Los textos visibles están en la sección 9; los renombres y tipos finales, en la Matriz A.
- Las rutas de evidencia se escriben una vez por tabla, no en cada fila.
- La sección 17.2 lista las candidatas a depuración con su ID y remite a la sección de origen.
- Hallazgos y vacíos están en una sola tabla (sección 16); un asunto ya cubierto por una fila no se repite en otra sección.
- Excepción aprobada: la ubicación (posición y tamaño) de banners, logos, formas y textos aparece en la sección 9 (inventario de todos los visuales) y en la 13.2 (vista de estética por página).

### Nombres junto a los IDs

Todo ID que relaciona un objeto con otro va acompañado de su nombre, para identificarlo sin abrir el PBIP: `visual_id · nombre`, `page_id · página`, `bookmark_id · bookmark`, `measure_id · medida`, `table_id · tabla`. El nombre de un visual es su título; si no tiene, su texto; si tampoco, su tipo y el campo que muestra (por ejemplo, `Segmentación: Tecnología (Entregas Totales[combustible])`) o la imagen que contiene.
- Las demás secciones citan objetos por su ID nativo.

---

## 2. Rutas

| Elemento | Ruta |
|---|---|
| Ritual | `MCP_POWERBI\00_dlc\01_ai-dlc-censo` |
| BI original (solo lectura) | `MCP_POWERBI\01_bi\01_versiones\[versión]\[Nombre exacto del BI]` |
| Salida | `MCP_POWERBI\02_censo\[Nombre exacto del BI]` |

---

## 3. Fases

### Fase 0 — Ingreso y tipo de censo

Toda consulta o revisión de un censo existente empieza pidiendo el correo de quien revisa (R57); los comandos de consulta lo exigen con `--correo-revisor`.

1. Pedir el correo de quien realiza el CENSO y el del dueño/responsable del tablero. Sin ambos, el script no se ejecuta (R02). Anotar si son el mismo (R55).
2. Decidir el tipo con la carpeta de salida y `01_versiones`:

| Situación | Tipo | Comando de inicio |
|---|---|---|
| No existe `[BI] - censo.md` | `Inicial` | `borrador --tipo Inicial` |
| Hay una versión guardada más reciente que la censada (`vigencia` dice DESACTUALIZADO) | `Actualización` | Preguntar al usuario si guardó el PBIP en `01_versiones/<versión>/<BI>` (R54); con su confirmación, `borrador --tipo Actualización --pbip-guardado-confirmado` |
| Mismo PBIP y hay respuestas del dueño por registrar | `Validación` | `iniciar-validacion` |

### Fase 1 — Borrador automático

```bash
python scripts/censo.py borrador --pbip "01_bi/01_versiones/<versión>/<BI>" --salida "02_censo/<BI>" --version <versión> --tipo <Inicial|Actualización> \
  --correo-ejecutor "..." --correo-dueno-tablero "..." [--pbip-guardado-confirmado]
```

El script lee el PBIP sin modificarlo y escribe el Markdown con todo lo mecánico resuelto y la huella del PBIP en el encabezado. En `Inicial` escribe `[BI] - censo.md`; en `Actualización`, `[BI] - censo.borrador.md`, sin tocar el censo vigente.

En `Actualización`, a continuación:

```bash
python scripts/censo.py comparar --borrador "02_censo/<BI>/<BI> - censo.borrador.md" --origen "DLC de depuración DEP-001"
```

`comparar` traslada al borrador las interpretaciones y validaciones de las secciones 14 y 16 cuyos objetos siguen existiendo, reabre las que citan objetos eliminados, escribe el bloque de cambios (`[BI] - cambios.borrador.md`) e indica, para cada marcador, el rango de líneas del censo vigente cuyo texto puede reutilizarse si los cambios no lo afectan (R52).

### Fase 2 — Interpretación (IA)

```bash
python scripts/censo.py pendientes --markdown "<censo o borrador>" --correo-revisor "<correo>"
```

La lista indica la línea de cada marcador `[IA: …]` y los puntos pendientes de validación. La IA:

1. Lee **solo** las secciones que necesita para cada marcador (por ejemplo, 9 y 10 para los KPIs); no lee el documento completo ni el código del script. En una `Actualización`, reutiliza el texto del rango indicado por `comparar` si los objetos que describe no cambiaron.
2. Reemplaza cada marcador por su contenido, con certeza `Encontrado`, `Inferido` o `Desconocido`.
3. Revisa las filas H-A* y V-A* de la sección 16 (prioridad, impacto, certeza) y agrega hallazgos o vacíos de negocio que solo una lectura funcional puede detectar, por ejemplo una tarjeta cuyo título no coincide con lo que calcula. Sus filas usan los prefijos `H01`, `V01`… (nunca `H-A`/`V-A`) y no citan filas H-A ni V-A: si un asunto ya tiene fila, ajusta esa fila. Una conclusión transversal (por ejemplo, «el PBIP viene de una plantilla») va como vacío o en la sección 15, no como un hallazgo que agrupe otros.
4. No afirma en 2.1, 10, 14 o 15 algo que un vacío de la sección 16 declare desconocido: cita el vacío.
5. Interpreta cada columna calculada desde su expresión en 6.1 y su «Estado de uso», no desde su nombre; su significado es «Inferido» (R51).
6. En la sección 14 marca «Validación del dueño»: `No requerida` si la regla es `Encontrado`; `Pendiente de validación` si es `Inferido` (R55).
7. No corrige los datos mecánicos. Si detecta un error del script, lo registra como `Hallazgo` de categoría `Gobierno` en la sección 16 y lo reporta.

### Fase 2b — Validación con el dueño (R55)

- **Si quien realiza el censo es el dueño:** la IA obtiene las fichas con `censo.py guia-validacion` y presenta **un punto a la vez**, en lenguaje de negocio: qué se encontró, por qué importa, qué se necesita confirmar y cómo responder (R59). Registra cada respuesta en «Respuesta del dueño» con fecha, correo y sus palabras, y pasa el estado a `Confirmado por el dueño` o `Descartado por el dueño`; si no sabe, deja `Pendiente de validación` con la constancia de que se preguntó. Se puede pausar: lo respondido queda en el borrador y `guia-validacion` muestra solo lo que falta.
- **Si es otra persona:** no se pregunta en esta ejecución; el censo cierra `Completado pendiente de validación`.
- **Validación posterior:** se pide el correo de quien la inicia (R57). Si es el del dueño, se inicia. Si no, se le pregunta si conoce las respuestas y si acepta validar sin ser el dueño; solo con su aceptación se agrega `--acepta-validar-sin-ser-dueno` (R58):

```bash
python scripts/censo.py iniciar-validacion --markdown "02_censo/<BI>/<BI> - censo.md" --pbip "01_bi/01_versiones/<versión>/<BI>" --correo-revisor "<correo>"
python scripts/censo.py guia-validacion --markdown "02_censo/<BI>/<BI> - censo.borrador.md" --correo-revisor "<correo>"
# presentar punto por punto y registrar cada respuesta (R59)
python scripts/censo.py comparar --borrador "02_censo/<BI>/<BI> - censo.borrador.md" --origen "Validación con el dueño"
```

### Fase 3 — Validación

```bash
python scripts/censo.py validar --pbip "01_bi/01_versiones/<versión>/<BI>" --markdown "<censo o borrador>" --correo-revisor "<correo>"
```

Se comprueban las secciones 0–18, los marcadores pendientes, los catálogos, los conteos aproximados, los IDs truncados, los verbos de cambio, la regla R22, la conciliación objeto por objeto contra el PBIP, la huella (R53) y la validación con el dueño (R55, R56). Tarda segundos.

### Fase 4 — Registro

```bash
python scripts/censo.py registrar --pbip "01_bi/01_versiones/<versión>/<BI>" --markdown "<censo o borrador>" --alcance "..."
```

Vuelve a validar y, solo si no hay errores (R42): archiva el censo anterior en `versiones/`, deja el borrador como `[BI] - censo.md`, agrega el bloque a `[BI] - cambios.md` y la fila a `historial-censos.md`.

### Fase 5 — Vigencia y paso al DLC

```bash
python scripts/censo.py vigencia --markdown "02_censo/<BI>/<BI> - censo.md" --versiones "01_bi/01_versiones" --correo-revisor "<correo>"
```

Responde **VIGENTE** o **DESACTUALIZADO** y **APTO** o **NO APTO** para el DLC de modificación o depuración, con la lista de lo que falta (R53, R56).

---

## 4. Criterios de clasificación que aplica el script

**Columnas (CAT-02):**

- `En uso`: tiene referencias en V, F o BK, o la usa una medida o columna calculada que a su vez está en uso.
- `Uso técnico`: solo la usan relaciones, ordenamiento o jerarquías (M), pasos de Power Query que la usan para filtrar, combinar o agrupar (PQ), o seguridad (SEC). Transformarse a sí misma (por ejemplo, `Text.Proper`) no cuenta como uso.
- `Uso desconocido`: solo la referencian objetos DAX que no están en uso.
- `Sin uso interno identificado`: V, F, D, M, PQ y BK en `0` o `NA`.

**Medidas:** en uso si tienen referencias en visuales, filtros o bookmarks, o si las usa otra medida en uso. Se señalan las medidas sin expresión y las que repiten la expresión de otra.

**Visuales:** `Referencia rota` si algún campo **de datos** (eje, valores, leyenda, filas…) usa una entidad o campo inexistente: el visual no puede dibujarse. Si la entidad inexistente solo aparece en una **regla de formato** (colores por categoría, formato condicional, título dinámico), es un `Formato huérfano`: el visual funciona, se clasifica por sus datos y se informa en un hallazgo de tipo «Observación». `Uso desconocido` si el visual está oculto y ningún bookmark lo muestra; `En uso` en los demás casos.

**Bookmarks:** cada target se evalúa por separado: si **existe** en el PBIP y si **funciona** (no es referencia rota). Con `applyOnlyToTargetVisuals`, el bookmark solo actúa sobre sus targets; los demás estados que guardó son «sin efecto». Estado: `Referencia rota` si su página no existe o si ninguno de sus targets existe y funciona; `En uso` si un botón o navegador lo invoca; `Uso desconocido` en los demás casos, porque puede usarse desde el panel de marcadores.

**Reglas de negocio:** los filtros de página o informe sin condición guardada no son reglas; siguen inventariados en 11.1.

**Recursos:** `En uso` si algún visual o página los referencia; `Uso técnico` si son temas; `Sin uso interno identificado` si no los usa nada; `Referencia rota` si el archivo no existe.

---

## 5. Relación con el DLC de modificación, creación y depuración

- **Puerta de entrada (R56):** el DLC solo empieza si `censo.py vigencia` responde **APTO**: el censo es de la última versión guardada, su huella coincide, su estado es `Completado y validado` y no quedan reglas (14) ni puntos (16) pendientes de validación. Si responde NO APTO, el DLC no continúa hasta cerrar lo que lista. El DLC cita el `census_id` con el que parte.
- El DLC de modificación toma de aquí los IDs completos, las referencias de cada objeto (secciones 5, 7, 9, 11 y 12), las candidatas (17.2), los hallazgos y vacíos (16) y los recursos (13). Con eso arma su plan y su matriz de regresión.
- El DLC guarda cada cambio como una versión nueva en `01_versiones/<versión>/<BI>` y no se cierra hasta ejecutar el CENSO de tipo `Actualización` sobre esa versión, con `--origen` igual a su identificador (R52, R54). Así `[BI] - cambios.md` muestra qué cambió y por qué proceso, y el censo vigente muestra el tablero final.
