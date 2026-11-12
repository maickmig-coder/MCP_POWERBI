# Nebula BI — Repositorio de Business Intelligence y AI-DLC

Repositorio central de los tableros de Power BI de **Nebula** y de la metodología de trabajo asistido por IA
(**AI-DLC**) con la que se documentan, crean, modifican y depuran. Los tableros se guardan en formato **PBIP**.
Los mismos procesos los ejecutan el agente **Kiro** (`.kiro/steering/`) y Claude Code (`CLAUDE.md`).

## Estructura

```text
MCP_POWERBI/
├── README.md                       ← este archivo
├── CLAUDE.md                       ← reglas del proyecto para Claude Code
├── diccionario-datos.md            ← catálogo de Athena (copia del repositorio nbp033-ingenieria-inversa-tableros)
├── .kiro/
│   ├── settings/mcp.json           ← servidores MCP de Kiro (Power BI, documentación de AWS y Microsoft)
│   └── steering/                   ← guías instaladas para Kiro (censo y diccionario)
├── 00_dlc/                         ← metodología AI-DLC
│   ├── 00_diccionario_datos/       ← DLC del diccionario de datos + diccionario generado
│   ├── 01_ai-dlc-censo/            ← DLC del censo (radiografía de un tablero, sin modificarlo)
│   └── 02_ai_dlc_bi/               ← DLC de tableros
│       ├── 00_Base_Compartida/     ← reglas comunes a Creación, Modificación y Depuración
│       ├── 00_fuentes/             ← Logo_Nebula.png
│       ├── 01_Creacion/
│       ├── 02_Modificacion/
│       └── 03_Depuracion/
├── 01_bi/01_versiones/             ← versiones guardadas de cada tablero (no se editan)
│   ├── 00_original/<BI>/           ← primera versión aprobada
│   ├── NN_<proceso>_<ID>/<BI>/     ← versiones siguientes (01_modificacion_MOD-001…)
│   └── 01_kiro/<BI>/               ← copia de trabajo del agente (no es una versión)
└── 02_censo/
    ├── REGISTRO_CONTROL_TABLEROS.md  ← quién trabaja cada tablero y en qué estado está
    └── <BI>/                         ← censo vigente, cambios, historial y README del tablero
```

## Cómo se trabaja

```text
Censo  ──►  Diccionario de datos  ──►  Creación / Modificación / Depuración  ──►  versión nueva  ──►  Censo
```

| Proceso | Qué hace | Dónde |
|---|---|---|
| **Censo** | Documenta un tablero tal como está: fuentes, modelo, cálculos, gráficas, filtros, reglas de negocio y hallazgos. Solo lectura. Al cerrarse, actualiza el diccionario de datos. | `00_dlc/01_ai-dlc-censo` |
| **Diccionario de datos** | Inventario de conexiones, tablas y columnas de todos los tableros, con la estructura real del catálogo de Athena y una «versión de práctica» de cada tabla para construir sin datos ni contraseñas. | `00_dlc/00_diccionario_datos` |
| **Creación** | Construye un tablero nuevo con fuentes del diccionario y el diseño corporativo V10. | `00_dlc/02_ai_dlc_bi/01_Creacion` |
| **Modificación** | Cambia un tablero existente. Solo parte de un censo **vigente** (describe el tablero final) y **validado** por el dueño. | `00_dlc/02_ai_dlc_bi/02_Modificacion` |
| **Depuración** | Corrige integridad y rendimiento de un tablero existente; no agrega ni rediseña. Misma puerta del censo. | `00_dlc/02_ai_dlc_bi/03_Depuracion` |

## Principios

- Toda afirmación lleva certeza: **Encontrado**, **Inferido** o **Desconocido**; no se inventan fuentes, tipos ni reglas.
- Se trabaja en la copia `01_kiro`; las versiones guardadas no se editan. Cada trabajo termina en una versión nueva censada.
- Nada se elimina de un tablero sin la aprobación registrada del dueño; el censo solo lista candidatos.
- Las propuestas de la IA no se aplican sin aprobación del analista.
- Control de personas: solo dos correos (quien trabaja y quien solicita/es dueño).
- Nunca se guardan contraseñas, tokens ni cadenas de conexión con secretos, ni se crean tablas o vistas en las bases.

## Para empezar

- Leer `CLAUDE.md` (resumen de reglas) y el `README.md` del proceso que se va a ejecutar.
- Diccionario de datos: escribir «menú del diccionario».
- Censo: pedir «censar <tablero>» con los dos correos (quien censa y dueño del tablero).
