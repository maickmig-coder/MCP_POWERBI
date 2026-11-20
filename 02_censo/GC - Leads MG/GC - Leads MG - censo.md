# 0. Control obligatorio previo

- **Correo de quien realiza el CENSO:** miguel.b@nebula.com.co
- **Correo del dueño/responsable del tablero:** paola@nebula.com.co

Ambos correos se registraron antes de leer el PBIP (R02).

---

# Censo BI — GC - Leads MG

> Estado: Completado pendiente de validación
>
> census_id: 20261120T143932-gc-leads-mg
>
> Fecha y hora de ejecución: 2026-11-20T14:39:32-05:00
>
> Versión analizada: 00_original
>
> Huella del PBIP: sha256:5f864458fbcc520c079301b4fada4ab2493726dfa2b5be126725419f625ee8f7 (140 archivos)
>
> Tipo de CENSO: Inicial
>
> Versión del ritual: 2.3.10

Convenciones de todo el documento: los IDs son nativos y completos (CAT-15); `—` = no aplica o no disponible; las rutas de evidencia se indican una vez por tabla, relativas a la carpeta del BI. Cada dato aparece en un solo lugar; las demás secciones lo citan por su ID.

---

# 1. Identificación

| Campo | Valor |
|---|---|
| census_id | 20261120T143932-gc-leads-mg |
| census_id del censo anterior | No aplica |
| Nombre BI | GC - Leads MG |
| Archivo .pbip | GC - Leads MG.pbip |
| Área | Comercial / generación de leads de MG (marca MG, con salas en Perú) — Inferido: las consultas filtran la marca «MG» (RN18, RN19) y el tablero homologa salas de MG Perú (RN14); el PBIP no declara el área |
| Tecnología | Power BI PBIP — reporte PBIR, modelo TMDL, compatibilityLevel 1606 |
| Repositorio | No identificado en el PBIP |
| Ambiente | No identificado en el PBIP |
| Archivos de salida | `GC - Leads MG - censo.md`, `historial-censos.md` |

# 2. Objetivo y alcance

## 2.1 Objetivo del BI

Tablero de seguimiento de leads de MG que combina dos fuentes (Orbi y Atom, ambas consultadas en Athena) en la tabla `General`. Muestra el total de leads, cuántos están gestionados y el porcentaje (criterio de «gestionado» pendiente: V01), con desglose por centro, campaña, medio, estado y mes. Tiene una página visible (General) y tres ocultas a las que se llega con botones (Detalle, Días y Cita Agendada). El grano del dato es un lead (`lead_id`). Qué leads de Atom entran al tablero depende de una condición del SQL que no filtra como parece (H-A02). El público y el uso del tablero no están declarados en el PBIP: V04. Certeza: Inferido.

## 2.2 Pregunta central

¿Cuántos leads de MG entran, de qué campaña, medio y centro vienen, y qué porcentaje se ha gestionado? Certeza: Inferido; el uso de esa información está pendiente de confirmar (V04).

## 2.3 Alcance del censo

Lectura de solo lectura de todo el PBIP con `scripts/censo.py borrador`: modelo TMDL (tablas, columnas, medidas, relaciones, jerarquías, roles, particiones M), reporte PBIR (páginas, visuales, bindings, filtros, interacciones, bookmarks, botones, recursos y tema), contenido de las tablas embebidas y comparación de cada fuente con su estructura real en el catálogo de Athena (3.2). No incluye datos de las bases (filas), el servicio Power BI ni consumidores externos.

## 2.4 Fuentes inspeccionadas

| Elemento | Ruta | Objetos leídos |
|---|---|---:|
| Tablas TMDL | GC - Leads MG.SemanticModel/definition/tables/ | 26 |
| Relaciones | GC - Leads MG.SemanticModel/definition/relationships.tmdl | 18 |
| Roles | GC - Leads MG.SemanticModel/definition/roles/ | 0 |
| Páginas | GC - Leads MG.Report/definition/pages/ | 4 |
| Visuales | GC - Leads MG.Report/definition/pages/*/visuals/ | 91 |
| Bookmarks | GC - Leads MG.Report/definition/bookmarks/ | 2 |
| Recursos | GC - Leads MG.Report/StaticResources/ | 3 |

# 3. Fuentes de datos y conexiones

Todas las tablas del modelo con su origen: bases de datos, tablas escritas a mano (embebidas), tablas calculadas y tablas de fecha automáticas. 3.2 compara cada base con su estructura real; 3.3 muestra el contenido de las tablas embebidas; 3.4 detalla las tablas de fecha automáticas (R61–R63).

## 3.1 Fuentes y conexiones

Evidencia: particiones en `GC - Leads MG.SemanticModel/definition/tables/<Tabla>.tmdl`.

| fuente_id | Tabla del modelo | Partición | Modo | Tipo | Conector | Navegación |
|---|---|---|---|---|---|---|
| F01 | Atom | Atom | import | Origen (Value.NativeQuery) | AmazonAthena.Databases("Athena_ODBC2") · consulta SQL nativa (4.1; tablas que lee en 3.2) | — |
| F02 | Medidas | Medidas | import | Tabla embebida | Tabla embebida vacía (sin filas; 3.3) | — |
| F03 | Orbi leads | Orbi leads | import | Origen (Value.NativeQuery) | AmazonAthena.Databases("Athena_ODBC2") · consulta SQL nativa (4.3; tablas que lee en 3.2) | — |
| F04 | Parametros | Parametros | import | Origen (DateTimeZone.SwitchZone) | DateTimeZone.SwitchZone | — |
| F05 | Calendario | Calendario | import | Tabla calculada DAX | Expresión DAX (6.1) | Lee: General |
| F06 | Email_Orbi | Email_Orbi | import | Tabla calculada DAX | Expresión DAX (6.1) | Lee: Orbi leads |
| F07 | General | General | import | Tabla calculada DAX | Expresión DAX (6.1) | Lee: Atom, Orbi leads |
| F08 | Tel_Orbi | Tel_Orbi | import | Tabla calculada DAX | Expresión DAX (6.1) | Lee: Orbi leads |
| F09 | DateTableTemplate_6e965017-0446-4f64-9716-c00440e09d6a | DateTableTemplate_6e965017-0446-4f64-9716-c00440e09d6a | import | Tabla de fecha automática (Power BI) | Calendario DAX (3.4) | Plantilla (sin relación) |
| F10 | LocalDateTable_02a5d6a9-c380-4732-ab95-b5cc6fa07be3 | LocalDateTable_02a5d6a9-c380-4732-ab95-b5cc6fa07be3 | import | Tabla de fecha automática (Power BI) | Calendario DAX (3.4) | Fechas de Orbi leads[lead_created_at] |
| F11 | LocalDateTable_2a4febd5-474e-4a78-a1c4-4e33331cca51 | LocalDateTable_2a4febd5-474e-4a78-a1c4-4e33331cca51 | import | Tabla de fecha automática (Power BI) | Calendario DAX (3.4) | Fechas de Orbi leads[updated_at] |
| F12 | LocalDateTable_306883ba-3073-45e4-959f-c41701d22ad2 | LocalDateTable_306883ba-3073-45e4-959f-c41701d22ad2 | import | Tabla de fecha automática (Power BI) | Calendario DAX (3.4) | Fechas de Atom[ultima_actualizacion] |
| F13 | LocalDateTable_4069fc95-3b04-44b7-a146-e17eef31c965 | LocalDateTable_4069fc95-3b04-44b7-a146-e17eef31c965 | import | Tabla de fecha automática (Power BI) | Calendario DAX (3.4) | Fechas de Atom[lead_created_at] |
| F14 | LocalDateTable_52673d88-0ab9-49ce-886d-f5eade869640 | LocalDateTable_52673d88-0ab9-49ce-886d-f5eade869640 | import | Tabla de fecha automática (Power BI) | Calendario DAX (3.4) | Fechas de Atom[updated_at] |
| F15 | LocalDateTable_530313b0-a966-4706-9493-c8aa7a57a317 | LocalDateTable_530313b0-a966-4706-9493-c8aa7a57a317 | import | Tabla de fecha automática (Power BI) | Calendario DAX (3.4) | Fechas de Orbi leads[created_at] |
| F16 | LocalDateTable_66ac448c-938c-4528-8816-11b3e54e1806 | LocalDateTable_66ac448c-938c-4528-8816-11b3e54e1806 | import | Tabla de fecha automática (Power BI) | Calendario DAX (3.4) | Fechas de Atom[fecha_asignacion] |
| F17 | LocalDateTable_6c8c7523-345e-4ed0-a647-84ec42e712b8 | LocalDateTable_6c8c7523-345e-4ed0-a647-84ec42e712b8 | import | Tabla de fecha automática (Power BI) | Calendario DAX (3.4) | Fechas de Atom[fh_primer_mensaje_agente] |
| F18 | LocalDateTable_80504aa4-9389-4877-8ef1-49d7106673de | LocalDateTable_80504aa4-9389-4877-8ef1-49d7106673de | import | Tabla de fecha automática (Power BI) | Calendario DAX (3.4) | Fechas de General[lead_created_at] |
| F19 | LocalDateTable_8be1e938-b325-4949-a52e-399605e1608d | LocalDateTable_8be1e938-b325-4949-a52e-399605e1608d | import | Tabla de fecha automática (Power BI) | Calendario DAX (3.4) | Fechas de Atom[created_at] |
| F20 | LocalDateTable_8c71bff9-1618-4d4c-8f78-b3f67e1ab247 | LocalDateTable_8c71bff9-1618-4d4c-8f78-b3f67e1ab247 | import | Tabla de fecha automática (Power BI) | Calendario DAX (3.4) | Fechas de Parametros[Parametro] |
| F21 | LocalDateTable_9fb14d92-4303-4911-982e-f5fdddc298ba | LocalDateTable_9fb14d92-4303-4911-982e-f5fdddc298ba | import | Tabla de fecha automática (Power BI) | Calendario DAX (3.4) | Fechas de General[updated_at] |
| F22 | LocalDateTable_a107470f-adba-4dc8-9806-9431dde3512b | LocalDateTable_a107470f-adba-4dc8-9806-9431dde3512b | import | Tabla de fecha automática (Power BI) | Calendario DAX (3.4) | Fechas de Orbi leads[fecha_primera_gestion] |
| F23 | LocalDateTable_b86e5576-bfb4-4b10-b5fa-45ffc94d79d7 | LocalDateTable_b86e5576-bfb4-4b10-b5fa-45ffc94d79d7 | import | Tabla de fecha automática (Power BI) | Calendario DAX (3.4) | Fechas de Calendario[Fecha] |
| F24 | LocalDateTable_ccea026a-6cac-48f0-9da6-b4a61589cbe0 | LocalDateTable_ccea026a-6cac-48f0-9da6-b4a61589cbe0 | import | Tabla de fecha automática (Power BI) | Calendario DAX (3.4) | Fechas de Orbi leads[fecha_llegada] |
| F25 | LocalDateTable_e82a7ec6-9aa0-496b-af4f-4da25dcd928c | LocalDateTable_e82a7ec6-9aa0-496b-af4f-4da25dcd928c | import | Tabla de fecha automática (Power BI) | Calendario DAX (3.4) | Fechas de Orbi leads[Fecha] |
| F26 | LocalDateTable_f0a84349-d002-49a8-8ee5-86e0d9550369 | LocalDateTable_f0a84349-d002-49a8-8ee5-86e0d9550369 | import | Tabla de fecha automática (Power BI) | Calendario DAX (3.4) | Fechas de Atom[Fecha] |

El código M completo de cada consulta está en la sección 4.

**Parámetros M:** No aplica (sin `expressions.tmdl`).

Credenciales: el PBIP no contiene credenciales; no se registran (R06). Frecuencia de actualización y propietario: ver sección 16.

## 3.2 Estructura real de las fuentes

Catálogo de Athena: diccionario-datos.md (654 tablas), configurado en `00_dlc/00_diccionario_datos/config.json`. Es una copia del catálogo; si está desactualizado, una columna puede figurar como «No está en el catálogo» sin que falte en la base.

### Atom

Consulta SQL nativa (texto completo en 4.1). Lee 2 tabla(s): `atom_leads.leads` (32 columnas en el catálogo); `atom_leads.nebula_tiempos_de_agentes` (17 columnas en el catálogo). Cada columna que el tablero carga se busca en esas tablas. Resultado: Igual 13, No está en las tablas leídas 14, Se crea en Power Query 1.

| Tabla leída | Columna en la base | Tipo real | Columna en el tablero | Tipo en el tablero | Resultado | Posible dato personal |
|---|---|---|---|---|---|---|
| atom_leads.leads | lead_id | string | Atom[lead_id] | string | Igual (también en atom_leads.nebula_tiempos_de_agentes) | — |
| — | campaing_name | — | Atom[campaing_name] | string | No está en las tablas leídas: se calcula o renombra en el SQL | — |
| — | medium_value | — | Atom[medium_value] | string | No está en las tablas leídas: se calcula o renombra en el SQL | — |
| — | category_name | — | Atom[category_name] | string | No está en las tablas leídas: se calcula o renombra en el SQL | — |
| — | brand_name | — | Atom[brand_name] | string | No está en las tablas leídas: se calcula o renombra en el SQL | — |
| — | adviser_name | — | Atom[adviser_name] | string | No está en las tablas leídas: se calcula o renombra en el SQL | — |
| — | adviser_email | — | Atom[adviser_email] | string | No está en las tablas leídas: se calcula o renombra en el SQL | Sí (por el nombre) |
| — | client_name | — | Atom[client_name] | string | No está en las tablas leídas: se calcula o renombra en el SQL | — |
| — | client_phone | — | Atom[client_phone] | string | No está en las tablas leídas: se calcula o renombra en el SQL | — |
| — | client_email | — | Atom[client_email] | string | No está en las tablas leídas: se calcula o renombra en el SQL | Sí (por el nombre) |
| — | created_at | — | Atom[created_at] | dateTime | No está en las tablas leídas: se calcula o renombra en el SQL | — |
| — | updated_at | — | Atom[updated_at] | dateTime | No está en las tablas leídas: se calcula o renombra en el SQL | — |
| — | lead_created_at | — | Atom[lead_created_at] | dateTime | No está en las tablas leídas: se calcula o renombra en el SQL | — |
| — | management_time | — | Atom[management_time] | double | No está en las tablas leídas: se calcula o renombra en el SQL | — |
| atom_leads.leads | nombre_origen | string | Atom[nombre_origen] | string | Igual | — |
| atom_leads.leads | grupo | string | Atom[grupo] | string | Igual (también en atom_leads.nebula_tiempos_de_agentes) | — |
| atom_leads.leads | primer_usuario | string | Atom[primer_usuario] | string | Igual | — |
| atom_leads.leads | primer_grupo | string | Atom[primer_grupo] | string | Igual | — |
| atom_leads.leads | tipificacion | string | Atom[tipificacion] | string | Igual | — |
| atom_leads.nebula_tiempos_de_agentes | atencion | string | Atom[atencion] | string | Igual | — |
| atom_leads.leads | atendido | string | Atom[atendido] | string | Igual | — |
| — | — | — | Atom[Fecha] | dateTime | Se crea en Power Query: copia de «lead_created_at» | — |
| atom_leads.leads | ultima_actualizacion | timestamp | Atom[ultima_actualizacion] | dateTime | Igual (también en atom_leads.nebula_tiempos_de_agentes) | — |
| atom_leads.leads | fecha_asignacion | timestamp | Atom[fecha_asignacion] | dateTime | Igual | — |
| atom_leads.leads | asignado | string | Atom[asignado] | string | Igual | — |
| atom_leads.leads | canal | string | Atom[canal] | string | Igual | — |
| atom_leads.leads | fh_primer_mensaje_agente | timestamp | Atom[fh_primer_mensaje_agente] | dateTime | Igual (también en atom_leads.nebula_tiempos_de_agentes) | — |
| — | fh_asignacion_primera | — | Atom[fh_asignacion_primera] | string | No está en las tablas leídas: se calcula o renombra en el SQL | — |

### Orbi leads

Consulta SQL nativa (texto completo en 4.3). Lee 1 tabla(s): `tatooine_prod_core.materialized_leads_tracking` (44 columnas en el catálogo). Cada columna que el tablero carga se busca en esas tablas. Resultado: Igual 44, Se crea en Power Query 1, No está en las tablas leídas 4.

| Tabla leída | Columna en la base | Tipo real | Columna en el tablero | Tipo en el tablero | Resultado | Posible dato personal |
|---|---|---|---|---|---|---|
| tatooine_prod_core.materialized_leads_tracking | id | bigint | Orbi leads[id] | int64 | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | clasification_id | bigint | Orbi leads[clasification_id] | int64 | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | clasification_name | string | Orbi leads[clasification_name] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | action_id | bigint | Orbi leads[action_id] | int64 | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | action_name | string | Orbi leads[action_name] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | status_id | bigint | Orbi leads[status_id] | int64 | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | status_name | string | Orbi leads[status_name] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | campaing_id | bigint | Orbi leads[campaing_id] | int64 | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | campaing_name | string | Orbi leads[campaing_name] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | channel_id | bigint | Orbi leads[channel_id] | int64 | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | channel_value | string | Orbi leads[channel_value] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | medium_id | bigint | Orbi leads[medium_id] | int64 | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | medium_value | string | Orbi leads[medium_value] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | category_id | bigint | Orbi leads[category_id] | int64 | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | category_name | string | Orbi leads[category_name] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | country_name | string | Orbi leads[country_name] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | company_id | bigint | Orbi leads[company_id] | int64 | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | company_name | string | Orbi leads[company_name] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | brand_id | bigint | Orbi leads[brand_id] | int64 | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | brand_name | string | Orbi leads[brand_name] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | wholesaler | smallint | Orbi leads[wholesaler] | int64 | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | adviser_id | bigint | Orbi leads[adviser_id] | int64 | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | adviser_name | string | Orbi leads[adviser_name] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | adviser_email | string | Orbi leads[adviser_email] | string | Igual | Sí (por el nombre) |
| tatooine_prod_core.materialized_leads_tracking | adviser_document_type | string | Orbi leads[adviser_document_type] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | adviser_document_number | string | Orbi leads[adviser_document_number] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | concessionaire_id | bigint | Orbi leads[concessionaire_id] | int64 | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | concessionaire_names | string | Orbi leads[concessionaire_names] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | client_name | string | Orbi leads[client_name] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | client_phone | string | Orbi leads[client_phone] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | client_email | string | Orbi leads[client_email] | string | Igual | Sí (por el nombre) |
| tatooine_prod_core.materialized_leads_tracking | client_document_type_name | string | Orbi leads[client_document_type_name] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | client_document_number | string | Orbi leads[client_document_number] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | model_id | bigint | Orbi leads[model_id] | int64 | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | model_name | string | Orbi leads[model_name] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | model_year | string | Orbi leads[model_year] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | license_plate | string | Orbi leads[license_plate] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | created_at | timestamp | Orbi leads[created_at] | dateTime | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | updated_at | timestamp | Orbi leads[updated_at] | dateTime | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | lead_created_at | timestamp | Orbi leads[lead_created_at] | dateTime | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | management_time | int | Orbi leads[management_time] | int64 | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | adviser_business_type_id | bigint | Orbi leads[adviser_business_type_id] | int64 | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | adviser_business_type | string | Orbi leads[adviser_business_type] | string | Igual | — |
| tatooine_prod_core.materialized_leads_tracking | lead_id | bigint | Orbi leads[lead_id] | int64 | Igual | — |
| — | — | — | Orbi leads[Fecha] | dateTime | Se crea en Power Query: copia de «lead_created_at» | — |
| — | lead_id2 | — | Orbi leads[lead_id2] | int64 | No está en las tablas leídas: se calcula o renombra en el SQL | — |
| — | fecha_llegada | — | Orbi leads[fecha_llegada] | dateTime | No está en las tablas leídas: se calcula o renombra en el SQL | — |
| — | fecha_primera_gestion | — | Orbi leads[fecha_primera_gestion] | dateTime | No está en las tablas leídas: se calcula o renombra en el SQL | — |
| — | segundos_hasta_gestion | — | Orbi leads[segundos_hasta_gestion] | int64 | No está en las tablas leídas: se calcula o renombra en el SQL | — |

## 3.3 Contenido de las tablas embebidas

### Medidas

Evidencia: `GC - Leads MG.SemanticModel/definition/tables/Medidas.tmdl`. Tabla vacía (0 filas): no tiene contenido que validar. El modelo la usa para agrupar 3 medida(s) (sección 7).

## 3.4 Tablas de fecha automáticas

Las crea Power BI por cada columna de fecha cuando la inteligencia de tiempo automática está activa (5.4); no vienen de una base. Cada una cubre los años completos entre la fecha mínima y la máxima de su columna de origen. Columnas e IDs en 6.2.

| Tabla | Columna de fecha que la origina | Rango (expresión DAX) | Columnas | Estado de uso de sus columnas |
|---|---|---|---:|---|
| DateTableTemplate_6e965017-0446-4f64-9716-c00440e09d6a | Plantilla (sin relación) | `Calendar(Date(2015,1,1), Date(2015,1,1))` | 7 | En uso 3, Uso técnico 4 |
| LocalDateTable_02a5d6a9-c380-4732-ab95-b5cc6fa07be3 | Orbi leads[lead_created_at] | `Calendar(Date(Year(MIN('Orbi leads'[lead_created_at])), 1, 1), Date(Year(MAX('Orbi leads'[lead_created_at])), 12, 31))` | 7 | En uso 3, Uso técnico 4 |
| LocalDateTable_2a4febd5-474e-4a78-a1c4-4e33331cca51 | Orbi leads[updated_at] | `Calendar(Date(Year(MIN('Orbi leads'[updated_at])), 1, 1), Date(Year(MAX('Orbi leads'[updated_at])), 12, 31))` | 7 | En uso 3, Uso técnico 4 |
| LocalDateTable_306883ba-3073-45e4-959f-c41701d22ad2 | Atom[ultima_actualizacion] | `Calendar(Date(Year(MIN('Atom'[ultima_actualizacion])), 1, 1), Date(Year(MAX('Atom'[ultima_actualizacion])), 12, 31))` | 7 | En uso 3, Uso técnico 4 |
| LocalDateTable_4069fc95-3b04-44b7-a146-e17eef31c965 | Atom[lead_created_at] | `Calendar(Date(Year(MIN('Atom'[lead_created_at])), 1, 1), Date(Year(MAX('Atom'[lead_created_at])), 12, 31))` | 7 | En uso 3, Uso técnico 4 |
| LocalDateTable_52673d88-0ab9-49ce-886d-f5eade869640 | Atom[updated_at] | `Calendar(Date(Year(MIN('Atom'[updated_at])), 1, 1), Date(Year(MAX('Atom'[updated_at])), 12, 31))` | 7 | En uso 3, Uso técnico 4 |
| LocalDateTable_530313b0-a966-4706-9493-c8aa7a57a317 | Orbi leads[created_at] | `Calendar(Date(Year(MIN('Orbi leads'[created_at])), 1, 1), Date(Year(MAX('Orbi leads'[created_at])), 12, 31))` | 7 | En uso 3, Uso técnico 4 |
| LocalDateTable_66ac448c-938c-4528-8816-11b3e54e1806 | Atom[fecha_asignacion] | `Calendar(Date(Year(MIN('Atom'[fecha_asignacion])), 1, 1), Date(Year(MAX('Atom'[fecha_asignacion])), 12, 31))` | 7 | En uso 3, Uso técnico 4 |
| LocalDateTable_6c8c7523-345e-4ed0-a647-84ec42e712b8 | Atom[fh_primer_mensaje_agente] | `Calendar(Date(Year(MIN('Atom'[fh_primer_mensaje_agente])), 1, 1), Date(Year(MAX('Atom'[fh_primer_mensaje_agente])), 12, 31))` | 7 | En uso 3, Uso técnico 4 |
| LocalDateTable_80504aa4-9389-4877-8ef1-49d7106673de | General[lead_created_at] | `Calendar(Date(Year(MIN('General'[lead_created_at])), 1, 1), Date(Year(MAX('General'[lead_created_at])), 12, 31))` | 7 | En uso 3, Uso técnico 4 |
| LocalDateTable_8be1e938-b325-4949-a52e-399605e1608d | Atom[created_at] | `Calendar(Date(Year(MIN('Atom'[created_at])), 1, 1), Date(Year(MAX('Atom'[created_at])), 12, 31))` | 7 | En uso 3, Uso técnico 4 |
| LocalDateTable_8c71bff9-1618-4d4c-8f78-b3f67e1ab247 | Parametros[Parametro] | `Calendar(Date(Year(MIN('Parametros'[Parametro])), 1, 1), Date(Year(MAX('Parametros'[Parametro])), 12, 31))` | 7 | En uso 3, Uso técnico 4 |
| LocalDateTable_9fb14d92-4303-4911-982e-f5fdddc298ba | General[updated_at] | `Calendar(Date(Year(MIN('General'[updated_at])), 1, 1), Date(Year(MAX('General'[updated_at])), 12, 31))` | 7 | En uso 3, Uso técnico 4 |
| LocalDateTable_a107470f-adba-4dc8-9806-9431dde3512b | Orbi leads[fecha_primera_gestion] | `Calendar(Date(Year(MIN('Orbi leads'[fecha_primera_gestion])), 1, 1), Date(Year(MAX('Orbi leads'[fecha_primera_gestion])), 12, 31))` | 7 | En uso 3, Uso técnico 4 |
| LocalDateTable_b86e5576-bfb4-4b10-b5fa-45ffc94d79d7 | Calendario[Fecha] | `Calendar(Date(Year(MIN('Calendario'[Fecha])), 1, 1), Date(Year(MAX('Calendario'[Fecha])), 12, 31))` | 7 | En uso 3, Uso técnico 4 |
| LocalDateTable_ccea026a-6cac-48f0-9da6-b4a61589cbe0 | Orbi leads[fecha_llegada] | `Calendar(Date(Year(MIN('Orbi leads'[fecha_llegada])), 1, 1), Date(Year(MAX('Orbi leads'[fecha_llegada])), 12, 31))` | 7 | En uso 3, Uso técnico 4 |
| LocalDateTable_e82a7ec6-9aa0-496b-af4f-4da25dcd928c | Orbi leads[Fecha] | `Calendar(Date(Year(MIN('Orbi leads'[Fecha])), 1, 1), Date(Year(MAX('Orbi leads'[Fecha])), 12, 31))` | 7 | En uso 3, Uso técnico 4 |
| LocalDateTable_f0a84349-d002-49a8-8ee5-86e0d9550369 | Atom[Fecha] | `Calendar(Date(Year(MIN('Atom'[Fecha])), 1, 1), Date(Year(MAX('Atom'[Fecha])), 12, 31))` | 7 | En uso 3, Uso técnico 4 |

# 4. Transformaciones (Power Query/M)

El código M completo de cada consulta está aquí una sola vez. Los renombres y tipos finales por columna están en la Matriz A (columnas «Nombre en origen» y «Tipo»), no se repiten en la tabla de pasos.

## 4.1 Atom (partición `Atom`, 14 pasos)

Evidencia: `GC - Leads MG.SemanticModel/definition/tables/Atom.tmdl`.

```m
let
    Origen = Value.NativeQuery(AmazonAthena.Databases("Athena_ODBC2", null, []){[Kind="Database"]}[Data], "[[SQL de 3707 caracteres: ver «Consulta SQL» debajo]]", null, [EnableFolding=true]),
    #"Texto recortado" = Table.TransformColumns(Origen,{{"client_email", Text.Trim, type text}, {"client_phone", Text.Trim, type text}}),
    #"Texto en minúsculas" = Table.TransformColumns(#"Texto recortado",{{"client_email", Text.Lower, type text}}),
    #"Poner En Mayúsculas Cada Palabra" = Table.TransformColumns(#"Texto en minúsculas",{{"adviser_name", Text.Proper, type text}, {"category_name", Text.Proper, type text}}),
    #"Valor reemplazado" = Table.ReplaceValue(#"Poner En Mayúsculas Cada Palabra",".",",",Replacer.ReplaceText,{"management_time"}),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Valor reemplazado",{{"management_time", type number}}),
    #"Columna duplicada" = Table.DuplicateColumn(#"Tipo cambiado", "lead_created_at", "lead_created_at - Copia"),
    #"Columnas con nombre cambiado" = Table.RenameColumns(#"Columna duplicada",{{"lead_created_at - Copia", "Fecha"}}),
    #"Tipo cambiado1" = Table.TransformColumnTypes(#"Columnas con nombre cambiado",{{"Fecha", type date}}),
    #"Poner En Mayúsculas Cada Palabra1" = Table.TransformColumns(#"Tipo cambiado1",{{"campaing_name", Text.Proper, type text}}),
    #"Valor reemplazado1" = Table.ReplaceValue(#"Poner En Mayúsculas Cada Palabra1","T"," ",Replacer.ReplaceText,{"created_at"}),
    #"Tipo cambiado2" = Table.TransformColumnTypes(#"Valor reemplazado1",{{"created_at", type datetime}}),
    #"Valor reemplazado2" = Table.ReplaceValue(#"Tipo cambiado2","T"," ",Replacer.ReplaceText,{"fh_primer_mensaje_agente"}),
    #"Tipo cambiado3" = Table.TransformColumnTypes(#"Valor reemplazado2",{{"fh_primer_mensaje_agente", type datetime}})
in
    #"Tipo cambiado3"
```

Consulta SQL (texto completo de la consulta nativa):

```sql
select distinct
lead_id
,campaing_name
,medium_value
,category_name
,brand_name
,adviser_name
,adviser_email
,client_name
,client_phone
,client_email
,created_at
,updated_at
,lead_created_at
,management_time
,nombre_origen
,grupo
,atencion
,primer_usuario
,primer_grupo
,tipificacion
,atendido
,ultima_actualizacion
,fecha_asignacion
,asignado
,canal
,fh_primer_mensaje_agente
,fh_asignacion_primera
from
(select
 lead_id
,upper(nombre_campania) as campaing_name
,case when trim(split_part(canal, '-', 1))='WA' then 'Whatsapp'  
      when trim(split_part(canal, '-', 1))='IG' then 'Redes Sociales'
      when trim(split_part(canal, '-', 1))='FB' then 'Redes Sociales'
      end as medium_value
,case when lower(customtipodenegocio)='taller' then 'Posventa' when trim(customtipodenegocio) = '' then 'Sin definir' else customtipodenegocio end as category_name
,case when canal2 <> '' then 'MG' else null end as brand_name
,b.agente as adviser_name
,b.email_agente as adviser_email
,nombre_cliente as client_name
,telefono as client_phone
,correo as client_email
,b.fh_asignacion as created_at
,b.ultima_actualizacion2 as updated_at
,fecha_inicio_conversacion as lead_created_at
,b.tiempo_de_atencion as management_time
,nombre_origen
,b.grupo
,b.atencion
,primer_usuario
,primer_grupo
,tipificacion
,atendido
,ultima_actualizacion
,fecha_asignacion
,asignado
,canal
,b.fh_primer_mensaje_agente
,b.fh_asignacion_primera
from atom_leads.leads

-- Canal MG
left join
(select distinct
canal as canal2
from atom_leads.leads
where (upper(nombre_campania) like '%MG%' or upper(grupo) like '%MG%') and (lower(canal) like '%MG%' or lower(canal) like '%+%')
) m
on canal2 = canal

--Ultima Gestion
left join
(select distinct
*
from
(select distinct
 LAST_VALUE(grupo)                  OVER (PARTITION BY lead_id ORDER BY fh_asignacion asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as grupo
,LAST_VALUE(agente)                 OVER (PARTITION BY lead_id ORDER BY fh_asignacion asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as agente
,LAST_VALUE(email_agente)           OVER (PARTITION BY lead_id ORDER BY fh_asignacion asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as email_agente
,LAST_VALUE(fh_asignacion)          OVER (PARTITION BY lead_id ORDER BY fh_asignacion asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as fh_asignacion
,LAST_VALUE(fh_asignacion)          OVER (PARTITION BY lead_id ORDER BY fh_asignacion desc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as fh_asignacion_primera
,LAST_VALUE(channel_name)           OVER (PARTITION BY lead_id ORDER BY fh_asignacion asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as channel_name
,LAST_VALUE(tiempo_de_atencion)     OVER (PARTITION BY lead_id ORDER BY fh_asignacion asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as tiempo_de_atencion
,LAST_VALUE(ultima_actualizacion)   OVER (PARTITION BY lead_id ORDER BY fh_asignacion asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as ultima_actualizacion2
,LAST_VALUE(atencion)               OVER (PARTITION BY lead_id ORDER BY fh_asignacion asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as atencion
,LAST_VALUE(categoria_atencion)     OVER (PARTITION BY lead_id ORDER BY fh_asignacion asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as categoria_atencion
,LAST_VALUE(fh_primer_mensaje_agente)     OVER (PARTITION BY lead_id ORDER BY fh_primer_mensaje_agente desc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as fh_primer_mensaje_agente
,lead_id as lead_id2
from atom_leads.nebula_tiempos_de_agentes)a)b
on lead_id2 = lead_id
)a
where not brand_name is null
```

| # | Paso | Operación | Columnas afectadas |
|---:|---|---|---|
| 1 | Origen | Origen (Value.NativeQuery) | Data |
| 2 | Texto recortado | Transformación de columnas | client_email, client_phone |
| 3 | Texto en minúsculas | Transformación de columnas | client_email |
| 4 | Poner En Mayúsculas Cada Palabra | Transformación de columnas | adviser_name, category_name |
| 5 | Valor reemplazado | Reemplazo de valores | — |
| 6 | Tipo cambiado | Cambio de tipo | 1 cambio(s) de tipo: management_time |
| 7 | Columna duplicada | Duplicar columna | — |
| 8 | Columnas con nombre cambiado | Renombrado | 1 renombre(s) |
| 9 | Tipo cambiado1 | Cambio de tipo | 1 cambio(s) de tipo: Fecha |
| 10 | Poner En Mayúsculas Cada Palabra1 | Transformación de columnas | campaing_name |
| 11 | Valor reemplazado1 | Reemplazo de valores | — |
| 12 | Tipo cambiado2 | Cambio de tipo | 1 cambio(s) de tipo: created_at |
| 13 | Valor reemplazado2 | Reemplazo de valores | — |
| 14 | Tipo cambiado3 | Cambio de tipo | 1 cambio(s) de tipo: fh_primer_mensaje_agente |

## 4.2 Medidas (partición `Medidas`, 3 pasos)

Evidencia: `GC - Leads MG.SemanticModel/definition/tables/Medidas.tmdl`.

```m
let
    Origen = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Columna1 = _t]),
    #"Tipo cambiado" = Table.TransformColumnTypes(Origen,{{"Columna1", type text}}),
    #"Columnas quitadas" = Table.RemoveColumns(#"Tipo cambiado",{"Columna1"})
in
    #"Columnas quitadas"
```

| # | Paso | Operación | Columnas afectadas |
|---:|---|---|---|
| 1 | Origen | Tabla embebida | — |
| 2 | Tipo cambiado | Cambio de tipo | 1 cambio(s) de tipo: Columna1 |
| 3 | Columnas quitadas | Eliminación de columnas | Elimina: Tipo cambiado, Columna1 |

## 4.3 Orbi leads (partición `Orbi leads`, 11 pasos)

Evidencia: `GC - Leads MG.SemanticModel/definition/tables/Orbi leads.tmdl`.

```m
let
    Origen = Value.NativeQuery(AmazonAthena.Databases("Athena_ODBC2", null, []){[Kind="Database"]}[Data], "[[SQL de 7652 caracteres: ver «Consulta SQL» debajo]]", null, [EnableFolding=true]),
    #"Texto recortado" = Table.TransformColumns(Origen,{{"client_email", Text.Trim, type text}, {"client_phone", Text.Trim, type text}}),
    #"Texto en minúsculas" = Table.TransformColumns(#"Texto recortado",{{"client_email", Text.Lower, type text}}),
    #"Valor reemplazado" = Table.ReplaceValue(#"Texto en minúsculas","+","",Replacer.ReplaceText,{"client_phone"}),
    #"Valor reemplazado1" = Table.ReplaceValue(#"Valor reemplazado","-","",Replacer.ReplaceText,{"client_phone"}),
    #"Valor reemplazado2" = Table.ReplaceValue(#"Valor reemplazado1"," ","",Replacer.ReplaceText,{"client_phone"}),
    #"Poner En Mayúsculas Cada Palabra" = Table.TransformColumns(#"Valor reemplazado2",{{"adviser_name", Text.Proper, type text}, {"category_name", Text.Proper, type text}}),
    #"Columna duplicada" = Table.DuplicateColumn(#"Poner En Mayúsculas Cada Palabra", "lead_created_at", "lead_created_at - Copia"),
    #"Columnas con nombre cambiado" = Table.RenameColumns(#"Columna duplicada",{{"lead_created_at - Copia", "Fecha"}}),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Columnas con nombre cambiado",{{"Fecha", type date}}),
    #"Poner En Mayúsculas Cada Palabra1" = Table.TransformColumns(#"Tipo cambiado",{{"campaing_name", Text.Proper, type text}})
in
    #"Poner En Mayúsculas Cada Palabra1"
```

Consulta SQL (texto completo de la consulta nativa):

```sql
select distinct
*
from
(select distinct
 LAST_VALUE(id)                        OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as id
,LAST_VALUE(clasification_id)          OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as clasification_id
,LAST_VALUE(clasification_name)        OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as clasification_name
,LAST_VALUE(action_id)                 OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as action_id
,LAST_VALUE(action_name)               OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as action_name
,LAST_VALUE(status_id)                 OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as status_id
,LAST_VALUE(status_name)               OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as status_name
,LAST_VALUE(campaing_id)               OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as campaing_id
,LAST_VALUE(campaing_name)             OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as campaing_name
,LAST_VALUE(channel_id)                OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as channel_id
,LAST_VALUE(channel_value)             OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as channel_value
,LAST_VALUE(medium_id)                 OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as medium_id
,LAST_VALUE(medium_value)              OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as medium_value
,LAST_VALUE(category_id)               OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as category_id
,LAST_VALUE(category_name)             OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as category_name
,LAST_VALUE(country_name)              OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as country_name
,LAST_VALUE(company_id)                OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as company_id
,LAST_VALUE(company_name)              OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as company_name
,LAST_VALUE(brand_id)                  OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as brand_id
,LAST_VALUE(brand_name)                OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as brand_name
,LAST_VALUE(wholesaler)                OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as wholesaler
,LAST_VALUE(adviser_id)                OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as adviser_id
,LAST_VALUE(adviser_name)              OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as adviser_name
,LAST_VALUE(adviser_email)             OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as adviser_email
,LAST_VALUE(adviser_document_type)     OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as adviser_document_type
,LAST_VALUE(adviser_document_number)   OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as adviser_document_number
,LAST_VALUE(concessionaire_id)         OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as concessionaire_id
,LAST_VALUE(concessionaire_names)      OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as concessionaire_names
,LAST_VALUE(client_name)               OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as client_name
,LAST_VALUE(client_phone)              OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as client_phone
,LAST_VALUE(client_email)              OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as client_email
,LAST_VALUE(client_document_type_name) OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as client_document_type_name
,LAST_VALUE(client_document_number)    OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as client_document_number
,LAST_VALUE(model_id)                  OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as model_id
,LAST_VALUE(model_name)                OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as model_name
,LAST_VALUE(model_year)                OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as model_year
,LAST_VALUE(license_plate)             OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as license_plate
,LAST_VALUE(created_at)                OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as created_at
,LAST_VALUE(updated_at)                OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as updated_at
,LAST_VALUE(lead_created_at)           OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as lead_created_at
,LAST_VALUE(management_time)           OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as management_time
,LAST_VALUE(adviser_business_type_id)  OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as adviser_business_type_id
,LAST_VALUE(adviser_business_type)     OVER (PARTITION BY lead_id ORDER BY created_at asc rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as adviser_business_type
,lead_id
from tatooine_prod_core.materialized_leads_tracking)a

left join
(SELECT
    lead_id as lead_id2,
    MIN(lead_created_at) AS fecha_llegada,
    MIN(CASE WHEN status_id <> 1 THEN created_at END) AS fecha_primera_gestion,
    date_diff(
        'second',
        MIN(lead_created_at),
        MIN(CASE WHEN status_id <> 1 THEN created_at END)
    ) AS segundos_hasta_gestion
FROM tatooine_prod_core.materialized_leads_tracking
GROUP BY lead_id)k
on lead_id2 = lead_id

where upper(brand_name) like '%MG%'
```

| # | Paso | Operación | Columnas afectadas |
|---:|---|---|---|
| 1 | Origen | Origen (Value.NativeQuery) | Data |
| 2 | Texto recortado | Transformación de columnas | client_email, client_phone |
| 3 | Texto en minúsculas | Transformación de columnas | client_email |
| 4 | Valor reemplazado | Reemplazo de valores | — |
| 5 | Valor reemplazado1 | Reemplazo de valores | — |
| 6 | Valor reemplazado2 | Reemplazo de valores | — |
| 7 | Poner En Mayúsculas Cada Palabra | Transformación de columnas | adviser_name, category_name |
| 8 | Columna duplicada | Duplicar columna | — |
| 9 | Columnas con nombre cambiado | Renombrado | 1 renombre(s) |
| 10 | Tipo cambiado | Cambio de tipo | 1 cambio(s) de tipo: Fecha |
| 11 | Poner En Mayúsculas Cada Palabra1 | Transformación de columnas | campaing_name |

## 4.4 Parametros (partición `Parametros`, 4 pasos)

Evidencia: `GC - Leads MG.SemanticModel/definition/tables/Parametros.tmdl`.

```m
let
    Origen = DateTimeZone.SwitchZone(DateTimeZone.LocalNow(),-5,0),
    #"Convertida en tabla" = #table(1, {{Origen}}),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Convertida en tabla",{{"Column1", type datetimezone}}),
    #"Columnas con nombre cambiado" = Table.RenameColumns(#"Tipo cambiado",{{"Column1", "Parametro"}})
in
    #"Columnas con nombre cambiado"
```

| # | Paso | Operación | Columnas afectadas |
|---:|---|---|---|
| 1 | Origen | Origen (DateTimeZone.SwitchZone) | — |
| 2 | Convertida en tabla | Tabla literal | — |
| 3 | Tipo cambiado | Cambio de tipo | 1 cambio(s) de tipo: Column1 |
| 4 | Columnas con nombre cambiado | Renombrado | 1 renombre(s) |

# 5. Modelo de datos

## 5.1 Tablas

Evidencia: `GC - Leads MG.SemanticModel/definition/tables/<Tabla>.tmdl`.

| table_id | Tabla | Origen | Visibilidad | Columnas | Medidas | Particiones (modo) |
|---|---|---|---|---:|---:|---|
| b755d7f1-c560-4496-87aa-5a2f02db6754 | Atom | Importada (M) | Oculta | 36 | 0 | Atom (import) |
| 1772bd6c-2d45-4545-9514-77579db2a29a | Calendario | Calculada DAX | Visible | 5 | 0 | Calendario (import) |
| cf6f7b3b-c479-4965-b0ff-22c180c9f4b9 | Email_Orbi | Calculada DAX | Oculta | 4 | 0 | Email_Orbi (import) |
| 603c0b13-d64f-4b7e-98a4-52d2e9e9b73d | General | Calculada DAX | Visible | 27 | 0 | General (import) |
| 331c410a-9c35-4021-80c7-800360304b36 | Medidas | Solo medidas | Visible | 0 | 3 | Medidas (import) |
| 0579b9c4-4834-4081-9b64-b8a520a4fd29 | Orbi leads | Importada (M) | Oculta | 50 | 0 | Orbi leads (import) |
| 3eed8040-583a-49c8-b5e8-4a4820387176 | Parametros | Importada (M) | Visible | 1 | 0 | Parametros (import) |
| 8a114745-26d1-4c4d-8352-3b0a7e30888b | Tel_Orbi | Calculada DAX | Oculta | 4 | 0 | Tel_Orbi (import) |

Además, 18 tablas de fecha automáticas (inventario en 6.2).

- `General`: hechos (tabla calculada y visible). Una fila por lead, con los leads de Orbi más los de Atom que no se encontraron en Orbi (RN21). Es la tabla que consumen los visuales. Certeza: Inferido.
- `Orbi leads`: hechos de origen (oculta, consulta SQL a Athena sobre `tatooine_prod_core.materialized_leads_tracking`). Una fila por lead de MG, con los valores de su último registro (RN19, RN20); alimenta a `General`. Certeza: Encontrado.
- `Atom`: hechos de origen (oculta, consulta SQL a Athena sobre `atom_leads.leads` y `atom_leads.nebula_tiempos_de_agentes`). Una fila por lead de los canales que pasan el filtro RN18 (H-A02), con los valores de su último registro (RN20); alimenta a `General` solo con los marcados «Si» en `Criterio` (RN05). Certeza: Encontrado.
- `Email_Orbi` y `Tel_Orbi`: auxiliares ocultas y calculadas. Combinaciones distintas de correo (o teléfono), mes y año de los leads de Orbi; sirven para cruzar con Atom (RN01 a RN04). Sin relaciones.
- `Calendario`: dimensión de fechas (calculada, visible). Una fila por fecha distinta de `General[Fecha]`; da Año, Mes, NombreMes y Dia a los filtros y gráficos. Certeza: Inferido.
- `Medidas`: tabla contenedora vacía de las 3 medidas (`Leads`, `Total Leads sin nuevos`, `%Gestionados`); sin columnas ni relaciones. Certeza: Encontrado.
- `Parametros`: auxiliar. Una fila con la fecha y hora de la última carga; la usan las tarjetas «Última Actualización». Certeza: Encontrado.
- Tablas de fecha automáticas: auxiliares de Power BI, una por columna de fecha (3.4 y 6.2).

## 5.2 Relaciones

Evidencia: `GC - Leads MG.SemanticModel/definition/relationships.tmdl`.

| relationship_id | Desde | Hacia | Cardinalidad | Filtro | Activa | joinOnDateBehavior |
|---|---|---|---|---|---|---|
| 82534416-130d-457b-bdac-0a538c0d9f28 | Parametros[Parametro] | LocalDateTable_8c71bff9-1618-4d4c-8f78-b3f67e1ab247[Date] | many:one | oneDirection | Sí | datePartOnly |
| 50053091-3deb-4b92-b5f4-42e4bf1b1b8c | Orbi leads[created_at] | LocalDateTable_530313b0-a966-4706-9493-c8aa7a57a317[Date] | many:one | oneDirection | Sí | datePartOnly |
| 5ee187fc-bc73-4618-b7e4-1448284373ad | Orbi leads[updated_at] | LocalDateTable_2a4febd5-474e-4a78-a1c4-4e33331cca51[Date] | many:one | oneDirection | Sí | datePartOnly |
| ce196ceb-8cde-4f95-82e1-e529f44bbc78 | Orbi leads[lead_created_at] | LocalDateTable_02a5d6a9-c380-4732-ab95-b5cc6fa07be3[Date] | many:one | oneDirection | Sí | datePartOnly |
| a4e79a57-53a0-47fe-8480-00f2e3f3719d | Atom[updated_at] | LocalDateTable_52673d88-0ab9-49ce-886d-f5eade869640[Date] | many:one | oneDirection | Sí | datePartOnly |
| 574b3ee2-3aba-468b-8ebd-ba5e8336f082 | Atom[lead_created_at] | LocalDateTable_4069fc95-3b04-44b7-a146-e17eef31c965[Date] | many:one | oneDirection | Sí | datePartOnly |
| aed14155-6be1-4236-b97e-6637383b71f4 | Orbi leads[Fecha] | LocalDateTable_e82a7ec6-9aa0-496b-af4f-4da25dcd928c[Date] | many:one | oneDirection | Sí | datePartOnly |
| 5e45fb49-daf7-4ea7-8e2f-a074d42d0849 | Atom[Fecha] | LocalDateTable_f0a84349-d002-49a8-8ee5-86e0d9550369[Date] | many:one | oneDirection | Sí | datePartOnly |
| 9ed683e5-4216-48c4-86aa-a99762e620c7 | Atom[ultima_actualizacion] | LocalDateTable_306883ba-3073-45e4-959f-c41701d22ad2[Date] | many:one | oneDirection | Sí | datePartOnly |
| 69419a61-df3b-48e6-9f7a-f5eb773cd0e3 | Atom[fecha_asignacion] | LocalDateTable_66ac448c-938c-4528-8816-11b3e54e1806[Date] | many:one | oneDirection | Sí | datePartOnly |
| 93688ee0-ae0d-40cf-8480-744fec5ae924 | Atom[created_at] | LocalDateTable_8be1e938-b325-4949-a52e-399605e1608d[Date] | many:one | oneDirection | Sí | datePartOnly |
| 31e8ecf8-3a03-48a5-9709-5a22ce6d244e | Atom[fh_primer_mensaje_agente] | LocalDateTable_6c8c7523-345e-4ed0-a647-84ec42e712b8[Date] | many:one | oneDirection | Sí | datePartOnly |
| c70bec6c-a334-4c1a-94c3-55b13de83cb2 | Orbi leads[fecha_llegada] | LocalDateTable_ccea026a-6cac-48f0-9da6-b4a61589cbe0[Date] | many:one | oneDirection | Sí | datePartOnly |
| eadcaead-1561-49e1-ac77-0041f2a761d5 | Orbi leads[fecha_primera_gestion] | LocalDateTable_a107470f-adba-4dc8-9806-9431dde3512b[Date] | many:one | oneDirection | Sí | datePartOnly |
| e1c51a25-a8d0-4b20-9327-27fe9fc3c938 | General[updated_at] | LocalDateTable_9fb14d92-4303-4911-982e-f5fdddc298ba[Date] | many:one | oneDirection | Sí | datePartOnly |
| 33ed605a-42b3-4a3c-8065-b77fbecaef63 | General[lead_created_at] | LocalDateTable_80504aa4-9389-4877-8ef1-49d7106673de[Date] | many:one | oneDirection | Sí | datePartOnly |
| 29990a5a-4cc9-aef1-0f7e-1bd76e3ba465 | General[Fecha] | Calendario[Fecha] | many:one | oneDirection | Sí | — |
| 97a683d8-2747-45de-a7bb-e2f5bbc01c68 | Calendario[Fecha] | LocalDateTable_b86e5576-bfb4-4b10-b5fa-45ffc94d79d7[Date] | many:one | oneDirection | Sí | datePartOnly |

## 5.3 Jerarquías y ordenamiento

_Sin registros._

Ordenamiento (`sortByColumn`): Calendario[NombreMes] por Mes Las 18 tablas automáticas tienen su jerarquía de fechas propia.

## 5.4 Propiedades del modelo

| Propiedad | Valor |
|---|---|
| culture | es-ES |
| defaultPowerBIDataSourceVersion | powerBI_V3 |
| sourceQueryCulture | es-CO |
| valueFilterBehavior | independent |
| dataAccessOptions.legacyRedirects | Sí |
| dataAccessOptions.returnErrorValuesAsNull | Sí |
| compatibilityLevel | 1606 |

## 5.5 Seguridad

No aplica: el modelo no tiene roles.

# 6. Columnas

Clases de dependencia (CAT-03): V visuales · F filtros y segmentaciones · D DAX · M relaciones, jerarquías y ordenamiento · PQ pasos de Power Query · BK bookmarks · SQL consulta nativa.
Valor de cada celda (CAT-04): número = referencias encontradas · `0` = no encontrada en el alcance revisado · `NA` = no aplica · `NV` = no verificable · `P` = pendiente. SEC: no aplica (sin roles). El detalle de cada referencia está en su sección de origen (V → 9, F → 11, D → 6.1 expresiones y 7, M → 5, BK → 12).

## 6.1 Matriz A — columnas por tabla

### Atom (36 columnas)

Evidencia: `GC - Leads MG.SemanticModel/definition/tables/Atom.tmdl`.

| column_id | Columna | Nombre en origen | Tipo | Clase | Visibilidad | V | F | D | M | PQ | BK | SQL | Estado de uso | Nota |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| f76d6495-5d31-4e8e-acd3-c627de0c9fb1 | lead_id | lead_id | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| f6f07be1-1cd9-4a58-bb74-9bfe612dee0a | campaing_name | campaing_name | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| 99378a26-374f-4823-be4e-88bbcfbe3db1 | medium_value | medium_value | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| 770b9fa8-c9bd-43d5-84ef-08a0f7fb8876 | category_name | category_name | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| 6c80798c-3139-462d-88ca-20d6601f5b2b | brand_name | brand_name | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| 6add23bd-a39a-4357-942b-befde7544eac | adviser_name | adviser_name | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| 9b46f0a3-3569-4792-8b53-f846de31142a | adviser_email | adviser_email | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| 942e7551-dfda-47d1-826d-c9ce016f5f7c | client_name | client_name | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| c80a9777-f34d-4a32-938a-17e90b0bd6de | client_phone | client_phone | string | Origen | Oculta | 0 | 0 | 2 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía Cruce_Tel, tabla calculada General |
| 03a90625-721f-4de6-84bd-f931dcc9da12 | client_email | client_email | string | Origen | Oculta | 0 | 0 | 2 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía Cruce_Email, tabla calculada General |
| 25d90b75-7cda-4768-83f7-71fd2c014d11 | created_at | created_at | dateTime | Origen | Oculta | 0 | 0 | 2 | 1 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| 4a68845b-cd09-4631-ac21-a95db9cae5b9 | updated_at | updated_at | dateTime | Origen | Oculta | 0 | 0 | 2 | 1 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| d58ab649-d7a3-4e19-bacb-7daa14c07a9c | lead_created_at | lead_created_at | dateTime | Origen | Oculta | 0 | 0 | 4 | 1 | 0 | 0 | 1 | En uso | Uso indirecto vía Cruce_Email, Cruce_Tel, tabla calculada General |
| 688d33ed-4064-4e5f-be49-48a759418aa6 | management_time | management_time | double | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía management_time2 |
| 728e488d-8a45-46ca-9ff9-0b6e0cd2a17f | nombre_origen | nombre_origen | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| f7be5a06-fc00-43f8-9ab0-2310cd5e64f4 | grupo | grupo | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| 3a25def0-5a92-4814-8596-6e8972f1c9bc | primer_usuario | primer_usuario | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| 5f3fdeba-dcb1-4bfb-9df2-98d8a1189dc4 | primer_grupo | primer_grupo | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| 08be363e-0dfa-4754-a325-3dc6614d457d | Cruce_Tel | — | — | Calculada DAX | Oculta | 0 | 0 | 1 | 0 | NA | 0 | NA | En uso | Uso indirecto vía Cruce_Tel_Orbi |
| ea865bce-4448-4a1f-9758-055dafd541c9 | Cruce_Email | — | — | Calculada DAX | Oculta | 0 | 0 | 1 | 0 | NA | 0 | NA | En uso | Uso indirecto vía Cruce_Email_Orbi |
| bdc48d02-5360-4c08-9a84-7f1668b339eb | Cruce_Tel_Orbi | — | — | Calculada DAX | Oculta | 0 | 0 | 1 | 0 | NA | 0 | NA | En uso | Uso indirecto vía Criterio |
| 445ee536-adef-4072-b325-962e1fab582b | Cruce_Email_Orbi | — | — | Calculada DAX | Oculta | 0 | 0 | 1 | 0 | NA | 0 | NA | En uso | Uso indirecto vía Criterio |
| b30c9fbd-cffd-4612-9e43-9f287af6710d | Criterio | — | — | Calculada DAX | Oculta | 0 | 0 | 1 | 0 | NA | 0 | NA | En uso | Uso indirecto vía tabla calculada General |
| b9a6cc0c-e0fd-4c75-b0ea-b5bbe758313a | management_time2 | — | — | Calculada DAX | Oculta | 0 | 0 | 1 | 0 | NA | 0 | NA | En uso | Uso indirecto vía tabla calculada General |
| a68dc107-4863-4adb-98cd-b31a39840359 | tipificacion | tipificacion | string | Origen | Oculta | 0 | 0 | 2 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía status_name, tabla calculada General |
| eac2d8ca-6f37-42ea-99af-b4b866612017 | atencion | atencion | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía status_name |
| d777c3b7-3605-41fc-a649-3d2295a411b5 | atendido | atendido | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía status_name |
| ed4c34d7-e339-4432-9515-f2b0c349679b | status_name | — | — | Calculada DAX | Oculta | 0 | 0 | 1 | 0 | NA | 0 | NA | En uso | Uso indirecto vía tabla calculada General |
| 9368453f-db3e-44ae-8a95-83dae5f4bbcc | Fecha | lead_created_at - Copia | dateTime | Origen | Visible | 0 | 0 | 2 | 1 | 0 | 0 | 0 | En uso | Uso indirecto vía tabla calculada General |
| 1fcc7b46-ffea-4fe8-865d-57760434e2b6 | ultima_actualizacion | ultima_actualizacion | dateTime | Origen | Visible | 0 | 0 | 1 | 1 | 0 | 0 | 1 | Uso técnico | — |
| 5c06d019-122b-419c-89e3-9cb3373cde31 | fecha_asignacion | fecha_asignacion | dateTime | Origen | Visible | 0 | 0 | 2 | 1 | 0 | 0 | 1 | En uso | Uso indirecto vía atom gestión |
| 4758a6c9-d5b5-4f58-97bd-1d675e491cca | asignado | asignado | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| 64b531da-a727-468a-b302-21e467afed2c | canal | canal | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| d1d9f3bc-4d44-4d5b-9b87-f1091f52395b | fh_primer_mensaje_agente | fh_primer_mensaje_agente | dateTime | Origen | Visible | 0 | 0 | 2 | 1 | 0 | 0 | 1 | En uso | Uso indirecto vía atom gestión |
| 88b6527f-6d2d-4a5b-8c9b-f20d6f31e308 | fh_asignacion_primera | fh_asignacion_primera | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| 4cda05e5-27f6-4f14-90a5-eecfe8fad228 | atom gestión | — | — | Calculada DAX | Visible | 0 | 0 | 1 | 0 | NA | 0 | NA | En uso | Uso indirecto vía tabla calculada General |

Expresiones de columnas calculadas de Atom:

```dax
-- Cruce_Tel
Atom[client_phone]&"|"&MONTH(Atom[lead_created_at])&"|"&YEAR(Atom[lead_created_at])

-- Cruce_Email
Atom[client_email]&"|"&MONTH(Atom[lead_created_at])&"|"&YEAR(Atom[lead_created_at])

-- Cruce_Tel_Orbi
LOOKUPVALUE(Tel_Orbi[Orbi leads_client_phone],Tel_Orbi[Cruce_Tel],Atom[Cruce_Tel])

-- Cruce_Email_Orbi
LOOKUPVALUE(Email_Orbi[Orbi leads_client_email],Email_Orbi[Cruce_Email],Atom[Cruce_Email])

-- Criterio
IF(Atom[Cruce_Tel_Orbi]=BLANK() && Atom[Cruce_Email_Orbi]=BLANK(),"Si","No")

-- management_time2
Atom[management_time]/60

-- status_name
VAR AtendidoBase =
IF(Atom[atendido]="1","Atendido",
IF(Atom[atendido]="0" && Atom[atencion]="Si","Atendido",
IF(Atom[atendido]="0" && [tipificacion]="No tipificado","No Atendido",
IF(ISBLANK([atendido]),"Sin Identificar","Atendido"))))
RETURN AtendidoBase

-- atom gestión
var _1 = DATEDIFF(Atom[fecha_asignacion],Atom[fh_primer_mensaje_agente],MINUTE)
RETURN _1
```

### Calendario (5 columnas)

Evidencia: `GC - Leads MG.SemanticModel/definition/tables/Calendario.tmdl`.

| column_id | Columna | Nombre en origen | Tipo | Clase | Visibilidad | V | F | D | M | PQ | BK | SQL | Estado de uso | Nota |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c1c9abe0-a5a0-4444-ba0f-1d7a604cfd71 | Fecha | — | — | Origen | Visible | 0 | 0 | 4 | 2 | NA | 0 | NA | En uso | Uso indirecto vía Año, Dia, Mes |
| d795baed-d4d7-4225-97be-84ad7513ad2d | Año | — | — | Calculada DAX | Visible | 2 | 32 | 0 | 0 | NA | 2 | NA | En uso | — |
| 4ab18da6-0ade-47e9-8934-1bd7f2ef68c3 | Mes | — | — | Calculada DAX | Visible | 0 | 0 | 1 | 1 | NA | 0 | NA | En uso | Uso indirecto vía NombreMes |
| d1ea3667-b0b1-4efa-976f-95bca08c47af | NombreMes | — | — | Calculada DAX | Visible | 9 | 4 | 0 | 0 | NA | 2 | NA | En uso | — |
| a7a2042d-b069-4dda-8f14-1a988937ea59 | Dia | — | — | Calculada DAX | Visible | 1 | 0 | 0 | 0 | NA | 0 | NA | En uso | — |

Expresión de la tabla calculada Calendario (partición `Calendario`):

```dax
DISTINCT(General[Fecha])
```

Expresiones de columnas calculadas de Calendario:

```dax
-- Año
YEAR(Calendario[Fecha])

-- Mes
MONTH(Calendario[Fecha])

-- NombreMes
SWITCH(Calendario[Mes],1,"Enero",
                                   2,"Febrero",
                                   3,"Marzo",
                                   4,"Abril",
                                   5,"Mayo",
                                   6,"Junio",
                                   7,"Julio",
                                   8,"Agosto",
                                   9,"Septiembre",
                                   10,"Octubre",
                                   11,"Noviembre",
                                   12,"Diciembre"

                  )

-- Dia
DAY(Calendario[Fecha])
```

### Email_Orbi (4 columnas)

Evidencia: `GC - Leads MG.SemanticModel/definition/tables/Email_Orbi.tmdl`.

| column_id | Columna | Nombre en origen | Tipo | Clase | Visibilidad | V | F | D | M | PQ | BK | SQL | Estado de uso | Nota |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 64ec809e-9c3b-46bf-ac1b-d1a849dc3335 | Orbi leads_client_email | — | — | Origen | Oculta | 0 | 0 | 2 | 0 | NA | 0 | NA | En uso | Uso indirecto vía Cruce_Email, Cruce_Email_Orbi |
| bec6bb61-5ece-4f71-8508-067aa0212b4d | Mes | — | — | Origen | Oculta | 0 | 0 | 1 | 0 | NA | 0 | NA | En uso | Uso indirecto vía Cruce_Email |
| f4c1433f-dcbe-4cb6-80fd-84d0ee84e819 | Año | — | — | Origen | Oculta | 0 | 0 | 1 | 0 | NA | 0 | NA | En uso | Uso indirecto vía Cruce_Email |
| 08030cfb-2fe5-4c66-b9c7-b7539a010e6a | Cruce_Email | — | — | Calculada DAX | Oculta | 0 | 0 | 1 | 0 | NA | 0 | NA | En uso | Uso indirecto vía Cruce_Email_Orbi |

Expresión de la tabla calculada Email_Orbi (partición `Email_Orbi`):

```dax
VAR OPE1 = SELECTCOLUMNS('Orbi leads',
                         'Orbi leads'[client_email],
                         "Mes",MONTH('Orbi leads'[lead_created_at]),
                         "Año",YEAR('Orbi leads'[lead_created_at])
                        )
RETURN
DISTINCT(OPE1)
```

Expresiones de columnas calculadas de Email_Orbi:

```dax
-- Cruce_Email
Email_Orbi[Orbi leads_client_email]&"|"&Email_Orbi[Mes]&"|"&Email_Orbi[Año]
```

### General (27 columnas)

Evidencia: `GC - Leads MG.SemanticModel/definition/tables/General.tmdl`.

| column_id | Columna | Nombre en origen | Tipo | Clase | Visibilidad | V | F | D | M | PQ | BK | SQL | Estado de uso | Nota |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 76240127-1a55-4841-aa24-175e0497697f | nombre_origen | — | — | Origen | Visible | 0 | 0 | 0 | 0 | NA | 0 | NA | Sin uso interno identificado | — |
| 5f367d92-0c67-45a3-bbbe-1b2b24314faf | grupo | — | — | Origen | Visible | 0 | 0 | 0 | 0 | NA | 0 | NA | Sin uso interno identificado | — |
| 16c77d6b-9a73-43b6-a4b9-404af79ca171 | primer_usuario | — | — | Origen | Visible | 0 | 0 | 0 | 0 | NA | 0 | NA | Sin uso interno identificado | — |
| 75480fc9-a2e0-4585-994d-57516882643d | primer_grupo | — | — | Origen | Visible | 0 | 0 | 0 | 0 | NA | 0 | NA | Sin uso interno identificado | — |
| 1f6bbad1-f9f3-4cdf-960e-69792acfc69e | Fuente | — | — | Origen | Visible | 0 | 4 | 1 | 0 | NA | 2 | NA | En uso | — |
| 8ea4f07b-d7d3-47a5-aa10-d9388b4be16c | lead_id | — | — | Origen | Visible | 1 | 0 | 2 | 0 | NA | 0 | NA | En uso | — |
| 7886810d-860b-45bd-815a-238014e95896 | status_name | — | — | Origen | Visible | 7 | 0 | 1 | 0 | NA | 2 | NA | En uso | — |
| be01a8c6-93dc-455a-84cb-aca5871ec641 | campaing_name | — | — | Origen | Visible | 3 | 4 | 0 | 0 | NA | 2 | NA | En uso | — |
| 56095bbb-cb7a-4e50-9ea0-42bd1703c530 | medium_value | — | — | Origen | Visible | 3 | 1 | 0 | 0 | NA | 2 | NA | En uso | — |
| 3e36bb67-850f-47f6-a37f-a1ae674f0c76 | category_name | — | — | Origen | Visible | 0 | 4 | 0 | 0 | NA | 2 | NA | En uso | — |
| 92830340-cec0-4e5c-ad2e-aab12b8c1e12 | brand_name | — | — | Origen | Visible | 1 | 0 | 0 | 0 | NA | 0 | NA | En uso | — |
| 2d76a411-cd1d-403c-b81d-ebcd21668ddd | adviser_name | — | — | Origen | Visible | 2 | 0 | 0 | 0 | NA | 2 | NA | En uso | — |
| 6ea1a2cd-0c20-4400-b675-33fa7b8973ca | adviser_email | — | — | Origen | Visible | 0 | 0 | 0 | 0 | NA | 0 | NA | Sin uso interno identificado | — |
| 8b4ae1c9-cd78-4e8a-b52e-ba51f5b7d0cf | client_name | — | — | Origen | Visible | 1 | 0 | 0 | 0 | NA | 0 | NA | En uso | — |
| 68ea042a-945f-4c66-8f8a-0e51ba73e9cf | client_phone | — | — | Origen | Visible | 1 | 0 | 0 | 0 | NA | 0 | NA | En uso | — |
| bb269c0f-8743-4dcd-92cf-963f9286dfe1 | client_email | — | — | Origen | Visible | 1 | 0 | 0 | 0 | NA | 0 | NA | En uso | — |
| a0080d7f-1845-491b-ac35-b62b49be9f14 | created_at | — | string | Origen | Visible | 1 | 0 | 0 | 0 | NA | 0 | NA | En uso | — |
| 114a548c-45e1-4578-b3ca-d4b096f75d6d | updated_at | — | — | Origen | Visible | 0 | 0 | 1 | 1 | NA | 0 | NA | Uso técnico | — |
| 53c276d0-d118-4fe9-87d7-54a9b1a671c7 | lead_created_at | — | — | Origen | Visible | 0 | 0 | 1 | 1 | NA | 0 | NA | Uso técnico | — |
| 28dac8d4-da5b-4b38-8101-acd9c8f03dbe | management_time | — | — | Origen | Visible | 0 | 0 | 0 | 0 | NA | 0 | NA | Sin uso interno identificado | — |
| de673104-2d78-418e-b9a8-7579b1ab4875 | Fecha | — | — | Origen | Visible | 0 | 0 | 1 | 1 | NA | 0 | NA | En uso | Uso indirecto vía tabla calculada Calendario |
| fa78d927-8bd8-46d8-8299-3cf5ba13f5d9 | centro | — | — | Origen | Visible | 0 | 0 | 1 | 0 | NA | 0 | NA | En uso | Uso indirecto vía centro2 |
| 9c0edb13-ce41-409e-a4bc-2dedbf210657 | centro2 | — | — | Calculada DAX | Visible | 2 | 4 | 0 | 0 | NA | 2 | NA | En uso | — |
| db28b9df-076c-4989-9f5a-eb66efb90a87 | tipificacion | — | — | Origen | Visible | 1 | 4 | 0 | 0 | NA | 0 | NA | En uso | — |
| 8ed6c683-3af7-4dd1-9ffc-dc4ddd982351 | Action_name | — | — | Origen | Visible | 0 | 1 | 0 | 0 | NA | 0 | NA | En uso | — |
| bc3dbddf-1fbe-40fd-90a5-b80e3fe09e00 | Gestión | — | — | Origen | Visible | 0 | 4 | 0 | 0 | NA | 0 | NA | En uso | — |
| 098469b0-e460-4c35-a8d4-87ff3fbe3c32 | Tiempo de contacto | — | — | Origen | Visible | 1 | 0 | 0 | 0 | NA | 0 | NA | En uso | — |

Expresión de la tabla calculada General (partición `General`):

```dax
VAR Orbi = SELECTCOLUMNS('Orbi leads',
                         "lead_id",'Orbi leads'[lead_id],
                         "Action_name",'Orbi leads'[action_name],
                         "Gestión",'Orbi leads'[Orbi gestión],
                         "Tiempo de contacto",BLANK(),
                         "status_name",'Orbi leads'[status_name],
                         "campaing_name",'Orbi leads'[campaing_name],
                         "medium_value",'Orbi leads'[medium_value],
                         "category_name",'Orbi leads'[category_name],
                         "brand_name",'Orbi leads'[brand_name],
                         "centro",'Orbi leads'[concessionaire_names],
                         "tipificacion",'Orbi leads'[action_name],
                         "adviser_name",'Orbi leads'[adviser_name],
                         "adviser_email",'Orbi leads'[adviser_email],
                         "client_name",'Orbi leads'[client_name],
                         "client_phone",'Orbi leads'[client_phone],
                         "client_email",'Orbi leads'[client_email],
                         "created_at",'Orbi leads'[created_at],
                         "updated_at",'Orbi leads'[updated_at],
                         "lead_created_at",'Orbi leads'[lead_created_at],
                         "management_time",'Orbi leads'[management_time],
                         "nombre_origen",BLANK(),
                         "grupo",BLANK(),
                         "primer_usuario",BLANK(),
                         "primer_grupo",BLANK(),
                         "Fecha",'Orbi leads'[Fecha],
                         "Fuente","Orbi Leads"
                        )
VAR Ato = SELECTCOLUMNS(FILTER(Atom,Atom[Criterio]="Si"),
                         "lead_id",Atom[lead_id],
                         "Action_name",BLANK(),
                         "Gestión",BLANK(),
                         "Tiempo de contacto",Atom[atom gestión],
                         "status_name",Atom[status_name],
                         "campaing_name",Atom[campaing_name],
                         "medium_value",Atom[medium_value],
                         "category_name",Atom[category_name],
                         "brand_name",Atom[brand_name],
                         "centro",IF(Atom[grupo]=BLANK(),"Sin Definir",Atom[grupo]),
                         "tipificacion",Atom[tipificacion],
                         "adviser_name",IF(Atom[adviser_name]=BLANK(),"Sin Definir",Atom[adviser_name]),
                         "adviser_email",Atom[adviser_email],
                         "client_name",Atom[client_name],
                         "client_phone",Atom[client_phone],
                         "client_email",Atom[client_email],
                         "created_at",Atom[created_at],
                         "updated_at",Atom[updated_at],
                         "lead_created_at",Atom[lead_created_at],
                         "management_time",Atom[management_time2],
                         "nombre_origen",Atom[nombre_origen],
                         "grupo",Atom[grupo],
                         "primer_usuario",Atom[primer_usuario],
                         "primer_grupo",Atom[primer_grupo],
                         "Fecha",Atom[Fecha],
                         "Fuente","Atom"
                        )
VAR Uni = UNION(Orbi,Ato)
Return Uni
```

Expresiones de columnas calculadas de General:

```dax
-- centro2
SWITCH(General[centro],
                 "MG Perú Sala Surco","MGA-Lima-Surco",
                 "MG Perú Sala Sur Motors - Aviación","Peru - MG Mayorista - Sur Motors - Aviación",
                 "MG Perú Sala Interamericana Trujillo","Peru - MG Mayorista - Interamericana - Norte Trujillo",
                 "MG Perú Sala Interamericana Norte - Piura","Peru - MG Mayorista - Interamericana Norte - Piura",
                 "MG Perú Sala Zautos - La Victoria","Peru - MG Mayorista - Zautos - La Victoria",
                 "MG Perú Sala Satelital - Mall Bellavista","Peru - MG Mayorista - Satelital Mall - Bellavista",
                 "MG Perú Sala Sur Motors - Dolores","Peru - MG Mayorista - Sur Motors - Dolores",
                 "MG Perú Sala Interamericana Norte - Chiclayo","Peru - MG Mayorista - Interamericana Norte - Chiclayo",
                 "MG Perú Sala Zual Cars - Huaraz","Peru - MG Mayorista - Zual Cars - Huaraz",
                 "MG Perú Sala WankaMotors - Huancayo","Peru - MG Mayorista - Wankamotors - Huancayo",
                 "MG Perú Sala Satelital - Mall Santa Anita","Peru - MG Mayorista - Satelital Mall - Santa Anita",
                 "MG Perú Sala Satelital - Mall Plaza Norte","Peru - MG Mayorista - Satelital Mall - Plaza norte",
                 "MG Perú Sala Autocentro - Tarapoto","Peru - MG Mayorista - Autocentro Tarapoto - Tarapoto",
                 "MG Perú Sala Zual Cars - Tacna","Peru - MG Mayorista - Zual Cars - Tacna",
                 "MG Perú Sala Sur Motors - Juliaca","Peru - MG Mayorista - Sur Motors - Juliaca",
                 General[centro]
                )
```

### Medidas (0 columnas)

Evidencia: `GC - Leads MG.SemanticModel/definition/tables/Medidas.tmdl`.

_Sin registros._

### Orbi leads (50 columnas)

Evidencia: `GC - Leads MG.SemanticModel/definition/tables/Orbi leads.tmdl`.

| column_id | Columna | Nombre en origen | Tipo | Clase | Visibilidad | V | F | D | M | PQ | BK | SQL | Estado de uso | Nota |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 42391bf1-c16e-4b0a-91e2-3958f95733d2 | id | id | int64 | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| a4c00fe8-0670-42f7-a789-105cf137db9f | clasification_id | clasification_id | int64 | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| b5a511c5-1b24-4285-b311-9f004118535c | clasification_name | clasification_name | string | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| ddbf884b-ed48-4d92-aabd-79291bbd54cb | action_id | action_id | int64 | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| f364feaf-c7ea-41ab-bd41-daa2b13d8a71 | action_name | action_name | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| 06d38462-8dfb-4df7-97f4-18dff2827bf6 | status_id | status_id | int64 | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| 3dc3e85b-340a-4437-ab9a-8aa449ab51d3 | status_name | status_name | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| 75ba5a3a-19d0-4267-92b0-31e5ef0d5051 | campaing_id | campaing_id | int64 | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| 545836a5-ff9b-4fa3-a598-30a47ac85706 | campaing_name | campaing_name | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| 93fc81e5-1c39-45bb-94a5-cc43ba9a7907 | channel_id | channel_id | int64 | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| 48cb3405-ee46-4c22-bdeb-0e90e3846e60 | channel_value | channel_value | string | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| 184959d9-6c15-4725-b513-0856a2edd85f | medium_id | medium_id | int64 | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| df1ba371-e937-48df-819a-975a0a4cb412 | medium_value | medium_value | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| febdf777-9146-425d-aa4f-376d479cc374 | category_id | category_id | int64 | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| c9269836-6732-46db-bdfd-4abcbfead80b | category_name | category_name | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| 9bef26ff-0035-4e38-9352-2c473c744805 | country_name | country_name | string | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| d24c993a-7a61-4e1e-a340-37d7a2654e5e | company_id | company_id | int64 | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| b7915320-5083-43a7-9188-292306c69f42 | company_name | company_name | string | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| bc8a7b7b-61cc-485d-9fd0-27d0c45c4eb5 | brand_id | brand_id | int64 | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| 0209aea7-603c-4f79-acc6-b970ff1e7ad6 | brand_name | brand_name | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| 7dab7caa-13ff-46b8-adde-fbeac6408ff1 | wholesaler | wholesaler | int64 | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| 7537faec-d96b-4ac3-8b34-823ad6150caa | adviser_id | adviser_id | int64 | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| 9386ac6b-f81f-4ffe-b57c-0a0e4a65eeb9 | adviser_name | adviser_name | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| c6d3fab7-0804-4b64-b928-5029c2201bc2 | adviser_email | adviser_email | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| 5b1f2a28-bcb1-4b77-b988-c4b486f99f08 | adviser_document_type | adviser_document_type | string | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| 05737df5-707d-435d-823b-fcd1f67626a0 | adviser_document_number | adviser_document_number | string | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| 99d328fb-39d1-45c9-9f55-b2947597ef12 | concessionaire_id | concessionaire_id | int64 | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| 9420f8b1-638d-4212-ba86-ac92bd1651f6 | concessionaire_names | concessionaire_names | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| 3f9de8fa-2c01-4039-aec6-c90ca4f790da | client_name | client_name | string | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| 9437bb86-ccbb-40c3-a7ee-4a47783f1330 | client_phone | client_phone | string | Origen | Oculta | 0 | 0 | 2 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General, tabla calculada Tel_Orbi |
| 309bed67-26d6-4b41-bb4c-4a6b54a38234 | client_email | client_email | string | Origen | Oculta | 0 | 0 | 2 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada Email_Orbi, tabla calculada General |
| 836053dd-6bf6-4dbb-9193-cf456fd2061f | client_document_type_name | client_document_type_name | string | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| fc09e986-7c4b-4a5f-ac8d-728b70e02242 | client_document_number | client_document_number | string | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| a0d2095f-a139-4a64-9d98-5c7588c6aebb | model_id | model_id | int64 | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| 1df62411-1d48-4148-b720-179dce9522c5 | model_name | model_name | string | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| 8f4b7854-ea6f-499f-bfc4-ceae1ca77d51 | model_year | model_year | string | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| b8b3e7f7-9d0a-44fb-b4f7-ea0564166131 | license_plate | license_plate | string | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| 4acb975e-91b6-43fd-ae2f-88338c71fbaf | created_at | created_at | dateTime | Origen | Oculta | 0 | 0 | 2 | 1 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| ca84c679-2b7d-45ac-9e50-5621834437cb | updated_at | updated_at | dateTime | Origen | Oculta | 0 | 0 | 2 | 1 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| 8d932647-0fd3-4b69-81b5-6db794315ba5 | lead_created_at | lead_created_at | dateTime | Origen | Oculta | 0 | 0 | 4 | 1 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada Email_Orbi, tabla calculada General, tabla calculada Tel_Orbi |
| 5e5d1283-fdd5-4e9e-9ff7-aeb2628cfa96 | management_time | management_time | int64 | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| 57fc2890-0d00-4f98-aadc-82db554ee53e | adviser_business_type_id | adviser_business_type_id | int64 | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| 7f93fb36-c144-49d7-bf85-fa737fc8e95b | adviser_business_type | adviser_business_type | string | Origen | Oculta | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| 7c43fea6-4c68-4d58-9959-b6cee7ffeb9b | lead_id | lead_id | int64 | Origen | Oculta | 0 | 0 | 1 | 0 | 0 | 0 | 1 | En uso | Uso indirecto vía tabla calculada General |
| 3120b618-3702-4162-9083-3ea09d462f47 | Fecha | lead_created_at - Copia | dateTime | Origen | Visible | 0 | 0 | 2 | 1 | 0 | 0 | 0 | En uso | Uso indirecto vía tabla calculada General |
| a2f748f3-2e0f-4d9a-b93b-78f9cc5f25fd | lead_id2 | lead_id2 | int64 | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| 4901f7f3-7456-4d9f-bf16-7f25cf64e854 | fecha_llegada | fecha_llegada | dateTime | Origen | Visible | 0 | 0 | 2 | 1 | 0 | 0 | 1 | En uso | Uso indirecto vía Orbi gestión |
| d064781c-79c2-4aba-8caa-c20fd6a8af43 | fecha_primera_gestion | fecha_primera_gestion | dateTime | Origen | Visible | 0 | 0 | 2 | 1 | 0 | 0 | 1 | En uso | Uso indirecto vía Orbi gestión |
| 572ffdd3-5135-410e-a7a4-86909140735a | segundos_hasta_gestion | segundos_hasta_gestion | int64 | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 1 | Sin uso interno identificado | — |
| bc29b82a-e949-44d6-bc62-051139598048 | Orbi gestión | — | — | Calculada DAX | Visible | 0 | 0 | 1 | 0 | NA | 0 | NA | En uso | Uso indirecto vía tabla calculada General |

Expresiones de columnas calculadas de Orbi leads:

```dax
-- Orbi gestión
var _1 = DATEDIFF('Orbi leads'[fecha_llegada],'Orbi leads'[fecha_primera_gestion],MINUTE)
RETURN IF(_1>120,"Mayor a 2 horas","Menor a 2 horas")
```

### Parametros (1 columnas)

Evidencia: `GC - Leads MG.SemanticModel/definition/tables/Parametros.tmdl`.

| column_id | Columna | Nombre en origen | Tipo | Clase | Visibilidad | V | F | D | M | PQ | BK | SQL | Estado de uso | Nota |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a957dd6f-758f-406a-be60-f7edc67cfbf6 | Parametro | Column1 | dateTime | Origen | Visible | 4 | 0 | 1 | 1 | 0 | 2 | NA | En uso | — |

### Tel_Orbi (4 columnas)

Evidencia: `GC - Leads MG.SemanticModel/definition/tables/Tel_Orbi.tmdl`.

| column_id | Columna | Nombre en origen | Tipo | Clase | Visibilidad | V | F | D | M | PQ | BK | SQL | Estado de uso | Nota |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| e4cedf2d-98d3-4606-bdc1-9cc498a49729 | Orbi leads_client_phone | — | — | Origen | Oculta | 0 | 0 | 2 | 0 | NA | 0 | NA | En uso | Uso indirecto vía Cruce_Tel, Cruce_Tel_Orbi |
| b65bb59f-517d-4409-91a3-cabcffece884 | Mes | — | — | Origen | Oculta | 0 | 0 | 1 | 0 | NA | 0 | NA | En uso | Uso indirecto vía Cruce_Tel |
| e1ae07d1-b4ea-4aad-ab3e-14f8646215e9 | Año | — | — | Origen | Oculta | 0 | 0 | 1 | 0 | NA | 0 | NA | En uso | Uso indirecto vía Cruce_Tel |
| 9dbbf7de-ab32-4e98-b2fa-5104e565bd46 | Cruce_Tel | — | — | Calculada DAX | Oculta | 0 | 0 | 1 | 0 | NA | 0 | NA | En uso | Uso indirecto vía Cruce_Tel_Orbi |

Expresión de la tabla calculada Tel_Orbi (partición `Tel_Orbi`):

```dax
VAR OPE1 = SELECTCOLUMNS('Orbi leads',
                         'Orbi leads'[client_phone],
                         "Mes",MONTH('Orbi leads'[lead_created_at]),
                         "Año",YEAR('Orbi leads'[lead_created_at])
                        )
RETURN
DISTINCT(OPE1)
```

Expresiones de columnas calculadas de Tel_Orbi:

```dax
-- Cruce_Tel
Tel_Orbi[Orbi leads_client_phone]&"|"&Tel_Orbi[Mes]&"|"&Tel_Orbi[Año]
```

## 6.2 Tablas de fecha automáticas

Las genera Power BI por la inteligencia de tiempo automática; tienen la misma estructura. Se listan sus IDs completos por columna.

| table_id | Tabla | Origen (relación) | Columnas | column_id por columna | Estado de uso |
|---|---|---|---:|---|---|
| b18661e5-0b75-4fdb-9060-061354704c60 | DateTableTemplate_6e965017-0446-4f64-9716-c00440e09d6a | Plantilla (sin relación) | 7 | Date=5aea896d-c943-4da4-a699-a4de761634a3; Año=b1911b4f-4827-4546-97eb-1c61b8b80415; NroMes=dcc2e899-d7f5-4028-9809-2673d45a1e7e; Mes=3d766a74-70c5-43fa-8e63-7b7c6778991b; NroTrimestre=437e0f94-0b13-437a-9087-c85f5826daac; Trimestre=5f63ca2a-4ab0-45bc-9849-49c89226d37a; Día=56a665bb-f539-433a-9206-1cc46ec0a872 | En uso 3, Uso técnico 4 |
| 0a610c22-98cd-48b8-b3b2-46ac0138b2f4 | LocalDateTable_02a5d6a9-c380-4732-ab95-b5cc6fa07be3 | Orbi leads[lead_created_at] | 7 | Date=0b90e4b2-b885-415a-9345-adedeac3f025; Año=de3c73d1-cbc9-4153-aa51-e6a9e621d02f; NroMes=84fa6f6d-b295-4ffd-b6c7-5cce1a288f84; Mes=86bc5d81-1502-41be-8884-41f280eb717f; NroTrimestre=a5652123-e853-4adc-aa56-e413824d1d7a; Trimestre=8074ae26-0c2b-444d-b653-f43d360585d8; Día=b13798cd-0344-4df9-891b-65bc185b56fc | En uso 3, Uso técnico 4 |
| 8acca1c6-6ed1-4c5c-bd81-87e2179f9c48 | LocalDateTable_2a4febd5-474e-4a78-a1c4-4e33331cca51 | Orbi leads[updated_at] | 7 | Date=5cc9e8d2-9138-421f-86ca-f75bae3854d0; Año=312d5783-6a05-4f4c-b864-02e6d62f9302; NroMes=e1694119-ddd9-4a2c-b843-fa2254bae907; Mes=1e23e7cf-bd93-4168-bc25-642df6228306; NroTrimestre=e7a39a9a-a96f-4b4e-8aba-e16f14d8f2c9; Trimestre=4ceccc3f-7667-4518-8e53-d8d20d222db5; Día=14245cfd-c4ae-4205-be3b-e6d008043177 | En uso 3, Uso técnico 4 |
| c70dedf2-24b4-430a-8f43-b3aefa5ac4fe | LocalDateTable_306883ba-3073-45e4-959f-c41701d22ad2 | Atom[ultima_actualizacion] | 7 | Date=0fd5d80f-2541-410d-aebd-ed58196a4818; Año=50f47ce7-51b7-4a7d-9a7a-09fa7082f492; NroMes=ac9bf13c-3496-44f3-940b-85391a0d919a; Mes=9bbb9a89-d96d-4bd8-9f20-b71a7e6e2c23; NroTrimestre=9a5ca444-a270-4495-9843-02c456557f6a; Trimestre=559c60c2-45f7-4cfc-b64a-76428940cebf; Día=889d9bf4-aa62-4004-811f-287f349ae7b5 | En uso 3, Uso técnico 4 |
| d54d64d0-4e79-4fed-8089-f8912e67c7a3 | LocalDateTable_4069fc95-3b04-44b7-a146-e17eef31c965 | Atom[lead_created_at] | 7 | Date=90966ff0-cbbe-4c95-9410-6deebebb5081; Año=305e88aa-79ab-436d-8198-8d4564fe6bee; NroMes=5c221b05-49cd-4441-9573-b13705f8ab27; Mes=a9aeea76-4f73-4868-bfa9-e6991135b812; NroTrimestre=9bda0515-3681-421a-86b8-518dcb9bd20d; Trimestre=a6db9f48-713b-4aa3-a88c-e1ea91275796; Día=256382c4-7d7a-42d8-8cc0-843a7d7434de | En uso 3, Uso técnico 4 |
| 85f6cfeb-9bab-44f2-854d-7f12d413eb0d | LocalDateTable_52673d88-0ab9-49ce-886d-f5eade869640 | Atom[updated_at] | 7 | Date=818af647-f46c-4802-ac4a-56446e0641cd; Año=b7dfe2f9-6353-4234-8fc2-2ca25f893132; NroMes=a68ed596-a5ad-4be0-9a07-0ecc6b5173a4; Mes=824d4f5e-3be5-46ee-b8df-ff8b6f42a8fa; NroTrimestre=f29053b0-2c24-423a-822d-b038732c976d; Trimestre=d46fc8f2-45f5-4f02-9d5d-9733db12658c; Día=4dc2ea92-8004-40ee-a550-1f6276644b09 | En uso 3, Uso técnico 4 |
| fc90c0bb-bf81-4ddb-b48c-cdd3880aa93d | LocalDateTable_530313b0-a966-4706-9493-c8aa7a57a317 | Orbi leads[created_at] | 7 | Date=bd85d49d-e5b7-4597-b247-fc1e4bc49626; Año=d08f3876-6612-49f2-bd1f-d0c4bcc70ccf; NroMes=f5352c74-5f56-4913-b1c0-3479baee7ca6; Mes=48602588-dd2d-4925-8148-61b737156adf; NroTrimestre=17a55391-3551-4fde-b69d-88a5e3fefd46; Trimestre=1209dea5-c56d-4d11-bfd9-1005fdd4ca2f; Día=164f2503-2500-4fb0-8316-d904bfc10c84 | En uso 3, Uso técnico 4 |
| e6647dc8-a48d-4550-b37a-59159f418ba2 | LocalDateTable_66ac448c-938c-4528-8816-11b3e54e1806 | Atom[fecha_asignacion] | 7 | Date=1e42c5ed-7409-47fc-a016-e8927882983b; Año=31d2f162-d994-464c-b11a-d0db97dfafed; NroMes=fc935142-dd4a-41f5-a993-410625b0ac31; Mes=4dd6f253-58fa-490b-9e93-61014c4b9f09; NroTrimestre=aff6becd-bac5-49c6-8005-fe5c24bafa91; Trimestre=2747df34-d0e1-4e98-a049-1c9ba095d75d; Día=915e1285-fcaa-4579-b9b5-f0853d753e44 | En uso 3, Uso técnico 4 |
| a4ff3a3e-c3ac-4f6a-9f4a-92c46d7aa920 | LocalDateTable_6c8c7523-345e-4ed0-a647-84ec42e712b8 | Atom[fh_primer_mensaje_agente] | 7 | Date=18c8770f-c772-488a-8107-28b66805696d; Año=985010ed-9b76-4fe8-9fcf-bc505efea764; NroMes=dc213f41-f785-4cbb-9cda-934d81634f80; Mes=8f745a0f-0c39-4e80-99b9-2347bd9b620c; NroTrimestre=2b6115fa-0997-4b48-a48e-09a4090af8ed; Trimestre=270bcdf5-ff24-47ff-8c57-40ad0c1b95b7; Día=166f33c8-dda5-4828-b752-ef2ee7217ffd | En uso 3, Uso técnico 4 |
| 0f75be35-0f4f-4496-979f-92d7b944fc79 | LocalDateTable_80504aa4-9389-4877-8ef1-49d7106673de | General[lead_created_at] | 7 | Date=cba81239-8186-456c-8324-51352c5f8e53; Año=8e7e245b-160b-45ac-990f-c8cf986b48ab; NroMes=039114a7-6b86-47c5-854b-7c602425284e; Mes=34e80fbd-7952-48e0-b2f1-2b445140b091; NroTrimestre=9e7044c0-49a2-4c01-9e55-1de2e327e069; Trimestre=690d6a3b-e52a-4650-a1c0-3cfb69e526d2; Día=7f52144e-6e42-4775-86b3-9780e996486b | En uso 3, Uso técnico 4 |
| d1e2e1e3-983a-4c50-8e2c-fd42830960a8 | LocalDateTable_8be1e938-b325-4949-a52e-399605e1608d | Atom[created_at] | 7 | Date=fd98232c-17d0-43f7-a2bf-d27959ad0e1c; Año=a27cd175-d5e9-4387-87ba-f41bae678b14; NroMes=2adee0ff-3cdc-4225-98e6-9983d6a3dafa; Mes=edb73111-4cd5-4957-8dab-f2269ed47092; NroTrimestre=ea31bfdd-0626-4c87-ab2e-d013efe57003; Trimestre=af764b8d-7ad9-4f8d-b1f6-a3ed5cffd8d7; Día=17817779-ae0a-4da5-b360-62c0303856e6 | En uso 3, Uso técnico 4 |
| 53093fb2-aa44-4daf-8c3f-8650988e432f | LocalDateTable_8c71bff9-1618-4d4c-8f78-b3f67e1ab247 | Parametros[Parametro] | 7 | Date=b9e49eee-a4c0-440d-835b-5ce75ee752cd; Año=d1318adc-6a7b-4dbf-ac16-e4a344219bcf; NroMes=614edd69-ecbd-4743-a9e5-a22880a696a1; Mes=35f27d6e-9d37-42d6-b1dc-ec82f6f94728; NroTrimestre=172ff452-8ec9-42b5-9b3d-ba19c9b526d1; Trimestre=4cd6aacd-2c57-44b3-8a5d-821bde974db9; Día=b3a1e23b-2862-4d11-bbe1-fdfd2218da57 | En uso 3, Uso técnico 4 |
| db71c484-9683-4c52-b45f-52a40cb0f039 | LocalDateTable_9fb14d92-4303-4911-982e-f5fdddc298ba | General[updated_at] | 7 | Date=a33ab835-0bf5-4882-ad1e-b7eaded3568a; Año=b4fe5815-a345-418e-9570-03e082361139; NroMes=8611d830-cf80-4ca6-b31a-6a24ec6072d6; Mes=d669bdf9-e3ea-4ac8-bfa7-eb628b7ca8db; NroTrimestre=909a46b2-d0a0-4424-bde1-a126e66d332c; Trimestre=ffb6d08b-fce9-4e5c-b33a-436e777aa17a; Día=dd41bbbb-b436-4fd9-ae4a-4d05a2ef7478 | En uso 3, Uso técnico 4 |
| 6a042488-6a98-4b80-abf5-f1e667f27804 | LocalDateTable_a107470f-adba-4dc8-9806-9431dde3512b | Orbi leads[fecha_primera_gestion] | 7 | Date=e8ff66b8-02b4-480a-9c05-0582d8e3e5c1; Año=b020274b-e56f-4be8-a902-fcf0a536ddff; NroMes=c8f0a0f8-9f4b-4410-ad7c-be3e9bbf2335; Mes=c6f96fd5-5f1a-4c8f-bca1-25afec6b8d06; NroTrimestre=06a885fe-1391-4afb-b555-783085af2cc0; Trimestre=a2135455-1aa4-4457-a66b-cd823e5fb2b9; Día=92894be7-dc93-464e-b652-80233b2667cc | En uso 3, Uso técnico 4 |
| 93faf528-f2c7-40d8-9e72-c9d7d639be5c | LocalDateTable_b86e5576-bfb4-4b10-b5fa-45ffc94d79d7 | Calendario[Fecha] | 7 | Date=1529c401-20e0-460e-9364-ec793a754b85; Año=06c75d7a-8d48-4b4b-a4dc-ae14642f82c0; NroMes=f5061130-0cc5-407c-88f2-9fb32205fa82; Mes=a0532342-aef6-46a5-8c2d-84469c1398b5; NroTrimestre=bbadb5ac-d4a0-4361-8761-97d0cd948c99; Trimestre=49461e34-0a03-409d-ac5b-6b973e66f7f1; Día=8e2e1450-e6a3-48c1-a508-bd758a4a66e1 | En uso 3, Uso técnico 4 |
| afa18c16-44ea-4e26-b637-bfa126a75f64 | LocalDateTable_ccea026a-6cac-48f0-9da6-b4a61589cbe0 | Orbi leads[fecha_llegada] | 7 | Date=92dd137d-ce85-4155-9c2d-1b5c47cecae7; Año=2e21a9d1-df03-48ef-9ef4-db3fdb5d19c8; NroMes=59012766-7a83-479e-8d5e-c2b9ed68a513; Mes=81963739-fca0-4d7b-b0c6-1e41a00b07c2; NroTrimestre=d7305611-3efb-4c60-8811-0a2f3e1aaf1b; Trimestre=5368d7f0-d08b-4480-9eb8-00aa1b75d148; Día=3c30e931-53b7-4cb5-83b9-8dbc14e9da2c | En uso 3, Uso técnico 4 |
| be17ff1f-5edb-48f2-9599-06e5a63af97b | LocalDateTable_e82a7ec6-9aa0-496b-af4f-4da25dcd928c | Orbi leads[Fecha] | 7 | Date=f86f6064-4605-4474-aae6-71cf61e8dea3; Año=73fb5e27-8c87-4029-8a3e-85a8a723b809; NroMes=a43134ca-41ec-4dd9-8dc2-8d2456dd0a17; Mes=673eba50-6eb7-41db-9414-6e076e2f21d1; NroTrimestre=fe007726-a711-498c-8605-ced00ff1a3fd; Trimestre=242e055f-7196-437b-aa75-9c062de582af; Día=641deb8f-49d1-4273-a060-536f713deb9e | En uso 3, Uso técnico 4 |
| 659899bc-482e-44e8-b6a7-7878a0f63b01 | LocalDateTable_f0a84349-d002-49a8-8ee5-86e0d9550369 | Atom[Fecha] | 7 | Date=584c21b7-297f-4866-94be-093aca6da759; Año=b8d035e1-3fcb-4a8e-9cba-877f4ffde4ba; NroMes=8036c6b1-6466-475c-a79f-ce8d17e9ce55; Mes=41e9263e-13a6-444d-a265-6662cd0d2915; NroTrimestre=ca905399-1ce1-49c9-81c8-0a027dd5e7ac; Trimestre=496d410d-8566-4770-9734-c0dd6e78a1ca; Día=df4cde8f-12d0-4f40-975c-d2553c295b78 | En uso 3, Uso técnico 4 |

# 7. Medidas

Evidencia: `GC - Leads MG.SemanticModel/definition/tables/<Tabla>.tmdl`. Las expresiones completas están en el bloque de código al final de la sección.

| measure_id | Medida | Tabla | Formato | Usa | V | F | BK | D | Estado de uso | Nota |
|---|---|---|---|---|---|---|---|---|---|---|
| f7cbfe6b-d82c-4707-9fa0-f8585fc973a9 | Leads | Medidas | #,0 | General[lead_id] | 18 | 1 | 2 | 1 | En uso | — |
| 4c3da279-0fc4-4306-b741-b3bcdb56c50d | Total Leads sin nuevos | Medidas | #,0 | General[lead_id], General[status_name], General[Fuente] | 6 | 0 | 2 | 1 | En uso | — |
| 11399105-301c-4023-9b14-25bb8385ca8d | %Gestionados | Medidas | 0.00\ %;-0.00\ %;0.00\ % | Total Leads sin nuevos, Leads | 4 | 0 | 2 | 0 | En uso | — |

```dax
-- Medidas[Leads]
DISTINCTCOUNT(General[lead_id])

-- Medidas[Total Leads sin nuevos]
VAR OPE1 = CALCULATE(DISTINCTCOUNTNOBLANK(General[lead_id]),General[status_name]<>"Nuevo" && General[Fuente]="Orbi Leads")
VAR OPE2 = CALCULATE(DISTINCTCOUNTNOBLANK(General[lead_id]),General[status_name]="Atendido" && General[Fuente]="Atom")
RETURN
OPE1+OPE2

-- Medidas[%Gestionados]
DIVIDE([Total Leads sin nuevos],[Leads])
```

# 8. Páginas

Evidencia: `GC - Leads MG.Report/definition/pages/<page_id>/page.json`.

| page_id | Página | Orden | Visibilidad | Tamaño | Ajuste | Fondo | Tipo | Visuales |
|---|---|---:|---|---|---|---|---|---:|
| 5a5f1a6f0cc9bb4020bc | General | 1 | Visible | 1280×720 | FitToPage | #F6F6F5 | Normal | 25 |
| 5530a675c4ec857bce9b | Detalle | 2 | Oculta | 1280×720 | FitToPage | #F6F6F5 | Normal | 22 |
| 62aebec2a6e955dde5c4 | Días | 3 | Oculta | 1280×720 | FitToPage | #F6F6F5 | Normal | 19 |
| 512599bb0a5a991b53db | Cita Agendada | 4 | Oculta | 1280×720 | FitToPage | #F6F6F5 | Normal | 25 |

# 9. Visuales

Evidencia: `GC - Leads MG.Report/definition/pages/<page_id>/visuals/<visual_id>/visual.json`. Posición y tamaño en píxeles enteros del lienzo.

Por cada página hay dos tablas: la primera dice **qué es y dónde está** cada visual (una fila por visual); la segunda, **qué datos usa** (una fila por campo). Clases: «Con binding válido» = muestra datos y todos sus campos existen; «Decorativo» = imagen, forma o texto sin datos; «Botón/acción»; «Referencia rota» = algún campo de datos apunta a una entidad que no existe, por lo que el visual no puede dibujarse. Un «Formato huérfano» es una regla de formato (colores por categoría, formato condicional) que apunta a una entidad inexistente: no impide que el visual funcione y no lo convierte en referencia rota.

## 9.1 General (`5a5f1a6f0cc9bb4020bc`) — 25 visuales

| visual_id | Nombre | Tipo | Oculto | x | y | Ancho | Alto | z | Grupo | Clase | Formato huérfano | Estado de uso |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| 0c8ae0466609c5a58590 | Segmentación: Tipificación (General[tipificacion]) | slicer | No | 773 | 73 | 169 | 70 | 18006 | — | Con binding válido | No | En uso |
| 18106529a7229a8c0d0b | Año | slicer | No | 573 | 73 | 194 | 70 | 18002 | — | Con binding válido | No | En uso |
| 22c8e08106520a16532a | Botón Centro | actionButton | Sí | 865 | 289 | 123 | 24 | 18004 | — | Botón/acción | No | En uso |
| 30ef5613128cb692ea06 | Días | actionButton | No | 1144 | 199 | 123 | 29 | 18000 | — | Botón/acción | No | En uso |
| 31caf527e0784ec8de3d | Leads Por Centro | clusteredBarChart | No | 846 | 252 | 419 | 454 | 18003 | — | Con binding válido | Sí | En uso |
| 46483f57c705d050e02a | Año | slicer | No | 259 | 75 | 165 | 70 | 15000 | — | Con binding válido | No | En uso |
| 69d41e746aa9dd6220c2 | Año | slicer | No | 1105 | 73 | 148 | 70 | 18008 | — | Con binding válido | No | En uso |
| 7467a556e5287639abb0 | Año | slicer | No | 950 | 73 | 148 | 70 | 16000 | — | Con binding válido | No | En uso |
| 7b7f120ad03e39b73c4d | Imagen: Logo-Nebula22412030801788796.png | image | No | 1144 | 26 | 120 | 22 | 3000 | — | Decorativo | No | En uso |
| 8130ddd7e08c2704410c | Forma sin título | shape | No | 130 | 14 | 22 | 55 | 2000 | — | Decorativo | No | En uso |
| 85f9ad65c309c4985a6b | Forma sin título | shape | No | 0 | 0 | 1280 | 156 | 0 | — | Decorativo | No | En uso |
| 88852134b360130cbb84 | Leads Por Mes | lineChart | No | 14 | 252 | 471 | 218 | 9000 | — | Con binding válido | Sí | En uso |
| 963042e66cda8a1c0854 | Leads | textbox | No | 10 | 13 | 502 | 60 | 1000 | — | Decorativo | No | En uso |
| 97ab69d8068898241489 | % Gestionados | card | No | 788 | 166 | 215 | 80 | 14000 | — | Con binding válido | No | En uso |
| a60f74a73c00acb4753c | Año | slicer | No | 9 | 74 | 109 | 70 | 7000 | — | Con binding válido | No | En uso |
| aac2f915e77801ddad45 | Leads por Medio | pieChart | No | 494 | 252 | 341 | 218 | 11000 | — | Con binding válido | No | En uso |
| ae522e0dc253001505b6 | Detalle | actionButton | No | 1144 | 166 | 124 | 29 | 5000 | — | Botón/acción | No | En uso |
| b281fb425925679b971c | Total Leads | card | No | 281 | 165 | 215 | 80 | 6000 | — | Con binding válido | No | En uso |
| bfe0635e74a280504506 | Última Actualización | card | No | 153 | 7 | 226 | 68 | 4000 | — | Con binding válido | No | En uso |
| cd36b94b85c34947cb9e | Estado Actual Por Campaña | pivotTable | Sí | 848 | 251 | 419 | 454 | 12000 | — | Con binding válido | No | En uso |
| d66836dfea787b742d87 | Botón Campaña | actionButton | No | 862 | 289 | 122 | 24 | 18005 | — | Botón/acción | No | En uso |
| df2da022b8bd64859b96 | Estado Actual Leads Asesor | pivotTable | No | 12 | 477 | 824 | 229 | 10000 | — | Con binding válido | No | En uso |
| df7b3ec4996816832797 | Año | slicer | No | 123 | 74 | 130 | 70 | 8000 | — | Con binding válido | No | En uso |
| e1cec93ba657b6a2ccd6 | Leads Gestionados | card | No | 536 | 165 | 215 | 80 | 13000 | — | Con binding válido | No | En uso |
| fde6c2de0e14a29ec150 | Año | slicer | No | 429 | 73 | 135 | 70 | 17000 | — | Con binding válido | No | En uso |

Bindings de General (32):

| visual_id | Visual | Rol | Campo | Agregación | Referencia |
|---|---|---|---|---|---|
| 0c8ae0466609c5a58590 | Segmentación: Tipificación (General[tipificacion]) | Values | General[tipificacion] | — | Válida |
| 18106529a7229a8c0d0b | Año | Values | General[centro2] | — | Válida |
| 31caf527e0784ec8de3d | Leads Por Centro | Category | General[centro2] | — | Válida |
| 31caf527e0784ec8de3d | Leads Por Centro | Y | Medidas[Leads] | — | Válida |
| 31caf527e0784ec8de3d | Leads Por Centro | Y | Medidas[Total Leads sin nuevos] | — | Válida |
| 31caf527e0784ec8de3d | Leads Por Centro | Formato/propiedad | VehiculosEntregados[Gama] | — | Formato huérfano |
| 31caf527e0784ec8de3d | Leads Por Centro | Formato/propiedad | Funnel Digital[Origen] | — | Formato huérfano |
| 46483f57c705d050e02a | Año | Values | General[campaing_name] | — | Válida |
| 69d41e746aa9dd6220c2 | Año | Values | General[Gestión] | — | Válida |
| 7467a556e5287639abb0 | Año | Values | General[Fuente] | — | Válida |
| 88852134b360130cbb84 | Leads Por Mes | Category | Calendario[NombreMes] | — | Válida |
| 88852134b360130cbb84 | Leads Por Mes | Series | Calendario[Año] | — | Válida |
| 88852134b360130cbb84 | Leads Por Mes | Y | Medidas[Leads] | — | Válida |
| 88852134b360130cbb84 | Leads Por Mes | Formato/propiedad | VehiculosEntregados[Gama] | — | Formato huérfano |
| 88852134b360130cbb84 | Leads Por Mes | Formato/propiedad | Funnel Digital[Origen] | — | Formato huérfano |
| 97ab69d8068898241489 | % Gestionados | Values | Medidas[%Gestionados] | — | Válida |
| a60f74a73c00acb4753c | Año | Values | Calendario[Año] | — | Válida |
| aac2f915e77801ddad45 | Leads por Medio | Category | General[medium_value] | — | Válida |
| aac2f915e77801ddad45 | Leads por Medio | Y | Medidas[Leads] | — | Válida |
| b281fb425925679b971c | Total Leads | Values | Medidas[Leads] | — | Válida |
| bfe0635e74a280504506 | Última Actualización | Values | Parametros[Parametro] | Min | Válida |
| cd36b94b85c34947cb9e | Estado Actual Por Campaña | Columns | General[status_name] | — | Válida |
| cd36b94b85c34947cb9e | Estado Actual Por Campaña | Rows | General[campaing_name] | — | Válida |
| cd36b94b85c34947cb9e | Estado Actual Por Campaña | Values | Medidas[Leads] | — | Válida |
| cd36b94b85c34947cb9e | Estado Actual Por Campaña | Formato/propiedad | Calendario[NombreMes] | — | Válida |
| df2da022b8bd64859b96 | Estado Actual Leads Asesor | Columns | General[status_name] | — | Válida |
| df2da022b8bd64859b96 | Estado Actual Leads Asesor | Rows | General[adviser_name] | — | Válida |
| df2da022b8bd64859b96 | Estado Actual Leads Asesor | Values | Medidas[Leads] | — | Válida |
| df2da022b8bd64859b96 | Estado Actual Leads Asesor | Formato/propiedad | Calendario[NombreMes] | — | Válida |
| df7b3ec4996816832797 | Año | Values | Calendario[NombreMes] | — | Válida |
| e1cec93ba657b6a2ccd6 | Leads Gestionados | Values | Medidas[Total Leads sin nuevos] | — | Válida |
| fde6c2de0e14a29ec150 | Año | Values | General[category_name] | — | Válida |

## 9.2 Detalle (`5530a675c4ec857bce9b`) — 22 visuales

| visual_id | Nombre | Tipo | Oculto | x | y | Ancho | Alto | z | Grupo | Clase | Formato huérfano | Estado de uso |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| 0a8e34e81b960a48dbab | Forma sin título | shape | No | 130 | 14 | 22 | 55 | 2000 | — | Decorativo | No | En uso |
| 277ff960ee881b05b662 | Año | slicer | No | 573 | 73 | 194 | 70 | 17018 | — | Con binding válido | No | En uso |
| 3b9f86c059655b821849 | Tipificación Por Estado | pivotTable | No | 867 | 254 | 395 | 213 | 17012 | — | Con binding válido | No | En uso |
| 41b98b47ace3073986a1 | Leads Por Estado | pieChart | No | 443 | 254 | 417 | 213 | 13000 | — | Con binding válido | Sí | En uso |
| 4de425c50a2a0d0d7da3 | Año | slicer | No | 9 | 74 | 109 | 70 | 17013 | — | Con binding válido | No | En uso |
| 60a8d616a3b762017e01 | Última Actualización | card | No | 153 | 7 | 226 | 68 | 4000 | — | Con binding válido | No | En uso |
| 762df504015559003b02 | Segmentación: Tipificación (General[tipificacion]) | slicer | No | 773 | 73 | 169 | 70 | 17019 | — | Con binding válido | No | En uso |
| 7e08797f4bd3c07c324b | Leads | textbox | No | 10 | 13 | 502 | 60 | 1000 | — | Decorativo | No | En uso |
| 83542d749ad2a069c86b | Detalle | tableEx | No | 16 | 474 | 1249 | 243 | 14000 | — | Con binding válido | No | En uso |
| 8607acb6d143a7041cc0 | General | actionButton | No | 1146 | 165 | 122 | 30 | 5000 | — | Botón/acción | No | En uso |
| 973bc72ab782849a977b | Días | actionButton | No | 1146 | 199 | 123 | 29 | 17000 | — | Botón/acción | No | En uso |
| 974d0f82b136c0620b0e | Año | slicer | No | 429 | 73 | 135 | 70 | 17017 | — | Con binding válido | No | En uso |
| 9f21e89606a070200443 | Año | slicer | No | 123 | 74 | 130 | 70 | 17014 | — | Con binding válido | No | En uso |
| bff0421dae410e278066 | Leads Por Mes | clusteredBarChart | No | 16 | 254 | 418 | 213 | 15000 | — | Con binding válido | Sí | En uso |
| c5b0cc52ab0a7dec6d08 | Año | slicer | No | 1105 | 73 | 148 | 70 | 17020 | — | Con binding válido | No | En uso |
| cfe32cda6c909606e1d0 | Año | slicer | No | 950 | 73 | 148 | 70 | 17016 | — | Con binding válido | No | En uso |
| d49cf8a70de7660a53a9 | Forma sin título | shape | No | 0 | 0 | 1280 | 156 | 0 | — | Decorativo | No | En uso |
| d696bcc0d275185e560b | Año | slicer | No | 259 | 75 | 165 | 70 | 17015 | — | Con binding válido | No | En uso |
| d81d62b4921ea7c96008 | Imagen: Logo-Nebula22412030801788796.png | image | No | 1144 | 26 | 120 | 22 | 3000 | — | Decorativo | No | En uso |
| edc2f27420a55ac608b9 | % Gestionados | card | No | 788 | 166 | 215 | 80 | 17005 | — | Con binding válido | No | En uso |
| f308d59b90290b04cc6e | Leads Gestionados | card | No | 536 | 165 | 215 | 80 | 17004 | — | Con binding válido | No | En uso |
| ff8e7130d6e0030d10e0 | Total Leads | card | No | 281 | 165 | 215 | 80 | 17001 | — | Con binding válido | No | En uso |

Bindings de Detalle (34):

| visual_id | Visual | Rol | Campo | Agregación | Referencia |
|---|---|---|---|---|---|
| 277ff960ee881b05b662 | Año | Values | General[centro2] | — | Válida |
| 3b9f86c059655b821849 | Tipificación Por Estado | Columns | Calendario[NombreMes] | — | Válida |
| 3b9f86c059655b821849 | Tipificación Por Estado | Rows | General[tipificacion] | — | Válida |
| 3b9f86c059655b821849 | Tipificación Por Estado | Values | Medidas[Leads] | — | Válida |
| 41b98b47ace3073986a1 | Leads Por Estado | Category | General[status_name] | — | Válida |
| 41b98b47ace3073986a1 | Leads Por Estado | Y | Medidas[Leads] | — | Válida |
| 41b98b47ace3073986a1 | Leads Por Estado | Formato/propiedad | VehiculosEntregados[Gama] | — | Formato huérfano |
| 41b98b47ace3073986a1 | Leads Por Estado | Formato/propiedad | Funnel Digital[Origen] | — | Formato huérfano |
| 4de425c50a2a0d0d7da3 | Año | Values | Calendario[Año] | — | Válida |
| 60a8d616a3b762017e01 | Última Actualización | Values | Parametros[Parametro] | Min | Válida |
| 762df504015559003b02 | Segmentación: Tipificación (General[tipificacion]) | Values | General[tipificacion] | — | Válida |
| 83542d749ad2a069c86b | Detalle | Values | General[lead_id] | — | Válida |
| 83542d749ad2a069c86b | Detalle | Values | General[client_name] | — | Válida |
| 83542d749ad2a069c86b | Detalle | Values | General[brand_name] | — | Válida |
| 83542d749ad2a069c86b | Detalle | Values | General[campaing_name] | — | Válida |
| 83542d749ad2a069c86b | Detalle | Values | General[client_email] | — | Válida |
| 83542d749ad2a069c86b | Detalle | Values | General[client_phone] | — | Válida |
| 83542d749ad2a069c86b | Detalle | Values | General[medium_value] | — | Válida |
| 83542d749ad2a069c86b | Detalle | Values | General[status_name] | — | Válida |
| 83542d749ad2a069c86b | Detalle | Values | General[created_at] | — | Válida |
| 83542d749ad2a069c86b | Detalle | Values | General[Tiempo de contacto] | — | Válida |
| 974d0f82b136c0620b0e | Año | Values | General[category_name] | — | Válida |
| 9f21e89606a070200443 | Año | Values | Calendario[NombreMes] | — | Válida |
| bff0421dae410e278066 | Leads Por Mes | Category | Calendario[NombreMes] | — | Válida |
| bff0421dae410e278066 | Leads Por Mes | Series | General[status_name] | — | Válida |
| bff0421dae410e278066 | Leads Por Mes | Y | Medidas[Leads] | — | Válida |
| bff0421dae410e278066 | Leads Por Mes | Formato/propiedad | VehiculosEntregados[Gama] | — | Formato huérfano |
| bff0421dae410e278066 | Leads Por Mes | Formato/propiedad | Funnel Digital[Origen] | — | Formato huérfano |
| c5b0cc52ab0a7dec6d08 | Año | Values | General[Gestión] | — | Válida |
| cfe32cda6c909606e1d0 | Año | Values | General[Fuente] | — | Válida |
| d696bcc0d275185e560b | Año | Values | General[campaing_name] | — | Válida |
| edc2f27420a55ac608b9 | % Gestionados | Values | Medidas[%Gestionados] | — | Válida |
| f308d59b90290b04cc6e | Leads Gestionados | Values | Medidas[Total Leads sin nuevos] | — | Válida |
| ff8e7130d6e0030d10e0 | Total Leads | Values | Medidas[Leads] | — | Válida |

## 9.3 Días (`62aebec2a6e955dde5c4`) — 19 visuales

| visual_id | Nombre | Tipo | Oculto | x | y | Ancho | Alto | z | Grupo | Clase | Formato huérfano | Estado de uso |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| 0fd661a032712444cd13 | Año | slicer | No | 123 | 74 | 130 | 70 | 15007 | — | Con binding válido | No | En uso |
| 2aaac833cc40883a2212 | Segmentación: Tipificación (General[tipificacion]) | slicer | No | 773 | 73 | 169 | 70 | 15012 | — | Con binding válido | No | En uso |
| 362806e0bc36a521ba94 | % Gestionados | card | No | 788 | 166 | 215 | 80 | 15005 | — | Con binding válido | No | En uso |
| 3ae24a9bc85b696c12d9 | Año | slicer | No | 429 | 73 | 135 | 70 | 15010 | — | Con binding válido | No | En uso |
| 3b1238777043285beced | Año | slicer | No | 9 | 74 | 109 | 70 | 15006 | — | Con binding válido | No | En uso |
| 58c124ed43032ab5b751 | Detalle | actionButton | No | 1144 | 199 | 123 | 29 | 15000 | — | Botón/acción | No | En uso |
| 6461e3677819014073d9 | Año | slicer | No | 259 | 75 | 165 | 70 | 15008 | — | Con binding válido | No | En uso |
| 681b53b4ca0e1ead507b | Total Leads | card | No | 281 | 165 | 215 | 80 | 15001 | — | Con binding válido | No | En uso |
| 7ea9b780b7c30821ee80 | General | actionButton | No | 1146 | 165 | 122 | 30 | 14000 | — | Botón/acción | No | En uso |
| 9ee41b8fb54a31b576cd | Año | slicer | No | 950 | 73 | 148 | 70 | 15009 | — | Con binding válido | No | En uso |
| 9eee605dba530a00c130 | Total leads por días del mes | lineChart | No | 14 | 256 | 1249 | 456 | 13000 | — | Con binding válido | Sí | En uso |
| b3e52184e5a5655abb18 | Leads Gestionados | card | No | 536 | 165 | 215 | 80 | 15004 | — | Con binding válido | No | En uso |
| b7bf50e38a2a650d1cbb | Leads | textbox | No | 10 | 13 | 502 | 60 | 1000 | — | Decorativo | No | En uso |
| d35a3eb2852c48c8eeec | Año | slicer | No | 573 | 73 | 194 | 70 | 15011 | — | Con binding válido | No | En uso |
| e3a2959dd6d189491a0b | Forma sin título | shape | No | 130 | 14 | 22 | 55 | 2000 | — | Decorativo | No | En uso |
| ef6046104857770c9edc | Imagen: Logo-Nebula22412030801788796.png | image | No | 1144 | 26 | 120 | 22 | 3000 | — | Decorativo | No | En uso |
| f4328e565b1a1cd4c63b | Última Actualización | card | No | 153 | 7 | 226 | 68 | 4000 | — | Con binding válido | No | En uso |
| f9f468839301408cb5e5 | Forma sin título | shape | No | 0 | 0 | 1280 | 156 | 0 | — | Decorativo | No | En uso |
| fe53f0f045aeeb8dcad5 | Año | slicer | No | 1105 | 73 | 148 | 70 | 15013 | — | Con binding válido | No | En uso |

Bindings de Días (17):

| visual_id | Visual | Rol | Campo | Agregación | Referencia |
|---|---|---|---|---|---|
| 0fd661a032712444cd13 | Año | Values | Calendario[NombreMes] | — | Válida |
| 2aaac833cc40883a2212 | Segmentación: Tipificación (General[tipificacion]) | Values | General[tipificacion] | — | Válida |
| 362806e0bc36a521ba94 | % Gestionados | Values | Medidas[%Gestionados] | — | Válida |
| 3ae24a9bc85b696c12d9 | Año | Values | General[category_name] | — | Válida |
| 3b1238777043285beced | Año | Values | Calendario[Año] | — | Válida |
| 6461e3677819014073d9 | Año | Values | General[campaing_name] | — | Válida |
| 681b53b4ca0e1ead507b | Total Leads | Values | Medidas[Leads] | — | Válida |
| 9ee41b8fb54a31b576cd | Año | Values | General[Fuente] | — | Válida |
| 9eee605dba530a00c130 | Total leads por días del mes | Category | Calendario[Dia] | — | Válida |
| 9eee605dba530a00c130 | Total leads por días del mes | Series | Calendario[NombreMes] | — | Válida |
| 9eee605dba530a00c130 | Total leads por días del mes | Y | Medidas[Leads] | — | Válida |
| 9eee605dba530a00c130 | Total leads por días del mes | Formato/propiedad | VehiculosEntregados[Gama] | — | Formato huérfano |
| 9eee605dba530a00c130 | Total leads por días del mes | Formato/propiedad | Funnel Digital[Origen] | — | Formato huérfano |
| b3e52184e5a5655abb18 | Leads Gestionados | Values | Medidas[Total Leads sin nuevos] | — | Válida |
| d35a3eb2852c48c8eeec | Año | Values | General[centro2] | — | Válida |
| f4328e565b1a1cd4c63b | Última Actualización | Values | Parametros[Parametro] | Min | Válida |
| fe53f0f045aeeb8dcad5 | Año | Values | General[Gestión] | — | Válida |

## 9.4 Cita Agendada (`512599bb0a5a991b53db`) — 25 visuales

| visual_id | Nombre | Tipo | Oculto | x | y | Ancho | Alto | z | Grupo | Clase | Formato huérfano | Estado de uso |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| 11f3f826101a637755eb | Leads | textbox | No | 10 | 13 | 502 | 60 | 1000 | — | Decorativo | No | En uso |
| 17ef0fc6b0004b9e13c3 | Año | slicer | No | 1105 | 73 | 148 | 70 | 24008 | — | Con binding válido | No | En uso |
| 20e2c4b5b10d63667b4b | Año | slicer | No | 259 | 75 | 165 | 70 | 24003 | — | Con binding válido | No | En uso |
| 230203b80cd7dae4c694 | Leads por Medio | pieChart | No | 494 | 252 | 341 | 218 | 11000 | — | Con binding válido | No | En uso |
| 2ec568f5aed88ac632b3 | Botón Centro | actionButton | Sí | 865 | 289 | 123 | 24 | 21000 | — | Botón/acción | No | Uso desconocido |
| 3cf99ef07474ed230802 | Segmentación: Tipificación (General[tipificacion]) | slicer | No | 773 | 73 | 169 | 70 | 24007 | — | Con binding válido | No | En uso |
| 3e8e50d0ce305c0c1773 | Estado Actual Leads Asesor | pivotTable | No | 12 | 477 | 824 | 229 | 10000 | — | Con binding válido | No | En uso |
| 4ccd33593b68ac581943 | Leads Por Centro | clusteredBarChart | No | 846 | 252 | 419 | 454 | 20000 | — | Con binding válido | Sí | En uso |
| 54bb486e40da053209c5 | Detalle | actionButton | No | 1144 | 166 | 124 | 29 | 5000 | — | Botón/acción | No | En uso |
| 771af917920b90b06662 | % Gestionados | card | No | 788 | 166 | 215 | 80 | 14000 | — | Con binding válido | No | En uso |
| 7d6ed2b763a573573a60 | Leads Gestionados | card | No | 536 | 165 | 215 | 80 | 13000 | — | Con binding válido | No | En uso |
| 7f21050ab92b09336526 | Forma sin título | shape | No | 130 | 14 | 22 | 55 | 2000 | — | Decorativo | No | En uso |
| 8cdc2d786b000ae0e42c | Imagen: Logo-Nebula22412030801788796.png | image | No | 1144 | 26 | 120 | 22 | 3000 | — | Decorativo | No | En uso |
| 959957a0d34e54005a43 | Estado Actual Por Campaña | pivotTable | Sí | 848 | 251 | 419 | 454 | 12000 | — | Con binding válido | No | Uso desconocido |
| 97e3e193811090b8994d | Año | slicer | No | 123 | 74 | 130 | 70 | 24002 | — | Con binding válido | No | En uso |
| 9ccfba57526b15032805 | Botón Campaña | actionButton | No | 862 | 289 | 122 | 24 | 22000 | — | Botón/acción | No | En uso |
| a214c6981c373204ba46 | Año | slicer | No | 429 | 73 | 135 | 70 | 24005 | — | Con binding válido | No | En uso |
| ab71c6e65080a9eaa82e | Total Leads | card | No | 281 | 165 | 215 | 80 | 6000 | — | Con binding válido | No | En uso |
| b1dca116d7b5b2b49c25 | Forma sin título | shape | No | 0 | 0 | 1280 | 156 | 0 | — | Decorativo | No | En uso |
| b6791fcb998ed58a07ec | Días | actionButton | No | 1144 | 199 | 123 | 29 | 18000 | — | Botón/acción | No | En uso |
| c30659788e6c1782a8d0 | Leads Por Mes | lineChart | No | 14 | 252 | 471 | 218 | 9000 | — | Con binding válido | Sí | En uso |
| c36233ee7e7dd9572643 | Año | slicer | No | 950 | 73 | 148 | 70 | 24004 | — | Con binding válido | No | En uso |
| c9b042401cc69403d10a | Año | slicer | No | 9 | 74 | 109 | 70 | 24001 | — | Con binding válido | No | En uso |
| ee76c22fe4a2535a2bd9 | Año | slicer | No | 573 | 73 | 194 | 70 | 24006 | — | Con binding válido | No | En uso |
| fd6649c4e6392049e9c7 | Última Actualización | card | No | 153 | 7 | 226 | 68 | 4000 | — | Con binding válido | No | En uso |

Bindings de Cita Agendada (32):

| visual_id | Visual | Rol | Campo | Agregación | Referencia |
|---|---|---|---|---|---|
| 17ef0fc6b0004b9e13c3 | Año | Values | General[Gestión] | — | Válida |
| 20e2c4b5b10d63667b4b | Año | Values | General[campaing_name] | — | Válida |
| 230203b80cd7dae4c694 | Leads por Medio | Category | General[medium_value] | — | Válida |
| 230203b80cd7dae4c694 | Leads por Medio | Y | Medidas[Leads] | — | Válida |
| 3cf99ef07474ed230802 | Segmentación: Tipificación (General[tipificacion]) | Values | General[tipificacion] | — | Válida |
| 3e8e50d0ce305c0c1773 | Estado Actual Leads Asesor | Columns | General[status_name] | — | Válida |
| 3e8e50d0ce305c0c1773 | Estado Actual Leads Asesor | Rows | General[adviser_name] | — | Válida |
| 3e8e50d0ce305c0c1773 | Estado Actual Leads Asesor | Values | Medidas[Leads] | — | Válida |
| 3e8e50d0ce305c0c1773 | Estado Actual Leads Asesor | Formato/propiedad | Calendario[NombreMes] | — | Válida |
| 4ccd33593b68ac581943 | Leads Por Centro | Category | General[centro2] | — | Válida |
| 4ccd33593b68ac581943 | Leads Por Centro | Y | Medidas[Leads] | — | Válida |
| 4ccd33593b68ac581943 | Leads Por Centro | Y | Medidas[Total Leads sin nuevos] | — | Válida |
| 4ccd33593b68ac581943 | Leads Por Centro | Formato/propiedad | VehiculosEntregados[Gama] | — | Formato huérfano |
| 4ccd33593b68ac581943 | Leads Por Centro | Formato/propiedad | Funnel Digital[Origen] | — | Formato huérfano |
| 771af917920b90b06662 | % Gestionados | Values | Medidas[%Gestionados] | — | Válida |
| 7d6ed2b763a573573a60 | Leads Gestionados | Values | Medidas[Total Leads sin nuevos] | — | Válida |
| 959957a0d34e54005a43 | Estado Actual Por Campaña | Columns | General[status_name] | — | Válida |
| 959957a0d34e54005a43 | Estado Actual Por Campaña | Rows | General[campaing_name] | — | Válida |
| 959957a0d34e54005a43 | Estado Actual Por Campaña | Values | Medidas[Leads] | — | Válida |
| 959957a0d34e54005a43 | Estado Actual Por Campaña | Formato/propiedad | Calendario[NombreMes] | — | Válida |
| 97e3e193811090b8994d | Año | Values | Calendario[NombreMes] | — | Válida |
| a214c6981c373204ba46 | Año | Values | General[category_name] | — | Válida |
| ab71c6e65080a9eaa82e | Total Leads | Values | Medidas[Leads] | — | Válida |
| c30659788e6c1782a8d0 | Leads Por Mes | Category | Calendario[NombreMes] | — | Válida |
| c30659788e6c1782a8d0 | Leads Por Mes | Series | Calendario[Año] | — | Válida |
| c30659788e6c1782a8d0 | Leads Por Mes | Y | Medidas[Leads] | — | Válida |
| c30659788e6c1782a8d0 | Leads Por Mes | Formato/propiedad | VehiculosEntregados[Gama] | — | Formato huérfano |
| c30659788e6c1782a8d0 | Leads Por Mes | Formato/propiedad | Funnel Digital[Origen] | — | Formato huérfano |
| c36233ee7e7dd9572643 | Año | Values | General[Fuente] | — | Válida |
| c9b042401cc69403d10a | Año | Values | Calendario[Año] | — | Válida |
| ee76c22fe4a2535a2bd9 | Año | Values | General[centro2] | — | Válida |
| fd6649c4e6392049e9c7 | Última Actualización | Values | Parametros[Parametro] | Min | Válida |

## 9.5 Conciliación por página

| page_id | Página | visual.json en PBIP | Fichas | Con binding válido | Decorativos | Botones/acciones | Con referencia rota | Suma | Con formato huérfano (informativo) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 5a5f1a6f0cc9bb4020bc | General | 25 | 25 | 17 | 4 | 4 | 0 | 25 | 2 |
| 5530a675c4ec857bce9b | Detalle | 22 | 22 | 16 | 4 | 2 | 0 | 22 | 2 |
| 62aebec2a6e955dde5c4 | Días | 19 | 19 | 13 | 4 | 2 | 0 | 19 | 1 |
| 512599bb0a5a991b53db | Cita Agendada | 25 | 25 | 17 | 4 | 4 | 0 | 25 | 2 |
| Total | — | 91 | 91 | 63 | 16 | 12 | 0 | 91 | 7 |

La columna «Suma» debe ser igual a «visual.json en PBIP». «Con formato huérfano» no suma: esos visuales ya están contados en su clase.

# 10. KPIs

Se listan los visuales de tipo tarjeta o indicador con lo que calculan realmente. En «Calcula», `Count` es el recuento de valores distintos (opción «Recuento (distintivo)» de Power BI) y `CountNonNull`, el recuento de valores no vacíos (opción «Recuento»: cuenta filas, con repetidos). Las tarjetas cuyo título promete un promedio, valores distintos o una vigencia que el cálculo no hace tienen su fila al inicio de la sección 16 (R65).

Interpretación de cada tarjeta, con certeza Inferido. Las tarjetas usan medidas definidas (sección 7), no recuentos implícitos; el criterio de «gestionado» está pendiente de confirmar en V01.

| Página | visual_id | Título | Calcula | Oculto | Interpretación funcional |
|---|---|---|---|---|---|
| Cita Agendada | 771af917920b90b06662 | % Gestionados | [%Gestionados] | No | Leads gestionados dividido entre total de leads (`%Gestionados`); depende del criterio de V01. |
| Cita Agendada | 7d6ed2b763a573573a60 | Leads Gestionados | [Total Leads sin nuevos] | No | Leads distintos ya gestionados: de Orbi, los que no tienen estado «Nuevo»; de Atom, los que tienen estado «Atendido». El criterio de «gestionado» no es el mismo en ambas fuentes (V01). |
| Cita Agendada | ab71c6e65080a9eaa82e | Total Leads | [Leads] | No | Número de leads distintos (`lead_id`) de la tabla `General`, en el contexto de filtros de la página. En esta página solo cuenta los leads con acción «Cita agendada» (RN17). |
| Cita Agendada | fd6649c4e6392049e9c7 | Última Actualización | Min(Parametros[Parametro]) | No | Fecha y hora de la última carga de datos (`Parametros`). |
| Detalle | 60a8d616a3b762017e01 | Última Actualización | Min(Parametros[Parametro]) | No | Fecha y hora de la última carga de datos (`Parametros`). |
| Detalle | edc2f27420a55ac608b9 | % Gestionados | [%Gestionados] | No | Leads gestionados dividido entre total de leads (`%Gestionados`); depende del criterio de V01. |
| Detalle | f308d59b90290b04cc6e | Leads Gestionados | [Total Leads sin nuevos] | No | Leads distintos ya gestionados: de Orbi, los que no tienen estado «Nuevo»; de Atom, los que tienen estado «Atendido». El criterio de «gestionado» no es el mismo en ambas fuentes (V01). |
| Detalle | ff8e7130d6e0030d10e0 | Total Leads | [Leads] | No | Número de leads distintos (`lead_id`) de la tabla `General`, en el contexto de filtros de la página. |
| General | 97ab69d8068898241489 | % Gestionados | [%Gestionados] | No | Leads gestionados dividido entre total de leads (`%Gestionados`); depende del criterio de V01. |
| General | b281fb425925679b971c | Total Leads | [Leads] | No | Número de leads distintos (`lead_id`) de la tabla `General`, en el contexto de filtros de la página. |
| General | bfe0635e74a280504506 | Última Actualización | Min(Parametros[Parametro]) | No | Fecha y hora de la última carga de datos (`Parametros`). |
| General | e1cec93ba657b6a2ccd6 | Leads Gestionados | [Total Leads sin nuevos] | No | Leads distintos ya gestionados: de Orbi, los que no tienen estado «Nuevo»; de Atom, los que tienen estado «Atendido». El criterio de «gestionado» no es el mismo en ambas fuentes (V01). |
| Días | 362806e0bc36a521ba94 | % Gestionados | [%Gestionados] | No | Leads gestionados dividido entre total de leads (`%Gestionados`); depende del criterio de V01. |
| Días | 681b53b4ca0e1ead507b | Total Leads | [Leads] | No | Número de leads distintos (`lead_id`) de la tabla `General`, en el contexto de filtros de la página. |
| Días | b3e52184e5a5655abb18 | Leads Gestionados | [Total Leads sin nuevos] | No | Leads distintos ya gestionados: de Orbi, los que no tienen estado «Nuevo»; de Atom, los que tienen estado «Atendido». El criterio de «gestionado» no es el mismo en ambas fuentes (V01). |
| Días | f4328e565b1a1cd4c63b | Última Actualización | Min(Parametros[Parametro]) | No | Fecha y hora de la última carga de datos (`Parametros`). |

# 11. Filtros, segmentaciones e interacciones

## 11.1 Filtros (35)

Evidencia: `filterConfig` de `report.json` (Informe), `page.json` (Página) y `visual.json` (Visual).

| filter_id | Ámbito | Página | Visual | Campo | Tipo | Condición | Oculto | Bloqueado | Invertido |
|---|---|---|---|---|---|---|---|---|---|
| 7171fdc25401eb631db2 | Página | 512599bb0a5a991b53db · Cita Agendada | — | General[Action_name] | Categorical | IN (Cita agendada) | No | No | No |
| Filter5417728b44b2c09b6844 | Visual | 512599bb0a5a991b53db · Cita Agendada | 17ef0fc6b0004b9e13c3 · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| b54eba5fa4472040c6c4 | Visual | 512599bb0a5a991b53db · Cita Agendada | 17ef0fc6b0004b9e13c3 · Año | —[—] | Exclude | NOT IN (null) | No | No | No |
| Filter5417728b44b2c09b6844 | Visual | 512599bb0a5a991b53db · Cita Agendada | 20e2c4b5b10d63667b4b · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| 106da4e8a930001b8001 | Visual | 512599bb0a5a991b53db · Cita Agendada | 230203b80cd7dae4c694 · Leads por Medio | General[medium_value] | Categorical | Sin condición guardada | No | No | No |
| 3c4e24e9b097b21e20b0 | Visual | 512599bb0a5a991b53db · Cita Agendada | 230203b80cd7dae4c694 · Leads por Medio | Medidas[Leads] | Advanced | Sin condición guardada | No | No | No |
| Filter5417728b44b2c09b6844 | Visual | 512599bb0a5a991b53db · Cita Agendada | 97e3e193811090b8994d · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 512599bb0a5a991b53db · Cita Agendada | a214c6981c373204ba46 · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 512599bb0a5a991b53db · Cita Agendada | c36233ee7e7dd9572643 · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 512599bb0a5a991b53db · Cita Agendada | c9b042401cc69403d10a · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 512599bb0a5a991b53db · Cita Agendada | ee76c22fe4a2535a2bd9 · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 5530a675c4ec857bce9b · Detalle | 277ff960ee881b05b662 · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 5530a675c4ec857bce9b · Detalle | 4de425c50a2a0d0d7da3 · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 5530a675c4ec857bce9b · Detalle | 974d0f82b136c0620b0e · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 5530a675c4ec857bce9b · Detalle | 9f21e89606a070200443 · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 5530a675c4ec857bce9b · Detalle | c5b0cc52ab0a7dec6d08 · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| b54eba5fa4472040c6c4 | Visual | 5530a675c4ec857bce9b · Detalle | c5b0cc52ab0a7dec6d08 · Año | —[—] | Exclude | NOT IN (null) | No | No | No |
| Filter5417728b44b2c09b6844 | Visual | 5530a675c4ec857bce9b · Detalle | cfe32cda6c909606e1d0 · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 5530a675c4ec857bce9b · Detalle | d696bcc0d275185e560b · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 5a5f1a6f0cc9bb4020bc · General | 18106529a7229a8c0d0b · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 5a5f1a6f0cc9bb4020bc · General | 46483f57c705d050e02a · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 5a5f1a6f0cc9bb4020bc · General | 69d41e746aa9dd6220c2 · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| b54eba5fa4472040c6c4 | Visual | 5a5f1a6f0cc9bb4020bc · General | 69d41e746aa9dd6220c2 · Año | —[—] | Exclude | NOT IN (null) | No | No | No |
| Filter5417728b44b2c09b6844 | Visual | 5a5f1a6f0cc9bb4020bc · General | 7467a556e5287639abb0 · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 5a5f1a6f0cc9bb4020bc · General | a60f74a73c00acb4753c · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 5a5f1a6f0cc9bb4020bc · General | df7b3ec4996816832797 · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 5a5f1a6f0cc9bb4020bc · General | fde6c2de0e14a29ec150 · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 62aebec2a6e955dde5c4 · Días | 0fd661a032712444cd13 · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 62aebec2a6e955dde5c4 · Días | 3ae24a9bc85b696c12d9 · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 62aebec2a6e955dde5c4 · Días | 3b1238777043285beced · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 62aebec2a6e955dde5c4 · Días | 6461e3677819014073d9 · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 62aebec2a6e955dde5c4 · Días | 9ee41b8fb54a31b576cd · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 62aebec2a6e955dde5c4 · Días | d35a3eb2852c48c8eeec · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| Filter5417728b44b2c09b6844 | Visual | 62aebec2a6e955dde5c4 · Días | fe53f0f045aeeb8dcad5 · Año | Calendario[Año] | Categorical | Sin condición guardada | No | No | true |
| b54eba5fa4472040c6c4 | Visual | 62aebec2a6e955dde5c4 · Días | fe53f0f045aeeb8dcad5 · Año | —[—] | Exclude | NOT IN (null) | No | No | No |

## 11.2 Segmentaciones (32)

| visual_id | Segmentación | Página | Modo | Selección única | Grupo de sincronización |
|---|---|---|---|---|---|
| 17ef0fc6b0004b9e13c3 | Año | 512599bb0a5a991b53db · Cita Agendada | Dropdown | false | Gestión |
| 20e2c4b5b10d63667b4b | Año | 512599bb0a5a991b53db · Cita Agendada | Dropdown | false | campaing_name |
| 3cf99ef07474ed230802 | Segmentación: Tipificación (General[tipificacion]) | 512599bb0a5a991b53db · Cita Agendada | Dropdown | false | tipificacion |
| 97e3e193811090b8994d | Año | 512599bb0a5a991b53db · Cita Agendada | Dropdown | false | NombreMes |
| a214c6981c373204ba46 | Año | 512599bb0a5a991b53db · Cita Agendada | Dropdown | false | category_name |
| c36233ee7e7dd9572643 | Año | 512599bb0a5a991b53db · Cita Agendada | Dropdown | false | Fuente |
| c9b042401cc69403d10a | Año | 512599bb0a5a991b53db · Cita Agendada | Dropdown | false | Año |
| ee76c22fe4a2535a2bd9 | Año | 512599bb0a5a991b53db · Cita Agendada | Dropdown | false | centro2 |
| 277ff960ee881b05b662 | Año | 5530a675c4ec857bce9b · Detalle | Dropdown | false | centro2 |
| 4de425c50a2a0d0d7da3 | Año | 5530a675c4ec857bce9b · Detalle | Dropdown | false | Año |
| 762df504015559003b02 | Segmentación: Tipificación (General[tipificacion]) | 5530a675c4ec857bce9b · Detalle | Dropdown | false | tipificacion |
| 974d0f82b136c0620b0e | Año | 5530a675c4ec857bce9b · Detalle | Dropdown | false | category_name |
| 9f21e89606a070200443 | Año | 5530a675c4ec857bce9b · Detalle | Dropdown | false | NombreMes |
| c5b0cc52ab0a7dec6d08 | Año | 5530a675c4ec857bce9b · Detalle | Dropdown | false | Gestión |
| cfe32cda6c909606e1d0 | Año | 5530a675c4ec857bce9b · Detalle | Dropdown | false | Fuente |
| d696bcc0d275185e560b | Año | 5530a675c4ec857bce9b · Detalle | Dropdown | false | campaing_name |
| 0c8ae0466609c5a58590 | Segmentación: Tipificación (General[tipificacion]) | 5a5f1a6f0cc9bb4020bc · General | Dropdown | false | tipificacion |
| 18106529a7229a8c0d0b | Año | 5a5f1a6f0cc9bb4020bc · General | Dropdown | false | centro2 |
| 46483f57c705d050e02a | Año | 5a5f1a6f0cc9bb4020bc · General | Dropdown | false | campaing_name |
| 69d41e746aa9dd6220c2 | Año | 5a5f1a6f0cc9bb4020bc · General | Dropdown | false | Gestión |
| 7467a556e5287639abb0 | Año | 5a5f1a6f0cc9bb4020bc · General | Dropdown | false | Fuente |
| a60f74a73c00acb4753c | Año | 5a5f1a6f0cc9bb4020bc · General | Dropdown | false | Año |
| df7b3ec4996816832797 | Año | 5a5f1a6f0cc9bb4020bc · General | Dropdown | false | NombreMes |
| fde6c2de0e14a29ec150 | Año | 5a5f1a6f0cc9bb4020bc · General | Dropdown | false | category_name |
| 0fd661a032712444cd13 | Año | 62aebec2a6e955dde5c4 · Días | Dropdown | false | NombreMes |
| 2aaac833cc40883a2212 | Segmentación: Tipificación (General[tipificacion]) | 62aebec2a6e955dde5c4 · Días | Dropdown | false | tipificacion |
| 3ae24a9bc85b696c12d9 | Año | 62aebec2a6e955dde5c4 · Días | Dropdown | false | category_name |
| 3b1238777043285beced | Año | 62aebec2a6e955dde5c4 · Días | Dropdown | false | Año |
| 6461e3677819014073d9 | Año | 62aebec2a6e955dde5c4 · Días | Dropdown | false | campaing_name |
| 9ee41b8fb54a31b576cd | Año | 62aebec2a6e955dde5c4 · Días | Dropdown | false | Fuente |
| d35a3eb2852c48c8eeec | Año | 62aebec2a6e955dde5c4 · Días | Dropdown | false | centro2 |
| fe53f0f045aeeb8dcad5 | Año | 62aebec2a6e955dde5c4 · Días | Dropdown | false | Gestión |

## 11.3 Interacciones (0)

Evidencia: `visualInteractions` de cada `page.json`.

_Sin registros._

# 12. Bookmarks, botones y navegación

Evidencia: `GC - Leads MG.Report/definition/bookmarks/<bookmark_id>.bookmark.json`.

## 12.1 Bookmarks (2)

Opciones comunes a la mayoría de los bookmarks: `applyOnlyToTargetVisuals=True`. Solo se indican en la tabla las que difieren.

«Targets» son los visuales a los que se aplica el bookmark (`targetVisualNames`). Un target puede **existir** en el PBIP y aun así **no funcionar** (referencia rota de datos). El estado del bookmark considera ambas cosas.

| bookmark_id | Nombre | Página | Opciones distintas | Targets: total / existen / funcionan | Invocado por | Estado de uso | Motivo |
|---|---|---|---|---|---|---|---|
| 3b896a8209987e360a5e | Leads Campaña | 5a5f1a6f0cc9bb4020bc · General | — | 4 / 4 / 4 | 9ccfba57526b15032805 · Botón Campaña; d66836dfea787b742d87 · Botón Campaña | En uso | Lo invoca un botón o navegador |
| 59657b803a253a4c7c9a | Leads Centro | 5a5f1a6f0cc9bb4020bc · General | — | 4 / 4 / 4 | 2ec568f5aed88ac632b3 · Botón Centro; 22c8e08106520a16532a · Botón Centro | En uso | Lo invoca un botón o navegador |

## 12.2 Detalle de cada bookmark

Una fila por bookmark y efecto. «Se aplica» = lo que realmente pasa al activar el bookmark. «Guardado sin efecto» = estados que Power BI guardó al crear el bookmark (foto de toda la página) pero que no se aplican porque el bookmark solo actúa sobre sus targets (`applyOnlyToTargetVisuals`). Cada visual se lista como `visual_id · nombre · funciona/roto`.

| bookmark_id | Bookmark | Página | Efecto | Cantidad | Visuales (visual_id · nombre · estado) |
|---|---|---|---|---:|---|
| 3b896a8209987e360a5e | Leads Campaña | 5a5f1a6f0cc9bb4020bc · General | Se aplica: muestra | 2 | cd36b94b85c34947cb9e · Estado Actual Por Campaña · funciona; 22c8e08106520a16532a · Botón Centro · funciona |
| 3b896a8209987e360a5e | Leads Campaña | 5a5f1a6f0cc9bb4020bc · General | Se aplica: oculta | 2 | d66836dfea787b742d87 · Botón Campaña · funciona; 31caf527e0784ec8de3d · Leads Por Centro · funciona |
| 3b896a8209987e360a5e | Leads Campaña | 5a5f1a6f0cc9bb4020bc · General | Guardado sin efecto | 19 | Detalle por visual en 12.3 |
| 59657b803a253a4c7c9a | Leads Centro | 5a5f1a6f0cc9bb4020bc · General | Se aplica: muestra | 2 | d66836dfea787b742d87 · Botón Campaña · funciona; 31caf527e0784ec8de3d · Leads Por Centro · funciona |
| 59657b803a253a4c7c9a | Leads Centro | 5a5f1a6f0cc9bb4020bc · General | Se aplica: oculta | 2 | 22c8e08106520a16532a · Botón Centro · funciona; cd36b94b85c34947cb9e · Estado Actual Por Campaña · funciona |
| 59657b803a253a4c7c9a | Leads Centro | 5a5f1a6f0cc9bb4020bc · General | Guardado sin efecto | 19 | Detalle por visual en 12.3 |

## 12.3 Estados guardados sin efecto

Matriz por página: una fila por visual y una columna por bookmark. `O` = guardado oculto, `V` = guardado visible, `·` = sin estado guardado en ese bookmark. Son estados que Power BI guardó en la foto de la página pero que no se aplican porque el bookmark solo actúa sobre sus targets (12.2). Se mapean para que un cambio futuro sobre el bookmark (por ejemplo, quitar `applyOnlyToTargetVisuals`) conozca su efecto.

### 5a5f1a6f0cc9bb4020bc · General

Columnas: **B1** = 3b896a8209987e360a5e · Leads Campaña; **B2** = 59657b803a253a4c7c9a · Leads Centro.

| Visual (visual_id · nombre · estado) | B1 | B2 |
|---|---|---|
| 97ab69d8068898241489 · % Gestionados · funciona | V | V |
| df7b3ec4996816832797 · Año · funciona | V | V |
| a60f74a73c00acb4753c · Año · funciona | V | V |
| 46483f57c705d050e02a · Año · funciona | V | V |
| 18106529a7229a8c0d0b · Año · funciona | V | V |
| 7467a556e5287639abb0 · Año · funciona | V | V |
| fde6c2de0e14a29ec150 · Año · funciona | V | V |
| ae522e0dc253001505b6 · Detalle · funciona | V | V |
| 30ef5613128cb692ea06 · Días · funciona | V | V |
| df2da022b8bd64859b96 · Estado Actual Leads Asesor · funciona | V | V |
| 85f9ad65c309c4985a6b · Forma sin título · funciona | V | V |
| 8130ddd7e08c2704410c · Forma sin título · funciona | V | V |
| 7b7f120ad03e39b73c4d · Imagen: Logo-Nebula22412030801788796.png · funciona | V | V |
| 963042e66cda8a1c0854 · Leads · funciona | V | V |
| e1cec93ba657b6a2ccd6 · Leads Gestionados · funciona | V | V |
| 88852134b360130cbb84 · Leads Por Mes · funciona | V | V |
| aac2f915e77801ddad45 · Leads por Medio · funciona | V | V |
| b281fb425925679b971c · Total Leads · funciona | V | V |
| bfe0635e74a280504506 · Última Actualización · funciona | V | V |

## 12.4 Botones y acciones

| Botón (visual_id · nombre) | Página | Acción | Destino | Bookmark asociado |
|---|---|---|---|---|
| 2ec568f5aed88ac632b3 · Botón Centro | 512599bb0a5a991b53db · Cita Agendada | Bookmark | 62aebec2a6e955dde5c4 · Días | 59657b803a253a4c7c9a · Leads Centro |
| 54bb486e40da053209c5 · Detalle | 512599bb0a5a991b53db · Cita Agendada | PageNavigation | 5530a675c4ec857bce9b · Detalle | Bookmark10e743eaa7b865b22e04 · no existe en el PBIP |
| 9ccfba57526b15032805 · Botón Campaña | 512599bb0a5a991b53db · Cita Agendada | Bookmark | 62aebec2a6e955dde5c4 · Días | 3b896a8209987e360a5e · Leads Campaña |
| b6791fcb998ed58a07ec · Días | 512599bb0a5a991b53db · Cita Agendada | PageNavigation | 62aebec2a6e955dde5c4 · Días | Bookmark10e743eaa7b865b22e04 · no existe en el PBIP |
| 8607acb6d143a7041cc0 · General | 5530a675c4ec857bce9b · Detalle | PageNavigation | 5a5f1a6f0cc9bb4020bc · General | Bookmark10e743eaa7b865b22e04 · no existe en el PBIP |
| 973bc72ab782849a977b · Días | 5530a675c4ec857bce9b · Detalle | PageNavigation | 62aebec2a6e955dde5c4 · Días | Bookmark10e743eaa7b865b22e04 · no existe en el PBIP |
| 22c8e08106520a16532a · Botón Centro | 5a5f1a6f0cc9bb4020bc · General | Bookmark | 62aebec2a6e955dde5c4 · Días | 59657b803a253a4c7c9a · Leads Centro |
| 30ef5613128cb692ea06 · Días | 5a5f1a6f0cc9bb4020bc · General | PageNavigation | 62aebec2a6e955dde5c4 · Días | Bookmark10e743eaa7b865b22e04 · no existe en el PBIP |
| ae522e0dc253001505b6 · Detalle | 5a5f1a6f0cc9bb4020bc · General | PageNavigation | 5530a675c4ec857bce9b · Detalle | Bookmark10e743eaa7b865b22e04 · no existe en el PBIP |
| d66836dfea787b742d87 · Botón Campaña | 5a5f1a6f0cc9bb4020bc · General | Bookmark | 62aebec2a6e955dde5c4 · Días | 3b896a8209987e360a5e · Leads Campaña |
| 58c124ed43032ab5b751 · Detalle | 62aebec2a6e955dde5c4 · Días | PageNavigation | 5530a675c4ec857bce9b · Detalle | Bookmark10e743eaa7b865b22e04 · no existe en el PBIP |
| 7ea9b780b7c30821ee80 · General | 62aebec2a6e955dde5c4 · Días | PageNavigation | 5a5f1a6f0cc9bb4020bc · General | Bookmark10e743eaa7b865b22e04 · no existe en el PBIP |

## 12.5 Tooltips y drillthrough

No encontrado: ninguna página es de tipo Tooltip o Drillthrough.

El efecto real al activar cada bookmark o botón no se ve en los archivos; se declara en 17.1.

# 13. Recursos, tema y presentación

Sección de estética: archivos gráficos, dónde está ubicado cada elemento visual de diseño (banners, logos, formas, textos) y el tema.

## 13.1 Archivos de recursos (3)

Rutas relativas a la carpeta del BI (`C:/dev/MCP_POWERBI/01_bi/01_versiones/00_original/GC - Leads MG`).

| resource_id | Tipo | Ruta del archivo | Peso (bytes) | Tamaño original (px) | Usos | Estado de uso |
|---|---|---|---:|---|---:|---|
| Fluent2-CY26SU08 | BaseTheme | GC - Leads MG.Report/StaticResources/SharedResources/BaseThemes/Fluent2-CY26SU08.json | 99561 | — | 0 | Uso técnico |
| Logo-Nebula22412030801788796.png | Image | GC - Leads MG.Report/StaticResources/RegisteredResources/Logo-Nebula22412030801788796.png | 1750 | 160×36 | 4 | En uso |
| Tema_1_BI_Nebula258303627248908.json | CustomTheme | GC - Leads MG.Report/StaticResources/RegisteredResources/Tema_1_BI_Nebula258303627248908.json | 10050 | — | 0 | Uso técnico |

## 13.2 Ubicación de los elementos de diseño por página

Incluye todo lo que está dentro de un banner (también tarjetas y segmentaciones, porque forman parte de su composición) y, fuera del banner, las imágenes, formas, textos y botones. Un banner es una forma que ocupa al menos el 80 % del ancho de la página; pertenecen a él los elementos que quedan dentro de su franja vertical. Tamaño colocado frente al original indica la escala de cada imagen.

### General (`5a5f1a6f0cc9bb4020bc`)

| Zona | visual_id | Elemento | Rol en el diseño | x | y | Ancho | Alto | z | Oculto | Imagen (archivo · original → colocado) |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|
| Banner superior | 85f9ad65c309c4985a6b | Forma sin título | Fondo del banner | 0 | 0 | 1280 | 156 | 0 | No | — |
| Banner superior | bfe0635e74a280504506 | Última Actualización | Contenido: Tarjeta | 153 | 7 | 226 | 68 | 4000 | No | — |
| Banner superior | 963042e66cda8a1c0854 | Leads | Título / texto | 10 | 13 | 502 | 60 | 1000 | No | — |
| Banner superior | 8130ddd7e08c2704410c | Forma sin título | Forma / fondo de bloque | 130 | 14 | 22 | 55 | 2000 | No | — |
| Banner superior | 7b7f120ad03e39b73c4d | Imagen: Logo-Nebula22412030801788796.png | Logo / imagen | 1144 | 26 | 120 | 22 | 3000 | No | Logo-Nebula22412030801788796.png · 160×36 → 120×22 (75 %) · GC - Leads MG.Report/StaticResources/RegisteredResources/Logo-Nebula22412030801788796.png |
| Banner superior | fde6c2de0e14a29ec150 | Año | Contenido: Segmentación | 429 | 73 | 135 | 70 | 17000 | No | — |
| Banner superior | 18106529a7229a8c0d0b | Año | Contenido: Segmentación | 573 | 73 | 194 | 70 | 18002 | No | — |
| Banner superior | 0c8ae0466609c5a58590 | Segmentación: Tipificación (General[tipificacion]) | Contenido: Segmentación | 773 | 73 | 169 | 70 | 18006 | No | — |
| Banner superior | 7467a556e5287639abb0 | Año | Contenido: Segmentación | 950 | 73 | 148 | 70 | 16000 | No | — |
| Banner superior | 69d41e746aa9dd6220c2 | Año | Contenido: Segmentación | 1105 | 73 | 148 | 70 | 18008 | No | — |
| Banner superior | a60f74a73c00acb4753c | Año | Contenido: Segmentación | 9 | 74 | 109 | 70 | 7000 | No | — |
| Banner superior | df7b3ec4996816832797 | Año | Contenido: Segmentación | 123 | 74 | 130 | 70 | 8000 | No | — |
| Banner superior | 46483f57c705d050e02a | Año | Contenido: Segmentación | 259 | 75 | 165 | 70 | 15000 | No | — |
| Cuerpo de la página | ae522e0dc253001505b6 | Detalle | Botón | 1144 | 166 | 124 | 29 | 5000 | No | — |
| Cuerpo de la página | 30ef5613128cb692ea06 | Días | Botón | 1144 | 199 | 123 | 29 | 18000 | No | — |
| Cuerpo de la página | d66836dfea787b742d87 | Botón Campaña | Botón | 862 | 289 | 122 | 24 | 18005 | No | — |
| Cuerpo de la página | 22c8e08106520a16532a | Botón Centro | Botón | 865 | 289 | 123 | 24 | 18004 | Sí | — |

### Detalle (`5530a675c4ec857bce9b`)

| Zona | visual_id | Elemento | Rol en el diseño | x | y | Ancho | Alto | z | Oculto | Imagen (archivo · original → colocado) |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|
| Banner superior | d49cf8a70de7660a53a9 | Forma sin título | Fondo del banner | 0 | 0 | 1280 | 156 | 0 | No | — |
| Banner superior | 60a8d616a3b762017e01 | Última Actualización | Contenido: Tarjeta | 153 | 7 | 226 | 68 | 4000 | No | — |
| Banner superior | 7e08797f4bd3c07c324b | Leads | Título / texto | 10 | 13 | 502 | 60 | 1000 | No | — |
| Banner superior | 0a8e34e81b960a48dbab | Forma sin título | Forma / fondo de bloque | 130 | 14 | 22 | 55 | 2000 | No | — |
| Banner superior | d81d62b4921ea7c96008 | Imagen: Logo-Nebula22412030801788796.png | Logo / imagen | 1144 | 26 | 120 | 22 | 3000 | No | Logo-Nebula22412030801788796.png · 160×36 → 120×22 (75 %) · GC - Leads MG.Report/StaticResources/RegisteredResources/Logo-Nebula22412030801788796.png |
| Banner superior | 974d0f82b136c0620b0e | Año | Contenido: Segmentación | 429 | 73 | 135 | 70 | 17017 | No | — |
| Banner superior | 277ff960ee881b05b662 | Año | Contenido: Segmentación | 573 | 73 | 194 | 70 | 17018 | No | — |
| Banner superior | 762df504015559003b02 | Segmentación: Tipificación (General[tipificacion]) | Contenido: Segmentación | 773 | 73 | 169 | 70 | 17019 | No | — |
| Banner superior | cfe32cda6c909606e1d0 | Año | Contenido: Segmentación | 950 | 73 | 148 | 70 | 17016 | No | — |
| Banner superior | c5b0cc52ab0a7dec6d08 | Año | Contenido: Segmentación | 1105 | 73 | 148 | 70 | 17020 | No | — |
| Banner superior | 4de425c50a2a0d0d7da3 | Año | Contenido: Segmentación | 9 | 74 | 109 | 70 | 17013 | No | — |
| Banner superior | 9f21e89606a070200443 | Año | Contenido: Segmentación | 123 | 74 | 130 | 70 | 17014 | No | — |
| Banner superior | d696bcc0d275185e560b | Año | Contenido: Segmentación | 259 | 75 | 165 | 70 | 17015 | No | — |
| Cuerpo de la página | 8607acb6d143a7041cc0 | General | Botón | 1146 | 165 | 122 | 30 | 5000 | No | — |
| Cuerpo de la página | 973bc72ab782849a977b | Días | Botón | 1146 | 199 | 123 | 29 | 17000 | No | — |

### Días (`62aebec2a6e955dde5c4`)

| Zona | visual_id | Elemento | Rol en el diseño | x | y | Ancho | Alto | z | Oculto | Imagen (archivo · original → colocado) |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|
| Banner superior | f9f468839301408cb5e5 | Forma sin título | Fondo del banner | 0 | 0 | 1280 | 156 | 0 | No | — |
| Banner superior | f4328e565b1a1cd4c63b | Última Actualización | Contenido: Tarjeta | 153 | 7 | 226 | 68 | 4000 | No | — |
| Banner superior | b7bf50e38a2a650d1cbb | Leads | Título / texto | 10 | 13 | 502 | 60 | 1000 | No | — |
| Banner superior | e3a2959dd6d189491a0b | Forma sin título | Forma / fondo de bloque | 130 | 14 | 22 | 55 | 2000 | No | — |
| Banner superior | ef6046104857770c9edc | Imagen: Logo-Nebula22412030801788796.png | Logo / imagen | 1144 | 26 | 120 | 22 | 3000 | No | Logo-Nebula22412030801788796.png · 160×36 → 120×22 (75 %) · GC - Leads MG.Report/StaticResources/RegisteredResources/Logo-Nebula22412030801788796.png |
| Banner superior | 3ae24a9bc85b696c12d9 | Año | Contenido: Segmentación | 429 | 73 | 135 | 70 | 15010 | No | — |
| Banner superior | d35a3eb2852c48c8eeec | Año | Contenido: Segmentación | 573 | 73 | 194 | 70 | 15011 | No | — |
| Banner superior | 2aaac833cc40883a2212 | Segmentación: Tipificación (General[tipificacion]) | Contenido: Segmentación | 773 | 73 | 169 | 70 | 15012 | No | — |
| Banner superior | 9ee41b8fb54a31b576cd | Año | Contenido: Segmentación | 950 | 73 | 148 | 70 | 15009 | No | — |
| Banner superior | fe53f0f045aeeb8dcad5 | Año | Contenido: Segmentación | 1105 | 73 | 148 | 70 | 15013 | No | — |
| Banner superior | 3b1238777043285beced | Año | Contenido: Segmentación | 9 | 74 | 109 | 70 | 15006 | No | — |
| Banner superior | 0fd661a032712444cd13 | Año | Contenido: Segmentación | 123 | 74 | 130 | 70 | 15007 | No | — |
| Banner superior | 6461e3677819014073d9 | Año | Contenido: Segmentación | 259 | 75 | 165 | 70 | 15008 | No | — |
| Cuerpo de la página | 7ea9b780b7c30821ee80 | General | Botón | 1146 | 165 | 122 | 30 | 14000 | No | — |
| Cuerpo de la página | 58c124ed43032ab5b751 | Detalle | Botón | 1144 | 199 | 123 | 29 | 15000 | No | — |

### Cita Agendada (`512599bb0a5a991b53db`)

| Zona | visual_id | Elemento | Rol en el diseño | x | y | Ancho | Alto | z | Oculto | Imagen (archivo · original → colocado) |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|
| Banner superior | b1dca116d7b5b2b49c25 | Forma sin título | Fondo del banner | 0 | 0 | 1280 | 156 | 0 | No | — |
| Banner superior | fd6649c4e6392049e9c7 | Última Actualización | Contenido: Tarjeta | 153 | 7 | 226 | 68 | 4000 | No | — |
| Banner superior | 11f3f826101a637755eb | Leads | Título / texto | 10 | 13 | 502 | 60 | 1000 | No | — |
| Banner superior | 7f21050ab92b09336526 | Forma sin título | Forma / fondo de bloque | 130 | 14 | 22 | 55 | 2000 | No | — |
| Banner superior | 8cdc2d786b000ae0e42c | Imagen: Logo-Nebula22412030801788796.png | Logo / imagen | 1144 | 26 | 120 | 22 | 3000 | No | Logo-Nebula22412030801788796.png · 160×36 → 120×22 (75 %) · GC - Leads MG.Report/StaticResources/RegisteredResources/Logo-Nebula22412030801788796.png |
| Banner superior | a214c6981c373204ba46 | Año | Contenido: Segmentación | 429 | 73 | 135 | 70 | 24005 | No | — |
| Banner superior | ee76c22fe4a2535a2bd9 | Año | Contenido: Segmentación | 573 | 73 | 194 | 70 | 24006 | No | — |
| Banner superior | 3cf99ef07474ed230802 | Segmentación: Tipificación (General[tipificacion]) | Contenido: Segmentación | 773 | 73 | 169 | 70 | 24007 | No | — |
| Banner superior | c36233ee7e7dd9572643 | Año | Contenido: Segmentación | 950 | 73 | 148 | 70 | 24004 | No | — |
| Banner superior | 17ef0fc6b0004b9e13c3 | Año | Contenido: Segmentación | 1105 | 73 | 148 | 70 | 24008 | No | — |
| Banner superior | c9b042401cc69403d10a | Año | Contenido: Segmentación | 9 | 74 | 109 | 70 | 24001 | No | — |
| Banner superior | 97e3e193811090b8994d | Año | Contenido: Segmentación | 123 | 74 | 130 | 70 | 24002 | No | — |
| Banner superior | 20e2c4b5b10d63667b4b | Año | Contenido: Segmentación | 259 | 75 | 165 | 70 | 24003 | No | — |
| Cuerpo de la página | 54bb486e40da053209c5 | Detalle | Botón | 1144 | 166 | 124 | 29 | 5000 | No | — |
| Cuerpo de la página | b6791fcb998ed58a07ec | Días | Botón | 1144 | 199 | 123 | 29 | 18000 | No | — |
| Cuerpo de la página | 9ccfba57526b15032805 | Botón Campaña | Botón | 862 | 289 | 122 | 24 | 22000 | No | — |
| Cuerpo de la página | 2ec568f5aed88ac632b3 | Botón Centro | Botón | 865 | 289 | 123 | 24 | 21000 | Sí | — |

## 13.3 Tema

| Tema | Nombre | Archivo | dataColors | Fondo | Primer plano | Fuentes |
|---|---|---|---|---|---|---|
| base | Fluent 2 (Preview) | SharedResources/BaseThemes/Fluent2-CY26SU08.json | #118DFF, #12239E, #E66C37, #6B007B, #E044A7, #744EC2, #D9B300, #D64550, #197278, #1AAB40, #15C6F4, #4092FF | #FFFFFF | #242424 | DIN, Segoe UI, Segoe UI Semibold |
| personalizado | Tema 1_BI_Nebula | RegisteredResources/Tema_1_BI_Nebula258303627248908.json | #1A73E8, #8943A7, #AE0A33, #028AB0, #E06806, #1A73E8, #8943A7, #AE0A33, #3599B8, #DFBFBF, #4AC5BB, #5F6B6D | — | — | 'Segoe UI', wf_segoe-ui_normal, helvetica, arial, sans-serif |

## 13.4 Metadatos del proyecto

| Elemento | Valor |
|---|---|
| Archivo .pbip | GC - Leads MG.pbip |
| Modelo referenciado por el reporte | ../GC - Leads MG.SemanticModel |
| Versión PBIR | 4.0 |
| logicalId del reporte | 1b06267e-7de5-4e60-bed1-1f4d8c895954 |
| logicalId del modelo | 375227e1-6720-4319-a999-4d1cca81a751 |
| Página activa al abrir | 5a5f1a6f0cc9bb4020bc · General |

# 14. Reglas de negocio

La implementación remite al objeto que la contiene; el código está en las secciones 4, 6.1 y 11. Los filtros sin condición guardada no son reglas (siguen inventariados en 11.1).

Las reglas RN01 a RN16 se interpretan desde la expresión de la columna (6.1); su significado de negocio es «Inferido» (R51). RN18 a RN20 salen del SQL de la sección 4 (RN18 cita la fila H-A02, R67) y RN21 es una regla de conjunto (R64). Los filtros de página no reparten el tablero en segmentos: solo la página Cita Agendada tiene uno (RN17).

| rule_id | Regla | Implementación (dónde) | Interpretación funcional | Certeza | Validación del dueño | Respuesta del dueño |
|---|---|---|---|---|---|---|
| RN01 | Columna calculada Cruce_Tel | Atom[Cruce_Tel] (6.1) | Une el teléfono del lead con el mes y el año de creación para poder buscarlo entre los teléfonos de los leads de Orbi (`Tel_Orbi`). | Inferido | Pendiente de validación | — |
| RN02 | Columna calculada Cruce_Email | Atom[Cruce_Email] (6.1) | Une el correo del lead con el mes y el año de creación para poder buscarlo entre los correos de los leads de Orbi (`Email_Orbi`). | Inferido | Pendiente de validación | — |
| RN03 | Columna calculada Cruce_Tel_Orbi | Atom[Cruce_Tel_Orbi] (6.1) | Busca el teléfono del lead de Atom en `Tel_Orbi` (mismo teléfono, mes y año); queda vacío si no lo encuentra. | Inferido | Pendiente de validación | — |
| RN04 | Columna calculada Cruce_Email_Orbi | Atom[Cruce_Email_Orbi] (6.1) | Busca el correo del lead de Atom en `Email_Orbi` (mismo correo, mes y año); queda vacío si no lo encuentra. | Inferido | Pendiente de validación | — |
| RN05 | Columna calculada Criterio | Atom[Criterio] (6.1) | Marca «Si» el lead de Atom que no se encontró en Orbi ni por teléfono ni por correo, y «No» el que sí; la tabla `General` solo toma de Atom los marcados «Si» (RN21). | Inferido | Pendiente de validación | — |
| RN06 | Columna calculada management_time2 | Atom[management_time2] (6.1) | Convierte el tiempo de gestión de Atom de minutos a horas (lo divide entre 60). | Inferido | Pendiente de validación | — |
| RN07 | Columna calculada status_name | Atom[status_name] (6.1) | Estado del lead de Atom: «Atendido» si `atendido` es 1 o si es 0 con `atencion` igual a «Si»; «No Atendido» si es 0 y no tiene tipificación; «Sin Identificar» si viene vacío; en los demás casos, «Atendido». | Inferido | Pendiente de validación | — |
| RN08 | Columna calculada atom gestión | Atom[atom gestión] (6.1) | Calcula los minutos entre la asignación del lead de Atom y el primer mensaje del agente. | Inferido | Pendiente de validación | — |
| RN09 | Columna calculada Año | Calendario[Año] (6.1) | Año de la fecha del calendario. | Inferido | Pendiente de validación | — |
| RN10 | Columna calculada Mes | Calendario[Mes] (6.1) | Número de mes (1 a 12) de la fecha del calendario. | Inferido | Pendiente de validación | — |
| RN11 | Columna calculada NombreMes | Calendario[NombreMes] (6.1) | Nombre del mes en español según su número. | Inferido | Pendiente de validación | — |
| RN12 | Columna calculada Dia | Calendario[Dia] (6.1) | Día del mes de la fecha del calendario. | Inferido | Pendiente de validación | — |
| RN13 | Columna calculada Cruce_Email | Email_Orbi[Cruce_Email] (6.1) | Une el correo con el mes y el año para cruzar con Atom (`Cruce_Email` de Atom). | Inferido | Pendiente de validación | — |
| RN14 | Columna calculada centro2 | General[centro2] (6.1) | Homologa 14 nombres de sala de MG Perú al nombre de concesionario usado en el tablero; si el centro no está en la lista, deja el nombre original. | Inferido | Pendiente de validación | — |
| RN15 | Columna calculada Orbi gestión | Orbi leads[Orbi gestión] (6.1) | Clasifica el lead de Orbi como «Mayor a 2 horas» si pasaron más de 120 minutos entre la llegada y la primera gestión; si no, «Menor a 2 horas». | Inferido | Pendiente de validación | — |
| RN16 | Columna calculada Cruce_Tel | Tel_Orbi[Cruce_Tel] (6.1) | Une el teléfono con el mes y el año para cruzar con Atom (`Cruce_Tel` de Atom). | Inferido | Pendiente de validación | — |
| RN17 | Filtro de página en Cita Agendada | 7171fdc25401eb631db2: General[Action_name] IN (Cita agendada) (11.1) | La página Cita Agendada solo muestra leads con acción «Cita agendada». | Encontrado | No requerida | — |
| RN18 | Filtros de carga en la consulta SQL de Atom | Subconsulta de canales (4.1): `where (upper(nombre_campania) like '%MG%' or upper(grupo) like '%MG%') and (lower(canal) like '%MG%' or lower(canal) like '%+%')`; y al final `where not brand_name is null` | Atom carga solo los leads cuyo canal salió de esa subconsulta: campaña o grupo con «MG» y canal con «+». La condición `lower(canal) like '%MG%'` no filtra como parece (nunca se cumple, H-A02), por lo que en la práctica solo cuenta la condición del «+». Los demás leads de `atom_leads.leads` no entran al tablero. | Encontrado | No requerida | — |
| RN19 | Filtro de carga en la consulta SQL de Orbi leads | `where upper(brand_name) like '%MG%'` (4.3) | Orbi leads solo carga leads cuya marca contiene «MG». | Encontrado | No requerida | — |
| RN20 | Un registro por lead en las consultas SQL | `LAST_VALUE(...) OVER (PARTITION BY lead_id ...)` (4.1 y 4.3) | Cada lead llega con los valores de su último registro (por fecha de creación en Orbi y por fecha de asignación en Atom); la primera gestión de Orbi es el primer registro con `status_id` distinto de 1. | Inferido | Pendiente de validación | — |
| RN21 | Regla de conjunto: la tabla `General` combina dos fuentes de leads | RN05, RN18, RN19 y la fórmula de la tabla calculada `General` (6.1) | La tabla `General`, que usan los gráficos, reúne todos los leads de MG de Orbi y solo los leads de Atom que cumplen RN18 y no se encontraron en Orbi (mismo teléfono o correo, en el mismo mes y año). Se distinguen por la columna `Fuente` («Orbi Leads» o «Atom»). | Inferido | Pendiente de validación | — |

# 15. Dependencias

- Medidas más referenciadas por otras medidas: [Total Leads sin nuevos] (1), [Leads] (1).
- Tablas sin relaciones con otras tablas: Email_Orbi, Medidas, Tel_Orbi.

```text
Athena tatooine_prod_core.materialized_leads_tracking (F03) → SQL 4.3 (RN19, RN20) → tabla Orbi leads (oculta) → columna Orbi gestión (RN15)
Athena atom_leads.leads + atom_leads.nebula_tiempos_de_agentes (F01) → SQL 4.1 (RN18, RN20; H-A02) → tabla Atom (oculta) → Cruce_* (RN01–RN04), Criterio (RN05), status_name (RN07), atom gestión (RN08)
Orbi leads → Email_Orbi y Tel_Orbi (calculadas, RN13, RN16) → cruce con Atom (RN03, RN04)
Orbi leads + Atom con Criterio = «Si» → tabla General (calculada, RN21) → columna centro2 (RN14)
General → medidas Leads, Total Leads sin nuevos y %Gestionados (7) → tarjetas y gráficos de las páginas General, Detalle, Días y Cita Agendada → KPIs (10)
General[Fecha] → Calendario (calculada) → Año, Mes, NombreMes y Dia → segmentaciones y ejes de los gráficos
Parametros (F04) → tarjetas «Última Actualización»
Vacíos que afectan el mapa: V01 (criterio de gestionado), V02 (cruce Atom-Orbi)
```

# 16. Hallazgos, vacíos y puntos de revisión

Tabla maestra única (R45): hallazgos, riesgos, observaciones y vacíos de información, una fila por asunto. Las filas `H-A*` y `V-A*` las genera el script; la IA revisa certeza, prioridad e impacto y agrega las de negocio (`H01`, `V01`…). No se repite un asunto que ya cubre otra fila: se ajusta esa fila. La columna «Punto de revisión» no usa verbos de cambio (R47).

Filas H-A y V-A revisadas; las filas `V01`–`V04` son vacíos de negocio agregados en la lectura funcional.

| ID | Tipo | Categoría | Descripción concreta | Página y objeto | page_id | visual_id / object_id (con nombre) | bookmark_id / estado | Evidencia exacta | Certeza | Objetos afectados y dependencias | Impacto | Prioridad | Punto de revisión | Validación requerida | Estado | Respuesta del dueño |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H-A01 | Observación | Presentación | 7 visuales que funcionan conservan reglas de formato que apuntan a entidades inexistentes (Funnel Digital, VehiculosEntregados). Figuran como «Formato huérfano» en los bindings de la sección 9. | Cita Agendada, Detalle, Días, General | 512599bb0a5a991b53db, 5530a675c4ec857bce9b, 5a5f1a6f0cc9bb4020bc, 62aebec2a6e955dde5c4 | 4ccd33593b68ac581943 · Leads Por Centro; c30659788e6c1782a8d0 · Leads Por Mes; 41b98b47ace3073986a1 · Leads Por Estado; bff0421dae410e278066 · Leads Por Mes; 31caf527e0784ec8de3d · Leads Por Centro; 88852134b360130cbb84 · Leads Por Mes; 9eee605dba530a00c130 · Total leads por días del mes | — | Filas «Formato huérfano» en los bindings (sección 9) | Encontrado | Ninguno: la regla no se aplica | Bajo: no afecta los datos mostrados | Baja | Revisar con el dueño si estos formatos heredados de la plantilla deben conservarse. | Sí | Pendiente de validación | — |
| H-A02 | Riesgo | Fuentes | El SQL de «Atom» tiene 1 condición(es) que no filtran como parecen: `lower(canal) like '%MG%'` nunca se cumple. La función convierte el texto a minúsculas (o mayúsculas) y luego lo compara con un texto escrito en el caso contrario. | Modelo | — | Atom | — | Consulta SQL de la sección 4.1 | Encontrado | Filas que carga Atom y todo lo que la usa (6.1) | El tablero puede estar dejando fuera (o dentro) filas que la condición pretendía filtrar | Alta | Confirmar con el dueño qué debía filtrar cada condición y si las filas que hoy carga el tablero son las esperadas. | Sí | Pendiente de validación | — |
| V-A01 | Vacío | Gobierno | No se conoce: Frecuencia y proceso de actualización. | BI | — | — | — | El PBIP no guarda la programación de refresco | Desconocido | — | Vigencia del dato | Media | Confirmar con el dueño. | Sí (paola@nebula.com.co) | Pendiente de validación | — |
| V-A02 | Vacío | Gobierno | No se conoce: Ambiente y workspace de publicación. | BI | — | — | — | Sin evidencia en el PBIP | Desconocido | — | Dónde se consume | Media | Confirmar con el dueño. | Sí (paola@nebula.com.co) | Pendiente de validación | — |
| V-A03 | Vacío | Gobierno | No se conoce: Propietario de cada fuente de la sección 3. | BI | — | — | — | No está en el PBIP | Desconocido | — | Gobierno del dato | Media | Confirmar con el dueño. | Sí (paola@nebula.com.co) | Pendiente de validación | — |
| V01 | Vacío | Métrica | No se conoce el criterio de «gestionado». La medida `Total Leads sin nuevos` cuenta como gestionado el lead de Orbi con estado distinto de «Nuevo» y el lead de Atom con estado «Atendido»; son criterios distintos para cada fuente. Además, el SQL de Orbi calcula la primera gestión con `status_id` distinto de 1 y la medida usa el nombre del estado; no se confirma que ambos signifiquen lo mismo. Lo usan las tarjetas «Leads Gestionados» y «% Gestionados» de las cuatro páginas. | General, Detalle, Días, Cita Agendada | 5a5f1a6f0cc9bb4020bc, 5530a675c4ec857bce9b, 62aebec2a6e955dde5c4, 512599bb0a5a991b53db | 4c3da279-0fc4-4306-b741-b3bcdb56c50d · Total Leads sin nuevos; 11399105-301c-4023-9b14-25bb8385ca8d · %Gestionados | — | Medidas en la sección 7, SQL de la sección 4.3 y tarjetas de la sección 10 | Desconocido | Medida [%Gestionados] y tarjetas «Leads Gestionados» y «% Gestionados» | El porcentaje de gestión podría no ser comparable entre las dos fuentes | Alta | Confirmar con el dueño qué significa «gestionado» y si los criterios de cada fuente son los esperados. | Sí (paola@nebula.com.co) | Pendiente de validación | — |
| V02 | Vacío | Datos | No se conoce si el cruce de leads entre Atom y Orbi es el esperado. `General` toma de Atom solo los leads que no coinciden con uno de Orbi por teléfono o correo, en el mismo mes y año (RN05, RN21). | Modelo | — | 603c0b13-d64f-4b7e-98a4-52d2e9e9b73d · General | — | RN01 a RN05, RN21 y fórmula de `General` (6.1) | Desconocido | Total Leads y todo lo que se mide sobre `General` | Un lead repetido en otro mes o con otro teléfono o correo contaría dos veces; uno distinto con el mismo dato dejaría de contarse | Alta | Confirmar con el dueño que ese criterio de cruce define cuándo un lead de Atom ya está en Orbi. | Sí (paola@nebula.com.co) | Pendiente de validación | — |
| V03 | Vacío | Métrica | No se conoce qué tiempo de gestión debe medir el tablero. Orbi lo mide desde la llegada hasta la primera gestión y lo clasifica contra 2 horas (RN15); Atom lo mide en minutos desde la asignación hasta el primer mensaje del agente, sin umbral (RN08). Ambos van a las columnas `Gestión` y `Tiempo de contacto` de `General`. | Detalle, Días | 5530a675c4ec857bce9b, 62aebec2a6e955dde5c4 | 603c0b13-d64f-4b7e-98a4-52d2e9e9b73d · General | — | RN08, RN15 y fórmula de `General` (6.1) | Desconocido | Visuales que usan `Gestión` y `Tiempo de contacto` | Los dos tiempos tienen punto de partida distinto, así que no son comparables | Media | Confirmar con el dueño si el umbral de 2 horas es la meta y si Orbi y Atom deben medirse desde el mismo momento. | Sí (paola@nebula.com.co) | Pendiente de validación | — |
| V04 | Vacío | Gobierno | No se conoce el público del tablero ni la decisión que apoya, ni por qué tres de sus cuatro páginas están ocultas. | BI | — | — | — | Sin evidencia en el PBIP; páginas Detalle, Días y Cita Agendada ocultas (sección 8) | Desconocido | — | Define si los vacíos y los hallazgos son críticos | Media | Confirmar con el dueño quién usa el tablero y para qué. | Sí (paola@nebula.com.co) | Pendiente de validación | — |

# 17. Limitaciones y control para DLC posteriores

## 17.1 Limitaciones

1. Censo estructural: no se ejecutó el modelo ni se vieron datos; un binding correcto no garantiza el valor mostrado.
2. La base de datos no se consultó: su estructura real sale del catálogo de Athena (3.2), que es una copia y puede estar desactualizada; el uso de columnas fuera del PBIP no es verificable.
3. El efecto en ejecución de bookmarks y botones requiere validación visual en Power BI Desktop.
4. Literales de más de 300 caracteres en M se omiten en el código de la sección 4; el contenido de las tablas embebidas se muestra en 3.3.
5. El censo describe solo la versión analizada del PBIP; los cambios respecto a versiones anteriores están en «[BI] - cambios.md» (R52).

Sin limitaciones adicionales.

## 17.2 Candidatas a depuración

Objetos con estado `Sin uso interno identificado` o `Referencia rota`. Su detalle está en la sección de origen; aquí solo lo que necesita el DLC de depuración. Aprobación de todas: **Pendiente; el CENSO no autoriza eliminar** (R27). Los objetos `En uso` y `Uso técnico` se consideran protegidos. Los formatos huérfanos no son candidatos: su visual funciona.

Riesgo y pruebas por defecto según el tipo de objeto (la IA puede precisarlos en la columna «Nota» de cada fila):

| Tipo | Riesgo por defecto | Pruebas sugeridas |
|---|---|---|
| Columna | Medio: puede tener uso fuera del PBIP (fuente, otros reportes) | Confirmar con el dueño y con la fuente; comparar totales de visuales antes y después |

| # | Tipo | Objeto | ID | Sección | Estado de uso | Nota |
|---:|---|---|---|---|---|---|
| 1 | Columna | Atom[asignado] | 4758a6c9-d5b5-4f58-97bd-1d675e491cca | 6.1 | Sin uso interno identificado | — |
| 2 | Columna | Atom[canal] | 64b531da-a727-468a-b302-21e467afed2c | 6.1 | Sin uso interno identificado | — |
| 3 | Columna | Atom[fh_asignacion_primera] | 88b6527f-6d2d-4a5b-8c9b-f20d6f31e308 | 6.1 | Sin uso interno identificado | — |
| 4 | Columna | General[nombre_origen] | 76240127-1a55-4841-aa24-175e0497697f | 6.1 | Sin uso interno identificado | — |
| 5 | Columna | General[grupo] | 5f367d92-0c67-45a3-bbbe-1b2b24314faf | 6.1 | Sin uso interno identificado | — |
| 6 | Columna | General[primer_usuario] | 16c77d6b-9a73-43b6-a4b9-404af79ca171 | 6.1 | Sin uso interno identificado | — |
| 7 | Columna | General[primer_grupo] | 75480fc9-a2e0-4585-994d-57516882643d | 6.1 | Sin uso interno identificado | — |
| 8 | Columna | General[adviser_email] | 6ea1a2cd-0c20-4400-b675-33fa7b8973ca | 6.1 | Sin uso interno identificado | — |
| 9 | Columna | General[management_time] | 28dac8d4-da5b-4b38-8101-acd9c8f03dbe | 6.1 | Sin uso interno identificado | — |
| 10 | Columna | Orbi leads[id] | 42391bf1-c16e-4b0a-91e2-3958f95733d2 | 6.1 | Sin uso interno identificado | — |
| 11 | Columna | Orbi leads[clasification_id] | a4c00fe8-0670-42f7-a789-105cf137db9f | 6.1 | Sin uso interno identificado | — |
| 12 | Columna | Orbi leads[clasification_name] | b5a511c5-1b24-4285-b311-9f004118535c | 6.1 | Sin uso interno identificado | — |
| 13 | Columna | Orbi leads[action_id] | ddbf884b-ed48-4d92-aabd-79291bbd54cb | 6.1 | Sin uso interno identificado | — |
| 14 | Columna | Orbi leads[status_id] | 06d38462-8dfb-4df7-97f4-18dff2827bf6 | 6.1 | Sin uso interno identificado | — |
| 15 | Columna | Orbi leads[campaing_id] | 75ba5a3a-19d0-4267-92b0-31e5ef0d5051 | 6.1 | Sin uso interno identificado | — |
| 16 | Columna | Orbi leads[channel_id] | 93fc81e5-1c39-45bb-94a5-cc43ba9a7907 | 6.1 | Sin uso interno identificado | — |
| 17 | Columna | Orbi leads[channel_value] | 48cb3405-ee46-4c22-bdeb-0e90e3846e60 | 6.1 | Sin uso interno identificado | — |
| 18 | Columna | Orbi leads[medium_id] | 184959d9-6c15-4725-b513-0856a2edd85f | 6.1 | Sin uso interno identificado | — |
| 19 | Columna | Orbi leads[category_id] | febdf777-9146-425d-aa4f-376d479cc374 | 6.1 | Sin uso interno identificado | — |
| 20 | Columna | Orbi leads[country_name] | 9bef26ff-0035-4e38-9352-2c473c744805 | 6.1 | Sin uso interno identificado | — |
| 21 | Columna | Orbi leads[company_id] | d24c993a-7a61-4e1e-a340-37d7a2654e5e | 6.1 | Sin uso interno identificado | — |
| 22 | Columna | Orbi leads[company_name] | b7915320-5083-43a7-9188-292306c69f42 | 6.1 | Sin uso interno identificado | — |
| 23 | Columna | Orbi leads[brand_id] | bc8a7b7b-61cc-485d-9fd0-27d0c45c4eb5 | 6.1 | Sin uso interno identificado | — |
| 24 | Columna | Orbi leads[wholesaler] | 7dab7caa-13ff-46b8-adde-fbeac6408ff1 | 6.1 | Sin uso interno identificado | — |
| 25 | Columna | Orbi leads[adviser_id] | 7537faec-d96b-4ac3-8b34-823ad6150caa | 6.1 | Sin uso interno identificado | — |
| 26 | Columna | Orbi leads[adviser_document_type] | 5b1f2a28-bcb1-4b77-b988-c4b486f99f08 | 6.1 | Sin uso interno identificado | — |
| 27 | Columna | Orbi leads[adviser_document_number] | 05737df5-707d-435d-823b-fcd1f67626a0 | 6.1 | Sin uso interno identificado | — |
| 28 | Columna | Orbi leads[concessionaire_id] | 99d328fb-39d1-45c9-9f55-b2947597ef12 | 6.1 | Sin uso interno identificado | — |
| 29 | Columna | Orbi leads[client_document_type_name] | 836053dd-6bf6-4dbb-9193-cf456fd2061f | 6.1 | Sin uso interno identificado | — |
| 30 | Columna | Orbi leads[client_document_number] | fc09e986-7c4b-4a5f-ac8d-728b70e02242 | 6.1 | Sin uso interno identificado | — |
| 31 | Columna | Orbi leads[model_id] | a0d2095f-a139-4a64-9d98-5c7588c6aebb | 6.1 | Sin uso interno identificado | — |
| 32 | Columna | Orbi leads[model_name] | 1df62411-1d48-4148-b720-179dce9522c5 | 6.1 | Sin uso interno identificado | — |
| 33 | Columna | Orbi leads[model_year] | 8f4b7854-ea6f-499f-bfc4-ceae1ca77d51 | 6.1 | Sin uso interno identificado | — |
| 34 | Columna | Orbi leads[license_plate] | b8b3e7f7-9d0a-44fb-b4f7-ea0564166131 | 6.1 | Sin uso interno identificado | — |
| 35 | Columna | Orbi leads[adviser_business_type_id] | 57fc2890-0d00-4f98-aadc-82db554ee53e | 6.1 | Sin uso interno identificado | — |
| 36 | Columna | Orbi leads[adviser_business_type] | 7f93fb36-c144-49d7-bf85-fa737fc8e95b | 6.1 | Sin uso interno identificado | — |
| 37 | Columna | Orbi leads[lead_id2] | a2f748f3-2e0f-4d9a-b93b-78f9cc5f25fd | 6.1 | Sin uso interno identificado | — |
| 38 | Columna | Orbi leads[segundos_hasta_gestion] | 572ffdd3-5135-410e-a7a4-86909140735a | 6.1 | Sin uso interno identificado | — |

# 18. Validación final

## 18.1 Conciliación contra el PBIP

| Inventario | En PBIP | En este documento | Diferencia |
|---|---:|---:|---:|
| Tablas | 26 | 26 | 0 |
| Columnas | 253 | 253 | 0 |
| Medidas | 3 | 3 | 0 |
| Relaciones | 18 | 18 | 0 |
| Páginas | 4 | 4 | 0 |
| Visuales | 91 | 91 | 0 |
| Filtros | 35 | 35 | 0 |
| Segmentaciones | 32 | 32 | 0 |
| Interacciones | 0 | 0 | 0 |
| Bookmarks | 2 | 2 | 0 |
| Recursos | 3 | 3 | 0 |

`censo.py validar` recalcula esta tabla desde el documento y el PBIP. El resultado de la validación queda en `historial-censos.md`.

## 18.2 Estado final

Completado pendiente de validación: la conciliación con el PBIP no tiene diferencias y no quedan marcadores sin completar, pero las reglas de negocio inferidas (14) y los puntos de la sección 16 siguen sin confirmar por el dueño (paola@nebula.com.co); quien realizó el censo (miguel.b@nebula.com.co) no es el dueño. Hasta cerrar la validación el tablero no es apto para el DLC de modificación ni para el de depuración (R56).
