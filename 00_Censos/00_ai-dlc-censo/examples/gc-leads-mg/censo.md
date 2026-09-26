# Ejemplo de censo — GC - Leads MG

> Este ejemplo está basado en el censo proporcionado del BI **GC - Leads MG**. Se conserva como ejemplo de salida del ritual y no representa una instrucción para modificar el BI.

# 1. Identificación

| Campo | Resultado |
|---|---|
| Nombre | GC - Leads MG |
| Proyecto | `GC - Leads MG.pbip` |
| Modelo | `GC - Leads MG.SemanticModel` |
| Reporte | `GC - Leads MG.Report` |
| Formato modelo | TMDL |
| Formato reporte | PBIR |
| Mercado identificado | Automotriz, MG, Perú |
| Fecha del censo | Según documento fuente |

# 2. Objetivo funcional

El reporte monitorea la gestión comercial de leads de la marca MG. Consolida leads provenientes de dos plataformas de captación/atención y mide volumen de leads y porcentaje gestionado, con análisis por tiempo, centro/sala, campaña, medio, asesor, estado y tipificación.

# 3. Fuentes

## Orbi Leads

Origen identificado:

`tatooine_prod_core.materialized_leads_tracking`

La información se filtra a marca MG.

## Atom

Orígenes identificados:

- `atom_leads.leads`
- `atom_leads.nebula_tiempos_de_agentes`

La información se relaciona con canales y tiempos de atención.

## Conexión

Amazon Athena vía ODBC con DSN `Athena_ODBC2`.

# 4. Modelo

## Tablas visibles/de negocio

- `General`
- `Calendario`
- `Medidas`
- `Parametros`

## Tablas de apoyo/staging

- `Orbi leads`
- `Atom`
- `Tel_Orbi`
- `Email_Orbi`

También se identifican tablas automáticas de fecha de Power BI.

# 5. Tabla central

`General` es una tabla calculada mediante `UNION` de Orbi y Atom.

Los registros de Atom se incorporan mediante una lógica de anti-join contra Orbi basada en teléfono o email dentro del mismo mes y año.

# 6. KPIs

| KPI | Definición resumida |
|---|---|
| Leads | Cantidad de `lead_id` distintos |
| Total Leads sin nuevos | Leads considerados gestionados según reglas distintas para Orbi y Atom |
| %Gestionados | Leads gestionados / Leads |

# 7. Elementos utilizados

Entre los campos utilizados por los visuales se identifican:

- `General[lead_id]`
- `General[Fuente]`
- `General[status_name]`
- `General[campaing_name]`
- `General[medium_value]`
- `General[category_name]`
- `General[brand_name]`
- `General[adviser_name]`
- `General[client_name]`
- `General[client_email]`
- `General[client_phone]`
- `General[centro2]`
- `General[tipificacion]`
- `General[Gestión]`
- `General[Tiempo de contacto]`
- `General[created_at]`
- `General[Action_name]`
- `Calendario[Año]`
- `Calendario[NombreMes]`
- `Calendario[Dia]`
- `Parametros[Parametro]`

# 8. Elementos no utilizados

El censo fuente identifica como no utilizados directamente en visuales varios campos de `General`, entre ellos:

- `adviser_email`
- `centro`
- `updated_at`
- `lead_created_at`
- `management_time`
- `nombre_origen`
- `grupo`
- `primer_usuario`
- `primer_grupo`

También se identifican tablas staging que no se exponen directamente en visuales y tablas auxiliares utilizadas como insumo de la lógica de deduplicación.

> La clasificación como "no utilizado" no implica que el elemento deba eliminarse; debe interpretarse dentro del contexto de este ritual.

# 9. Reglas de negocio identificadas

## Gestión Orbi

Se clasifica según el tiempo entre llegada y primera gestión:

- Mayor a 2 horas.
- Menor a 2 horas.

## Deduplicación Atom vs Orbi

Se construyen cruces por:

- Teléfono + mes + año.
- Email + mes + año.

Atom se incorpora cuando no existe coincidencia en Orbi.

## Estado Atom

El estado se deriva de condiciones relacionadas con:

- `atendido`
- `atencion`
- `tipificacion`

# 10. Relación principal

Se identifica una relación entre:

`General[Fecha] → Calendario[Fecha]`

con cardinalidad muchos a uno.

# 11. Páginas

Se identifican:

1. `General` — visible.
2. `Detalle` — oculta.
3. `Días` — oculta.
4. `Cita Agendada` — oculta.

# 12. Vacíos o puntos a validar

Ejemplos derivados del análisis:

| Punto | Motivo |
|---|---|
| Definición funcional exacta de algunos estados | La lógica técnica puede requerir confirmación funcional |
| Propietarios de las fuentes | No forma parte del inventario técnico disponible |
| Frecuencia/proceso operativo de actualización | Debe confirmarse si no está documentado en el proyecto |
| Propósito de algunos elementos no utilizados | Requiere validación funcional/técnica |

# 13. Propuestas de revisión IA

Las propuestas deben generarse únicamente cuando exista evidencia suficiente.

Ejemplos de categorías que el agente podría evaluar:

- Gobierno de fuentes.
- Definición funcional de KPIs.
- Granularidad.
- Dependencias.
- Reglas de deduplicación.
- Elementos automáticos de fecha.
- Campos sin uso.
- Responsables.
- Proceso de actualización.

# 14. Limitaciones

Este ejemplo conserva únicamente la información soportada por el censo suministrado. Cualquier dato no presente en el censo original debe permanecer como desconocido o pendiente de validación.

# 15. Resultado

El censo proporciona una visión técnica y funcional estructurada del BI y deja identificados:

- Componentes.
- Fuentes.
- Modelo.
- KPIs.
- Uso de campos.
- Elementos no utilizados.
- Reglas.
- Dependencias.
- Vacíos.
- Posibles puntos de revisión.

El ejemplo no contempla modificaciones al BI.
