# AI-DLC — Diccionario de datos (v2.4.1)

Inventario, en un solo lugar, de **las conexiones, tablas y columnas que usan los tableros**. Se arma leyendo
todos los censos. Además deja una "versión de práctica" de cada tabla (mismas columnas, sin datos ni contraseñas)
para que Creación construya tableros nuevos y cambie a la conexión real al final.

```text
01_ai-dlc-censo  ──►  00_diccionario_datos  ──►  02_ai_dlc_bi\01_Creacion
 (un tablero a la vez)     (todos los censos)               (usa el diccionario)
```

## Qué hay en esta carpeta

| Archivo | Para qué |
|---|---|
| `ai-dlc/menu-diccionario.md` | Menú de 4 opciones para las personas |
| `ai-dlc/disparadores.md` | Qué hace el agente con cada frase |
| `kiro/steering/disparadores-diccionario.md` | Hace que Kiro (y Claude, vía `CLAUDE.md`) reconozca el menú y las frases. Instalada para Kiro como `.kiro/steering/disparadores-diccionario.md`: si se modifica aquí, se vuelve a copiar allá |
| `scripts/diccionario.py` | Lee los censos, arma el diccionario, busca y revisa si está al día |
| `config.json` | Ruta del catálogo de Athena (`catalogo_athena`). Hoy: `diccionario-datos.md` en la **raíz del proyecto**, una copia del catálogo del repositorio `nbp033-ingenieria-inversa-tableros` (`inputs\schemas\diccionario-datos.md`). Una ruta relativa se resuelve desde la raíz, así funciona igual en cualquier equipo. Cuando el otro repositorio publique una versión nueva, se vuelve a copiar a la raíz |
| `diccionario-datos.md` | **El diccionario** (generado, no se edita a mano): conexiones, tablas, columnas y qué tableros usan cada tabla |
| `diccionario-datos.json` | Lo mismo, para el agente (generado) |
| `simulacion\Sim_<tabla>.m` / `Real_<tabla>.m` | Versión de práctica y conexión real de cada tabla (generados) |

## Qué contiene el diccionario

1. **Conexiones:** tipo de conexión (Athena, SQL Server…), servidor o DSN y qué tableros la usan.
2. **Tablas:** de qué conexión salen, su ruta, de dónde se tomó su estructura y qué tableros las usan.
3. **Columnas por tabla:** tipo **real** de la base, nombre en cada tablero (y si un tablero le cambia el tipo o la
   quita), si parece dato personal (marcado automáticamente por el nombre) y qué filtros de carga le pone cada
   tablero (solo como información: la versión de práctica no los aplica).

### Cuándo se actualiza

**Solo, al cerrar cada censo** (regla R60 del censo): `censo.py registrar` ejecuta `actualizar` con el correo de
quien hizo el censo. «actualiza censos» queda para repetirlo si falló o si cambió el catálogo de Athena. El
diccionario lee solo el censo vigente de cada tablero (`02_censo/<BI>/<BI> - censo.md`), nunca borradores ni
censos archivados. De la lista de fuentes del censo (3.1) toma solo las que vienen de una base: las tablas calculadas
y las de fecha automáticas las genera Power BI y no son conexiones. El censo, a su vez, usa el mismo catálogo de Athena
para comparar cada fuente con su estructura real (R61 del censo v2.3.7).

### Si varios tableros usan la misma tabla

Cada tabla aparece **una sola vez**, con la suma de lo que dicen todos los censos:

| Situación | Qué hace el diccionario |
|---|---|
| Un tablero carga más columnas que otro | Se listan todas; cada columna dice qué tableros la cargan («Nombre en los tableros»). Una columna que solo usa un tablero aparece con ese tablero. |
| Un tablero quita una columna | Aparece igual, con «quitada en <tablero>». |
| La tabla está en el catálogo de Athena | Columnas y tipos salen del catálogo completo; las que ningún tablero usa dicen «ningún tablero la usa». Lo que cargue cada tablero no cambia la estructura. |
| La tabla no está en el catálogo | Se usa la unión de lo que cargan los tableros. Una columna que **ningún** tablero carga no se conoce (por ejemplo, si todos la descartan seleccionando columnas). |
| Dos tableros dan tipos distintos | Con catálogo: manda el tipo real y se anota «<tablero> lo cambia a …». Sin catálogo: «distinto entre tableros» y la versión de práctica usa `type any`. |
| Filtros de carga distintos | Una línea por tablero, cada uno con sus filtros; ninguno se aplica a la versión de práctica. |
| La misma tabla por conexiones distintas (otro DSN o consulta SQL propia) | Quedan como tablas separadas, porque el diccionario las identifica por conexión y ruta. |

### De dónde sale la estructura real

| La tabla… | Columnas y tipos salen de | Cómo se ve |
|---|---|---|
| está en el catálogo de Athena | el catálogo, en su orden, antes de cualquier ajuste de un tablero | `varchar`, `integer`, `timestamp(3)`… |
| no está (fuente aún no migrada, SQL Server, etc.) | el censo (tipo final en el tablero) | «No verificado en catálogo (en el tablero: …)» |

Si un tablero usa una columna que el catálogo no tiene, se marca «⚠ No está en el catálogo» y aparece un aviso: el
catálogo puede estar desactualizado. Si el catálogo trae tildes o eñes dañadas («a�o»), la comparación las tolera
y el diccionario muestra el nombre correcto del censo. El diccionario solo **lee** el catálogo (nunca lo modifica);
cuando cambia la copia, `estado` lo detecta y «actualiza censos» lo incorpora. **Si el catálogo configurado no se
encuentra, `actualizar` se detiene** (no regenera solo con los censos, porque perdería los tipos reales); se corrige
la ruta o, si es intencional, se usa `--sin-catalogo`.

### Censos que no describen el tablero final

Al actualizar, cada censo se revisa con el mismo control que usa `censo.py vigencia` (última versión guardada en
`01_versiones` y misma huella del PBIP; la copia de trabajo `01_kiro` no cuenta). Si un censo ya no describe el
tablero final (por ejemplo, se guardó una versión nueva sin censar), el diccionario lo marca «⚠ NO describe el
tablero final» y muestra un aviso: sus fuentes pueden estar desactualizadas hasta que se vuelva a censar. `estado`
detecta ese cambio aunque el censo no se haya tocado.

### Versiones de práctica obsoletas

Al actualizar, se borran de `simulacion\` los `Sim_` / `Real_` de tablas que ya ningún tablero usa, para que
Creación no tome una versión de práctica obsoleta.

## Cómo se usa

Escribir **«menú del diccionario»** y elegir: 1 ver fuentes · 2 buscar · 3 qué tableros usan algo · 4 actualizar.

Comandos (desde `C:\dev\MCP_POWERBI`):

```bash
python 00_dlc/00_diccionario_datos/scripts/diccionario.py <comando> --censos 02_censo --salida 00_dlc/00_diccionario_datos
```

`estado` · `actualizar --correo-ejecutor <correo>` · `buscar --texto X` · `impacto --objeto X [--columna C]` ·
`simulacion --objeto X`. Requisitos: Python 3.10 o superior, sin paquetes externos. Para el control de vigencia usa
`censo_versiones.py` del DLC del censo (`00_dlc/01_ai-dlc-censo/scripts`); si no está, ese control se omite.

## Alcance

Solo lectura. No modifica censos ni tableros, no se conecta a bases de datos, no guarda contraseñas ni datos y no
crea tablas. Solo conoce las tablas que algún tablero censado usa.

## Cambios en v2.4.1 (2026-11-13)

- Una consulta SQL ya no figura como «Solo censo (no está en el catálogo)»: dice qué tablas del catálogo lee
  («Consulta SQL: columnas del censo; lee del catálogo …»). Cada columna toma el tipo real de la tabla leída donde
  está, o se marca «calculada o renombrada en el SQL». El resumen cuenta aparte las consultas SQL que solo leen
  tablas del catálogo.
- `estado` dice cuándo el diccionario está desactualizado porque se actualizó su programa.

## Cambios en v2.4 (2026-11-13)

- **Consultas SQL nativas:** el SQL es el segundo argumento de `Value.NativeQuery` (antes se tomaba el nombre del
  servidor y la conexión real quedaba inservible). Cada consulta es una fuente propia, con nombre legible
  («Consulta Atom c1cfb0»); antes dos consultas distintas se mezclaban en una sola.
- La conexión real copia el origen tal como lo usa el tablero (por ejemplo
  `AmazonAthena.Databases("Athena_ODBC2", null, []){[Kind="Database"]}[Data]`) y su SQL completo.
- Lee el SQL del bloque «Consulta SQL» del censo (ritual v2.3.9). Si un censo anterior omite el SQL, avisa y no registra
  esa fuente: hay que volver a censar.
- Ignora las columnas que crea la propia consulta M (duplicadas o agregadas) y las tablas calculadas y de fecha
  automáticas: no existen en la base. Escribe siempre en UTF-8.

## Cambios en v2.3 (2026-11-12)

- El catálogo de Athena se lee desde la copia en la raíz del proyecto (ruta relativa en `config.json`).
- Si el catálogo configurado no se encuentra, `actualizar` se detiene en vez de degradar los tipos.
- Los censos que no describen el tablero final se marcan y avisan (mismo control que `censo.py vigencia`).
- Se borran las versiones de práctica de tablas que ya no se usan.

## Cambios en v2.2 (2026-11-11)

La búsqueda y la versión de práctica alcanzan **todo el catálogo de Athena**, no solo las tablas que ya usan los
tableros: así un tablero nuevo puede partir de una tabla que nadie ha usado todavía. Esas tablas no se listan en
`diccionario-datos.md` (solo se indica cuántas hay); se consultan con «busca fuente …».

## Cambios en v2.1 (2026-11-11)

La estructura de cada tabla pasa a ser la **real de la base** (catálogo de Athena), no la que deja un tablero
después de sus ajustes. El catálogo se lee desde su repositorio (`nbp033-ingenieria-inversa-tableros`), con la
ruta en `config.json`. Sin catálogo para una tabla, se usa el censo y se marca.

## Cambios en v2.0 (2026-11-11)

Se simplificó para que sea un inventario: se retiraron la revisión obligatoria de la IA (`anotaciones-ia.md`), el
cierre formal (`validar`, `registrar`, `historial-diccionario.md`), el Excel, los comandos `borrador` y
`pendientes`, y las secciones de relaciones, tablas auxiliares, puntos abiertos de los censos, conflictos,
limitaciones y validación. El menú pasó de 11 a 4 opciones.
