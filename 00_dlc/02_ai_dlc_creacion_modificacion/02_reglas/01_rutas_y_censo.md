# 3. RUTAS, CENSO Y ORIGINAL

## Rutas oficiales

```text
NIGGA\
├── 00_dlc\
│   ├── 01_ai-dlc-censo\
│   └── 02_ai_dlc_creacion_modificacion\
│       └── 01_fuentes\
│           └── Logo_Nebula.png
├── 01_bi\
│   └── 01_versiones\
│       └── 00_original\
│           └── [Nombre exacto BI]\
├── 01_documentacion_tableros\
└── 02_censo\
```

## Modificación/depuración de BI existente

1. Solicitar nombre exacto del informe.
2. Buscar el CENSO en `NIGGA\02_censo`.
3. Si existe, cargarlo como contexto.
4. Si no existe, bloquear la modificación/depuración que requiera estado actual.
5. Realizar el CENSO siguiendo:
   `NIGGA\00_dlc\01_ai-dlc-censo`
6. Guardar el CENSO en `NIGGA\02_censo` con el nombre exacto del tablero.
7. Guardar el original como PBIP en:
   `NIGGA\01_bi\01_versiones\00_original\[Nombre exacto BI]`
8. El original nunca es el destino del cambio.

## Regla del nombre

El nombre exacto del BI debe utilizarse para localizar, crear y relacionar
los activos del proceso.


## Control de trazabilidad por tablero

Cada tablero debe tener su propio registro antes de iniciar cualquier trabajo.

```text
NIGGA\
└── 01_bi\
    └── 01_versiones\
        └── 00_original\
            ├── REGISTRO_CONTROL_TABLEROS.md
            └── [Nombre exacto BI]\
                ├── README.md
                └── [PBIP/versiones/documentos relacionados]
```

El `REGISTRO_CONTROL_TABLEROS.md` permite identificar rápidamente quién está
trabajando cada tablero.

El `README.md` dentro de cada carpeta contiene la trazabilidad detallada y el
histórico completo de creación, modificaciones y depuraciones.

### Regla de continuidad

Un mismo tablero mantiene el mismo README durante toda su vida útil.
Si después de una creación se realizan una o varias modificaciones o
depuraciones, estas se agregan al histórico existente.

No crear un README nuevo por cada intervención.


## Regla de trazabilidad por correo

Para cada tablero, el README ubicado en:

`NIGGA\01_bi\01_versiones\00_original\[Nombre exacto BI]\README.md`

debe registrar únicamente:

- correo de quien trabaja/modifica;
- correo de quien solicita/es dueño.

El registro central:

`NIGGA\01_bi\01_versiones\00_original\REGISTRO_CONTROL_TABLEROS.md`

debe reflejar estos dos correos para el estado actual del tablero.


## Regla específica para modificación sin CENSO

Cuando se vaya a modificar un BI existente y no exista su CENSO, se debe:

```text
1. BLOQUEAR MODIFICACIÓN
2. Conservar PBIP original:
   NIGGA\01_bi\01_versiones\00_original\[Nombre exacto BI]\
3. Ejecutar:
   NIGGA\00_dlc\01_ai-dlc-censo
4. Guardar resultado:
   NIGGA\02_censo
5. Verificar CENSO
6. Habilitar modificación
```

La existencia del CENSO debe verificarse antes de ejecutar cualquier cambio
sobre el BI.


## Regla específica para depuración/mejora sin CENSO

La depuración/mejora de un BI existente sigue la misma regla de contexto que
la modificación:

```text
1. Buscar CENSO.
2. Si no existe → BLOQUEAR.
3. Conservar PBIP original en:
   NIGGA\01_bi\01_versiones\00_original\[Nombre exacto BI]\
4. Ejecutar:
   NIGGA\00_dlc\01_ai-dlc-censo
5. Guardar:
   NIGGA\02_censo
6. Verificar CENSO.
7. Habilitar depuración/mejora.
```

No se debe ejecutar depuración sobre un BI existente sin contexto suficiente.


# REGLA TRANSVERSAL — COPIA DE TRABAJO EN REPOSITORIO KIRO

Todo BI que sea **creado, modificado o depurado/mejorado por el agente** debe
tener una copia de trabajo correspondiente dentro del repositorio:

```text
NIGGA\01_bi\01_versiones\01_kiro
```

Esta carpeta será el **repositorio oficial de trabajo del agente** para las
copias correspondientes de los BI.

## Regla

Antes de comenzar a crear, modificar o depurar un BI, el agente debe generar
o preparar la copia de trabajo correspondiente y guardarla en:

```text
NIGGA\01_bi\01_versiones\01_kiro\[Nombre exacto BI]\
```

El trabajo del agente se realiza sobre esta copia de trabajo, nunca sobre el
original conservado en:

```text
NIGGA\01_bi\01_versiones\00_original\[Nombre exacto BI]\
```

## Separación de originales y trabajo

```text
NIGGA\01_bi\01_versiones\
├── 00_original\
│   └── [Nombre exacto BI]\
│       └── PBIP original
│
└── 01_kiro\
    └── [Nombre exacto BI]\
        └── Copia de trabajo del agente
```

### Regla de protección

- `00_original` = referencia/original protegido.
- `01_kiro` = copia sobre la que trabaja el agente.

El agente **no debe modificar directamente el contenido de `00_original`**.

## Aplicación por tipo de trabajo

### Creación

La creación realizada por el agente debe tener su copia de trabajo en:

```text
NIGGA\01_bi\01_versiones\01_kiro\[Nombre exacto BI]\
```

### Modificación

Cuando exista un BI que será modificado:

1. conservar el original en `00_original`;
2. generar/preparar la copia de trabajo;
3. guardar la copia en `01_kiro\[Nombre exacto BI]\`;
4. ejecutar la modificación sobre la copia de trabajo.

### Depuración y Mejora

Cuando exista un BI que será depurado/mejorado:

1. conservar el original en `00_original`;
2. generar/preparar la copia de trabajo;
3. guardar la copia en `01_kiro\[Nombre exacto BI]\`;
4. ejecutar la depuración/mejora sobre la copia de trabajo.

## Trazabilidad

La existencia de la copia de trabajo debe quedar documentada en el README
del tablero y, cuando corresponda, en el Registro de Cambio.

Debe poder identificarse:

- tablero;
- ruta del original;
- ruta de la copia de trabajo;
- versión/referencia trabajada.

## Regla de continuidad

`01_kiro` es el repositorio de trabajo del agente.

Las nuevas versiones o intervenciones deben conservar la trazabilidad definida
por el AI-DLC y no deben sobrescribir el original protegido.

Esta regla es transversal y se aplica a **Creación, Modificación y
Depuración/Mejora**.
