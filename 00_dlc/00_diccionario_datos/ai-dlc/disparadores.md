# Disparadores del diccionario de datos (v2.3)

Frases que dice la persona y lo que hace el agente (Kiro o Claude). Cada disparador ejecuta
`scripts/diccionario.py`, así el resultado no depende de la interpretación de la IA.

Abreviatura: `A` = `--censos "02_censo" --salida "00_dlc/00_diccionario_datos"` (desde la raíz `MCP_POWERBI`).

## Regla común

**Antes de responder sobre fuentes, comprobar que el diccionario esté al día** (`estado A`). Si hay un censo nuevo,
modificado o eliminado, o cambió el catálogo de Athena, ejecutar primero DD-01. Los comandos de consulta lo hacen cumplir: responden `DETENIDO`
(código 10/11) si el diccionario no está al día. El correo se pide una vez por sesión, solo para actualizar.

## Resumen

| ID | Menú | Frases (ejemplos) | Ejecuta | Escribe |
|---|---|---|---|---|
| DD-00 | — | «menú del diccionario», «¿qué puedo hacer?» | Muestra el menú | No |
| DD-01 | 4 | «actualiza censos», «actualiza diccionario» | `estado`; si cambió algo → `actualizar --correo-ejecutor <correo>` | Solo si hay cambios |
| DD-02 | 1 | «consulta diccionario», «¿qué fuentes hay?» | `estado` (→ DD-01) y responder desde `diccionario-datos.md` | No |
| DD-04 | 2 | «busca fuente X», «¿dónde está la columna X?» | `buscar --texto "X"`; 0 resultados → DD-07 | No |
| DD-05 | 3 | «¿qué tableros usan X?», «impacto de X» | `impacto --objeto "X" [--columna "C"]` | No |
| DD-06 | — (Creación) | «prepara la conexión de X», «simula fuente X» | `simulacion --objeto "X"` | No |
| DD-07 | — (automático) | «fuente nueva X», o búsqueda sin resultados | Protocolo de fuente nueva | No |

## Detalle

**DD-01 — Actualizar.** Normalmente no hace falta pedirlo: el censo actualiza el diccionario al registrarse (R60
del censo). Se usa para repetir una actualización que falló o para incorporar un catálogo de Athena nuevo.
`AL_DIA` → «sin cambios; el diccionario no se regenera». Si no → `actualizar` e informar
censos usados, conexiones, tablas, columnas y los avisos (censos en formato anterior, consultas que combinan
orígenes, tablas sin columnas y, sobre todo, **censos que NO describen el tablero final**: decir qué tablero es y
que hay que volver a censarlo). Si responde «DETENIDO: no se encuentra el catálogo», no forzar: pedir que se revise
la ruta en `config.json`. Este DLC no censa: un censo con problemas se rehace con el DLC del censo.

**DD-02 — Consultar.** Responder con las secciones 1 (conexiones) y 2 (tablas) del diccionario; para algo concreto,
DD-04 o DD-05. Citar el `diccionario_id`. Nunca responder de memoria ni desde un censo individual.

**DD-04 — Buscar.** Busca en el nombre de la tabla (en origen y en los tableros) y en sus columnas, sin distinguir
mayúsculas ni tildes: primero en las tablas que usan los tableros y luego en **todo el catálogo de Athena** (tablas
que ningún tablero usa todavía, útiles para tableros nuevos; se listan hasta 25, `--limite` cambia el máximo).
Si hay varias, mostrarlas y pedir que la persona elija.

**DD-05 — Impacto.** Lista los tableros que traen la tabla o la columna, con su nombre en cada tablero, los que la
quitan y los filtros de carga que la usan. Decir siempre: el uso en gráficas, medidas y filtros de página está en
el censo de cada tablero listado.

**DD-06 — Versión de práctica (para Creación).** Entrega el parámetro `ModoSimulacion` y las consultas
`Sim_` / `Real_` / `Src_`, y avisa las columnas que podrían ser datos personales. Se usa con la regla 16 de Creación.
También sirve para tablas que **solo están en el catálogo**: la estructura sale del catálogo y la conexión real se
arma con el mismo DSN de Athena que usan los tableros (se avisa que hay que verificarla; si no hay DSN conocido, se
pide). Escribir «esquema.tabla» si el nombre se repite en varios esquemas.

**DD-07 — Fuente nueva.** Solo cuando no está en el diccionario **ni en el catálogo de Athena**. Decir que no
figura (con su `diccionario_id`). Si el servidor ya es
conocido (sección 1), proponer la misma conexión y pedir la tabla; si no, pedir motor, servidor/DSN, base, esquema,
tabla y método de autenticación administrado (nunca contraseñas ni tokens), o la lista de columnas para simular.
La fuente entra al diccionario cuando el tablero que la use se cense.

## Reglas en todos los disparadores

1. **Solo lectura:** no modifica censos, tableros ni bases de datos; no crea tablas ni vistas.
2. **Todo sale de un censo:** lo que no está en un censo no se completa de memoria.
3. **Origen y tablero separados:** columnas y tipos son de la tabla de origen; filtros de carga, renombres y
   columnas quitadas son decisiones de cada tablero y nunca se heredan sin aprobación.
4. **Estructura real:** columnas y tipos salen del catálogo de Athena (otro repositorio; ruta en `config.json`, solo
   lectura) cuando la tabla está ahí; si no
   (fuente aún no migrada), del censo, marcados «no verificado en catálogo». Si un tablero cambia el tipo real
   (ej.: NIT de texto a número), se indica junto al nombre en ese tablero.
5. **Datos personales:** se marcan solos por el nombre de la columna; Creación decide con el dueño si se incluyen.
6. **Sin contraseñas ni datos:** no se registran credenciales ni filas.
7. **Alcance:** el diccionario lista las tablas que usan los tableros; la búsqueda cubre además todo el catálogo de
   Athena. Las fuentes aún no migradas que ningún tablero usa no se conocen (→ DD-07).
