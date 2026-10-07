# REGISTRO DE CAMBIO — AI-DLC

## Objetivo

Documentar de forma individual cada cambio realizado sobre un tablero,
permitiendo comparar el estado anterior con el estado posterior y dejar
trazabilidad de la decisión, dependencias, validación e impacto.

Este registro complementa el README histórico del tablero.

---

## 1. IDENTIFICACIÓN

| Campo | Información |
|---|---|
| Nombre exacto del tablero | [Nombre BI] |
| Tipo de trabajo | [Creación / Modificación / Depuración y Mejora] |
| Fecha | [AAAA-MM-DD] |
| Versión/referencia | [vX] |
| Correo de quien trabaja/modifica | [correo] |
| Correo de quien solicita/es dueño | [correo] |
| Estado del cambio | [Propuesto / Aprobado / En desarrollo / Validado / Rechazado] |

---

## 2. CAMBIO SOLICITADO

[Describir exactamente qué se solicitó.]

## 3. MOTIVO / OBJETIVO

[Por qué se requiere el cambio y qué se espera resolver.]

## 4. ESTADO ANTERIOR

### Elementos afectados

- [ ]
- [ ]
- [ ]

### Estado antes del cambio

[Describir cómo estaba el tablero antes de intervenir.]

### Evidencia / referencia

[Archivo, versión, captura, medida, consulta, página, visual u otra referencia.]

---

## 5. PROPUESTA DE CAMBIO

[Describir qué se propone modificar.]

### Alcance

Incluido:
- [ ]

No incluido:
- [ ]

---

## 6. DEPENDENCIAS AFECTADAS

| Elemento modificado | Depende de | Impacta a | Riesgo |
|---|---|---|---|
| [Elemento] | [Dependencia] | [Impacto] | [Bajo/Medio/Alto] |

Considerar cuando aplique:

- Fuentes.
- Consultas SQL.
- Power Query.
- Tablas.
- Columnas.
- Relaciones.
- Medidas.
- DAX.
- Filtros.
- KPIs.
- Visuales.
- Marcadores.
- Botones.
- Navegación.
- Estados alternativos.
- Otros elementos heredados.

---

## 7. DECISIÓN DEL ANALISTA

| Campo | Información |
|---|---|
| Decisión | [Aprobado / Rechazado / Pendiente] |
| Correo de quien toma la decisión | [correo] |
| Fecha | [AAAA-MM-DD] |
| Justificación | [Motivo] |

La IA no debe ejecutar cambios que requieran aprobación si el analista no los
ha aprobado.

---

## 8. CAMBIO REALIZADO

[Describir exactamente qué se modificó.]

### Elementos modificados

- [ ]
- [ ]
- [ ]

### Elementos no modificados

- [ ]
- [ ]

### Motivo de cualquier diferencia respecto a la propuesta

[Descripción]

---

## 9. ESTADO POSTERIOR

[Describir cómo quedó el tablero después del cambio.]

### Resultado

- [ ]
- [ ]
- [ ]

---

## 10. VALIDACIÓN ANTES / DESPUÉS

| Validación | Antes | Después | Resultado |
|---|---|---|---|
| KPI | [Valor/estado] | [Valor/estado] | [OK/Alerta] |
| Totales | [Valor/estado] | [Valor/estado] | [OK/Alerta] |
| Conteos | [Valor/estado] | [Valor/estado] | [OK/Alerta] |
| Filtros | [Estado] | [Estado] | [OK/Alerta] |
| Medidas | [Estado] | [Estado] | [OK/Alerta] |
| Relaciones | [Estado] | [Estado] | [OK/Alerta] |
| Visuales afectados | [Estado] | [Estado] | [OK/Alerta] |
| Rendimiento | [Medición] | [Medición] | [OK/Alerta] |

No todas las validaciones aplican a todos los cambios. Las que no apliquen
deben marcarse como "No aplica" y, cuando sea relevante, indicar por qué.

---

## 11. BENEFICIO / IMPACTO

### Beneficio esperado

[Qué mejora se esperaba obtener.]

### Beneficio/impacto observado

[Qué se obtuvo realmente después del cambio.]

### Impacto técnico

[Impacto en modelo, fuentes, rendimiento, mantenimiento u otros.]

### Impacto funcional

[Impacto para el usuario o proceso de negocio.]

---

## 12. ALERTAS Y PENDIENTES

| Tipo | Descripción | Correo responsable | Estado |
|---|---|---|---|
| [Bloqueante/Advertencia/Información] | [Descripción] | [correo] | [Pendiente/Cerrado] |

---

## 13. CIERRE DEL CAMBIO

| Campo | Información |
|---|---|
| Cambio validado | [Sí/No] |
| Fecha de validación | [AAAA-MM-DD] |
| Correo de quien trabaja/modifica | [correo] |
| Estado final | [Entregado/Cerrado/Bloqueado] |
| Pendientes | [Descripción / Ninguno] |

---

## 14. RELACIÓN CON EL HISTÓRICO

Este registro debe quedar relacionado con la intervención correspondiente en:

`NIGGA\01_bi\01_versiones\00_original\[Nombre exacto BI]\README.md`

El README conserva la historia acumulada del tablero; este documento conserva
el detalle específico del cambio.
