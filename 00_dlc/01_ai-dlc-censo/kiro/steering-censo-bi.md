---
inclusion: auto
name: censo-bi
description: Ritual AI-DLC CENSO de tableros Power BI (PBIP). Úsalo siempre que se pida crear, actualizar, revisar, consultar, validar o iniciar la validación de un censo, ver su vigencia o sus pendientes, o registrar respuestas del dueño del tablero.
---

# Steering — Ejecutar el CENSO BI (ritual AI-DLC v2.3.3)

Copiar este archivo a `MCP_POWERBI/.kiro/steering/censo-bi.md`. Se carga solo cuando el pedido trata de un censo (inclusión automática); también puede invocarse con `#censo-bi`.

**Antes de cualquier acción** (crear, revisar, validar, consultar vigencia o pendientes): pide el correo de quien lo solicita y no ejecutes nada hasta tenerlo (paso 0, R57). Si el script responde que falta `--correo-revisor`, el paquete instalado está bien y faltó el correo; si el README del paquete no dice v2.3.3, el paquete está desactualizado: avisa al usuario.

Objetivo: producir `[BI] - censo.md` con el menor consumo posible. El script hace el trabajo mecánico en segundos; tú solo interpretas.

## Flujo obligatorio (en español, sin detenerte entre pasos)

0. **Revisión de un censo existente (R57).** Si el usuario pide revisar, consultar o validar cualquier censo, lo primero es preguntar: «¿Cuál es tu correo?». No aceptes nombres y no ejecutes nada hasta tenerlo. Pásalo como `--correo-revisor` en `vigencia`, `pendientes`, `validar` e `iniciar-validacion`.
   - **Para iniciar una validación (R58):** compara su correo con el del dueño (sección 0 del censo).
     - Si es el dueño: dile «Eres el dueño del tablero: inicio la validación» y ejecuta `iniciar-validacion`.
     - Si no lo es: pregúntale «No eres el dueño del tablero (dueño: <correo>). ¿Conoces las respuestas de los puntos pendientes y aceptas iniciar la validación sin ser el dueño? Quedará registrado.» Solo con un «sí» explícito agrega `--acepta-validar-sin-ser-dueno`. Si dice que no, detente y sugiere que la haga el dueño.
1. **Correos.** Si el usuario no dio el correo de quien realiza el CENSO y el del dueño del tablero, pídelos y detente. No aceptes nombres. Anota si son el mismo correo: entonces el usuario **es el dueño** (paso 7). En un censo nuevo, `--correo-revisor` es el correo de quien realiza el CENSO.
2. **Lee solo** `00_dlc/01_ai-dlc-censo/ai-dlc/ritual-censo-bi.md` y `criterios-puntos-revision.md`. No leas `scripts/*.py`, el CHANGELOG ni el historial completo.
3. **Tipo de censo.** Si no existe `02_censo/[BI]/[BI] - censo.md`, es `Inicial`. Si existe, ejecuta `python scripts/censo.py vigencia --markdown "..." --versiones "../../01_bi/01_versiones" --correo-revisor "<correo>"`:
   - **DESACTUALIZADO por una versión más reciente** → `Actualización`. Antes del borrador **pregunta al usuario**: «¿Guardaste el PBIP de la versión <versión> en 01_bi/01_versiones/<versión>/<BI>? ¿Viene de un DLC de modificación o de depuración (con qué identificador)?». Sin su confirmación, detente (R54).
   - **VIGENTE y el usuario trae respuestas del dueño** → `Validación`: `python scripts/censo.py iniciar-validacion --markdown "..." --pbip "..." --correo-revisor "<correo>"` (antes, aplica el paso 0: dueño o aceptación explícita, R58) y salta al paso 7.
4. **Borrador** (una sola ejecución, en primer plano, desde `00_dlc/01_ai-dlc-censo`):
   ```
   python scripts/censo.py borrador --pbip "..\..\01_bi\01_versiones\<versión>\[BI]" --salida "..\..\02_censo\[BI]" --version <versión> --tipo <Inicial|Actualización> --correo-ejecutor "..." --correo-dueno-tablero "..." [--pbip-guardado-confirmado]
   ```
   Si el script responde «CENSO BLOQUEADO», muestra el mensaje al usuario y detente.
   En `Actualización`, ejecuta enseguida `python scripts/censo.py comparar --borrador "...\[BI] - censo.borrador.md" --origen "<DLC y su ID, o No informado>"`.
5. **Pendientes:** `python scripts/censo.py pendientes --markdown "<censo o borrador>" --correo-revisor "<correo>"`. Te da la línea de cada `[IA: …]` y los puntos pendientes de validación con el dueño.
6. **Completa cada marcador** con una edición puntual (`str_replace` del texto del marcador). En una `Actualización`, `comparar` te indica el rango del censo vigente con el texto anterior: reutilízalo si los objetos que describe no cambiaron. Para decidir, lee **solo** el rango de líneas de la sección relacionada:
   | Marcador | Lee |
   |---|---|
   | Área, objetivo, pregunta central | Secciones 5.1, 8 y 10 |
   | Rol y granularidad de tablas | 5.1, 5.2 y la Matriz A de la tabla |
   | KPIs | 10 y, si hace falta, la fórmula de la medida en 7 |
   | Reglas de negocio | 14, la expresión citada en 6.1 y la fila de esa columna en la Matriz A (estado de uso) |
   | Dependencias | 3, 5.2, 7 (tabla) y 9.x (conciliación) |
   | Hallazgos y vacíos | 16 y la sección que cite cada fila |
   | Estado (encabezado y 18.2) | Resultado de `validar` |
7. **Validación con el dueño (R55).** En la sección 14 marca «Validación del dueño»: `No requerida` si la regla es Encontrado; `Pendiente de validación` si es Inferido.
   - **Si el usuario es el dueño, o aceptó validar sin serlo (R58):** ejecuta `python scripts/censo.py guia-validacion --markdown "..." --correo-revisor "<correo>"` y conduce la conversación **punto por punto** como dice la sección «Cómo presentar la validación» (R59). Registra cada respuesta apenas la recibas.
   - **Si no es el dueño:** no preguntes; el censo cierra `Completado pendiente de validación`.
   - Si la persona necesita pausar: lo respondido ya quedó escrito en el borrador; para retomar, vuelve a ejecutar `guia-validacion` sobre el mismo borrador (solo muestra lo que falta).
   - En una `Validación`, al terminar: `python scripts/censo.py comparar --borrador "..." --origen "Validación con el dueño"`.
8. **Validar:** `python scripts/censo.py validar --pbip "..." --markdown "..." --correo-revisor "<correo>"`. Corrige **solo** las líneas que indique cada error.
9. **Registrar:** `python scripts/censo.py registrar --pbip "..." --markdown "..." --alcance "..."`.
10. **Vigencia:** `python scripts/censo.py vigencia --markdown "...\[BI] - censo.md" --versiones "..\..\01_bi\01_versiones" --correo-revisor "<correo>"`.
11. **Cierre:** responde en 3–5 líneas: ruta del censo, estado, cambios respecto a la versión anterior (de `[BI] - cambios.md`), puntos pendientes con el dueño y el resultado de `vigencia` (APTO / NO APTO para el DLC). No pegues el documento.

## Cómo presentar la validación (R59)

Quien responde normalmente no conoce Power BI por dentro ni el proceso de cambios. Tu trabajo es que entienda **qué se revisa, por qué importa y qué se le pregunta**, sin abrumarlo.

**1. Antes del primer punto**, un mensaje corto de bienvenida:

> Vamos a revisar juntos {N} puntos del tablero «{BI}». En cada uno te cuento qué encontramos, por qué importa y qué necesito que me confirmes. Puedes responder con tus palabras; si no sabes algo, dímelo y lo dejamos anotado. Mientras haya puntos sin confirmar, no se podrán hacer cambios al tablero. Podemos pausar cuando quieras y retomar después.

**2. Un punto por mensaje**, en el orden de `guia-validacion` (primero lo de prioridad alta), con esta plantilla (entre 80 y 180 palabras):

> **Punto {n} de {N} — {título en lenguaje de negocio}** · prioridad {alta/media/baja}
>
> **Qué encontramos:** {1–3 frases: qué pasa, en qué página y en qué gráfico o tarjeta, con su título tal como lo ve el usuario}.
>
> **Por qué importa:** {el impacto concreto: qué número puede leerse mal, qué decisión podría tomarse con un dato equivocado o qué parte del tablero no funciona}.
>
> **Lo que necesito que me confirmes:** {una pregunta concreta, como máximo dos si están ligadas}.
>
> Puedes responder, por ejemplo: «Sí, así es…», «No, en realidad…» o «No lo sé».

Usa los datos de la ficha («Qué se encontró», «Dónde», «Impacto», «Qué hay que confirmar»), pero **tradúcelos**:

| En la ficha | Cómo decirlo |
|---|---|
| Visual, tarjeta (card), segmentación (slicer) | «el gráfico», «la tarjeta», «el filtro desplegable», con su título |
| Bookmark | «vista guardada» (lo que muestra un botón al hacer clic) |
| Medida, `CountNonNull`, `Sum` | «el cálculo»: «cuenta registros», «suma el valor» |
| Columna calculada | «un campo que el tablero arma a partir de otros datos» |
| Filtro de página | «la página solo muestra…» |
| Referencia rota, entidad inexistente | «el gráfico usa datos que no existen en este tablero, por eso sale vacío o con error» |
| Formato huérfano | «quedó una regla de colores o formato de otro tablero; no afecta el número» |
| Sin uso interno identificado | «no lo usa ningún gráfico, filtro ni cálculo del tablero» |
| DLC de modificación o depuración | «el proceso para hacer cambios al tablero» |

No muestres IDs, nombres de archivos, código DAX o M, «visual.json», «binding» ni números de sección. Si la persona pide el detalle técnico, dáselo.

**3. Ejemplo** (H-A12 del censo de GC - Flotillas):

> **Punto 1 de 27 — Tarjetas cuyo número podría no corresponder a su título** · prioridad alta
>
> **Qué encontramos:** en las páginas de Empresas y Convenios hay tres tarjetas que cuentan cuántos registros tienen el año diligenciado, en vez de usar un cálculo definido. Una de ellas, en Convenios, se titula «Ticket promedio», pero muestra una cantidad de registros, no un valor promedio.
>
> **Por qué importa:** quien mire «Ticket promedio» va a creer que ve el valor promedio por unidad, cuando ve un conteo. Si con ese número se fijan precios o metas, la decisión partiría de un dato equivocado.
>
> **Lo que necesito que me confirmes:** ¿la tarjeta «Ticket promedio» de Convenios debería mostrar el valor promedio por unidad? ¿Y las tarjetas «Total unidades» deben mostrar el número de unidades entregadas?

Para una regla de negocio (sección 14), explica qué hace el campo con un ejemplo de valores y pregunta si esa es la lógica del negocio. Ejemplo para RN06: «El tablero agrupa las entregas en dos semestres según el mes: enero a junio es S1 y julio a diciembre es S2. ¿Así se manejan los semestres en el negocio?».

**4. Cómo registrar cada respuesta** (en la fila de la ficha, apenas responda):

| Respuesta | Estado (16) o «Validación del dueño» (14) | «Respuesta del dueño» |
|---|---|---|
| Lo que dice el censo es correcto | `Confirmado por el dueño` | `{fecha} · {correo}: {sus palabras, resumidas sin cambiar el sentido}` |
| Lo que dice el censo no es correcto o no aplica | `Descartado por el dueño` | `{fecha} · {correo}: {cómo es en realidad}` |
| No lo sabe | `Pendiente de validación` | `{fecha} · {correo}: se preguntó; no lo sabe{, sugiere consultar a …}` |

Si la respuesta es ambigua, repregunta una sola vez con opciones concretas. Después de registrar, confirma en una línea: «Anotado: {resumen}. Quedan {k} puntos.» y pasa al siguiente.

**5. Al terminar**, resume en 4–6 líneas: cuántos confirmados, descartados y sin respuesta; qué significa (si quedan puntos sin respuesta, el tablero sigue sin poder modificarse, R56) y quién podría responder los pendientes. Luego sigue con `comparar`, `validar` y `registrar`.

## Reglas de redacción

- Todo ID que escribas va con su nombre: `visual_id · nombre`, `page_id · página`, `bookmark_id · bookmark` (R48).
- Un asunto va en una sola fila de la sección 16. Si ya existe una fila H-A o V-A que lo cubre, ajústala; no crees otra ni lo repitas en KPIs, dependencias o limitaciones (cítala por su ID).
- Un visual con «Formato huérfano» funciona: no lo describas como roto.
- Tus filas en la sección 16 usan `H01`, `V01`… (nunca `H-A`/`V-A`) y no citan filas H-A ni V-A. No crees filas que «agrupen» otras; una conclusión transversal va como vacío o en la sección 15.
- No afirmes en 2.1, 10, 14 o 15 lo que un vacío declara desconocido. Citar el vacío no basta si el texto sigue afirmando: si no se sabe qué es un campo, no le pongas adjetivo.
  - Incorrecto: «valor facturado (cuyo rótulo no está confirmado; ver V01)».
  - Correcto: «valor (`Entregas Totales[Valor]`, definición pendiente: V01)».
- Una columna calculada se interpreta por su expresión en 6.1, nunca por su nombre, y respetando su «Estado de uso» (R51). Su certeza es «Inferido».
  - Incorrecto: «DIVISION S: clasifica la división/segmento» o «RENTING: separa la línea renting» si 6.1 dice «Sin uso interno identificado».
  - Correcto: «DIVISION S: semestre S1 (ene–jun) o S2 (jul–dic) según el mes de `FechaEntregaCliente`» y «RENTING: marca …; sin uso interno identificado (17.2)».
- En 17.1 solo van limitaciones del proceso del censo; nunca problemas del tablero. Antes de agregar una, lee las 5 estándar: si la tuya dice lo mismo con otras palabras (por ejemplo, «no se abrió el tablero en Power BI Desktop» ya está en la 1 y la 3), no la agregues. El validador avisa si se parece a una estándar.

## Prohibido (genera costo sin valor)

- Presentar varios puntos en un mismo mensaje, usar jerga técnica sin traducirla o registrar una respuesta que la persona no dio (R59).
- Revisar o validar un censo sin el correo de quien revisa (R57), o usar `--acepta-validar-sin-ser-dueno` sin la aceptación explícita de la persona (R58).
- Editar `[BI] - cambios.md`, `historial-censos.md` o un censo de `versiones/`: los escribe `registrar`.
- Iniciar o recomendar un cambio al tablero si `vigencia` dice NO APTO (R56).
- Escribir scripts propios para generar tablas, JSON o Excel. El censo no tiene Excel ni JSON.
- Leer el Markdown completo, el código del script o el TMDL completo para «entenderlo». Lee rangos.
- Leer `examples/` durante un censo: el ejemplo es de otro tablero y es referencia para personas.
- Ejecutar comandos en segundo plano, con `Tee-Object`, redirecciones o esperas con `Start-Sleep`: cada comando termina en segundos.
- Reescribir o «mejorar» tablas que generó el script. Si ves un error del script, regístralo en la sección 16 (categoría Gobierno) y avísalo al usuario.
- Usar verbos de cambio («cambiar», «eliminar», «reemplazar», «corregir»…) en la columna «Punto de revisión».

## Si algo falla

- `CENSO BLOQUEADO (R02)`: faltan correos; pídelos.
- Error de lectura del PBIP en «Advertencias de lectura» (sección 2.4): continúa y decláralo en la sección 17.1.
- `validar` reporta diferencias de conciliación en un borrador sin editar: es un error del script; repórtalo al usuario con el texto exacto y no lo corrijas a mano.
