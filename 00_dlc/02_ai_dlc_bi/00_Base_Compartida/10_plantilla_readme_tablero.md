# README — CONTROL E HISTÓRICO DEL TABLERO

> Crear al inicio y conservar durante toda la vida del tablero.

## 1. IDENTIFICACIÓN

| Campo | Información |
|---|---|
| Nombre exacto del tablero | [Nombre] |
| Tipo de trabajo actual | [Creación / Modificación / Depuración y Mejora] |
| Correo de quien trabaja/modifica | [correo] |
| Correo de quien solicita/es dueño | [correo] |
| Fecha de inicio | [AAAA-MM-DD] |
| Estado actual | [Estado] |
| Versión/referencia | [Versión] |
| CENSO de partida | [No aplica (creación nueva) / census_id con `vigencia` = VIGENTE y APTO] |
| Censo de cierre | [census_id del censo de la versión entregada / Pendiente] |
| Última actualización | [AAAA-MM-DD] |

## 2. RUTAS

- Este README y el censo: `MCP_POWERBI\02_censo\[Nombre exacto BI]\`
- Copia de trabajo: `MCP_POWERBI\01_bi\01_versiones\01_kiro\[Nombre exacto BI]\`
- Versión entregada: `MCP_POWERBI\01_bi\01_versiones\[versión]\[Nombre exacto BI]\` (`00_original` en Creación;
  `NN_<proceso>_<ID>` en Modificación y Depuración)

## 3. OBJETIVO DEL TRABAJO ACTUAL

[Descripción]

## 4. HISTÓRICO DE TRABAJOS

| Fecha | Tipo | Correo quien trabaja/modifica | Correo quien solicita/es dueño | Versión | Cambio realizado | Decisión | Estado |
|---|---|---|---|---|---|---|---|
| [AAAA-MM-DD] | [Tipo] | [correo] | [correo] | [vX] | [Cambio] | [Decisión] | [Estado] |

## 5. CAMBIOS REALIZADOS

### Solicitud
[Qué se pidió.]

### Cambios ejecutados
1. [Cambio]
2. [Cambio]

### Cambios no ejecutados
1. [Cambio / motivo]

## 6. DECISIONES

| Fecha | Decisión | Correo de quien tomó la decisión | Motivo |
|---|---|---|---|
| [AAAA-MM-DD] | [Decisión] | [correo] | [Motivo] |

## 7. VALIDACIONES

- [ ] Cambio solicitado validado.
- [ ] Dependencias revisadas.
- [ ] Integridad revisada.
- [ ] Visuales ocultos/marcadores revisados cuando aplique.
- [ ] Rendimiento revisado cuando aplique.
- [ ] Pruebas antes/después cuando aplique.
- [ ] Encoding/BOM validado cuando aplique.
- [ ] Alertas comunicadas.
- [ ] Pendientes documentados.

## 8. ALERTAS Y PENDIENTES

| Fecha | Tipo | Descripción | Correo responsable | Estado |
|---|---|---|---|---|
| [AAAA-MM-DD] | [Tipo] | [Descripción] | [correo] | [Estado] |

## 9. CIERRE

| Campo | Información |
|---|---|
| Fecha de cierre | [AAAA-MM-DD] |
| Correo de quien trabaja/modifica | [correo] |
| Estado final | [Entregado/Cerrado/Bloqueado] |
| Validación final | [Sí/No] |
| Pendientes | [Descripción / Ninguno] |

## 10. CONTINUIDAD

Cuando vuelva a trabajarse:
1. no crear otro README;
2. actualizar el correo de quien trabaja/modifica;
3. conservar el correo de quien solicita/es dueño;
4. agregar una nueva intervención al histórico;
5. documentar cambios, decisiones, validaciones y pendientes.
