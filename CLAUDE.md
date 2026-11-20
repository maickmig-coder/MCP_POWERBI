# MCP_POWERBI — Contexto del proyecto

Proyecto con metodología **AI-DLC** para documentar y construir tableros **Power BI guardados en PBIP**.
El **censo** de cada tablero es la fuente de verdad para cualquier creación, modificación o depuración.
Los mismos procesos los ejecuta también el agente **Kiro**; aquí se siguen exactamente las mismas reglas.

## Cómo hablar con las personas

- Responder siempre en **español** y en **lenguaje sencillo**: muchas personas del equipo no son técnicas.
  Decir "tablero", "tabla", "dato", "fuente"; dejar los términos técnicos (IDs, M, TMDL, comandos) como referencia al final.
- Antes de cambiar archivos, explicar en una o dos frases qué se va a hacer.
- Al terminar, decir qué cambió y cuál es el siguiente paso natural.

## Mapa de carpetas (raíz `C:\dev\MCP_POWERBI`)

```text
MCP_POWERBI\
├── diccionario-datos.md         ← catálogo de Athena (copia del repo nbp033-ingenieria-inversa-tableros); no se edita
├── 00_dlc\
│   ├── 00_diccionario_datos\    ← DLC del diccionario + diccionario generado (este último no se edita a mano)
│   ├── 01_ai-dlc-censo\         ← DLC del censo
│   └── 02_ai_dlc_bi\            ← DLC de tableros
│       ├── 00_Base_Compartida\  ← reglas comunes a Creación, Modificación y Depuración (una sola copia)
│       ├── 00_fuentes\Logo_Nebula.png
│       ├── 01_Creacion\ · 02_Modificacion\ · 03_Depuracion\
├── 01_bi\01_versiones\                      ← SOLO versiones guardadas: nunca se edita un PBIP aquí
│   ├── 00_original\[Nombre exacto BI]\      ← primera versión aprobada
│   ├── NN_<proceso>_<ID>\[Nombre exacto BI]\ ← versiones siguientes (01_modificacion_MOD-001…)
│   └── 01_kiro\[Nombre exacto BI]\          ← copia de trabajo: aquí se construye (NO es una versión)
└── 02_censo\
    ├── REGISTRO_CONTROL_TABLEROS.md         ← registro central de tableros
    └── [Nombre BI]\
        ├── README.md                        ← historial de trabajo del tablero
        └── [Nombre BI] - censo.md           ← un censo por tablero
```

Ciclo: **Censo → Diccionario de datos → Creación / Modificación / Depuración → versión nueva → Censo**.
Rutas, versiones y puerta del censo de los tres procesos: `00_dlc\02_ai_dlc_bi\00_Base_Compartida\01_rutas_y_censo.md`.

---

## 1. Censo — `00_dlc\01_ai-dlc-censo`

**Qué es:** la "radiografía" de un tablero: fuentes, transformaciones, modelo, columnas, medidas, visuales,
filtros, bookmarks, reglas de negocio, hallazgos y candidatos a depuración. Un tablero a la vez.

**Antes de censar:** leer el `README.md` de esa carpeta; es el documento rector y define el ritual vigente
(versión 2.3.10, con su script `censo.py`). Guías de Kiro instaladas en `.kiro\steering\`; si se cambia una guía en
`00_dlc\01_ai-dlc-censo\kiro\`, volver a copiarla allí.

Reglas que nunca cambian:
- Pedir **dos correos** antes de leer el PBIP: quién realiza el censo y quién es dueño del tablero.
- El PBIP se lee, **nunca se modifica**.
- Resultado solo en **Markdown**: `02_censo\[Nombre BI]\[Nombre BI] - censo.md`, más su historial.
- Cada versión nueva del PBIP se censa **completa**; las diferencias entre versiones van en un archivo de cambios aparte.
- Si quien censa no es el dueño, el estado queda «Completado pendiente de validación» hasta que el dueño confirme
  las reglas inferidas y los pendientes. Modificación y depuración quedan **bloqueadas** hasta esa confirmación.
- El censo **no autoriza eliminar** nada; solo lista candidatos con evidencia.
- No registrar credenciales.
- La sección 3 documenta **todas** las fuentes (R61–R63): cada base comparada columna por columna con el catálogo de
  Athena, el contenido de las tablas escritas a mano y las tablas de fecha automáticas con su columna de origen. En la
  sección 14 se revisan las reglas de conjunto (R64), por ejemplo un tablero repartido en una página por segmento.

Al cerrar un censo (`registrar`), el propio censo actualiza el diccionario de datos (R60); no pedir «actualiza
censos» aparte. Si `registrar` muestra «AVISO (R60)», informarlo y sugerir «actualiza censos» para repetirlo.

**¿El censo describe el tablero final?** Lo responde `censo.py vigencia` (R53): el censo debe ser de la última
versión guardada en `01_versiones` y su huella debe coincidir. La copia de trabajo `01_kiro` no cuenta como versión
y no se puede censar (R54): primero se guarda como versión `NN_<proceso>_<ID>`.

---

## 2. Diccionario de datos — `00_dlc\00_diccionario_datos`

**Qué es (v2.4.1):** un inventario armado con **todos** los censos: conexiones (tipo y servidor), tablas y columnas
(tipo real, nombre en cada tablero, posible dato personal) y qué tableros usan cada tabla con sus filtros de carga.
La estructura real (columnas y tipos antes de los ajustes de cada tablero) sale del catálogo de Athena:
`diccionario-datos.md` en la raíz del proyecto, copia del repositorio `nbp033-ingenieria-inversa-tableros`
(ruta relativa en `00_dlc\00_diccionario_datos\config.json`; solo lectura). Si el catálogo no se encuentra,
`actualizar` se detiene en vez de degradar los tipos. Si una tabla no está en el catálogo (fuente aún no migrada),
sale del censo y se marca. Los censos que no describen el tablero final se marcan «NO describe el tablero final». La búsqueda («busca fuente») y la versión de práctica alcanzan
**todo el catálogo**, incluidas tablas que ningún tablero usa todavía: tenerlas presentes en cada creación nueva.
Se genera en `00_dlc\00_diccionario_datos`. Deja una "versión de práctica" de cada tabla (mismas columnas, sin datos
ni contraseñas) para que Creación construya y cambie a la conexión real al final. Sin revisión de la IA ni cierre
formal: se actualiza solo al cerrar cada censo; «actualiza censos» queda para repetirlo o incorporar un catálogo nuevo.
Si varios tableros usan la misma tabla, aparece una sola vez con la unión de sus columnas y qué tablero usa cada una
(detalle en el README del diccionario).

Documentos: `ai-dlc/menu-diccionario.md` (menú de 4 opciones), `ai-dlc/disparadores.md` (qué hacer en cada opción).

Comando base (desde la raíz; en Windows puede ser `py` en vez de `python`):

```bash
python 00_dlc/00_diccionario_datos/scripts/diccionario.py <comando> --censos 02_censo --salida 00_dlc/00_diccionario_datos
```

**Regla obligatoria:** antes de responder cualquier pregunta sobre fuentes, ejecutar `estado`.
Si no es `AL_DIA` (censo nuevo, modificado o eliminado), ejecutar primero `actualizar --correo-ejecutor <correo>`
(pedir el correo una vez por sesión, explicando que es para dejar registro). Nunca responder sobre fuentes de
memoria ni desde un censo individual.

Los disparadores y el menú completo están en el archivo importado a continuación; aplicarlos igual que Kiro:

@00_dlc/00_diccionario_datos/kiro/steering/disparadores-diccionario.md

---

## 3. Creación de tableros nuevos — `00_dlc\02_ai_dlc_bi\01_Creacion`

**Qué es:** el proceso para construir un tablero **nuevo**. Antes de empezar, leer el `README.md` de la carpeta de
Creación (`00_dlc\02_ai_dlc_bi\01_Creacion\README.md`) y seguir su orden de lectura. Las reglas comunes están en
`00_dlc\02_ai_dlc_bi\00_Base_Compartida\`.

Reglas clave:
- Solo para tableros nuevos. Si se parte de un tablero existente, detenerse: es Modificación o Depuración.
- Pedir **dos correos**: quién trabaja y quién solicita / es dueño.
- Crear el README del tablero en `02_censo\[Nombre BI]\README.md` y actualizar `02_censo\REGISTRO_CONTROL_TABLEROS.md`.
- Construir **solo** en `01_bi\01_versiones\01_kiro\[Nombre BI]\`; al aprobarse, guardar la versión en
  `01_versiones\00_original\[Nombre BI]\` y censarla (tipo `Inicial`).
- **Fuentes:** únicamente desde el diccionario de datos (regla `00_Base_Compartida\16_diccionario_datos_y_simulacion.md`):
  1. «consulta diccionario» (verifica que esté al día);
  2. ubicar la fuente y decidir con la persona columnas (incluidos datos personales) y filtros de carga (nada se hereda en silencio);
  3. construir en modo simulación: parámetro `ModoSimulacion` y consultas `Sim_` / `Real_` / `Src_`;
  4. antes de liberar, `ModoSimulacion = false` y verificar el esquema real contra el diccionario.
  Si la tabla solo está en el catálogo de Athena (ningún tablero la usa), se usa igual: estructura del catálogo y
  conexión con el DSN de Athena conocido, verificada en el paso 4.
  Si la fuente no está ni en el diccionario ni en el catálogo, pedir datos de conexión **sin contraseñas** (o el esquema) y declararla fuente nueva.
- **Diseño corporativo V10** (`02_diseno_corporativo.md`): header `#323131`; **solo logo Nebula**;
  segmentaciones **oscuras** (`#474747`, borde `#323131`, texto blanco, 69 × 135); botones con **radio 6 px**;
  colores del tema en orden azul `#1A73E8`, violeta `#8943A7`, rojo `#AE0A33`, teal `#028AB0`, naranja `#E06806`; fuente Segoe UI.
- Las **decisiones pendientes** del diseño (sección 4.17: px/pt, colores 6–8, color de advertencia, tono de KPI,
  jerarquía de filtros fuera de Leads, radio de segmentaciones, tamaño de ícono) se **preguntan**; no se deciden solas.
- KPIs y gráficos: preguntar si la persona los define o quiere propuestas; ninguna propuesta de IA se aplica sin aprobación.
- No declarar un tablero listo con bloqueantes críticos o validaciones sin ejecutar.

---

## 4. Modificación y Depuración — `00_dlc\02_ai_dlc_bi\02_Modificacion` y `03_Depuracion`

Antes de empezar, leer el `README.md` del proceso y seguir su orden de lectura.

- **Puerta del censo:** `censo.py vigencia` debe dar **VIGENTE** (el censo describe el tablero final) y **APTO**
  (validado por el dueño). Si no: `BLOQUEADO — CENSO REQUERIDO / DESACTUALIZADO / SIN VALIDAR`.
- Pedir **dos correos**; continuar el README del tablero en `02_censo\[Nombre BI]\README.md` y el registro central.
- Copia de trabajo en `01_kiro` desde la última versión guardada; ejecutar solo lo aprobado.
- **Cierre:** guardar la versión nueva `01_versiones\NN_modificacion_<ID>\` o `NN_depuracion_<ID>\` y censarla
  (tipo `Actualización`, `--origen "DLC de … <ID>"`); el trabajo no se cierra sin ese censo.
- **Modificación** usa el diccionario (regla 16) si agrega fuentes; conserva el diseño existente y aplica V10 a lo nuevo.
- **Depuración solo depura:** no agrega fuentes, tablas, columnas de origen, páginas ni visuales, y no rediseña.

---

## Prohibido en todo el proyecto

- Pedir, escribir o guardar contraseñas, tokens o cadenas de conexión con secretos.
- Modificar censos, versiones guardadas en `01_versiones` (salvo `01_kiro`) o el diccionario generado a mano.
- Crear, modificar o borrar tablas o vistas en las bases de datos.
- Inventar fuentes, tipos, reglas de negocio o datos: lo que no tenga evidencia se marca `Desconocido`.
- Eliminar objetos de un tablero sin la aprobación registrada del dueño.
