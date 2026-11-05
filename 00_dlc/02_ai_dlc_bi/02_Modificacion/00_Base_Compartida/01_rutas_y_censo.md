# RUTAS, CENSO Y ORIGINAL — DLC DE MODIFICACIÓN

## Rutas oficiales

```text
MCP_POWERBI\
├── 00_dlc\
│   └── 01_ai-dlc-censo\
├── 01_bi\
│   └── 01_versiones\
│       ├── 00_original\
│       │   ├── REGISTRO_CONTROL_TABLEROS.md\
│       │   └── [Nombre exacto BI]\
│       │       └── README.md\
│       └── 01_kiro\
│           └── [Nombre exacto BI]\
├── 01_documentacion_tableros\
└── 02_censo\
```

## Regla de identificación

Antes de actuar, solicitar o confirmar el nombre exacto del BI. Usar el mismo nombre para localizar el CENSO, el original, la copia Kiro y la documentación. No asumir equivalencias entre nombres parecidos.

## Puerta de entrada: CENSO obligatorio

1. Buscar el CENSO en `MCP_POWERBI\02_censo`.
2. Confirmar que corresponde al BI exacto y que está disponible/legible.
3. Si no existe, no corresponde o no se puede validar, establecer el estado `BLOQUEADO — CENSO REQUERIDO` (si no corresponde o no es legible, indicar además la causa concreta).
4. Ejecutar el ritual ubicado en `MCP_POWERBI\00_dlc\01_ai-dlc-censo` y guardar el resultado en `MCP_POWERBI\02_censo`.
5. Volver a verificar identidad y disponibilidad del CENSO.
6. Solo entonces habilitar el análisis y ejecución de la modificación.

## Protección del original y copia Kiro

- Original PBIP: `MCP_POWERBI\01_bi\01_versiones\00_original\[Nombre exacto BI]\`.
- Copia de trabajo: `MCP_POWERBI\01_bi\01_versiones\01_kiro\[Nombre exacto BI]\`.
- Nunca ejecutar cambios sobre `00_original`.
- Crear/preparar y usar la copia Kiro únicamente después de validar el CENSO.
- Si el original no está disponible como PBIP o no puede preservarse, detener la ejecución y explicar el bloqueo; no sobrescribir ni reemplazar silenciosamente el original.

## Trazabilidad

Mantener un README histórico por tablero en `MCP_POWERBI\01_bi\01_versiones\00_original\[Nombre exacto BI]\README.md` y el registro central en `MCP_POWERBI\01_bi\01_versiones\00_original\REGISTRO_CONTROL_TABLEROS.md`.

Registrar únicamente los dos correos definidos para el control de responsables:
- correo de quien trabaja/modifica;
- correo de quien solicita/es dueño del requerimiento.

El README es acumulativo: no crear uno nuevo por cada intervención. El registro central refleja el estado actual; el histórico conserva intervenciones anteriores.

## Fuentes corporativas

Logo oficial: `MCP_POWERBI\00_dlc\02_ai_dlc_creacion_modificacion\00_fuentes\Logo_Nebula.png`.
No sustituirlo automáticamente si falta; informar la ruta esperada y solicitar la fuente o autorización.
