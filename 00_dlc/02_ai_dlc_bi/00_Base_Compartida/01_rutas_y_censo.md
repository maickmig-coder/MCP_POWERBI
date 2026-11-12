# RUTAS, VERSIONES, CENSO Y TRAZABILIDAD — CREACIÓN, MODIFICACIÓN Y DEPURACIÓN

Documento común a los tres procesos. Las diferencias por proceso están en «Entrada del censo según el proceso».

## Rutas oficiales

```text
MCP_POWERBI\
├── diccionario-datos.md                  ← catálogo de Athena (copia del repositorio nbp033-ingenieria-inversa-tableros)
├── 00_dlc\
│   ├── 00_diccionario_datos\             ← DLC del diccionario y diccionario generado (no se edita a mano)
│   │   ├── config.json                   (ruta del catálogo de Athena)
│   │   ├── diccionario-datos.md / .json  (generado)
│   │   └── simulacion\                   (Sim_<objeto>.m, Real_<objeto>.m)
│   ├── 01_ai-dlc-censo\                  ← DLC del censo
│   └── 02_ai_dlc_bi\
│       ├── 00_Base_Compartida\           ← reglas comunes a los tres procesos (este archivo)
│       ├── 00_fuentes\
│       │   └── Logo_Nebula.png
│       ├── 01_Creacion\
│       ├── 02_Modificacion\
│       └── 03_Depuracion\
├── 01_bi\
│   └── 01_versiones\                     ← SOLO versiones guardadas del tablero (el PBIP nunca se edita aquí)
│       ├── 00_original\[Nombre exacto BI]\          primera versión aprobada
│       ├── NN_<proceso>_<ID>\[Nombre exacto BI]\     versiones siguientes (01_modificacion_MOD-001, 02_depuracion_DEP-001…)
│       └── 01_kiro\[Nombre exacto BI]\               copia de trabajo del agente (NO es una versión)
├── 01_documentacion_tableros\
└── 02_censo\
    ├── REGISTRO_CONTROL_TABLEROS.md      ← registro central de todos los tableros
    └── [Nombre exacto BI]\
        ├── README.md                     ← historial de trabajo del tablero (creación, modificaciones, depuraciones)
        ├── [Nombre exacto BI] - censo.md ← censo vigente (lo escribe el DLC del censo)
        └── … (cambios, historial y revisiones del censo)
```

Ruta oficial del logo: `MCP_POWERBI\00_dlc\02_ai_dlc_bi\00_fuentes\Logo_Nebula.png`. No usar rutas antiguas
(`01_fuentes`, `02_ai_dlc_creacion_modificacion`) ni rutas locales de desarrollo. Si el logo falta, informar la ruta
esperada y solicitarlo; no sustituirlo.

## Regla de nombre

Solicitar y confirmar el nombre exacto del BI antes de crear carpetas o archivos. Usar el mismo nombre en
`01_versiones`, `01_kiro`, `02_censo`, el README, el registro central y la documentación. No asumir equivalencias
entre nombres parecidos. En una creación, si el nombre aún no está definido, registrar un nombre provisional aprobado.

## Versiones y copia de trabajo

- `01_versiones` guarda **solo versiones terminadas y aprobadas** del tablero. Nunca se edita un PBIP allí.
- `01_kiro\[Nombre exacto BI]\` es la **copia de trabajo** del agente: todo se construye o cambia ahí. No cuenta como
  versión: el censo la ignora y bloquea censarla (R54).
- Al aprobarse el trabajo, el resultado se guarda como **versión nueva**, sin sobrescribir las anteriores:
  - Creación: `01_versiones\00_original\[Nombre exacto BI]\`;
  - Modificación / Depuración: `01_versiones\NN_<proceso>_<ID>\[Nombre exacto BI]\`, donde `NN` es el número siguiente
    a la última versión de ese tablero (dos dígitos) e `<ID>` el identificador del trabajo (`MOD-001`, `DEP-001`).
- La versión nueva **siempre se censa** (`Inicial` en Creación; `Actualización` con `--origen "<DLC> <ID>"` en
  Modificación y Depuración). Al registrarse, el censo actualiza solo el diccionario de datos (R60 del censo).
  El trabajo no se cierra hasta que ese censo esté registrado.

## Entrada del censo según el proceso

### Creación
El censo del BI nuevo **no es requisito de entrada** (aún no existe): se marca `No aplica`. Las fuentes salen del
diccionario de datos (regla `16_diccionario_datos_y_simulacion.md`). Si la solicitud parte de un BI existente
(copiar, reconstruir, continuar), no es Creación: reclasificar como Modificación o Depuración.

### Modificación y Depuración — puerta del censo (R56)
Antes de preparar la copia de trabajo, ejecutar desde `00_dlc/01_ai-dlc-censo`:

```bash
python scripts/censo.py vigencia --markdown "../../02_censo/<BI>/<BI> - censo.md" --versiones "../../01_bi/01_versiones" --correo-revisor "<correo>"
```

| Resultado | Acción |
|---|---|
| No existe el censo | `BLOQUEADO — CENSO REQUERIDO`: ejecutar el DLC del censo (tipo `Inicial`) y volver a verificar. |
| `DESACTUALIZADO` (hay una versión guardada más reciente, la huella no coincide o hay un borrador abierto) | `BLOQUEADO — CENSO DESACTUALIZADO`: el censo no describe el tablero final. Censar la última versión (tipo `Actualización`) y volver a verificar. |
| `VIGENTE` pero `NO APTO` (estado distinto de «Completado y validado» o puntos pendientes con el dueño) | `BLOQUEADO — CENSO SIN VALIDAR`: completar la validación con el dueño (`iniciar-validacion` + `guia-validacion`). |
| `VIGENTE` y `APTO` | Continuar. Registrar el `census_id` en el README y en la plantilla del proceso. |

La copia de trabajo se prepara **desde la última versión guardada** que indica `vigencia` (no necesariamente
`00_original`).

## Trazabilidad por tablero

Cada tablero tiene, desde el inicio del trabajo:
- `MCP_POWERBI\02_censo\[Nombre exacto BI]\README.md`: historial acumulativo (plantilla `10_plantilla_readme_tablero.md`).
  En una creación, la carpeta se crea al iniciar; el censo se agregará al liberar el tablero.
- `MCP_POWERBI\02_censo\REGISTRO_CONTROL_TABLEROS.md`: estado actual de todos los tableros
  (plantilla `11_plantilla_registro_central.md`).
- Correo de quien trabaja/modifica y correo de quien solicita/es dueño (no se piden otros datos personales).
- Fecha, tipo de trabajo, estado, decisiones, validaciones, `census_id` de partida y versión entregada.

Un tablero mantiene el mismo README toda su vida: cada intervención se agrega al historial; no se crea un README
nuevo. Estos archivos son la única escritura permitida fuera de `01_kiro`, junto con la versión nueva aprobada.
