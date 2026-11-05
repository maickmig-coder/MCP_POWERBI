---
inclusion: manual
---

# Steering — Ejecutar el CENSO BI (ritual AI-DLC v2.3)

Copiar este archivo a `MCP_POWERBI/.kiro/steering/censo-bi.md` e invocarlo con `#censo-bi` al pedir un censo.

Objetivo: producir `[BI] - censo.md` con el menor consumo posible. El script hace el trabajo mecánico en segundos; tú solo interpretas.

## Flujo obligatorio (en español, sin detenerte entre pasos)

1. **Correos.** Si el usuario no dio el correo de quien realiza el CENSO y el del dueño del tablero, pídelos y detente. No aceptes nombres. Anota si son el mismo correo: entonces el usuario **es el dueño** (paso 7).
2. **Lee solo** `00_dlc/01_ai-dlc-censo/ai-dlc/ritual-censo-bi.md` y `criterios-puntos-revision.md`. No leas `scripts/*.py`, el CHANGELOG ni el historial completo.
3. **Tipo de censo.** Si no existe `02_censo/[BI]/[BI] - censo.md`, es `Inicial`. Si existe, ejecuta `python scripts/censo.py vigencia --markdown "..." --versiones "../../01_bi/01_versiones"`:
   - **DESACTUALIZADO por una versión más reciente** → `Actualización`. Antes del borrador **pregunta al usuario**: «¿Guardaste el PBIP de la versión <versión> en 01_bi/01_versiones/<versión>/<BI>? ¿Viene de un DLC de modificación o de depuración (con qué identificador)?». Sin su confirmación, detente (R54).
   - **VIGENTE y el usuario trae respuestas del dueño** → `Validación`: `python scripts/censo.py iniciar-validacion --markdown "..." --pbip "..."` y salta al paso 7.
4. **Borrador** (una sola ejecución, en primer plano, desde `00_dlc/01_ai-dlc-censo`):
   ```
   python scripts/censo.py borrador --pbip "..\..\01_bi\01_versiones\<versión>\[BI]" --salida "..\..\02_censo\[BI]" --version <versión> --tipo <Inicial|Actualización> --correo-ejecutor "..." --correo-dueno-tablero "..." [--pbip-guardado-confirmado]
   ```
   Si el script responde «CENSO BLOQUEADO», muestra el mensaje al usuario y detente.
   En `Actualización`, ejecuta enseguida `python scripts/censo.py comparar --borrador "...\[BI] - censo.borrador.md" --origen "<DLC y su ID, o No informado>"`.
5. **Pendientes:** `python scripts/censo.py pendientes --markdown "<censo o borrador>"`. Te da la línea de cada `[IA: …]` y los puntos pendientes de validación con el dueño.
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
   - **Si el usuario es el dueño:** preséntale los puntos pendientes de `pendientes` en grupos de 5 (ID, pregunta concreta y evidencia en una línea) y registra cada respuesta en «Respuesta del dueño» con la fecha. Pasa el estado a `Confirmado por el dueño` o `Descartado por el dueño`. Si no sabe, deja `Pendiente de validación` y escribe «<fecha>: se preguntó; el dueño no lo sabe».
   - **Si no es el dueño:** no preguntes; el censo cierra `Completado pendiente de validación`.
   - En una `Validación`, al terminar: `python scripts/censo.py comparar --borrador "..." --origen "Validación con el dueño"`.
8. **Validar:** `python scripts/censo.py validar --pbip "..." --markdown "..."`. Corrige **solo** las líneas que indique cada error.
9. **Registrar:** `python scripts/censo.py registrar --pbip "..." --markdown "..." --alcance "..."`.
10. **Vigencia:** `python scripts/censo.py vigencia --markdown "...\[BI] - censo.md" --versiones "..\..\01_bi\01_versiones"`.
11. **Cierre:** responde en 3–5 líneas: ruta del censo, estado, cambios respecto a la versión anterior (de `[BI] - cambios.md`), puntos pendientes con el dueño y el resultado de `vigencia` (APTO / NO APTO para el DLC). No pegues el documento.

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
