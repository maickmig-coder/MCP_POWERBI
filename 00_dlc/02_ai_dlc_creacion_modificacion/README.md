# AI-DLC FINAL — Ritual Integral para Power BI

## Versión
Versión consolidada oficial de trabajo.

## Objetivo
Este paquete consolida las reglas anteriores del AI-DLC con las nuevas reglas
surgidas de los casos reales del proyecto.

El ritual contempla tres procesos:

1. Creación de BI.
2. Modificación de BI existente.
3. Depuración y Mejora de BI.

Además contempla CENSO, diseño corporativo, integridad, fuentes, consultas,
SQL, Power Query, modelo, DAX, rendimiento, dependencias, versionamiento,
decisiones del analista, pruebas antes/después y cierre formal.

## Relación con CENSO

- AI-DLC-CENSO responde: "¿Cómo está construido actualmente el BI?"
- AI-DLC responde: "¿Qué debemos construir, modificar o depurar y cómo hacerlo?"

## Rutas oficiales

- Ritual CENSO:
  `NIGGA\00_dlc\01_ai-dlc-censo`
- AI-DLC creación/modificación:
  `NIGGA\00_dlc\02_ai_dlc_creacion_modificacion`
- Fuentes corporativas:
  `NIGGA\00_dlc\02_ai_dlc_creacion_modificacion\00_fuentes`
- Logo oficial:
  `C:\dev\NIGGA\00_dlc\02_ai_dlc_creacion_modificacion\00_fuentes\Logo_Nebula.png`
- BI originales y carpeta de trazabilidad:
  `NIGGA\01_bi\01_versiones\00_original\[Nombre exacto BI]`
- Registro central de tableros:
  `NIGGA\01_bi\01_versiones\00_original\REGISTRO_CONTROL_TABLEROS.md`
- README/histórico de cada tablero:
  `NIGGA\01_bi\01_versiones\00_original\[Nombre exacto BI]\README.md`
- CENSO:
  `NIGGA\02_censo`
- Documentación de tableros:
  `NIGGA\01_documentacion_tableros`

## Regla de evolución del propio AI-DLC

Ninguna nueva versión debe eliminar silenciosamente una regla existente.

Antes de publicar una versión nueva:
1. comparar con la versión anterior;
2. identificar reglas nuevas;
3. identificar reglas modificadas;
4. identificar reglas reemplazadas;
5. identificar reglas eliminadas;
6. justificar cualquier reemplazo o eliminación;
7. conservar trazabilidad de la versión anterior.

## Principio
No asumir información que pueda cambiar el resultado. Preguntar cuando falte
información relevante. Diferenciar solicitud, obligación técnica, propuesta de IA
y decisión del analista. No ejecutar cambios fuera del alcance aprobado.


## Control de responsables y trazabilidad

Desde el inicio de cualquier creación, modificación o depuración se debe
registrar quién trabaja el tablero.

Cada tablero mantiene un único README histórico dentro de su carpeta:

```text
NIGGA\01_bi\01_versiones\00_original\[Nombre exacto BI]\README.md
```

El README conserva la historia completa del tablero: responsable, solicitante,
fechas, tipo de trabajo, versiones, cambios realizados, decisiones,
validaciones, alertas y pendientes.

Adicionalmente existe un registro central:

```text
NIGGA\01_bi\01_versiones\00_original\REGISTRO_CONTROL_TABLEROS.md
```

El registro central permite identificar rápidamente quién está trabajando cada
tablero y en qué estado se encuentra.

**Regla:** si un tablero se crea y posteriormente se modifica varias veces,
no se crea un README nuevo. Se continúa la misma historia en el README
existente.


## Control de personas por tablero

El control de personas se simplifica a únicamente:
- Correo de quien trabaja/modifica el tablero.
- Correo de quien solicita/es dueño del requerimiento.

No se requieren nombres u otros datos personales para este control.


## Versión V4 — Consolidación

Esta versión consolida el AI-DLC y mantiene las reglas funcionales anteriores.
El control de identificación de personas se simplifica exclusivamente a dos
correos:

- Correo de quien trabaja/modifica.
- Correo de quien solicita/es dueño.

El historial del tablero permanece en un único README dentro de la carpeta del
tablero.
