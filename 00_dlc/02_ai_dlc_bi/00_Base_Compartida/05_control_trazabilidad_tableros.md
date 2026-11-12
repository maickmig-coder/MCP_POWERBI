# CONTROL DE TRAZABILIDAD DEL TABLERO

## Objetivo

Todo tablero debe registrar únicamente los correos electrónicos de:
- **Correo de quien está trabajando/modificando el tablero.**
- **Correo de quien solicita/es dueño del requerimiento.**

Aplica a Creación, Modificación y Depuración/Mejora.

## Registro obligatorio al inicio

Antes de comenzar, crear o localizar (en la carpeta de salida del censo del tablero):

`MCP_POWERBI\02_censo\[Nombre exacto BI]\README.md`

El README debe contener como mínimo:

```text
Correo de quien trabaja/modifica: [correo]
Correo de quien solicita/es dueño: [correo]
```

## Histórico

El README conserva todas las intervenciones. No se borran registros anteriores.

| Fecha | Tipo de trabajo | Correo quien trabaja/modifica | Correo quien solicita/es dueño | census_id de partida | Versión entregada | Cambio realizado | Decisión | Estado |
|---|---|---|---|---|---|---|---|---|

## Continuidad

Si un tablero se crea y después se modifica varias veces, se mantiene el mismo README. No se crea uno nuevo por cada intervención.

## Registro central

Debe existir:

`MCP_POWERBI\02_censo\REGISTRO_CONTROL_TABLEROS.md`

| Tablero | Tipo de trabajo | Correo quien trabaja/modifica | Correo quien solicita/es dueño | Fecha inicio | Estado | Última actualización |
|---|---|---|---|---|---|---|

## Regla

Para el control de personas se registran **únicamente los dos correos definidos**. No se requieren nombres, cargos, teléfonos u otros datos personales.

La documentación técnica, cambios, decisiones, validaciones, alertas y pendientes continúa en el README.

## Rutas de trabajo y de versión

El README y el registro viven en `02_censo`; los artefactos en construcción, en
`MCP_POWERBI\01_bi\01_versiones\01_kiro\[Nombre exacto BI]\`; la versión aprobada se guarda como versión nueva en
`01_versiones` según `01_rutas_y_censo.md` y se censa antes de cerrar el trabajo.
