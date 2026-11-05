# RUTAS Y CONTROL DE ACTIVOS — CREACIÓN

## Alcance de este archivo

Este archivo aplica al proceso de **Creación de un BI nuevo**. No convierte una modificación o una depuración de un BI existente en creación. Si se descubre que el trabajo parte de un informe existente, detener el flujo y clasificar la solicitud correctamente antes de intervenir.

## Rutas oficiales

```text
MCP_POWERBI\
├── 00_dlc\
│   ├── 01_ai-dlc-censo\
│   └── 02_ai_dlc_creacion_modificacion\
│       └── 00_fuentes\
│           └── Logo_Nebula.png
├── 01_bi\
│   └── 01_versiones\
│       ├── 00_original\
│       │   ├── REGISTRO_CONTROL_TABLEROS.md
│       │   └── [Nombre exacto BI]\
│       │       ├── README.md
│       │       └── [versión base aprobada, cuando exista]
│       └── 01_kiro\
│           └── [Nombre exacto BI]\
│               └── [artefactos en construcción]
├── 01_documentacion_tableros\
└── 02_censo\
```

Ruta oficial del logo:
`MCP_POWERBI\00_dlc\02_ai_dlc_creacion_modificacion\00_fuentes\Logo_Nebula.png`

No usar la ruta antigua `01_fuentes` ni una ruta local de desarrollo como fuente oficial.

## Regla de nombre

Solicitar y confirmar el nombre exacto del BI antes de crear carpetas o archivos. Usar el mismo nombre para el README, registro central, carpeta Kiro, artefactos y documentación relacionada. Si el nombre aún no está definido, registrar un nombre provisional aprobado y no inventarlo unilateralmente.

## Creación: separación de trazabilidad y trabajo

### 1. Carpeta de trazabilidad

Crear o localizar:
`MCP_POWERBI\01_bi\01_versiones\00_original\[Nombre exacto BI]\`

Esta carpeta contiene el README histórico y, una vez aprobado el BI, la versión base liberada/protegida. **No se construye ni se modifica el artefacto de trabajo dentro de `00_original`.** Si aún no existe una versión aprobada, no simular que ya existe un original; documentar el estado como `En construcción`.

### 2. Copia de trabajo obligatoria

Crear la carpeta de trabajo:
`MCP_POWERBI\01_bi\01_versiones\01_kiro\[Nombre exacto BI]\`

Todos los artefactos en construcción se trabajan en esta ubicación. Mantener la estructura de proyecto PBIP y sus archivos asociados cuando aplique.

### 3. Liberación inicial

Cuando el analista apruebe la entrega y pasen las validaciones:
- registrar la versión/referencia liberada;
- conservar la versión base aprobada y protegida en `00_original\[Nombre exacto BI]\` según el mecanismo de versionado autorizado;
- conservar la ruta de trabajo Kiro y su historial;
- actualizar README, registro central y documentación técnica/funcional.

No sobrescribir una versión base aprobada sin conservar su reversibilidad e historial. Si el mecanismo exacto de promoción/versionado no está disponible, informar la limitación y solicitar definición; no fingir que se realizó.

## CENSO en una creación nueva

El CENSO **no es un requisito de entrada** para construir un BI verdaderamente nuevo. En la plantilla y registros debe marcarse `No aplica`.

Si la solicitud implica copiar, reconstruir, sustituir o continuar un BI existente, no asumir que es una creación limpia: confirmar el tipo de trabajo. Si es modificación o depuración de un BI existente, se aplican sus reglas específicas y el CENSO obligatorio.

## Registro de trazabilidad por tablero

Cada BI debe contar desde el inicio con:
- `README.md` acumulativo en `00_original\[Nombre exacto BI]\README.md`;
- registro central `MCP_POWERBI\01_bi\01_versiones\00_original\REGISTRO_CONTROL_TABLEROS.md`;
- ruta de trabajo `01_kiro\[Nombre exacto BI]\` documentada;
- correo de quien trabaja/modifica;
- correo de quien solicita/es dueño;
- fecha, estado, objetivo, decisiones, validaciones y versión/referencia.

Para el control de personas, solicitar únicamente los dos correos. No sustituirlos por nombres ni exigir datos personales adicionales.

## Regla transversal de copia Kiro

Todo BI creado por el agente debe construirse en:
`MCP_POWERBI\01_bi\01_versiones\01_kiro\[Nombre exacto BI]\`

`00_original` es el área protegida para la trazabilidad y la versión base aprobada; `01_kiro` es el área de trabajo. Nunca desarrollar directamente en `00_original`.
