# Diccionario de Datos — Nebula Data Lake

Generado automáticamente desde AWS Glue Data Catalog.

Las databases se organizan por **capas del data lake**:

- **🥉 Capa Bronce (raw / ingesta):** datos extraídos directamente de sistemas operacionales (MySQL, SQL Server, Redshift) sin transformación de negocio, más allá del alineamiento de esquema o dedup. El nombre de la database corresponde al sistema/esquema fuente. Incluye la sub-capa de **referencia/maestras** (tablas de lookup cargadas desde CSV que alimentan los joins de la capa plata).
- **🥈 Capa Plata / Materialized (transformada):** datos con lógica de negocio aplicada (normalización, joins, agregaciones, deduplicación conformada). Las databases suelen tener el sufijo `*_materialized_data` o corresponden a la capa Gold de BI. Se derivan de la capa bronce y se consumen desde Athena / Power BI.

> Nota: `stage` es la database de aterrizaje raw (bronce) donde caen tablas `spiga_*`; los jobs `materialized_*` escriben en las databases `*_materialized_data`. Las tablas base de Spiga (SQL Server PSCService) se reparten en dos databases según su cadencia y volumen:
> - **`spiga_dbmlc`**: tablas full de cadencia **diaria** (`migrate-spiga-pscservice-extract`) más los maestros gigantes de terceros de cadencia **semanal** (`migrate-spiga-terceros-semanal`: `spiga_DatosTerceros`, `spiga_Terceros`, `spiga_TercerosCorreos`, `spiga_TercerosTelefonos`, separados del diario para no colgar la cadena cuando la réplica se degrada).
> - **`spiga_dbmlc_incremental`**: tablas transaccionales por periodo con **cargue incremental** (`migrate-spiga-incremental-extract`), particionadas por `anio`/`mes` (`ano_periodo`/`mes_periodo`).
>
> Los jobs de materialización consumen las tablas Spiga desde `spiga_dbmlc` / `spiga_dbmlc_incremental` en lugar de `stage`.

---

## Índice de Schemas por Capa

### 🥉 Capa Bronce (raw / ingesta) — 28 schemas

Fuentes operacionales extraídas sin transformación de negocio.

- [alaris_db](#-alaris_db) (3 tablas)
- [aleen_backend_db](#-aleen_backend_db) (2 tablas)
- [asesor-digital-db](#-asesor-digital-db) (9 tablas)
- [atom_leads](#-atom_leads) (2 tablas)
- [batuu_backend_db](#-batuu_backend_db) (1 tablas)
- [bracca_db](#-bracca_db) (1 tablas)
- [cc_cdn](#-cc_cdn) (6 tablas)
- [cc_cdn_2](#-cc_cdn_2) (1 tablas)
- [clap](#-clap) (3 tablas)
- [cotizaciones_db](#-cotizaciones_db) (1 tablas)
- [endor_prod](#-endor_prod) (12 tablas)
- [eos_prod_core](#-eos_prod_core) (7 tablas)
- [nbp021-byss](#-nbp021-byss) (11 tablas)
- [orbi_atenea](#-orbi_atenea) (9 tablas)
- [runt](#-runt) (4 tablas)
- [seissa](#-seissa) (74 tablas)
- [seissa-analytics](#-seissa-analytics) (4 tablas)
- [sonardd_jdoc_analytics](#-sonardd_jdoc_analytics) (38 tablas)
- [sonardd_jdoc_analytics_cr](#-sonardd_jdoc_analytics_cr) (32 tablas)
- [sonardd_jdoc_data_core_cr](#-sonardd_jdoc_data_core_cr) (30 tablas)
- [sonnard_jdoc_data_core](#-sonnard_jdoc_data_core) (30 tablas)
- [spiga](#-spiga) (49 tablas)
- [spiga_dbmlc](#-spiga_dbmlc) (49 tablas)
- [spiga_dbmlc_incremental](#-spiga_dbmlc_incremental) (14 tablas)
- [stage](#-stage) (98 tablas)
- [taris_db](#-taris_db) (10 tablas)
- [tatooine_prod_core](#-tatooine_prod_core) (1 tablas)
- [usados_casatoro_db](#-usados_casatoro_db) (1 tablas)

#### 📚 Sub-capa Referencia / Maestras — 1 schema

Tablas de lookup (cargadas desde CSV) que alimentan los joins de la capa plata.

- [maestras](#-maestras) (5 tablas)

### 🥈 Capa Plata / Materialized (transformada) — 11 schemas

Datos con lógica de negocio aplicada, derivados de la capa bronce.

- [ nebula_materialized_data](#-nebula_materialized_data) (2 tablas)
- [bi_materialized_data](#-bi_materialized_data) (8 tablas)
- [compra_inteligente](#-compra_inteligente) (9 tablas)
- [data_finanzauto](#-data_finanzauto) (7 tablas)
- [genai](#-genai) (3 tablas)
- [nebula](#-nebula) (8 tablas)
- [nebula_otros](#-nebula_otros) (15 tablas)
- [pricing](#-pricing) (11 tablas)
- [seissa_materialized_data](#-seissa_materialized_data) (35 tablas)
- [silver](#-silver) (1 tablas)
- [spiga_materialized_data](#-spiga_materialized_data) (18 tablas)

---

## 🥈 nebula_materialized_data

`Capa: Plata / Materialized`

###  nebula_materialized_data.vw_tracking_insurance

**Columnas:** 71

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `insurance_entry_id` | decimal(20,0) | YES |  |
| 3 | `case_number` | varchar | YES |  |
| 4 | `origin` | varchar | YES |  |
| 5 | `origin_spiga` | varchar | YES |  |
| 6 | `days_since_creation` | integer | YES |  |
| 7 | `step_id` | decimal(20,0) | YES |  |
| 8 | `step_name` | varchar | YES |  |
| 9 | `insurance_company_id` | decimal(20,0) | YES |  |
| 10 | `insurance_company_name` | varchar | YES |  |
| 11 | `financing_entity_id` | decimal(20,0) | YES |  |
| 12 | `financing_entity_name` | varchar | YES |  |
| 13 | `expired_at` | date | YES |  |
| 14 | `validity_at` | date | YES |  |
| 15 | `amount` | double | YES |  |
| 16 | `vehicle_status` | varchar | YES |  |
| 17 | `placa` | varchar | YES |  |
| 18 | `mileage` | varchar | YES |  |
| 19 | `vehicle_brand` | varchar | YES |  |
| 20 | `vehicle_line` | varchar | YES |  |
| 21 | `vehicle_model` | varchar | YES |  |
| 22 | `vehicle_version` | varchar | YES |  |
| 23 | `vehicle_value` | varchar | YES |  |
| 24 | `version_spiga` | varchar | YES |  |
| 25 | `vin` | varchar | YES |  |
| 26 | `code_fasecolda` | varchar | YES |  |
| 27 | `fuel_spiga` | varchar | YES |  |
| 28 | `circulation_city` | varchar | YES |  |
| 29 | `adviser_spiga_name` | varchar | YES |  |
| 30 | `user_document_type` | varchar | YES |  |
| 31 | `user_identification_number` | bigint | YES |  |
| 32 | `user_first_name` | varchar | YES |  |
| 33 | `user_second_name` | varchar | YES |  |
| 34 | `user_surname` | varchar | YES |  |
| 35 | `user_second_surname` | varchar | YES |  |
| 36 | `user_phone` | varchar | YES |  |
| 37 | `user_email` | varchar | YES |  |
| 38 | `user_birthdate` | varchar | YES |  |
| 39 | `user_gender` | varchar | YES |  |
| 40 | `user_residence_address` | varchar | YES |  |
| 41 | `user_residence_city` | varchar | YES |  |
| 42 | `company_group_id` | decimal(20,0) | YES |  |
| 43 | `company_group_agile_id` | varchar | YES |  |
| 44 | `company_group_spiga_id` | varchar | YES |  |
| 45 | `company_group_name` | varchar | YES |  |
| 46 | `company_id` | decimal(20,0) | YES |  |
| 47 | `company_agile_id` | varchar | YES |  |
| 48 | `company_spiga_id` | varchar | YES |  |
| 49 | `company_name` | varchar | YES |  |
| 50 | `headquarter_id` | decimal(20,0) | YES |  |
| 51 | `headquarter_agile_id` | varchar | YES |  |
| 52 | `headquarter_spiga_id` | varchar | YES |  |
| 53 | `headquarter_name` | varchar | YES |  |
| 54 | `adviser_manager_id` | decimal(20,0) | YES |  |
| 55 | `adviser_manager_identification_number` | bigint | YES |  |
| 56 | `adviser_manager_name` | varchar | YES |  |
| 57 | `adviser_manager_email` | varchar | YES |  |
| 58 | `adviser_id` | decimal(20,0) | YES |  |
| 59 | `adviser_identification_number` | bigint | YES |  |
| 60 | `adviser_name` | varchar | YES |  |
| 61 | `adviser_email` | varchar | YES |  |
| 62 | `date_time_response` | timestamp(3) | YES |  |
| 63 | `insurance_entity_id` | decimal(20,0) | YES |  |
| 64 | `insurance_entity_name` | varchar | YES |  |
| 65 | `response_time` | bigint | YES |  |
| 66 | `finished_at` | varchar | YES |  |
| 67 | `created_at` | timestamp(3) | YES |  |
| 68 | `updated_at` | timestamp(3) | YES |  |
| 69 | `created_at_invoice` | varchar | YES |  |
| 70 | `created_at_delivery` | varchar | YES |  |
| 71 | `created_at_quotation` | timestamp(3) | YES |  |

###  nebula_materialized_data.vw_traking

**Columnas:** 36

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `financing_entry_id` | decimal(20,0) | YES |  |
| 3 | `case_number` | varchar | YES |  |
| 4 | `days_since_creation` | integer | YES |  |
| 5 | `step_id` | decimal(20,0) | YES |  |
| 6 | `step_name` | varchar | YES |  |
| 7 | `approved_amount` | double | YES |  |
| 8 | `approved_rate` | double | YES |  |
| 9 | `approved_terms_months` | integer | YES |  |
| 10 | `rejection_cause` | varchar | YES |  |
| 11 | `adviser_manager_id` | decimal(20,0) | YES |  |
| 12 | `adviser_manager_identification_number` | bigint | YES |  |
| 13 | `adviser_manager_name` | varchar | YES |  |
| 14 | `adviser_manager_email` | varchar | YES |  |
| 15 | `adviser_id` | decimal(20,0) | YES |  |
| 16 | `adviser_identification_number` | bigint | YES |  |
| 17 | `adviser_name` | varchar | YES |  |
| 18 | `adviser_email` | varchar | YES |  |
| 19 | `date_time_response` | timestamp(3) | YES |  |
| 20 | `financing_entity_id` | decimal(20,0) | YES |  |
| 21 | `financing_entity_name` | varchar | YES |  |
| 22 | `company_group_id` | decimal(20,0) | YES |  |
| 23 | `company_group_agile_id` | varchar | YES |  |
| 24 | `company_group_spiga_id` | varchar | YES |  |
| 25 | `company_group_name` | varchar | YES |  |
| 26 | `company_id` | decimal(20,0) | YES |  |
| 27 | `company_agile_id` | varchar | YES |  |
| 28 | `company_spiga_id` | varchar | YES |  |
| 29 | `company_name` | varchar | YES |  |
| 30 | `headquarter_id` | decimal(20,0) | YES |  |
| 31 | `headquarter_agile_id` | varchar | YES |  |
| 32 | `headquarter_spiga_id` | varchar | YES |  |
| 33 | `headquarter_name` | varchar | YES |  |
| 34 | `response_time` | bigint | YES |  |
| 35 | `finished_at` | varchar | YES |  |
| 36 | `created_at` | timestamp(3) | YES |  |

## 🥉 alaris_db

`Capa: Bronce / Raw`

### alaris_db.license_plates_view

**Columnas:** 37

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `placa` | varchar | YES |  |
| 3 | `asignacion_placa` | varchar | YES |  |
| 4 | `marca` | varchar | YES |  |
| 5 | `cf` | varchar | YES |  |
| 6 | `ch` | varchar | YES |  |
| 7 | `vehicle_price` | decimal(15,2) | YES |  |
| 8 | `linea` | varchar | YES |  |
| 9 | `empresa` | varchar | YES |  |
| 10 | `empresa_id` | integer | YES |  |
| 11 | `sede` | varchar | YES |  |
| 12 | `center_id` | integer | YES |  |
| 13 | `line_id` | varchar | YES |  |
| 14 | `asesor` | varchar | YES |  |
| 15 | `cedula_asesor` | varchar | YES |  |
| 16 | `correo_asesor` | varchar | YES |  |
| 17 | `analista` | varchar | YES |  |
| 18 | `cedula_analista` | varchar | YES |  |
| 19 | `correo_analista` | varchar | YES |  |
| 20 | `fecha_solicitud` | timestamp(3) | YES |  |
| 21 | `fecha_de_inicio` | timestamp(3) | YES |  |
| 22 | `prenda` | varchar | YES |  |
| 23 | `entidad_financiera` | varchar | YES |  |
| 24 | `estado_soat` | varchar | YES |  |
| 25 | `fecha_solicitud_soat` | timestamp(3) | YES |  |
| 26 | `estado_impuesto` | varchar | YES |  |
| 27 | `fecha_solicitud_pago_impuesto` | timestamp(3) | YES |  |
| 28 | `fecha_de_en_radicacion` | timestamp(3) | YES |  |
| 29 | `fecha_de_aprobado` | timestamp(3) | YES |  |
| 30 | `fecha_tp_placa_fisica` | timestamp(3) | YES |  |
| 31 | `fecha_de_finalizado` | timestamp(3) | YES |  |
| 32 | `estado_actual` | varchar | YES |  |
| 33 | `fecha_novedad_1` | timestamp(3) | YES |  |
| 34 | `motivo_novedad_1` | varchar | YES |  |
| 35 | `fecha_novedad_2` | timestamp(3) | YES |  |
| 36 | `motivo_novedad_2` | varchar | YES |  |
| 37 | `bonos` | varchar | YES |  |

### alaris_db.purchase_transfer_view

**Columnas:** 35

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `placa` | varchar | YES |  |
| 3 | `asignacion_placa` | varchar | YES |  |
| 4 | `marca` | varchar | YES |  |
| 5 | `cf` | varchar | YES |  |
| 6 | `ch` | varchar | YES |  |
| 7 | `vehicle_price` | decimal(15,2) | YES |  |
| 8 | `empresa` | varchar | YES |  |
| 9 | `empresa_id` | integer | YES |  |
| 10 | `linea` | varchar | YES |  |
| 11 | `linea_id` | varchar | YES |  |
| 12 | `sede` | varchar | YES |  |
| 13 | `sede_id` | integer | YES |  |
| 14 | `asesor` | varchar | YES |  |
| 15 | `cedula_asesor` | varchar | YES |  |
| 16 | `analista` | varchar | YES |  |
| 17 | `cedula_analista` | varchar | YES |  |
| 18 | `correo_analista` | varchar | YES |  |
| 19 | `fecha_solicitud` | timestamp(3) | YES |  |
| 20 | `fecha_de_inicio` | timestamp(3) | YES |  |
| 21 | `prenda` | varchar | YES |  |
| 22 | `entidad_financiera` | varchar | YES |  |
| 23 | `estado_pagos` | varchar | YES |  |
| 24 | `estado_paz_y_salvo` | varchar | YES |  |
| 25 | `fecha_de_pte_documentos` | timestamp(3) | YES |  |
| 26 | `fecha_de_en_radicacion` | timestamp(3) | YES |  |
| 27 | `fecha_de_pte_entrega_tp` | timestamp(3) | YES |  |
| 28 | `fecha_de_finalizado` | timestamp(3) | YES |  |
| 29 | `estado_actual` | varchar | YES |  |
| 30 | `fecha_rechazo` | timestamp(3) | YES |  |
| 31 | `motivo_rechazo` | varchar | YES |  |
| 32 | `fecha_novedad_1` | timestamp(3) | YES |  |
| 33 | `motivo_novedad_1` | varchar | YES |  |
| 34 | `fecha_novedad_2` | timestamp(3) | YES |  |
| 35 | `motivo_novedad_2` | varchar | YES |  |

### alaris_db.sales_transfer_view

**Columnas:** 34

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `placa` | varchar | YES |  |
| 3 | `asignacion_placa` | varchar | YES |  |
| 4 | `marca` | varchar | YES |  |
| 5 | `cf` | varchar | YES |  |
| 6 | `ch` | varchar | YES |  |
| 7 | `vehicle_price` | decimal(15,2) | YES |  |
| 8 | `empresa` | varchar | YES |  |
| 9 | `empresa_id` | integer | YES |  |
| 10 | `linea` | varchar | YES |  |
| 11 | `linea_id` | varchar | YES |  |
| 12 | `sede` | varchar | YES |  |
| 13 | `sede_id` | integer | YES |  |
| 14 | `asesor` | varchar | YES |  |
| 15 | `cedula_asesor` | varchar | YES |  |
| 16 | `analista` | varchar | YES |  |
| 17 | `cedula_analista` | varchar | YES |  |
| 18 | `correo_analista` | varchar | YES |  |
| 19 | `fecha_solicitud` | timestamp(3) | YES |  |
| 20 | `fecha_de_inicio` | timestamp(3) | YES |  |
| 21 | `prenda` | varchar | YES |  |
| 22 | `entidad_financiera` | varchar | YES |  |
| 23 | `estado_pagos` | varchar | YES |  |
| 24 | `fecha_de_pte_documentos` | timestamp(3) | YES |  |
| 25 | `fecha_de_en_radicacion` | timestamp(3) | YES |  |
| 26 | `fecha_de_pte_entrega_tp` | timestamp(3) | YES |  |
| 27 | `fecha_de_finalizado` | timestamp(3) | YES |  |
| 28 | `estado_actual` | varchar | YES |  |
| 29 | `fecha_rechazo` | timestamp(3) | YES |  |
| 30 | `motivo_rechazo` | varchar | YES |  |
| 31 | `fecha_novedad_1` | timestamp(3) | YES |  |
| 32 | `motivo_novedad_1` | varchar | YES |  |
| 33 | `fecha_novedad_2` | timestamp(3) | YES |  |
| 34 | `motivo_novedad_2` | varchar | YES |  |

## 🥉 aleen_backend_db

`Capa: Bronce / Raw`

### aleen_backend_db.vw_download

**Columnas:** 3

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `app_key` | varchar | YES |  |
| 2 | `units` | integer | YES |  |
| 3 | `created_at` | timestamp(3) | YES |  |

### aleen_backend_db.vw_user_app

**Columnas:** 7

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `full_name` | varchar | YES |  |
| 2 | `email` | varchar | YES |  |
| 3 | `document` | varchar | YES |  |
| 4 | `vehicles` | bigint | YES |  |
| 5 | `company_spiga_id` | integer | YES |  |
| 6 | `created_at` | timestamp(3) | YES |  |
| 7 | `last_login` | timestamp(3) | YES |  |

## 🥉 asesor-digital-db

`Capa: Bronce / Raw`

### asesor-digital-db.campaigns

**Columnas:** 32

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `name` | varchar | YES |  |
| 3 | `status` | varchar | YES |  |
| 4 | `start_date` | date | YES |  |
| 5 | `end_date` | date | YES |  |
| 6 | `end_hour` | varchar | YES |  |
| 7 | `type_campaign` | varchar | YES |  |
| 8 | `type_campaign_special` | varchar | YES |  |
| 9 | `category` | varchar | YES |  |
| 10 | `category_id` | bigint | YES |  |
| 11 | `distributor_id` | bigint | YES |  |
| 12 | `business_line` | bigint | YES |  |
| 13 | `email_special` | varchar | YES |  |
| 14 | `means_id` | bigint | YES |  |
| 15 | `config_manual_user` | smallint | YES |  |
| 16 | `brand_company_id` | integer | YES |  |
| 17 | `sub_brand_id` | bigint | YES |  |
| 18 | `postmark_id` | varchar | YES |  |
| 19 | `breaker_nodriza` | varchar | YES |  |
| 20 | `breaker_poll` | varchar | YES |  |
| 21 | `template_id` | bigint | YES |  |
| 22 | `breaker_spiga` | varchar | YES |  |
| 23 | `breaker_alert` | varchar | YES |  |
| 24 | `breaker_option_alert` | varchar | YES |  |
| 25 | `ids_alert_adviser` | varchar | YES |  |
| 26 | `first_time` | bigint | YES |  |
| 27 | `second_time` | bigint | YES |  |
| 28 | `third_time` | bigint | YES |  |
| 29 | `created_at` | timestamp(3) | YES |  |
| 30 | `updated_at` | timestamp(3) | YES |  |
| 31 | `manage_duplicates` | varchar | YES |  |
| 32 | `activate_email_delivery` | varchar | YES |  |

### asesor-digital-db.leads_bag

**Columnas:** 22

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `name` | varchar | YES |  |
| 3 | `phone` | varchar | YES |  |
| 4 | `email` | varchar | YES |  |
| 5 | `type_of_assignment` | varchar | YES |  |
| 6 | `current_status` | varchar | YES |  |
| 7 | `jsondata` | varchar | YES |  |
| 8 | `emailplanin` | varchar | YES |  |
| 9 | `commission` | varchar | YES |  |
| 10 | `way` | varchar | YES |  |
| 11 | `outstanding` | varchar | YES |  |
| 12 | `qualification` | varchar | YES |  |
| 13 | `message` | varchar | YES |  |
| 14 | `campaign_id` | bigint | YES |  |
| 15 | `last_management_id` | varchar | YES |  |
| 16 | `interested_model` | varchar | YES |  |
| 17 | `interested_version` | varchar | YES |  |
| 18 | `plate` | varchar | YES |  |
| 19 | `campus_scheduling` | varchar | YES |  |
| 20 | `lead_alert_cycle` | varchar | YES |  |
| 21 | `created_at` | timestamp(3) | YES |  |
| 22 | `updated_at` | timestamp(3) | YES |  |

### asesor-digital-db.managements

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `name` | varchar | YES |  |
| 3 | `status` | varchar | YES |  |
| 4 | `status_lead_id` | varchar | YES |  |
| 5 | `reason_id` | varchar | YES |  |
| 6 | `reason_taller_id` | varchar | YES |  |
| 7 | `reason_repuestos_id` | varchar | YES |  |
| 8 | `reason_latoneria_id` | varchar | YES |  |
| 9 | `reason_accesorios_id` | varchar | YES |  |
| 10 | `reason_carrotaller_id` | varchar | YES |  |
| 11 | `created_at` | timestamp(3) | YES |  |
| 12 | `updated_at` | timestamp(3) | YES |  |

### asesor-digital-db.parameters

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `value` | varchar | YES |  |
| 3 | `status` | varchar | YES |  |
| 4 | `is_dependent_of_parameter` | varchar | YES |  |
| 5 | `parameter_dependent_id` | varchar | YES |  |
| 6 | `group_id` | bigint | YES |  |
| 7 | `created_at` | timestamp(3) | YES |  |
| 8 | `updated_at` | timestamp(3) | YES |  |

### asesor-digital-db.records

**Columnas:** 11

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `description` | varchar | YES |  |
| 3 | `user_id` | bigint | YES |  |
| 4 | `lead_owner_id` | varchar | YES |  |
| 5 | `leads_bag_id` | bigint | YES |  |
| 6 | `management_id` | bigint | YES |  |
| 7 | `management_commentary_id` | varchar | YES |  |
| 8 | `leads_bag_state_id` | varchar | YES |  |
| 9 | `observation` | varchar | YES |  |
| 10 | `created_at` | timestamp(3) | YES |  |
| 11 | `updated_at` | timestamp(3) | YES |  |

### asesor-digital-db.report_av_version1

**Columnas:** 72

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `lead_id` | varchar | YES |  |
| 3 | `brand_id` | varchar | YES |  |
| 4 | `brand_name` | varchar | YES |  |
| 5 | `sub_brand_id` | bigint | YES |  |
| 6 | `sub_brand` | varchar | YES |  |
| 7 | `link_contact` | varchar | YES |  |
| 8 | `date` | timestamp(3) | YES |  |
| 9 | `name_client` | varchar | YES |  |
| 10 | `email` | varchar | YES |  |
| 11 | `phone` | varchar | YES |  |
| 12 | `adviser_id` | bigint | YES |  |
| 13 | `name_adviser` | varchar | YES |  |
| 14 | `name_concessionaire` | varchar | YES |  |
| 15 | `concessionaire_id` | bigint | YES |  |
| 16 | `status` | varchar | YES |  |
| 17 | `first_management_date` | timestamp(3) | YES |  |
| 18 | `last_management_date` | timestamp(3) | YES |  |
| 19 | `name_first_management` | varchar | YES |  |
| 20 | `campaign_id` | varchar | YES |  |
| 21 | `name_campaign` | varchar | YES |  |
| 22 | `last_comment` | varchar | YES |  |
| 23 | `management_id` | bigint | YES |  |
| 24 | `management` | varchar | YES |  |
| 25 | `management_commentary_id` | bigint | YES |  |
| 26 | `management_commentary` | varchar | YES |  |
| 27 | `authorize_contact` | varchar | YES |  |
| 28 | `terms_conditions` | varchar | YES |  |
| 29 | `authorize` | varchar | YES |  |
| 30 | `type_document` | varchar | YES |  |
| 31 | `document_number` | varchar | YES |  |
| 32 | `serial_number` | varchar | YES |  |
| 33 | `model` | varchar | YES |  |
| 34 | `name_city` | varchar | YES |  |
| 35 | `vehicle_interested` | varchar | YES |  |
| 36 | `category_id` | bigint | YES |  |
| 37 | `name_category` | varchar | YES |  |
| 38 | `medium_id` | bigint | YES |  |
| 39 | `name_medium` | varchar | YES |  |
| 40 | `name_submedium` | varchar | YES |  |
| 41 | `product` | varchar | YES |  |
| 42 | `business_line_id` | bigint | YES |  |
| 43 | `business_line` | varchar | YES |  |
| 44 | `name_model` | varchar | YES |  |
| 45 | `distributor_id` | bigint | YES |  |
| 46 | `distributor` | varchar | YES |  |
| 47 | `model_generic` | varchar | YES |  |
| 48 | `model_year` | varchar | YES |  |
| 49 | `license_plate` | varchar | YES |  |
| 50 | `campus_scheduling` | varchar | YES |  |
| 51 | `mileage` | varchar | YES |  |
| 52 | `last_revision` | varchar | YES |  |
| 53 | `utm_source` | varchar | YES |  |
| 54 | `utm_medium` | varchar | YES |  |
| 55 | `alert_type` | varchar | YES |  |
| 56 | `failure_code` | varchar | YES |  |
| 57 | `fault_description` | varchar | YES |  |
| 58 | `how_did_you_find_out` | varchar | YES |  |
| 59 | `organization_name` | varchar | YES |  |
| 60 | `notification_reference` | varchar | YES |  |
| 61 | `timestamp_v1` | varchar | YES |  |
| 62 | `machine_pin` | varchar | YES |  |
| 63 | `machine_brand` | varchar | YES |  |
| 64 | `machine_model` | varchar | YES |  |
| 65 | `severity` | varchar | YES |  |
| 66 | `diagnostic_codes` | varchar | YES |  |
| 67 | `market_stall` | varchar | YES |  |
| 68 | `repetitions` | varchar | YES |  |
| 69 | `duration` | varchar | YES |  |
| 70 | `engine_hours` | varchar | YES |  |
| 71 | `created_at` | timestamp(3) | YES |  |
| 72 | `updated_at` | timestamp(3) | YES |  |

### asesor-digital-db.report_qlik_copy

**Columnas:** 28

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `lead_id` | bigint | YES |  |
| 3 | `brand_id` | integer | YES |  |
| 4 | `sub_brand_id` | bigint | YES |  |
| 5 | `creation_date_lead` | date | YES |  |
| 6 | `update_date_lead` | date | YES |  |
| 7 | `end_date` | date | YES |  |
| 8 | `total_management_hours` | varchar | YES |  |
| 9 | `total_management_minutes` | varchar | YES |  |
| 10 | `adviser_id` | bigint | YES |  |
| 11 | `campus_id` | bigint | YES |  |
| 12 | `city_id` | bigint | YES |  |
| 13 | `status_id` | bigint | YES |  |
| 14 | `total_status_hours` | varchar | YES |  |
| 15 | `total_status_minutes` | varchar | YES |  |
| 16 | `total_status_days` | varchar | YES |  |
| 17 | `total_status_hms` | varchar | YES |  |
| 18 | `campaign_id` | bigint | YES |  |
| 19 | `type_of_register` | varchar | YES |  |
| 20 | `medium` | varchar | YES |  |
| 21 | `category_id` | bigint | YES |  |
| 22 | `management_id` | bigint | YES |  |
| 23 | `distributor_id` | bigint | YES |  |
| 24 | `business_line_id` | bigint | YES |  |
| 25 | `license_plate` | varchar | YES |  |
| 26 | `campus_scheduling_id` | bigint | YES |  |
| 27 | `created_at` | timestamp(3) | YES |  |
| 28 | `updated_at` | timestamp(3) | YES |  |

### asesor-digital-db.status

**Columnas:** 9

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `name` | varchar | YES |  |
| 3 | `class_icon` | varchar | YES |  |
| 4 | `sn_webhook` | varchar | YES |  |
| 5 | `webhook_url` | varchar | YES |  |
| 6 | `status_after_webhook` | varchar | YES |  |
| 7 | `color` | varchar | YES |  |
| 8 | `created_at` | timestamp(3) | YES |  |
| 9 | `updated_at` | timestamp(3) | YES |  |

### asesor-digital-db.users

**Columnas:** 24

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `name` | varchar | YES |  |
| 3 | `email` | varchar | YES |  |
| 4 | `password` | varchar | YES |  |
| 5 | `api_token` | varchar | YES |  |
| 6 | `type` | varchar | YES |  |
| 7 | `access_token` | varchar | YES |  |
| 8 | `status` | varchar | YES |  |
| 9 | `counter` | bigint | YES |  |
| 10 | `profile_id` | bigint | YES |  |
| 11 | `cell_phone_number` | varchar | YES |  |
| 12 | `category_id` | bigint | YES |  |
| 13 | `online_availability` | varchar | YES |  |
| 14 | `user_manager_id` | bigint | YES |  |
| 15 | `user_spiga_id` | bigint | YES |  |
| 16 | `user_spiga_company` | bigint | YES |  |
| 17 | `user_spiga_center` | bigint | YES |  |
| 18 | `email_report` | varchar | YES |  |
| 19 | `survey_assistant` | varchar | YES |  |
| 20 | `image_name` | varchar | YES |  |
| 21 | `remember_token` | varchar | YES |  |
| 22 | `created_at` | timestamp(3) | YES |  |
| 23 | `updated_at` | timestamp(3) | YES |  |
| 24 | `identification_card` | varchar | YES |  |

## 🥉 atom_leads

`Capa: Bronce / Raw`

### atom_leads.leads

**Columnas:** 32

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `lead_id` | varchar | YES |  |
| 2 | `url` | varchar | YES |  |
| 3 | `fecha_inicio_conversacion` | timestamp(3) | YES |  |
| 4 | `canal` | varchar | YES |  |
| 5 | `nombre_cliente` | varchar | YES |  |
| 6 | `telefono` | varchar | YES |  |
| 7 | `correo` | varchar | YES |  |
| 8 | `inbound_outbound` | varchar | YES |  |
| 9 | `tipo_de_origen` | varchar | YES |  |
| 10 | `nombre_origen` | varchar | YES |  |
| 11 | `asignado` | varchar | YES |  |
| 12 | `grupo` | varchar | YES |  |
| 13 | `agente` | varchar | YES |  |
| 14 | `id_agente` | varchar | YES |  |
| 15 | `email_agente` | varchar | YES |  |
| 16 | `fecha_asignacion` | timestamp(3) | YES |  |
| 17 | `atendido` | varchar | YES |  |
| 18 | `categoria_atencion` | varchar | YES |  |
| 19 | `fh_primer_mensaje_agente` | timestamp(3) | YES |  |
| 20 | `tiempo_primer_respuesta` | varchar | YES |  |
| 21 | `tiempo_promedio_de_respuesta` | varchar | YES |  |
| 22 | `tiempo_de_atencion` | varchar | YES |  |
| 23 | `tipificacion` | varchar | YES |  |
| 24 | `nombre_campania` | varchar | YES |  |
| 25 | `ult_fecha_reasignacion` | timestamp(3) | YES |  |
| 26 | `primer_usuario` | varchar | YES |  |
| 27 | `primer_grupo` | varchar | YES |  |
| 28 | `ultima_actualizacion` | timestamp(3) | YES |  |
| 29 | `customtipodenegocio` | varchar | YES |  |
| 30 | `custommotivodeconversacion` | varchar | YES |  |
| 31 | `customcodigointernodesurcursal` | varchar | YES |  |
| 32 | `customcodigointernodmarca` | varchar | YES |  |

### atom_leads.nebula_tiempos_de_agentes

**Columnas:** 17

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `url` | varchar | YES |  |
| 2 | `lead_id` | varchar | YES |  |
| 3 | `numero_telefono` | varchar | YES |  |
| 4 | `grupo` | varchar | YES |  |
| 5 | `fh_primer_mensaje` | varchar | YES |  |
| 6 | `agente` | varchar | YES |  |
| 7 | `email_agente` | varchar | YES |  |
| 8 | `fh_asignacion` | varchar | YES |  |
| 9 | `tiempo_de_primera_respuesta` | varchar | YES |  |
| 10 | `fh_primer_mensaje_agente` | varchar | YES |  |
| 11 | `tiempo_promedio_de_respuesta` | varchar | YES |  |
| 12 | `channel_name` | varchar | YES |  |
| 13 | `tiempo_de_atencion` | varchar | YES |  |
| 14 | `ultima_actualizacion` | timestamp(3) | YES |  |
| 15 | `source` | varchar | YES |  |
| 16 | `atencion` | varchar | YES |  |
| 17 | `categoria_atencion` | varchar | YES |  |

## 🥉 batuu_backend_db

`Capa: Bronce / Raw`

### batuu_backend_db.buybags_view

**Columnas:** 18

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `plate` | varchar | YES |  |
| 3 | `sede` | varchar | YES |  |
| 4 | `id_empresa` | integer | YES |  |
| 5 | `id_centro` | integer | YES |  |
| 6 | `id_line` | varchar | YES |  |
| 7 | `created_at` | timestamp(3) | YES |  |
| 8 | `adviser_name` | varchar | YES |  |
| 9 | `adviser_document` | varchar | YES |  |
| 10 | `adviser_email` | varchar | YES |  |
| 11 | `buyer_name` | varchar | YES |  |
| 12 | `buyer_document` | varchar | YES |  |
| 13 | `standard` | varchar | YES |  |
| 14 | `first_quote_date` | timestamp(3) | YES |  |
| 15 | `expertise_date` | timestamp(3) | YES |  |
| 16 | `state` | varchar | YES |  |
| 17 | `state_date` | timestamp(3) | YES |  |
| 18 | `last_quote_date` | timestamp(3) | YES |  |

## 🥈 bi_materialized_data

`Capa: Plata / Materialized`

### bi_materialized_data.consulta_movi

**Columnas:** 74

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `referencia` | varchar | YES |  |
| 2 | `descripcionreferencia` | varchar | YES |  |
| 3 | `descripcionclasificacion1` | varchar | YES |  |
| 4 | `unidades` | double | YES |  |
| 5 | `precio` | double | YES |  |
| 6 | `dtoporc` | double | YES |  |
| 7 | `idterceros` | bigint | YES |  |
| 8 | `fechafactura` | timestamp(3) | YES |  |
| 9 | `fechaalta` | timestamp(3) | YES |  |
| 10 | `descripcionmovimientotipo` | varchar | YES |  |
| 11 | `nombreempresa` | varchar | YES |  |
| 12 | `nombrecentro` | varchar | YES |  |
| 13 | `idempleadosalta` | bigint | YES |  |
| 14 | `nombreempleadoalta` | varchar | YES |  |
| 15 | `nombretercero` | varchar | YES |  |
| 16 | `idclasificacion1` | varchar | YES |  |
| 17 | `vendedor` | varchar | YES |  |
| 18 | `descripcionclasificacion3` | varchar | YES |  |
| 19 | `preciocompra` | varchar | YES |  |
| 20 | `fechadecorte` | timestamp(3) | YES |  |
| 21 | `idempresas` | bigint | YES |  |
| 22 | `idcentros` | bigint | YES |  |
| 23 | `idsecciones` | bigint | YES |  |
| 24 | `idtipolinea` | varchar | YES |  |
| 25 | `idmovimientotipos` | varchar | YES |  |
| 26 | `idmr` | varchar | YES |  |
| 27 | `serie` | varchar | YES |  |
| 28 | `numero` | varchar | YES |  |
| 29 | `ida�o` | varchar | YES |  |
| 30 | `seriefactura` | varchar | YES |  |
| 31 | `factura` | varchar | YES |  |
| 32 | `a�ofactura` | varchar | YES |  |
| 33 | `descripcionmr` | varchar | YES |  |
| 34 | `iddepartamentos` | varchar | YES |  |
| 35 | `nombrecomercialtercerotrabajo` | varchar | YES |  |
| 36 | `nombretercerotrabajo` | varchar | YES |  |
| 37 | `nifcif` | varchar | YES |  |
| 38 | `nombreempleado` | varchar | YES |  |
| 39 | `descripcionclasificacion2` | varchar | YES |  |
| 40 | `idclasificacion2` | varchar | YES |  |
| 41 | `descripcionclasificacion1movimiento` | varchar | YES |  |
| 42 | `descripcionpedidotipoventas` | varchar | YES |  |
| 43 | `tipocargotaller` | varchar | YES |  |
| 44 | `pmc` | double | YES |  |
| 45 | `gastosadicionales` | double | YES |  |
| 46 | `descripcionclasificacion5` | varchar | YES |  |
| 47 | `descripcionclasificacion6` | varchar | YES |  |
| 48 | `vin` | varchar | YES |  |
| 49 | `load_date` | varchar | YES |  |
| 50 | `siglacentro` | varchar | YES |  |
| 51 | `movimiento` | varchar | YES |  |
| 52 | `valorneto` | double | YES |  |
| 53 | `totalbruto` | double | YES |  |
| 54 | `totalvmediomov` | double | YES |  |
| 55 | `numerofactura` | varchar | YES |  |
| 56 | `numeroalbaran` | varchar | YES |  |
| 57 | `ecs` | varchar | YES |  |
| 58 | `llaveemple` | varchar | YES |  |
| 59 | `llave` | varchar | YES |  |
| 60 | `ano_factura` | integer | YES |  |
| 61 | `mes_factura` | integer | YES |  |
| 62 | `codunidadnegocio` | integer | YES |  |
| 63 | `nombreunidadnegocio` | varchar | YES |  |
| 64 | `linea` | varchar | YES |  |
| 65 | `ciudad` | varchar | YES |  |
| 66 | `descripcion_tipo_cargo` | varchar | YES |  |
| 67 | `correo` | varchar | YES |  |
| 68 | `telefono` | varchar | YES |  |
| 69 | `codigo_cargo_generico` | varchar | YES |  |
| 70 | `codigoempleado` | bigint | YES |  |
| 71 | `empresa_empleado` | varchar | YES |  |
| 72 | `marca_empleado` | varchar | YES |  |
| 73 | `nombre_cargo_generico` | varchar | YES |  |
| 74 | `nombre_centro_empleado` | varchar | YES |  |

### bi_materialized_data.custodio

**Columnas:** 210

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `comprasnumdet` | bigint | YES |  |
| 12 | `idasientos` | bigint | YES |  |
| 13 | `a�oasiento` | varchar | YES |  |
| 14 | `idvehiculos` | bigint | YES |  |
| 15 | `idterceros` | bigint | YES |  |
| 16 | `idcompratipos` | varchar | YES |  |
| 17 | `numexpedientescompramultiple` | bigint | YES |  |
| 18 | `idmarcas` | bigint | YES |  |
| 19 | `idgamas` | bigint | YES |  |
| 20 | `codmodelo` | varchar | YES |  |
| 21 | `extmodelo` | varchar | YES |  |
| 22 | `a�omodelo` | varchar | YES |  |
| 23 | `idversiones` | varchar | YES |  |
| 24 | `idtarifas` | bigint | YES |  |
| 25 | `seriefactura` | varchar | YES |  |
| 26 | `numfactura` | varchar | YES |  |
| 27 | `a�ofactura` | varchar | YES |  |
| 28 | `fechaalta` | timestamp(3) | YES |  |
| 29 | `fechaanulacion` | timestamp(3) | YES |  |
| 30 | `fechacampaalta` | timestamp(3) | YES |  |
| 31 | `fecharecepcion` | timestamp(3) | YES |  |
| 32 | `fechafactura` | timestamp(3) | YES |  |
| 33 | `fechaasiento` | timestamp(3) | YES |  |
| 34 | `fechareserva` | timestamp(3) | YES |  |
| 35 | `importacionrealizada` | bigint | YES |  |
| 36 | `importacionmodificada` | bigint | YES |  |
| 37 | `fechaimportacionrealizada` | timestamp(3) | YES |  |
| 38 | `fechaimportacionmodificada` | timestamp(3) | YES |  |
| 39 | `preciobase` | double | YES |  |
| 40 | `preciopintura` | double | YES |  |
| 41 | `preciotransporte` | double | YES |  |
| 42 | `precioopciones` | double | YES |  |
| 43 | `preciootroscargos` | double | YES |  |
| 44 | `importecompra` | double | YES |  |
| 45 | `baseimponible` | double | YES |  |
| 46 | `idcentrosasignadoventa` | bigint | YES |  |
| 47 | `idseccionesasignadaventa` | bigint | YES |  |
| 48 | `preciolegalizacion` | double | YES |  |
| 49 | `precioisv` | double | YES |  |
| 50 | `precioecovalor` | double | YES |  |
| 51 | `baseexenta` | double | YES |  |
| 52 | `sumadescuentos` | double | YES |  |
| 53 | `idempleadosreserva` | bigint | YES |  |
| 54 | `idagentesreserva` | bigint | YES |  |
| 55 | `idterceros_cedidoconcesionario` | bigint | YES |  |
| 56 | `numfacturamensual` | bigint | YES |  |
| 57 | `idsecciones` | bigint | YES |  |
| 58 | `numexpedicion` | varchar | YES |  |
| 59 | `programa` | varchar | YES |  |
| 60 | `realizargastoadicionalautomatico` | bigint | YES |  |
| 61 | `nocontabilizardocumentacion` | bigint | YES |  |
| 62 | `observaciones` | varchar | YES |  |
| 63 | `comprasnumdet_abonado` | bigint | YES |  |
| 64 | `idcompraestados` | varchar | YES |  |
| 65 | `usermod` | bigint | YES |  |
| 66 | `hostmod` | varchar | YES |  |
| 67 | `versionfila` | bigint | YES |  |
| 68 | `fechaabono` | timestamp(3) | YES |  |
| 69 | `idusuariosanulacion` | bigint | YES |  |
| 70 | `idempleadosanulacion` | bigint | YES |  |
| 71 | `hostanulacion` | varchar | YES |  |
| 72 | `idasientos_polizanoactivo` | bigint | YES |  |
| 73 | `a�oasiento_polizanoactivo` | varchar | YES |  |
| 74 | `nombremarca` | varchar | YES |  |
| 75 | `backcolorcabecerargb` | varchar | YES |  |
| 76 | `backcolordetallergb` | varchar | YES |  |
| 77 | `forecolorcabecerargb` | varchar | YES |  |
| 78 | `forecolordetallergb` | varchar | YES |  |
| 79 | `nombregama` | varchar | YES |  |
| 80 | `preciolegalizacion1` | double | YES |  |
| 81 | `precioisv1` | double | YES |  |
| 82 | `precioecovalor1` | double | YES |  |
| 83 | `activo` | bigint | YES |  |
| 84 | `idcarroceriatipos` | varchar | YES |  |
| 85 | `idclasificaciontipos` | varchar | YES |  |
| 86 | `idmarcatallermodelos` | varchar | YES |  |
| 87 | `idtracciontipos` | varchar | YES |  |
| 88 | `idcambiotipos` | varchar | YES |  |
| 89 | `idtonelajetipos` | varchar | YES |  |
| 90 | `iddistanciaejestipos` | varchar | YES |  |
| 91 | `codexternomodelo` | varchar | YES |  |
| 92 | `potenciafiscal` | varchar | YES |  |
| 93 | `potenciareal` | varchar | YES |  |
| 94 | `cilindrada` | double | YES |  |
| 95 | `aceleracion` | varchar | YES |  |
| 96 | `velocidadmax` | double | YES |  |
| 97 | `par` | varchar | YES |  |
| 98 | `numerocilindros` | bigint | YES |  |
| 99 | `consumointerurbano` | double | YES |  |
| 100 | `consumourbano` | double | YES |  |
| 101 | `consumomedio` | double | YES |  |
| 102 | `emisionesco2interurbano` | double | YES |  |
| 103 | `emisionesco2urbano` | double | YES |  |
| 104 | `emisionesco2medio` | double | YES |  |
| 105 | `importado` | bigint | YES |  |
| 106 | `modificado` | bigint | YES |  |
| 107 | `permiteplanprever` | bigint | YES |  |
| 108 | `visibleweb` | bigint | YES |  |
| 109 | `periodoinspeccion` | bigint | YES |  |
| 110 | `kilometrosinspeccion` | varchar | YES |  |
| 111 | `descripcionmodelotaller` | varchar | YES |  |
| 112 | `vin` | varchar | YES |  |
| 113 | `matricula` | varchar | YES |  |
| 114 | `comision` | varchar | YES |  |
| 115 | `fechamatriculacion` | timestamp(3) | YES |  |
| 116 | `codigofabricacion` | varchar | YES |  |
| 117 | `fechafabricacion` | timestamp(3) | YES |  |
| 118 | `numeromotor` | varchar | YES |  |
| 119 | `nombreempresa` | varchar | YES |  |
| 120 | `nombrecentro` | varchar | YES |  |
| 121 | `diasstock` | bigint | YES |  |
| 122 | `idrecursos` | bigint | YES |  |
| 123 | `idubicacionesultimarealizada` | varchar | YES |  |
| 124 | `fechaexpedientealtaultimarealizada` | timestamp(3) | YES |  |
| 125 | `ubicacionvn` | varchar | YES |  |
| 126 | `fechaubicacion` | timestamp(3) | YES |  |
| 127 | `idubicacionesultima` | varchar | YES |  |
| 128 | `fechaexpedientealtaultima` | timestamp(3) | YES |  |
| 129 | `ubicacionvnprevista` | varchar | YES |  |
| 130 | `fechasalidareal` | timestamp(3) | YES |  |
| 131 | `nombreempleadoreserva` | varchar | YES |  |
| 132 | `nombreagente` | varchar | YES |  |
| 133 | `cedido` | varchar | YES |  |
| 134 | `fechallegadapuerto` | timestamp(3) | YES |  |
| 135 | `fecharetirada` | timestamp(3) | YES |  |
| 136 | `datoscarta` | varchar | YES |  |
| 137 | `preciocompra` | double | YES |  |
| 138 | `precioventa` | double | YES |  |
| 139 | `transportecompra` | double | YES |  |
| 140 | `precioventaopcionales` | bigint | YES |  |
| 141 | `rodajetrimestral` | double | YES |  |
| 142 | `gastosmatriculacion` | double | YES |  |
| 143 | `atipicos` | double | YES |  |
| 144 | `transporteventa` | double | YES |  |
| 145 | `preciolegalizacionventa` | double | YES |  |
| 146 | `impuesto576porc` | double | YES |  |
| 147 | `numpedidovn` | varchar | YES |  |
| 148 | `idtercerospedido` | bigint | YES |  |
| 149 | `fechainiciofranquicia` | timestamp(3) | YES |  |
| 150 | `fechafinalfranquicia` | timestamp(3) | YES |  |
| 151 | `fechaaradefinitiva` | timestamp(3) | YES |  |
| 152 | `fechaentregaconcesionario` | timestamp(3) | YES |  |
| 153 | `fechacompromisoentrega` | timestamp(3) | YES |  |
| 154 | `mesesgarantiaobligatoriavn` | bigint | YES |  |
| 155 | `numpedidofabrica` | varchar | YES |  |
| 156 | `numpedidomarca` | varchar | YES |  |
| 157 | `pedidoobservaciones` | varchar | YES |  |
| 158 | `idpedidolocaltipos` | varchar | YES |  |
| 159 | `fechadespacho` | timestamp(3) | YES |  |
| 160 | `diasestancia` | bigint | YES |  |
| 161 | `observacionubicacion` | varchar | YES |  |
| 162 | `diasdecarenciadocumentacion` | bigint | YES |  |
| 163 | `diascarencia` | bigint | YES |  |
| 164 | `situacion` | varchar | YES |  |
| 165 | `permitirfacturarenotrocentro` | bigint | YES |  |
| 166 | `idpaises_origen` | varchar | YES |  |
| 167 | `importacion` | bigint | YES |  |
| 168 | `factorcambiomonedacontravalor` | double | YES |  |
| 169 | `importepedidoservicios` | double | YES |  |
| 170 | `importegastosadicionales` | double | YES |  |
| 171 | `fechapedido` | timestamp(3) | YES |  |
| 172 | `diasexposicion` | bigint | YES |  |
| 173 | `homologacion` | bigint | YES |  |
| 174 | `nombreprospectoreservapedido` | varchar | YES |  |
| 175 | `nombreclientereservapedido` | varchar | YES |  |
| 176 | `nombreclientereservacompra` | varchar | YES |  |
| 177 | `precioiuc` | double | YES |  |
| 178 | `a�opedidosservicios` | varchar | YES |  |
| 179 | `seriepedidosservicios` | varchar | YES |  |
| 180 | `idpedidosservicios` | bigint | YES |  |
| 181 | `idmonedas` | bigint | YES |  |
| 182 | `factorcambiomoneda` | double | YES |  |
| 183 | `idregimencontable` | varchar | YES |  |
| 184 | `colorcompleto` | varchar | YES |  |
| 185 | `tapiceriacompleta` | varchar | YES |  |
| 186 | `descripcioncambiotipos` | varchar | YES |  |
| 187 | `nombreversion` | varchar | YES |  |
| 188 | `nombretarifa` | varchar | YES |  |
| 189 | `nombremodelo` | varchar | YES |  |
| 190 | `descripcionestadocompra` | varchar | YES |  |
| 191 | `descripciontipocombustible` | varchar | YES |  |
| 192 | `descripcionpedidolocaltipos` | varchar | YES |  |
| 193 | `descripcioncomprausos` | varchar | YES |  |
| 194 | `descripcionestadopedidosservicio` | varchar | YES |  |
| 195 | `idtercerosreserva` | bigint | YES |  |
| 196 | `idcomprausos` | varchar | YES |  |
| 197 | `visualizarenstockcomprausos` | bigint | YES |  |
| 198 | `tipocompra` | varchar | YES |  |
| 199 | `idiventario` | bigint | YES |  |
| 200 | `fechaultimoinventario` | timestamp(3) | YES |  |
| 201 | `documentosinventario` | bigint | YES |  |
| 202 | `documentosrespuestasinventario` | bigint | YES |  |
| 203 | `porcimpuestos_iva` | double | YES |  |
| 204 | `porcimpuestos_con` | double | YES |  |
| 205 | `idcentrosubicacion` | bigint | YES |  |
| 206 | `load_date` | varchar | YES |  |
| 207 | `conteocustodio` | integer | YES |  |
| 208 | `ecs` | varchar | YES |  |
| 209 | `codunidadnegocio` | smallint | YES |  |
| 210 | `nombreunidadnegocio` | varchar | YES |  |

### bi_materialized_data.entregas_totales

**Columnas:** 46

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `fechadecorte` | timestamp(3) | YES |  |
| 2 | `idempresas` | integer | YES |  |
| 3 | `a�o` | integer | YES |  |
| 4 | `codigoempresa` | integer | YES |  |
| 5 | `empresa` | varchar | YES |  |
| 6 | `codigocentro` | integer | YES |  |
| 7 | `centro` | varchar | YES |  |
| 8 | `codigoseccion` | integer | YES |  |
| 9 | `seccion` | varchar | YES |  |
| 10 | `codigomarca` | integer | YES |  |
| 11 | `marca` | varchar | YES |  |
| 12 | `codigogama` | integer | YES |  |
| 13 | `gama` | varchar | YES |  |
| 14 | `codigomodelo` | varchar | YES |  |
| 15 | `a�omodelo` | varchar | YES |  |
| 16 | `modelo` | varchar | YES |  |
| 17 | `cedulavendedor` | varchar | YES |  |
| 18 | `nombrevendedor` | varchar | YES |  |
| 19 | `nit` | varchar | YES |  |
| 20 | `nombretercero` | varchar | YES |  |
| 21 | `cantidad` | integer | YES |  |
| 22 | `valor` | double | YES |  |
| 23 | `tipo` | varchar | YES |  |
| 24 | `fechaentregacliente` | timestamp(3) | YES |  |
| 25 | `fechafactura` | timestamp(3) | YES |  |
| 26 | `fechamod` | timestamp(3) | YES |  |
| 27 | `vin` | varchar | YES |  |
| 28 | `entrega` | varchar | YES |  |
| 29 | `placa` | varchar | YES |  |
| 30 | `fechamatriculacion` | timestamp(3) | YES |  |
| 31 | `combustible` | varchar | YES |  |
| 32 | `procedencia` | varchar | YES |  |
| 33 | `procedenciadetalle` | varchar | YES |  |
| 34 | `tipooportunidad` | varchar | YES |  |
| 35 | `correo` | varchar | YES |  |
| 36 | `telefono` | varchar | YES |  |
| 37 | `codunidadnegocio` | smallint | YES |  |
| 38 | `nombreunidadnegocio` | varchar | YES |  |
| 39 | `tipocliente` | varchar | YES |  |
| 40 | `nombrevendedorhomologado` | varchar | YES |  |
| 41 | `clase` | varchar | YES |  |
| 42 | `color` | varchar | YES |  |
| 43 | `esultimamodificacion` | integer | YES |  |
| 44 | `emailvendedor` | varchar | YES |  |
| 45 | `rowhash` | varchar | YES |  |
| 46 | `extractionid` | bigint | YES |  |

### bi_materialized_data.informa_facturacion

**Columnas:** 73

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idempresas` | bigint | YES |  |
| 2 | `idcentros` | bigint | YES |  |
| 3 | `idsecciones` | bigint | YES |  |
| 4 | `centro` | varchar | YES |  |
| 5 | `linea` | varchar | YES |  |
| 6 | `matricula` | varchar | YES |  |
| 7 | `vin` | varchar | YES |  |
| 8 | `idmarcas` | bigint | YES |  |
| 9 | `idgamas` | bigint | YES |  |
| 10 | `marca` | varchar | YES |  |
| 11 | `gama` | varchar | YES |  |
| 12 | `idterceros` | bigint | YES |  |
| 13 | `nombretercero` | varchar | YES |  |
| 14 | `nombreterceroaux` | varchar | YES |  |
| 15 | `pkterceros` | varchar | YES |  |
| 16 | `fechafactura` | date | YES |  |
| 17 | `fechaalta` | timestamp(3) | YES |  |
| 18 | `fechaentrega` | timestamp(3) | YES |  |
| 19 | `fechacierre` | timestamp(3) | YES |  |
| 20 | `anoprincipal` | integer | YES |  |
| 21 | `mesprincipal` | integer | YES |  |
| 22 | `diaprincipal` | integer | YES |  |
| 23 | `ano_periodo` | bigint | YES |  |
| 24 | `mes_periodo` | bigint | YES |  |
| 25 | `a�oot` | varchar | YES |  |
| 26 | `serieot` | varchar | YES |  |
| 27 | `numot` | bigint | YES |  |
| 28 | `numtrabajo` | bigint | YES |  |
| 29 | `descripciontrabajo` | varchar | YES |  |
| 30 | `seriefactura` | varchar | YES |  |
| 31 | `numfactura` | varchar | YES |  |
| 32 | `a�ofactura` | varchar | YES |  |
| 33 | `idempleados` | bigint | YES |  |
| 34 | `idempleadosrec` | bigint | YES |  |
| 35 | `idempleadosretirada` | bigint | YES |  |
| 36 | `idempleadosresponsable` | varchar | YES |  |
| 37 | `idempleadocierre` | bigint | YES |  |
| 38 | `asesor` | varchar | YES |  |
| 39 | `importemobruto1` | double | YES |  |
| 40 | `importematerialbruto1` | double | YES |  |
| 41 | `importesubbruto1` | double | YES |  |
| 42 | `importevarbruto1` | double | YES |  |
| 43 | `importepintbruto1` | double | YES |  |
| 44 | `importemanoobra` | double | YES |  |
| 45 | `importetot` | double | YES |  |
| 46 | `importevarios` | double | YES |  |
| 47 | `importepintura` | double | YES |  |
| 48 | `importematerialneto` | double | YES |  |
| 49 | `facturatotal` | double | YES |  |
| 50 | `facturavalermo` | double | YES |  |
| 51 | `costetotal` | double | YES |  |
| 52 | `costemat` | double | YES |  |
| 53 | `costemo` | double | YES |  |
| 54 | `costemochapa` | double | YES |  |
| 55 | `costemopintura` | double | YES |  |
| 56 | `costemoresto` | double | YES |  |
| 57 | `costepint` | double | YES |  |
| 58 | `costesub` | double | YES |  |
| 59 | `ecs` | varchar | YES |  |
| 60 | `codunidadnegocio` | smallint | YES |  |
| 61 | `nombreunidadnegocio` | varchar | YES |  |
| 62 | `horasfacturadas` | bigint | YES |  |
| 63 | `kmts` | bigint | YES |  |
| 64 | `a�omodelo` | varchar | YES |  |
| 65 | `idcargotipos` | varchar | YES |  |
| 66 | `idimputaciontipos` | bigint | YES |  |
| 67 | `descripcionseccioncargos` | varchar | YES |  |
| 68 | `idseriesgarantias` | varchar | YES |  |
| 69 | `numalbaran` | bigint | YES |  |
| 70 | `a�oalbaran` | varchar | YES |  |
| 71 | `idubicaciones` | varchar | YES |  |
| 72 | `idvehiculos` | bigint | YES |  |
| 73 | `descripcion_ubicacion` | varchar | YES |  |

### bi_materialized_data.inventario_vo

**Columnas:** 69

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `comprasnumdet` | bigint | YES |  |
| 12 | `fechadepreciar` | timestamp(3) | YES |  |
| 13 | `vin` | varchar | YES |  |
| 14 | `matricula` | varchar | YES |  |
| 15 | `idsecciones` | bigint | YES |  |
| 16 | `idcompratipos` | varchar | YES |  |
| 17 | `idregistrotipos` | varchar | YES |  |
| 18 | `fechaasiento` | timestamp(3) | YES |  |
| 19 | `idcomprainternatipos` | varchar | YES |  |
| 20 | `descripcioncomprainternatipo` | varchar | YES |  |
| 21 | `nombreempresa` | varchar | YES |  |
| 22 | `nombrecentro` | varchar | YES |  |
| 23 | `descripcionseccion` | varchar | YES |  |
| 24 | `descripciontipocompra` | varchar | YES |  |
| 25 | `descripciontipocombustible` | varchar | YES |  |
| 26 | `tipocomprainmovilizado` | bigint | YES |  |
| 27 | `idmarcas` | bigint | YES |  |
| 28 | `idgamas` | bigint | YES |  |
| 29 | `codmodelo` | varchar | YES |  |
| 30 | `extmodelo` | varchar | YES |  |
| 31 | `a�omodelo` | varchar | YES |  |
| 32 | `nombremarca` | varchar | YES |  |
| 33 | `nombregama` | varchar | YES |  |
| 34 | `idcompraestados` | varchar | YES |  |
| 35 | `nombremodelo` | varchar | YES |  |
| 36 | `a�ofactura` | varchar | YES |  |
| 37 | `seriefactura` | varchar | YES |  |
| 38 | `numfactura` | varchar | YES |  |
| 39 | `fechafactura` | timestamp(3) | YES |  |
| 40 | `descripcioncompraestados` | varchar | YES |  |
| 41 | `ultimaubicacionvn` | varchar | YES |  |
| 42 | `ubicacionvnfechainventario` | varchar | YES |  |
| 43 | `color` | varchar | YES |  |
| 44 | `tapiceria` | varchar | YES |  |
| 45 | `baseimponiblecompra` | double | YES |  |
| 46 | `depreciacioncompra` | double | YES |  |
| 47 | `compra576` | double | YES |  |
| 48 | `exentos` | double | YES |  |
| 49 | `gastosaumentanstock` | double | YES |  |
| 50 | `gastosnoaumentanstock` | double | YES |  |
| 51 | `gastospendientesaumentanstock` | double | YES |  |
| 52 | `gastospendientesnoaumentanstock` | double | YES |  |
| 53 | `totalgastoscontravalor` | double | YES |  |
| 54 | `importecompracontravalor` | double | YES |  |
| 55 | `pedidossinasignaraumentastock` | double | YES |  |
| 56 | `usodestino` | varchar | YES |  |
| 57 | `importetotaldepreciado` | double | YES |  |
| 58 | `observaciones_compra` | varchar | YES |  |
| 59 | `load_date` | varchar | YES |  |
| 60 | `valorcompra` | double | YES |  |
| 61 | `dias` | integer | YES |  |
| 62 | `edad` | varchar | YES |  |
| 63 | `pacto` | integer | YES |  |
| 64 | `nuevaubicacionreserva` | varchar | YES |  |
| 65 | `codcentro_udn` | smallint | YES |  |
| 66 | `nombrecentro_udn` | varchar | YES |  |
| 67 | `ecs` | varchar | YES |  |
| 68 | `codunidadnegocio` | smallint | YES |  |
| 69 | `nombreunidadnegocio` | varchar | YES |  |

### bi_materialized_data.inventarios_vn

**Columnas:** 78

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `comprasnumdet` | bigint | YES |  |
| 12 | `vin` | varchar | YES |  |
| 13 | `matricula` | varchar | YES |  |
| 14 | `comision` | varchar | YES |  |
| 15 | `idsecciones` | bigint | YES |  |
| 16 | `fkcompratipos` | varchar | YES |  |
| 17 | `nombreempresa` | varchar | YES |  |
| 18 | `nombrecentro` | varchar | YES |  |
| 19 | `descripcionseccion` | varchar | YES |  |
| 20 | `descripciontipocompra` | varchar | YES |  |
| 21 | `descripciontipocombustible` | varchar | YES |  |
| 22 | `idmarcas` | bigint | YES |  |
| 23 | `idgamas` | bigint | YES |  |
| 24 | `codmodelo` | varchar | YES |  |
| 25 | `extmodelo` | varchar | YES |  |
| 26 | `a�omodelo` | varchar | YES |  |
| 27 | `nombremarca` | varchar | YES |  |
| 28 | `nombregama` | varchar | YES |  |
| 29 | `nombremodelo` | varchar | YES |  |
| 30 | `a�ofactura` | varchar | YES |  |
| 31 | `seriefactura` | varchar | YES |  |
| 32 | `numfactura` | varchar | YES |  |
| 33 | `fechafactura` | timestamp(3) | YES |  |
| 34 | `idcompraestados` | varchar | YES |  |
| 35 | `a�oalbaran` | varchar | YES |  |
| 36 | `seriealbaran` | varchar | YES |  |
| 37 | `numalbaran` | varchar | YES |  |
| 38 | `fechaalbaran` | timestamp(3) | YES |  |
| 39 | `descripcionestadocompra` | varchar | YES |  |
| 40 | `color` | varchar | YES |  |
| 41 | `tapiceria` | varchar | YES |  |
| 42 | `ultimaubicacionvn` | varchar | YES |  |
| 43 | `ubicacionvnfechainventario` | varchar | YES |  |
| 44 | `baseimponiblecompra` | double | YES |  |
| 45 | `gastosaumentanstock` | double | YES |  |
| 46 | `gastosnoaumentanstock` | double | YES |  |
| 47 | `gastospendientesaumentanstock` | double | YES |  |
| 48 | `gastospendientesnoaumentanstock` | double | YES |  |
| 49 | `totalgastoscontravalor` | double | YES |  |
| 50 | `baseimponiblecompracontravalor` | double | YES |  |
| 51 | `descripcioncompraestados` | varchar | YES |  |
| 52 | `dtoimporte` | double | YES |  |
| 53 | `importereclamado` | double | YES |  |
| 54 | `pedidossinasignaraumentastock` | double | YES |  |
| 55 | `usodestino` | varchar | YES |  |
| 56 | `idversiones` | varchar | YES |  |
| 57 | `idincidenciatipos` | varchar | YES |  |
| 58 | `idtercerosactividadincidenciatipos` | bigint | YES |  |
| 59 | `idactividadincidenciatipos` | bigint | YES |  |
| 60 | `idactividadesdetincidenciatipos` | bigint | YES |  |
| 61 | `incidenciatiposdescripcion` | varchar | YES |  |
| 62 | `descripcionversion` | varchar | YES |  |
| 63 | `idcategoriagamatipos` | varchar | YES |  |
| 64 | `numeromotor` | varchar | YES |  |
| 65 | `numhomologacion` | varchar | YES |  |
| 66 | `fecha` | timestamp(3) | YES |  |
| 67 | `numdeclaracion` | varchar | YES |  |
| 68 | `fechalevante` | timestamp(3) | YES |  |
| 69 | `numlevante` | varchar | YES |  |
| 70 | `observaciones_compra` | varchar | YES |  |
| 71 | `load_date` | varchar | YES |  |
| 72 | `valorcompra` | double | YES |  |
| 73 | `dias` | integer | YES |  |
| 74 | `edad` | varchar | YES |  |
| 75 | `pacto` | integer | YES |  |
| 76 | `ecs` | varchar | YES |  |
| 77 | `codunidadnegocio` | smallint | YES |  |
| 78 | `nombreunidadnegocio` | varchar | YES |  |

### bi_materialized_data.presentaciones_comite

> **Formato:** Apache Iceberg (format-version 2, Snappy, target file size 128 MB). Reemplaza el Dataflow Power BI "PresentacionesComite". Consolida P&G (`balance`=17) y Balance General (`balance`=18). La configuración oficial de presentaciones (`nombrecentro`, `empresa`, `ecs`) proviene de `spiga_materialized_data.presentaciones_config` (dependencia: ese job debe correr antes).

**Columnas:** 31

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codigopresentacion` | integer | YES |  |
| 2 | `nombrepresentacion` | varchar | YES |  |
| 3 | `anio` | integer | YES |  |
| 4 | `mes` | integer | YES |  |
| 5 | `fecha` | date | YES |  |
| 6 | `codigoconcepto` | integer | YES |  |
| 7 | `nombreconcepto` | varchar | YES |  |
| 8 | `nivel1` | integer | YES |  |
| 9 | `nivel2` | integer | YES |  |
| 10 | `nivel3` | integer | YES |  |
| 11 | `nivel4` | integer | YES |  |
| 12 | `concepto1` | varchar | YES |  |
| 13 | `concepto2` | varchar | YES |  |
| 14 | `concepto3` | varchar | YES |  |
| 15 | `concepto4` | varchar | YES |  |
| 16 | `sede` | varchar | YES |  |
| 17 | `idsede` | integer | YES |  |
| 18 | `valor` | double | YES |  |
| 19 | `presupuesto` | double | YES |  |
| 20 | `valordivision` | double | YES |  |
| 21 | `presupuesto_co` | double | YES |  |
| 22 | `llave` | varchar | YES |  |
| 23 | `op_cerradas` | varchar | YES | S/N: operaciones cerradas (pres. 3/83) |
| 24 | `llavefinal` | varchar | YES | Llave tras reclasificación (maestras.reclasificacion_llaves_comite) |
| 25 | `nombrecentro` | varchar | YES |  |
| 26 | `empresa` | varchar | YES |  |
| 27 | `ecs` | varchar | YES | Override manual > ECS oficial de presentaciones_config |
| 28 | `administrativos` | varchar | YES | S/B: excluye llaves administrativas |
| 29 | `presentaciones` | varchar | YES | Tipo: General / Posventa / Lineas / Administrativo |
| 30 | `concepto_presentaciones` | varchar | YES | Repuestos / Taller / Nuevos / Usados (solo tipo General) |
| 31 | `balance` | integer | YES | 17=P&G, 18=Balance General |

### bi_materialized_data.stock_vo

**Columnas:** 125

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `comprasnumdet` | bigint | YES |  |
| 12 | `idvehiculos` | bigint | YES |  |
| 13 | `idcompratipos` | varchar | YES |  |
| 14 | `codcompramultiple` | bigint | YES |  |
| 15 | `fechaalta` | timestamp(3) | YES |  |
| 16 | `fechaanulacion` | timestamp(3) | YES |  |
| 17 | `fecharecepcion` | timestamp(3) | YES |  |
| 18 | `idsecciones` | bigint | YES |  |
| 19 | `fechaabono` | timestamp(3) | YES |  |
| 20 | `comprasnumdetabonado` | bigint | YES |  |
| 21 | `idcompraestados` | varchar | YES |  |
| 22 | `observaciones` | varchar | YES |  |
| 23 | `idregistrotipos` | varchar | YES |  |
| 24 | `reservafecha` | timestamp(3) | YES |  |
| 25 | `reservaidempleados` | bigint | YES |  |
| 26 | `reservaterceros` | bigint | YES |  |
| 27 | `realizargastoadicionalautomatico` | bigint | YES |  |
| 28 | `nocontabilizardocumentacion` | bigint | YES |  |
| 29 | `idempleadovendedor` | bigint | YES |  |
| 30 | `kms` | bigint | YES |  |
| 31 | `a�oexpedientecambio` | varchar | YES |  |
| 32 | `serieexpedientecambio` | varchar | YES |  |
| 33 | `numexpedientecambio` | bigint | YES |  |
| 34 | `fechaasiento` | timestamp(3) | YES |  |
| 35 | `prever` | bigint | YES |  |
| 36 | `generaasiento` | varchar | YES |  |
| 37 | `idmoduloorigen` | varchar | YES |  |
| 38 | `idusuariosanulacion` | bigint | YES |  |
| 39 | `idempleadosanulacion` | bigint | YES |  |
| 40 | `hostanulacion` | varchar | YES |  |
| 41 | `usermod` | bigint | YES |  |
| 42 | `hostmod` | varchar | YES |  |
| 43 | `versionfila` | bigint | YES |  |
| 44 | `reservaimporte` | double | YES |  |
| 45 | `importecompra` | double | YES |  |
| 46 | `precioventaminimo` | double | YES |  |
| 47 | `visibleweb` | bigint | YES |  |
| 48 | `comercializable` | bigint | YES |  |
| 49 | `idcomprausos` | varchar | YES |  |
| 50 | `vin` | varchar | YES |  |
| 51 | `matricula` | varchar | YES |  |
| 52 | `comision` | varchar | YES |  |
| 53 | `fechamatriculacion` | timestamp(3) | YES |  |
| 54 | `idmarcas` | bigint | YES |  |
| 55 | `idgamas` | bigint | YES |  |
| 56 | `codmodelo` | varchar | YES |  |
| 57 | `extmodelo` | varchar | YES |  |
| 58 | `a�omodelo` | varchar | YES |  |
| 59 | `idversiones` | varchar | YES |  |
| 60 | `idmarcasexterna` | bigint | YES |  |
| 61 | `idgamasexterna` | bigint | YES |  |
| 62 | `codmodeloexterna` | varchar | YES |  |
| 63 | `extmodeloexterna` | varchar | YES |  |
| 64 | `a�omodeloexterna` | varchar | YES |  |
| 65 | `idversionesexterna` | varchar | YES |  |
| 66 | `kmsactuales` | bigint | YES |  |
| 67 | `permitirfacturarenotrocentro` | bigint | YES |  |
| 68 | `otrasobservaciones` | varchar | YES |  |
| 69 | `horasusoactual` | bigint | YES |  |
| 70 | `nombremarca` | varchar | YES |  |
| 71 | `nombregama` | varchar | YES |  |
| 72 | `nombremodelo` | varchar | YES |  |
| 73 | `nombregamaexterna` | varchar | YES |  |
| 74 | `nombremodeloexterna` | varchar | YES |  |
| 75 | `descripciontipocombustible` | varchar | YES |  |
| 76 | `descripciontipocombustibleexterna` | varchar | YES |  |
| 77 | `descripcionestadocompra` | varchar | YES |  |
| 78 | `potenciareal` | varchar | YES |  |
| 79 | `potenciarealexterna` | varchar | YES |  |
| 80 | `numeropuertas` | varchar | YES |  |
| 81 | `numeroplazas` | varchar | YES |  |
| 82 | `nombreempresa` | varchar | YES |  |
| 83 | `nombrecentro` | varchar | YES |  |
| 84 | `descripcionseccion` | varchar | YES |  |
| 85 | `descripciontiporegistro` | varchar | YES |  |
| 86 | `idcomprainternatipos` | varchar | YES |  |
| 87 | `descripcioncompratipos` | varchar | YES |  |
| 88 | `descripcioncarroceriatipos` | varchar | YES |  |
| 89 | `diasstock` | bigint | YES |  |
| 90 | `fecharetirada` | timestamp(3) | YES |  |
| 91 | `importeventasugerido` | double | YES |  |
| 92 | `nombreempleadoreserva` | varchar | YES |  |
| 93 | `nombreterceroreserva` | varchar | YES |  |
| 94 | `idrecursos` | bigint | YES |  |
| 95 | `importebi` | double | YES |  |
| 96 | `importedvn` | double | YES |  |
| 97 | `importe576` | double | YES |  |
| 98 | `exentos` | double | YES |  |
| 99 | `importegastosadicionales` | double | YES |  |
| 100 | `importedepreciado` | double | YES |  |
| 101 | `descripcioncomprausos` | varchar | YES |  |
| 102 | `importepedidoservicios` | double | YES |  |
| 103 | `nombrescedentes` | varchar | YES |  |
| 104 | `colorcompleto` | varchar | YES |  |
| 105 | `colorcompletoexterna` | varchar | YES |  |
| 106 | `tapiceriacompleta` | varchar | YES |  |
| 107 | `visualizarenstockcomprausos` | bigint | YES |  |
| 108 | `fechafactura` | timestamp(3) | YES |  |
| 109 | `fechafabricacion` | timestamp(3) | YES |  |
| 110 | `descripcionversion` | varchar | YES |  |
| 111 | `programasmarca` | varchar | YES |  |
| 112 | `idiventario` | bigint | YES |  |
| 113 | `fechaultimoinventario` | timestamp(3) | YES |  |
| 114 | `documentosinventario` | bigint | YES |  |
| 115 | `documentosrespuestasinventario` | bigint | YES |  |
| 116 | `sitiomatricula` | varchar | YES |  |
| 117 | `fechaproximaitv` | timestamp(3) | YES |  |
| 118 | `fechavencimientoseguro` | timestamp(3) | YES |  |
| 119 | `ubicacionvo` | varchar | YES |  |
| 120 | `observacionubicacionvo` | varchar | YES |  |
| 121 | `idubicavno` | varchar | YES |  |
| 122 | `load_date` | varchar | YES |  |
| 123 | `ecs` | varchar | YES |  |
| 124 | `codunidadnegocio` | smallint | YES |  |
| 125 | `nombreunidadnegocio` | varchar | YES |  |

## 🥉 bracca_db

`Capa: Bronce / Raw`

### bracca_db.warranties_view

**Columnas:** 35

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `plate` | varchar | YES |  |
| 3 | `document` | varchar | YES |  |
| 4 | `center_name` | varchar | YES |  |
| 5 | `id_company` | integer | YES |  |
| 6 | `id_line` | varchar | YES |  |
| 7 | `id_center` | integer | YES |  |
| 8 | `asesor` | varchar | YES |  |
| 9 | `cedula_asesor` | varchar | YES |  |
| 10 | `correo_asesor` | varchar | YES |  |
| 11 | `registration_at` | timestamp(3) | YES |  |
| 12 | `activated_at` | timestamp(3) | YES |  |
| 13 | `pending_at` | timestamp(3) | YES |  |
| 14 | `sistema_motor` | varchar | YES |  |
| 15 | `caja_cambios` | varchar | YES |  |
| 16 | `caja_transferencia` | varchar | YES |  |
| 17 | `traccion` | varchar | YES |  |
| 18 | `embrague` | varchar | YES |  |
| 19 | `frenos` | varchar | YES |  |
| 20 | `aire` | varchar | YES |  |
| 21 | `sistema_enfriamiento` | varchar | YES |  |
| 22 | `sensores` | varchar | YES |  |
| 23 | `componentes_electricos` | varchar | YES |  |
| 24 | `quotation_price` | decimal(20,2) | YES |  |
| 25 | `charge_manto` | decimal(20,2) | YES |  |
| 26 | `charge_client` | decimal(20,2) | YES |  |
| 27 | `charge_concessionaire` | decimal(20,2) | YES |  |
| 28 | `charge_cda` | decimal(20,2) | YES |  |
| 29 | `charge_repair_shop` | decimal(20,2) | YES |  |
| 30 | `manto_price` | decimal(20,2) | YES |  |
| 31 | `pending_invoice_at` | timestamp(3) | YES |  |
| 32 | `expired_at` | timestamp(3) | YES |  |
| 33 | `expire_reason` | varchar | YES |  |
| 34 | `upload_invoice_at` | timestamp(3) | YES |  |
| 35 | `repair_shop` | varchar | YES |  |

## 🥉 cc_cdn
`Capa: Bronce / Raw`

### cc_cdn.wscapnet_ford

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | integer | YES |  |
| 2 | `fecha` | date | YES |  |
| 3 | `fecha_hora` | timestamp(3) | YES |  |
| 4 | `id_estrategia` | integer | YES |  |
| 5 | `year_estrategia` | integer | YES |  |
| 6 | `mes_estrategia` | varchar | YES |  |
| 7 | `tipo_estrategia` | varchar | YES |  |
| 8 | `estrategia` | varchar | YES |  |
| 9 | `estado` | varchar | YES |  |
| 10 | `vin` | varchar | YES |  |
| 11 | `placas` | varchar | YES |  |
| 12 | `contactado` | integer | YES |  |
| 13 | `nocontactado` | integer | YES |  |
| 14 | `total` | integer | YES |  |
| 15 | `status_citas` | varchar | YES |  |
| 16 | `sub_tipificacion` | varchar | YES |  |
| 17 | `tipo_contacto` | varchar | YES |  |
| 18 | `efectivo` | integer | YES |  |
| 19 | `usuarioasignado` | varchar | YES |  |
| 20 | `visita` | integer | YES |  |
| 21 | `fecha_ini_orden_servicio` | varchar | YES |  |
| 22 | `nombre_cliente` | varchar | YES |  |
| 23 | `telefono` | varchar | YES |  |
| 24 | `celular` | varchar | YES |  |
| 25 | `direccion` | varchar | YES |  |
| 26 | `modelo` | varchar | YES |  |
| 27 | `year_modelo` | integer | YES |  |
| 28 | `correo` | varchar | YES |  |
| 29 | `observaciones` | varchar | YES |  |
| 30 | `ultima_actualizacion` | timestamp(3) | YES |  |

### cc_cdn.wscapnet_mazda

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | integer | YES |  |
| 2 | `fecha` | date | YES |  |
| 3 | `fecha_hora` | timestamp(3) | YES |  |
| 4 | `id_estrategia` | integer | YES |  |
| 5 | `year_estrategia` | integer | YES |  |
| 6 | `mes_estrategia` | varchar | YES |  |
| 7 | `tipo_estrategia` | varchar | YES |  |
| 8 | `estrategia` | varchar | YES |  |
| 9 | `estado` | varchar | YES |  |
| 10 | `vin` | varchar | YES |  |
| 11 | `placas` | varchar | YES |  |
| 12 | `contactado` | integer | YES |  |
| 13 | `nocontactado` | integer | YES |  |
| 14 | `total` | integer | YES |  |
| 15 | `status_citas` | varchar | YES |  |
| 16 | `sub_tipificacion` | varchar | YES |  |
| 17 | `tipo_contacto` | varchar | YES |  |
| 18 | `efectivo` | integer | YES |  |
| 19 | `usuarioasignado` | varchar | YES |  |
| 20 | `visita` | integer | YES |  |
| 21 | `fecha_ini_orden_servicio` | varchar | YES |  |
| 22 | `nombre_cliente` | varchar | YES |  |
| 23 | `telefono` | varchar | YES |  |
| 24 | `celular` | varchar | YES |  |
| 25 | `direccion` | varchar | YES |  |
| 26 | `modelo` | varchar | YES |  |
| 27 | `year_modelo` | integer | YES |  |
| 28 | `correo` | varchar | YES |  |
| 29 | `observaciones` | varchar | YES |  |
| 30 | `ultima_actualizacion` | timestamp(3) | YES |  |

### cc_cdn.wscapnet_mercedes_benz

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | integer | YES |  |
| 2 | `fecha` | date | YES |  |
| 3 | `fecha_hora` | timestamp(3) | YES |  |
| 4 | `id_estrategia` | integer | YES |  |
| 5 | `year_estrategia` | integer | YES |  |
| 6 | `mes_estrategia` | varchar | YES |  |
| 7 | `tipo_estrategia` | varchar | YES |  |
| 8 | `estrategia` | varchar | YES |  |
| 9 | `estado` | varchar | YES |  |
| 10 | `vin` | varchar | YES |  |
| 11 | `placas` | varchar | YES |  |
| 12 | `contactado` | integer | YES |  |
| 13 | `nocontactado` | integer | YES |  |
| 14 | `total` | integer | YES |  |
| 15 | `status_citas` | varchar | YES |  |
| 16 | `sub_tipificacion` | varchar | YES |  |
| 17 | `tipo_contacto` | varchar | YES |  |
| 18 | `efectivo` | integer | YES |  |
| 19 | `usuarioasignado` | varchar | YES |  |
| 20 | `visita` | integer | YES |  |
| 21 | `fecha_ini_orden_servicio` | varchar | YES |  |
| 22 | `nombre_cliente` | varchar | YES |  |
| 23 | `telefono` | varchar | YES |  |
| 24 | `celular` | varchar | YES |  |
| 25 | `direccion` | varchar | YES |  |
| 26 | `modelo` | varchar | YES |  |
| 27 | `year_modelo` | integer | YES |  |
| 28 | `correo` | varchar | YES |  |
| 29 | `observaciones` | varchar | YES |  |
| 30 | `ultima_actualizacion` | timestamp(3) | YES |  |

### cc_cdn.wscapnet_mitsubishi

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | integer | YES |  |
| 2 | `fecha` | date | YES |  |
| 3 | `fecha_hora` | timestamp(3) | YES |  |
| 4 | `id_estrategia` | integer | YES |  |
| 5 | `year_estrategia` | integer | YES |  |
| 6 | `mes_estrategia` | varchar | YES |  |
| 7 | `tipo_estrategia` | varchar | YES |  |
| 8 | `estrategia` | varchar | YES |  |
| 9 | `estado` | varchar | YES |  |
| 10 | `vin` | varchar | YES |  |
| 11 | `placas` | varchar | YES |  |
| 12 | `contactado` | integer | YES |  |
| 13 | `nocontactado` | integer | YES |  |
| 14 | `total` | integer | YES |  |
| 15 | `status_citas` | varchar | YES |  |
| 16 | `sub_tipificacion` | varchar | YES |  |
| 17 | `tipo_contacto` | varchar | YES |  |
| 18 | `efectivo` | integer | YES |  |
| 19 | `usuarioasignado` | varchar | YES |  |
| 20 | `visita` | integer | YES |  |
| 21 | `fecha_ini_orden_servicio` | varchar | YES |  |
| 22 | `nombre_cliente` | varchar | YES |  |
| 23 | `telefono` | varchar | YES |  |
| 24 | `celular` | varchar | YES |  |
| 25 | `direccion` | varchar | YES |  |
| 26 | `modelo` | varchar | YES |  |
| 27 | `year_modelo` | integer | YES |  |
| 28 | `correo` | varchar | YES |  |
| 29 | `observaciones` | varchar | YES |  |
| 30 | `ultima_actualizacion` | timestamp(3) | YES |  |

### cc_cdn.wscapnet_renault

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | integer | YES |  |
| 2 | `fecha` | date | YES |  |
| 3 | `fecha_hora` | timestamp(3) | YES |  |
| 4 | `id_estrategia` | integer | YES |  |
| 5 | `year_estrategia` | integer | YES |  |
| 6 | `mes_estrategia` | varchar | YES |  |
| 7 | `tipo_estrategia` | varchar | YES |  |
| 8 | `estrategia` | varchar | YES |  |
| 9 | `estado` | varchar | YES |  |
| 10 | `vin` | varchar | YES |  |
| 11 | `placas` | varchar | YES |  |
| 12 | `contactado` | integer | YES |  |
| 13 | `nocontactado` | integer | YES |  |
| 14 | `total` | integer | YES |  |
| 15 | `status_citas` | varchar | YES |  |
| 16 | `sub_tipificacion` | varchar | YES |  |
| 17 | `tipo_contacto` | varchar | YES |  |
| 18 | `efectivo` | integer | YES |  |
| 19 | `usuarioasignado` | varchar | YES |  |
| 20 | `visita` | integer | YES |  |
| 21 | `fecha_ini_orden_servicio` | varchar | YES |  |
| 22 | `nombre_cliente` | varchar | YES |  |
| 23 | `telefono` | varchar | YES |  |
| 24 | `celular` | varchar | YES |  |
| 25 | `direccion` | varchar | YES |  |
| 26 | `modelo` | varchar | YES |  |
| 27 | `year_modelo` | integer | YES |  |
| 28 | `correo` | varchar | YES |  |
| 29 | `observaciones` | varchar | YES |  |
| 30 | `ultima_actualizacion` | timestamp(3) | YES |  |

### cc_cdn.wscapnet_volkswagen

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | integer | YES |  |
| 2 | `fecha` | date | YES |  |
| 3 | `fecha_hora` | timestamp(3) | YES |  |
| 4 | `id_estrategia` | integer | YES |  |
| 5 | `year_estrategia` | integer | YES |  |
| 6 | `mes_estrategia` | varchar | YES |  |
| 7 | `tipo_estrategia` | varchar | YES |  |
| 8 | `estrategia` | varchar | YES |  |
| 9 | `estado` | varchar | YES |  |
| 10 | `vin` | varchar | YES |  |
| 11 | `placas` | varchar | YES |  |
| 12 | `contactado` | integer | YES |  |
| 13 | `nocontactado` | integer | YES |  |
| 14 | `total` | integer | YES |  |
| 15 | `status_citas` | varchar | YES |  |
| 16 | `sub_tipificacion` | varchar | YES |  |
| 17 | `tipo_contacto` | varchar | YES |  |
| 18 | `efectivo` | integer | YES |  |
| 19 | `usuarioasignado` | varchar | YES |  |
| 20 | `visita` | integer | YES |  |
| 21 | `fecha_ini_orden_servicio` | varchar | YES |  |
| 22 | `nombre_cliente` | varchar | YES |  |
| 23 | `telefono` | varchar | YES |  |
| 24 | `celular` | varchar | YES |  |
| 25 | `direccion` | varchar | YES |  |
| 26 | `modelo` | varchar | YES |  |
| 27 | `year_modelo` | integer | YES |  |
| 28 | `correo` | varchar | YES |  |
| 29 | `observaciones` | varchar | YES |  |
| 30 | `ultima_actualizacion` | timestamp(3) | YES |  |

## 🥉 cc_cdn_2

`Capa: Bronce / Raw`

### cc_cdn_2.wscapnet_all

**Columnas:** 32

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | integer | YES |  |
| 2 | `fecha` | date | YES |  |
| 3 | `fecha_hora` | timestamp(3) | YES |  |
| 4 | `id_estrategia` | integer | YES |  |
| 5 | `year_estrategia` | integer | YES |  |
| 6 | `mes_estrategia` | varchar | YES |  |
| 7 | `tipo_estrategia` | varchar | YES |  |
| 8 | `estrategia` | varchar | YES |  |
| 9 | `estado` | varchar | YES |  |
| 10 | `vin` | varchar | YES |  |
| 11 | `placas` | varchar | YES |  |
| 12 | `contactado` | integer | YES |  |
| 13 | `nocontactado` | integer | YES |  |
| 14 | `total` | integer | YES |  |
| 15 | `status_citas` | varchar | YES |  |
| 16 | `sub_tipificacion` | varchar | YES |  |
| 17 | `tipo_contacto` | varchar | YES |  |
| 18 | `efectivo` | varchar | YES |  |
| 19 | `usuarioasignado` | varchar | YES |  |
| 20 | `visita` | integer | YES |  |
| 21 | `fecha_ini_orden_servicio` | varchar | YES |  |
| 22 | `nombre_cliente` | varchar | YES |  |
| 23 | `telefono` | varchar | YES |  |
| 24 | `celular` | varchar | YES |  |
| 25 | `direccion` | varchar | YES |  |
| 26 | `modelo` | varchar | YES |  |
| 27 | `year_modelo` | integer | YES |  |
| 28 | `correo` | varchar | YES |  |
| 29 | `observaciones` | varchar | YES |  |
| 30 | `ultima_actualizacion` | timestamp(3) | YES |  |
| 31 | `capital_id` | integer | YES |  |
| 32 | `marca` | varchar | YES |  |

## 🥉 clap

`Capa: Bronce / Raw`

### clap.dm_progress_user_x_course

**Columnas:** 69

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `user_id` | varchar | YES |  |
| 2 | `user_complete_name` | varchar | YES |  |
| 3 | `user_status` | varchar | YES |  |
| 4 | `email` | varchar | YES |  |
| 5 | `personal_id` | varchar | YES |  |
| 6 | `mobile_number` | varchar | YES |  |
| 7 | `city` | varchar | YES |  |
| 8 | `attr_1` | varchar | YES |  |
| 9 | `attr_2` | varchar | YES |  |
| 10 | `attr_3` | varchar | YES |  |
| 11 | `attr_4` | varchar | YES |  |
| 12 | `attr_5` | varchar | YES |  |
| 13 | `attr_6` | varchar | YES |  |
| 14 | `attr_7` | varchar | YES |  |
| 15 | `attr_8` | varchar | YES |  |
| 16 | `attr_9` | varchar | YES |  |
| 17 | `attr_10` | varchar | YES |  |
| 18 | `attr_11` | varchar | YES |  |
| 19 | `attr_12` | varchar | YES |  |
| 20 | `attr_13` | varchar | YES |  |
| 21 | `attr_14` | varchar | YES |  |
| 22 | `attr_15` | varchar | YES |  |
| 23 | `attr_16` | varchar | YES |  |
| 24 | `attr_17` | varchar | YES |  |
| 25 | `attr_18` | varchar | YES |  |
| 26 | `attr_19` | varchar | YES |  |
| 27 | `attr_20` | varchar | YES |  |
| 28 | `user_created_date` | varchar | YES |  |
| 29 | `enrollment_date` | varchar | YES |  |
| 30 | `enrollment_type` | varchar | YES |  |
| 31 | `start_date` | varchar | YES |  |
| 32 | `end_date` | varchar | YES |  |
| 33 | `course_id` | varchar | YES |  |
| 34 | `course_name` | varchar | YES |  |
| 35 | `course_type` | varchar | YES |  |
| 36 | `course_length` | varchar | YES |  |
| 37 | `course_status` | varchar | YES |  |
| 38 | `course_progress` | varchar | YES |  |
| 39 | `lesson_progress` | varchar | YES |  |
| 40 | `module_progress` | varchar | YES |  |
| 41 | `next_uncompleted_lesson_id` | varchar | YES |  |
| 42 | `main_category_name` | varchar | YES |  |
| 43 | `subcategory` | varchar | YES |  |
| 44 | `attempts_done` | varchar | YES |  |
| 45 | `completed_date` | varchar | YES |  |
| 46 | `org_id` | varchar | YES |  |
| 47 | `org_name` | varchar | YES |  |
| 48 | `last_lesson_view` | varchar | YES |  |
| 49 | `certificate_id` | varchar | YES |  |
| 50 | `certificate_generated_at` | varchar | YES |  |
| 51 | `eval_id` | varchar | YES |  |
| 52 | `eval_score` | varchar | YES |  |
| 53 | `eval_result` | varchar | YES |  |
| 54 | `eval_completed_date` | varchar | YES |  |
| 55 | `eval_score_tem` | varchar | YES |  |
| 56 | `initial_eval_id` | varchar | YES |  |
| 57 | `initial_eval_score` | varchar | YES |  |
| 58 | `initial_eval_result` | varchar | YES |  |
| 59 | `initial_eval_completed_date` | varchar | YES |  |
| 60 | `initial_eval_score_tem` | varchar | YES |  |
| 61 | `total_course_length_seconds` | varchar | YES |  |
| 62 | `total_lesson_time_seconds` | varchar | YES |  |
| 63 | `enrollment_grp_id` | varchar | YES |  |
| 64 | `enrollment_group_name` | varchar | YES |  |
| 65 | `by_profile` | varchar | YES |  |
| 66 | `updated_at` | varchar | YES |  |
| 67 | `updated_at_s3` | varchar | YES |  |
| 68 | `status` | varchar | YES |  |
| 69 | `survey_complete` | varchar | YES |  |

### clap.summary_forms_performance_review

**Columnas:** 34

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `user_id` | varchar | YES |  |
| 2 | `name_completed` | varchar | YES |  |
| 3 | `user_email` | varchar | YES |  |
| 4 | `personal_id` | varchar | YES |  |
| 5 | `attr_1` | varchar | YES |  |
| 6 | `attr_2` | varchar | YES |  |
| 7 | `attr_3` | varchar | YES |  |
| 8 | `attr_4` | varchar | YES |  |
| 9 | `attr_5` | varchar | YES |  |
| 10 | `attr_6` | varchar | YES |  |
| 11 | `attr_7` | varchar | YES |  |
| 12 | `attr_8` | varchar | YES |  |
| 13 | `user_status` | varchar | YES |  |
| 14 | `evaluator_name_completed` | varchar | YES |  |
| 15 | `evaluator_personal_id` | varchar | YES |  |
| 16 | `evaluator_email` | varchar | YES |  |
| 17 | `org_id` | varchar | YES |  |
| 18 | `template_id` | varchar | YES |  |
| 19 | `template_name` | varchar | YES |  |
| 20 | `enrollment_id` | varchar | YES |  |
| 21 | `enrollment_name` | varchar | YES |  |
| 22 | `cycle_number` | varchar | YES |  |
| 23 | `form_id` | varchar | YES |  |
| 24 | `evaluator_id` | varchar | YES |  |
| 25 | `form_name` | varchar | YES |  |
| 26 | `form_type` | varchar | YES |  |
| 27 | `form_max_score` | varchar | YES |  |
| 28 | `form_percentage_enable` | varchar | YES |  |
| 29 | `form_percentage` | varchar | YES |  |
| 30 | `form_score_calculated` | varchar | YES |  |
| 31 | `cycle_weight` | varchar | YES |  |
| 32 | `cycle_name` | varchar | YES |  |
| 33 | `cycle_status` | varchar | YES |  |
| 34 | `completed_date` | varchar | YES |  |

### clap.user_x_form_performance_review

**Columnas:** 81

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `user_id` | varchar | YES |  |
| 2 | `user_full_name` | varchar | YES |  |
| 3 | `user_email` | varchar | YES |  |
| 4 | `user_personal_id` | varchar | YES |  |
| 5 | `user_status` | varchar | YES |  |
| 6 | `user_attr_1` | varchar | YES |  |
| 7 | `user_attr_2` | varchar | YES |  |
| 8 | `user_attr_3` | varchar | YES |  |
| 9 | `user_attr_4` | varchar | YES |  |
| 10 | `user_attr_5` | varchar | YES |  |
| 11 | `user_attr_6` | varchar | YES |  |
| 12 | `user_attr_7` | varchar | YES |  |
| 13 | `user_attr_8` | varchar | YES |  |
| 14 | `evaluator_id` | varchar | YES |  |
| 15 | `evaluator_full_name` | varchar | YES |  |
| 16 | `evaluator_personal_id` | varchar | YES |  |
| 17 | `evaluator_email` | varchar | YES |  |
| 18 | `template_id` | varchar | YES |  |
| 19 | `template_name` | varchar | YES |  |
| 20 | `org_id` | varchar | YES |  |
| 21 | `enrollment_id` | varchar | YES |  |
| 22 | `enrollment_name` | varchar | YES |  |
| 23 | `enrollment_status` | varchar | YES |  |
| 24 | `enrollment_date` | varchar | YES |  |
| 25 | `cycle_number` | varchar | YES |  |
| 26 | `cycle_id` | varchar | YES |  |
| 27 | `cycle_name` | varchar | YES |  |
| 28 | `cycle_weight` | varchar | YES |  |
| 29 | `cycle_status` | varchar | YES |  |
| 30 | `open_date` | varchar | YES |  |
| 31 | `close_date` | varchar | YES |  |
| 32 | `form_id` | varchar | YES |  |
| 33 | `form_name` | varchar | YES |  |
| 34 | `form_type` | varchar | YES |  |
| 35 | `form_total_score` | varchar | YES |  |
| 36 | `form_percentage_enable` | varchar | YES |  |
| 37 | `form_percentage` | varchar | YES |  |
| 38 | `form_max_score` | varchar | YES |  |
| 39 | `competence_id` | varchar | YES |  |
| 40 | `competence_weight` | varchar | YES |  |
| 41 | `competence_score` | varchar | YES |  |
| 42 | `resource_id` | varchar | YES |  |
| 43 | `resource_score` | varchar | YES |  |
| 44 | `resource_weight` | varchar | YES |  |
| 45 | `competence_evaluate_behaviors` | varchar | YES |  |
| 46 | `nine_box_score` | varchar | YES |  |
| 47 | `objective_id` | varchar | YES |  |
| 48 | `objective_name` | varchar | YES |  |
| 49 | `objective_description` | varchar | YES |  |
| 50 | `objective_weight` | varchar | YES |  |
| 51 | `objective_created_date` | varchar | YES |  |
| 52 | `objective_score` | varchar | YES |  |
| 53 | `okr_id` | varchar | YES |  |
| 54 | `okr_advance` | varchar | YES |  |
| 55 | `okr_kr_type` | varchar | YES |  |
| 56 | `okr_kr_initial_value` | varchar | YES |  |
| 57 | `okr_kr_final_value` | varchar | YES |  |
| 58 | `okr_kr_unit` | varchar | YES |  |
| 59 | `objective_kpi_id` | varchar | YES |  |
| 60 | `objective_kpi_name` | varchar | YES |  |
| 61 | `objective_kpi_weight` | varchar | YES |  |
| 62 | `objective_kpi_score` | varchar | YES |  |
| 63 | `objective_kpi_type` | varchar | YES |  |
| 64 | `objective_kpi_initial_value` | varchar | YES |  |
| 65 | `objective_kpi_final_value` | varchar | YES |  |
| 66 | `objective_kpi_unit` | varchar | YES |  |
| 67 | `question_id` | varchar | YES |  |
| 68 | `question_stament` | varchar | YES |  |
| 69 | `question_max_score` | varchar | YES |  |
| 70 | `question_min_score` | varchar | YES |  |
| 71 | `question_answer` | varchar | YES |  |
| 72 | `question_score` | varchar | YES |  |
| 73 | `agreement_name` | varchar | YES |  |
| 74 | `agreement_weight` | varchar | YES |  |
| 75 | `content_id` | varchar | YES |  |
| 76 | `content_type` | varchar | YES |  |
| 77 | `comments` | varchar | YES |  |
| 78 | `completed_date` | varchar | YES |  |
| 79 | `status` | varchar | YES |  |
| 80 | `updated_at` | varchar | YES |  |
| 81 | `updated_at_s3` | varchar | YES |  |

## 🥈 compra_inteligente

`Capa: Plata / Materialized`

### compra_inteligente.ci_control_homologacion_runt

**Columnas:** 4

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `marca` | varchar | YES |  |
| 2 | `linea` | varchar | YES |  |
| 3 | `clase` | varchar | YES |  |
| 4 | `clasificacion` | varchar | YES |  |

### compra_inteligente.ci_control_homologacion_spiga

**Columnas:** 6

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codigo_modelo` | varchar | YES |  |
| 2 | `anio_modelo` | varchar | YES |  |
| 3 | `marca` | varchar | YES |  |
| 4 | `clasificacion` | varchar | YES |  |
| 5 | `modelo_version` | varchar | YES |  |
| 6 | `origen` | varchar | YES |  |

### compra_inteligente.ci_custodio_fasecolda

**Columnas:** 25

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `vin` | varchar | YES |  |
| 2 | `centro` | varchar | YES |  |
| 3 | `codigo_modelo` | varchar | YES |  |
| 4 | `anio_modelo` | varchar | YES |  |
| 5 | `marca` | varchar | YES |  |
| 6 | `clasificacion` | varchar | YES |  |
| 7 | `modelo_version` | varchar | YES |  |
| 8 | `gama` | varchar | YES |  |
| 9 | `color` | varchar | YES |  |
| 10 | `fechadecorte` | timestamp(3) | YES |  |
| 11 | `codigo_fasecolda` | varchar | YES |  |
| 12 | `clase_fc` | varchar | YES |  |
| 13 | `carroceria_fc` | varchar | YES |  |
| 14 | `marca_fc` | varchar | YES |  |
| 15 | `linea_fc` | varchar | YES |  |
| 16 | `linea_consolidada_fc` | varchar | YES |  |
| 17 | `cilindraje_fc` | varchar | YES |  |
| 18 | `combustible_fc` | varchar | YES |  |
| 19 | `airbags_fc` | varchar | YES |  |
| 20 | `transmision_fc` | varchar | YES |  |
| 21 | `tipo_traccion_fc` | varchar | YES |  |
| 22 | `version_fc` | varchar | YES |  |
| 23 | `especificaciones_fc` | varchar | YES |  |
| 24 | `traccion_tipo_fc` | varchar | YES |  |
| 25 | `marca_no_contar` | integer | YES |  |

### compra_inteligente.ci_entregas_fasecolda

**Columnas:** 35

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `vin` | varchar | YES |  |
| 2 | `centro` | varchar | YES |  |
| 3 | `codigo_modelo` | varchar | YES |  |
| 4 | `anio_modelo` | varchar | YES |  |
| 5 | `marca` | varchar | YES |  |
| 6 | `clasificacion` | varchar | YES |  |
| 7 | `modelo_version` | varchar | YES |  |
| 8 | `tipo` | varchar | YES |  |
| 9 | `gama` | varchar | YES |  |
| 10 | `color` | varchar | YES |  |
| 11 | `kmsactuales` | bigint | YES |  |
| 12 | `placa` | varchar | YES |  |
| 13 | `fechaentregacliente` | timestamp(3) | YES |  |
| 14 | `nombreterceros` | varchar | YES |  |
| 15 | `cantidad` | integer | YES |  |
| 16 | `precio_venta` | double | YES |  |
| 17 | `netocompra` | decimal(38,12) | YES |  |
| 18 | `netoventa` | decimal(38,6) | YES |  |
| 19 | `margen` | decimal(38,6) | YES |  |
| 20 | `por_margen` | decimal(38,6) | YES |  |
| 21 | `codigo_fasecolda` | varchar | YES |  |
| 22 | `clase_fc` | varchar | YES |  |
| 23 | `carroceria_fc` | varchar | YES |  |
| 24 | `marca_fc` | varchar | YES |  |
| 25 | `linea_fc` | varchar | YES |  |
| 26 | `linea_consolidada_fc` | varchar | YES |  |
| 27 | `cilindraje_fc` | varchar | YES |  |
| 28 | `combustible_fc` | varchar | YES |  |
| 29 | `airbags_fc` | varchar | YES |  |
| 30 | `transmision_fc` | varchar | YES |  |
| 31 | `tipo_traccion_fc` | varchar | YES |  |
| 32 | `version_fc` | varchar | YES |  |
| 33 | `especificaciones_fc` | varchar | YES |  |
| 34 | `traccion_tipo_fc` | varchar | YES |  |
| 35 | `marca_no_contar` | integer | YES |  |

### compra_inteligente.ci_facturados_no_entregados_consignacion_fasecolda

**Columnas:** 26

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `vin` | varchar | YES |  |
| 2 | `centro` | varchar | YES |  |
| 3 | `codigo_modelo` | varchar | YES |  |
| 4 | `anio_modelo` | varchar | YES |  |
| 5 | `marca` | varchar | YES |  |
| 6 | `clasificacion` | varchar | YES |  |
| 7 | `modelo_version` | varchar | YES |  |
| 8 | `tipo` | varchar | YES |  |
| 9 | `gama` | varchar | YES |  |
| 10 | `color` | varchar | YES |  |
| 11 | `fechadecorte` | timestamp(3) | YES |  |
| 12 | `codigo_fasecolda` | varchar | YES |  |
| 13 | `clase_fc` | varchar | YES |  |
| 14 | `carroceria_fc` | varchar | YES |  |
| 15 | `marca_fc` | varchar | YES |  |
| 16 | `linea_fc` | varchar | YES |  |
| 17 | `linea_consolidada_fc` | varchar | YES |  |
| 18 | `cilindraje_fc` | varchar | YES |  |
| 19 | `combustible_fc` | varchar | YES |  |
| 20 | `airbags_fc` | varchar | YES |  |
| 21 | `transmision_fc` | varchar | YES |  |
| 22 | `tipo_traccion_fc` | varchar | YES |  |
| 23 | `version_fc` | varchar | YES |  |
| 24 | `especificaciones_fc` | varchar | YES |  |
| 25 | `traccion_tipo_fc` | varchar | YES |  |
| 26 | `marca_no_contar` | integer | YES |  |

### compra_inteligente.ci_facturados_no_entregados_fasecolda

**Columnas:** 26

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `vin` | varchar | YES |  |
| 2 | `centro` | varchar | YES |  |
| 3 | `codigo_modelo` | varchar | YES |  |
| 4 | `anio_modelo` | varchar | YES |  |
| 5 | `marca` | varchar | YES |  |
| 6 | `clasificacion` | varchar | YES |  |
| 7 | `modelo_version` | varchar | YES |  |
| 8 | `tipo` | varchar | YES |  |
| 9 | `gama` | varchar | YES |  |
| 10 | `color` | varchar | YES |  |
| 11 | `fechadecorte` | timestamp(3) | YES |  |
| 12 | `codigo_fasecolda` | varchar | YES |  |
| 13 | `clase_fc` | varchar | YES |  |
| 14 | `carroceria_fc` | varchar | YES |  |
| 15 | `marca_fc` | varchar | YES |  |
| 16 | `linea_fc` | varchar | YES |  |
| 17 | `linea_consolidada_fc` | varchar | YES |  |
| 18 | `cilindraje_fc` | varchar | YES |  |
| 19 | `combustible_fc` | varchar | YES |  |
| 20 | `airbags_fc` | varchar | YES |  |
| 21 | `transmision_fc` | varchar | YES |  |
| 22 | `tipo_traccion_fc` | varchar | YES |  |
| 23 | `version_fc` | varchar | YES |  |
| 24 | `especificaciones_fc` | varchar | YES |  |
| 25 | `traccion_tipo_fc` | varchar | YES |  |
| 26 | `marca_no_contar` | integer | YES |  |

### compra_inteligente.ci_homologacion_fasecolda_mayorista

**Columnas:** 23

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `nombre_marca` | varchar | YES |  |
| 2 | `nombre_gama` | varchar | YES |  |
| 3 | `nombre_modelo` | varchar | YES |  |
| 4 | `nombre_version` | varchar | YES |  |
| 5 | `anio_modelo` | integer | YES |  |
| 6 | `marca_homologada` | varchar | YES |  |
| 7 | `codigo_homologo` | varchar | YES |  |
| 8 | `confiabilidad` | integer | YES |  |
| 9 | `comentario` | varchar | YES |  |
| 10 | `created_at` | timestamp(3) | YES |  |
| 11 | `clase` | varchar | YES |  |
| 12 | `carroceria` | varchar | YES |  |
| 13 | `marca` | varchar | YES |  |
| 14 | `linea` | varchar | YES |  |
| 15 | `linea_consolidada` | varchar | YES |  |
| 16 | `cilindraje` | varchar | YES |  |
| 17 | `combustible` | varchar | YES |  |
| 18 | `airbags` | varchar | YES |  |
| 19 | `transmision` | varchar | YES |  |
| 20 | `tipo_traccion` | varchar | YES |  |
| 21 | `version` | varchar | YES |  |
| 22 | `especificaciones` | varchar | YES |  |
| 23 | `traccion_tipo` | varchar | YES |  |

### compra_inteligente.ci_inventario_fasecolda

**Columnas:** 26

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `vin` | varchar | YES |  |
| 2 | `centro` | varchar | YES |  |
| 3 | `codigo_modelo` | varchar | YES |  |
| 4 | `anio_modelo` | varchar | YES |  |
| 5 | `marca` | varchar | YES |  |
| 6 | `clasificacion` | varchar | YES |  |
| 7 | `modelo_version` | varchar | YES |  |
| 8 | `gama` | varchar | YES |  |
| 9 | `color` | varchar | YES |  |
| 10 | `estado` | varchar | YES |  |
| 11 | `fechadecorte` | timestamp(3) | YES |  |
| 12 | `codigo_fasecolda` | varchar | YES |  |
| 13 | `clase_fc` | varchar | YES |  |
| 14 | `carroceria_fc` | varchar | YES |  |
| 15 | `marca_fc` | varchar | YES |  |
| 16 | `linea_fc` | varchar | YES |  |
| 17 | `linea_consolidada_fc` | varchar | YES |  |
| 18 | `cilindraje_fc` | varchar | YES |  |
| 19 | `combustible_fc` | varchar | YES |  |
| 20 | `airbags_fc` | varchar | YES |  |
| 21 | `transmision_fc` | varchar | YES |  |
| 22 | `tipo_traccion_fc` | varchar | YES |  |
| 23 | `version_fc` | varchar | YES |  |
| 24 | `especificaciones_fc` | varchar | YES |  |
| 25 | `traccion_tipo_fc` | varchar | YES |  |
| 26 | `marca_no_contar` | integer | YES |  |

### compra_inteligente.ci_runt_fasecolda

**Columnas:** 38

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `anio_matricula` | integer | YES |  |
| 2 | `mes_matricula` | integer | YES |  |
| 3 | `dia_matricula` | integer | YES |  |
| 4 | `clase` | varchar | YES |  |
| 5 | `carroceria` | varchar | YES |  |
| 6 | `marca` | varchar | YES |  |
| 7 | `clasificacion` | varchar | YES |  |
| 8 | `linea` | varchar | YES |  |
| 9 | `modelo` | integer | YES |  |
| 10 | `cilindraje` | integer | YES |  |
| 11 | `combustible` | varchar | YES |  |
| 12 | `airbags` | varchar | YES |  |
| 13 | `transmision` | varchar | YES |  |
| 14 | `tipo_traccion` | varchar | YES |  |
| 15 | `segmento` | varchar | YES |  |
| 16 | `segmento_x` | varchar | YES |  |
| 17 | `segmento_e` | varchar | YES |  |
| 18 | `body_style` | varchar | YES |  |
| 19 | `marca_otras` | varchar | YES |  |
| 20 | `linea_consolidada` | varchar | YES |  |
| 21 | `consecutivo` | integer | YES |  |
| 22 | `seg_tamanio` | varchar | YES |  |
| 23 | `sub_segmentos` | varchar | YES |  |
| 24 | `cantidades` | bigint | YES |  |
| 25 | `codigo_fasecolda` | varchar | YES |  |
| 26 | `clase_fc` | varchar | YES |  |
| 27 | `carroceria_fc` | varchar | YES |  |
| 28 | `marca_fc` | varchar | YES |  |
| 29 | `linea_fc` | varchar | YES |  |
| 30 | `linea_consolidada_fc` | varchar | YES |  |
| 31 | `cilindraje_fc` | varchar | YES |  |
| 32 | `combustible_fc` | varchar | YES |  |
| 33 | `airbags_fc` | varchar | YES |  |
| 34 | `transmision_fc` | varchar | YES |  |
| 35 | `tipo_traccion_fc` | varchar | YES |  |
| 36 | `version_fc` | varchar | YES |  |
| 37 | `especificaciones_fc` | varchar | YES |  |
| 38 | `traccion_tipo_fc` | varchar | YES |  |

## 🥉 cotizaciones_db

`Capa: Bronce / Raw`

### cotizaciones_db.vw_quotation

**Columnas:** 41

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `ad_lead_id` | integer | YES |  |
| 3 | `channel` | varchar | YES |  |
| 4 | `quotation_serial` | varchar | YES |  |
| 5 | `quotation_version` | integer | YES |  |
| 6 | `adviser_id` | decimal(20,0) | YES |  |
| 7 | `adviser_name` | varchar | YES |  |
| 8 | `adviser_document` | varchar | YES |  |
| 9 | `adviser_email` | varchar | YES |  |
| 10 | `adviser_brand` | varchar | YES |  |
| 11 | `adviser_company` | varchar | YES |  |
| 12 | `adviser_city` | varchar | YES |  |
| 13 | `adviser_country` | varchar | YES |  |
| 14 | `adviser_location` | varchar | YES |  |
| 15 | `adviser_center_id` | varchar | YES |  |
| 16 | `adviser_center_name` | varchar | YES |  |
| 17 | `customer_name` | varchar | YES |  |
| 18 | `customer_document_type` | varchar | YES |  |
| 19 | `customer_document` | varchar | YES |  |
| 20 | `customer_email` | varchar | YES |  |
| 21 | `customer_phone` | varchar | YES |  |
| 22 | `car_model` | varchar | YES |  |
| 23 | `car_version` | varchar | YES |  |
| 24 | `quotation_status` | varchar | YES |  |
| 25 | `quotation_views` | integer | YES |  |
| 26 | `quotation_created_date` | timestamp(3) | YES |  |
| 27 | `quotation_updated_date` | timestamp(3) | YES |  |
| 28 | `quotation_notification_date` | timestamp(3) | YES |  |
| 29 | `quotation_separation_date` | timestamp(3) | YES |  |
| 30 | `channel_id` | decimal(20,0) | YES |  |
| 31 | `channel_value` | varchar | YES |  |
| 32 | `medium_id` | decimal(20,0) | YES |  |
| 33 | `medium_value` | varchar | YES |  |
| 34 | `min_cold_temp_range` | decimal(20,0) | YES |  |
| 35 | `max_cold_temp_range` | decimal(20,0) | YES |  |
| 36 | `min_warm_temp_range` | decimal(20,0) | YES |  |
| 37 | `max_warm_temp_range` | decimal(20,0) | YES |  |
| 38 | `hot_temp_range` | decimal(20,0) | YES |  |
| 39 | `temperature` | varchar | YES |  |
| 40 | `company_id` | varchar | YES |  |
| 41 | `brand_id` | varchar | YES |  |

## 🥈 data_finanzauto

`Capa: Plata / Materialized`

### data_finanzauto.vw_finanzauto_clientes

**Columnas:** 32

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `pkfkempresas` | integer | YES |  |
| 2 | `nombreempresa` | varchar | YES |  |
| 3 | `fecha_alta` | timestamp(3) | YES |  |
| 4 | `fechamod` | timestamp(3) | YES |  |
| 5 | `numero_identificacion` | varchar | YES |  |
| 6 | `tipoidentificacion` | bigint | YES |  |
| 7 | `descrpciontipoidentificacion` | varchar | YES |  |
| 8 | `nombre` | varchar | YES |  |
| 9 | `telprincipal` | varchar | YES |  |
| 10 | `celular1` | varchar | YES |  |
| 11 | `email_principal` | varchar | YES |  |
| 12 | `direccion_principal` | varchar | YES |  |
| 13 | `empresatrabajo` | varchar | YES |  |
| 14 | `numeroempleados` | bigint | YES |  |
| 15 | `a�oconstitucion` | varchar | YES |  |
| 16 | `tipocontribuyente` | varchar | YES |  |
| 17 | `licenciaconducir_lugarexpedicion` | varchar | YES |  |
| 18 | `fkestadociviltipos` | varchar | YES |  |
| 19 | `estado_civil` | varchar | YES |  |
| 20 | `sexo` | varchar | YES |  |
| 21 | `descripcion_sexo` | varchar | YES |  |
| 22 | `pkterceroformacionniveles_iden` | integer | YES |  |
| 23 | `nivel` | varchar | YES |  |
| 24 | `fktercerocargos` | integer | YES |  |
| 25 | `cargo` | varchar | YES |  |
| 26 | `fkactividadtipos` | varchar | YES |  |
| 27 | `descripcionactividadtipos` | varchar | YES |  |
| 28 | `numerohijos` | integer | YES |  |
| 29 | `ciudadprincipal` | varchar | YES |  |
| 30 | `fechanacimiento` | timestamp(3) | YES |  |
| 31 | `fechavinculo` | timestamp(3) | YES |  |
| 32 | `habeas` | varchar | YES |  |

### data_finanzauto.vw_finanzauto_comprasvo

**Columnas:** 48

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idempresas` | bigint | YES |  |
| 2 | `nombreempresa` | varchar | YES |  |
| 3 | `idcentros` | bigint | YES |  |
| 4 | `centro` | varchar | YES |  |
| 5 | `importetotal` | double | YES |  |
| 6 | `fechafactura` | timestamp(3) | YES |  |
| 7 | `idvehiculos` | bigint | YES |  |
| 8 | `vin` | varchar | YES |  |
| 9 | `kms` | bigint | YES |  |
| 10 | `idcomercializable` | bigint | YES |  |
| 11 | `comercializable` | varchar | YES |  |
| 12 | `idmarcas` | bigint | YES |  |
| 13 | `nombremarca` | varchar | YES |  |
| 14 | `idgamas` | bigint | YES |  |
| 15 | `nombregama` | varchar | YES |  |
| 16 | `codmodelo` | varchar | YES |  |
| 17 | `nombremodelo` | varchar | YES |  |
| 18 | `a�omodelo` | varchar | YES |  |
| 19 | `fechadeactualizacion` | timestamp(3) | YES |  |
| 20 | `cilindrada` | double | YES |  |
| 21 | `combustible` | varchar | YES |  |
| 22 | `carroceria` | varchar | YES |  |
| 23 | `color` | varchar | YES |  |
| 24 | `gis` | decimal(18,4) | YES |  |
| 25 | `gnis` | decimal(18,4) | YES |  |
| 26 | `nombreclasificacion` | varchar | YES |  |
| 27 | `matricula` | varchar | YES |  |
| 28 | `perfilcliente` | varchar | YES |  |
| 29 | `nifcif` | varchar | YES |  |
| 30 | `fkdocumentaciontipos` | integer | YES |  |
| 31 | `tipodocumento` | varchar | YES |  |
| 32 | `nombre_completo` | varchar | YES |  |
| 33 | `fecha_alta` | timestamp(3) | YES |  |
| 34 | `fkestadociviltipos` | varchar | YES |  |
| 35 | `estado_civil` | varchar | YES |  |
| 36 | `sexo` | varchar | YES |  |
| 37 | `decripcion_sexo` | varchar | YES |  |
| 38 | `pkterceroformacionniveles_iden` | integer | YES |  |
| 39 | `nivel` | varchar | YES |  |
| 40 | `fktercerocargos` | integer | YES |  |
| 41 | `cargo` | varchar | YES |  |
| 42 | `fkactividadtipos` | varchar | YES |  |
| 43 | `descripcionactividadtipos` | varchar | YES |  |
| 44 | `numerohijos` | integer | YES |  |
| 45 | `ciudadprincipal` | varchar | YES |  |
| 46 | `fechanacimiento` | timestamp(3) | YES |  |
| 47 | `numerofactura` | varchar | YES |  |
| 48 | `tipodeproducto` | varchar | YES |  |

### data_finanzauto.vw_finanzauto_mostrador

**Columnas:** 24

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codigoempresa` | smallint | YES |  |
| 2 | `empresa` | varchar | YES |  |
| 3 | `cedula` | varchar | YES |  |
| 4 | `nombrecliente` | varchar | YES |  |
| 5 | `habeas` | varchar | YES |  |
| 6 | `descuentocategoriatarjeta` | varchar | YES |  |
| 7 | `categoriaagendamiento` | varchar | YES |  |
| 8 | `marca` | varchar | YES |  |
| 9 | `centro` | varchar | YES |  |
| 10 | `seccion` | varchar | YES |  |
| 11 | `referencia` | varchar | YES |  |
| 12 | `descripcionreferencia` | varchar | YES |  |
| 13 | `fechacierre` | timestamp(3) | YES |  |
| 14 | `numerofactura` | varchar | YES |  |
| 15 | `valorunitarioreferencia` | decimal(18,4) | YES |  |
| 16 | `unidadesvendidas` | decimal(18,4) | YES |  |
| 17 | `porcdescuento` | decimal(13,7) | YES |  |
| 18 | `impuestos` | decimal(38,6) | YES |  |
| 19 | `valorneto` | decimal(38,6) | YES |  |
| 20 | `cedulavendedorrepuestos` | bigint | YES |  |
| 21 | `nombrevendedorrepuestos` | varchar | YES |  |
| 22 | `codclasificacion1mov` | varchar | YES |  |
| 23 | `clasificacion1mov` | varchar | YES |  |
| 24 | `tipodeproducto` | varchar | YES |  |

### data_finanzauto.vw_finanzauto_taller

**Columnas:** 27

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codigoempresa` | smallint | YES |  |
| 2 | `empresa` | varchar | YES |  |
| 3 | `cedula` | varchar | YES |  |
| 4 | `nombrecliente` | varchar | YES |  |
| 5 | `habeas` | varchar | YES |  |
| 6 | `descuentocategoriatarjeta` | varchar | YES |  |
| 7 | `categoriaagendamiento` | varchar | YES |  |
| 8 | `marca` | varchar | YES |  |
| 9 | `vin` | varchar | YES |  |
| 10 | `placa` | varchar | YES |  |
| 11 | `centro` | varchar | YES |  |
| 12 | `seccion` | varchar | YES |  |
| 13 | `codigo` | varchar | YES |  |
| 14 | `descripcion` | varchar | YES |  |
| 15 | `fechaaperturaorden` | timestamp(3) | YES |  |
| 16 | `fechacierre` | timestamp(3) | YES |  |
| 17 | `numot` | varchar | YES |  |
| 18 | `numerofacturataller` | varchar | YES |  |
| 19 | `valorunitario` | decimal(18,4) | YES |  |
| 20 | `unidadesvendidas` | decimal(28,13) | YES |  |
| 21 | `porcentajedescuento` | decimal(15,9) | YES |  |
| 22 | `importeimpuesto` | decimal(38,6) | YES |  |
| 23 | `valorneto` | decimal(38,6) | YES |  |
| 24 | `cedulavendedorrepuestos` | bigint | YES |  |
| 25 | `nombrevendedorrepuestos` | varchar | YES |  |
| 26 | `tipocargo` | varchar | YES |  |
| 27 | `tipodeproducto` | varchar | YES |  |

### data_finanzauto.vw_finanzauto_vehiculos

**Columnas:** 35

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | integer | YES |  |
| 2 | `placa` | varchar | YES |  |
| 3 | `vin` | varchar | YES |  |
| 4 | `numdocumentopropietario` | varchar | YES |  |
| 5 | `codigomarca` | bigint | YES |  |
| 6 | `nombremarca` | varchar | YES |  |
| 7 | `codigogama` | bigint | YES |  |
| 8 | `nombregama` | varchar | YES |  |
| 9 | `codmodelo` | varchar | YES |  |
| 10 | `nombremodelo` | varchar | YES |  |
| 11 | `extmodelo` | varchar | YES |  |
| 12 | `a�omodelo` | varchar | YES |  |
| 13 | `potencia` | varchar | YES |  |
| 14 | `torque` | varchar | YES |  |
| 15 | `cilindrada` | double | YES |  |
| 16 | `combustible` | varchar | YES |  |
| 17 | `carroceria` | varchar | YES |  |
| 18 | `numeromotor` | varchar | YES |  |
| 19 | `sitioplaca` | varchar | YES |  |
| 20 | `servicio` | varchar | YES |  |
| 21 | `paisorigen` | varchar | YES |  |
| 22 | `fechafingarantiamecanica` | timestamp(3) | YES |  |
| 23 | `kilometrosfingarantia` | bigint | YES |  |
| 24 | `fechaultimainspeccion` | timestamp(3) | YES |  |
| 25 | `fechaproximainspeccion` | timestamp(3) | YES |  |
| 26 | `kilometrosinspeccion` | varchar | YES |  |
| 27 | `kmsactuales` | bigint | YES |  |
| 28 | `tiposeguro` | varchar | YES |  |
| 29 | `ciaseguros` | varchar | YES |  |
| 30 | `fechaalta` | timestamp(3) | YES |  |
| 31 | `deducible` | double | YES |  |
| 32 | `fechaadquisicionseguro` | timestamp(3) | YES |  |
| 33 | `fechavencimientoseguro` | timestamp(3) | YES |  |
| 34 | `valorseguro` | decimal(18,4) | YES |  |
| 35 | `numeropoliza` | varchar | YES |  |

### data_finanzauto.vw_finanzauto_ventasvn

**Columnas:** 66

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `vin` | varchar | YES |  |
| 2 | `kmsactuales` | bigint | YES |  |
| 3 | `codigomarca` | bigint | YES |  |
| 4 | `marca` | varchar | YES |  |
| 5 | `codigogama` | bigint | YES |  |
| 6 | `gama` | varchar | YES |  |
| 7 | `codigomodelo` | varchar | YES |  |
| 8 | `modelo` | varchar | YES |  |
| 9 | `a�omodelo` | varchar | YES |  |
| 10 | `idempresas` | bigint | YES |  |
| 11 | `empresa` | varchar | YES |  |
| 12 | `codigocentro` | bigint | YES |  |
| 13 | `centro` | varchar | YES |  |
| 14 | `tipo` | varchar | YES |  |
| 15 | `fechaentregacliente` | timestamp(3) | YES |  |
| 16 | `fechafactura` | timestamp(3) | YES |  |
| 17 | `valor` | double | YES |  |
| 18 | `fechadeactualizacion` | timestamp(3) | YES |  |
| 19 | `cilindrada` | double | YES |  |
| 20 | `fechamatriculacion` | timestamp(3) | YES |  |
| 21 | `sitioplaca` | varchar | YES |  |
| 22 | `combustible` | varchar | YES |  |
| 23 | `carroceria` | varchar | YES |  |
| 24 | `color` | varchar | YES |  |
| 25 | `gis` | decimal(18,4) | YES |  |
| 26 | `gnis` | decimal(18,4) | YES |  |
| 27 | `nombreclasificacion` | varchar | YES |  |
| 28 | `placa` | varchar | YES |  |
| 29 | `perfilcliente` | varchar | YES |  |
| 30 | `tiponegocio` | varchar | YES |  |
| 31 | `tipoventa` | varchar | YES |  |
| 32 | `tipocompra` | varchar | YES |  |
| 33 | `tipoventamarca` | varchar | YES |  |
| 34 | `tipofinanciacion` | varchar | YES |  |
| 35 | `nifcif` | varchar | YES |  |
| 36 | `fkdocumentaciontipos` | integer | YES |  |
| 37 | `tipodocumento` | varchar | YES |  |
| 38 | `nombre_completo` | varchar | YES |  |
| 39 | `fecha_alta` | timestamp(3) | YES |  |
| 40 | `fkestadociviltipos` | varchar | YES |  |
| 41 | `estado_civil` | varchar | YES |  |
| 42 | `sexo` | varchar | YES |  |
| 43 | `decripcion_sexo` | varchar | YES |  |
| 44 | `pkterceroformacionniveles_iden` | integer | YES |  |
| 45 | `nivel` | varchar | YES |  |
| 46 | `fktercerocargos` | integer | YES |  |
| 47 | `cargo` | varchar | YES |  |
| 48 | `fkactividadtipos` | varchar | YES |  |
| 49 | `descripcionactividadtipos` | varchar | YES |  |
| 50 | `numerohijos` | integer | YES |  |
| 51 | `ciudadprincipal` | varchar | YES |  |
| 52 | `fechanacimiento` | timestamp(3) | YES |  |
| 53 | `cedulavendedor` | varchar | YES |  |
| 54 | `nombrevendedor` | varchar | YES |  |
| 55 | `preciovehiculo` | decimal(18,4) | YES |  |
| 56 | `preciolista` | decimal(18,4) | YES |  |
| 57 | `valordto` | decimal(18,4) | YES |  |
| 58 | `totalfactura` | decimal(18,4) | YES |  |
| 59 | `procedencia` | varchar | YES |  |
| 60 | `nombreversion` | varchar | YES |  |
| 61 | `procedenciadetalle` | varchar | YES |  |
| 62 | `tipooportunidad` | varchar | YES |  |
| 63 | `cantidadpasajeros` | varchar | YES |  |
| 64 | `capacidaddecarga` | varchar | YES |  |
| 65 | `numerofactura` | varchar | YES |  |
| 66 | `tipodeproducto` | varchar | YES |  |

### data_finanzauto.vw_finanzauto_ventasvo

**Columnas:** 66

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `vin` | varchar | YES |  |
| 2 | `kmsactuales` | bigint | YES |  |
| 3 | `codigomarca` | bigint | YES |  |
| 4 | `marca` | varchar | YES |  |
| 5 | `codigogama` | bigint | YES |  |
| 6 | `gama` | varchar | YES |  |
| 7 | `codigomodelo` | varchar | YES |  |
| 8 | `modelo` | varchar | YES |  |
| 9 | `a�omodelo` | varchar | YES |  |
| 10 | `idempresas` | bigint | YES |  |
| 11 | `empresa` | varchar | YES |  |
| 12 | `codigocentro` | bigint | YES |  |
| 13 | `centro` | varchar | YES |  |
| 14 | `tipo` | varchar | YES |  |
| 15 | `fechaentregacliente` | timestamp(3) | YES |  |
| 16 | `fechafactura` | timestamp(3) | YES |  |
| 17 | `valor` | double | YES |  |
| 18 | `fechadeactualizacion` | timestamp(3) | YES |  |
| 19 | `cilindrada` | double | YES |  |
| 20 | `fechamatriculacion` | timestamp(3) | YES |  |
| 21 | `sitioplaca` | varchar | YES |  |
| 22 | `combustible` | varchar | YES |  |
| 23 | `carroceria` | varchar | YES |  |
| 24 | `color` | varchar | YES |  |
| 25 | `gis` | decimal(18,4) | YES |  |
| 26 | `gnis` | decimal(18,4) | YES |  |
| 27 | `nombreclasificacion` | varchar | YES |  |
| 28 | `placa` | varchar | YES |  |
| 29 | `perfilcliente` | varchar | YES |  |
| 30 | `tiponegocio` | varchar | YES |  |
| 31 | `tipoventa` | varchar | YES |  |
| 32 | `tipocompra` | varchar | YES |  |
| 33 | `tipoventamarca` | varchar | YES |  |
| 34 | `tipofinanciacion` | varchar | YES |  |
| 35 | `nifcif` | varchar | YES |  |
| 36 | `fkdocumentaciontipos` | integer | YES |  |
| 37 | `tipodocumento` | varchar | YES |  |
| 38 | `nombre_completo` | varchar | YES |  |
| 39 | `fecha_alta` | timestamp(3) | YES |  |
| 40 | `fkestadociviltipos` | varchar | YES |  |
| 41 | `estado_civil` | varchar | YES |  |
| 42 | `sexo` | varchar | YES |  |
| 43 | `decripcion_sexo` | varchar | YES |  |
| 44 | `pkterceroformacionniveles_iden` | integer | YES |  |
| 45 | `nivel` | varchar | YES |  |
| 46 | `fktercerocargos` | integer | YES |  |
| 47 | `cargo` | varchar | YES |  |
| 48 | `fkactividadtipos` | varchar | YES |  |
| 49 | `descripcionactividadtipos` | varchar | YES |  |
| 50 | `numerohijos` | integer | YES |  |
| 51 | `ciudadprincipal` | varchar | YES |  |
| 52 | `fechanacimiento` | timestamp(3) | YES |  |
| 53 | `cedulavendedor` | varchar | YES |  |
| 54 | `nombrevendedor` | varchar | YES |  |
| 55 | `preciovehiculo` | decimal(18,4) | YES |  |
| 56 | `preciolista` | decimal(18,4) | YES |  |
| 57 | `valordto` | decimal(18,4) | YES |  |
| 58 | `totalfactura` | decimal(18,4) | YES |  |
| 59 | `procedencia` | varchar | YES |  |
| 60 | `nombreversion` | varchar | YES |  |
| 61 | `procedenciadetalle` | varchar | YES |  |
| 62 | `tipooportunidad` | varchar | YES |  |
| 63 | `cantidadpasajeros` | varchar | YES |  |
| 64 | `capacidaddecarga` | varchar | YES |  |
| 65 | `numerofactura` | varchar | YES |  |
| 66 | `tipodeproducto` | varchar | YES |  |

## 🥉 endor_prod

`Capa: Bronce / Raw`

### endor_prod.bookings

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `advisors` | varchar | YES |  |
| 3 | `booking_date` | date | YES |  |
| 4 | `vin` | varchar | YES |  |
| 5 | `observation` | varchar | YES |  |
| 6 | `user_id` | decimal(20,0) | YES |  |
| 7 | `created_at` | timestamp(3) | YES |  |
| 8 | `updated_at` | timestamp(3) | YES |  |

### endor_prod.entries

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `purchase_date` | date | YES |  |
| 3 | `admision_date` | date | YES |  |
| 4 | `vin` | varchar | YES |  |
| 5 | `location_id` | decimal(20,0) | YES |  |
| 6 | `user_id` | decimal(20,0) | YES |  |
| 7 | `created_at` | timestamp(3) | YES |  |
| 8 | `updated_at` | timestamp(3) | YES |  |

### endor_prod.locations

**Columnas:** 26

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `uuid` | varchar | YES |  |
| 3 | `name` | varchar | YES |  |
| 4 | `enabled` | boolean | YES |  |
| 5 | `enabled_schedule` | boolean | YES |  |
| 6 | `city_cod` | varchar | YES |  |
| 7 | `city_cod_name` | varchar | YES |  |
| 8 | `address` | varchar | YES |  |
| 9 | `neighborhood` | varchar | YES |  |
| 10 | `week` | varchar | YES |  |
| 11 | `weekend` | varchar | YES |  |
| 12 | `email` | varchar | YES |  |
| 13 | `phone` | varchar | YES |  |
| 14 | `whatsapp` | varchar | YES |  |
| 15 | `latitude` | varchar | YES |  |
| 16 | `longitude` | varchar | YES |  |
| 17 | `description` | varchar | YES |  |
| 18 | `contact` | varchar | YES |  |
| 19 | `map` | varchar | YES |  |
| 20 | `premium` | boolean | YES |  |
| 21 | `type_location` | boolean | YES |  |
| 22 | `locations_availability_id` | decimal(20,0) | YES |  |
| 23 | `created_at` | timestamp(3) | YES |  |
| 24 | `updated_at` | timestamp(3) | YES |  |
| 25 | `spiga_id` | varchar | YES |  |
| 26 | `spiga_company_id` | bigint | YES |  |

### endor_prod.manufacturers

**Columnas:** 4

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `name` | varchar | YES |  |
| 3 | `created_at` | timestamp(3) | YES |  |
| 4 | `updated_at` | timestamp(3) | YES |  |

### endor_prod.models

**Columnas:** 6

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `manufacturer_id` | decimal(20,0) | YES |  |
| 3 | `name` | varchar | YES |  |
| 4 | `fasecolda` | varchar | YES |  |
| 5 | `created_at` | timestamp(3) | YES |  |
| 6 | `updated_at` | timestamp(3) | YES |  |

### endor_prod.prices

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `purchase_value` | decimal(19,4) | YES |  |
| 3 | `transfer_value` | decimal(19,4) | YES |  |
| 4 | `enlistment_value` | decimal(19,4) | YES |  |
| 5 | `total_cost` | decimal(19,4) | YES |  |
| 6 | `sale_price` | decimal(19,4) | YES |  |
| 7 | `old_price` | decimal(19,4) | YES |  |
| 8 | `vin` | varchar | YES |  |
| 9 | `details` | varchar | YES |  |
| 10 | `iva` | decimal(19,4) | YES |  |
| 11 | `ipo` | decimal(19,4) | YES |  |
| 12 | `utility` | decimal(19,4) | YES |  |
| 13 | `user_id` | decimal(20,0) | YES |  |
| 14 | `created_at` | timestamp(3) | YES |  |
| 15 | `updated_at` | timestamp(3) | YES |  |

### endor_prod.purchase_requests

**Columnas:** 34

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `uuid` | varchar | YES |  |
| 3 | `date` | timestamp(3) | YES |  |
| 4 | `vehicles_id` | decimal(20,0) | YES |  |
| 5 | `scheduling_availabilities_id` | decimal(20,0) | YES |  |
| 6 | `manufacturers_id` | decimal(20,0) | YES |  |
| 7 | `models_id` | decimal(20,0) | YES |  |
| 8 | `version` | varchar | YES |  |
| 9 | `transmission` | varchar | YES |  |
| 10 | `kilometrage` | varchar | YES |  |
| 11 | `cc` | varchar | YES |  |
| 12 | `year` | varchar | YES |  |
| 13 | `name_client` | varchar | YES |  |
| 14 | `email_client` | varchar | YES |  |
| 15 | `phone_client` | varchar | YES |  |
| 16 | `value_quotation` | decimal(19,4) | YES |  |
| 17 | `value_quotation_with_percentage` | decimal(19,4) | YES |  |
| 18 | `note_quotation` | varchar | YES |  |
| 19 | `note_close` | varchar | YES |  |
| 20 | `new_solicitud_id` | varchar | YES |  |
| 21 | `scheduling_workshop` | varchar | YES |  |
| 22 | `schedule_date` | date | YES |  |
| 23 | `schedule_time` | varchar | YES |  |
| 24 | `status` | varchar | YES |  |
| 25 | `fds` | boolean | YES |  |
| 26 | `premium` | boolean | YES |  |
| 27 | `accept_terms` | boolean | YES |  |
| 28 | `adviser_id` | decimal(20,0) | YES |  |
| 29 | `manage_date` | timestamp(3) | YES |  |
| 30 | `created_at` | timestamp(3) | YES |  |
| 31 | `updated_at` | timestamp(3) | YES |  |
| 32 | `origin` | varchar | YES |  |
| 33 | `utm_source` | varchar | YES |  |
| 34 | `utm_campaign` | varchar | YES |  |

### endor_prod.settings

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `key` | varchar | YES |  |
| 3 | `display_name` | varchar | YES |  |
| 4 | `value` | varchar | YES |  |
| 5 | `details` | varchar | YES |  |
| 6 | `type` | varchar | YES |  |
| 7 | `order` | integer | YES |  |
| 8 | `group` | varchar | YES |  |

### endor_prod.vehicle_statuses

**Columnas:** 5

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | integer | YES |  |
| 2 | `name` | varchar | YES |  |
| 3 | `description` | varchar | YES |  |
| 4 | `created_at` | timestamp(3) | YES |  |
| 5 | `updated_at` | timestamp(3) | YES |  |

### endor_prod.vehicle_types

**Columnas:** 5

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `name` | varchar | YES |  |
| 3 | `abbr` | varchar | YES |  |
| 4 | `created_at` | timestamp(3) | YES |  |
| 5 | `updated_at` | timestamp(3) | YES |  |

### endor_prod.vehicles

**Columnas:** 33

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `uuid` | varchar | YES |  |
| 3 | `type_id` | decimal(20,0) | YES |  |
| 4 | `vin` | varchar | YES |  |
| 5 | `slug` | varchar | YES |  |
| 6 | `version` | varchar | YES |  |
| 7 | `status` | integer | YES |  |
| 8 | `kilometrage` | integer | YES |  |
| 9 | `year` | integer | YES |  |
| 10 | `cc` | integer | YES |  |
| 11 | `registered_city_cod` | varchar | YES |  |
| 12 | `city_cod_name` | varchar | YES |  |
| 13 | `features` | varchar | YES |  |
| 14 | `checklist` | varchar | YES |  |
| 15 | `model_id` | decimal(20,0) | YES |  |
| 16 | `manufacturer_id` | decimal(20,0) | YES |  |
| 17 | `entry_id` | decimal(20,0) | YES |  |
| 18 | `price_id` | decimal(20,0) | YES |  |
| 19 | `booking_id` | decimal(20,0) | YES |  |
| 20 | `created_at` | timestamp(3) | YES |  |
| 21 | `updated_at` | timestamp(3) | YES |  |
| 22 | `bonus` | boolean | YES |  |
| 23 | `bonus_start` | date | YES |  |
| 24 | `bonus_end` | date | YES |  |
| 25 | `has_360` | boolean | YES |  |
| 26 | `image` | varchar | YES |  |
| 27 | `on_consignment` | boolean | YES |  |
| 28 | `consignment_of` | varchar | YES |  |
| 29 | `invoice_date` | date | YES |  |
| 30 | `invoice_comment` | varchar | YES |  |
| 31 | `main_image` | varchar | YES |  |
| 32 | `cf` | varchar | YES |  |
| 33 | `ch` | varchar | YES |  |

### endor_prod.vehicles_details_vw

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `plate` | varchar | YES |  |
| 2 | `location` | varchar | YES |  |
| 3 | `publication_date` | timestamp(3) | YES |  |
| 4 | `price` | decimal(19,4) | YES |  |
| 5 | `status` | varchar | YES |  |
| 6 | `manufacturer` | varchar | YES |  |
| 7 | `commercial_line` | varchar | YES |  |
| 8 | `version` | varchar | YES |  |
| 9 | `model` | integer | YES |  |
| 10 | `cc` | integer | YES |  |
| 11 | `km` | integer | YES |  |
| 12 | `color` | varchar | YES |  |

## 🥉 eos_prod_core

`Capa: Bronce / Raw`

### eos_prod_core.vw_financial_requests

**Columnas:** 204

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `financing_entry_id` | decimal(20,0) | YES |  |
| 2 | `primer_nombre` | varchar | YES |  |
| 3 | `segundo_nombre` | varchar | YES |  |
| 4 | `primer_apellido` | varchar | YES |  |
| 5 | `segundo_apellido` | varchar | YES |  |
| 6 | `email` | varchar | YES |  |
| 7 | `numero_de_celular` | varchar | YES |  |
| 8 | `tipo_de_identificacion` | varchar | YES |  |
| 9 | `numero_de_identificacion` | varchar | YES |  |
| 10 | `fecha_expedicion` | varchar | YES |  |
| 11 | `ciudad_expedicion` | varchar | YES |  |
| 12 | `fecha_nacimiento` | varchar | YES |  |
| 13 | `lugar_de_nacimiento` | varchar | YES |  |
| 14 | `genero` | varchar | YES |  |
| 15 | `estado_civil` | varchar | YES |  |
| 16 | `edad` | varchar | YES |  |
| 17 | `nacionalidad` | varchar | YES |  |
| 18 | `departamento_residencia` | varchar | YES |  |
| 19 | `ciudad_residencia` | varchar | YES |  |
| 20 | `direccion_residencia` | varchar | YES |  |
| 21 | `informacion_adicional` | varchar | YES |  |
| 22 | `antiguedad_residencia` | varchar | YES |  |
| 23 | `telefono_fijo` | varchar | YES |  |
| 24 | `tipo_vivienda` | varchar | YES |  |
| 25 | `estrato` | varchar | YES |  |
| 26 | `marca_vehiculo` | varchar | YES |  |
| 27 | `linea_vehiculo` | varchar | YES |  |
| 28 | `version_vehiculo` | varchar | YES |  |
| 29 | `vitrina` | varchar | YES |  |
| 30 | `valor_vehiculo` | varchar | YES |  |
| 31 | `plazo_financiacion` | varchar | YES |  |
| 32 | `valor_a_financiar` | varchar | YES |  |
| 33 | `ocupacion` | varchar | YES |  |
| 34 | `nivel_educativo` | varchar | YES |  |
| 35 | `profesiones` | varchar | YES |  |
| 36 | `declara_renta` | varchar | YES |  |
| 37 | `entidad_pagadora` | varchar | YES |  |
| 38 | `fecha_en_la_que_te_pensionaste` | varchar | YES |  |
| 39 | `nombre_institucion_donde_estudia` | varchar | YES |  |
| 40 | `numero_semestre_programa` | varchar | YES |  |
| 41 | `nombre_empresa` | varchar | YES |  |
| 42 | `actividad_economica` | varchar | YES |  |
| 43 | `ciudad_empresa` | varchar | YES |  |
| 44 | `direccion_empresa` | varchar | YES |  |
| 45 | `telefono_empresa` | varchar | YES |  |
| 46 | `tipo_de_contrato` | varchar | YES |  |
| 47 | `ingresos_mensuales` | varchar | YES |  |
| 48 | `fecha_inicio_trabajo_actual` | varchar | YES |  |
| 49 | `celular_referencia_personal` | varchar | YES |  |
| 50 | `parentesco_referencia_personal` | varchar | YES |  |
| 51 | `correo_referencia_personal` | varchar | YES |  |
| 52 | `direccion_referencia_personal` | varchar | YES |  |
| 53 | `goza_reconocimiento_publico_politico` | varchar | YES |  |
| 54 | `realiza_operaciones_moneda_extranjera` | varchar | YES |  |
| 55 | `residente_fiscal_pais_diferente_colombia` | varchar | YES |  |
| 56 | `basicos_mensuales` | varchar | YES |  |
| 57 | `variables_mensuales` | varchar | YES |  |
| 58 | `otros_ingresos` | varchar | YES |  |
| 59 | `egresos_mensuales` | varchar | YES |  |
| 60 | `personas_a_cargo` | varchar | YES |  |
| 61 | `valor_total_activos` | varchar | YES |  |
| 62 | `valor_total_vehiculos` | varchar | YES |  |
| 63 | `valor_total_pasivos` | varchar | YES |  |
| 64 | `foto_cedula_frontal` | varchar | YES |  |
| 65 | `foto_cedula_posterior` | varchar | YES |  |
| 66 | `anio_vehiculo` | varchar | YES |  |
| 67 | `pais_de_expedicion` | varchar | YES |  |
| 68 | `departamento_de_expedicion` | varchar | YES |  |
| 69 | `pais_de_residencia` | varchar | YES |  |
| 70 | `pais_de_nacimiento` | varchar | YES |  |
| 71 | `departamento_de_nacimiento` | varchar | YES |  |
| 72 | `pais_de_la_empresa` | varchar | YES |  |
| 73 | `departamento_de_la_empresa` | varchar | YES |  |
| 74 | `estado_del_vehiculo` | varchar | YES |  |
| 75 | `tipo_de_servicio_del_vehiculo` | varchar | YES |  |
| 76 | `nombre_referencia_personal` | varchar | YES |  |
| 77 | `nombre_referencia_familiar` | varchar | YES |  |
| 78 | `parentesco_referencia_familiar` | varchar | YES |  |
| 79 | `telefono_referencia_familiar` | varchar | YES |  |
| 80 | `por_concepto_de` | varchar | YES |  |
| 81 | `asesores` | varchar | YES |  |
| 82 | `relacion_persona_suma_ingresos` | varchar | YES |  |
| 83 | `sumar_ingresos` | varchar | YES |  |
| 84 | `foto_cedula_frontal_parentesco` | varchar | YES |  |
| 85 | `foto_cedula_posterior_parentesco` | varchar | YES |  |
| 86 | `term_conditions_relationship` | varchar | YES |  |
| 87 | `total_gastos_mensuales` | varchar | YES |  |
| 88 | `numero_de_celular_parentesco` | varchar | YES |  |
| 89 | `tipo_de_identificacion_suma_ingresos` | varchar | YES |  |
| 90 | `numero_de_identificacion_suma_ingresos` | varchar | YES |  |
| 91 | `correo_electronico_suma_ingresos` | varchar | YES |  |
| 92 | `primer_nombre_suma_ingresos` | varchar | YES |  |
| 93 | `segundo_nombre_suma_ingresos` | varchar | YES |  |
| 94 | `primer_apellido_suma_ingresos` | varchar | YES |  |
| 95 | `segundo_apellido_suma_ingresos` | varchar | YES |  |
| 96 | `fecha_de_nacimiento_suma_ingresos` | varchar | YES |  |
| 97 | `edad_suma_ingresos` | varchar | YES |  |
| 98 | `nombre_empresa_suma_ingresos` | varchar | YES |  |
| 99 | `actividad_economica_suma_ingresos` | varchar | YES |  |
| 100 | `direccion_empresa_suma_ingresos` | varchar | YES |  |
| 101 | `telefono_empresa_suma_ingresos` | varchar | YES |  |
| 102 | `fecha_inicio_trabajo_actual_suma_ingresos` | varchar | YES |  |
| 103 | `ingreso_mensual_suma_ingresos` | varchar | YES |  |
| 104 | `otros_ingresos_suma_ingresos` | varchar | YES |  |
| 105 | `grupo_etnico` | varchar | YES |  |
| 106 | `placa` | varchar | YES |  |
| 107 | `razon_social` | varchar | YES |  |
| 108 | `nit_empresa` | varchar | YES |  |
| 109 | `celular_referencia_familiar` | varchar | YES |  |
| 110 | `tipo_de_servicio_del_vehiculo_juridico` | varchar | YES |  |
| 111 | `valor_chasis` | varchar | YES |  |
| 112 | `valor_carroceria` | varchar | YES |  |
| 113 | `plazo_financiacion_juridico` | varchar | YES |  |
| 114 | `email_empresa` | varchar | YES |  |
| 115 | `tipo_sociedad_empresa` | varchar | YES |  |
| 116 | `cual_tipo_sociedad_empresa` | varchar | YES |  |
| 117 | `fecha_constitucion_empresa` | varchar | YES |  |
| 118 | `ingresos_operacionales_mensuales` | varchar | YES |  |
| 119 | `agregar_informacion_socios_empresa` | varchar | YES |  |
| 120 | `nombre_empresa_socio_1` | varchar | YES |  |
| 121 | `porcentaje_participacion_empresa_socio_1` | varchar | YES |  |
| 122 | `nombre_empresa_socio_2` | varchar | YES |  |
| 123 | `porcentaje_participacion_empresa_socio_2` | varchar | YES |  |
| 124 | `nombre_empresa_socio_3` | varchar | YES |  |
| 125 | `porcentaje_participacion_empresa_socio_3` | varchar | YES |  |
| 126 | `nombre_empresa_socio_4` | varchar | YES |  |
| 127 | `porcentaje_participacion_empresa_socio_4` | varchar | YES |  |
| 128 | `nombre_empresa_socio_5` | varchar | YES |  |
| 129 | `porcentaje_participacion_empresa_socio_5` | varchar | YES |  |
| 130 | `agregar_informacion_referencias_bancarias_empresa` | varchar | YES |  |
| 131 | `banco_1` | varchar | YES |  |
| 132 | `numero_cuenta_empresa_1` | varchar | YES |  |
| 133 | `antiguedad_empresa_1` | varchar | YES |  |
| 134 | `creditos_aprobados_empresa_1` | varchar | YES |  |
| 135 | `creditos_vigentes_empresa_1` | varchar | YES |  |
| 136 | `banco_2` | varchar | YES |  |
| 137 | `numero_cuenta_empresa_2` | varchar | YES |  |
| 138 | `antiguedad_empresa_2` | varchar | YES |  |
| 139 | `creditos_aprobados_empresa_2` | varchar | YES |  |
| 140 | `creditos_vigentes_empresa_2` | varchar | YES |  |
| 141 | `banco_3` | varchar | YES |  |
| 142 | `numero_cuenta_empresa_3` | varchar | YES |  |
| 143 | `antiguedad_empresa_3` | varchar | YES |  |
| 144 | `creditos_aprobados_empresa_3` | varchar | YES |  |
| 145 | `creditos_vigentes_empresa_3` | varchar | YES |  |
| 146 | `agregar_informacion_vehiculos_maquinaria_empresa` | varchar | YES |  |
| 147 | `anio_vehiculo_empresa_1` | varchar | YES |  |
| 148 | `marca_vehiculo_empresa_1` | varchar | YES |  |
| 149 | `linea_vehiculo_empresa_1` | varchar | YES |  |
| 150 | `clase_vehiculo_empresa_1` | varchar | YES |  |
| 151 | `placa_empresa_1` | varchar | YES |  |
| 152 | `valor_comercial_vehiculo_empresa_1` | varchar | YES |  |
| 153 | `pignorado_a_empresa_1` | varchar | YES |  |
| 154 | `valor_pignorado_a_empresa_1` | varchar | YES |  |
| 155 | `anio_vehiculo_empresa_2` | varchar | YES |  |
| 156 | `marca_vehiculo_empresa_2` | varchar | YES |  |
| 157 | `linea_vehiculo_empresa_2` | varchar | YES |  |
| 158 | `clase_vehiculo_empresa_2` | varchar | YES |  |
| 159 | `placa_empresa_2` | varchar | YES |  |
| 160 | `valor_comercial_vehiculo_empresa_2` | varchar | YES |  |
| 161 | `pignorado_a_empresa_2` | varchar | YES |  |
| 162 | `valor_pignorado_a_empresa_2` | varchar | YES |  |
| 163 | `anio_vehiculo_empresa_3` | varchar | YES |  |
| 164 | `marca_vehiculo_empresa_3` | varchar | YES |  |
| 165 | `linea_vehiculo_empresa_3` | varchar | YES |  |
| 166 | `clase_vehiculo_empresa_3` | varchar | YES |  |
| 167 | `placa_empresa_3` | varchar | YES |  |
| 168 | `valor_comercial_vehiculo_empresa_3` | varchar | YES |  |
| 169 | `pignorado_a_empresa_3` | varchar | YES |  |
| 170 | `valor_pignorado_a_empresa_3` | varchar | YES |  |
| 171 | `agregar_informacion_prestamos_bancarios_vigentes_empresa` | varchar | YES |  |
| 172 | `entidad_prestamo_empresa_1` | varchar | YES |  |
| 173 | `valor_prestamo_empresa_1` | varchar | YES |  |
| 174 | `valor_cuota_mensual_empresa_1` | varchar | YES |  |
| 175 | `entidad_prestamo_empresa_2` | varchar | YES |  |
| 176 | `valor_prestamo_empresa_2` | varchar | YES |  |
| 177 | `valor_cuota_mensual_empresa_2` | varchar | YES |  |
| 178 | `documento_empresa` | varchar | YES |  |
| 179 | `form_juridical` | varchar | YES |  |
| 180 | `telefono_empresa_juridico` | varchar | YES |  |
| 181 | `pais_de_la_empresa_juridico` | varchar | YES |  |
| 182 | `departamento_de_la_empresa_juridico` | varchar | YES |  |
| 183 | `ciudad_empresa_juridico` | varchar | YES |  |
| 184 | `direccion_empresa_juridico` | varchar | YES |  |
| 185 | `actividad_economica_empresa_juridico` | varchar | YES |  |
| 186 | `atribuciones_representante_legal_empresa` | varchar | YES |  |
| 187 | `valor_total_activos_empresa_juridico` | varchar | YES |  |
| 188 | `valor_total_pasivos_empresa_juridico` | varchar | YES |  |
| 189 | `ingresos_mensuales_empresa_juridico` | varchar | YES |  |
| 190 | `egresos_mensuales_empresa_juridico` | varchar | YES |  |
| 191 | `codigo_fasecolda` | varchar | YES |  |
| 192 | `tipo_de_cliente` | varchar | YES |  |
| 193 | `company_id` | decimal(20,0) | YES |  |
| 194 | `company_agile_id` | varchar | YES |  |
| 195 | `company_spiga_id` | varchar | YES |  |
| 196 | `company` | varchar | YES |  |
| 197 | `line_id` | decimal(20,0) | YES |  |
| 198 | `line_agile_id` | varchar | YES |  |
| 199 | `line_spiga_id` | varchar | YES |  |
| 200 | `line` | varchar | YES |  |
| 201 | `headquarter_id` | decimal(20,0) | YES |  |
| 202 | `headquarter_agile_id` | varchar | YES |  |
| 203 | `headquarter_spiga_id` | varchar | YES |  |
| 204 | `headquarter` | varchar | YES |  |

### eos_prod_core.vw_financing_entries_search

**Columnas:** 23

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `case_number` | varchar | YES |  |
| 3 | `session_uuid` | varchar | YES |  |
| 4 | `identification_number` | varchar | YES |  |
| 5 | `first_name` | varchar | YES |  |
| 6 | `second_name` | varchar | YES |  |
| 7 | `surname` | varchar | YES |  |
| 8 | `second_surname` | varchar | YES |  |
| 9 | `financing_value` | varchar | YES |  |
| 10 | `adviser` | varchar | YES |  |
| 11 | `headquarter_id` | decimal(20,0) | YES |  |
| 12 | `headquarter_name` | varchar | YES |  |
| 13 | `company_id` | decimal(20,0) | YES |  |
| 14 | `company_name` | varchar | YES |  |
| 15 | `company_group_id` | decimal(20,0) | YES |  |
| 16 | `company_group_name` | varchar | YES |  |
| 17 | `financing_entity_id` | decimal(20,0) | YES |  |
| 18 | `financing_entity_ids` | varchar | YES |  |
| 19 | `financing_entry_step_id` | decimal(20,0) | YES |  |
| 20 | `step_key_name` | varchar | YES |  |
| 21 | `financing_entry_step_is_active` | boolean | YES |  |
| 22 | `financing_entry_step_created_at` | timestamp(3) | YES |  |
| 23 | `created_at` | timestamp(3) | YES |  |

### eos_prod_core.vw_financing_entry_values

**Columnas:** 4

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `financing_entry_id` | decimal(20,0) | YES |  |
| 3 | `field_id` | decimal(20,0) | YES |  |
| 4 | `field_value` | varchar | YES |  |

### eos_prod_core.vw_financing_priority_rules

**Columnas:** 10

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `line_id` | decimal(20,0) | YES |  |
| 2 | `line_name` | varchar | YES |  |
| 3 | `financing_entity_id` | decimal(20,0) | YES |  |
| 4 | `financing_entity_name` | varchar | YES |  |
| 5 | `is_priority` | boolean | YES |  |
| 6 | `priority` | varchar | YES |  |
| 7 | `step_id` | decimal(20,0) | YES |  |
| 8 | `step_name` | varchar | YES |  |
| 9 | `hour_time` | integer | YES |  |
| 10 | `minute_time` | integer | YES |  |

### eos_prod_core.vw_tracking_insurance

**Columnas:** 78

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `insurance_entry_id` | decimal(20,0) | YES |  |
| 3 | `case_number` | varchar | YES |  |
| 4 | `origin` | varchar | YES |  |
| 5 | `origin_spiga` | varchar | YES |  |
| 6 | `label` | varchar | YES |  |
| 7 | `old_insurance_entry_id` | decimal(20,0) | YES |  |
| 8 | `days_since_creation` | integer | YES |  |
| 9 | `step_id` | decimal(20,0) | YES |  |
| 10 | `step_name` | varchar | YES |  |
| 11 | `insurance_company_id` | decimal(20,0) | YES |  |
| 12 | `insurance_company_name` | varchar | YES |  |
| 13 | `financing_entity_id` | decimal(20,0) | YES |  |
| 14 | `financing_entity_name` | varchar | YES |  |
| 15 | `expired_at` | date | YES |  |
| 16 | `validity_at` | date | YES |  |
| 17 | `amount` | double | YES |  |
| 18 | `vehicle_status` | varchar | YES |  |
| 19 | `placa` | varchar | YES |  |
| 20 | `mileage` | varchar | YES |  |
| 21 | `vehicle_brand` | varchar | YES |  |
| 22 | `vehicle_line` | varchar | YES |  |
| 23 | `vehicle_model` | varchar | YES |  |
| 24 | `vehicle_version` | varchar | YES |  |
| 25 | `vehicle_value` | varchar | YES |  |
| 26 | `invoiced_vehicle_value` | varchar | YES |  |
| 27 | `version_spiga` | varchar | YES |  |
| 28 | `vin` | varchar | YES |  |
| 29 | `code_fasecolda` | varchar | YES |  |
| 30 | `fuel_spiga` | varchar | YES |  |
| 31 | `vehicle_service_type` | varchar | YES |  |
| 32 | `circulation_city` | varchar | YES |  |
| 33 | `adviser_spiga_name` | varchar | YES |  |
| 34 | `user_document_type` | varchar | YES |  |
| 35 | `user_customer_type` | varchar | YES |  |
| 36 | `user_identification_number` | bigint | YES |  |
| 37 | `user_first_name` | varchar | YES |  |
| 38 | `user_second_name` | varchar | YES |  |
| 39 | `user_surname` | varchar | YES |  |
| 40 | `user_second_surname` | varchar | YES |  |
| 41 | `user_phone` | varchar | YES |  |
| 42 | `user_email` | varchar | YES |  |
| 43 | `user_birthdate` | varchar | YES |  |
| 44 | `user_gender` | varchar | YES |  |
| 45 | `user_residence_address` | varchar | YES |  |
| 46 | `user_residence_city` | varchar | YES |  |
| 47 | `incomplete_spiga_data` | varchar | YES |  |
| 48 | `company_group_id` | decimal(20,0) | YES |  |
| 49 | `company_group_agile_id` | varchar | YES |  |
| 50 | `company_group_spiga_id` | varchar | YES |  |
| 51 | `company_group_name` | varchar | YES |  |
| 52 | `company_id` | decimal(20,0) | YES |  |
| 53 | `company_agile_id` | varchar | YES |  |
| 54 | `company_spiga_id` | varchar | YES |  |
| 55 | `company_name` | varchar | YES |  |
| 56 | `headquarter_id` | decimal(20,0) | YES |  |
| 57 | `headquarter_agile_id` | varchar | YES |  |
| 58 | `headquarter_spiga_id` | varchar | YES |  |
| 59 | `headquarter_name` | varchar | YES |  |
| 60 | `adviser_manager_id` | decimal(20,0) | YES |  |
| 61 | `adviser_manager_identification_number` | bigint | YES |  |
| 62 | `adviser_manager_name` | varchar | YES |  |
| 63 | `adviser_manager_email` | varchar | YES |  |
| 64 | `adviser_id` | decimal(20,0) | YES |  |
| 65 | `adviser_identification_number` | bigint | YES |  |
| 66 | `adviser_name` | varchar | YES |  |
| 67 | `adviser_email` | varchar | YES |  |
| 68 | `date_time_response` | timestamp(3) | YES |  |
| 69 | `insurance_entity_id` | decimal(20,0) | YES |  |
| 70 | `insurance_entity_name` | varchar | YES |  |
| 71 | `response_time` | bigint | YES |  |
| 72 | `finished_at` | varchar | YES |  |
| 73 | `invoice_date` | timestamp(3) | YES |  |
| 74 | `created_at` | timestamp(3) | YES |  |
| 75 | `updated_at` | timestamp(3) | YES |  |
| 76 | `created_at_invoice` | varchar | YES |  |
| 77 | `created_at_delivery` | varchar | YES |  |
| 78 | `created_at_quotation` | timestamp(3) | YES |  |

### eos_prod_core.vw_traking

**Columnas:** 64

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `financing_entry_id` | decimal(20,0) | YES |  |
| 3 | `case_number` | varchar | YES |  |
| 4 | `days_since_creation` | integer | YES |  |
| 5 | `step_id` | decimal(20,0) | YES |  |
| 6 | `step_name` | varchar | YES |  |
| 7 | `created_study` | timestamp(3) | YES |  |
| 8 | `created_approved` | timestamp(3) | YES |  |
| 9 | `created_disbursement` | timestamp(3) | YES |  |
| 10 | `approved_amount` | double | YES |  |
| 11 | `disbursement_amount` | double | YES |  |
| 12 | `approved_rate` | double | YES |  |
| 13 | `approved_terms_months` | integer | YES |  |
| 14 | `rejection_cause` | varchar | YES |  |
| 15 | `financing_entity_id` | decimal(20,0) | YES |  |
| 16 | `financing_entity_name` | varchar | YES |  |
| 17 | `vehicle_status` | varchar | YES |  |
| 18 | `placa` | varchar | YES |  |
| 19 | `vin` | varchar | YES |  |
| 20 | `vehicle_brand` | varchar | YES |  |
| 21 | `vehicle_model` | varchar | YES |  |
| 22 | `vehicle_year` | varchar | YES |  |
| 23 | `vehicle_version` | varchar | YES |  |
| 24 | `vehicle_value` | varchar | YES |  |
| 25 | `financing_value` | varchar | YES |  |
| 26 | `vehicle_service_type` | varchar | YES |  |
| 27 | `circulation_city` | varchar | YES |  |
| 28 | `user_document_type` | varchar | YES |  |
| 29 | `user_identification_number` | bigint | YES |  |
| 30 | `user_first_name` | varchar | YES |  |
| 31 | `user_second_name` | varchar | YES |  |
| 32 | `user_surname` | varchar | YES |  |
| 33 | `user_second_surname` | varchar | YES |  |
| 34 | `user_phone` | varchar | YES |  |
| 35 | `user_email` | varchar | YES |  |
| 36 | `user_birthdate` | varchar | YES |  |
| 37 | `user_gender` | varchar | YES |  |
| 38 | `user_residence_address` | varchar | YES |  |
| 39 | `user_residence_city` | varchar | YES |  |
| 40 | `company_group_id` | decimal(20,0) | YES |  |
| 41 | `company_group_agile_id` | varchar | YES |  |
| 42 | `company_group_spiga_id` | varchar | YES |  |
| 43 | `company_group_name` | varchar | YES |  |
| 44 | `company_id` | decimal(20,0) | YES |  |
| 45 | `company_agile_id` | varchar | YES |  |
| 46 | `company_spiga_id` | varchar | YES |  |
| 47 | `company_name` | varchar | YES |  |
| 48 | `headquarter_id` | decimal(20,0) | YES |  |
| 49 | `headquarter_agile_id` | varchar | YES |  |
| 50 | `headquarter_spiga_id` | varchar | YES |  |
| 51 | `headquarter_name` | varchar | YES |  |
| 52 | `adviser_manager_id` | decimal(20,0) | YES |  |
| 53 | `adviser_manager_identification_number` | bigint | YES |  |
| 54 | `adviser_manager_name` | varchar | YES |  |
| 55 | `adviser_manager_email` | varchar | YES |  |
| 56 | `adviser_id` | decimal(20,0) | YES |  |
| 57 | `adviser_identification_number` | bigint | YES |  |
| 58 | `adviser_name` | varchar | YES |  |
| 59 | `adviser_email` | varchar | YES |  |
| 60 | `response_time` | bigint | YES |  |
| 61 | `finished_at` | varchar | YES |  |
| 62 | `date_time_response` | timestamp(3) | YES |  |
| 63 | `created_at` | timestamp(3) | YES |  |
| 64 | `updated_at` | timestamp(3) | YES |  |

### eos_prod_core.vw_traking_unique

**Columnas:** 25

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | decimal(20,0) | YES |  |
| 2 | `financing_entry_id` | decimal(20,0) | YES |  |
| 3 | `case_number` | varchar | YES |  |
| 4 | `days_since_creation` | integer | YES |  |
| 5 | `step_id` | decimal(20,0) | YES |  |
| 6 | `step_name` | varchar | YES |  |
| 7 | `approved_amount` | double | YES |  |
| 8 | `approved_rate` | double | YES |  |
| 9 | `approved_terms_months` | integer | YES |  |
| 10 | `rejection_cause` | varchar | YES |  |
| 11 | `adviser_manager_id` | decimal(20,0) | YES |  |
| 12 | `adviser_manager_identification_number` | bigint | YES |  |
| 13 | `adviser_manager_name` | varchar | YES |  |
| 14 | `adviser_manager_email` | varchar | YES |  |
| 15 | `adviser_id` | decimal(20,0) | YES |  |
| 16 | `adviser_identification_number` | bigint | YES |  |
| 17 | `adviser_name` | varchar | YES |  |
| 18 | `adviser_email` | varchar | YES |  |
| 19 | `date_time_response` | timestamp(3) | YES |  |
| 20 | `financing_entity_id` | decimal(20,0) | YES |  |
| 21 | `financing_entity_name` | varchar | YES |  |
| 22 | `response_time` | bigint | YES |  |
| 23 | `finished_at` | varchar | YES |  |
| 24 | `created_at` | timestamp(3) | YES |  |
| 25 | `updated_at` | timestamp(3) | YES |  |

## 🥈 genai

`Capa: Plata / Materialized`

### genai.asousados

**Columnas:** 6

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `segmento` | varchar | YES |  |
| 2 | `marca` | varchar | YES |  |
| 3 | `tipo` | varchar | YES |  |
| 4 | `catalogo` | varchar | YES |  |
| 5 | `modelo` | varchar | YES |  |
| 6 | `monto_venta` | double | YES |  |

### genai.modelo_recomendacion

**Columnas:** 18

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `nit` | bigint | YES |  |
| 2 | `tipo_persona` | varchar | YES |  |
| 3 | `es_juridico` | bigint | YES |  |
| 4 | `num_compras` | bigint | YES |  |
| 5 | `segmento` | varchar | YES |  |
| 6 | `dias_predichos` | bigint | YES |  |
| 7 | `fecha_estimada` | varchar | YES |  |
| 8 | `dias_hasta_estimada` | bigint | YES |  |
| 9 | `urgencia` | varchar | YES |  |
| 10 | `ultima_fecha` | varchar | YES |  |
| 11 | `ultimo_vin` | varchar | YES |  |
| 12 | `ultima_gama` | varchar | YES |  |
| 13 | `ultima_marca` | varchar | YES |  |
| 14 | `ultimo_valor` | double | YES |  |
| 15 | `recomendacion_transicion_v1` | varchar | YES |  |
| 16 | `recomendacion_similitud_v1` | varchar | YES |  |
| 17 | `recomendacion_transicion_v2` | varchar | YES |  |
| 18 | `recomendacion_similitud_v2` | varchar | YES |  |

### genai.variables_macroeconomicas

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `fecha` | date | YES |  |
| 2 | `trm_cop_usd` | decimal(10,2) | YES |  |
| 3 | `ipc` | decimal(10,2) | YES |  |
| 4 | `ibr_overnight` | decimal(10,3) | YES |  |
| 5 | `euro_cop_eur` | decimal(10,5) | YES |  |
| 6 | `ibr_3m` | decimal(10,3) | YES |  |
| 7 | `ibr_6m` | decimal(10,3) | YES |  |
| 8 | `ibr_12m` | decimal(10,3) | YES |  |

## 📚 maestras

`Capa: Bronce / Referencia (lookup)`

### maestras.ciudad_por_centro

**Columnas:** 2

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `nombre_centro` | varchar | YES |  |
| 2 | `ciudad` | varchar | YES |  |

### maestras.linea_por_sigla

**Columnas:** 2

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sigla_centro` | varchar | YES |  |
| 2 | `linea` | varchar | YES |  |

### maestras.linea_por_sigla_taller

**Columnas:** 4

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sigla` | varchar | YES |  |
| 2 | `linea` | varchar | YES |  |
| 3 | `match_type` | varchar | YES |  |
| 4 | `priority` | varchar | YES |  |

### maestras.normalizacion_centros_taller

**Columnas:** 2

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `nombre_original` | varchar | YES |  |
| 2 | `nombre_normalizado` | varchar | YES |  |

### maestras.tipo_cargo_taller

**Columnas:** 2

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codigo` | varchar | YES |  |
| 2 | `descripcion` | varchar | YES |  |

## 🥉 nbp021-byss

`Capa: Bronce / Raw`

### nbp021-byss.ci_custodio_fasecolda

**Columnas:** 28

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `vin` | varchar | YES |  |
| 2 | `anio` | integer | YES |  |
| 3 | `mes` | integer | YES |  |
| 4 | `descripcion_compra_estados` | varchar | YES |  |
| 5 | `nombre_marca` | varchar | YES |  |
| 6 | `nombre_modelo` | varchar | YES |  |
| 7 | `nombre_gama` | varchar | YES |  |
| 8 | `cod_modelo` | varchar | YES |  |
| 9 | `color` | varchar | YES |  |
| 10 | `anio_modelo` | varchar | YES |  |
| 11 | `nombre_centro` | varchar | YES |  |
| 12 | `inventario_custodio` | integer | YES |  |
| 13 | `color_def` | varchar | YES |  |
| 14 | `codigo_homologo` | varchar | YES |  |
| 15 | `clase_fc` | varchar | YES |  |
| 16 | `carroceria_fc` | varchar | YES |  |
| 17 | `marca_fc` | varchar | YES |  |
| 18 | `linea_fc` | varchar | YES |  |
| 19 | `linea_consolidada_fc` | varchar | YES |  |
| 20 | `modelo_fc` | varchar | YES |  |
| 21 | `cilindraje_fc` | varchar | YES |  |
| 22 | `combustible_fc` | varchar | YES |  |
| 23 | `airbags_fc` | varchar | YES |  |
| 24 | `transmision_fc` | varchar | YES |  |
| 25 | `tipo_traccion_fc` | varchar | YES |  |
| 26 | `version_fc` | varchar | YES |  |
| 27 | `especificaciones_fc` | varchar | YES |  |
| 28 | `traccion_tipo_fc` | varchar | YES |  |

### nbp021-byss.ci_entregas_fasecolda

**Columnas:** 34

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `vin` | varchar | YES |  |
| 2 | `centro` | varchar | YES |  |
| 3 | `codigo_modelo` | varchar | YES |  |
| 4 | `anio_modelo` | varchar | YES |  |
| 5 | `marca` | varchar | YES |  |
| 6 | `clasificacion` | varchar | YES |  |
| 7 | `modelo_version` | varchar | YES |  |
| 8 | `tipo` | varchar | YES |  |
| 9 | `gama` | varchar | YES |  |
| 10 | `color` | varchar | YES |  |
| 11 | `fechaentregacliente` | date | YES |  |
| 12 | `cantidad` | integer | YES |  |
| 13 | `precio_venta` | decimal(18,2) | YES |  |
| 14 | `netocompra` | decimal(38,13) | YES |  |
| 15 | `netoventa` | decimal(38,4) | YES |  |
| 16 | `margen` | decimal(38,4) | YES |  |
| 17 | `por_margen` | decimal(38,6) | YES |  |
| 18 | `rn` | bigint | YES |  |
| 19 | `colortransformado` | varchar | YES |  |
| 20 | `codigo_homologo` | varchar | YES |  |
| 21 | `clase_fc` | varchar | YES |  |
| 22 | `carroceria_fc` | varchar | YES |  |
| 23 | `marca_fc` | varchar | YES |  |
| 24 | `linea_fc` | varchar | YES |  |
| 25 | `linea_consolidada_fc` | varchar | YES |  |
| 26 | `modelo_fc` | varchar | YES |  |
| 27 | `cilindraje_fc` | varchar | YES |  |
| 28 | `combustible_fc` | varchar | YES |  |
| 29 | `airbags_fc` | varchar | YES |  |
| 30 | `transmision_fc` | varchar | YES |  |
| 31 | `tipo_traccion_fc` | varchar | YES |  |
| 32 | `version_fc` | varchar | YES |  |
| 33 | `especificaciones_fc` | varchar | YES |  |
| 34 | `traccion_tipo_fc` | varchar | YES |  |

### nbp021-byss.ci_facturados_no_entregados_fasecolda

**Columnas:** 34

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `vin` | varchar | YES |  |
| 2 | `anio` | integer | YES |  |
| 3 | `mes` | integer | YES |  |
| 4 | `nombre_centro` | varchar | YES |  |
| 5 | `codigo_modelo` | varchar | YES |  |
| 6 | `modelo_version` | varchar | YES |  |
| 7 | `nombregama` | varchar | YES |  |
| 8 | `descripcion_compra_tipos` | varchar | YES |  |
| 9 | `nombre_marca` | varchar | YES |  |
| 10 | `clasificacion` | varchar | YES |  |
| 11 | `anio_modelo` | varchar | YES |  |
| 12 | `fecha_corte` | date | YES |  |
| 13 | `fecha_venta` | date | YES |  |
| 14 | `color` | varchar | YES |  |
| 15 | `fecha_entrega_cliente` | date | YES |  |
| 16 | `no_entregado` | varchar | YES |  |
| 17 | `marca_base` | varchar | YES |  |
| 18 | `registros` | integer | YES |  |
| 19 | `colortransformado` | varchar | YES |  |
| 20 | `codigo_homologo` | varchar | YES |  |
| 21 | `clase_fc` | varchar | YES |  |
| 22 | `carroceria_fc` | varchar | YES |  |
| 23 | `marca_fc` | varchar | YES |  |
| 24 | `linea_fc` | varchar | YES |  |
| 25 | `linea_consolidada_fc` | varchar | YES |  |
| 26 | `modelo_fc` | varchar | YES |  |
| 27 | `cilindraje_fc` | varchar | YES |  |
| 28 | `combustible_fc` | varchar | YES |  |
| 29 | `airbags_fc` | varchar | YES |  |
| 30 | `transmision_fc` | varchar | YES |  |
| 31 | `tipo_traccion_fc` | varchar | YES |  |
| 32 | `version_fc` | varchar | YES |  |
| 33 | `especificaciones_fc` | varchar | YES |  |
| 34 | `traccion_tipo_fc` | varchar | YES |  |

### nbp021-byss.ci_homologacion_fasecolda_mayorista

**Columnas:** 23

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `nombre_marca` | varchar | YES |  |
| 2 | `nombre_gama` | varchar | YES |  |
| 3 | `nombre_modelo` | varchar | YES |  |
| 4 | `nombre_version` | varchar | YES |  |
| 5 | `anio_modelo` | integer | YES |  |
| 6 | `marca_homologada` | varchar | YES |  |
| 7 | `codigo_homologo` | varchar | YES |  |
| 8 | `confiabilidad` | integer | YES |  |
| 9 | `comentario` | varchar | YES |  |
| 10 | `created_at` | timestamp(3) | YES |  |
| 11 | `clase` | varchar | YES |  |
| 12 | `carroceria` | varchar | YES |  |
| 13 | `marca` | varchar | YES |  |
| 14 | `linea` | varchar | YES |  |
| 15 | `linea_consolidada` | varchar | YES |  |
| 16 | `cilindraje` | varchar | YES |  |
| 17 | `combustible` | varchar | YES |  |
| 18 | `airbags` | varchar | YES |  |
| 19 | `transmision` | varchar | YES |  |
| 20 | `tipo_traccion` | varchar | YES |  |
| 21 | `version` | varchar | YES |  |
| 22 | `especificaciones` | varchar | YES |  |
| 23 | `traccion_tipo` | varchar | YES |  |

### nbp021-byss.ci_inventario_fasecolda

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `anio` | integer | YES |  |
| 2 | `mes` | integer | YES |  |
| 3 | `vin` | varchar | YES |  |
| 4 | `descripcion_compra_estados` | varchar | YES |  |
| 5 | `nombre_marca` | varchar | YES |  |
| 6 | `clasificacion` | varchar | YES |  |
| 7 | `nombre_modelo` | varchar | YES |  |
| 8 | `nombre_gama` | varchar | YES |  |
| 9 | `cod_modelo` | varchar | YES |  |
| 10 | `color` | varchar | YES |  |
| 11 | `anio_modelo` | varchar | YES |  |
| 12 | `fechadecorte` | date | YES |  |
| 13 | `nombre_centro` | varchar | YES |  |
| 14 | `valida_custodio` | varchar | YES |  |
| 15 | `inventario` | integer | YES |  |
| 16 | `codigo_homologo` | varchar | YES |  |
| 17 | `clase_fc` | varchar | YES |  |
| 18 | `carroceria_fc` | varchar | YES |  |
| 19 | `marca_fc` | varchar | YES |  |
| 20 | `linea_fc` | varchar | YES |  |
| 21 | `linea_consolidada_fc` | varchar | YES |  |
| 22 | `modelo_fc` | varchar | YES |  |
| 23 | `cilindraje_fc` | varchar | YES |  |
| 24 | `combustible_fc` | varchar | YES |  |
| 25 | `airbags_fc` | varchar | YES |  |
| 26 | `transmision_fc` | varchar | YES |  |
| 27 | `tipo_traccion_fc` | varchar | YES |  |
| 28 | `version_fc` | varchar | YES |  |
| 29 | `especificaciones_fc` | varchar | YES |  |
| 30 | `traccion_tipo_fc` | varchar | YES |  |

### nbp021-byss.ci_runt_fasecolda

**Columnas:** 41

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `a�o_matricula` | integer | YES |  |
| 2 | `mes_matricula` | integer | YES |  |
| 3 | `dia_matricula` | integer | YES |  |
| 4 | `clase` | varchar | YES |  |
| 5 | `carroceria` | varchar | YES |  |
| 6 | `marca` | varchar | YES |  |
| 7 | `clasificacion` | varchar | YES |  |
| 8 | `linea` | varchar | YES |  |
| 9 | `modelo` | integer | YES |  |
| 10 | `cilindraje` | integer | YES |  |
| 11 | `combustible` | varchar | YES |  |
| 12 | `airbag` | varchar | YES |  |
| 13 | `tipo_transmision` | varchar | YES |  |
| 14 | `tipo_traccion` | varchar | YES |  |
| 15 | `segmento` | varchar | YES |  |
| 16 | `segmento_x_europeo` | varchar | YES |  |
| 17 | `segmento_europeo` | varchar | YES |  |
| 18 | `body_style_europeo` | varchar | YES |  |
| 19 | `marca_homologada` | varchar | YES |  |
| 20 | `linea_homologada` | varchar | YES |  |
| 21 | `id_vehiculo` | integer | YES |  |
| 22 | `seg` | varchar | YES |  |
| 23 | `sub_seg` | varchar | YES |  |
| 24 | `linea_consolidada_seg` | varchar | YES |  |
| 25 | `cantidades` | bigint | YES |  |
| 26 | `codigo_fasecolda` | varchar | YES |  |
| 27 | `clase_fc` | varchar | YES |  |
| 28 | `carroceria_fc` | varchar | YES |  |
| 29 | `marca_fc` | varchar | YES |  |
| 30 | `linea_fc` | varchar | YES |  |
| 31 | `linea_consolidada_fc` | varchar | YES |  |
| 32 | `modelo_fc` | varchar | YES |  |
| 33 | `cilindraje_fc` | varchar | YES |  |
| 34 | `combustible_fc` | varchar | YES |  |
| 35 | `airbags_fc` | varchar | YES |  |
| 36 | `transmision_fc` | varchar | YES |  |
| 37 | `tipo_traccion_fc` | varchar | YES |  |
| 38 | `version_fc` | varchar | YES |  |
| 39 | `especificaciones_fc` | varchar | YES |  |
| 40 | `traccion_tipo_fc` | varchar | YES |  |
| 41 | `marca_no_contar` | integer | YES |  |

### nbp021-byss.ci_runt_homologacion_livianos

**Columnas:** 13

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `marca` | varchar | YES |  |
| 2 | `linea` | varchar | YES |  |
| 3 | `modelo` | integer | YES |  |
| 4 | `cilindraje` | decimal(20,0) | YES |  |
| 5 | `combustible` | varchar | YES |  |
| 6 | `tipo_transmision` | varchar | YES |  |
| 7 | `tipo_traccion` | varchar | YES |  |
| 8 | `codigo_fasecolda` | varchar | YES |  |
| 9 | `confiabilidad` | integer | YES |  |
| 10 | `intentos_fallidos` | integer | YES |  |
| 11 | `ultimo_intento` | timestamp(3) | YES |  |
| 12 | `disponible_desde` | timestamp(3) | YES |  |
| 13 | `excluir_homologacion` | varchar | YES |  |

### nbp021-byss.ci_runt_homologacion_pesados

**Columnas:** 13

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `marca` | varchar | YES |  |
| 2 | `linea` | varchar | YES |  |
| 3 | `modelo` | integer | YES |  |
| 4 | `cilindraje` | double | YES |  |
| 5 | `combustible` | varchar | YES |  |
| 6 | `tipo_transmision` | varchar | YES |  |
| 7 | `tipo_traccion` | varchar | YES |  |
| 8 | `codigo_fasecolda` | varchar | YES |  |
| 9 | `confiabilidad` | integer | YES |  |
| 10 | `intentos_fallidos` | integer | YES |  |
| 11 | `ultimo_intento` | timestamp(3) | YES |  |
| 12 | `disponible_desde` | timestamp(3) | YES |  |
| 13 | `excluir_homologacion` | varchar | YES |  |

### nbp021-byss.fasecolda_vehicles

**Columnas:** 11

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `year` | integer | YES |  |
| 3 | `brand` | varchar | YES |  |
| 4 | `model` | varchar | YES |  |
| 5 | `version` | varchar | YES |  |
| 6 | `extra` | varchar | YES |  |
| 7 | `display_name` | varchar | YES |  |
| 8 | `cf` | varchar | YES |  |
| 9 | `ch` | varchar | YES |  |
| 10 | `fasecolda_version_id` | varchar | YES |  |
| 11 | `payload` | varchar | YES |  |

### nbp021-byss.runt_clasificacion_europea

**Columnas:** 5

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `marca` | varchar | YES |  |
| 2 | `linea` | varchar | YES |  |
| 3 | `segmento_x` | varchar | YES |  |
| 4 | `segmento` | varchar | YES |  |
| 5 | `body_style` | varchar | YES |  |

### nbp021-byss.runt_vehicle_fasecolda_matching

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `a�o_matricula` | integer | YES |  |
| 2 | `clase` | varchar | YES |  |
| 3 | `carroceria` | varchar | YES |  |
| 4 | `marca` | varchar | YES |  |
| 5 | `linea` | varchar | YES |  |
| 6 | `modelo` | integer | YES |  |
| 7 | `cilindraje` | decimal(28,6) | YES |  |
| 8 | `combustible` | varchar | YES |  |
| 9 | `airbag` | integer | YES |  |
| 10 | `tipo_transmision` | varchar | YES |  |
| 11 | `tipo_traccion` | varchar | YES |  |
| 12 | `runt_registro` | varchar | YES |  |
| 13 | `codigo_fasecolda` | varchar | YES |  |
| 14 | `confiabilidad` | decimal(5,2) | YES |  |
| 15 | `comentario` | varchar | YES |  |

## 🥈 nebula
`Capa: Plata / Materialized`

### nebula.materialized_leads_tracking

**Columnas:** 44

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `lead_id` | bigint | YES |  |
| 3 | `clasification_id` | bigint | YES |  |
| 4 | `clasification_name` | varchar | YES |  |
| 5 | `action_id` | bigint | YES |  |
| 6 | `action_name` | varchar | YES |  |
| 7 | `status_id` | bigint | YES |  |
| 8 | `status_name` | varchar | YES |  |
| 9 | `campaing_id` | bigint | YES |  |
| 10 | `campaing_name` | varchar | YES |  |
| 11 | `channel_id` | bigint | YES |  |
| 12 | `channel_value` | varchar | YES |  |
| 13 | `medium_id` | bigint | YES |  |
| 14 | `medium_value` | varchar | YES |  |
| 15 | `category_id` | bigint | YES |  |
| 16 | `category_name` | varchar | YES |  |
| 17 | `country_name` | varchar | YES |  |
| 18 | `company_name` | varchar | YES |  |
| 19 | `brand_id` | bigint | YES |  |
| 20 | `brand_name` | varchar | YES |  |
| 21 | `wholesaler` | bigint | YES |  |
| 22 | `adviser_id` | bigint | YES |  |
| 23 | `adviser_name` | varchar | YES |  |
| 24 | `adviser_email` | varchar | YES |  |
| 25 | `adviser_document_type` | varchar | YES |  |
| 26 | `adviser_document_number` | varchar | YES |  |
| 27 | `concessionaire_id` | bigint | YES |  |
| 28 | `concessionaire_names` | varchar | YES |  |
| 29 | `client_name` | varchar | YES |  |
| 30 | `client_phone` | varchar | YES |  |
| 31 | `client_email` | varchar | YES |  |
| 32 | `client_document_type_name` | varchar | YES |  |
| 33 | `client_document_number` | varchar | YES |  |
| 34 | `model_id` | bigint | YES |  |
| 35 | `model_name` | varchar | YES |  |
| 36 | `model_year` | varchar | YES |  |
| 37 | `license_plate` | varchar | YES |  |
| 38 | `created_at` | timestamp(3) | YES |  |
| 39 | `updated_at` | timestamp(3) | YES |  |
| 40 | `lead_created_at` | timestamp(3) | YES |  |
| 41 | `management_time` | bigint | YES |  |
| 42 | `adviser_business_type_id` | bigint | YES |  |
| 43 | `adviser_business_type` | varchar | YES |  |
| 44 | `load_date` | varchar | YES |  |

### nebula.materialized_leads_tracking_filtered

**Columnas:** 40

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `lead_id` | bigint | YES |  |
| 3 | `clasification_id` | bigint | YES |  |
| 4 | `clasification_name` | varchar | YES |  |
| 5 | `action_id` | bigint | YES |  |
| 6 | `action_name` | varchar | YES |  |
| 7 | `status_id` | bigint | YES |  |
| 8 | `status_name` | varchar | YES |  |
| 9 | `campaing_id` | bigint | YES |  |
| 10 | `campaing_name` | varchar | YES |  |
| 11 | `medium_id` | bigint | YES |  |
| 12 | `medium_value` | varchar | YES |  |
| 13 | `category_id` | bigint | YES |  |
| 14 | `category_name` | varchar | YES |  |
| 15 | `country_name` | varchar | YES |  |
| 16 | `company_name` | varchar | YES |  |
| 17 | `brand_id` | bigint | YES |  |
| 18 | `brand_name` | varchar | YES |  |
| 19 | `wholesaler` | bigint | YES |  |
| 20 | `adviser_id` | bigint | YES |  |
| 21 | `adviser_name` | varchar | YES |  |
| 22 | `adviser_email` | varchar | YES |  |
| 23 | `adviser_document_type` | varchar | YES |  |
| 24 | `adviser_document_number` | varchar | YES |  |
| 25 | `adviser_business_type_id` | bigint | YES |  |
| 26 | `adviser_business_type` | varchar | YES |  |
| 27 | `concessionaire_id` | bigint | YES |  |
| 28 | `concessionaire_names` | varchar | YES |  |
| 29 | `client_name` | varchar | YES |  |
| 30 | `client_phone` | varchar | YES |  |
| 31 | `client_email` | varchar | YES |  |
| 32 | `client_document_type_name` | varchar | YES |  |
| 33 | `client_document_number` | varchar | YES |  |
| 34 | `model_id` | bigint | YES |  |
| 35 | `model_name` | varchar | YES |  |
| 36 | `model_year` | varchar | YES |  |
| 37 | `license_plate` | varchar | YES |  |
| 38 | `created_at` | timestamp(3) | YES |  |
| 39 | `updated_at` | timestamp(3) | YES |  |
| 40 | `fecha_cargue` | varchar | YES |  |

### nebula.vw_financial_requests

**Columnas:** 109

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `financing_entry_id` | varchar | YES |  |
| 2 | `primer-nombre` | varchar | YES |  |
| 3 | `segundo-nombre` | varchar | YES |  |
| 4 | `primer-apellido` | varchar | YES |  |
| 5 | `segundo-apellido` | varchar | YES |  |
| 6 | `email` | varchar | YES |  |
| 7 | `numero-de-celular` | varchar | YES |  |
| 8 | `tipo-de-identificacion` | varchar | YES |  |
| 9 | `numero-de-identificacion` | varchar | YES |  |
| 10 | `fecha-expedicion` | varchar | YES |  |
| 11 | `ciudad-expedicion` | varchar | YES |  |
| 12 | `fecha-nacimiento` | varchar | YES |  |
| 13 | `lugar-de-nacimiento` | varchar | YES |  |
| 14 | `genero` | varchar | YES |  |
| 15 | `estado-civil` | varchar | YES |  |
| 16 | `edad` | varchar | YES |  |
| 17 | `nacionalidad` | varchar | YES |  |
| 18 | `departamento-residencia` | varchar | YES |  |
| 19 | `ciudad-residencia` | varchar | YES |  |
| 20 | `direccion-residencia` | varchar | YES |  |
| 21 | `informacion-adicional` | varchar | YES |  |
| 22 | `antiguedad-residencia` | varchar | YES |  |
| 23 | `telefono-fijo` | varchar | YES |  |
| 24 | `tipo-vivienda` | varchar | YES |  |
| 25 | `estrato` | varchar | YES |  |
| 26 | `marca-vehiculo` | varchar | YES |  |
| 27 | `linea-vehiculo` | varchar | YES |  |
| 28 | `version-vehiculo` | varchar | YES |  |
| 29 | `vitrina` | varchar | YES |  |
| 30 | `valor-vehiculo` | varchar | YES |  |
| 31 | `plazo-financiacion` | varchar | YES |  |
| 32 | `valor-a-financiar` | varchar | YES |  |
| 33 | `ocupacion` | varchar | YES |  |
| 34 | `nivel-educativo` | varchar | YES |  |
| 35 | `profesiones` | varchar | YES |  |
| 36 | `declara-renta` | varchar | YES |  |
| 37 | `entidad-pagadora` | varchar | YES |  |
| 38 | `fecha-en-la-que-te-pensionaste` | varchar | YES |  |
| 39 | `nombre-institucion-donde-estudia` | varchar | YES |  |
| 40 | `numero-semestre-programa` | varchar | YES |  |
| 41 | `nombre-empresa` | varchar | YES |  |
| 42 | `actividad-economica` | varchar | YES |  |
| 43 | `ciudad-empresa` | varchar | YES |  |
| 44 | `direccion-empresa` | varchar | YES |  |
| 45 | `telefono-empresa` | varchar | YES |  |
| 46 | `tipo-de-contrato` | varchar | YES |  |
| 47 | `ingresos-mensuales` | varchar | YES |  |
| 48 | `fecha-inicio-trabajo-actual` | varchar | YES |  |
| 49 | `celular-referencia-personal` | varchar | YES |  |
| 50 | `parentesco-referencia-personal` | varchar | YES |  |
| 51 | `correo-referencia-personal` | varchar | YES |  |
| 52 | `direccion-referencia-personal` | varchar | YES |  |
| 53 | `goza-reconocimiento-publico-politico` | varchar | YES |  |
| 54 | `realiza-operaciones-moneda-extranjera` | varchar | YES |  |
| 55 | `residente-fiscal-pais-diferente-colombia` | varchar | YES |  |
| 56 | `basicos-mensuales` | varchar | YES |  |
| 57 | `variables-mensuales` | varchar | YES |  |
| 58 | `otros-ingresos` | varchar | YES |  |
| 59 | `egresos-mensuales` | varchar | YES |  |
| 60 | `personas-a-cargo` | varchar | YES |  |
| 61 | `valor-total-activos` | varchar | YES |  |
| 62 | `valor-total-vehiculos` | varchar | YES |  |
| 63 | `valor-total-pasivos` | varchar | YES |  |
| 64 | `foto-cedula-frontal` | varchar | YES |  |
| 65 | `foto-cedula-posterior` | varchar | YES |  |
| 66 | `anio-vehiculo` | varchar | YES |  |
| 67 | `pais-de-expedicion` | varchar | YES |  |
| 68 | `departamento-de-expedicion` | varchar | YES |  |
| 69 | `pais-de-residencia` | varchar | YES |  |
| 70 | `pais-de-nacimiento` | varchar | YES |  |
| 71 | `departamento-de-nacimiento` | varchar | YES |  |
| 72 | `pais-de-la-empresa` | varchar | YES |  |
| 73 | `departamento-de-la-empresa` | varchar | YES |  |
| 74 | `estado-del-vehiculo` | varchar | YES |  |
| 75 | `tipo-de-servicio-del-vehiculo` | varchar | YES |  |
| 76 | `nombre-referencia-personal` | varchar | YES |  |
| 77 | `nombre-referencia-familiar` | varchar | YES |  |
| 78 | `parentesco-referencia-familiar` | varchar | YES |  |
| 79 | `telefono-referencia-familiar` | varchar | YES |  |
| 80 | `por-concepto-de` | varchar | YES |  |
| 81 | `asesores` | varchar | YES |  |
| 82 | `relacion-persona-suma-ingresos` | varchar | YES |  |
| 83 | `sumar-ingresos` | varchar | YES |  |
| 84 | `foto-cedula-frontal-parentesco` | varchar | YES |  |
| 85 | `foto-cedula-posterior-parentesco` | varchar | YES |  |
| 86 | `term-conditions-relationship` | varchar | YES |  |
| 87 | `total-gastos-mensuales` | varchar | YES |  |
| 88 | `numero-de-celular-parentesco` | varchar | YES |  |
| 89 | `tipo-de-identificacion-suma-ingresos` | varchar | YES |  |
| 90 | `numero-de-identificacion-suma-ingresos` | varchar | YES |  |
| 91 | `correo-electronico-suma-ingresos` | varchar | YES |  |
| 92 | `primer-nombre-suma-ingresos` | varchar | YES |  |
| 93 | `segundo-nombre-suma-ingresos` | varchar | YES |  |
| 94 | `primer-apellido-suma-ingresos` | varchar | YES |  |
| 95 | `segundo-apellido-suma-ingresos` | varchar | YES |  |
| 96 | `fecha-de-nacimiento-suma-ingresos` | varchar | YES |  |
| 97 | `edad-suma-ingresos` | varchar | YES |  |
| 98 | `nombre-empresa-suma-ingresos` | varchar | YES |  |
| 99 | `actividad-economica-suma-ingresos` | varchar | YES |  |
| 100 | `direccion-empresa-suma-ingresos` | varchar | YES |  |
| 101 | `telefono-empresa-suma-ingresos` | varchar | YES |  |
| 102 | `fecha-inicio-trabajo-actual-suma-ingresos` | varchar | YES |  |
| 103 | `ingreso-mensual-suma-ingresos` | varchar | YES |  |
| 104 | `otros-ingresos-suma-ingresos` | varchar | YES |  |
| 105 | `grupo-etnico` | varchar | YES |  |
| 106 | `company` | varchar | YES |  |
| 107 | `line` | varchar | YES |  |
| 108 | `headquarter` | varchar | YES |  |
| 109 | `load_date` | varchar | YES |  |

### nebula.vw_financial_requests_filtered

**Columnas:** 105

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `financing_entry_id` | varchar | YES |  |
| 2 | `primer-nombre` | varchar | YES |  |
| 3 | `segundo-nombre` | varchar | YES |  |
| 4 | `primer-apellido` | varchar | YES |  |
| 5 | `segundo-apellido` | varchar | YES |  |
| 6 | `email` | varchar | YES |  |
| 7 | `numero-de-celular` | varchar | YES |  |
| 8 | `tipo-de-identificacion` | varchar | YES |  |
| 9 | `numero-de-identificacion` | varchar | YES |  |
| 10 | `fecha-expedicion` | varchar | YES |  |
| 11 | `ciudad-expedicion` | varchar | YES |  |
| 12 | `fecha-nacimiento` | varchar | YES |  |
| 13 | `lugar-de-nacimiento` | varchar | YES |  |
| 14 | `genero` | varchar | YES |  |
| 15 | `estado-civil` | varchar | YES |  |
| 16 | `edad` | varchar | YES |  |
| 17 | `nacionalidad` | varchar | YES |  |
| 18 | `departamento-residencia` | varchar | YES |  |
| 19 | `ciudad-residencia` | varchar | YES |  |
| 20 | `direccion-residencia` | varchar | YES |  |
| 21 | `informacion-adicional` | varchar | YES |  |
| 22 | `antiguedad-residencia` | varchar | YES |  |
| 23 | `telefono-fijo` | varchar | YES |  |
| 24 | `tipo-vivienda` | varchar | YES |  |
| 25 | `estrato` | varchar | YES |  |
| 26 | `marca-vehiculo` | varchar | YES |  |
| 27 | `linea-vehiculo` | varchar | YES |  |
| 28 | `version-vehiculo` | varchar | YES |  |
| 29 | `vitrina` | varchar | YES |  |
| 30 | `valor-vehiculo` | varchar | YES |  |
| 31 | `plazo-financiacion` | varchar | YES |  |
| 32 | `valor-a-financiar` | varchar | YES |  |
| 33 | `ocupacion` | varchar | YES |  |
| 34 | `nivel-educativo` | varchar | YES |  |
| 35 | `profesiones` | varchar | YES |  |
| 36 | `declara-renta` | varchar | YES |  |
| 37 | `nombre-institucion-donde-estudia` | varchar | YES |  |
| 38 | `numero-semestre-programa` | varchar | YES |  |
| 39 | `nombre-empresa` | varchar | YES |  |
| 40 | `actividad-economica` | varchar | YES |  |
| 41 | `ciudad-empresa` | varchar | YES |  |
| 42 | `direccion-empresa` | varchar | YES |  |
| 43 | `telefono-empresa` | varchar | YES |  |
| 44 | `tipo-de-contrato` | varchar | YES |  |
| 45 | `ingresos-mensuales` | varchar | YES |  |
| 46 | `fecha-inicio-trabajo-actual` | varchar | YES |  |
| 47 | `celular-referencia-personal` | varchar | YES |  |
| 48 | `parentesco-referencia-personal` | varchar | YES |  |
| 49 | `correo-referencia-personal` | varchar | YES |  |
| 50 | `direccion-referencia-personal` | varchar | YES |  |
| 51 | `goza-reconocimiento-publico-politico` | varchar | YES |  |
| 52 | `realiza-operaciones-moneda-extranjera` | varchar | YES |  |
| 53 | `residente-fiscal-pais-diferente-colombia` | varchar | YES |  |
| 54 | `basicos-mensuales` | varchar | YES |  |
| 55 | `variables-mensuales` | varchar | YES |  |
| 56 | `otros-ingresos` | varchar | YES |  |
| 57 | `egresos-mensuales` | varchar | YES |  |
| 58 | `personas-a-cargo` | varchar | YES |  |
| 59 | `valor-total-activos` | varchar | YES |  |
| 60 | `valor-total-vehiculos` | varchar | YES |  |
| 61 | `valor-total-pasivos` | varchar | YES |  |
| 62 | `foto-cedula-frontal` | varchar | YES |  |
| 63 | `foto-cedula-posterior` | varchar | YES |  |
| 64 | `anio-vehiculo` | varchar | YES |  |
| 65 | `pais-de-expedicion` | varchar | YES |  |
| 66 | `departamento-de-expedicion` | varchar | YES |  |
| 67 | `pais-de-residencia` | varchar | YES |  |
| 68 | `pais-de-nacimiento` | varchar | YES |  |
| 69 | `departamento-de-nacimiento` | varchar | YES |  |
| 70 | `pais-de-la-empresa` | varchar | YES |  |
| 71 | `departamento-de-la-empresa` | varchar | YES |  |
| 72 | `estado-del-vehiculo` | varchar | YES |  |
| 73 | `tipo-de-servicio-del-vehiculo` | varchar | YES |  |
| 74 | `nombre-referencia-familiar` | varchar | YES |  |
| 75 | `parentesco-referencia-familiar` | varchar | YES |  |
| 76 | `telefono-referencia-familiar` | varchar | YES |  |
| 77 | `asesores` | varchar | YES |  |
| 78 | `relacion-persona-suma-ingresos` | varchar | YES |  |
| 79 | `sumar-ingresos` | varchar | YES |  |
| 80 | `foto-cedula-frontal-parentesco` | varchar | YES |  |
| 81 | `foto-cedula-posterior-parentesco` | varchar | YES |  |
| 82 | `term-conditions-relationship` | varchar | YES |  |
| 83 | `por-concepto-de` | varchar | YES |  |
| 84 | `total-gastos-mensuales` | varchar | YES |  |
| 85 | `numero-de-celular-parentesco` | varchar | YES |  |
| 86 | `tipo-de-identificacion-suma-ingresos` | varchar | YES |  |
| 87 | `numero-de-identificacion-suma-ingresos` | varchar | YES |  |
| 88 | `correo-electronico-suma-ingresos` | varchar | YES |  |
| 89 | `primer-nombre-suma-ingresos` | varchar | YES |  |
| 90 | `segundo-nombre-suma-ingresos` | varchar | YES |  |
| 91 | `primer-apellido-suma-ingresos` | varchar | YES |  |
| 92 | `segundo-apellido-suma-ingresos` | varchar | YES |  |
| 93 | `fecha-de-nacimiento-suma-ingresos` | varchar | YES |  |
| 94 | `edad-suma-ingresos` | varchar | YES |  |
| 95 | `nombre-empresa-suma-ingresos` | varchar | YES |  |
| 96 | `actividad-economica-suma-ingresos` | varchar | YES |  |
| 97 | `direccion-empresa-suma-ingresos` | varchar | YES |  |
| 98 | `telefono-empresa-suma-ingresos` | varchar | YES |  |
| 99 | `fecha-inicio-trabajo-actual-suma-ingresos` | varchar | YES |  |
| 100 | `ingreso-mensual-suma-ingresos` | varchar | YES |  |
| 101 | `otros-ingresos-suma-ingresos` | varchar | YES |  |
| 102 | `grupo-etnico` | varchar | YES |  |
| 103 | `company` | varchar | YES |  |
| 104 | `headquarter` | varchar | YES |  |
| 105 | `fecha_cargue` | varchar | YES |  |

### nebula.vw_financing_entry_values

**Columnas:** 5

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `financing_entry_id` | bigint | YES |  |
| 3 | `field_id` | bigint | YES |  |
| 4 | `field_value` | varchar | YES |  |
| 5 | `load_date` | varchar | YES |  |

### nebula.vw_quotation

**Columnas:** 42

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `ad_lead_id` | bigint | YES |  |
| 3 | `channel` | varchar | YES |  |
| 4 | `quotation_serial` | varchar | YES |  |
| 5 | `quotation_version` | bigint | YES |  |
| 6 | `adviser_id` | bigint | YES |  |
| 7 | `adviser_name` | varchar | YES |  |
| 8 | `adviser_document` | varchar | YES |  |
| 9 | `adviser_email` | varchar | YES |  |
| 10 | `adviser_brand` | varchar | YES |  |
| 11 | `adviser_company` | varchar | YES |  |
| 12 | `adviser_city` | varchar | YES |  |
| 13 | `adviser_country` | varchar | YES |  |
| 14 | `adviser_location` | varchar | YES |  |
| 15 | `adviser_center_id` | varchar | YES |  |
| 16 | `adviser_center_name` | varchar | YES |  |
| 17 | `customer_name` | varchar | YES |  |
| 18 | `customer_document_type` | varchar | YES |  |
| 19 | `customer_document` | varchar | YES |  |
| 20 | `customer_email` | varchar | YES |  |
| 21 | `customer_phone` | varchar | YES |  |
| 22 | `car_model` | varchar | YES |  |
| 23 | `car_version` | varchar | YES |  |
| 24 | `quotation_status` | varchar | YES |  |
| 25 | `quotation_views` | bigint | YES |  |
| 26 | `quotation_created_date` | timestamp(3) | YES |  |
| 27 | `quotation_updated_date` | timestamp(3) | YES |  |
| 28 | `quotation_notification_date` | timestamp(3) | YES |  |
| 29 | `channel_id` | bigint | YES |  |
| 30 | `channel_value` | varchar | YES |  |
| 31 | `medium_id` | bigint | YES |  |
| 32 | `medium_value` | varchar | YES |  |
| 33 | `min_cold_temp_range` | varchar | YES |  |
| 34 | `max_cold_temp_range` | varchar | YES |  |
| 35 | `min_warm_temp_range` | varchar | YES |  |
| 36 | `max_warm_temp_range` | varchar | YES |  |
| 37 | `hot_temp_range` | varchar | YES |  |
| 38 | `temperature` | varchar | YES |  |
| 39 | `company_id` | varchar | YES |  |
| 40 | `brand_id` | varchar | YES |  |
| 41 | `quotation_separation_date` | varchar | YES |  |
| 42 | `load_date` | varchar | YES |  |

### nebula.vw_traking

**Columnas:** 32

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `financing_entry_id` | varchar | YES |  |
| 3 | `case_number` | varchar | YES |  |
| 4 | `days_since_creation` | varchar | YES |  |
| 5 | `step_id` | varchar | YES |  |
| 6 | `step_name` | varchar | YES |  |
| 7 | `approved_amount` | varchar | YES |  |
| 8 | `approved_rate` | varchar | YES |  |
| 9 | `approved_terms_months` | varchar | YES |  |
| 10 | `rejection_cause` | varchar | YES |  |
| 11 | `adviser_id` | varchar | YES |  |
| 12 | `adviser_name` | varchar | YES |  |
| 13 | `adviser_email` | varchar | YES |  |
| 14 | `date_time_response` | varchar | YES |  |
| 15 | `financing_entity_id` | varchar | YES |  |
| 16 | `financing_entity_name` | varchar | YES |  |
| 17 | `response_time` | varchar | YES |  |
| 18 | `finished_at` | varchar | YES |  |
| 19 | `created_at` | varchar | YES |  |
| 20 | `company_group_id` | varchar | YES |  |
| 21 | `company_group_agile_id` | varchar | YES |  |
| 22 | `company_group_name` | varchar | YES |  |
| 23 | `company_id` | varchar | YES |  |
| 24 | `company_agile_id` | varchar | YES |  |
| 25 | `company_name` | varchar | YES |  |
| 26 | `headquarter_id` | varchar | YES |  |
| 27 | `headquarter_agile_id` | varchar | YES |  |
| 28 | `headquarter_name` | varchar | YES |  |
| 29 | `company_group_spiga_id` | varchar | YES |  |
| 30 | `company_spiga_id` | varchar | YES |  |
| 31 | `headquarter_spiga_id` | varchar | YES |  |
| 32 | `load_date` | varchar | YES |  |

### nebula.vw_traking_unique

**Columnas:** 20

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `financing_entry_id` | bigint | YES |  |
| 3 | `case_number` | varchar | YES |  |
| 4 | `days_since_creation` | bigint | YES |  |
| 5 | `step_id` | bigint | YES |  |
| 6 | `step_name` | varchar | YES |  |
| 7 | `approved_amount` | double | YES |  |
| 8 | `approved_rate` | double | YES |  |
| 9 | `approved_terms_months` | bigint | YES |  |
| 10 | `rejection_cause` | varchar | YES |  |
| 11 | `adviser_id` | bigint | YES |  |
| 12 | `adviser_name` | varchar | YES |  |
| 13 | `adviser_email` | varchar | YES |  |
| 14 | `date_time_response` | timestamp(3) | YES |  |
| 15 | `financing_entity_id` | bigint | YES |  |
| 16 | `financing_entity_name` | varchar | YES |  |
| 17 | `response_time` | bigint | YES |  |
| 18 | `finished_at` | varchar | YES |  |
| 19 | `created_at` | timestamp(3) | YES |  |
| 20 | `load_date` | varchar | YES |  |

## 🥈 nebula_otros

`Capa: Plata / Materialized`

### nebula_otros.asesores_recompra

**Columnas:** 7

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `no. ` | integer | YES |  |
| 2 | `l�nea` | varchar | YES |  |
| 3 | `cedula` | integer | YES |  |
| 4 | `nombre ` | varchar | YES |  |
| 5 | `ciudad` | varchar | YES |  |
| 6 | `correo` | varchar | YES |  |
| 7 | `celular` | varchar | YES |  |

### nebula_otros.autos

**Columnas:** 42

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id_vehiculo` | bigint | YES |  |
| 2 | `a�o_matricula` | varchar | YES |  |
| 3 | `mes_matricula` | varchar | YES |  |
| 4 | `dia_matricula` | varchar | YES |  |
| 5 | `clase` | varchar | YES |  |
| 6 | `carroceria` | varchar | YES |  |
| 7 | `marca` | varchar | YES |  |
| 8 | `linea` | varchar | YES |  |
| 9 | `modelo` | varchar | YES |  |
| 10 | `servicio` | varchar | YES |  |
| 11 | `pais_origen` | varchar | YES |  |
| 12 | `color` | varchar | YES |  |
| 13 | `segmento` | varchar | YES |  |
| 14 | `cilindraje` | varchar | YES |  |
| 15 | `numero_ejes` | varchar | YES |  |
| 16 | `numero_puertas` | varchar | YES |  |
| 17 | `pasajeros_sentados` | varchar | YES |  |
| 18 | `capacidad_carga` | varchar | YES |  |
| 19 | `peso` | varchar | YES |  |
| 20 | `departamento` | varchar | YES |  |
| 21 | `municipio` | varchar | YES |  |
| 22 | `combustible` | varchar | YES |  |
| 23 | `tipo_matricula` | varchar | YES |  |
| 24 | `prenda` | varchar | YES |  |
| 25 | `nombre_entidad_prenda` | varchar | YES |  |
| 26 | `ciudad_propietario` | varchar | YES |  |
| 27 | `modalidad` | varchar | YES |  |
| 28 | `aire_acondicionado` | varchar | YES |  |
| 29 | `airbag` | varchar | YES |  |
| 30 | `tipo_transmision` | varchar | YES |  |
| 31 | `nivel_emisiones` | varchar | YES |  |
| 32 | `tipo_aspiracion` | varchar | YES |  |
| 33 | `apoya_cabeza` | varchar | YES |  |
| 34 | `tipo_freno` | varchar | YES |  |
| 35 | `tipo_traccion` | varchar | YES |  |
| 36 | `leasing` | varchar | YES |  |
| 37 | `nombre_entidad_leasing` | varchar | YES |  |
| 38 | `nit_leasing` | varchar | YES |  |
| 39 | `acreedor` | varchar | YES |  |
| 40 | `nombre_aseguradora` | varchar | YES |  |
| 41 | `claraboya_sunroof` | varchar | YES |  |
| 42 | `identificador_combustible` | varchar | YES |  |

### nebula_otros.autos_peru

**Columnas:** 24

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `fecha_alta` | varchar | YES |  |
| 2 | `departamento` | varchar | YES |  |
| 3 | `oficina_registral` | varchar | YES |  |
| 4 | `clase_vehicular` | varchar | YES |  |
| 5 | `categoria_aap` | varchar | YES |  |
| 6 | `carroceria` | varchar | YES |  |
| 7 | `marca` | varchar | YES |  |
| 8 | `modelo` | varchar | YES |  |
| 9 | `version` | varchar | YES |  |
| 10 | `pbv` | varchar | YES |  |
| 11 | `asientos` | varchar | YES |  |
| 12 | `combustible` | varchar | YES |  |
| 13 | `categoria` | varchar | YES |  |
| 14 | `uso_vehiculo` | varchar | YES |  |
| 15 | `tipo_doc_prop` | varchar | YES |  |
| 16 | `formula_rodante` | varchar | YES |  |
| 17 | `transmision` | varchar | YES |  |
| 18 | `cilindrada` | varchar | YES |  |
| 19 | `potencia_motor` | varchar | YES |  |
| 20 | `color` | varchar | YES |  |
| 21 | `anio_mod` | varchar | YES |  |
| 22 | `pais_origen` | varchar | YES |  |
| 23 | `tramite_origen` | varchar | YES |  |
| 24 | `cantidad` | varchar | YES |  |

### nebula_otros.centros_mayoristas

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `name` | varchar | YES |  |
| 2 | `brand` | varchar | YES |  |
| 3 | `center_name` | varchar | YES |  |
| 4 | `center_code` | varchar | YES |  |
| 5 | `country` | varchar | YES |  |
| 6 | `company_id` | varchar | YES |  |
| 7 | `code` | varchar | YES |  |
| 8 | `status` | varchar | YES |  |

### nebula_otros.ci_spiga_homologacion_general

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codigomodelo` | varchar | YES |  |
| 2 | `anio_modelo` | varchar | YES |  |
| 3 | `marca` | varchar | YES |  |
| 4 | `clasificacion` | varchar | YES |  |
| 5 | `gama` | varchar | YES |  |
| 6 | `modelo` | varchar | YES |  |
| 7 | `extmodelo` | varchar | YES |  |
| 8 | `cilindraje` | decimal(8,2) | YES |  |
| 9 | `combustible` | varchar | YES |  |
| 10 | `traccion` | varchar | YES |  |
| 11 | `confiabilidad` | integer | YES |  |
| 12 | `intentos_fallidos` | integer | YES |  |
| 13 | `ultimo_intento` | date | YES |  |
| 14 | `disponible_desde` | date | YES |  |
| 15 | `codigo_fasecolda` | varchar | YES |  |

### nebula_otros.ci_spiga_homologacion_usados

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codigo_modelo` | varchar | YES |  |
| 2 | `anio_modelo` | varchar | YES |  |
| 3 | `marca` | varchar | YES |  |
| 4 | `gama` | varchar | YES |  |
| 5 | `modelo_version` | varchar | YES |  |
| 6 | `cilindraje` | decimal(8,2) | YES |  |
| 7 | `clasificacion` | varchar | YES |  |
| 8 | `codigo_fasecolda` | varchar | YES |  |
| 9 | `confiabilidad` | integer | YES |  |
| 10 | `intentos_fallidos` | integer | YES |  |
| 11 | `ultimo_intento` | date | YES |  |
| 12 | `disponible_desde` | date | YES |  |

### nebula_otros.ciudad_centro

**Columnas:** 3

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codigocentro` | integer | YES |  |
| 2 | `centro` | varchar | YES |  |
| 3 | `ciudad` | varchar | YES |  |

### nebula_otros.output_recompra

**Columnas:** 19

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `nit` | varchar | YES |  |
| 2 | `tipo_persona` | varchar | YES |  |
| 3 | `es_juridico` | integer | YES |  |
| 4 | `num_compras` | integer | YES |  |
| 5 | `segmento` | varchar | YES |  |
| 6 | `dias_predichos` | integer | YES |  |
| 7 | `fecha_estimada` | date | YES |  |
| 8 | `dias_hasta_estimada` | integer | YES |  |
| 9 | `urgencia` | varchar | YES |  |
| 10 | `ultima_fecha` | date | YES |  |
| 11 | `ultimo_vin` | varchar | YES |  |
| 12 | `ultima_gama` | varchar | YES |  |
| 13 | `ultima_marca` | varchar | YES |  |
| 14 | `ultimo_valor` | double | YES |  |
| 15 | `valida_marca` | varchar | YES |  |
| 16 | `recomendacion_transicion_v1` | varchar | YES |  |
| 17 | `recomendacion_similitud_v1` | varchar | YES |  |
| 18 | `recomendacion_transicion_v2` | varchar | YES |  |
| 19 | `recomendacion_similitud_v2` | varchar | YES |  |

### nebula_otros.runt

**Columnas:** 57

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `consecutivo` | integer | YES |  |
| 2 | `anio_mi` | integer | YES |  |
| 3 | `mes_mi` | integer | YES |  |
| 4 | `clase` | varchar | YES |  |
| 5 | `carroceria` | varchar | YES |  |
| 6 | `marca` | varchar | YES |  |
| 7 | `categoria` | varchar(13) | YES |  |
| 8 | `linea` | varchar | YES |  |
| 9 | `linea_consolidada` | varchar | YES |  |
| 10 | `modelo` | integer | YES |  |
| 11 | `servicio` | varchar | YES |  |
| 12 | `nacional_importado` | varchar | YES |  |
| 13 | `color` | varchar | YES |  |
| 14 | `segmento` | varchar | YES |  |
| 15 | `sub_segmentos` | varchar | YES |  |
| 16 | `cilindraje` | integer | YES |  |
| 17 | `cantidad_ejes` | integer | YES |  |
| 18 | `puertas` | integer | YES |  |
| 19 | `pasajeros_sentados` | integer | YES |  |
| 20 | `capacidad_carga` | integer | YES |  |
| 21 | `peso` | integer | YES |  |
| 22 | `departamento` | varchar | YES |  |
| 23 | `region` | varchar | YES |  |
| 24 | `municipio_ciudad` | varchar | YES |  |
| 25 | `combustible` | varchar | YES |  |
| 26 | `combust_nev` | varchar | YES |  |
| 27 | `combust_nev_categoria` | varchar(15) | YES |  |
| 28 | `tipo_matricula` | varchar | YES |  |
| 29 | `prenda_si_no` | varchar | YES |  |
| 30 | `nombre_entidad_prenda` | varchar | YES |  |
| 31 | `ciudad_residencia_propietario` | varchar | YES |  |
| 32 | `modalidad_transporte` | varchar | YES |  |
| 33 | `a_c` | varchar | YES |  |
| 34 | `airbags` | integer | YES |  |
| 35 | `transmision` | varchar | YES |  |
| 36 | `nivel_emisiones` | varchar | YES |  |
| 37 | `tipo_aspiracion` | varchar | YES |  |
| 38 | `apoyacabezas` | varchar | YES |  |
| 39 | `tipo_freno` | varchar | YES |  |
| 40 | `tipo_traccion` | varchar | YES |  |
| 41 | `leasing` | varchar | YES |  |
| 42 | `nombre_entidad_leasing` | varchar | YES |  |
| 43 | `nit_leasing` | varchar | YES |  |
| 44 | `acreedor` | varchar | YES |  |
| 45 | `nombre_aseguradora` | varchar | YES |  |
| 46 | `fecha` | date | YES |  |
| 47 | `origen` | varchar | YES |  |
| 48 | `iso_ue` | varchar | YES |  |
| 49 | `byd_rel` | varchar | YES |  |
| 50 | `cantidad` | integer | YES |  |
| 51 | `concatenado` | varchar | YES |  |
| 52 | `segmento_x` | varchar | YES |  |
| 53 | `segmento_e` | varchar | YES |  |
| 54 | `body_style` | varchar | YES |  |
| 55 | `representante_importador_vc` | varchar | YES |  |
| 56 | `seg_tamanio` | varchar | YES |  |
| 57 | `crucetamanio` | varchar | YES |  |

### nebula_otros.runt_ajustada

**Columnas:** 57

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `consecutivo` | integer | YES |  |
| 2 | `anio_mi` | integer | YES |  |
| 3 | `mes_mi` | integer | YES |  |
| 4 | `clase` | varchar | YES |  |
| 5 | `carroceria` | varchar | YES |  |
| 6 | `marca` | varchar | YES |  |
| 7 | `categoria` | varchar(13) | YES |  |
| 8 | `linea` | varchar | YES |  |
| 9 | `linea_consolidada` | varchar | YES |  |
| 10 | `modelo` | integer | YES |  |
| 11 | `servicio` | varchar | YES |  |
| 12 | `nacional_importado` | varchar | YES |  |
| 13 | `color` | varchar | YES |  |
| 14 | `segmento` | varchar | YES |  |
| 15 | `sub_segmentos` | varchar | YES |  |
| 16 | `cilindraje` | integer | YES |  |
| 17 | `cantidad_ejes` | integer | YES |  |
| 18 | `puertas` | integer | YES |  |
| 19 | `pasajeros_sentados` | integer | YES |  |
| 20 | `capacidad_carga` | integer | YES |  |
| 21 | `peso` | integer | YES |  |
| 22 | `departamento` | varchar | YES |  |
| 23 | `region` | varchar | YES |  |
| 24 | `municipio_ciudad` | varchar | YES |  |
| 25 | `combustible` | varchar | YES |  |
| 26 | `combust_nev` | varchar | YES |  |
| 27 | `combust_nev_categoria` | varchar(15) | YES |  |
| 28 | `tipo_matricula` | varchar | YES |  |
| 29 | `prenda_si_no` | varchar | YES |  |
| 30 | `nombre_entidad_prenda` | varchar | YES |  |
| 31 | `ciudad_residencia_propietario` | varchar | YES |  |
| 32 | `modalidad_transporte` | varchar | YES |  |
| 33 | `a_c` | varchar | YES |  |
| 34 | `airbags` | integer | YES |  |
| 35 | `transmision` | varchar | YES |  |
| 36 | `nivel_emisiones` | varchar | YES |  |
| 37 | `tipo_aspiracion` | varchar | YES |  |
| 38 | `apoyacabezas` | varchar | YES |  |
| 39 | `tipo_freno` | varchar | YES |  |
| 40 | `tipo_traccion` | varchar | YES |  |
| 41 | `leasing` | varchar | YES |  |
| 42 | `nombre_entidad_leasing` | varchar | YES |  |
| 43 | `nit_leasing` | varchar | YES |  |
| 44 | `acreedor` | varchar | YES |  |
| 45 | `nombre_aseguradora` | varchar | YES |  |
| 46 | `fecha` | date | YES |  |
| 47 | `origen` | varchar | YES |  |
| 48 | `iso_ue` | varchar | YES |  |
| 49 | `byd_rel` | varchar | YES |  |
| 50 | `cantidad` | integer | YES |  |
| 51 | `concatenado` | varchar | YES |  |
| 52 | `segmento_x` | varchar | YES |  |
| 53 | `segmento_e` | varchar | YES |  |
| 54 | `body_style` | varchar | YES |  |
| 55 | `representante_importador_vc` | varchar | YES |  |
| 56 | `seg_tamanio` | varchar | YES |  |
| 57 | `crucetamanio` | varchar | YES |  |

### nebula_otros.runt_final

**Columnas:** 67

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `consecutivo` | integer | YES |  |
| 2 | `anio_mi` | integer | YES |  |
| 3 | `mes_mi` | integer | YES |  |
| 4 | `clase` | varchar | YES |  |
| 5 | `carroceria` | varchar | YES |  |
| 6 | `marca` | varchar | YES |  |
| 7 | `marca_otras` | varchar | YES |  |
| 8 | `linea` | varchar | YES |  |
| 9 | `linea_consolidada` | varchar | YES |  |
| 10 | `modelo` | integer | YES |  |
| 11 | `servicio` | varchar | YES |  |
| 12 | `nacional_importado` | varchar | YES |  |
| 13 | `color` | varchar | YES |  |
| 14 | `segmento` | varchar | YES |  |
| 15 | `sub_segmentos` | varchar | YES |  |
| 16 | `cilindraje` | varchar | YES |  |
| 17 | `cantidad_ejes` | varchar | YES |  |
| 18 | `puertas` | varchar | YES |  |
| 19 | `pasajeros_sentados` | varchar | YES |  |
| 20 | `capacidad_carga` | varchar | YES |  |
| 21 | `peso` | varchar | YES |  |
| 22 | `departamento` | varchar | YES |  |
| 23 | `region` | varchar | YES |  |
| 24 | `municipio_ciudad` | varchar | YES |  |
| 25 | `combustible` | varchar | YES |  |
| 26 | `combust_nev` | varchar | YES |  |
| 27 | `tipo_matricula` | varchar | YES |  |
| 28 | `prenda_si_no` | varchar | YES |  |
| 29 | `nombre_entidad_prenda` | varchar | YES |  |
| 30 | `ciudad_residencia_propietario` | varchar | YES |  |
| 31 | `modalidad_transporte` | varchar | YES |  |
| 32 | `a_c` | varchar | YES |  |
| 33 | `airbags` | varchar | YES |  |
| 34 | `transmision` | varchar | YES |  |
| 35 | `nivel_emisiones` | varchar | YES |  |
| 36 | `tipo_aspiracion` | varchar | YES |  |
| 37 | `apoyacabezas` | varchar | YES |  |
| 38 | `tipo_freno` | varchar | YES |  |
| 39 | `tipo_traccion` | varchar | YES |  |
| 40 | `leasing` | varchar | YES |  |
| 41 | `nombre_entidad_leasing` | varchar | YES |  |
| 42 | `nit_leasing` | varchar | YES |  |
| 43 | `acreedor` | varchar | YES |  |
| 44 | `nombre_aseguradora` | varchar | YES |  |
| 45 | `claraboya_sunroof` | varchar | YES |  |
| 46 | `identificador_combustible` | varchar | YES |  |
| 47 | `fecha` | date | YES |  |
| 48 | `origen` | varchar | YES |  |
| 49 | `iso_ue` | varchar | YES |  |
| 50 | `byd_rel` | varchar | YES |  |
| 51 | `cantidad` | varchar | YES |  |
| 52 | `concatenado` | varchar | YES |  |
| 53 | `concatenado2` | varchar | YES |  |
| 54 | `segmento_x` | varchar | YES |  |
| 55 | `segmento_e` | varchar | YES |  |
| 56 | `body_style` | varchar | YES |  |
| 57 | `representante_importador_vc` | varchar | YES |  |
| 58 | `representante_importador_nev` | varchar | YES |  |
| 59 | `seg_tamanio` | varchar | YES |  |
| 60 | `crucetamanio` | varchar | YES |  |
| 61 | `llavepais` | varchar | YES |  |
| 62 | `llave_mt` | varchar | YES |  |
| 63 | `minitrucks` | varchar | YES |  |
| 64 | `sub_segmento_vhc` | varchar | YES |  |
| 65 | `segmento_vhc` | varchar | YES |  |
| 66 | `sub_sub_segmento_vhc` | varchar | YES |  |
| 67 | `filtro_carroceria` | varchar | YES |  |

### nebula_otros.vehiculos_fasecolda

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codigo_homologacion` | varchar | YES |  |
| 2 | `clase` | varchar | YES |  |
| 3 | `carroceria` | varchar | YES |  |
| 4 | `marca` | varchar | YES |  |
| 5 | `linea` | varchar | YES |  |
| 6 | `linea_consolidada` | varchar | YES |  |
| 7 | `modelo` | varchar | YES |  |
| 8 | `cilindraje` | varchar | YES |  |
| 9 | `combustible` | varchar | YES |  |
| 10 | `airbags` | varchar | YES |  |
| 11 | `transmision` | varchar | YES |  |
| 12 | `tipo_traccion` | varchar | YES |  |
| 13 | `version` | varchar | YES |  |
| 14 | `especificaciones` | varchar | YES |  |
| 15 | `traccion_tipo` | varchar | YES |  |

### nebula_otros.vista_asignacion_final_recompra

**Columnas:** 13

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `nombre_completo` | varchar | YES |  |
| 2 | `correo` | varchar | YES |  |
| 3 | `telefono` | varchar | YES |  |
| 4 | `documento` | varchar | YES |  |
| 5 | `centro` | varchar | YES |  |
| 6 | `anio_modelo_ultima_compra` | varchar | YES |  |
| 7 | `ultimo_vin` | varchar | YES |  |
| 8 | `marca_recomendada` | varchar | YES |  |
| 9 | `modelo_recomendado` | varchar | YES |  |
| 10 | `fecha_estimada` | date | YES |  |
| 11 | `fila_marca` | bigint | YES |  |
| 12 | `registros` | bigint | YES |  |
| 13 | `valida_asignacion` | integer | YES |  |

### nebula_otros.vista_conteo_registros_asesores

**Columnas:** 3

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `linea` | varchar | YES |  |
| 2 | `asesores` | bigint | YES |  |
| 3 | `registros` | bigint | YES |  |

### nebula_otros.vista_final_recompra

**Columnas:** 11

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `nombre_completo` | varchar | YES |  |
| 2 | `correo` | varchar | YES |  |
| 3 | `telefono` | varchar | YES |  |
| 4 | `documento` | varchar | YES |  |
| 5 | `centro` | varchar | YES |  |
| 6 | `anio_modelo_ultima_compra` | varchar | YES |  |
| 7 | `ultimo_vin` | varchar | YES |  |
| 8 | `marca_recomendada` | varchar | YES |  |
| 9 | `modelo_recomendado` | varchar | YES |  |
| 10 | `fecha_estimada` | date | YES |  |
| 11 | `fila_marca` | bigint | YES |  |

## 🥉 orbi_atenea

`Capa: Bronce / Raw`

### orbi_atenea.vw_atenea_contactabilidad

**Columnas:** 19

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id_mes` | integer | YES |  |
| 2 | `a�o` | integer | YES |  |
| 3 | `linea` | varchar | YES |  |
| 4 | `idlinea` | decimal(20,0) | YES |  |
| 5 | `sede` | varchar | YES |  |
| 6 | `idsede` | decimal(20,0) | YES |  |
| 7 | `idcompa�ia` | varchar | YES |  |
| 8 | `compa�ia` | varchar | YES |  |
| 9 | `area` | varchar | YES |  |
| 10 | `idarea` | decimal(20,0) | YES |  |
| 11 | `mes` | varchar | YES |  |
| 12 | `contactabilidad` | varchar | YES |  |
| 13 | `idcontactabilidad` | integer | YES |  |
| 14 | `total` | decimal(23,0) | YES |  |
| 15 | `basescargadas` | bigint | YES |  |
| 16 | `porcentaje` | varchar | YES |  |
| 17 | `case_created_at` | timestamp(3) | YES |  |
| 18 | `fecha_actualizacion` | timestamp(3) | YES |  |
| 19 | `origen_db` | varchar | YES |  |

### orbi_atenea.vw_atenea_contactabilidad_detalle

**Columnas:** 22

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id_mes` | integer | YES |  |
| 2 | `a�o` | integer | YES |  |
| 3 | `linea` | varchar | YES |  |
| 4 | `idlinea` | decimal(20,0) | YES |  |
| 5 | `sede` | varchar | YES |  |
| 6 | `idsede` | decimal(20,0) | YES |  |
| 7 | `idcompa�ia` | varchar | YES |  |
| 8 | `compa�ia` | varchar | YES |  |
| 9 | `area` | varchar | YES |  |
| 10 | `idarea` | decimal(20,0) | YES |  |
| 11 | `mes` | varchar | YES |  |
| 12 | `contactabilidad` | varchar | YES |  |
| 13 | `idcontactabilidad` | integer | YES |  |
| 14 | `nombrecliente` | varchar | YES |  |
| 15 | `placa` | varchar | YES |  |
| 16 | `vin` | varchar | YES |  |
| 17 | `cedulacliente` | varchar | YES |  |
| 18 | `telefonocontacto` | varchar | YES |  |
| 19 | `nombreasesor` | varchar | YES |  |
| 20 | `nombreasesorspiga` | varchar | YES |  |
| 21 | `fecha_actualizacion` | timestamp(3) | YES |  |
| 22 | `origen_db` | varchar | YES |  |

### orbi_atenea.vw_atenea_nps

**Columnas:** 22

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id_mes` | integer | YES |  |
| 2 | `a�o` | integer | YES |  |
| 3 | `mes` | varchar | YES |  |
| 4 | `sede` | varchar | YES |  |
| 5 | `idsede` | decimal(20,0) | YES |  |
| 6 | `linea` | varchar | YES |  |
| 7 | `idlinea` | decimal(20,0) | YES |  |
| 8 | `id_compa�ia` | bigint | YES |  |
| 9 | `area` | varchar | YES |  |
| 10 | `idarea` | decimal(20,0) | YES |  |
| 11 | `promotores` | decimal(23,0) | YES |  |
| 12 | `neutros` | decimal(23,0) | YES |  |
| 13 | `detractores` | decimal(23,0) | YES |  |
| 14 | `total` | decimal(23,0) | YES |  |
| 15 | `porcentajepromotor` | varchar | YES |  |
| 16 | `porcentajeneutros` | varchar | YES |  |
| 17 | `porcentajedetractores` | varchar | YES |  |
| 18 | `npstotal` | varchar | YES |  |
| 19 | `meta` | varchar | YES |  |
| 20 | `compa�ia` | varchar | YES |  |
| 21 | `fecha_actualizacion` | timestamp(3) | YES |  |
| 22 | `origen_db` | varchar | YES |  |

### orbi_atenea.vw_atenea_nps_detalle

**Columnas:** 44

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idmes` | integer | YES |  |
| 2 | `a�o` | integer | YES |  |
| 3 | `mes` | varchar | YES |  |
| 4 | `nombrecliente` | varchar | YES |  |
| 5 | `cedulacliente` | varchar | YES |  |
| 6 | `numerocelular` | varchar | YES |  |
| 7 | `telefono` | varchar | YES |  |
| 8 | `telefono2` | varchar | YES |  |
| 9 | `ciudad` | varchar | YES |  |
| 10 | `email` | varchar | YES |  |
| 11 | `sede` | varchar | YES |  |
| 12 | `idsede` | decimal(20,0) | YES |  |
| 13 | `linea` | varchar | YES |  |
| 14 | `idlinea` | decimal(20,0) | YES |  |
| 15 | `compa�ia` | varchar | YES |  |
| 16 | `idcompa�ia` | varchar | YES |  |
| 17 | `marca` | varchar | YES |  |
| 18 | `area` | varchar | YES |  |
| 19 | `idarea` | decimal(20,0) | YES |  |
| 20 | `placa` | varchar | YES |  |
| 21 | `descripciontrabajo` | varchar | YES |  |
| 22 | `nombreasesorspiga` | varchar | YES |  |
| 23 | `asesor` | varchar | YES |  |
| 24 | `fechagestion` | timestamp(3) | YES |  |
| 25 | `resultadogestion` | varchar | YES |  |
| 26 | `canal` | varchar | YES |  |
| 27 | `idcanal` | varchar | YES |  |
| 28 | `usuario` | varchar | YES |  |
| 29 | `nombreusuario` | varchar | YES |  |
| 30 | `numerocontactado` | varchar | YES |  |
| 31 | `pregunta` | varchar | YES |  |
| 32 | `respuesta` | varchar | YES |  |
| 33 | `codigocaso` | varchar | YES |  |
| 34 | `tipocaso` | varchar | YES |  |
| 35 | `clasificacioncaso` | varchar | YES |  |
| 36 | `subclasificacioncaso` | varchar | YES |  |
| 37 | `detalle` | varchar | YES |  |
| 38 | `descripci�n` | varchar | YES |  |
| 39 | `fechacreacioncaso` | timestamp(3) | YES |  |
| 40 | `fechavencimientocaso` | varchar | YES |  |
| 41 | `fechacierrecaso` | timestamp(3) | YES |  |
| 42 | `responsablecaso` | varchar | YES |  |
| 43 | `fecha_actualizacion` | timestamp(3) | YES |  |
| 44 | `origen_db` | varchar | YES |  |

### orbi_atenea.vw_atenea_ordenes_asesores_total

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `advisername` | varchar | YES |  |
| 2 | `totalasesor` | bigint | YES |  |
| 3 | `id_mes` | integer | YES |  |
| 4 | `mes` | varchar | YES |  |
| 5 | `anio` | integer | YES |  |
| 6 | `idcompa�ia` | varchar | YES |  |
| 7 | `compania` | varchar | YES |  |
| 8 | `linea` | varchar | YES |  |
| 9 | `idlinea` | decimal(20,0) | YES |  |
| 10 | `sede` | varchar | YES |  |
| 11 | `idsede` | varchar | YES |  |
| 12 | `area` | varchar | YES |  |
| 13 | `idarea` | decimal(20,0) | YES |  |
| 14 | `fecha_actualizacion` | timestamp(3) | YES |  |
| 15 | `origen_db` | varchar | YES |  |

### orbi_atenea.vw_atenea_pqr

**Columnas:** 39

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `id_mes` | integer | YES |  |
| 3 | `a�o` | integer | YES |  |
| 4 | `mes` | varchar | YES |  |
| 5 | `idcompa�ia` | varchar | YES |  |
| 6 | `empresa` | varchar | YES |  |
| 7 | `idlinea` | bigint | YES |  |
| 8 | `linea` | varchar | YES |  |
| 9 | `idsede` | bigint | YES |  |
| 10 | `sede` | varchar | YES |  |
| 11 | `proceso` | varchar | YES |  |
| 12 | `identificationnumber` | varchar | YES |  |
| 13 | `nombrecliente` | varchar | YES |  |
| 14 | `placa` | varchar | YES |  |
| 15 | `gamma` | varchar | YES |  |
| 16 | `modelo` | varchar | YES |  |
| 17 | `kilometraje` | varchar | YES |  |
| 18 | `vin` | varchar | YES |  |
| 19 | `marcavehiculo` | varchar | YES |  |
| 20 | `numeromotor` | varchar | YES |  |
| 21 | `telefonocontacto` | varchar | YES |  |
| 22 | `idticket` | bigint | YES |  |
| 23 | `c�digocaso` | varchar | YES |  |
| 24 | `tipocaso` | varchar | YES |  |
| 25 | `clasificacioncaso` | varchar | YES |  |
| 26 | `subclasificacioncaso` | varchar | YES |  |
| 27 | `detalle` | varchar | YES |  |
| 28 | `descripci�n` | varchar | YES |  |
| 29 | `fecharegistro` | timestamp(3) | YES |  |
| 30 | `fecharespuesta` | timestamp(3) | YES |  |
| 31 | `cantidaddiascierre` | integer | YES |  |
| 32 | `cantidaddiastranscurridos` | integer | YES |  |
| 33 | `estado` | varchar | YES |  |
| 34 | `origen` | varchar | YES |  |
| 35 | `subclasificaci�n` | varchar | YES |  |
| 36 | `nombreasesor` | varchar | YES |  |
| 37 | `nombreasesorspiga` | varchar | YES |  |
| 38 | `fecha_actualizacion` | timestamp(3) | YES |  |
| 39 | `origen_db` | varchar | YES |  |

### orbi_atenea.vw_atenea_preguntas_detalle

**Columnas:** 44

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idmes` | integer | YES |  |
| 2 | `a�o` | integer | YES |  |
| 3 | `mes` | varchar | YES |  |
| 4 | `nombrecliente` | varchar | YES |  |
| 5 | `cedulacliente` | varchar | YES |  |
| 6 | `numerocelular` | varchar | YES |  |
| 7 | `telefono` | varchar | YES |  |
| 8 | `telefono2` | varchar | YES |  |
| 9 | `ciudad` | varchar | YES |  |
| 10 | `email` | varchar | YES |  |
| 11 | `sede` | varchar | YES |  |
| 12 | `idsede` | decimal(20,0) | YES |  |
| 13 | `linea` | varchar | YES |  |
| 14 | `idlinea` | decimal(20,0) | YES |  |
| 15 | `idcompa�ia` | varchar | YES |  |
| 16 | `compa�ia` | varchar | YES |  |
| 17 | `marca` | varchar | YES |  |
| 18 | `area` | varchar | YES |  |
| 19 | `idarea` | decimal(20,0) | YES |  |
| 20 | `placa` | varchar | YES |  |
| 21 | `descripciontrabajo` | varchar | YES |  |
| 22 | `nombreasesorspiga` | varchar | YES |  |
| 23 | `asesor` | varchar | YES |  |
| 24 | `fechagestion` | timestamp(3) | YES |  |
| 25 | `resultadogestion` | varchar | YES |  |
| 26 | `canal` | varchar | YES |  |
| 27 | `idcanal` | varchar | YES |  |
| 28 | `usuario` | varchar | YES |  |
| 29 | `nombreusuario` | varchar | YES |  |
| 30 | `numerocontactado` | varchar | YES |  |
| 31 | `pregunta` | varchar | YES |  |
| 32 | `respuesta` | varchar | YES |  |
| 33 | `codigocaso` | varchar | YES |  |
| 34 | `tipocaso` | varchar | YES |  |
| 35 | `clasificacioncaso` | varchar | YES |  |
| 36 | `subclasificacioncaso` | varchar | YES |  |
| 37 | `detalle` | varchar | YES |  |
| 38 | `descripci�n` | varchar | YES |  |
| 39 | `fechacreacioncaso` | timestamp(3) | YES |  |
| 40 | `fechavencimientocaso` | varchar | YES |  |
| 41 | `fechacierrecaso` | timestamp(3) | YES |  |
| 42 | `responsablecaso` | varchar | YES |  |
| 43 | `fecha_actualizacion` | timestamp(3) | YES |  |
| 44 | `origen_db` | varchar | YES |  |

### orbi_atenea.vw_atenea_satisfaccion

**Columnas:** 26

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id_mes` | integer | YES |  |
| 2 | `a�o` | integer | YES |  |
| 3 | `mes` | varchar | YES |  |
| 4 | `sede` | varchar | YES |  |
| 5 | `idsede` | decimal(20,0) | YES |  |
| 6 | `linea` | varchar | YES |  |
| 7 | `idlinea` | decimal(20,0) | YES |  |
| 8 | `area` | varchar | YES |  |
| 9 | `idarea` | decimal(20,0) | YES |  |
| 10 | `encuestasefectivas` | bigint | YES |  |
| 11 | `res_1` | decimal(23,0) | YES |  |
| 12 | `res_2` | decimal(23,0) | YES |  |
| 13 | `res_3` | decimal(23,0) | YES |  |
| 14 | `res_4` | decimal(23,0) | YES |  |
| 15 | `res_5` | decimal(23,0) | YES |  |
| 16 | `res_6` | decimal(23,0) | YES |  |
| 17 | `res_7` | decimal(23,0) | YES |  |
| 18 | `res_8` | decimal(23,0) | YES |  |
| 19 | `res_9` | decimal(23,0) | YES |  |
| 20 | `res_10` | decimal(23,0) | YES |  |
| 21 | `satisfaccion` | varchar | YES |  |
| 22 | `meta` | varchar | YES |  |
| 23 | `idcompa�ia` | varchar | YES |  |
| 24 | `compa�ia` | varchar | YES |  |
| 25 | `fecha_actualizacion` | timestamp(3) | YES |  |
| 26 | `origen_db` | varchar | YES |  |

### orbi_atenea.vw_atenea_satisfaccion_detalle

**Columnas:** 44

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idmes` | integer | YES |  |
| 2 | `a�o` | integer | YES |  |
| 3 | `mes` | varchar | YES |  |
| 4 | `nombrecliente` | varchar | YES |  |
| 5 | `cedulacliente` | varchar | YES |  |
| 6 | `numerocelular` | varchar | YES |  |
| 7 | `telefono` | varchar | YES |  |
| 8 | `telefono2` | varchar | YES |  |
| 9 | `ciudad` | varchar | YES |  |
| 10 | `email` | varchar | YES |  |
| 11 | `sede` | varchar | YES |  |
| 12 | `idsede` | decimal(20,0) | YES |  |
| 13 | `linea` | varchar | YES |  |
| 14 | `idlinea` | decimal(20,0) | YES |  |
| 15 | `idcompa�ia` | varchar | YES |  |
| 16 | `compa�ia` | varchar | YES |  |
| 17 | `marca` | varchar | YES |  |
| 18 | `area` | varchar | YES |  |
| 19 | `idarea` | decimal(20,0) | YES |  |
| 20 | `placa` | varchar | YES |  |
| 21 | `descripciontrabajo` | varchar | YES |  |
| 22 | `nombreasesorspiga` | varchar | YES |  |
| 23 | `asesor` | varchar | YES |  |
| 24 | `fechagestion` | timestamp(3) | YES |  |
| 25 | `resultadogestion` | varchar | YES |  |
| 26 | `canal` | varchar | YES |  |
| 27 | `idcanal` | varchar | YES |  |
| 28 | `usuario` | varchar | YES |  |
| 29 | `nombreusuario` | varchar | YES |  |
| 30 | `numerocontactado` | varchar | YES |  |
| 31 | `pregunta` | varchar | YES |  |
| 32 | `respuesta` | varchar | YES |  |
| 33 | `codigocaso` | varchar | YES |  |
| 34 | `tipocaso` | varchar | YES |  |
| 35 | `clasificacioncaso` | varchar | YES |  |
| 36 | `subclasificacioncaso` | varchar | YES |  |
| 37 | `detalle` | varchar | YES |  |
| 38 | `descripci�n` | varchar | YES |  |
| 39 | `fechacreacioncaso` | timestamp(3) | YES |  |
| 40 | `fechavencimientocaso` | varchar | YES |  |
| 41 | `fechacierrecaso` | timestamp(3) | YES |  |
| 42 | `responsablecaso` | varchar | YES |  |
| 43 | `fecha_actualizacion` | timestamp(3) | YES |  |
| 44 | `origen_db` | varchar | YES |  |

## 🥈 pricing

`Capa: Plata / Materialized`

### pricing.pr_carroya_vehiculos

**Columnas:** 32

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `year` | integer | YES |  |
| 3 | `title` | varchar | YES |  |
| 4 | `status` | varchar | YES |  |
| 5 | `sold` | varchar | YES |  |
| 6 | `price` | bigint | YES |  |
| 7 | `brand` | varchar | YES |  |
| 8 | `model` | varchar | YES |  |
| 9 | `detail` | varchar | YES |  |
| 10 | `fenomenoya` | boolean | YES |  |
| 11 | `kilometers` | integer | YES |  |
| 12 | `color` | varchar | YES |  |
| 13 | `city` | varchar | YES |  |
| 14 | `featured` | integer | YES |  |
| 15 | `cylindrical` | integer | YES |  |
| 16 | `ctipocaja` | varchar | YES |  |
| 17 | `ccombustible` | varchar | YES |  |
| 18 | `cplaca` | varchar | YES |  |
| 19 | `cclienteidusuario` | varchar | YES |  |
| 20 | `csellername` | varchar | YES |  |
| 21 | `cselleremail` | varchar | YES |  |
| 22 | `csellerphone` | varchar | YES |  |
| 23 | `csellercity` | varchar | YES |  |
| 24 | `cselleradress` | varchar | YES |  |
| 25 | `cprecioint` | bigint | YES |  |
| 26 | `cfechapublicacion` | timestamp(3) | YES |  |
| 27 | `cfechaactualizacion` | timestamp(3) | YES |  |
| 28 | `curlimagen` | varchar | YES |  |
| 29 | `images` | varchar | YES |  |
| 30 | `accesorios` | varchar | YES |  |
| 31 | `id_hash` | varchar | YES |  |
| 32 | `fecha_scraping` | date | YES |  |

### pricing.pr_datos_asousados

**Columnas:** 17

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `segmento` | varchar | YES |  |
| 2 | `marca` | varchar | YES |  |
| 3 | `tipo` | varchar | YES |  |
| 4 | `catalogo` | varchar | YES |  |
| 5 | `2026` | double | YES |  |
| 6 | `2025` | double | YES |  |
| 7 | `2024` | double | YES |  |
| 8 | `2023` | double | YES |  |
| 9 | `2022` | double | YES |  |
| 10 | `2021` | double | YES |  |
| 11 | `2020` | double | YES |  |
| 12 | `2019` | double | YES |  |
| 13 | `2018` | double | YES |  |
| 14 | `2017` | double | YES |  |
| 15 | `2016` | double | YES |  |
| 16 | `2015` | double | YES |  |
| 17 | `2014` | double | YES |  |

### pricing.pr_datos_usados

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `anio_modelo` | varchar | YES |  |
| 2 | `marca` | varchar | YES |  |
| 3 | `linea` | varchar | YES |  |
| 4 | `sub_linea` | varchar | YES |  |
| 5 | `version` | varchar | YES |  |
| 6 | `extra` | varchar | YES |  |
| 7 | `version_extra` | varchar | YES |  |
| 8 | `kms` | double | YES |  |
| 9 | `placa` | varchar | YES |  |
| 10 | `empresa` | varchar | YES |  |
| 11 | `fecha_publicacion` | timestamp(3) | YES |  |
| 12 | `precio_venta` | decimal(38,4) | YES |  |
| 13 | `fecha_venta` | timestamp(3) | YES |  |
| 14 | `color` | varchar | YES |  |
| 15 | `url` | varchar | YES |  |

### pricing.pr_decremento_valor_vehiculo

**Columnas:** 13

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `nivel` | varchar | YES |  |
| 2 | `y2026` | real | YES |  |
| 3 | `y2025` | real | YES |  |
| 4 | `y2024` | real | YES |  |
| 5 | `y2023` | real | YES |  |
| 6 | `y2022` | real | YES |  |
| 7 | `y2021` | real | YES |  |
| 8 | `y2020` | real | YES |  |
| 9 | `y2019` | real | YES |  |
| 10 | `y2018` | real | YES |  |
| 11 | `y2017` | real | YES |  |
| 12 | `y2016` | real | YES |  |
| 13 | `y2015` | real | YES |  |

### pricing.pr_entregas_rentabilidad

**Columnas:** 38

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `vin` | varchar | YES |  |
| 2 | `centro` | varchar | YES |  |
| 3 | `codigo_modelo` | varchar | YES |  |
| 4 | `anio_modelo` | varchar | YES |  |
| 5 | `marca` | varchar | YES |  |
| 6 | `modelo_version` | varchar | YES |  |
| 7 | `tipo` | varchar | YES |  |
| 8 | `gama` | varchar | YES |  |
| 9 | `color` | varchar | YES |  |
| 10 | `kmsactuales` | bigint | YES |  |
| 11 | `placa` | varchar | YES |  |
| 12 | `fechaentregacliente` | timestamp(3) | YES |  |
| 13 | `nombreterceros` | varchar | YES |  |
| 14 | `nit` | varchar | YES |  |
| 15 | `fecha_venta` | timestamp(3) | YES |  |
| 16 | `fechafacturacompra` | timestamp(3) | YES |  |
| 17 | `total_factura` | decimal(20,4) | YES |  |
| 18 | `cantidad` | integer | YES |  |
| 19 | `precio_venta` | double | YES |  |
| 20 | `importecompra` | decimal(38,14) | YES |  |
| 21 | `netocompra` | decimal(38,12) | YES |  |
| 22 | `netoventa` | decimal(38,6) | YES |  |
| 23 | `margen` | decimal(38,6) | YES |  |
| 24 | `por_margen` | decimal(38,6) | YES |  |
| 25 | `codigo_fasecolda` | varchar | YES |  |
| 26 | `clase_f` | varchar | YES |  |
| 27 | `carroceria_f` | varchar | YES |  |
| 28 | `marca_f` | varchar | YES |  |
| 29 | `linea_f` | varchar | YES |  |
| 30 | `linea_consolidada_f` | varchar | YES |  |
| 31 | `cilindraje_f` | varchar | YES |  |
| 32 | `combustible_f` | varchar | YES |  |
| 33 | `airbags_f` | varchar | YES |  |
| 34 | `transmision_f` | varchar | YES |  |
| 35 | `tipo_traccion_f` | varchar | YES |  |
| 36 | `version_f` | varchar | YES |  |
| 37 | `especificaciones_f` | varchar | YES |  |
| 38 | `traccion_tipo_f` | varchar | YES |  |

### pricing.pr_homologacion_scaping

**Columnas:** 7

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `fuente` | varchar | YES |  |
| 2 | `texto_original` | varchar | YES |  |
| 3 | `marca` | varchar | YES |  |
| 4 | `modelo` | varchar | YES |  |
| 5 | `ano` | integer | YES |  |
| 6 | `codigo_fasecolda` | varchar | YES |  |
| 7 | `confiabilidad` | integer | YES |  |

### pricing.pr_mercadolibre_vehiculos

**Columnas:** 11

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id_hash` | varchar | YES |  |
| 2 | `nombre` | varchar | YES |  |
| 3 | `a�o_modelo` | integer | YES |  |
| 4 | `kilometraje` | varchar | YES |  |
| 5 | `valor` | bigint | YES |  |
| 6 | `url` | varchar | YES |  |
| 7 | `ubicacion` | varchar | YES |  |
| 8 | `publicacion_mes_anio` | varchar | YES |  |
| 9 | `publicacion_mes` | varchar | YES |  |
| 10 | `publicacion_anio` | varchar | YES |  |
| 11 | `fecha_scraping` | date | YES |  |

### pricing.pr_pricing_vehiculos

**Columnas:** 43

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `anio_modelo` | varchar | YES |  |
| 2 | `marca_f` | varchar | YES |  |
| 3 | `linea_f` | varchar | YES |  |
| 4 | `linea_consolidada_f` | varchar | YES |  |
| 5 | `version_f` | varchar | YES |  |
| 6 | `especificaciones_f` | varchar | YES |  |
| 7 | `clasificacion` | varchar | YES |  |
| 8 | `nivel_rotacion` | varchar | YES |  |
| 9 | `tiempo_rotacion` | real | YES |  |
| 10 | `demanda_unidades` | integer | YES |  |
| 11 | `margen_porcentual` | real | YES |  |
| 12 | `cal_margen_generado` | real | YES |  |
| 13 | `cal_tiempo_rotacion` | real | YES |  |
| 14 | `cal_demanda_unidades` | real | YES |  |
| 15 | `calificacion_final` | integer | YES |  |
| 16 | `condicion` | varchar | YES |  |
| 17 | `y2026` | real | YES |  |
| 18 | `y2025` | real | YES |  |
| 19 | `y2024` | real | YES |  |
| 20 | `y2023` | real | YES |  |
| 21 | `y2022` | real | YES |  |
| 22 | `y2021` | real | YES |  |
| 23 | `y2020` | real | YES |  |
| 24 | `y2019` | real | YES |  |
| 25 | `y2018` | real | YES |  |
| 26 | `y2017` | real | YES |  |
| 27 | `y2016` | real | YES |  |
| 28 | `y2015` | real | YES |  |
| 29 | `promedio_venta` | decimal(24,8) | YES |  |
| 30 | `extra_f` | varchar | YES |  |
| 31 | `version_extra` | varchar | YES |  |
| 32 | `y2026_p` | double | YES |  |
| 33 | `y2025_p` | double | YES |  |
| 34 | `y2024_p` | double | YES |  |
| 35 | `y2023_p` | double | YES |  |
| 36 | `y2022_p` | double | YES |  |
| 37 | `y2021_p` | double | YES |  |
| 38 | `y2020_p` | double | YES |  |
| 39 | `y2019_p` | double | YES |  |
| 40 | `y2018_p` | double | YES |  |
| 41 | `y2017_p` | double | YES |  |
| 42 | `y2016_p` | double | YES |  |
| 43 | `y2015_p` | double | YES |  |

### pricing.pr_scoring_vehiculos

**Columnas:** 16

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `anio_modelo` | integer | YES |  |
| 2 | `marca` | varchar | YES |  |
| 3 | `modelo` | varchar | YES |  |
| 4 | `margen_generado` | real | YES |  |
| 5 | `tiempo_rotacion` | real | YES |  |
| 6 | `demanda_unidades` | integer | YES |  |
| 7 | `margen_porcentual` | real | YES |  |
| 8 | `cal_margen_generado` | real | YES |  |
| 9 | `cal_tiempo_rotacion` | real | YES |  |
| 10 | `cal_demanda_unidades` | real | YES |  |
| 11 | `calificacion_final` | integer | YES |  |
| 12 | `nivel_calificacion` | varchar | YES |  |
| 13 | `margen_curva` | varchar | YES |  |
| 14 | `rotacion_curva` | varchar | YES |  |
| 15 | `demanda_curva` | varchar | YES |  |
| 16 | `nivel_rotacion` | varchar | YES |  |

### pricing.pr_scoring_vehiculos_historico

**Columnas:** 17

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `anio_modelo` | integer | YES |  |
| 2 | `marca` | varchar | YES |  |
| 3 | `modelo` | varchar | YES |  |
| 4 | `margen_generado` | real | YES |  |
| 5 | `tiempo_rotacion` | real | YES |  |
| 6 | `demanda_unidades` | integer | YES |  |
| 7 | `margen_porcentual` | real | YES |  |
| 8 | `cal_margen_generado` | real | YES |  |
| 9 | `cal_tiempo_rotacion` | real | YES |  |
| 10 | `cal_demanda_unidades` | real | YES |  |
| 11 | `calificacion_final` | integer | YES |  |
| 12 | `nivel_calificacion` | varchar | YES |  |
| 13 | `nivel_rotacion` | varchar | YES |  |
| 14 | `margen_curva` | varchar | YES |  |
| 15 | `rotacion_curva` | varchar | YES |  |
| 16 | `demanda_curva` | varchar | YES |  |
| 17 | `fecha_ejecucion` | varchar | YES |  |

### pricing.pr_scraping_rentabilidad

**Columnas:** 20

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codigo_homologacion` | varchar | YES |  |
| 2 | `clase` | varchar | YES |  |
| 3 | `carroceria` | varchar | YES |  |
| 4 | `marca` | varchar | YES |  |
| 5 | `linea` | varchar | YES |  |
| 6 | `linea_consolidada` | varchar | YES |  |
| 7 | `modelo` | varchar | YES |  |
| 8 | `cilindraje` | varchar | YES |  |
| 9 | `combustible` | varchar | YES |  |
| 10 | `airbags` | varchar | YES |  |
| 11 | `transmision` | varchar | YES |  |
| 12 | `tipo_traccion` | varchar | YES |  |
| 13 | `version` | varchar | YES |  |
| 14 | `especificaciones` | varchar | YES |  |
| 15 | `traccion_tipo` | varchar | YES |  |
| 16 | `valor` | bigint | YES |  |
| 17 | `fecha_publicacion` | date | YES |  |
| 18 | `fuente` | varchar | YES |  |
| 19 | `kilometraje` | integer | YES |  |
| 20 | `url` | varchar | YES |  |

## 🥉 runt

`Capa: Bronce / Raw`

### runt.autos

**Columnas:** 42

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id_vehiculo` | bigint | YES |  |
| 2 | `a�o_matricula` | varchar | YES |  |
| 3 | `mes_matricula` | varchar | YES |  |
| 4 | `dia_matricula` | varchar | YES |  |
| 5 | `clase` | varchar | YES |  |
| 6 | `carroceria` | varchar | YES |  |
| 7 | `marca` | varchar | YES |  |
| 8 | `linea` | varchar | YES |  |
| 9 | `modelo` | varchar | YES |  |
| 10 | `servicio` | varchar | YES |  |
| 11 | `pais_origen` | varchar | YES |  |
| 12 | `color` | varchar | YES |  |
| 13 | `segmento` | varchar | YES |  |
| 14 | `cilindraje` | varchar | YES |  |
| 15 | `numero_ejes` | varchar | YES |  |
| 16 | `numero_puertas` | varchar | YES |  |
| 17 | `pasajeros_sentados` | varchar | YES |  |
| 18 | `capacidad_carga` | varchar | YES |  |
| 19 | `peso` | varchar | YES |  |
| 20 | `departamento` | varchar | YES |  |
| 21 | `municipio` | varchar | YES |  |
| 22 | `combustible` | varchar | YES |  |
| 23 | `tipo_matricula` | varchar | YES |  |
| 24 | `prenda` | varchar | YES |  |
| 25 | `nombre_entidad_prenda` | varchar | YES |  |
| 26 | `ciudad_propietario` | varchar | YES |  |
| 27 | `modalidad` | varchar | YES |  |
| 28 | `aire_acondicionado` | varchar | YES |  |
| 29 | `airbag` | varchar | YES |  |
| 30 | `tipo_transmision` | varchar | YES |  |
| 31 | `nivel_emisiones` | varchar | YES |  |
| 32 | `tipo_aspiracion` | varchar | YES |  |
| 33 | `apoya_cabeza` | varchar | YES |  |
| 34 | `tipo_freno` | varchar | YES |  |
| 35 | `tipo_traccion` | varchar | YES |  |
| 36 | `leasing` | varchar | YES |  |
| 37 | `nombre_entidad_leasing` | varchar | YES |  |
| 38 | `nit_leasing` | varchar | YES |  |
| 39 | `acreedor` | varchar | YES |  |
| 40 | `nombre_aseguradora` | varchar | YES |  |
| 41 | `claraboya_sunroof` | varchar | YES |  |
| 42 | `identificador_combustible` | varchar | YES |  |

### runt.autos_peru

**Columnas:** 24

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `fecha_alta` | varchar | YES |  |
| 2 | `departamento` | varchar | YES |  |
| 3 | `oficina_registral` | varchar | YES |  |
| 4 | `clase_vehicular` | varchar | YES |  |
| 5 | `categoria_aap` | varchar | YES |  |
| 6 | `carroceria` | varchar | YES |  |
| 7 | `marca` | varchar | YES |  |
| 8 | `modelo` | varchar | YES |  |
| 9 | `version` | varchar | YES |  |
| 10 | `pbv` | varchar | YES |  |
| 11 | `asientos` | varchar | YES |  |
| 12 | `combustible` | varchar | YES |  |
| 13 | `categoria` | varchar | YES |  |
| 14 | `uso_vehiculo` | varchar | YES |  |
| 15 | `tipo_doc_prop` | varchar | YES |  |
| 16 | `formula_rodante` | varchar | YES |  |
| 17 | `transmision` | varchar | YES |  |
| 18 | `cilindrada` | varchar | YES |  |
| 19 | `potencia_motor` | varchar | YES |  |
| 20 | `color` | varchar | YES |  |
| 21 | `anio_mod` | varchar | YES |  |
| 22 | `pais_origen` | varchar | YES |  |
| 23 | `tramite_origen` | varchar | YES |  |
| 24 | `cantidad` | varchar | YES |  |

### runt.prenda

**Columnas:** 35

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `placa` | varchar | YES |  |
| 2 | `id_vehiculo` | bigint | YES |  |
| 3 | `a�o_matricula` | bigint | YES |  |
| 4 | `mes_matricula` | bigint | YES |  |
| 5 | `dia_matricula` | bigint | YES |  |
| 6 | `clase` | varchar | YES |  |
| 7 | `vin` | varchar | YES |  |
| 8 | `carroceria` | varchar | YES |  |
| 9 | `chasis` | varchar | YES |  |
| 10 | `linea` | varchar | YES |  |
| 11 | `modelo` | bigint | YES |  |
| 12 | `servicio` | varchar | YES |  |
| 13 | `pais` | varchar | YES |  |
| 14 | `color` | varchar | YES |  |
| 15 | `segmento` | varchar | YES |  |
| 16 | `cilindraje` | bigint | YES |  |
| 17 | `numero_ejes` | bigint | YES |  |
| 18 | `numero_puertas` | bigint | YES |  |
| 19 | `pasajeros_sentados` | bigint | YES |  |
| 20 | `capacidad_carga` | varchar | YES |  |
| 21 | `peso` | bigint | YES |  |
| 22 | `departamento` | varchar | YES |  |
| 23 | `municipio` | varchar | YES |  |
| 24 | `combustible` | varchar | YES |  |
| 25 | `tipo_matricula` | varchar | YES |  |
| 26 | `ciudad_propietario` | varchar | YES |  |
| 27 | `declaracion_importacion` | bigint | YES |  |
| 28 | `motor` | varchar | YES |  |
| 29 | `serie` | varchar | YES |  |
| 30 | `marca` | varchar | YES |  |
| 31 | `blindado` | varchar | YES |  |
| 32 | `nit_empresa_blindaje` | varchar | YES |  |
| 33 | `claraboya_sunroof` | varchar | YES |  |
| 34 | `identificador_combustible` | bigint | YES |  |
| 35 | `archivo` | varchar | YES |  |

### runt.runt_final

**Columnas:** 67

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `consecutivo` | integer | YES |  |
| 2 | `anio_mi` | integer | YES |  |
| 3 | `mes_mi` | integer | YES |  |
| 4 | `clase` | varchar | YES |  |
| 5 | `carroceria` | varchar | YES |  |
| 6 | `marca` | varchar | YES |  |
| 7 | `marca_otras` | varchar | YES |  |
| 8 | `linea` | varchar | YES |  |
| 9 | `linea_consolidada` | varchar | YES |  |
| 10 | `modelo` | integer | YES |  |
| 11 | `servicio` | varchar | YES |  |
| 12 | `nacional_importado` | varchar | YES |  |
| 13 | `color` | varchar | YES |  |
| 14 | `segmento` | varchar | YES |  |
| 15 | `sub_segmentos` | varchar | YES |  |
| 16 | `cilindraje` | varchar | YES |  |
| 17 | `cantidad_ejes` | varchar | YES |  |
| 18 | `puertas` | varchar | YES |  |
| 19 | `pasajeros_sentados` | varchar | YES |  |
| 20 | `capacidad_carga` | varchar | YES |  |
| 21 | `peso` | varchar | YES |  |
| 22 | `departamento` | varchar | YES |  |
| 23 | `region` | varchar | YES |  |
| 24 | `municipio_ciudad` | varchar | YES |  |
| 25 | `combustible` | varchar | YES |  |
| 26 | `combust_nev` | varchar | YES |  |
| 27 | `tipo_matricula` | varchar | YES |  |
| 28 | `prenda_si_no` | varchar | YES |  |
| 29 | `nombre_entidad_prenda` | varchar | YES |  |
| 30 | `ciudad_residencia_propietario` | varchar | YES |  |
| 31 | `modalidad_transporte` | varchar | YES |  |
| 32 | `a_c` | varchar | YES |  |
| 33 | `airbags` | varchar | YES |  |
| 34 | `transmision` | varchar | YES |  |
| 35 | `nivel_emisiones` | varchar | YES |  |
| 36 | `tipo_aspiracion` | varchar | YES |  |
| 37 | `apoyacabezas` | varchar | YES |  |
| 38 | `tipo_freno` | varchar | YES |  |
| 39 | `tipo_traccion` | varchar | YES |  |
| 40 | `leasing` | varchar | YES |  |
| 41 | `nombre_entidad_leasing` | varchar | YES |  |
| 42 | `nit_leasing` | varchar | YES |  |
| 43 | `acreedor` | varchar | YES |  |
| 44 | `nombre_aseguradora` | varchar | YES |  |
| 45 | `claraboya_sunroof` | varchar | YES |  |
| 46 | `identificador_combustible` | varchar | YES |  |
| 47 | `fecha` | date | YES |  |
| 48 | `origen` | varchar | YES |  |
| 49 | `iso_ue` | varchar | YES |  |
| 50 | `byd_rel` | varchar | YES |  |
| 51 | `cantidad` | varchar | YES |  |
| 52 | `concatenado` | varchar | YES |  |
| 53 | `concatenado2` | varchar | YES |  |
| 54 | `segmento_x` | varchar | YES |  |
| 55 | `segmento_e` | varchar | YES |  |
| 56 | `body_style` | varchar | YES |  |
| 57 | `representante_importador_vc` | varchar | YES |  |
| 58 | `representante_importador_nev` | varchar | YES |  |
| 59 | `seg_tamanio` | varchar | YES |  |
| 60 | `crucetamanio` | varchar | YES |  |
| 61 | `llavepais` | varchar | YES |  |
| 62 | `llave_mt` | varchar | YES |  |
| 63 | `minitrucks` | varchar | YES |  |
| 64 | `sub_segmento_vhc` | varchar | YES |  |
| 65 | `segmento_vhc` | varchar | YES |  |
| 66 | `sub_sub_segmento_vhc` | varchar | YES |  |
| 67 | `filtro_carroceria` | varchar | YES |  |

## 🥉 seissa

`Capa: Bronce / Raw`

### seissa.bellpi_predictions

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `last_purchase_date` | date | YES |  |
| 3 | `days_since_last_purchase` | integer | YES |  |
| 4 | `total_purchases` | integer | YES |  |
| 5 | `total_spent` | real | YES |  |
| 6 | `last_product` | integer | YES |  |
| 7 | `unique_products` | integer | YES |  |
| 8 | `avg_days_between_purchases` | real | YES |  |
| 9 | `age` | varchar | YES |  |
| 10 | `gender` | varchar | YES |  |
| 11 | `city` | varchar | YES |  |
| 12 | `predicted_product` | integer | YES |  |
| 13 | `probability` | real | YES |  |
| 14 | `empresa_origen` | varchar | YES |  |
| 15 | `timestamp` | date | YES |  |

### seissa.bonaparte_predictions

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `last_purchase_date` | date | YES |  |
| 3 | `days_since_last_purchase` | integer | YES |  |
| 4 | `total_purchases` | integer | YES |  |
| 5 | `total_spent` | real | YES |  |
| 6 | `last_product` | integer | YES |  |
| 7 | `unique_products` | integer | YES |  |
| 8 | `avg_days_between_purchases` | real | YES |  |
| 9 | `age` | varchar | YES |  |
| 10 | `gender` | varchar | YES |  |
| 11 | `city` | varchar | YES |  |
| 12 | `predicted_product` | integer | YES |  |
| 13 | `probability` | real | YES |  |
| 14 | `empresa_origen` | varchar | YES |  |
| 15 | `timestamp` | date | YES |  |

### seissa.casatoro_predictions

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `last_purchase_date` | date | YES |  |
| 3 | `days_since_last_purchase` | integer | YES |  |
| 4 | `total_purchases` | integer | YES |  |
| 5 | `total_spent` | real | YES |  |
| 6 | `last_product` | integer | YES |  |
| 7 | `unique_products` | integer | YES |  |
| 8 | `avg_days_between_purchases` | real | YES |  |
| 9 | `age` | varchar | YES |  |
| 10 | `gender` | varchar | YES |  |
| 11 | `city` | varchar | YES |  |
| 12 | `predicted_product` | integer | YES |  |
| 13 | `probability` | real | YES |  |
| 14 | `empresa_origen` | varchar | YES |  |
| 15 | `timestamp` | date | YES |  |

### seissa.clientes_muestra_10000

**Columnas:** 1

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |

### seissa.cmn_cities

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `city_id` | integer | YES |  |
| 2 | `departament` | varchar | YES |  |
| 3 | `municipality` | varchar | YES |  |
| 4 | `code_municipality` | varchar | YES |  |
| 5 | `commune` | varchar | YES |  |
| 6 | `code_commune` | varchar | YES |  |
| 7 | `latitude_municipality` | varchar | YES |  |
| 8 | `longitude_municipality` | varchar | YES |  |

### seissa.cmn_colors

**Columnas:** 4

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `color_id` | integer | YES |  |
| 2 | `color` | varchar | YES |  |
| 3 | `homologated_color` | varchar | YES |  |
| 4 | `status` | boolean | YES |  |

### seissa.cmn_companies

**Columnas:** 4

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `company_id` | integer | YES |  |
| 2 | `company_name` | varchar | YES |  |
| 3 | `acronymus_company` | varchar | YES |  |
| 4 | `status` | boolean | YES |  |

### seissa.cmn_country_codes

**Columnas:** 4

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `code_id` | integer | YES |  |
| 2 | `code` | integer | YES |  |
| 3 | `country` | varchar | YES |  |
| 4 | `continent` | varchar | YES |  |

### seissa.dim_cli_address

**Columnas:** 5

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `address_id` | integer | YES |  |
| 2 | `city_id` | integer | YES |  |
| 3 | `address` | varchar | YES |  |
| 4 | `status` | boolean | YES |  |
| 5 | `load_data` | timestamp(3) | YES |  |

### seissa.dim_cli_economic_sector

**Columnas:** 6

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `economic_id` | integer | YES |  |
| 2 | `homologation` | varchar | YES |  |
| 3 | `sector` | varchar | YES |  |
| 4 | `category` | varchar | YES |  |
| 5 | `status` | boolean | YES |  |
| 6 | `load_date` | timestamp(3) | YES |  |

### seissa.dim_cli_education_level

**Columnas:** 3

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `education_id` | integer | YES |  |
| 2 | `name_education` | varchar | YES |  |
| 3 | `status` | boolean | YES |  |

### seissa.dim_cli_email

**Columnas:** 4

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `email_id` | integer | YES |  |
| 2 | `email` | varchar | YES |  |
| 3 | `status` | boolean | YES |  |
| 4 | `load_data` | timestamp(3) | YES |  |

### seissa.dim_cli_gender

**Columnas:** 3

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `gender_id` | integer | YES |  |
| 2 | `gender_name` | varchar | YES |  |
| 3 | `status` | boolean | YES |  |

### seissa.dim_cli_marital_status

**Columnas:** 3

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `marital_id` | integer | YES |  |
| 2 | `marital_status` | varchar | YES |  |
| 3 | `status` | boolean | YES |  |

### seissa.dim_cli_occupation

**Columnas:** 6

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `occupation_id` | integer | YES |  |
| 2 | `homologation` | varchar | YES |  |
| 3 | `occupation` | varchar | YES |  |
| 4 | `category` | varchar | YES |  |
| 5 | `status` | boolean | YES |  |
| 6 | `load_date` | timestamp(3) | YES |  |

### seissa.dim_cli_phone

**Columnas:** 5

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `phone_id` | integer | YES |  |
| 2 | `phone_number` | varchar | YES |  |
| 3 | `area_code_id` | integer | YES |  |
| 4 | `status` | boolean | YES |  |
| 5 | `load_data` | timestamp(3) | YES |  |

### seissa.dim_cli_phone_area_code

**Columnas:** 3

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `area_code_id` | integer | YES |  |
| 2 | `city_id` | integer | YES |  |
| 3 | `code` | integer | YES |  |

### seissa.dim_cli_status_client

**Columnas:** 3

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `status_id` | integer | YES |  |
| 2 | `status_name` | varchar | YES |  |
| 3 | `status` | boolean | YES |  |

### seissa.dim_cli_type_identification

**Columnas:** 3

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `type_id` | integer | YES |  |
| 2 | `type_name` | varchar | YES |  |
| 3 | `status` | boolean | YES |  |

### seissa.dim_cli_type_person

**Columnas:** 3

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `type_person_id` | integer | YES |  |
| 2 | `type_person_name` | varchar | YES |  |
| 3 | `status` | boolean | YES |  |

### seissa.dim_concepts

**Columnas:** 3

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `concept_id` | integer | YES |  |
| 2 | `concept_name` | varchar | YES |  |
| 3 | `status` | boolean | YES |  |

### seissa.dim_link_client_address

**Columnas:** 6

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `cli_ph_id` | integer | YES |  |
| 2 | `client_id` | integer | YES |  |
| 3 | `address_id` | integer | YES |  |
| 4 | `company_id` | integer | YES |  |
| 5 | `status` | integer | YES |  |
| 6 | `load_data` | timestamp(3) | YES |  |

### seissa.dim_link_client_company

**Columnas:** 7

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `cli_ph_id` | integer | YES |  |
| 2 | `client_id` | integer | YES |  |
| 3 | `company_id` | integer | YES |  |
| 4 | `linking_date` | timestamp(3) | YES |  |
| 5 | `status_linking` | smallint | YES |  |
| 6 | `load_date` | timestamp(3) | YES |  |
| 7 | `update_date` | timestamp(3) | YES |  |

### seissa.dim_link_client_email

**Columnas:** 6

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `cli_em_id` | integer | YES |  |
| 2 | `client_id` | integer | YES |  |
| 3 | `email_id` | integer | YES |  |
| 4 | `company_id` | integer | YES |  |
| 5 | `status` | boolean | YES |  |
| 6 | `load_data` | timestamp(3) | YES |  |

### seissa.dim_link_client_phone

**Columnas:** 6

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `cli_ph_id` | integer | YES |  |
| 2 | `client_id` | integer | YES |  |
| 3 | `phone_id` | integer | YES |  |
| 4 | `company_id` | integer | YES |  |
| 5 | `status` | boolean | YES |  |
| 6 | `load_data` | timestamp(3) | YES |  |

### seissa.dim_link_vehicle_company

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `cli_veh_id` | integer | YES |  |
| 2 | `vehicle_id` | integer | YES |  |
| 3 | `company_id` | integer | YES |  |
| 4 | `linking_date` | timestamp(3) | YES |  |
| 5 | `status_linking` | smallint | YES |  |
| 6 | `client_id` | integer | YES |  |
| 7 | `load_date` | timestamp(3) | YES |  |
| 8 | `update_date` | timestamp(3) | YES |  |

### seissa.dim_pro_contracts

**Columnas:** 4

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `contract_id` | integer | YES |  |
| 2 | `contract_number` | varchar | YES |  |
| 3 | `date_load` | timestamp(3) | YES |  |
| 4 | `status` | boolean | YES |  |

### seissa.dim_pro_insurance_company_pt

**Columnas:** 3

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `insurance_id` | integer | YES |  |
| 2 | `product_id` | integer | YES |  |
| 3 | `company` | varchar | YES |  |

### seissa.dim_pro_product_homologation

**Columnas:** 4

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `homologated_product_id` | integer | YES |  |
| 2 | `company_id` | integer | YES |  |
| 3 | `homologated_product_name` | varchar | YES |  |
| 4 | `status` | boolean | YES |  |

### seissa.dim_pro_products_service

**Columnas:** 5

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `product_services_id` | integer | YES |  |
| 2 | `homologated_product_id` | integer | YES |  |
| 3 | `product_name` | varchar | YES |  |
| 4 | `status` | boolean | YES |  |
| 5 | `homologated_product_2` | varchar | YES |  |

### seissa.dim_pro_status_product

**Columnas:** 3

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `status_id` | integer | YES |  |
| 2 | `status_name` | varchar | YES |  |
| 3 | `status` | boolean | YES |  |

### seissa.dim_veh_body_car

**Columnas:** 2

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `body_id` | integer | YES |  |
| 2 | `body_car` | varchar | YES |  |

### seissa.dim_veh_brands

**Columnas:** 6

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `brand_id` | integer | YES |  |
| 2 | `brand` | varchar | YES |  |
| 3 | `homologated_brand` | varchar | YES |  |
| 4 | `status` | boolean | YES |  |
| 5 | `categoria` | varchar | YES |  |
| 6 | `load_data` | timestamp(3) | YES |  |

### seissa.dim_veh_class

**Columnas:** 7

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `class_id` | integer | YES |  |
| 2 | `class` | varchar | YES |  |
| 3 | `homologated_class` | varchar | YES |  |
| 4 | `consolidated_class` | varchar | YES |  |
| 5 | `body_car` | varchar | YES |  |
| 6 | `status` | boolean | YES |  |
| 7 | `load_data` | timestamp(3) | YES |  |

### seissa.dim_veh_condition

**Columnas:** 3

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `condition_id` | integer | YES |  |
| 2 | `condition_name` | varchar | YES |  |
| 3 | `status` | boolean | YES |  |

### seissa.dim_veh_fuel

**Columnas:** 5

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `fuel_id` | integer | YES |  |
| 2 | `fuel` | varchar | YES |  |
| 3 | `homologated_fuel` | varchar | YES |  |
| 4 | `status` | boolean | YES |  |
| 5 | `load_data` | timestamp(3) | YES |  |

### seissa.dim_veh_references

**Columnas:** 5

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `reference_id` | integer | YES |  |
| 2 | `reference` | varchar | YES |  |
| 3 | `homologated_reference` | varchar | YES |  |
| 4 | `status` | boolean | YES |  |
| 5 | `load_data` | timestamp(3) | YES |  |

### seissa.dim_veh_service

**Columnas:** 3

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `service_id` | integer | YES |  |
| 2 | `service` | varchar | YES |  |
| 3 | `status` | boolean | YES |  |

### seissa.equirent_predictions

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `last_purchase_date` | date | YES |  |
| 3 | `days_since_last_purchase` | integer | YES |  |
| 4 | `total_purchases` | integer | YES |  |
| 5 | `total_spent` | real | YES |  |
| 6 | `last_product` | integer | YES |  |
| 7 | `unique_products` | integer | YES |  |
| 8 | `avg_days_between_purchases` | real | YES |  |
| 9 | `age` | varchar | YES |  |
| 10 | `gender` | varchar | YES |  |
| 11 | `city` | varchar | YES |  |
| 12 | `predicted_product` | integer | YES |  |
| 13 | `probability` | real | YES |  |
| 14 | `empresa_origen` | varchar | YES |  |
| 15 | `timestamp` | date | YES |  |

### seissa.fact_clients

**Columnas:** 19

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `identification` | varchar | YES |  |
| 3 | `type_id` | integer | YES |  |
| 4 | `type_person_id` | integer | YES |  |
| 5 | `name` | varchar | YES |  |
| 6 | `status_id` | integer | YES |  |
| 7 | `gender_id` | integer | YES |  |
| 8 | `marital_id` | integer | YES |  |
| 9 | `education_id` | integer | YES |  |
| 10 | `economic_id` | integer | YES |  |
| 11 | `monthly_income` | decimal(16,4) | YES |  |
| 12 | `occupation_id` | integer | YES |  |
| 13 | `city_id` | integer | YES |  |
| 14 | `date_of_birth` | date | YES |  |
| 15 | `age` | integer | YES |  |
| 16 | `people_in_charge` | integer | YES |  |
| 17 | `code_country_id` | integer | YES |  |
| 18 | `load_data` | timestamp(3) | YES |  |
| 19 | `update_data` | timestamp(3) | YES |  |

### seissa.fact_purchased_products

**Columnas:** 11

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `product_id` | integer | YES |  |
| 2 | `company_id` | integer | YES |  |
| 3 | `product_service_id` | integer | YES |  |
| 4 | `contract_id` | integer | YES |  |
| 5 | `sale_amount` | decimal(19,4) | YES |  |
| 6 | `financed_amount` | decimal(19,4) | YES |  |
| 7 | `invoiced_amount` | decimal(19,4) | YES |  |
| 8 | `contract_date` | timestamp(3) | YES |  |
| 9 | `status_id` | integer | YES |  |
| 10 | `date_load` | timestamp(3) | YES |  |
| 11 | `update_data` | timestamp(3) | YES |  |

### seissa.fact_seissa

**Columnas:** 9

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `seissa_id` | integer | YES |  |
| 2 | `client_id` | integer | YES |  |
| 3 | `vehicle_id` | integer | YES |  |
| 4 | `product_id` | integer | YES |  |
| 5 | `company_id` | integer | YES |  |
| 6 | `concept_id` | integer | YES |  |
| 7 | `date_concept` | timestamp(3) | YES |  |
| 8 | `date_load` | timestamp(3) | YES |  |
| 9 | `update_date` | timestamp(3) | YES |  |

### seissa.fact_vehicles

**Columnas:** 19

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `vehicle_id` | integer | YES |  |
| 2 | `plate_name` | varchar | YES |  |
| 3 | `vin` | varchar | YES |  |
| 4 | `fasecolda_code` | varchar | YES |  |
| 5 | `year_model` | varchar | YES |  |
| 6 | `reference_id` | integer | YES |  |
| 7 | `engine_displacement` | integer | YES |  |
| 8 | `price` | decimal(18,2) | YES |  |
| 9 | `mileage` | double | YES |  |
| 10 | `brand_id` | integer | YES |  |
| 11 | `class_id` | integer | YES |  |
| 12 | `service_id` | integer | YES |  |
| 13 | `condition_id` | integer | YES |  |
| 14 | `fuel_id` | integer | YES |  |
| 15 | `city_id` | integer | YES |  |
| 16 | `color_id` | integer | YES |  |
| 17 | `mark_casatoro` | integer | YES |  |
| 18 | `date_load` | timestamp(3) | YES |  |
| 19 | `update_data` | timestamp(3) | YES |  |

### seissa.finandina_predictions

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `last_purchase_date` | date | YES |  |
| 3 | `days_since_last_purchase` | integer | YES |  |
| 4 | `total_purchases` | integer | YES |  |
| 5 | `total_spent` | real | YES |  |
| 6 | `last_product` | integer | YES |  |
| 7 | `unique_products` | integer | YES |  |
| 8 | `avg_days_between_purchases` | real | YES |  |
| 9 | `age` | varchar | YES |  |
| 10 | `gender` | varchar | YES |  |
| 11 | `city` | varchar | YES |  |
| 12 | `predicted_product` | integer | YES |  |
| 13 | `probability` | real | YES |  |
| 14 | `empresa_origen` | varchar | YES |  |
| 15 | `timestamp` | date | YES |  |

### seissa.finanzauto_predictions

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `last_purchase_date` | date | YES |  |
| 3 | `days_since_last_purchase` | integer | YES |  |
| 4 | `total_purchases` | integer | YES |  |
| 5 | `total_spent` | real | YES |  |
| 6 | `last_product` | integer | YES |  |
| 7 | `unique_products` | integer | YES |  |
| 8 | `avg_days_between_purchases` | real | YES |  |
| 9 | `age` | varchar | YES |  |
| 10 | `gender` | varchar | YES |  |
| 11 | `city` | varchar | YES |  |
| 12 | `predicted_product` | integer | YES |  |
| 13 | `probability` | real | YES |  |
| 14 | `empresa_origen` | varchar | YES |  |
| 15 | `timestamp` | date | YES |  |

### seissa.modelo_datos_bi

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `name` | varchar | YES |  |
| 3 | `age` | integer | YES |  |
| 4 | `gender_name` | varchar | YES |  |
| 5 | `monthly_income` | decimal(16,4) | YES |  |
| 6 | `municipality` | varchar | YES |  |
| 7 | `departament` | varchar | YES |  |
| 8 | `contract_id` | integer | YES |  |
| 9 | `product_id` | integer | YES |  |
| 10 | `homologated_product_name` | varchar | YES |  |
| 11 | `company_id` | integer | YES |  |
| 12 | `product_service_id` | integer | YES |  |
| 13 | `product_name` | varchar | YES |  |
| 14 | `sale_amount` | decimal(19,4) | YES |  |
| 15 | `contract_date` | timestamp(3) | YES |  |

### seissa.modelo_datos_ml

**Columnas:** 26

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `product_id` | integer | YES |  |
| 3 | `type_person_name` | varchar | YES |  |
| 4 | `product_services_id` | integer | YES |  |
| 5 | `numero_compra` | bigint | YES |  |
| 6 | `producto_origen_id` | integer | YES |  |
| 7 | `contract_date` | timestamp(3) | YES |  |
| 8 | `dias_proxima_compra` | bigint | YES |  |
| 9 | `target_id` | integer | YES |  |
| 10 | `sale_amount` | varchar | YES |  |
| 11 | `financed_amount` | varchar | YES |  |
| 12 | `invoiced_amount` | varchar | YES |  |
| 13 | `dias_desde_ultima_compra` | bigint | YES |  |
| 14 | `event_tipo` | integer | YES |  |
| 15 | `age` | integer | YES |  |
| 16 | `gender_name` | varchar | YES |  |
| 17 | `monthly_income` | decimal(16,4) | YES |  |
| 18 | `municipality` | varchar | YES |  |
| 19 | `departament` | varchar | YES |  |
| 20 | `marital_status` | varchar | YES |  |
| 21 | `occupation` | varchar | YES |  |
| 22 | `level_education` | varchar | YES |  |
| 23 | `client_status` | varchar | YES |  |
| 24 | `country` | varchar | YES |  |
| 25 | `fecha_primera_compra` | timestamp(3) | YES |  |
| 26 | `dias_desde_primera_compra` | bigint | YES |  |

### seissa.modelo_datos_ml_vf

**Columnas:** 46

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `sequence` | bigint | YES |  |
| 3 | `product_services_id` | integer | YES |  |
| 4 | `contract_date` | timestamp(3) | YES |  |
| 5 | `dias_proxima_compra` | bigint | YES |  |
| 6 | `sale_amount` | double | YES |  |
| 7 | `financed_amount` | double | YES |  |
| 8 | `invoiced_amount` | double | YES |  |
| 9 | `dias_desde_ultima_compra` | bigint | YES |  |
| 10 | `event_tipo` | integer | YES |  |
| 11 | `age` | integer | YES |  |
| 12 | `gender_name` | varchar | YES |  |
| 13 | `monthly_income` | decimal(16,4) | YES |  |
| 14 | `municipality` | varchar | YES |  |
| 15 | `departament` | varchar | YES |  |
| 16 | `marital_status` | varchar | YES |  |
| 17 | `occupation` | varchar | YES |  |
| 18 | `level_education` | varchar | YES |  |
| 19 | `client_status` | varchar | YES |  |
| 20 | `country` | varchar | YES |  |
| 21 | `fecha_primera_compra` | timestamp(3) | YES |  |
| 22 | `dias_desde_primera_compra` | bigint | YES |  |
| 23 | `type_person_name` | varchar | YES |  |
| 24 | `year` | bigint | YES |  |
| 25 | `month` | bigint | YES |  |
| 26 | `quarter` | bigint | YES |  |
| 27 | `day_of_week` | bigint | YES |  |
| 28 | `day_of_year` | bigint | YES |  |
| 29 | `is_first_purchase` | integer | YES |  |
| 30 | `days_since_first` | bigint | YES |  |
| 31 | `previous_product` | varchar | YES |  |
| 32 | `target_id` | integer | YES |  |
| 33 | `client_total_purchases` | bigint | YES |  |
| 34 | `client_unique_products` | bigint | YES |  |
| 35 | `client_avg_amount` | double | YES |  |
| 36 | `client_total_amount` | double | YES |  |
| 37 | `client_amount_std` | double | YES |  |
| 38 | `client_first_date` | timestamp(3) | YES |  |
| 39 | `client_last_date` | timestamp(3) | YES |  |
| 40 | `client_lifetime_days` | bigint | YES |  |
| 41 | `client_product_diversity` | double | YES |  |
| 42 | `product_unique_clients` | bigint | YES |  |
| 43 | `product_avg_amount` | double | YES |  |
| 44 | `product_frequency` | bigint | YES |  |
| 45 | `product_avg_sequence` | double | YES |  |
| 46 | `product_sequence_std` | double | YES |  |

### seissa.modelo_datos_what

**Columnas:** 45

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `sequence` | bigint | YES |  |
| 3 | `product_services_id` | integer | YES |  |
| 4 | `contract_date` | timestamp(3) | YES |  |
| 5 | `sale_amount` | double | YES |  |
| 6 | `target_id` | integer | YES |  |
| 7 | `financed_amount` | double | YES |  |
| 8 | `invoiced_amount` | double | YES |  |
| 9 | `dias_desde_ultima_compra` | bigint | YES |  |
| 10 | `event_tipo` | integer | YES |  |
| 11 | `age` | integer | YES |  |
| 12 | `gender_name` | varchar | YES |  |
| 13 | `monthly_income` | decimal(16,4) | YES |  |
| 14 | `municipality` | varchar | YES |  |
| 15 | `departament` | varchar | YES |  |
| 16 | `marital_status` | varchar | YES |  |
| 17 | `occupation` | varchar | YES |  |
| 18 | `level_education` | varchar | YES |  |
| 19 | `client_status` | varchar | YES |  |
| 20 | `country` | varchar | YES |  |
| 21 | `fecha_primera_compra` | timestamp(3) | YES |  |
| 22 | `dias_desde_primera_compra` | bigint | YES |  |
| 23 | `type_person_name` | varchar | YES |  |
| 24 | `year` | bigint | YES |  |
| 25 | `month` | bigint | YES |  |
| 26 | `quarter` | bigint | YES |  |
| 27 | `day_of_week` | bigint | YES |  |
| 28 | `day_of_year` | bigint | YES |  |
| 29 | `is_first_purchase` | integer | YES |  |
| 30 | `days_since_first` | bigint | YES |  |
| 31 | `previous_product` | varchar | YES |  |
| 32 | `client_total_purchases` | bigint | YES |  |
| 33 | `client_unique_products` | bigint | YES |  |
| 34 | `client_avg_amount` | double | YES |  |
| 35 | `client_total_amount` | double | YES |  |
| 36 | `client_amount_std` | double | YES |  |
| 37 | `client_first_date` | timestamp(3) | YES |  |
| 38 | `client_last_date` | timestamp(3) | YES |  |
| 39 | `client_lifetime_days` | bigint | YES |  |
| 40 | `client_product_diversity` | double | YES |  |
| 41 | `product_unique_clients` | bigint | YES |  |
| 42 | `product_avg_amount` | double | YES |  |
| 43 | `product_frequency` | bigint | YES |  |
| 44 | `product_avg_sequence` | double | YES |  |
| 45 | `product_sequence_std` | double | YES |  |

### seissa.modelo_datos_when

**Columnas:** 45

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `sequence` | bigint | YES |  |
| 3 | `product_services_id` | integer | YES |  |
| 4 | `contract_date` | timestamp(3) | YES |  |
| 5 | `sale_amount` | double | YES |  |
| 6 | `target_id` | integer | YES |  |
| 7 | `financed_amount` | double | YES |  |
| 8 | `invoiced_amount` | double | YES |  |
| 9 | `dias_desde_ultima_compra` | bigint | YES |  |
| 10 | `event_tipo` | integer | YES |  |
| 11 | `age` | integer | YES |  |
| 12 | `gender_name` | varchar | YES |  |
| 13 | `monthly_income` | decimal(16,4) | YES |  |
| 14 | `municipality` | varchar | YES |  |
| 15 | `departament` | varchar | YES |  |
| 16 | `marital_status` | varchar | YES |  |
| 17 | `occupation` | varchar | YES |  |
| 18 | `level_education` | varchar | YES |  |
| 19 | `client_status` | varchar | YES |  |
| 20 | `country` | varchar | YES |  |
| 21 | `fecha_primera_compra` | timestamp(3) | YES |  |
| 22 | `dias_desde_primera_compra` | bigint | YES |  |
| 23 | `type_person_name` | varchar | YES |  |
| 24 | `year` | bigint | YES |  |
| 25 | `month` | bigint | YES |  |
| 26 | `quarter` | bigint | YES |  |
| 27 | `day_of_week` | bigint | YES |  |
| 28 | `day_of_year` | bigint | YES |  |
| 29 | `is_first_purchase` | integer | YES |  |
| 30 | `days_since_first` | bigint | YES |  |
| 31 | `previous_product` | varchar | YES |  |
| 32 | `client_total_purchases` | bigint | YES |  |
| 33 | `client_unique_products` | bigint | YES |  |
| 34 | `client_avg_amount` | double | YES |  |
| 35 | `client_total_amount` | double | YES |  |
| 36 | `client_amount_std` | double | YES |  |
| 37 | `client_first_date` | timestamp(3) | YES |  |
| 38 | `client_last_date` | timestamp(3) | YES |  |
| 39 | `client_lifetime_days` | bigint | YES |  |
| 40 | `client_product_diversity` | double | YES |  |
| 41 | `product_unique_clients` | bigint | YES |  |
| 42 | `product_avg_amount` | double | YES |  |
| 43 | `product_frequency` | bigint | YES |  |
| 44 | `product_avg_sequence` | double | YES |  |
| 45 | `product_sequence_std` | double | YES |  |

### seissa.modelo_datos_who

**Columnas:** 44

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `sequence` | bigint | YES |  |
| 3 | `product_services_id` | integer | YES |  |
| 4 | `contract_date` | timestamp(3) | YES |  |
| 5 | `sale_amount` | double | YES |  |
| 6 | `financed_amount` | double | YES |  |
| 7 | `invoiced_amount` | double | YES |  |
| 8 | `dias_desde_ultima_compra` | bigint | YES |  |
| 9 | `event_tipo` | integer | YES |  |
| 10 | `age` | integer | YES |  |
| 11 | `gender_name` | varchar | YES |  |
| 12 | `monthly_income` | decimal(16,4) | YES |  |
| 13 | `municipality` | varchar | YES |  |
| 14 | `departament` | varchar | YES |  |
| 15 | `marital_status` | varchar | YES |  |
| 16 | `occupation` | varchar | YES |  |
| 17 | `level_education` | varchar | YES |  |
| 18 | `client_status` | varchar | YES |  |
| 19 | `country` | varchar | YES |  |
| 20 | `fecha_primera_compra` | timestamp(3) | YES |  |
| 21 | `dias_desde_primera_compra` | bigint | YES |  |
| 22 | `type_person_name` | varchar | YES |  |
| 23 | `year` | bigint | YES |  |
| 24 | `month` | bigint | YES |  |
| 25 | `quarter` | bigint | YES |  |
| 26 | `day_of_week` | bigint | YES |  |
| 27 | `day_of_year` | bigint | YES |  |
| 28 | `is_first_purchase` | integer | YES |  |
| 29 | `days_since_first` | bigint | YES |  |
| 30 | `previous_product` | varchar | YES |  |
| 31 | `client_total_purchases` | bigint | YES |  |
| 32 | `client_unique_products` | bigint | YES |  |
| 33 | `client_avg_amount` | double | YES |  |
| 34 | `client_total_amount` | double | YES |  |
| 35 | `client_amount_std` | double | YES |  |
| 36 | `client_first_date` | timestamp(3) | YES |  |
| 37 | `client_last_date` | timestamp(3) | YES |  |
| 38 | `client_lifetime_days` | bigint | YES |  |
| 39 | `client_product_diversity` | double | YES |  |
| 40 | `product_unique_clients` | bigint | YES |  |
| 41 | `product_avg_amount` | double | YES |  |
| 42 | `product_frequency` | bigint | YES |  |
| 43 | `product_avg_sequence` | double | YES |  |
| 44 | `product_sequence_std` | double | YES |  |

### seissa.modelo_recompra

**Columnas:** 33

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `vin` | varchar | YES |  |
| 2 | `gama` | varchar | YES |  |
| 3 | `anio_modelo` | varchar | YES |  |
| 4 | `marca` | varchar | YES |  |
| 5 | `combustible` | varchar | YES |  |
| 6 | `clasificacion` | varchar | YES |  |
| 7 | `cantidad` | varchar | YES |  |
| 8 | `valor` | varchar | YES |  |
| 9 | `fechaentregacliente` | varchar | YES |  |
| 10 | `edad` | varchar | YES |  |
| 11 | `sexo` | varchar | YES |  |
| 12 | `fkterceroclases` | varchar | YES |  |
| 13 | `a�o_entrega` | varchar | YES |  |
| 14 | `mes_entrega` | varchar | YES |  |
| 15 | `combustible_std` | varchar | YES |  |
| 16 | `categoria_combustible` | varchar | YES |  |
| 17 | `nivel_emisiones` | varchar | YES |  |
| 18 | `es_electrificado` | varchar | YES |  |
| 19 | `grupo_anio` | varchar | YES |  |
| 20 | `financiado` | varchar | YES |  |
| 21 | `ultimacompra` | varchar | YES |  |
| 22 | `diasdesdeultimacompra` | varchar | YES |  |
| 23 | `clientecompramultiple` | varchar | YES |  |
| 24 | `rebuy_prediction` | varchar | YES |  |
| 25 | `confidence` | varchar | YES |  |
| 26 | `days_prediction` | varchar | YES |  |
| 27 | `score_1` | varchar | YES |  |
| 28 | `gama_1` | varchar | YES |  |
| 29 | `score_2` | varchar | YES |  |
| 30 | `gama_2` | varchar | YES |  |
| 31 | `fecharecompra` | varchar | YES |  |
| 32 | `a�orecompra` | varchar | YES |  |
| 33 | `mesrecompra` | varchar | YES |  |

### seissa.motorysa_predictions

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `last_purchase_date` | date | YES |  |
| 3 | `days_since_last_purchase` | integer | YES |  |
| 4 | `total_purchases` | integer | YES |  |
| 5 | `total_spent` | real | YES |  |
| 6 | `last_product` | integer | YES |  |
| 7 | `unique_products` | integer | YES |  |
| 8 | `avg_days_between_purchases` | real | YES |  |
| 9 | `age` | varchar | YES |  |
| 10 | `gender` | varchar | YES |  |
| 11 | `city` | varchar | YES |  |
| 12 | `predicted_product` | integer | YES |  |
| 13 | `probability` | real | YES |  |
| 14 | `empresa_origen` | varchar | YES |  |
| 15 | `timestamp` | date | YES |  |

### seissa.productos_clientes_compartidos

**Columnas:** 6

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `cantidad` | bigint | YES |  |
| 2 | `product_service_id` | integer | YES |  |
| 3 | `company_id` | integer | YES |  |
| 4 | `llave` | integer | YES |  |
| 5 | `tipollave` | varchar(50) | YES |  |
| 6 | `company_name` | varchar | YES |  |

### seissa.promotec_predictions

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `last_purchase_date` | date | YES |  |
| 3 | `days_since_last_purchase` | integer | YES |  |
| 4 | `total_purchases` | integer | YES |  |
| 5 | `total_spent` | real | YES |  |
| 6 | `last_product` | integer | YES |  |
| 7 | `unique_products` | integer | YES |  |
| 8 | `avg_days_between_purchases` | real | YES |  |
| 9 | `age` | varchar | YES |  |
| 10 | `gender` | varchar | YES |  |
| 11 | `city` | varchar | YES |  |
| 12 | `predicted_product` | integer | YES |  |
| 13 | `probability` | real | YES |  |
| 14 | `empresa_origen` | varchar | YES |  |
| 15 | `timestamp` | date | YES |  |

### seissa.seissa_client_financial_profile

**Columnas:** 32

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `identification` | varchar | YES |  |
| 3 | `age` | integer | YES |  |
| 4 | `genero` | varchar | YES |  |
| 5 | `estado_civil` | varchar | YES |  |
| 6 | `ingreso_mensual` | decimal(16,4) | YES |  |
| 7 | `ciudad` | varchar | YES |  |
| 8 | `departamento` | varchar | YES |  |
| 9 | `total_empresas` | bigint | YES |  |
| 10 | `total_productos` | bigint | YES |  |
| 11 | `productos_ultimo_ano` | bigint | YES |  |
| 12 | `ultima_interaccion` | timestamp(3) | YES |  |
| 13 | `dias_ultima_interaccion` | bigint | YES |  |
| 14 | `total_contratos` | bigint | YES |  |
| 15 | `total_ventas` | decimal(38,4) | YES |  |
| 16 | `promedio_venta` | decimal(19,4) | YES |  |
| 17 | `mayor_venta` | decimal(19,4) | YES |  |
| 18 | `menor_venta` | decimal(19,4) | YES |  |
| 19 | `total_financiado` | decimal(38,4) | YES |  |
| 20 | `promedio_financiado` | decimal(19,4) | YES |  |
| 21 | `total_facturado` | decimal(38,4) | YES |  |
| 22 | `promedio_facturado` | decimal(19,4) | YES |  |
| 23 | `porcentaje_financiacion` | decimal(38,4) | YES |  |
| 24 | `valor_promedio_por_contrato` | decimal(38,4) | YES |  |
| 25 | `ventas_ultimo_ano` | decimal(38,4) | YES |  |
| 26 | `ventas_ultimos_6_meses` | decimal(38,4) | YES |  |
| 27 | `ventas_ultimos_3_meses` | decimal(38,4) | YES |  |
| 28 | `contratos_ultimo_ano` | bigint | YES |  |
| 29 | `ultimo_contrato_fecha` | timestamp(3) | YES |  |
| 30 | `primer_contrato_fecha` | timestamp(3) | YES |  |
| 31 | `dias_ultimo_contrato` | bigint | YES |  |
| 32 | `dias_como_cliente_financiero` | bigint | YES |  |

### seissa.seissa_product_pricing_summary

**Columnas:** 17

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `empresa` | varchar | YES |  |
| 2 | `producto` | varchar | YES |  |
| 3 | `total_ventas` | bigint | YES |  |
| 4 | `clientes_unicos` | bigint | YES |  |
| 5 | `precio_medio_efectivo` | decimal(20,4) | YES |  |
| 6 | `precio_medio_venta` | decimal(20,4) | YES |  |
| 7 | `precio_medio_financiado` | decimal(20,4) | YES |  |
| 8 | `precio_medio_facturado` | decimal(20,4) | YES |  |
| 9 | `precio_minimo` | decimal(20,4) | YES |  |
| 10 | `precio_maximo` | decimal(20,4) | YES |  |
| 11 | `desviacion_estandar` | double | YES |  |
| 12 | `volumen_total` | decimal(38,4) | YES |  |
| 13 | `primera_venta` | timestamp(3) | YES |  |
| 14 | `ultima_venta` | timestamp(3) | YES |  |
| 15 | `ventas_directas` | bigint | YES |  |
| 16 | `ventas_financiadas` | bigint | YES |  |
| 17 | `ventas_facturadas` | bigint | YES |  |

### seissa.seissa_product_transition_matrix

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `empresa_origen` | varchar | YES |  |
| 2 | `producto_origen` | varchar | YES |  |
| 3 | `producto_origen_id` | integer | YES |  |
| 4 | `precio_medio_origen` | decimal(19,4) | YES |  |
| 5 | `empresa_destino` | varchar | YES |  |
| 6 | `producto_destino` | varchar | YES |  |
| 7 | `producto_destino_id` | integer | YES |  |
| 8 | `precio_medio_destino` | decimal(19,4) | YES |  |
| 9 | `frecuencia_transicion` | bigint | YES |  |
| 10 | `clientes_unicos` | bigint | YES |  |
| 11 | `dias_promedio_entre_compras` | double | YES |  |
| 12 | `probabilidad_transicion` | double | YES |  |
| 13 | `es_auto_loop` | integer | YES |  |
| 14 | `es_estado_terminal` | integer | YES |  |
| 15 | `total_transiciones_desde_origen` | bigint | YES |  |

### seissa.tb_historico_trazabilidadcliente

**Columnas:** 7

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `numeroid` | varchar | YES |  |
| 2 | `compa�ia` | varchar | YES |  |
| 3 | `fechavinculo` | date | YES |  |
| 4 | `vigencia` | varchar | YES |  |
| 5 | `compartido` | integer | YES |  |
| 6 | `mescorte` | varchar | YES |  |
| 7 | `a�ocorte` | varchar | YES |  |

### seissa.tb_historico_trazabilidadproducto

**Columnas:** 13

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `compa�ia` | varchar | YES |  |
| 2 | `numeroid` | varchar | YES |  |
| 3 | `fechaproductoservicio` | date | YES |  |
| 4 | `numerocontrato` | varchar | YES |  |
| 5 | `nombreproductoservicio` | varchar | YES |  |
| 6 | `productohomologado` | varchar | YES |  |
| 7 | `productohomologado2` | varchar | YES |  |
| 8 | `vigenciaproductoservicio` | varchar | YES |  |
| 9 | `montoproductoservicio` | decimal(18,2) | YES |  |
| 10 | `fechaactualizacionvigencia` | date | YES |  |
| 11 | `vehiculo` | decimal(18,2) | YES |  |
| 12 | `mescorte` | varchar | YES |  |
| 13 | `a�ocorte` | varchar | YES |  |

### seissa.tb_historico_trazabilidadvehiculo

**Columnas:** 9

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `placa` | varchar | YES |  |
| 2 | `vin` | varchar | YES |  |
| 3 | `compania` | varchar | YES |  |
| 4 | `concepto` | varchar | YES |  |
| 5 | `fechavinculo` | date | YES |  |
| 6 | `numeroid` | varchar | YES |  |
| 7 | `compartido` | integer | YES |  |
| 8 | `mescorte` | varchar | YES |  |
| 9 | `a�ocorte` | varchar | YES |  |

### seissa.view_clientes

**Columnas:** 43

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `identification` | varchar | YES |  |
| 3 | `type_id` | integer | YES |  |
| 4 | `type_person_id` | integer | YES |  |
| 5 | `type_person_name` | varchar | YES |  |
| 6 | `name` | varchar | YES |  |
| 7 | `status_id` | integer | YES |  |
| 8 | `gender_id` | integer | YES |  |
| 9 | `gender_name` | varchar | YES |  |
| 10 | `marital_id` | integer | YES |  |
| 11 | `marital_status` | varchar | YES |  |
| 12 | `education_id` | integer | YES |  |
| 13 | `name_education` | varchar | YES |  |
| 14 | `economic_id` | integer | YES |  |
| 15 | `homolagation_economic` | varchar | YES |  |
| 16 | `sector` | varchar | YES |  |
| 17 | `category_economic` | varchar | YES |  |
| 18 | `monthly_income` | decimal(16,4) | YES |  |
| 19 | `occupation_id` | integer | YES |  |
| 20 | `homologation_occupation` | varchar | YES |  |
| 21 | `occupation` | varchar | YES |  |
| 22 | `category_occupation` | varchar | YES |  |
| 23 | `city_id` | integer | YES |  |
| 24 | `area_code_id` | integer | YES |  |
| 25 | `code` | integer | YES |  |
| 26 | `cli_ph_id` | integer | YES |  |
| 27 | `company_id` | integer | YES |  |
| 28 | `linking_date` | timestamp(3) | YES |  |
| 29 | `status_linking` | smallint | YES |  |
| 30 | `cli_ph_id_adress` | integer | YES |  |
| 31 | `address_id` | integer | YES |  |
| 32 | `address` | varchar | YES |  |
| 33 | `cli_em_id` | integer | YES |  |
| 34 | `email_id` | integer | YES |  |
| 35 | `email` | varchar | YES |  |
| 36 | `phone_id` | integer | YES |  |
| 37 | `phone_number` | varchar | YES |  |
| 38 | `date_of_birth` | date | YES |  |
| 39 | `age` | integer | YES |  |
| 40 | `people_in_charge` | integer | YES |  |
| 41 | `code_country_id` | integer | YES |  |
| 42 | `load_data` | timestamp(3) | YES |  |
| 43 | `update_data` | timestamp(3) | YES |  |

### seissa.view_productos

**Columnas:** 18

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `product_id` | integer | YES |  |
| 2 | `company_id` | integer | YES |  |
| 3 | `contract_id` | integer | YES |  |
| 4 | `product_service_id` | integer | YES |  |
| 5 | `insurance_id` | integer | YES |  |
| 6 | `company` | varchar | YES |  |
| 7 | `homologated_product_name` | varchar | YES |  |
| 8 | `homologated_product_id` | integer | YES |  |
| 9 | `product_name` | varchar | YES |  |
| 10 | `homologated_product_2` | varchar | YES |  |
| 11 | `contract_number` | varchar | YES |  |
| 12 | `status_id` | integer | YES |  |
| 13 | `status` | boolean | YES |  |
| 14 | `status_name` | varchar | YES |  |
| 15 | `sale_amount` | decimal(19,4) | YES |  |
| 16 | `financed_amount` | decimal(19,4) | YES |  |
| 17 | `invoiced_amount` | decimal(19,4) | YES |  |
| 18 | `contract_date` | timestamp(3) | YES |  |

### seissa.view_vehiculos

**Columnas:** 36

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `vehicle_id` | integer | YES |  |
| 2 | `plate_name` | varchar | YES |  |
| 3 | `vin` | varchar | YES |  |
| 4 | `fasecolda_code` | varchar | YES |  |
| 5 | `year_model` | varchar | YES |  |
| 6 | `cli_veh_id` | integer | YES |  |
| 7 | `company_id` | integer | YES |  |
| 8 | `linking_date` | timestamp(3) | YES |  |
| 9 | `status_linking` | smallint | YES |  |
| 10 | `client_id` | integer | YES |  |
| 11 | `reference_id` | integer | YES |  |
| 12 | `reference` | varchar | YES |  |
| 13 | `homologated_reference` | varchar | YES |  |
| 14 | `engine_displacement` | integer | YES |  |
| 15 | `price` | decimal(18,2) | YES |  |
| 16 | `mileage` | double | YES |  |
| 17 | `brand_id` | integer | YES |  |
| 18 | `brand` | varchar | YES |  |
| 19 | `homologated_brand` | varchar | YES |  |
| 20 | `class_id` | integer | YES |  |
| 21 | `class` | varchar | YES |  |
| 22 | `homologated_class` | varchar | YES |  |
| 23 | `consolidated_class` | varchar | YES |  |
| 24 | `body_car` | varchar | YES |  |
| 25 | `body_id` | integer | YES |  |
| 26 | `service_id` | integer | YES |  |
| 27 | `service` | varchar | YES |  |
| 28 | `condition_id` | integer | YES |  |
| 29 | `condition_name` | varchar | YES |  |
| 30 | `fuel_id` | integer | YES |  |
| 31 | `fuel` | varchar | YES |  |
| 32 | `homologated_fuel` | varchar | YES |  |
| 33 | `city_id` | integer | YES |  |
| 34 | `color_id` | integer | YES |  |
| 35 | `date_load` | timestamp(3) | YES |  |
| 36 | `mark_casatoro` | integer | YES |  |

### seissa.vista_datos_secuenciados

**Columnas:** 17

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `product_services_id` | integer | YES |  |
| 3 | `numero_compra` | bigint | YES |  |
| 4 | `producto_origen_id` | integer | YES |  |
| 5 | `contract_date` | timestamp(3) | YES |  |
| 6 | `dias_proxima_compra` | bigint | YES |  |
| 7 | `sale_amount` | varchar | YES |  |
| 8 | `financed_amount` | varchar | YES |  |
| 9 | `invoiced_amount` | varchar | YES |  |
| 10 | `dias_desde_ultima_compra` | bigint | YES |  |
| 11 | `event_tipo` | integer | YES |  |
| 12 | `age` | integer | YES |  |
| 13 | `gender_name` | varchar | YES |  |
| 14 | `monthly_income` | decimal(16,4) | YES |  |
| 15 | `municipality` | varchar | YES |  |
| 16 | `secuencia` | bigint | YES |  |
| 17 | `target_id` | integer | YES |  |

### seissa.vista_ecosistema_agent

**Columnas:** 28

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `product_services_id` | integer | YES |  |
| 3 | `product_name` | varchar | YES |  |
| 4 | `company` | varchar | YES |  |
| 5 | `company_id` | integer | YES |  |
| 6 | `contract_date` | date | YES |  |
| 7 | `total_compras` | bigint | YES |  |
| 8 | `producto_origen_id` | integer | YES |  |
| 9 | `producto_origen_name` | varchar | YES |  |
| 10 | `producto_origen_company` | varchar | YES |  |
| 11 | `target_id` | integer | YES |  |
| 12 | `dias_entre_compras` | bigint | YES |  |
| 13 | `dias_desde_ultima_compra` | bigint | YES |  |
| 14 | `sale_amount` | double | YES |  |
| 15 | `financed_amount` | double | YES |  |
| 16 | `invoiced_amount` | double | YES |  |
| 17 | `monto_total` | double | YES |  |
| 18 | `age` | integer | YES |  |
| 19 | `gender_name` | varchar | YES |  |
| 20 | `municipality` | varchar | YES |  |
| 21 | `departament` | varchar | YES |  |
| 22 | `country` | varchar | YES |  |
| 23 | `marital_status` | varchar | YES |  |
| 24 | `occupation` | varchar | YES |  |
| 25 | `level_education` | varchar | YES |  |
| 26 | `client_status` | varchar | YES |  |
| 27 | `fecha_primera_compra` | date | YES |  |
| 28 | `dias_desde_primera_compra` | bigint | YES |  |

### seissa.vw_inf_logos_clientes

**Columnas:** 5

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `compania` | varchar | YES |  |
| 2 | `compartido` | varchar(10) | YES |  |
| 3 | `clientes_unicos` | bigint | YES |  |
| 4 | `total_clientes` | bigint | YES |  |
| 5 | `fecha_vinculo` | varchar | YES |  |

### seissa.vw_inf_logos_vehiculos

**Columnas:** 5

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `compania` | varchar | YES |  |
| 2 | `compartido` | varchar(10) | YES |  |
| 3 | `vehiculos_unicos` | bigint | YES |  |
| 4 | `total_vehiculos` | bigint | YES |  |
| 5 | `fecha_vinculo` | varchar | YES |  |

### seissa.vw_inf_matrices

**Columnas:** 4

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `company` | varchar | YES |  |
| 2 | `producto` | varchar | YES |  |
| 3 | `clientes` | bigint | YES |  |
| 4 | `contratos` | bigint | YES |  |

### seissa.vw_productos_compartidos

**Columnas:** 14

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `numeroid` | varchar | YES |  |
| 2 | `anio_corte` | varchar | YES |  |
| 3 | `mes_corte` | varchar | YES |  |
| 4 | `date_concept` | timestamp(3) | YES |  |
| 5 | `status_linking_origen` | varchar | YES |  |
| 6 | `company_name_origen` | varchar | YES |  |
| 7 | `homologated_product_name_origen` | varchar | YES |  |
| 8 | `product_name_origen` | varchar | YES |  |
| 9 | `company_name_compartido` | varchar | YES |  |
| 10 | `homologated_product_name_compartido` | varchar | YES |  |
| 11 | `product_name_compartido` | varchar | YES |  |
| 12 | `clientes_en_comun` | bigint | YES |  |
| 13 | `total_productos_compania` | bigint | YES |  |
| 14 | `total_productos_compania_compartida` | bigint | YES |  |

### seissa.vw_productos_compartidos_prueba

**Columnas:** 10

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `numeroid` | varchar | YES |  |
| 2 | `anio_corte` | varchar | YES |  |
| 3 | `mes_corte` | varchar | YES |  |
| 4 | `status_linking_origen` | varchar | YES |  |
| 5 | `company_name_origen` | varchar | YES |  |
| 6 | `homologated_product_name_origen` | varchar | YES |  |
| 7 | `product_name_origen` | varchar | YES |  |
| 8 | `clientes_en_comun` | bigint | YES |  |
| 9 | `total_productos_compania` | bigint | YES |  |
| 10 | `registros` | bigint | YES |  |

### seissa.vw_trazabilidad_cliente

**Columnas:** 5

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `numeroid` | varchar | YES |  |
| 2 | `compania` | varchar | YES |  |
| 3 | `fechavinculo` | timestamp(3) | YES |  |
| 4 | `vigencia` | integer | YES |  |
| 5 | `compartido` | integer | YES |  |

### seissa.vw_trazabilidad_producto

**Columnas:** 11

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `compania` | varchar | YES |  |
| 2 | `numeroid` | varchar | YES |  |
| 3 | `fechaproductoservicio` | date | YES |  |
| 4 | `numerocontrato` | varchar | YES |  |
| 5 | `nombreproductoservicio` | varchar | YES |  |
| 6 | `productohomologado` | varchar | YES |  |
| 7 | `productohomologado2` | varchar | YES |  |
| 8 | `vigenciaproductoservicio` | varchar | YES |  |
| 9 | `montoproductoservicio` | decimal(38,4) | YES |  |
| 10 | `fechaactualizacionvigencia` | date | YES |  |
| 11 | `vehiculo` | integer | YES |  |

### seissa.vw_trazabilidad_vehiculo

**Columnas:** 7

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `placa` | varchar | YES |  |
| 2 | `vin` | varchar | YES |  |
| 3 | `compania` | varchar | YES |  |
| 4 | `concepto` | varchar | YES |  |
| 5 | `fechavinculo` | date | YES |  |
| 6 | `numeroid` | varchar | YES |  |
| 7 | `compartido` | integer | YES |  |

## 🥉 seissa-analytics

`Capa: Bronce / Raw`

### seissa-analytics.modelo_datos_bi_068c762d1b304dd5cc2a0d34f267a1a5

**Columnas:** 1

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `partition_0` | varchar | YES |  |

### seissa-analytics.seissa_client_financial_profile

**Columnas:** 1

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `partition_0` | varchar | YES |  |

### seissa-analytics.seissa_product_pricing_summary

**Columnas:** 1

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `partition_0` | varchar | YES |  |

### seissa-analytics.seissa_product_transition_matrix

**Columnas:** 1

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `partition_0` | varchar | YES |  |

## 🥈 seissa_materialized_data

`Capa: Plata / Materialized`

### seissa_materialized_data.categorias_seissa

**Columnas:** 9

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `product_services_id` | integer | YES |  |
| 2 | `product_name` | varchar | YES |  |
| 3 | `homologated_product_id` | integer | YES |  |
| 4 | `homologated_product_name` | varchar | YES |  |
| 5 | `homologated_product_2` | varchar | YES |  |
| 6 | `company_id` | integer | YES |  |
| 7 | `categoria` | varchar | YES |  |
| 8 | `sub_categoria` | varchar | YES |  |
| 9 | `productos` | varchar | YES |  |

### seissa_materialized_data.client_predictions

**Columnas:** 22

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `last_purchase_date` | date | YES |  |
| 3 | `days_since_last_purchase` | integer | YES |  |
| 4 | `total_purchases` | integer | YES |  |
| 5 | `total_spent` | double | YES |  |
| 6 | `predicted_product_1` | integer | YES |  |
| 7 | `probability_1` | double | YES |  |
| 8 | `predicted_product_2` | integer | YES |  |
| 9 | `probability_2` | double | YES |  |
| 10 | `predicted_product_3` | integer | YES |  |
| 11 | `probability_3` | double | YES |  |
| 12 | `predicted_days_to_next` | integer | YES |  |
| 13 | `predicted_purchase_date` | date | YES |  |
| 14 | `will_buy_soon_probability` | double | YES |  |
| 15 | `will_buy_soon` | varchar | YES |  |
| 16 | `last_product` | integer | YES |  |
| 17 | `most_frequent_product` | integer | YES |  |
| 18 | `unique_products` | integer | YES |  |
| 19 | `avg_days_between_purchases` | double | YES |  |
| 20 | `age` | double | YES |  |
| 21 | `gender` | varchar | YES |  |
| 22 | `city` | varchar | YES |  |

### seissa_materialized_data.cliente_producto_id_a

**Columnas:** 3

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `product_service_id` | integer | YES |  |
| 3 | `product_name` | varchar | YES |  |

### seissa_materialized_data.cliente_producto_id_h

**Columnas:** 6

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `numeroid` | varchar | YES |  |
| 2 | `product_services_id` | integer | YES |  |
| 3 | `company_id` | integer | YES |  |
| 4 | `status_linking` | varchar | YES |  |
| 5 | `mescorte` | varchar | YES |  |
| 6 | `anocorte` | varchar | YES |  |

### seissa_materialized_data.clientes_compartidos

**Columnas:** 3

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `compa�ia` | varchar | YES |  |
| 2 | `compa�ia_compartida` | varchar | YES |  |
| 3 | `cantidad` | bigint | YES |  |

### seissa_materialized_data.clientes_por_producto_a

**Columnas:** 4

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `cant_products` | bigint | YES |  |
| 2 | `client_id` | integer | YES |  |
| 3 | `cantidad_clientes_unicos` | integer | YES |  |
| 4 | `cantidad_vehiculos` | bigint | YES |  |

### seissa_materialized_data.clientes_por_producto_h

**Columnas:** 6

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `cant_products` | bigint | YES |  |
| 2 | `client_id` | varchar | YES |  |
| 3 | `cantidad_clientes_unicos` | integer | YES |  |
| 4 | `cantidad_vehiculos` | bigint | YES |  |
| 5 | `mescorte` | varchar | YES |  |
| 6 | `anocorte` | varchar | YES |  |

### seissa_materialized_data.historico_clientes_compartidos

**Columnas:** 5

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `compa�ia` | varchar | YES |  |
| 2 | `compa�ia_compartida` | varchar | YES |  |
| 3 | `mescorte` | varchar | YES |  |
| 4 | `a�ocorte` | varchar | YES |  |
| 5 | `cantidad` | bigint | YES |  |

### seissa_materialized_data.historico_trazabilidad_cliente

**Columnas:** 29

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `numeroid` | varchar | YES |  |
| 2 | `company_name` | varchar | YES |  |
| 3 | `linking_date` | date | YES |  |
| 4 | `status_linking` | varchar | YES |  |
| 5 | `compartido` | integer | YES |  |
| 6 | `mescorte` | varchar | YES |  |
| 7 | `anocorte` | varchar | YES |  |
| 8 | `gender` | varchar | YES |  |
| 9 | `marital_status` | varchar | YES |  |
| 10 | `education_level` | varchar | YES |  |
| 11 | `economic_sector_homologation` | varchar | YES |  |
| 12 | `economic_sector` | varchar | YES |  |
| 13 | `economic_sector_category` | varchar | YES |  |
| 14 | `occupation_homologation` | varchar | YES |  |
| 15 | `occupation` | varchar | YES |  |
| 16 | `occupation_category` | varchar | YES |  |
| 17 | `type_person` | varchar | YES |  |
| 18 | `type_identification` | varchar | YES |  |
| 19 | `name` | varchar | YES |  |
| 20 | `age` | integer | YES |  |
| 21 | `date_of_birth` | date | YES |  |
| 22 | `code` | integer | YES |  |
| 23 | `address` | varchar | YES |  |
| 24 | `email` | varchar | YES |  |
| 25 | `phone_number` | varchar | YES |  |
| 26 | `departament` | varchar | YES |  |
| 27 | `municipality` | varchar | YES |  |
| 28 | `latitude_municipality` | varchar | YES |  |
| 29 | `longitude_municipality` | varchar | YES |  |

### seissa_materialized_data.matriz_productos_compartidos_general

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `empresa_origen` | varchar | YES |  |
| 2 | `carfiao_productos` | bigint | YES |  |
| 3 | `bellpi_productos` | bigint | YES |  |
| 4 | `equirent_productos` | bigint | YES |  |
| 5 | `finandina_productos` | bigint | YES |  |
| 6 | `bonaparte_productos` | bigint | YES |  |
| 7 | `casatoro_productos` | bigint | YES |  |
| 8 | `promotec_productos` | bigint | YES |  |
| 9 | `simon_productos` | bigint | YES |  |
| 10 | `motorysa_productos` | bigint | YES |  |
| 11 | `finanzauto_productos` | bigint | YES |  |
| 12 | `total_productos` | bigint | YES |  |

### seissa_materialized_data.matriz_productos_compartidos_mensual_dc

**Columnas:** 14

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `anio` | integer | YES |  |
| 2 | `mes` | integer | YES |  |
| 3 | `empresa_origen` | varchar | YES |  |
| 4 | `carfiao_productos` | bigint | YES |  |
| 5 | `bellpi_productos` | bigint | YES |  |
| 6 | `equirent_productos` | bigint | YES |  |
| 7 | `finandina_productos` | bigint | YES |  |
| 8 | `bonaparte_productos` | bigint | YES |  |
| 9 | `casatoro_productos` | bigint | YES |  |
| 10 | `promotec_productos` | bigint | YES |  |
| 11 | `simon_productos` | bigint | YES |  |
| 12 | `motorysa_productos` | bigint | YES |  |
| 13 | `finanzauto_productos` | bigint | YES |  |
| 14 | `total_productos` | bigint | YES |  |

### seissa_materialized_data.matriz_productos_compartidos_mensual_df

**Columnas:** 14

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `anocorte` | varchar | YES |  |
| 2 | `mescorte` | varchar | YES |  |
| 3 | `empresa_origen` | varchar | YES |  |
| 4 | `carfiao_productos` | bigint | YES |  |
| 5 | `bellpi_productos` | bigint | YES |  |
| 6 | `equirent_productos` | bigint | YES |  |
| 7 | `finandina_productos` | bigint | YES |  |
| 8 | `bonaparte_productos` | bigint | YES |  |
| 9 | `casatoro_productos` | bigint | YES |  |
| 10 | `promotec_productos` | bigint | YES |  |
| 11 | `simon_productos` | bigint | YES |  |
| 12 | `motorysa_productos` | bigint | YES |  |
| 13 | `finanzauto_productos` | bigint | YES |  |
| 14 | `total_productos` | bigint | YES |  |

### seissa_materialized_data.p_historico_trazabilidad_producto

**Columnas:** 17

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `numeroid` | varchar | YES |  |
| 2 | `company_name` | varchar | YES |  |
| 3 | `fechaproductoservicio` | date | YES |  |
| 4 | `status_linking` | varchar | YES |  |
| 5 | `mescorte` | varchar | YES |  |
| 6 | `anocorte` | varchar | YES |  |
| 7 | `numerocontrato` | varchar | YES |  |
| 8 | `nombreproductoservicio` | varchar | YES |  |
| 9 | `productohomologado` | varchar | YES |  |
| 10 | `productohomologado2` | varchar | YES |  |
| 11 | `montoproductoservicio` | decimal(18,2) | YES |  |
| 12 | `fechaactualizacionvigencia` | date | YES |  |
| 13 | `vehiculo` | decimal(18,2) | YES |  |
| 14 | `llave_producto` | varchar | YES |  |
| 15 | `company_id` | integer | YES |  |
| 16 | `product_services_id` | integer | YES |  |
| 17 | `homologated_product_id` | integer | YES |  |

### seissa_materialized_data.productos_clientes_compartidos

**Columnas:** 6

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `cantidad` | bigint | YES |  |
| 2 | `product_service_id` | integer | YES |  |
| 3 | `company_id` | integer | YES |  |
| 4 | `llave` | integer | YES |  |
| 5 | `tipollave` | varchar | YES |  |
| 6 | `company_name` | varchar | YES |  |

### seissa_materialized_data.productos_compartidos

**Columnas:** 16

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `numeroid` | varchar | YES |  |
| 2 | `compania_origen` | varchar | YES |  |
| 3 | `producto_origen` | varchar | YES |  |
| 4 | `mescorte` | varchar | YES |  |
| 5 | `anocorte` | varchar | YES |  |
| 6 | `status_linking_origen` | varchar | YES |  |
| 7 | `date_concept_origen` | timestamp(3) | YES |  |
| 8 | `compania_compartida` | varchar | YES |  |
| 9 | `mes_compartido` | varchar | YES |  |
| 10 | `ano_compartido` | varchar | YES |  |
| 11 | `producto_compartido` | varchar | YES |  |
| 12 | `status_linking_compartido` | varchar | YES |  |
| 13 | `date_concept_compartido` | timestamp(3) | YES |  |
| 14 | `cantidad_empresa` | bigint | YES |  |
| 15 | `cantidad_compartida` | bigint | YES |  |
| 16 | `total_productos` | bigint | YES |  |

### seissa_materialized_data.productos_compartidos_general

**Columnas:** 5

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `empresa_origen` | varchar | YES |  |
| 2 | `producto_origen` | varchar | YES |  |
| 3 | `homologated_product_name` | varchar | YES |  |
| 4 | `homologated_product_2` | varchar | YES |  |
| 5 | `empresa_compartida` | varchar | YES |  |

### seissa_materialized_data.productos_compartidos_mensual_dc

**Columnas:** 7

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `anio` | integer | YES |  |
| 2 | `mes` | integer | YES |  |
| 3 | `empresa_origen` | varchar | YES |  |
| 4 | `producto_origen` | varchar | YES |  |
| 5 | `homologated_product_name` | varchar | YES |  |
| 6 | `homologated_product_2` | varchar | YES |  |
| 7 | `empresa_compartida` | varchar | YES |  |

### seissa_materialized_data.productos_compartidos_mensual_fc

**Columnas:** 7

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `anocorte` | varchar | YES |  |
| 2 | `mescorte` | varchar | YES |  |
| 3 | `empresa_origen` | varchar | YES |  |
| 4 | `producto_origen` | varchar | YES |  |
| 5 | `homologated_product_name` | varchar | YES |  |
| 6 | `homologated_product_2` | varchar | YES |  |
| 7 | `empresa_compartida` | varchar | YES |  |

### seissa_materialized_data.productos_compartidos_v2

**Columnas:** 19

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `numeroid` | varchar | YES |  |
| 2 | `cliente_unico` | integer | YES |  |
| 3 | `cliente_unico_periodo` | integer | YES |  |
| 4 | `cliente_unico_periodo_activo` | integer | YES |  |
| 5 | `cliente_unico_periodo_dc` | integer | YES |  |
| 6 | `cliente_unico_periodo_dc_activo` | integer | YES |  |
| 7 | `compania_origen` | varchar | YES |  |
| 8 | `producto_origen` | varchar | YES |  |
| 9 | `homologated_product_2` | varchar | YES |  |
| 10 | `homologated_product_name` | varchar | YES |  |
| 11 | `mescorte` | varchar | YES |  |
| 12 | `anocorte` | varchar | YES |  |
| 13 | `date_concept_origen` | timestamp(3) | YES |  |
| 14 | `anio_compra` | integer | YES |  |
| 15 | `mes_compra` | integer | YES |  |
| 16 | `productos_cliente` | integer | YES |  |
| 17 | `productos_periodo` | integer | YES |  |
| 18 | `productos_periodo_dc` | integer | YES |  |
| 19 | `total` | bigint | YES |  |

### seissa_materialized_data.productos_nombres

**Columnas:** 6

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `product_services_id` | integer | YES |  |
| 2 | `product_name` | varchar | YES |  |
| 3 | `homologated_product_id` | integer | YES |  |
| 4 | `homologated_product_name` | varchar | YES |  |
| 5 | `homologated_product_2` | varchar | YES |  |
| 6 | `company_id` | integer | YES |  |

### seissa_materialized_data.sin_productos

**Columnas:** 4

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `company_id` | integer | YES |  |
| 3 | `product_service_id` | integer | YES |  |
| 4 | `client_id_product` | integer | YES |  |

### seissa_materialized_data.tb_historico_trazabilidadvehiculo_def

**Columnas:** 26

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `placa` | varchar | YES |  |
| 2 | `vin` | varchar | YES |  |
| 3 | `compania` | varchar | YES |  |
| 4 | `concepto` | varchar | YES |  |
| 5 | `fechavinculo` | date | YES |  |
| 6 | `numeroid` | varchar | YES |  |
| 7 | `compartido` | integer | YES |  |
| 8 | `mescorte` | varchar | YES |  |
| 9 | `a�ocorte` | varchar | YES |  |
| 10 | `id_vehiculo` | varchar | YES |  |
| 11 | `fasecolda_code` | varchar | YES |  |
| 12 | `year_model` | varchar | YES |  |
| 13 | `price` | decimal(18,2) | YES |  |
| 14 | `mileage` | double | YES |  |
| 15 | `date_load` | timestamp(3) | YES |  |
| 16 | `brand_name` | varchar | YES |  |
| 17 | `color_name` | varchar | YES |  |
| 18 | `class_name` | varchar | YES |  |
| 19 | `homologated_class` | varchar | YES |  |
| 20 | `consolidated_class` | varchar | YES |  |
| 21 | `body_car` | varchar | YES |  |
| 22 | `condition_name` | varchar | YES |  |
| 23 | `fuel_name` | varchar | YES |  |
| 24 | `reference_name` | varchar | YES |  |
| 25 | `homologated_reference` | varchar | YES |  |
| 26 | `service_name` | varchar | YES |  |

### seissa_materialized_data.tb_trazabilidad_cliente_completo

**Columnas:** 31

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `numeroid` | varchar | YES |  |
| 2 | `compa�ia` | varchar | YES |  |
| 3 | `fechavinculo` | date | YES |  |
| 4 | `vigencia` | varchar | YES |  |
| 5 | `compartido` | integer | YES |  |
| 6 | `gender` | varchar | YES |  |
| 7 | `marital_status` | varchar | YES |  |
| 8 | `education_level` | varchar | YES |  |
| 9 | `economic_sector_homologation` | varchar | YES |  |
| 10 | `economic_sector` | varchar | YES |  |
| 11 | `economic_sector_category` | varchar | YES |  |
| 12 | `occupation_homologation` | varchar | YES |  |
| 13 | `occupation` | varchar | YES |  |
| 14 | `occupation_category` | varchar | YES |  |
| 15 | `type_person` | varchar | YES |  |
| 16 | `type_identification` | varchar | YES |  |
| 17 | `name` | varchar | YES |  |
| 18 | `age` | integer | YES |  |
| 19 | `date_of_birth` | date | YES |  |
| 20 | `code` | integer | YES |  |
| 21 | `address` | varchar | YES |  |
| 22 | `email` | varchar | YES |  |
| 23 | `phone_number` | varchar | YES |  |
| 24 | `departament` | varchar | YES |  |
| 25 | `municipality` | varchar | YES |  |
| 26 | `latitude_municipality` | varchar | YES |  |
| 27 | `longitude_municipality` | varchar | YES |  |
| 28 | `mescorte` | integer | YES |  |
| 29 | `anocorte` | integer | YES |  |
| 30 | `tabla` | varchar | YES |  |
| 31 | `company_id` | integer | YES |  |

### seissa_materialized_data.tb_trazabilidadcliente

**Columnas:** 27

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `numeroid` | varchar | YES |  |
| 2 | `compa�ia` | varchar | YES |  |
| 3 | `fechavinculo` | date | YES |  |
| 4 | `vigencia` | varchar | YES |  |
| 5 | `compartido` | integer | YES |  |
| 6 | `gender` | varchar | YES |  |
| 7 | `marital_status` | varchar | YES |  |
| 8 | `education_level` | varchar | YES |  |
| 9 | `economic_sector_homologation` | varchar | YES |  |
| 10 | `economic_sector` | varchar | YES |  |
| 11 | `economic_sector_category` | varchar | YES |  |
| 12 | `occupation_homologation` | varchar | YES |  |
| 13 | `occupation` | varchar | YES |  |
| 14 | `occupation_category` | varchar | YES |  |
| 15 | `type_person` | varchar | YES |  |
| 16 | `type_identification` | varchar | YES |  |
| 17 | `name` | varchar | YES |  |
| 18 | `age` | integer | YES |  |
| 19 | `date_of_birth` | date | YES |  |
| 20 | `code` | integer | YES |  |
| 21 | `address` | varchar | YES |  |
| 22 | `email` | varchar | YES |  |
| 23 | `phone_number` | varchar | YES |  |
| 24 | `departament` | varchar | YES |  |
| 25 | `municipality` | varchar | YES |  |
| 26 | `latitude_municipality` | varchar | YES |  |
| 27 | `longitude_municipality` | varchar | YES |  |

### seissa_materialized_data.tb_trazabilidadproducto

**Columnas:** 11

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `compa�ia` | varchar | YES |  |
| 2 | `numeroid` | varchar | YES |  |
| 3 | `fechaproductoservicio` | date | YES |  |
| 4 | `numerocontrato` | varchar | YES |  |
| 5 | `nombreproductoservicio` | varchar | YES |  |
| 6 | `productohomologado` | varchar | YES |  |
| 7 | `productohomologado2` | varchar | YES |  |
| 8 | `vigenciaproductoservicio` | varchar | YES |  |
| 9 | `fechaactualizacionvigencia` | date | YES |  |
| 10 | `vehiculo` | integer | YES |  |
| 11 | `montoproductoservicio` | decimal(29,4) | YES |  |

### seissa_materialized_data.tb_trazabilidadvehiculo

**Columnas:** 24

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `placa` | varchar | YES |  |
| 2 | `vin` | varchar | YES |  |
| 3 | `compa�ia` | varchar | YES |  |
| 4 | `concepto` | varchar | YES |  |
| 5 | `fechavinculo` | date | YES |  |
| 6 | `numeroid` | varchar | YES |  |
| 7 | `compartido` | integer | YES |  |
| 8 | `id_vehiculo` | varchar | YES |  |
| 9 | `fasecolda_code` | varchar | YES |  |
| 10 | `year_model` | varchar | YES |  |
| 11 | `price` | decimal(18,2) | YES |  |
| 12 | `mileage` | double | YES |  |
| 13 | `date_load` | timestamp(3) | YES |  |
| 14 | `brand_name` | varchar | YES |  |
| 15 | `color_name` | varchar | YES |  |
| 16 | `class_name` | varchar | YES |  |
| 17 | `homologated_class` | varchar | YES |  |
| 18 | `consolidated_class` | varchar | YES |  |
| 19 | `body_car` | varchar | YES |  |
| 20 | `condition_name` | varchar | YES |  |
| 21 | `fuel_name` | varchar | YES |  |
| 22 | `reference_name` | varchar | YES |  |
| 23 | `homologated_reference` | varchar | YES |  |
| 24 | `service_name` | varchar | YES |  |

### seissa_materialized_data.tbl_inf_logos_clientes

**Columnas:** 5

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `compa�ia` | varchar | YES |  |
| 2 | `compartido` | varchar | YES |  |
| 3 | `clientes_unicos` | bigint | YES |  |
| 4 | `total_clientes` | bigint | YES |  |
| 5 | `fecha_vinculo` | varchar | YES |  |

### seissa_materialized_data.tbl_inf_logos_vehiculos

**Columnas:** 5

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `compa�ia` | varchar | YES |  |
| 2 | `compartido` | varchar | YES |  |
| 3 | `vehiculos_unicos` | bigint | YES |  |
| 4 | `total_vehiculos` | bigint | YES |  |
| 5 | `fecha_vinculo` | varchar | YES |  |

### seissa_materialized_data.tbl_matrices

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `company` | varchar | YES |  |
| 2 | `producto` | varchar | YES |  |
| 3 | `clientes` | integer | YES |  |
| 4 | `contratos` | integer | YES |  |
| 5 | `bellpi` | integer | YES |  |
| 6 | `bonaparte` | integer | YES |  |
| 7 | `carfiao` | integer | YES |  |
| 8 | `casatoro` | integer | YES |  |
| 9 | `equirent` | integer | YES |  |
| 10 | `finandina` | integer | YES |  |
| 11 | `finanzauto` | integer | YES |  |
| 12 | `motorysa` | integer | YES |  |
| 13 | `promotec` | integer | YES |  |
| 14 | `simon` | integer | YES |  |
| 15 | `fecha_vinculo` | varchar | YES |  |

### seissa_materialized_data.trazabilidad_vehiculo

**Columnas:** 24

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `placa` | varchar | YES |  |
| 2 | `vin` | varchar | YES |  |
| 3 | `compa�ia` | varchar | YES |  |
| 4 | `concepto` | varchar | YES |  |
| 5 | `fechavinculo` | date | YES |  |
| 6 | `numeroid` | varchar | YES |  |
| 7 | `compartido` | integer | YES |  |
| 8 | `id_vehiculo` | varchar | YES |  |
| 9 | `fasecolda_code` | varchar | YES |  |
| 10 | `year_model` | varchar | YES |  |
| 11 | `price` | decimal(18,2) | YES |  |
| 12 | `mileage` | double | YES |  |
| 13 | `date_load` | timestamp(3) | YES |  |
| 14 | `brand_name` | varchar | YES |  |
| 15 | `color_name` | varchar | YES |  |
| 16 | `class_name` | varchar | YES |  |
| 17 | `homologated_class` | varchar | YES |  |
| 18 | `consolidated_class` | varchar | YES |  |
| 19 | `body_car` | varchar | YES |  |
| 20 | `condition_name` | varchar | YES |  |
| 21 | `fuel_name` | varchar | YES |  |
| 22 | `reference_name` | varchar | YES |  |
| 23 | `homologated_reference` | varchar | YES |  |
| 24 | `service_name` | varchar | YES |  |

### seissa_materialized_data.v_dim_link_vehicle_company_seissa

**Columnas:** 10

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `placa` | varchar | YES |  |
| 2 | `vin` | varchar | YES |  |
| 3 | `compania` | varchar | YES |  |
| 4 | `company_id` | integer | YES |  |
| 5 | `concepto` | varchar | YES |  |
| 6 | `vehiculo` | varchar | YES |  |
| 7 | `fechavinculo` | date | YES |  |
| 8 | `numeroid` | varchar | YES |  |
| 9 | `client_id` | integer | YES |  |
| 10 | `vigencia` | varchar | YES |  |

### seissa_materialized_data.v_historico_trazabilidadvehiculo

**Columnas:** 29

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `numeroid` | varchar | YES |  |
| 2 | `placa` | varchar | YES |  |
| 3 | `vin` | varchar | YES |  |
| 4 | `company_name` | varchar | YES |  |
| 5 | `concepto` | varchar | YES |  |
| 6 | `linking_date` | date | YES |  |
| 7 | `compartido` | integer | YES |  |
| 8 | `mescorte` | varchar | YES |  |
| 9 | `anocorte` | varchar | YES |  |
| 10 | `id_vehiculo` | varchar | YES |  |
| 11 | `join_key` | varchar | YES |  |
| 12 | `company_id` | integer | YES |  |
| 13 | `vigencia` | varchar | YES |  |
| 14 | `homologated_brand` | varchar | YES |  |
| 15 | `fasecolda_code` | varchar | YES |  |
| 16 | `year_model` | varchar | YES |  |
| 17 | `price` | decimal(18,2) | YES |  |
| 18 | `mileage` | double | YES |  |
| 19 | `date_load` | timestamp(3) | YES |  |
| 20 | `color_name` | varchar | YES |  |
| 21 | `class_name` | varchar | YES |  |
| 22 | `homologated_class` | varchar | YES |  |
| 23 | `consolidated_class` | varchar | YES |  |
| 24 | `body_car` | varchar | YES |  |
| 25 | `condition_name` | varchar | YES |  |
| 26 | `fuel_name` | varchar | YES |  |
| 27 | `reference_name` | varchar | YES |  |
| 28 | `homologated_reference` | varchar | YES |  |
| 29 | `service_name` | varchar | YES |  |

### seissa_materialized_data.vista_cliente_journey

**Columnas:** 36

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `product_services_id` | integer | YES |  |
| 3 | `product_name` | varchar | YES |  |
| 4 | `company` | varchar | YES |  |
| 5 | `vehicle_brand` | varchar | YES |  |
| 6 | `homologated_brand` | varchar | YES |  |
| 7 | `vehicle_class` | varchar | YES |  |
| 8 | `year_model` | varchar | YES |  |
| 9 | `vehicle_condition` | varchar | YES |  |
| 10 | `vehicle_fuel` | varchar | YES |  |
| 11 | `vehicle_price` | decimal(18,2) | YES |  |
| 12 | `vin` | varchar | YES |  |
| 13 | `plate_name` | varchar | YES |  |
| 14 | `numero_compra` | integer | YES |  |
| 15 | `producto_origen_id` | integer | YES |  |
| 16 | `producto_origen_name` | varchar | YES |  |
| 17 | `contract_date` | timestamp(3) | YES |  |
| 18 | `dias_proxima_compra` | integer | YES |  |
| 19 | `target_id` | integer | YES |  |
| 20 | `sale_amount` | double | YES |  |
| 21 | `financed_amount` | double | YES |  |
| 22 | `invoiced_amount` | double | YES |  |
| 23 | `dias_desde_ultima_compra` | integer | YES |  |
| 24 | `event_tipo` | integer | YES |  |
| 25 | `age` | integer | YES |  |
| 26 | `gender_name` | varchar | YES |  |
| 27 | `monthly_income` | decimal(16,4) | YES |  |
| 28 | `municipality` | varchar | YES |  |
| 29 | `departament` | varchar | YES |  |
| 30 | `marital_status` | varchar | YES |  |
| 31 | `occupation` | varchar | YES |  |
| 32 | `level_education` | varchar | YES |  |
| 33 | `client_status` | varchar | YES |  |
| 34 | `country` | varchar | YES |  |
| 35 | `fecha_primera_compra` | timestamp(3) | YES |  |
| 36 | `dias_desde_primera_compra` | integer | YES |  |

### seissa_materialized_data.vw_clientes_compartidos_resumen

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `empresa_origen` | varchar | YES |  |
| 2 | `carfiao_productos` | bigint | YES |  |
| 3 | `bellpi_productos` | bigint | YES |  |
| 4 | `equirent_productos` | bigint | YES |  |
| 5 | `finandina_productos` | bigint | YES |  |
| 6 | `bonaparte_productos` | bigint | YES |  |
| 7 | `casatoro_productos` | bigint | YES |  |
| 8 | `promotec_productos` | bigint | YES |  |
| 9 | `simon_productos` | bigint | YES |  |
| 10 | `motorysa_productos` | bigint | YES |  |
| 11 | `finanzauto_productos` | bigint | YES |  |
| 12 | `total_productos` | bigint | YES |  |

### seissa_materialized_data.vw_clientes_compartidos_resumen_mensual

**Columnas:** 14

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `anio` | bigint | YES |  |
| 2 | `mes` | bigint | YES |  |
| 3 | `empresa_origen` | varchar | YES |  |
| 4 | `carfiao_productos` | bigint | YES |  |
| 5 | `bellpi_productos` | bigint | YES |  |
| 6 | `equirent_productos` | bigint | YES |  |
| 7 | `finandina_productos` | bigint | YES |  |
| 8 | `bonaparte_productos` | bigint | YES |  |
| 9 | `casatoro_productos` | bigint | YES |  |
| 10 | `promotec_productos` | bigint | YES |  |
| 11 | `simon_productos` | bigint | YES |  |
| 12 | `motorysa_productos` | bigint | YES |  |
| 13 | `finanzauto_productos` | bigint | YES |  |
| 14 | `total_productos` | bigint | YES |  |

## 🥈 silver

`Capa: Plata / Materialized`

### silver.dim_cli_address

**Columnas:** 16

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `address_id` | integer | YES |  |
| 2 | `city_id` | integer | YES |  |
| 3 | `address` | varchar | YES |  |
| 4 | `status` | boolean | YES |  |
| 5 | `load_data` | timestamp(3) | YES |  |
| 6 | `_silver_processed_at` | timestamp(3) | YES |  |
| 7 | `_silver_job_run_id` | varchar | YES |  |
| 8 | `_silver_source_entity` | varchar | YES |  |
| 9 | `_silver_source_folder` | varchar | YES |  |
| 10 | `_silver_record_hash` | varchar | YES |  |
| 11 | `_silver_is_current` | boolean | YES |  |
| 12 | `_silver_valid_from` | date | YES |  |
| 13 | `_silver_valid_to` | date | YES |  |
| 14 | `_proc_year` | varchar | YES |  |
| 15 | `_proc_month` | varchar | YES |  |
| 16 | `_proc_day` | varchar | YES |  |

## 🥉 sonardd_jdoc_analytics

`Capa: Bronce / Raw`

### sonardd_jdoc_analytics.d_boundaries

**Columnas:** 16

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_boundary` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `organization_id` | varchar | YES |  |
| 4 | `field_id` | varchar | YES |  |
| 5 | `boundary_id` | varchar | YES |  |
| 6 | `boundary_name` | varchar | YES |  |
| 7 | `source_type` | varchar | YES |  |
| 8 | `created_time` | timestamp(3) | YES |  |
| 9 | `modified_time` | timestamp(3) | YES |  |
| 10 | `area_value` | decimal(18,6) | YES |  |
| 11 | `area_unit` | varchar | YES |  |
| 12 | `workable_area_value` | decimal(18,6) | YES |  |
| 13 | `workable_area_unit` | varchar | YES |  |
| 14 | `active` | boolean | YES |  |
| 15 | `irrigated` | boolean | YES |  |
| 16 | `archived` | boolean | YES |  |

### sonardd_jdoc_analytics.d_clients

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_client` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `organization_id` | varchar | YES |  |
| 4 | `client_id` | varchar | YES |  |
| 5 | `client_name` | varchar | YES |  |
| 6 | `archived` | boolean | YES |  |
| 7 | `user_creation_timestamp` | timestamp(3) | YES |  |
| 8 | `user_last_modified_timestamp` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.d_croptype_equipment_types

**Columnas:** 4

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_croptype_equipment_type` | bigint | YES |  |
| 2 | `croptype_id` | varchar | YES |  |
| 3 | `equipment_type_id` | varchar | YES |  |
| 4 | `equipment_type_name` | varchar | YES |  |

### sonardd_jdoc_analytics.d_croptypes

**Columnas:** 9

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_croptype` | bigint | YES |  |
| 2 | `croptype_id` | varchar | YES |  |
| 3 | `croptype_name` | varchar | YES |  |
| 4 | `translated_name` | varchar | YES |  |
| 5 | `color` | varchar | YES |  |
| 6 | `density_factor_value` | decimal(18,6) | YES |  |
| 7 | `density_factor_unit` | varchar | YES |  |
| 8 | `standard_payable_moisture_value` | decimal(18,6) | YES |  |
| 9 | `standard_payable_moisture_unit` | varchar | YES |  |

### sonardd_jdoc_analytics.d_devices

**Columnas:** 19

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_device` | bigint | YES |  |
| 2 | `device_id` | varchar | YES |  |
| 3 | `organization_id` | varchar | YES |  |
| 4 | `principal_id` | varchar | YES |  |
| 5 | `make_id` | varchar | YES |  |
| 6 | `type_id` | varchar | YES |  |
| 7 | `model_id` | varchar | YES |  |
| 8 | `equipment_id` | varchar | YES |  |
| 9 | `equipment_principal_id` | varchar | YES |  |
| 10 | `equipment_organization_id` | varchar | YES |  |
| 11 | `serial_number` | varchar | YES |  |
| 12 | `type_name` | varchar | YES |  |
| 13 | `model_name` | varchar | YES |  |
| 14 | `firmware_version` | varchar | YES |  |
| 15 | `archived` | boolean | YES |  |
| 16 | `decommissioned` | boolean | YES |  |
| 17 | `source_updated_at_utc` | timestamp(3) | YES |  |
| 18 | `created_at_utc` | timestamp(3) | YES |  |
| 19 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.d_equipment

**Columnas:** 22

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_equipment` | bigint | YES |  |
| 2 | `equipment_id` | varchar | YES |  |
| 3 | `organization_id` | varchar | YES |  |
| 4 | `principal_id` | varchar | YES |  |
| 5 | `make_id` | varchar | YES |  |
| 6 | `type_id` | varchar | YES |  |
| 7 | `isg_type_id` | varchar | YES |  |
| 8 | `model_id` | varchar | YES |  |
| 9 | `name` | varchar | YES |  |
| 10 | `serial_number` | varchar | YES |  |
| 11 | `engine_serial_number` | varchar | YES |  |
| 12 | `model_year` | integer | YES |  |
| 13 | `make_name` | varchar | YES |  |
| 14 | `type_name` | varchar | YES |  |
| 15 | `isg_type_name` | varchar | YES |  |
| 16 | `familia_maquina` | varchar | YES |  |
| 17 | `has_modem` | boolean | YES |  |
| 18 | `model_name` | varchar | YES |  |
| 19 | `organization_role_effective_ts` | timestamp(3) | YES |  |
| 20 | `source_updated_at_utc` | timestamp(3) | YES |  |
| 21 | `created_at_utc` | timestamp(3) | YES |  |
| 22 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.d_farms

**Columnas:** 9

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_farm` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `organization_id` | varchar | YES |  |
| 4 | `farm_id` | varchar | YES |  |
| 5 | `farm_name` | varchar | YES |  |
| 6 | `archived` | boolean | YES |  |
| 7 | `client_id` | varchar | YES |  |
| 8 | `user_creation_timestamp` | timestamp(3) | YES |  |
| 9 | `user_last_modified_timestamp` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.d_field_operations

**Columnas:** 21

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_field_operation_dim` | bigint | YES |  |
| 2 | `sk_field_operation` | bigint | YES |  |
| 3 | `sk_organization` | bigint | YES |  |
| 4 | `sk_field` | bigint | YES |  |
| 5 | `operation_key` | varchar | YES |  |
| 6 | `organization_id` | varchar | YES |  |
| 7 | `field_id` | varchar | YES |  |
| 8 | `operation_id` | varchar | YES |  |
| 9 | `operation_type` | varchar | YES |  |
| 10 | `operation_date` | date | YES |  |
| 11 | `crop_season` | varchar | YES |  |
| 12 | `treated_crop_name` | varchar | YES |  |
| 13 | `crop_name` | varchar | YES |  |
| 14 | `adapt_machine_type` | varchar | YES |  |
| 15 | `dt_start_utc` | timestamp(3) | YES |  |
| 16 | `dt_end_utc` | timestamp(3) | YES |  |
| 17 | `dt_modified_utc` | timestamp(3) | YES |  |
| 18 | `source_st_changed` | varchar | YES |  |
| 19 | `source_dt_last_sync_utc` | timestamp(3) | YES |  |
| 20 | `source_updated_at_utc` | timestamp(3) | YES |  |
| 21 | `gold_loaded_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.d_fields

**Columnas:** 13

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_field` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `organization_id` | varchar | YES |  |
| 4 | `field_id` | varchar | YES |  |
| 5 | `field_name` | varchar | YES |  |
| 6 | `archived` | boolean | YES |  |
| 7 | `last_modified_time` | timestamp(3) | YES |  |
| 8 | `primary_client_id` | varchar | YES |  |
| 9 | `primary_client_name` | varchar | YES |  |
| 10 | `primary_client_type` | varchar | YES |  |
| 11 | `primary_farm_id` | varchar | YES |  |
| 12 | `primary_farm_name` | varchar | YES |  |
| 13 | `primary_farm_type` | varchar | YES |  |

### sonardd_jdoc_analytics.d_flags

**Columnas:** 11

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_flag` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `organization_id` | varchar | YES |  |
| 4 | `flag_id` | varchar | YES |  |
| 5 | `flag_name` | varchar | YES |  |
| 6 | `color` | varchar | YES |  |
| 7 | `shape` | varchar | YES |  |
| 8 | `note` | varchar | YES |  |
| 9 | `created_time` | timestamp(3) | YES |  |
| 10 | `modified_time` | timestamp(3) | YES |  |
| 11 | `archived` | boolean | YES |  |

### sonardd_jdoc_analytics.d_guidance_lines

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_guidance_line` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `organization_id` | varchar | YES |  |
| 4 | `field_id` | varchar | YES |  |
| 5 | `guidance_line_id` | varchar | YES |  |
| 6 | `guidance_line_name` | varchar | YES |  |
| 7 | `guidance_type` | varchar | YES |  |
| 8 | `archived` | boolean | YES |  |

### sonardd_jdoc_analytics.d_implements

**Columnas:** 21

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_implement` | bigint | YES |  |
| 2 | `equipment_id` | varchar | YES |  |
| 3 | `organization_id` | varchar | YES |  |
| 4 | `principal_id` | varchar | YES |  |
| 5 | `make_id` | varchar | YES |  |
| 6 | `type_id` | varchar | YES |  |
| 7 | `isg_type_id` | varchar | YES |  |
| 8 | `model_id` | varchar | YES |  |
| 9 | `name` | varchar | YES |  |
| 10 | `serial_number` | varchar | YES |  |
| 11 | `engine_serial_number` | varchar | YES |  |
| 12 | `model_year` | integer | YES |  |
| 13 | `make_name` | varchar | YES |  |
| 14 | `type_name` | varchar | YES |  |
| 15 | `isg_type_name` | varchar | YES |  |
| 16 | `familia_maquina` | varchar | YES |  |
| 17 | `model_name` | varchar | YES |  |
| 18 | `organization_role_effective_ts` | timestamp(3) | YES |  |
| 19 | `source_updated_at_utc` | timestamp(3) | YES |  |
| 20 | `created_at_utc` | timestamp(3) | YES |  |
| 21 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.d_machine_measurement

**Columnas:** 17

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_machine_measurement` | bigint | YES |  |
| 2 | `canonical_technology_name` | varchar | YES |  |
| 3 | `canonical_measurement_id` | varchar | YES |  |
| 4 | `sequence_number` | integer | YES |  |
| 5 | `sequence_description` | varchar | YES |  |
| 6 | `is_range_indicator` | boolean | YES |  |
| 7 | `min_value` | double | YES |  |
| 8 | `max_value` | double | YES |  |
| 9 | `description` | varchar | YES |  |
| 10 | `aggregation_type` | varchar | YES |  |
| 11 | `aggregation_type_id` | varchar | YES |  |
| 12 | `default_measure_unit` | varchar | YES |  |
| 13 | `measurement_type` | varchar | YES |  |
| 14 | `ui_visible_indicator` | varchar | YES |  |
| 15 | `is_active` | boolean | YES |  |
| 16 | `created_at_utc` | timestamp(3) | YES |  |
| 17 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.d_operators

**Columnas:** 11

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_operator` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `organization_id` | varchar | YES |  |
| 4 | `operator_id` | varchar | YES |  |
| 5 | `operator_name` | varchar | YES |  |
| 6 | `first_name` | varchar | YES |  |
| 7 | `last_name` | varchar | YES |  |
| 8 | `archived` | boolean | YES |  |
| 9 | `date_modified` | timestamp(3) | YES |  |
| 10 | `user_creation_timestamp` | timestamp(3) | YES |  |
| 11 | `user_last_modified_timestamp` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.d_organizations

**Columnas:** 7

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_organization` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `name` | varchar | YES |  |
| 4 | `need_connection` | boolean | YES |  |
| 5 | `source_updated_at_utc` | timestamp(3) | YES |  |
| 6 | `created_at_utc` | timestamp(3) | YES |  |
| 7 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.etl_job_runs

**Columnas:** 9

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `run_id` | varchar | YES |  |
| 3 | `job_name` | varchar | YES |  |
| 4 | `started_at_utc` | timestamp(3) | YES |  |
| 5 | `finished_at_utc` | timestamp(3) | YES |  |
| 6 | `status` | varchar | YES |  |
| 7 | `rows_inserted` | integer | YES |  |
| 8 | `rows_updated` | integer | YES |  |
| 9 | `error_message` | varchar | YES |  |

### sonardd_jdoc_analytics.etl_watermarks

**Columnas:** 3

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `job_name` | varchar | YES |  |
| 2 | `last_success_ts_utc` | timestamp(3) | YES |  |
| 3 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.f_engine_hours

**Columnas:** 11

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_engine_hours` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `sk_equipment` | bigint | YES |  |
| 4 | `organization_id` | varchar | YES |  |
| 5 | `principal_id` | varchar | YES |  |
| 6 | `request_date` | date | YES |  |
| 7 | `report_time_utc` | timestamp(3) | YES |  |
| 8 | `hours_value` | decimal(12,2) | YES |  |
| 9 | `hours_unit` | varchar | YES |  |
| 10 | `source_created_at_utc` | timestamp(3) | YES |  |
| 11 | `gold_loaded_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.f_field_operation_composition

**Columnas:** 31

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_field_operation_composition` | bigint | YES |  |
| 2 | `sk_field_operation` | bigint | YES |  |
| 3 | `sk_organization` | bigint | YES |  |
| 4 | `sk_field` | bigint | YES |  |
| 5 | `operation_key` | varchar | YES |  |
| 6 | `organization_id` | varchar | YES |  |
| 7 | `field_id` | varchar | YES |  |
| 8 | `operation_id` | varchar | YES |  |
| 9 | `operation_date` | date | YES |  |
| 10 | `machine_count` | integer | YES |  |
| 11 | `operator_count` | integer | YES |  |
| 12 | `product_count` | integer | YES |  |
| 13 | `measurement_count` | integer | YES |  |
| 14 | `measurement_total_count` | integer | YES |  |
| 15 | `has_machine` | boolean | YES |  |
| 16 | `has_operator` | boolean | YES |  |
| 17 | `has_product` | boolean | YES |  |
| 18 | `has_measurement` | boolean | YES |  |
| 19 | `has_measurement_total` | boolean | YES |  |
| 20 | `machine_ids` | varchar | YES |  |
| 21 | `machine_vins` | varchar | YES |  |
| 22 | `machine_guids` | varchar | YES |  |
| 23 | `machine_erids` | varchar | YES |  |
| 24 | `operator_ids` | varchar | YES |  |
| 25 | `operator_names` | varchar | YES |  |
| 26 | `product_ids` | varchar | YES |  |
| 27 | `product_names` | varchar | YES |  |
| 28 | `product_kinds` | varchar | YES |  |
| 29 | `product_brands` | varchar | YES |  |
| 30 | `source_updated_at_utc` | timestamp(3) | YES |  |
| 31 | `gold_loaded_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.f_field_operation_kpis

**Columnas:** 50

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_field_operation_kpi` | bigint | YES |  |
| 2 | `sk_field_operation` | bigint | YES |  |
| 3 | `sk_organization` | bigint | YES |  |
| 4 | `sk_field` | bigint | YES |  |
| 5 | `organization_id` | varchar | YES |  |
| 6 | `field_id` | varchar | YES |  |
| 7 | `operation_id` | varchar | YES |  |
| 8 | `operation_key` | varchar | YES |  |
| 9 | `operation_type` | varchar | YES |  |
| 10 | `operation_date` | date | YES |  |
| 11 | `crop_season` | varchar | YES |  |
| 12 | `treated_crop_name` | varchar | YES |  |
| 13 | `crop_name` | varchar | YES |  |
| 14 | `adapt_machine_type` | varchar | YES |  |
| 15 | `machine_count` | integer | YES |  |
| 16 | `operator_count` | integer | YES |  |
| 17 | `product_count` | integer | YES |  |
| 18 | `measurement_count` | integer | YES |  |
| 19 | `measurement_total_count` | integer | YES |  |
| 20 | `has_machine` | boolean | YES |  |
| 21 | `has_operator` | boolean | YES |  |
| 22 | `has_product` | boolean | YES |  |
| 23 | `has_measurement` | boolean | YES |  |
| 24 | `has_measurement_total` | boolean | YES |  |
| 25 | `has_official_area` | boolean | YES |  |
| 26 | `has_application_product_total` | boolean | YES |  |
| 27 | `official_area_value` | double | YES |  |
| 28 | `official_area_unit` | varchar | YES |  |
| 29 | `official_area_source` | varchar | YES |  |
| 30 | `applied_area_value` | double | YES |  |
| 31 | `applied_area_unit` | varchar | YES |  |
| 32 | `average_speed_value` | double | YES |  |
| 33 | `average_speed_unit` | varchar | YES |  |
| 34 | `average_depth_value` | double | YES |  |
| 35 | `average_depth_unit` | varchar | YES |  |
| 36 | `yield_value` | double | YES |  |
| 37 | `yield_unit` | varchar | YES |  |
| 38 | `average_yield_value` | double | YES |  |
| 39 | `average_yield_unit` | varchar | YES |  |
| 40 | `average_moisture_value` | double | YES |  |
| 41 | `average_moisture_unit` | varchar | YES |  |
| 42 | `wet_mass_value` | double | YES |  |
| 43 | `wet_mass_unit` | varchar | YES |  |
| 44 | `total_material_value` | double | YES |  |
| 45 | `total_material_unit` | varchar | YES |  |
| 46 | `average_material_value` | double | YES |  |
| 47 | `average_material_unit` | varchar | YES |  |
| 48 | `duration_hours` | double | YES |  |
| 49 | `source_updated_at_utc` | timestamp(3) | YES |  |
| 50 | `gold_loaded_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.f_field_operation_machines

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_field_operation_machine` | bigint | YES |  |
| 2 | `sk_field_operation` | bigint | YES |  |
| 3 | `sk_organization` | bigint | YES |  |
| 4 | `sk_field` | bigint | YES |  |
| 5 | `organization_id` | varchar | YES |  |
| 6 | `field_id` | varchar | YES |  |
| 7 | `operation_id` | varchar | YES |  |
| 8 | `operation_date` | date | YES |  |
| 9 | `machine_id` | varchar | YES |  |
| 10 | `vin` | varchar | YES |  |
| 11 | `guid` | varchar | YES |  |
| 12 | `erid` | varchar | YES |  |
| 13 | `source_request_ts_utc` | timestamp(3) | YES |  |
| 14 | `source_updated_at_utc` | timestamp(3) | YES |  |
| 15 | `gold_loaded_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.f_field_operation_measurement_totals

**Columnas:** 39

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_field_operation_measurement_total` | bigint | YES |  |
| 2 | `sk_field_operation` | bigint | YES |  |
| 3 | `sk_organization` | bigint | YES |  |
| 4 | `sk_field` | bigint | YES |  |
| 5 | `organization_id` | varchar | YES |  |
| 6 | `operation_id` | varchar | YES |  |
| 7 | `field_id` | varchar | YES |  |
| 8 | `operation_date` | date | YES |  |
| 9 | `measurement_name` | varchar | YES |  |
| 10 | `measurement_category` | varchar | YES |  |
| 11 | `total_type` | varchar | YES |  |
| 12 | `item_type` | varchar | YES |  |
| 13 | `item_id` | varchar | YES |  |
| 14 | `item_name` | varchar | YES |  |
| 15 | `area_value` | double | YES |  |
| 16 | `area_unit` | varchar | YES |  |
| 17 | `applied_area_value` | double | YES |  |
| 18 | `applied_area_unit` | varchar | YES |  |
| 19 | `average_speed_value` | double | YES |  |
| 20 | `average_speed_unit` | varchar | YES |  |
| 21 | `average_depth_value` | double | YES |  |
| 22 | `average_depth_unit` | varchar | YES |  |
| 23 | `yield_value` | double | YES |  |
| 24 | `yield_unit` | varchar | YES |  |
| 25 | `average_yield_value` | double | YES |  |
| 26 | `average_yield_unit` | varchar | YES |  |
| 27 | `average_moisture_value` | double | YES |  |
| 28 | `average_moisture_unit` | varchar | YES |  |
| 29 | `wet_mass_value` | double | YES |  |
| 30 | `wet_mass_unit` | varchar | YES |  |
| 31 | `average_wet_mass_value` | double | YES |  |
| 32 | `average_wet_mass_unit` | varchar | YES |  |
| 33 | `total_material_value` | double | YES |  |
| 34 | `total_material_unit` | varchar | YES |  |
| 35 | `average_material_value` | double | YES |  |
| 36 | `average_material_unit` | varchar | YES |  |
| 37 | `source_request_ts_utc` | timestamp(3) | YES |  |
| 38 | `source_updated_at_utc` | timestamp(3) | YES |  |
| 39 | `gold_loaded_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.f_field_operation_measurements

**Columnas:** 33

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_field_operation_measurement` | bigint | YES |  |
| 2 | `sk_field_operation` | bigint | YES |  |
| 3 | `sk_organization` | bigint | YES |  |
| 4 | `sk_field` | bigint | YES |  |
| 5 | `organization_id` | varchar | YES |  |
| 6 | `operation_id` | varchar | YES |  |
| 7 | `field_id` | varchar | YES |  |
| 8 | `operation_date` | date | YES |  |
| 9 | `measurement_name` | varchar | YES |  |
| 10 | `measurement_category` | varchar | YES |  |
| 11 | `area_value` | double | YES |  |
| 12 | `area_unit` | varchar | YES |  |
| 13 | `average_speed_value` | double | YES |  |
| 14 | `average_speed_unit` | varchar | YES |  |
| 15 | `average_depth_value` | double | YES |  |
| 16 | `average_depth_unit` | varchar | YES |  |
| 17 | `yield_value` | double | YES |  |
| 18 | `yield_unit` | varchar | YES |  |
| 19 | `average_yield_value` | double | YES |  |
| 20 | `average_yield_unit` | varchar | YES |  |
| 21 | `average_moisture_value` | double | YES |  |
| 22 | `average_moisture_unit` | varchar | YES |  |
| 23 | `wet_mass_value` | double | YES |  |
| 24 | `wet_mass_unit` | varchar | YES |  |
| 25 | `average_wet_mass_value` | double | YES |  |
| 26 | `average_wet_mass_unit` | varchar | YES |  |
| 27 | `total_material_value` | double | YES |  |
| 28 | `total_material_unit` | varchar | YES |  |
| 29 | `average_material_value` | double | YES |  |
| 30 | `average_material_unit` | varchar | YES |  |
| 31 | `source_request_ts_utc` | timestamp(3) | YES |  |
| 32 | `source_updated_at_utc` | timestamp(3) | YES |  |
| 33 | `gold_loaded_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.f_field_operation_operators

**Columnas:** 17

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_field_operation_operator` | bigint | YES |  |
| 2 | `sk_field_operation` | bigint | YES |  |
| 3 | `sk_organization` | bigint | YES |  |
| 4 | `sk_field` | bigint | YES |  |
| 5 | `organization_id` | varchar | YES |  |
| 6 | `field_id` | varchar | YES |  |
| 7 | `operation_id` | varchar | YES |  |
| 8 | `operation_date` | date | YES |  |
| 9 | `machine_id` | varchar | YES |  |
| 10 | `machine_guid` | varchar | YES |  |
| 11 | `machine_erid` | varchar | YES |  |
| 12 | `machine_vin` | varchar | YES |  |
| 13 | `operator_id` | varchar | YES |  |
| 14 | `operator_name` | varchar | YES |  |
| 15 | `source_request_ts_utc` | timestamp(3) | YES |  |
| 16 | `source_updated_at_utc` | timestamp(3) | YES |  |
| 17 | `gold_loaded_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.f_field_operation_products

**Columnas:** 20

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_field_operation_product` | bigint | YES |  |
| 2 | `sk_field_operation` | bigint | YES |  |
| 3 | `sk_organization` | bigint | YES |  |
| 4 | `sk_field` | bigint | YES |  |
| 5 | `organization_id` | varchar | YES |  |
| 6 | `field_id` | varchar | YES |  |
| 7 | `operation_id` | varchar | YES |  |
| 8 | `operation_date` | date | YES |  |
| 9 | `product_kind` | varchar | YES |  |
| 10 | `item_type` | varchar | YES |  |
| 11 | `guid` | varchar | YES |  |
| 12 | `product_type` | varchar | YES |  |
| 13 | `product_id` | varchar | YES |  |
| 14 | `name` | varchar | YES |  |
| 15 | `brand` | varchar | YES |  |
| 16 | `tank_mix` | boolean | YES |  |
| 17 | `tillage_type` | varchar | YES |  |
| 18 | `source_request_ts_utc` | timestamp(3) | YES |  |
| 19 | `source_updated_at_utc` | timestamp(3) | YES |  |
| 20 | `gold_loaded_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.f_field_operations

**Columnas:** 22

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_field_operation` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `sk_field` | bigint | YES |  |
| 4 | `organization_id` | varchar | YES |  |
| 5 | `field_id` | varchar | YES |  |
| 6 | `operation_id` | varchar | YES |  |
| 7 | `operation_type` | varchar | YES |  |
| 8 | `crop_season` | varchar | YES |  |
| 9 | `dt_start_utc` | timestamp(3) | YES |  |
| 10 | `dt_end_utc` | timestamp(3) | YES |  |
| 11 | `dt_modified_utc` | timestamp(3) | YES |  |
| 12 | `operation_date` | date | YES |  |
| 13 | `treated_crop_name` | varchar | YES |  |
| 14 | `crop_name` | varchar | YES |  |
| 15 | `adapt_machine_type` | varchar | YES |  |
| 16 | `machine_count` | integer | YES |  |
| 17 | `operator_count` | integer | YES |  |
| 18 | `product_count` | integer | YES |  |
| 19 | `source_st_changed` | varchar | YES |  |
| 20 | `source_dt_last_sync_utc` | timestamp(3) | YES |  |
| 21 | `source_updated_at_utc` | timestamp(3) | YES |  |
| 22 | `gold_loaded_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.f_hours_of_operation

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_hours_of_operation` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `sk_equipment` | bigint | YES |  |
| 4 | `organization_id` | varchar | YES |  |
| 5 | `principal_id` | varchar | YES |  |
| 6 | `operation_date` | date | YES |  |
| 7 | `engine_state` | integer | YES |  |
| 8 | `duration_hours` | decimal(12,6) | YES |  |
| 9 | `first_start_utc` | timestamp(3) | YES |  |
| 10 | `last_end_utc` | timestamp(3) | YES |  |
| 11 | `source_last_created_at_utc` | timestamp(3) | YES |  |
| 12 | `gold_loaded_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.f_machine_alerts

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_machine_alert` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `sk_equipment` | bigint | YES |  |
| 4 | `organization_id` | varchar | YES |  |
| 5 | `principal_id` | varchar | YES |  |
| 6 | `alert_id` | varchar | YES |  |
| 7 | `alert_timestamp_utc` | timestamp(3) | YES |  |
| 8 | `alert_type` | varchar | YES |  |
| 9 | `severity` | varchar | YES |  |
| 10 | `description` | varchar | YES |  |
| 11 | `dtc_code` | varchar | YES |  |
| 12 | `source` | varchar | YES |  |
| 13 | `status` | varchar | YES |  |
| 14 | `color` | varchar | YES |  |
| 15 | `latitude` | double | YES |  |
| 16 | `longitude` | double | YES |  |
| 17 | `occurrences` | integer | YES |  |
| 18 | `engine_hours` | double | YES |  |
| 19 | `engine_hours_unit` | varchar | YES |  |
| 20 | `machine_linear_time` | bigint | YES |  |
| 21 | `three_letter_acronym` | varchar | YES |  |
| 22 | `nm_suspect_parameter` | varchar | YES |  |
| 23 | `failure_mode_indicator` | integer | YES |  |
| 24 | `codigo_diagnostico_falhas` | varchar | YES |  |
| 25 | `ignored` | boolean | YES |  |
| 26 | `invisible` | boolean | YES |  |
| 27 | `duration_seconds` | integer | YES |  |
| 28 | `duration_unit` | varchar | YES |  |
| 29 | `request_ts_utc` | timestamp(3) | YES |  |
| 30 | `created_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.f_machine_breadcrumbs

**Columnas:** 18

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_breadcrumb` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `sk_equipment` | bigint | YES |  |
| 4 | `organization_id` | varchar | YES |  |
| 5 | `principal_id` | varchar | YES |  |
| 6 | `event_timestamp_utc` | timestamp(3) | YES |  |
| 7 | `location_lat` | decimal(10,7) | YES |  |
| 8 | `location_lon` | decimal(10,7) | YES |  |
| 9 | `location_altitude` | decimal(10,2) | YES |  |
| 10 | `machine_status` | varchar | YES |  |
| 11 | `request_status` | varchar | YES |  |
| 12 | `request_http_code` | integer | YES |  |
| 13 | `request_ts_utc` | timestamp(3) | YES |  |
| 14 | `request_date_utc` | date | YES |  |
| 15 | `days_since_last_signal` | integer | YES |  |
| 16 | `signal_range_label` | varchar | YES |  |
| 17 | `status_conexao` | varchar | YES |  |
| 18 | `created_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.f_machine_device_state_reports

**Columnas:** 13

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_machine_device_state_report` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `sk_equipment` | bigint | YES |  |
| 4 | `sk_device` | bigint | YES |  |
| 5 | `organization_id` | varchar | YES |  |
| 6 | `principal_id` | varchar | YES |  |
| 7 | `request_date` | date | YES |  |
| 8 | `report_timestamp_utc` | timestamp(3) | YES |  |
| 9 | `device_id` | varchar | YES |  |
| 10 | `state_type` | varchar | YES |  |
| 11 | `state_value` | varchar | YES |  |
| 12 | `source_created_at_utc` | timestamp(3) | YES |  |
| 13 | `gold_loaded_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.f_machine_location_history

**Columnas:** 14

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_machine_location_history` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `sk_equipment` | bigint | YES |  |
| 4 | `organization_id` | varchar | YES |  |
| 5 | `principal_id` | varchar | YES |  |
| 6 | `request_date` | date | YES |  |
| 7 | `event_timestamp_utc` | timestamp(3) | YES |  |
| 8 | `location_lat` | decimal(10,7) | YES |  |
| 9 | `location_lon` | decimal(10,7) | YES |  |
| 10 | `heading` | decimal(6,2) | YES |  |
| 11 | `speed` | decimal(8,3) | YES |  |
| 12 | `speed_unit` | varchar | YES |  |
| 13 | `source_created_at_utc` | timestamp(3) | YES |  |
| 14 | `gold_loaded_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.f_machine_measurements

**Columnas:** 24

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_machine_measurement` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `sk_equipment` | bigint | YES |  |
| 4 | `sk_machine_measurement_dim` | bigint | YES |  |
| 5 | `organization_id` | varchar | YES |  |
| 6 | `equipment_id` | varchar | YES |  |
| 7 | `principal_id` | varchar | YES |  |
| 8 | `business_date` | date | YES |  |
| 9 | `equipment_key` | varchar | YES |  |
| 10 | `technology_name` | varchar | YES |  |
| 11 | `canonical_measurement_id` | varchar | YES |  |
| 12 | `mapping_source` | varchar | YES |  |
| 13 | `mapping_level_rank` | tinyint | YES |  |
| 14 | `interval_start_utc` | timestamp(3) | YES |  |
| 15 | `interval_end_utc` | timestamp(3) | YES |  |
| 16 | `request_ts_utc` | timestamp(3) | YES |  |
| 17 | `gold_loaded_at_utc` | timestamp(3) | YES |  |
| 18 | `measurement_value` | double | YES |  |
| 19 | `measurement_count` | integer | YES |  |
| 20 | `sequence_number` | integer | YES |  |
| 21 | `measure_unit` | varchar | YES |  |
| 22 | `raw_measurement_name` | varchar | YES |  |
| 23 | `raw_measurement_id` | varchar | YES |  |
| 24 | `created_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.measurement_exclusions

**Columnas:** 5

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `raw_measurement_name` | varchar | YES |  |
| 2 | `reason` | varchar | YES |  |
| 3 | `is_active` | boolean | YES |  |
| 4 | `created_at_utc` | timestamp(3) | YES |  |
| 5 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.measurement_mapping_by_equipment_key

**Columnas:** 7

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `equipment_key` | varchar | YES |  |
| 2 | `canonical_technology_name` | varchar | YES |  |
| 3 | `canonical_measurement_id` | varchar | YES |  |
| 4 | `description` | varchar | YES |  |
| 5 | `is_active` | boolean | YES |  |
| 6 | `created_at_utc` | timestamp(3) | YES |  |
| 7 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.measurement_mapping_default_by_type

**Columnas:** 7

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `canonical_technology_name` | varchar | YES |  |
| 2 | `equipment_type` | varchar | YES |  |
| 3 | `canonical_measurement_id` | varchar | YES |  |
| 4 | `description` | varchar | YES |  |
| 5 | `is_active` | boolean | YES |  |
| 6 | `created_at_utc` | timestamp(3) | YES |  |
| 7 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.measurement_mapping_default_general

**Columnas:** 6

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `canonical_technology_name` | varchar | YES |  |
| 2 | `canonical_measurement_id` | varchar | YES |  |
| 3 | `description` | varchar | YES |  |
| 4 | `is_active` | boolean | YES |  |
| 5 | `created_at_utc` | timestamp(3) | YES |  |
| 6 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.measurement_mapping_equipment_exceptions

**Columnas:** 7

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `equipment_id` | varchar | YES |  |
| 2 | `canonical_technology_name` | varchar | YES |  |
| 3 | `canonical_measurement_id` | varchar | YES |  |
| 4 | `description` | varchar | YES |  |
| 5 | `is_active` | boolean | YES |  |
| 6 | `created_at_utc` | timestamp(3) | YES |  |
| 7 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics.measurement_sequence_definitions

**Columnas:** 10

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `canonical_measurement_id` | varchar | YES |  |
| 2 | `canonical_technology_name` | varchar | YES |  |
| 3 | `sequence_number` | integer | YES |  |
| 4 | `sequence_description` | varchar | YES |  |
| 5 | `is_range_indicator` | boolean | YES |  |
| 6 | `min_value` | double | YES |  |
| 7 | `max_value` | double | YES |  |
| 8 | `is_active` | boolean | YES |  |
| 9 | `created_at_utc` | timestamp(3) | YES |  |
| 10 | `updated_at_utc` | timestamp(3) | YES |  |

## 🥉 sonardd_jdoc_analytics_cr

`Capa: Bronce / Raw`

### sonardd_jdoc_analytics_cr.d_boundaries

**Columnas:** 16

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_boundary` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `organization_id` | varchar | YES |  |
| 4 | `field_id` | varchar | YES |  |
| 5 | `boundary_id` | varchar | YES |  |
| 6 | `boundary_name` | varchar | YES |  |
| 7 | `source_type` | varchar | YES |  |
| 8 | `created_time` | timestamp(3) | YES |  |
| 9 | `modified_time` | timestamp(3) | YES |  |
| 10 | `area_value` | decimal(18,6) | YES |  |
| 11 | `area_unit` | varchar | YES |  |
| 12 | `workable_area_value` | decimal(18,6) | YES |  |
| 13 | `workable_area_unit` | varchar | YES |  |
| 14 | `active` | boolean | YES |  |
| 15 | `irrigated` | boolean | YES |  |
| 16 | `archived` | boolean | YES |  |

### sonardd_jdoc_analytics_cr.d_clients

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_client` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `organization_id` | varchar | YES |  |
| 4 | `client_id` | varchar | YES |  |
| 5 | `client_name` | varchar | YES |  |
| 6 | `archived` | boolean | YES |  |
| 7 | `user_creation_timestamp` | timestamp(3) | YES |  |
| 8 | `user_last_modified_timestamp` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.d_croptype_equipment_types

**Columnas:** 4

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_croptype_equipment_type` | bigint | YES |  |
| 2 | `croptype_id` | varchar | YES |  |
| 3 | `equipment_type_id` | varchar | YES |  |
| 4 | `equipment_type_name` | varchar | YES |  |

### sonardd_jdoc_analytics_cr.d_croptypes

**Columnas:** 9

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_croptype` | bigint | YES |  |
| 2 | `croptype_id` | varchar | YES |  |
| 3 | `croptype_name` | varchar | YES |  |
| 4 | `translated_name` | varchar | YES |  |
| 5 | `color` | varchar | YES |  |
| 6 | `density_factor_value` | decimal(18,6) | YES |  |
| 7 | `density_factor_unit` | varchar | YES |  |
| 8 | `standard_payable_moisture_value` | decimal(18,6) | YES |  |
| 9 | `standard_payable_moisture_unit` | varchar | YES |  |

### sonardd_jdoc_analytics_cr.d_devices

**Columnas:** 19

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_device` | bigint | YES |  |
| 2 | `device_id` | varchar | YES |  |
| 3 | `organization_id` | varchar | YES |  |
| 4 | `principal_id` | varchar | YES |  |
| 5 | `make_id` | varchar | YES |  |
| 6 | `type_id` | varchar | YES |  |
| 7 | `model_id` | varchar | YES |  |
| 8 | `equipment_id` | varchar | YES |  |
| 9 | `equipment_principal_id` | varchar | YES |  |
| 10 | `equipment_organization_id` | varchar | YES |  |
| 11 | `serial_number` | varchar | YES |  |
| 12 | `type_name` | varchar | YES |  |
| 13 | `model_name` | varchar | YES |  |
| 14 | `firmware_version` | varchar | YES |  |
| 15 | `archived` | boolean | YES |  |
| 16 | `decommissioned` | boolean | YES |  |
| 17 | `source_updated_at_utc` | timestamp(3) | YES |  |
| 18 | `created_at_utc` | timestamp(3) | YES |  |
| 19 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.d_equipment

**Columnas:** 22

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_equipment` | bigint | YES |  |
| 2 | `equipment_id` | varchar | YES |  |
| 3 | `organization_id` | varchar | YES |  |
| 4 | `principal_id` | varchar | YES |  |
| 5 | `make_id` | varchar | YES |  |
| 6 | `type_id` | varchar | YES |  |
| 7 | `isg_type_id` | varchar | YES |  |
| 8 | `model_id` | varchar | YES |  |
| 9 | `name` | varchar | YES |  |
| 10 | `serial_number` | varchar | YES |  |
| 11 | `engine_serial_number` | varchar | YES |  |
| 12 | `model_year` | integer | YES |  |
| 13 | `make_name` | varchar | YES |  |
| 14 | `type_name` | varchar | YES |  |
| 15 | `isg_type_name` | varchar | YES |  |
| 16 | `familia_maquina` | varchar | YES |  |
| 17 | `has_modem` | boolean | YES |  |
| 18 | `model_name` | varchar | YES |  |
| 19 | `organization_role_effective_ts` | timestamp(3) | YES |  |
| 20 | `source_updated_at_utc` | timestamp(3) | YES |  |
| 21 | `created_at_utc` | timestamp(3) | YES |  |
| 22 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.d_farms

**Columnas:** 9

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_farm` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `organization_id` | varchar | YES |  |
| 4 | `farm_id` | varchar | YES |  |
| 5 | `farm_name` | varchar | YES |  |
| 6 | `archived` | boolean | YES |  |
| 7 | `client_id` | varchar | YES |  |
| 8 | `user_creation_timestamp` | timestamp(3) | YES |  |
| 9 | `user_last_modified_timestamp` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.d_fields

**Columnas:** 13

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_field` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `organization_id` | varchar | YES |  |
| 4 | `field_id` | varchar | YES |  |
| 5 | `field_name` | varchar | YES |  |
| 6 | `archived` | boolean | YES |  |
| 7 | `last_modified_time` | timestamp(3) | YES |  |
| 8 | `primary_client_id` | varchar | YES |  |
| 9 | `primary_client_name` | varchar | YES |  |
| 10 | `primary_client_type` | varchar | YES |  |
| 11 | `primary_farm_id` | varchar | YES |  |
| 12 | `primary_farm_name` | varchar | YES |  |
| 13 | `primary_farm_type` | varchar | YES |  |

### sonardd_jdoc_analytics_cr.d_flags

**Columnas:** 11

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_flag` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `organization_id` | varchar | YES |  |
| 4 | `flag_id` | varchar | YES |  |
| 5 | `flag_name` | varchar | YES |  |
| 6 | `color` | varchar | YES |  |
| 7 | `shape` | varchar | YES |  |
| 8 | `note` | varchar | YES |  |
| 9 | `created_time` | timestamp(3) | YES |  |
| 10 | `modified_time` | timestamp(3) | YES |  |
| 11 | `archived` | boolean | YES |  |

### sonardd_jdoc_analytics_cr.d_guidance_lines

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_guidance_line` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `organization_id` | varchar | YES |  |
| 4 | `field_id` | varchar | YES |  |
| 5 | `guidance_line_id` | varchar | YES |  |
| 6 | `guidance_line_name` | varchar | YES |  |
| 7 | `guidance_type` | varchar | YES |  |
| 8 | `archived` | boolean | YES |  |

### sonardd_jdoc_analytics_cr.d_implements

**Columnas:** 21

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_implement` | bigint | YES |  |
| 2 | `equipment_id` | varchar | YES |  |
| 3 | `organization_id` | varchar | YES |  |
| 4 | `principal_id` | varchar | YES |  |
| 5 | `make_id` | varchar | YES |  |
| 6 | `type_id` | varchar | YES |  |
| 7 | `isg_type_id` | varchar | YES |  |
| 8 | `model_id` | varchar | YES |  |
| 9 | `name` | varchar | YES |  |
| 10 | `serial_number` | varchar | YES |  |
| 11 | `engine_serial_number` | varchar | YES |  |
| 12 | `model_year` | integer | YES |  |
| 13 | `make_name` | varchar | YES |  |
| 14 | `type_name` | varchar | YES |  |
| 15 | `isg_type_name` | varchar | YES |  |
| 16 | `familia_maquina` | varchar | YES |  |
| 17 | `model_name` | varchar | YES |  |
| 18 | `organization_role_effective_ts` | timestamp(3) | YES |  |
| 19 | `source_updated_at_utc` | timestamp(3) | YES |  |
| 20 | `created_at_utc` | timestamp(3) | YES |  |
| 21 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.d_machine_measurement

**Columnas:** 17

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_machine_measurement` | bigint | YES |  |
| 2 | `canonical_technology_name` | varchar | YES |  |
| 3 | `canonical_measurement_id` | varchar | YES |  |
| 4 | `sequence_number` | integer | YES |  |
| 5 | `sequence_description` | varchar | YES |  |
| 6 | `is_range_indicator` | boolean | YES |  |
| 7 | `min_value` | double | YES |  |
| 8 | `max_value` | double | YES |  |
| 9 | `description` | varchar | YES |  |
| 10 | `aggregation_type` | varchar | YES |  |
| 11 | `aggregation_type_id` | varchar | YES |  |
| 12 | `default_measure_unit` | varchar | YES |  |
| 13 | `measurement_type` | varchar | YES |  |
| 14 | `ui_visible_indicator` | varchar | YES |  |
| 15 | `is_active` | boolean | YES |  |
| 16 | `created_at_utc` | timestamp(3) | YES |  |
| 17 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.d_operators

**Columnas:** 11

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_operator` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `organization_id` | varchar | YES |  |
| 4 | `operator_id` | varchar | YES |  |
| 5 | `operator_name` | varchar | YES |  |
| 6 | `first_name` | varchar | YES |  |
| 7 | `last_name` | varchar | YES |  |
| 8 | `archived` | boolean | YES |  |
| 9 | `date_modified` | timestamp(3) | YES |  |
| 10 | `user_creation_timestamp` | timestamp(3) | YES |  |
| 11 | `user_last_modified_timestamp` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.d_organizations

**Columnas:** 7

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_organization` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `name` | varchar | YES |  |
| 4 | `need_connection` | boolean | YES |  |
| 5 | `source_updated_at_utc` | timestamp(3) | YES |  |
| 6 | `created_at_utc` | timestamp(3) | YES |  |
| 7 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.etl_job_runs

**Columnas:** 9

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `run_id` | varchar | YES |  |
| 3 | `job_name` | varchar | YES |  |
| 4 | `started_at_utc` | timestamp(3) | YES |  |
| 5 | `finished_at_utc` | timestamp(3) | YES |  |
| 6 | `status` | varchar | YES |  |
| 7 | `rows_inserted` | integer | YES |  |
| 8 | `rows_updated` | integer | YES |  |
| 9 | `error_message` | varchar | YES |  |

### sonardd_jdoc_analytics_cr.etl_watermarks

**Columnas:** 3

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `job_name` | varchar | YES |  |
| 2 | `last_success_ts_utc` | timestamp(3) | YES |  |
| 3 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.f_engine_hours

**Columnas:** 11

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_engine_hours` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `sk_equipment` | bigint | YES |  |
| 4 | `organization_id` | varchar | YES |  |
| 5 | `principal_id` | varchar | YES |  |
| 6 | `request_date` | date | YES |  |
| 7 | `report_time_utc` | timestamp(3) | YES |  |
| 8 | `hours_value` | decimal(12,2) | YES |  |
| 9 | `hours_unit` | varchar | YES |  |
| 10 | `source_created_at_utc` | timestamp(3) | YES |  |
| 11 | `gold_loaded_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.f_field_operation_measurement_totals

**Columnas:** 39

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_field_operation_measurement_total` | bigint | YES |  |
| 2 | `sk_field_operation` | bigint | YES |  |
| 3 | `sk_organization` | bigint | YES |  |
| 4 | `sk_field` | bigint | YES |  |
| 5 | `organization_id` | varchar | YES |  |
| 6 | `operation_id` | varchar | YES |  |
| 7 | `field_id` | varchar | YES |  |
| 8 | `operation_date` | date | YES |  |
| 9 | `measurement_name` | varchar | YES |  |
| 10 | `measurement_category` | varchar | YES |  |
| 11 | `total_type` | varchar | YES |  |
| 12 | `item_type` | varchar | YES |  |
| 13 | `item_id` | varchar | YES |  |
| 14 | `item_name` | varchar | YES |  |
| 15 | `area_value` | double | YES |  |
| 16 | `area_unit` | varchar | YES |  |
| 17 | `applied_area_value` | double | YES |  |
| 18 | `applied_area_unit` | varchar | YES |  |
| 19 | `average_speed_value` | double | YES |  |
| 20 | `average_speed_unit` | varchar | YES |  |
| 21 | `average_depth_value` | double | YES |  |
| 22 | `average_depth_unit` | varchar | YES |  |
| 23 | `yield_value` | double | YES |  |
| 24 | `yield_unit` | varchar | YES |  |
| 25 | `average_yield_value` | double | YES |  |
| 26 | `average_yield_unit` | varchar | YES |  |
| 27 | `average_moisture_value` | double | YES |  |
| 28 | `average_moisture_unit` | varchar | YES |  |
| 29 | `wet_mass_value` | double | YES |  |
| 30 | `wet_mass_unit` | varchar | YES |  |
| 31 | `average_wet_mass_value` | double | YES |  |
| 32 | `average_wet_mass_unit` | varchar | YES |  |
| 33 | `total_material_value` | double | YES |  |
| 34 | `total_material_unit` | varchar | YES |  |
| 35 | `average_material_value` | double | YES |  |
| 36 | `average_material_unit` | varchar | YES |  |
| 37 | `source_request_ts_utc` | timestamp(3) | YES |  |
| 38 | `source_updated_at_utc` | timestamp(3) | YES |  |
| 39 | `gold_loaded_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.f_field_operation_measurements

**Columnas:** 33

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_field_operation_measurement` | bigint | YES |  |
| 2 | `sk_field_operation` | bigint | YES |  |
| 3 | `sk_organization` | bigint | YES |  |
| 4 | `sk_field` | bigint | YES |  |
| 5 | `organization_id` | varchar | YES |  |
| 6 | `operation_id` | varchar | YES |  |
| 7 | `field_id` | varchar | YES |  |
| 8 | `operation_date` | date | YES |  |
| 9 | `measurement_name` | varchar | YES |  |
| 10 | `measurement_category` | varchar | YES |  |
| 11 | `area_value` | double | YES |  |
| 12 | `area_unit` | varchar | YES |  |
| 13 | `average_speed_value` | double | YES |  |
| 14 | `average_speed_unit` | varchar | YES |  |
| 15 | `average_depth_value` | double | YES |  |
| 16 | `average_depth_unit` | varchar | YES |  |
| 17 | `yield_value` | double | YES |  |
| 18 | `yield_unit` | varchar | YES |  |
| 19 | `average_yield_value` | double | YES |  |
| 20 | `average_yield_unit` | varchar | YES |  |
| 21 | `average_moisture_value` | double | YES |  |
| 22 | `average_moisture_unit` | varchar | YES |  |
| 23 | `wet_mass_value` | double | YES |  |
| 24 | `wet_mass_unit` | varchar | YES |  |
| 25 | `average_wet_mass_value` | double | YES |  |
| 26 | `average_wet_mass_unit` | varchar | YES |  |
| 27 | `total_material_value` | double | YES |  |
| 28 | `total_material_unit` | varchar | YES |  |
| 29 | `average_material_value` | double | YES |  |
| 30 | `average_material_unit` | varchar | YES |  |
| 31 | `source_request_ts_utc` | timestamp(3) | YES |  |
| 32 | `source_updated_at_utc` | timestamp(3) | YES |  |
| 33 | `gold_loaded_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.f_field_operations

**Columnas:** 22

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_field_operation` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `sk_field` | bigint | YES |  |
| 4 | `organization_id` | varchar | YES |  |
| 5 | `field_id` | varchar | YES |  |
| 6 | `operation_id` | varchar | YES |  |
| 7 | `operation_type` | varchar | YES |  |
| 8 | `crop_season` | varchar | YES |  |
| 9 | `dt_start_utc` | timestamp(3) | YES |  |
| 10 | `dt_end_utc` | timestamp(3) | YES |  |
| 11 | `dt_modified_utc` | timestamp(3) | YES |  |
| 12 | `operation_date` | date | YES |  |
| 13 | `treated_crop_name` | varchar | YES |  |
| 14 | `crop_name` | varchar | YES |  |
| 15 | `adapt_machine_type` | varchar | YES |  |
| 16 | `machine_count` | integer | YES |  |
| 17 | `operator_count` | integer | YES |  |
| 18 | `product_count` | integer | YES |  |
| 19 | `source_st_changed` | varchar | YES |  |
| 20 | `source_dt_last_sync_utc` | timestamp(3) | YES |  |
| 21 | `source_updated_at_utc` | timestamp(3) | YES |  |
| 22 | `gold_loaded_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.f_hours_of_operation

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_hours_of_operation` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `sk_equipment` | bigint | YES |  |
| 4 | `organization_id` | varchar | YES |  |
| 5 | `principal_id` | varchar | YES |  |
| 6 | `operation_date` | date | YES |  |
| 7 | `engine_state` | integer | YES |  |
| 8 | `duration_hours` | decimal(12,6) | YES |  |
| 9 | `first_start_utc` | timestamp(3) | YES |  |
| 10 | `last_end_utc` | timestamp(3) | YES |  |
| 11 | `source_last_created_at_utc` | timestamp(3) | YES |  |
| 12 | `gold_loaded_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.f_machine_alerts

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_machine_alert` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `sk_equipment` | bigint | YES |  |
| 4 | `organization_id` | varchar | YES |  |
| 5 | `principal_id` | varchar | YES |  |
| 6 | `alert_id` | varchar | YES |  |
| 7 | `alert_timestamp_utc` | timestamp(3) | YES |  |
| 8 | `alert_type` | varchar | YES |  |
| 9 | `severity` | varchar | YES |  |
| 10 | `description` | varchar | YES |  |
| 11 | `dtc_code` | varchar | YES |  |
| 12 | `source` | varchar | YES |  |
| 13 | `status` | varchar | YES |  |
| 14 | `color` | varchar | YES |  |
| 15 | `latitude` | double | YES |  |
| 16 | `longitude` | double | YES |  |
| 17 | `occurrences` | integer | YES |  |
| 18 | `engine_hours` | double | YES |  |
| 19 | `engine_hours_unit` | varchar | YES |  |
| 20 | `machine_linear_time` | bigint | YES |  |
| 21 | `three_letter_acronym` | varchar | YES |  |
| 22 | `nm_suspect_parameter` | varchar | YES |  |
| 23 | `failure_mode_indicator` | integer | YES |  |
| 24 | `codigo_diagnostico_falhas` | varchar | YES |  |
| 25 | `ignored` | boolean | YES |  |
| 26 | `invisible` | boolean | YES |  |
| 27 | `duration_seconds` | integer | YES |  |
| 28 | `duration_unit` | varchar | YES |  |
| 29 | `request_ts_utc` | timestamp(3) | YES |  |
| 30 | `created_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.f_machine_breadcrumbs

**Columnas:** 18

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_breadcrumb` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `sk_equipment` | bigint | YES |  |
| 4 | `organization_id` | varchar | YES |  |
| 5 | `principal_id` | varchar | YES |  |
| 6 | `event_timestamp_utc` | timestamp(3) | YES |  |
| 7 | `location_lat` | decimal(10,7) | YES |  |
| 8 | `location_lon` | decimal(10,7) | YES |  |
| 9 | `location_altitude` | decimal(10,2) | YES |  |
| 10 | `machine_status` | varchar | YES |  |
| 11 | `request_status` | varchar | YES |  |
| 12 | `request_http_code` | integer | YES |  |
| 13 | `request_ts_utc` | timestamp(3) | YES |  |
| 14 | `request_date_utc` | date | YES |  |
| 15 | `days_since_last_signal` | integer | YES |  |
| 16 | `signal_range_label` | varchar | YES |  |
| 17 | `status_conexao` | varchar | YES |  |
| 18 | `created_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.f_machine_device_state_reports

**Columnas:** 13

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_machine_device_state_report` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `sk_equipment` | bigint | YES |  |
| 4 | `sk_device` | bigint | YES |  |
| 5 | `organization_id` | varchar | YES |  |
| 6 | `principal_id` | varchar | YES |  |
| 7 | `request_date` | date | YES |  |
| 8 | `report_timestamp_utc` | timestamp(3) | YES |  |
| 9 | `device_id` | varchar | YES |  |
| 10 | `state_type` | varchar | YES |  |
| 11 | `state_value` | varchar | YES |  |
| 12 | `source_created_at_utc` | timestamp(3) | YES |  |
| 13 | `gold_loaded_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.f_machine_location_history

**Columnas:** 14

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_machine_location_history` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `sk_equipment` | bigint | YES |  |
| 4 | `organization_id` | varchar | YES |  |
| 5 | `principal_id` | varchar | YES |  |
| 6 | `request_date` | date | YES |  |
| 7 | `event_timestamp_utc` | timestamp(3) | YES |  |
| 8 | `location_lat` | decimal(10,7) | YES |  |
| 9 | `location_lon` | decimal(10,7) | YES |  |
| 10 | `heading` | decimal(6,2) | YES |  |
| 11 | `speed` | decimal(8,3) | YES |  |
| 12 | `speed_unit` | varchar | YES |  |
| 13 | `source_created_at_utc` | timestamp(3) | YES |  |
| 14 | `gold_loaded_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.f_machine_measurements

**Columnas:** 24

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `sk_machine_measurement` | bigint | YES |  |
| 2 | `sk_organization` | bigint | YES |  |
| 3 | `sk_equipment` | bigint | YES |  |
| 4 | `sk_machine_measurement_dim` | bigint | YES |  |
| 5 | `organization_id` | varchar | YES |  |
| 6 | `equipment_id` | varchar | YES |  |
| 7 | `principal_id` | varchar | YES |  |
| 8 | `business_date` | date | YES |  |
| 9 | `equipment_key` | varchar | YES |  |
| 10 | `technology_name` | varchar | YES |  |
| 11 | `canonical_measurement_id` | varchar | YES |  |
| 12 | `mapping_source` | varchar | YES |  |
| 13 | `mapping_level_rank` | tinyint | YES |  |
| 14 | `interval_start_utc` | timestamp(3) | YES |  |
| 15 | `interval_end_utc` | timestamp(3) | YES |  |
| 16 | `request_ts_utc` | timestamp(3) | YES |  |
| 17 | `gold_loaded_at_utc` | timestamp(3) | YES |  |
| 18 | `measurement_value` | double | YES |  |
| 19 | `measurement_count` | integer | YES |  |
| 20 | `sequence_number` | integer | YES |  |
| 21 | `measure_unit` | varchar | YES |  |
| 22 | `raw_measurement_name` | varchar | YES |  |
| 23 | `raw_measurement_id` | varchar | YES |  |
| 24 | `created_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.measurement_exclusions

**Columnas:** 5

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `raw_measurement_name` | varchar | YES |  |
| 2 | `reason` | varchar | YES |  |
| 3 | `is_active` | boolean | YES |  |
| 4 | `created_at_utc` | timestamp(3) | YES |  |
| 5 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.measurement_mapping_by_equipment_key

**Columnas:** 7

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `equipment_key` | varchar | YES |  |
| 2 | `canonical_technology_name` | varchar | YES |  |
| 3 | `canonical_measurement_id` | varchar | YES |  |
| 4 | `description` | varchar | YES |  |
| 5 | `is_active` | boolean | YES |  |
| 6 | `created_at_utc` | timestamp(3) | YES |  |
| 7 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.measurement_mapping_default_by_type

**Columnas:** 7

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `canonical_technology_name` | varchar | YES |  |
| 2 | `equipment_type` | varchar | YES |  |
| 3 | `canonical_measurement_id` | varchar | YES |  |
| 4 | `description` | varchar | YES |  |
| 5 | `is_active` | boolean | YES |  |
| 6 | `created_at_utc` | timestamp(3) | YES |  |
| 7 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.measurement_mapping_default_general

**Columnas:** 6

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `canonical_technology_name` | varchar | YES |  |
| 2 | `canonical_measurement_id` | varchar | YES |  |
| 3 | `description` | varchar | YES |  |
| 4 | `is_active` | boolean | YES |  |
| 5 | `created_at_utc` | timestamp(3) | YES |  |
| 6 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.measurement_mapping_equipment_exceptions

**Columnas:** 7

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `equipment_id` | varchar | YES |  |
| 2 | `canonical_technology_name` | varchar | YES |  |
| 3 | `canonical_measurement_id` | varchar | YES |  |
| 4 | `description` | varchar | YES |  |
| 5 | `is_active` | boolean | YES |  |
| 6 | `created_at_utc` | timestamp(3) | YES |  |
| 7 | `updated_at_utc` | timestamp(3) | YES |  |

### sonardd_jdoc_analytics_cr.measurement_sequence_definitions

**Columnas:** 10

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `canonical_measurement_id` | varchar | YES |  |
| 2 | `canonical_technology_name` | varchar | YES |  |
| 3 | `sequence_number` | integer | YES |  |
| 4 | `sequence_description` | varchar | YES |  |
| 5 | `is_range_indicator` | boolean | YES |  |
| 6 | `min_value` | double | YES |  |
| 7 | `max_value` | double | YES |  |
| 8 | `is_active` | boolean | YES |  |
| 9 | `created_at_utc` | timestamp(3) | YES |  |
| 10 | `updated_at_utc` | timestamp(3) | YES |  |

## 🥉 sonardd_jdoc_data_core_cr

`Capa: Bronce / Raw`

### sonardd_jdoc_data_core_cr.api_error_logs_dt

**Columnas:** 18

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `endpoint_base` | varchar | YES |  |
| 4 | `principal_id` | varchar | YES |  |
| 5 | `machine_name` | varchar | YES |  |
| 6 | `error_type` | varchar | YES |  |
| 7 | `error_code` | varchar | YES |  |
| 8 | `error_message` | varchar | YES |  |
| 9 | `error_details` | varchar | YES |  |
| 10 | `script_name` | varchar | YES |  |
| 11 | `execution_mode` | varchar | YES |  |
| 12 | `request_params` | varchar | YES |  |
| 13 | `retry_count` | integer | YES |  |
| 14 | `resolved` | boolean | YES |  |
| 15 | `resolution_timestamp` | timestamp(3) | YES |  |
| 16 | `occurred_at` | timestamp(3) | YES |  |
| 17 | `created_at` | timestamp(3) | YES |  |
| 18 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.boundaries_dt

**Columnas:** 25

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `field_id` | varchar | YES |  |
| 4 | `name` | varchar | YES |  |
| 5 | `source_type` | varchar | YES |  |
| 6 | `created_time` | timestamp(3) | YES |  |
| 7 | `modified_time` | timestamp(3) | YES |  |
| 8 | `area_value` | decimal(18,6) | YES |  |
| 9 | `area_unit` | varchar | YES |  |
| 10 | `workable_area_value` | decimal(18,6) | YES |  |
| 11 | `workable_area_unit` | varchar | YES |  |
| 12 | `extent_top_left_lat` | decimal(10,8) | YES |  |
| 13 | `extent_top_left_lon` | decimal(11,8) | YES |  |
| 14 | `extent_bottom_right_lat` | decimal(10,8) | YES |  |
| 15 | `extent_bottom_right_lon` | decimal(11,8) | YES |  |
| 16 | `center_lat` | decimal(10,8) | YES |  |
| 17 | `center_lon` | decimal(11,8) | YES |  |
| 18 | `archived` | boolean | YES |  |
| 19 | `active` | boolean | YES |  |
| 20 | `irrigated` | boolean | YES |  |
| 21 | `multipolygons_json` | varchar | YES |  |
| 22 | `total_polygons` | integer | YES |  |
| 23 | `total_points` | integer | YES |  |
| 24 | `created_at` | timestamp(3) | YES |  |
| 25 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.client_farms_dt

**Columnas:** 9

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `client_id` | varchar | YES |  |
| 4 | `name` | varchar | YES |  |
| 5 | `archived` | boolean | YES |  |
| 6 | `client_uri` | varchar | YES |  |
| 7 | `api_type` | varchar | YES |  |
| 8 | `created_at` | timestamp(3) | YES |  |
| 9 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.clients_dt

**Columnas:** 16

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `api_type` | varchar | YES |  |
| 4 | `name` | varchar | YES |  |
| 5 | `archived` | boolean | YES |  |
| 6 | `user_creation_timestamp` | timestamp(3) | YES |  |
| 7 | `created_by_user` | varchar | YES |  |
| 8 | `created_by_source_system_uri` | varchar | YES |  |
| 9 | `created_by_source_node` | varchar | YES |  |
| 10 | `user_last_modified_timestamp` | timestamp(3) | YES |  |
| 11 | `last_modified_by_user` | varchar | YES |  |
| 12 | `last_modified_by_source_system_uri` | varchar | YES |  |
| 13 | `last_modified_by_source_node` | varchar | YES |  |
| 14 | `content_hash` | varchar | YES |  |
| 15 | `created_at` | timestamp(3) | YES |  |
| 16 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.croptype_equipment_types_dt

**Columnas:** 6

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `croptype_id` | varchar | YES |  |
| 3 | `equipment_type_id` | varchar | YES |  |
| 4 | `equipment_type_name` | varchar | YES |  |
| 5 | `created_at` | timestamp(3) | YES |  |
| 6 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.croptypes_dt

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `api_type` | varchar | YES |  |
| 3 | `name` | varchar | YES |  |
| 4 | `translated_name` | varchar | YES |  |
| 5 | `color` | varchar | YES |  |
| 6 | `density_factor_value` | decimal(18,6) | YES |  |
| 7 | `density_factor_unit` | varchar | YES |  |
| 8 | `standard_payable_moisture_value` | decimal(18,6) | YES |  |
| 9 | `standard_payable_moisture_unit` | varchar | YES |  |
| 10 | `content_hash` | varchar | YES |  |
| 11 | `created_at` | timestamp(3) | YES |  |
| 12 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.devices_dt

**Columnas:** 38

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `api_type` | varchar | YES |  |
| 4 | `serial_number` | varchar | YES |  |
| 5 | `make_id` | varchar | YES |  |
| 6 | `make_name` | varchar | YES |  |
| 7 | `type_id` | varchar | YES |  |
| 8 | `type_name` | varchar | YES |  |
| 9 | `type_common_name` | varchar | YES |  |
| 10 | `model_id` | varchar | YES |  |
| 11 | `model_name` | varchar | YES |  |
| 12 | `firmware_version` | varchar | YES |  |
| 13 | `organization_role_type` | varchar | YES |  |
| 14 | `organization_role_effective_ts` | timestamp(3) | YES |  |
| 15 | `organization_role_event` | varchar | YES |  |
| 16 | `organization_role_in_possession` | boolean | YES |  |
| 17 | `archived` | boolean | YES |  |
| 18 | `decommissioned` | boolean | YES |  |
| 19 | `stolen` | boolean | YES |  |
| 20 | `principal_id` | varchar | YES |  |
| 21 | `messages_restricted` | boolean | YES |  |
| 22 | `pairing_status` | varchar | YES |  |
| 23 | `high_fidelity_config_version` | varchar | YES |  |
| 24 | `generic_config_version` | varchar | YES |  |
| 25 | `erid` | varchar | YES |  |
| 26 | `equipment_principal_id` | varchar | YES |  |
| 27 | `equipment_id` | varchar | YES |  |
| 28 | `equipment_organization_id` | varchar | YES |  |
| 29 | `content_hash` | varchar | YES |  |
| 30 | `first_seen_at` | timestamp(3) | YES |  |
| 31 | `last_seen_at` | timestamp(3) | YES |  |
| 32 | `is_active` | boolean | YES |  |
| 33 | `absence_count` | integer | YES |  |
| 34 | `inactivated_at` | timestamp(3) | YES |  |
| 35 | `reactivated_at` | timestamp(3) | YES |  |
| 36 | `last_change_at` | timestamp(3) | YES |  |
| 37 | `created_at` | timestamp(3) | YES |  |
| 38 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.engine_hours_dt

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `principal_id` | varchar | YES |  |
| 4 | `report_time` | timestamp(3) | YES |  |
| 5 | `hours_value` | decimal(12,2) | YES |  |
| 6 | `hours_unit` | varchar | YES |  |
| 7 | `created_at` | timestamp(3) | YES |  |
| 8 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.equipment_dt

**Columnas:** 38

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `api_type` | varchar | YES |  |
| 4 | `name` | varchar | YES |  |
| 5 | `serial_number` | varchar | YES |  |
| 6 | `engine_serial_number` | varchar | YES |  |
| 7 | `is_serial_number_certified` | boolean | YES |  |
| 8 | `model_year` | integer | YES |  |
| 9 | `make_id` | varchar | YES |  |
| 10 | `make_name` | varchar | YES |  |
| 11 | `make_certified` | boolean | YES |  |
| 12 | `make_deere_or_subsidiary` | boolean | YES |  |
| 13 | `type_id` | varchar | YES |  |
| 14 | `type_name` | varchar | YES |  |
| 15 | `isg_type_id` | varchar | YES |  |
| 16 | `isg_type_name` | varchar | YES |  |
| 17 | `model_id` | varchar | YES |  |
| 18 | `model_name` | varchar | YES |  |
| 19 | `model_certified` | boolean | YES |  |
| 20 | `principal_id` | varchar | YES |  |
| 21 | `telematics_capable` | boolean | YES |  |
| 22 | `archived` | boolean | YES |  |
| 23 | `organization_role_type` | varchar | YES |  |
| 24 | `organization_role_effective_ts` | timestamp(3) | YES |  |
| 25 | `organization_role_effective_tz_offset_min` | integer | YES |  |
| 26 | `organization_role_event` | varchar | YES |  |
| 27 | `is_csc` | boolean | YES |  |
| 28 | `erid` | varchar | YES |  |
| 29 | `content_hash` | varchar | YES |  |
| 30 | `first_seen_at` | timestamp(3) | YES |  |
| 31 | `last_seen_at` | timestamp(3) | YES |  |
| 32 | `is_active` | boolean | YES |  |
| 33 | `absence_count` | integer | YES |  |
| 34 | `inactivated_at` | timestamp(3) | YES |  |
| 35 | `reactivated_at` | timestamp(3) | YES |  |
| 36 | `last_change_at` | timestamp(3) | YES |  |
| 37 | `created_at` | timestamp(3) | YES |  |
| 38 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.farm_clients_dt

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `farm_id` | varchar | YES |  |
| 4 | `name` | varchar | YES |  |
| 5 | `archived` | boolean | YES |  |
| 6 | `api_type` | varchar | YES |  |
| 7 | `created_at` | timestamp(3) | YES |  |
| 8 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.farms_dt

**Columnas:** 17

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `name` | varchar | YES |  |
| 4 | `archived` | boolean | YES |  |
| 5 | `client_uri` | varchar | YES |  |
| 6 | `api_type` | varchar | YES |  |
| 7 | `user_creation_timestamp` | timestamp(3) | YES |  |
| 8 | `created_by_user` | varchar | YES |  |
| 9 | `created_by_source_system_uri` | varchar | YES |  |
| 10 | `created_by_source_node` | varchar | YES |  |
| 11 | `user_last_modified_timestamp` | timestamp(3) | YES |  |
| 12 | `last_modified_by_user` | varchar | YES |  |
| 13 | `last_modified_by_source_system_uri` | varchar | YES |  |
| 14 | `last_modified_by_source_node` | varchar | YES |  |
| 15 | `record_metadata_type` | varchar | YES |  |
| 16 | `created_at` | timestamp(3) | YES |  |
| 17 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.field_operation_machine_operators_dt

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `organization_id` | varchar | YES |  |
| 2 | `field_id` | varchar | YES |  |
| 3 | `operation_id` | varchar | YES |  |
| 4 | `machine_id` | varchar | YES |  |
| 5 | `machine_guid` | varchar | YES |  |
| 6 | `machine_erid` | varchar | YES |  |
| 7 | `machine_vin` | varchar | YES |  |
| 8 | `operator_id` | varchar | YES |  |
| 9 | `operator_name` | varchar | YES |  |
| 10 | `request_ts_utc` | timestamp(3) | YES |  |
| 11 | `created_at` | timestamp(3) | YES |  |
| 12 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.field_operation_machines_dt

**Columnas:** 10

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `organization_id` | varchar | YES |  |
| 2 | `field_id` | varchar | YES |  |
| 3 | `operation_id` | varchar | YES |  |
| 4 | `machine_id` | varchar | YES |  |
| 5 | `vin` | varchar | YES |  |
| 6 | `guid` | varchar | YES |  |
| 7 | `erid` | varchar | YES |  |
| 8 | `request_ts_utc` | timestamp(3) | YES |  |
| 9 | `created_at` | timestamp(3) | YES |  |
| 10 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.field_operation_measurement_totals_dt

**Columnas:** 34

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `organization_id` | varchar | YES |  |
| 2 | `operation_id` | varchar | YES |  |
| 3 | `field_id` | varchar | YES |  |
| 4 | `measurement_name` | varchar | YES |  |
| 5 | `measurement_category` | varchar | YES |  |
| 6 | `total_type` | varchar | YES |  |
| 7 | `item_type` | varchar | YES |  |
| 8 | `item_id` | varchar | YES |  |
| 9 | `item_name` | varchar | YES |  |
| 10 | `area_value` | double | YES |  |
| 11 | `area_unit` | varchar | YES |  |
| 12 | `applied_area_value` | double | YES |  |
| 13 | `applied_area_unit` | varchar | YES |  |
| 14 | `average_speed_value` | double | YES |  |
| 15 | `average_speed_unit` | varchar | YES |  |
| 16 | `average_depth_value` | double | YES |  |
| 17 | `average_depth_unit` | varchar | YES |  |
| 18 | `yield_value` | double | YES |  |
| 19 | `yield_unit` | varchar | YES |  |
| 20 | `average_yield_value` | double | YES |  |
| 21 | `average_yield_unit` | varchar | YES |  |
| 22 | `average_moisture_value` | double | YES |  |
| 23 | `average_moisture_unit` | varchar | YES |  |
| 24 | `wet_mass_value` | double | YES |  |
| 25 | `wet_mass_unit` | varchar | YES |  |
| 26 | `average_wet_mass_value` | double | YES |  |
| 27 | `average_wet_mass_unit` | varchar | YES |  |
| 28 | `total_material_value` | double | YES |  |
| 29 | `total_material_unit` | varchar | YES |  |
| 30 | `average_material_value` | double | YES |  |
| 31 | `average_material_unit` | varchar | YES |  |
| 32 | `request_ts_utc` | timestamp(3) | YES |  |
| 33 | `created_at` | timestamp(3) | YES |  |
| 34 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.field_operation_measurements_dt

**Columnas:** 28

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `organization_id` | varchar | YES |  |
| 2 | `operation_id` | varchar | YES |  |
| 3 | `field_id` | varchar | YES |  |
| 4 | `measurement_name` | varchar | YES |  |
| 5 | `measurement_category` | varchar | YES |  |
| 6 | `area_value` | double | YES |  |
| 7 | `area_unit` | varchar | YES |  |
| 8 | `average_speed_value` | double | YES |  |
| 9 | `average_speed_unit` | varchar | YES |  |
| 10 | `average_depth_value` | double | YES |  |
| 11 | `average_depth_unit` | varchar | YES |  |
| 12 | `yield_value` | double | YES |  |
| 13 | `yield_unit` | varchar | YES |  |
| 14 | `average_yield_value` | double | YES |  |
| 15 | `average_yield_unit` | varchar | YES |  |
| 16 | `average_moisture_value` | double | YES |  |
| 17 | `average_moisture_unit` | varchar | YES |  |
| 18 | `wet_mass_value` | double | YES |  |
| 19 | `wet_mass_unit` | varchar | YES |  |
| 20 | `average_wet_mass_value` | double | YES |  |
| 21 | `average_wet_mass_unit` | varchar | YES |  |
| 22 | `total_material_value` | double | YES |  |
| 23 | `total_material_unit` | varchar | YES |  |
| 24 | `average_material_value` | double | YES |  |
| 25 | `average_material_unit` | varchar | YES |  |
| 26 | `request_ts_utc` | timestamp(3) | YES |  |
| 27 | `created_at` | timestamp(3) | YES |  |
| 28 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.field_operation_products_dt

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `organization_id` | varchar | YES |  |
| 2 | `field_id` | varchar | YES |  |
| 3 | `operation_id` | varchar | YES |  |
| 4 | `product_kind` | varchar | YES |  |
| 5 | `item_type` | varchar | YES |  |
| 6 | `guid` | varchar | YES |  |
| 7 | `product_type` | varchar | YES |  |
| 8 | `product_id` | varchar | YES |  |
| 9 | `name` | varchar | YES |  |
| 10 | `brand` | varchar | YES |  |
| 11 | `tank_mix` | boolean | YES |  |
| 12 | `tillage_type` | varchar | YES |  |
| 13 | `request_ts_utc` | timestamp(3) | YES |  |
| 14 | `created_at` | timestamp(3) | YES |  |
| 15 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.field_operations_dt

**Columnas:** 18

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `organization_id` | varchar | YES |  |
| 2 | `field_id` | varchar | YES |  |
| 3 | `operation_id` | varchar | YES |  |
| 4 | `operation_type` | varchar | YES |  |
| 5 | `crop_season` | varchar | YES |  |
| 6 | `dt_modified` | timestamp(3) | YES |  |
| 7 | `dt_modified_raw` | varchar | YES |  |
| 8 | `dt_modified_prev` | timestamp(3) | YES |  |
| 9 | `dt_start` | timestamp(3) | YES |  |
| 10 | `dt_end` | timestamp(3) | YES |  |
| 11 | `treated_crop_name` | varchar | YES |  |
| 12 | `crop_name` | varchar | YES |  |
| 13 | `adapt_machine_type` | varchar | YES |  |
| 14 | `st_changed` | varchar | YES |  |
| 15 | `dt_last_sync` | timestamp(3) | YES |  |
| 16 | `request_ts_utc` | timestamp(3) | YES |  |
| 17 | `created_at` | timestamp(3) | YES |  |
| 18 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.fields_dt

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `name` | varchar | YES |  |
| 4 | `archived` | boolean | YES |  |
| 5 | `last_modified_time` | timestamp(3) | YES |  |
| 6 | `api_type` | varchar | YES |  |
| 7 | `primary_client_id` | varchar | YES |  |
| 8 | `primary_client_name` | varchar | YES |  |
| 9 | `primary_client_type` | varchar | YES |  |
| 10 | `primary_farm_id` | varchar | YES |  |
| 11 | `primary_farm_name` | varchar | YES |  |
| 12 | `primary_farm_client_uri` | varchar | YES |  |
| 13 | `primary_farm_type` | varchar | YES |  |
| 14 | `created_at` | timestamp(3) | YES |  |
| 15 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.flag_geometries_dt

**Columnas:** 7

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `flag_id` | varchar | YES |  |
| 4 | `geometry_type` | varchar | YES |  |
| 5 | `coordinates` | varchar | YES |  |
| 6 | `created_at` | timestamp(3) | YES |  |
| 7 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.flags_dt

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `api_type` | varchar | YES |  |
| 4 | `name` | varchar | YES |  |
| 5 | `color` | varchar | YES |  |
| 6 | `shape` | varchar | YES |  |
| 7 | `archived` | boolean | YES |  |
| 8 | `note` | varchar | YES |  |
| 9 | `created_time` | timestamp(3) | YES |  |
| 10 | `modified_time` | timestamp(3) | YES |  |
| 11 | `created_at` | timestamp(3) | YES |  |
| 12 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.guidance_lines_dt

**Columnas:** 10

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `field_id` | varchar | YES |  |
| 4 | `api_type` | varchar | YES |  |
| 5 | `name` | varchar | YES |  |
| 6 | `guidance_type` | varchar | YES |  |
| 7 | `archived` | boolean | YES |  |
| 8 | `coordinates` | varchar | YES |  |
| 9 | `created_at` | timestamp(3) | YES |  |
| 10 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.hours_of_operation_dt

**Columnas:** 9

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `principal_id` | varchar | YES |  |
| 4 | `start_date` | timestamp(3) | YES |  |
| 5 | `end_date` | timestamp(3) | YES |  |
| 6 | `engine_state` | integer | YES |  |
| 7 | `duration_hours` | decimal(12,6) | YES |  |
| 8 | `created_at` | timestamp(3) | YES |  |
| 9 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.machine_alerts_dt

**Columnas:** 28

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `principal_id` | varchar | YES |  |
| 4 | `alert_id` | varchar | YES |  |
| 5 | `alert_timestamp` | timestamp(3) | YES |  |
| 6 | `alert_type` | varchar | YES |  |
| 7 | `severity` | varchar | YES |  |
| 8 | `description` | varchar | YES |  |
| 9 | `dtc_code` | varchar | YES |  |
| 10 | `source` | varchar | YES |  |
| 11 | `status` | varchar | YES |  |
| 12 | `color` | varchar | YES |  |
| 13 | `location_lat` | double | YES |  |
| 14 | `location_lon` | double | YES |  |
| 15 | `occurrences` | integer | YES |  |
| 16 | `engine_hours_value` | double | YES |  |
| 17 | `engine_hours_unit` | varchar | YES |  |
| 18 | `machine_linear_time` | bigint | YES |  |
| 19 | `three_letter_acronym` | varchar | YES |  |
| 20 | `nm_suspect_parameter` | varchar | YES |  |
| 21 | `failure_mode_indicator` | integer | YES |  |
| 22 | `definition_id` | varchar | YES |  |
| 23 | `ignored` | boolean | YES |  |
| 24 | `invisible` | boolean | YES |  |
| 25 | `duration_value` | integer | YES |  |
| 26 | `duration_unit` | varchar | YES |  |
| 27 | `created_at` | timestamp(3) | YES |  |
| 28 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.machine_breadcrumbs_dt

**Columnas:** 17

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `principal_id` | varchar | YES |  |
| 4 | `event_timestamp` | timestamp(3) | YES |  |
| 5 | `event_sequence` | integer | YES |  |
| 6 | `location_lat` | decimal(10,7) | YES |  |
| 7 | `location_lon` | decimal(10,7) | YES |  |
| 8 | `location_altitude` | decimal(10,2) | YES |  |
| 9 | `heading` | decimal(6,2) | YES |  |
| 10 | `speed` | decimal(8,3) | YES |  |
| 11 | `speed_unit` | varchar | YES |  |
| 12 | `machine_status` | varchar | YES |  |
| 13 | `request_status` | varchar | YES |  |
| 14 | `request_http_code` | integer | YES |  |
| 15 | `request_ts_utc` | timestamp(3) | YES |  |
| 16 | `created_at` | timestamp(3) | YES |  |
| 17 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.machine_device_state_reports_dt

**Columnas:** 9

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `principal_id` | varchar | YES |  |
| 4 | `report_timestamp` | timestamp(3) | YES |  |
| 5 | `device_id` | varchar | YES |  |
| 6 | `state_type` | varchar | YES |  |
| 7 | `state_value` | varchar | YES |  |
| 8 | `created_at` | timestamp(3) | YES |  |
| 9 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.machine_location_history_dt

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `principal_id` | varchar | YES |  |
| 4 | `event_timestamp` | timestamp(3) | YES |  |
| 5 | `location_lat` | decimal(10,7) | YES |  |
| 6 | `location_lon` | decimal(10,7) | YES |  |
| 7 | `location_altitude` | decimal(10,2) | YES |  |
| 8 | `heading` | decimal(6,2) | YES |  |
| 9 | `speed` | decimal(8,3) | YES |  |
| 10 | `speed_unit` | varchar | YES |  |
| 11 | `created_at` | timestamp(3) | YES |  |
| 12 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.machine_measurements_dt

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `equipment_id` | varchar | YES |  |
| 4 | `principal_id` | varchar | YES |  |
| 5 | `measurement_id` | varchar | YES |  |
| 6 | `measurement_name` | varchar | YES |  |
| 7 | `sequence_number` | integer | YES |  |
| 8 | `interval_start_utc` | timestamp(3) | YES |  |
| 9 | `interval_end_utc` | timestamp(3) | YES |  |
| 10 | `actual_start_utc` | timestamp(3) | YES |  |
| 11 | `actual_end_utc` | timestamp(3) | YES |  |
| 12 | `business_date` | date | YES |  |
| 13 | `measurement_value` | double | YES |  |
| 14 | `measurement_count` | integer | YES |  |
| 15 | `measure_unit` | varchar | YES |  |
| 16 | `aggregation_type` | varchar | YES |  |
| 17 | `aggregation_type_id` | varchar | YES |  |
| 18 | `measurement_type` | varchar | YES |  |
| 19 | `ui_visible_indicator` | varchar | YES |  |
| 20 | `definition_description` | varchar | YES |  |
| 21 | `network_type` | varchar | YES |  |
| 22 | `request_start_utc` | timestamp(3) | YES |  |
| 23 | `request_end_utc` | timestamp(3) | YES |  |
| 24 | `request_ts_utc` | timestamp(3) | YES |  |
| 25 | `bucket_sequence_description` | varchar | YES |  |
| 26 | `bucket_range_indicator` | boolean | YES |  |
| 27 | `bucket_min_value` | double | YES |  |
| 28 | `bucket_max_value` | double | YES |  |
| 29 | `created_at` | timestamp(3) | YES |  |
| 30 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.operators_dt

**Columnas:** 20

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `api_type` | varchar | YES |  |
| 4 | `name` | varchar | YES |  |
| 5 | `first_name` | varchar | YES |  |
| 6 | `last_name` | varchar | YES |  |
| 7 | `archived` | boolean | YES |  |
| 8 | `guid` | varchar | YES |  |
| 9 | `date_modified` | timestamp(3) | YES |  |
| 10 | `user_creation_timestamp` | timestamp(3) | YES |  |
| 11 | `created_by_user` | varchar | YES |  |
| 12 | `created_by_source_system_uri` | varchar | YES |  |
| 13 | `created_by_source_node` | varchar | YES |  |
| 14 | `user_last_modified_timestamp` | timestamp(3) | YES |  |
| 15 | `last_modified_by_user` | varchar | YES |  |
| 16 | `last_modified_by_source_system_uri` | varchar | YES |  |
| 17 | `last_modified_by_source_node` | varchar | YES |  |
| 18 | `content_hash` | varchar | YES |  |
| 19 | `created_at` | timestamp(3) | YES |  |
| 20 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.organizations_dt

**Columnas:** 18

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `api_type` | varchar | YES |  |
| 3 | `name` | varchar | YES |  |
| 4 | `type` | varchar | YES |  |
| 5 | `member` | boolean | YES |  |
| 6 | `internal` | boolean | YES |  |
| 7 | `hierarchy_enabled` | boolean | YES |  |
| 8 | `need_connection` | boolean | YES |  |
| 9 | `content_hash` | varchar | YES |  |
| 10 | `first_seen_at` | timestamp(3) | YES |  |
| 11 | `last_seen_at` | timestamp(3) | YES |  |
| 12 | `is_active` | boolean | YES |  |
| 13 | `absence_count` | integer | YES |  |
| 14 | `inactivated_at` | timestamp(3) | YES |  |
| 15 | `reactivated_at` | timestamp(3) | YES |  |
| 16 | `last_change_at` | timestamp(3) | YES |  |
| 17 | `created_at` | timestamp(3) | YES |  |
| 18 | `updated_at` | timestamp(3) | YES |  |

### sonardd_jdoc_data_core_cr.sync_executions_dt

**Columnas:** 13

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `script_name` | varchar | YES |  |
| 4 | `execution_mode` | varchar | YES |  |
| 5 | `status` | varchar | YES |  |
| 6 | `started_at` | timestamp(3) | YES |  |
| 7 | `finished_at` | timestamp(3) | YES |  |
| 8 | `records_processed` | integer | YES |  |
| 9 | `records_inserted` | integer | YES |  |
| 10 | `records_updated` | integer | YES |  |
| 11 | `error_message` | varchar | YES |  |
| 12 | `created_at` | timestamp(3) | YES |  |
| 13 | `updated_at` | timestamp(3) | YES |  |

## 🥉 sonnard_jdoc_data_core

`Capa: Bronce / Raw`

### sonnard_jdoc_data_core.api_error_logs_dt

**Columnas:** 18

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `endpoint_base` | varchar | YES |  |
| 4 | `principal_id` | varchar | YES |  |
| 5 | `machine_name` | varchar | YES |  |
| 6 | `error_type` | varchar | YES |  |
| 7 | `error_code` | varchar | YES |  |
| 8 | `error_message` | varchar | YES |  |
| 9 | `error_details` | varchar | YES |  |
| 10 | `script_name` | varchar | YES |  |
| 11 | `execution_mode` | varchar | YES |  |
| 12 | `request_params` | varchar | YES |  |
| 13 | `retry_count` | integer | YES |  |
| 14 | `resolved` | boolean | YES |  |
| 15 | `resolution_timestamp` | timestamp(3) | YES |  |
| 16 | `occurred_at` | timestamp(3) | YES |  |
| 17 | `created_at` | timestamp(3) | YES |  |
| 18 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.boundaries_dt

**Columnas:** 25

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `field_id` | varchar | YES |  |
| 4 | `name` | varchar | YES |  |
| 5 | `source_type` | varchar | YES |  |
| 6 | `created_time` | timestamp(3) | YES |  |
| 7 | `modified_time` | timestamp(3) | YES |  |
| 8 | `area_value` | decimal(18,6) | YES |  |
| 9 | `area_unit` | varchar | YES |  |
| 10 | `workable_area_value` | decimal(18,6) | YES |  |
| 11 | `workable_area_unit` | varchar | YES |  |
| 12 | `extent_top_left_lat` | decimal(10,8) | YES |  |
| 13 | `extent_top_left_lon` | decimal(11,8) | YES |  |
| 14 | `extent_bottom_right_lat` | decimal(10,8) | YES |  |
| 15 | `extent_bottom_right_lon` | decimal(11,8) | YES |  |
| 16 | `center_lat` | decimal(10,8) | YES |  |
| 17 | `center_lon` | decimal(11,8) | YES |  |
| 18 | `archived` | boolean | YES |  |
| 19 | `active` | boolean | YES |  |
| 20 | `irrigated` | boolean | YES |  |
| 21 | `multipolygons_json` | varchar | YES |  |
| 22 | `total_polygons` | integer | YES |  |
| 23 | `total_points` | integer | YES |  |
| 24 | `created_at` | timestamp(3) | YES |  |
| 25 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.client_farms_dt

**Columnas:** 9

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `client_id` | varchar | YES |  |
| 4 | `name` | varchar | YES |  |
| 5 | `archived` | boolean | YES |  |
| 6 | `client_uri` | varchar | YES |  |
| 7 | `api_type` | varchar | YES |  |
| 8 | `created_at` | timestamp(3) | YES |  |
| 9 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.clients_dt

**Columnas:** 16

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `api_type` | varchar | YES |  |
| 4 | `name` | varchar | YES |  |
| 5 | `archived` | boolean | YES |  |
| 6 | `user_creation_timestamp` | timestamp(3) | YES |  |
| 7 | `created_by_user` | varchar | YES |  |
| 8 | `created_by_source_system_uri` | varchar | YES |  |
| 9 | `created_by_source_node` | varchar | YES |  |
| 10 | `user_last_modified_timestamp` | timestamp(3) | YES |  |
| 11 | `last_modified_by_user` | varchar | YES |  |
| 12 | `last_modified_by_source_system_uri` | varchar | YES |  |
| 13 | `last_modified_by_source_node` | varchar | YES |  |
| 14 | `content_hash` | varchar | YES |  |
| 15 | `created_at` | timestamp(3) | YES |  |
| 16 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.croptype_equipment_types_dt

**Columnas:** 6

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `croptype_id` | varchar | YES |  |
| 3 | `equipment_type_id` | varchar | YES |  |
| 4 | `equipment_type_name` | varchar | YES |  |
| 5 | `created_at` | timestamp(3) | YES |  |
| 6 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.croptypes_dt

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `api_type` | varchar | YES |  |
| 3 | `name` | varchar | YES |  |
| 4 | `translated_name` | varchar | YES |  |
| 5 | `color` | varchar | YES |  |
| 6 | `density_factor_value` | decimal(18,6) | YES |  |
| 7 | `density_factor_unit` | varchar | YES |  |
| 8 | `standard_payable_moisture_value` | decimal(18,6) | YES |  |
| 9 | `standard_payable_moisture_unit` | varchar | YES |  |
| 10 | `content_hash` | varchar | YES |  |
| 11 | `created_at` | timestamp(3) | YES |  |
| 12 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.devices_dt

**Columnas:** 38

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `api_type` | varchar | YES |  |
| 4 | `serial_number` | varchar | YES |  |
| 5 | `make_id` | varchar | YES |  |
| 6 | `make_name` | varchar | YES |  |
| 7 | `type_id` | varchar | YES |  |
| 8 | `type_name` | varchar | YES |  |
| 9 | `type_common_name` | varchar | YES |  |
| 10 | `model_id` | varchar | YES |  |
| 11 | `model_name` | varchar | YES |  |
| 12 | `firmware_version` | varchar | YES |  |
| 13 | `organization_role_type` | varchar | YES |  |
| 14 | `organization_role_effective_ts` | timestamp(3) | YES |  |
| 15 | `organization_role_event` | varchar | YES |  |
| 16 | `organization_role_in_possession` | boolean | YES |  |
| 17 | `archived` | boolean | YES |  |
| 18 | `decommissioned` | boolean | YES |  |
| 19 | `stolen` | boolean | YES |  |
| 20 | `principal_id` | varchar | YES |  |
| 21 | `messages_restricted` | boolean | YES |  |
| 22 | `pairing_status` | varchar | YES |  |
| 23 | `high_fidelity_config_version` | varchar | YES |  |
| 24 | `generic_config_version` | varchar | YES |  |
| 25 | `erid` | varchar | YES |  |
| 26 | `equipment_principal_id` | varchar | YES |  |
| 27 | `equipment_id` | varchar | YES |  |
| 28 | `equipment_organization_id` | varchar | YES |  |
| 29 | `content_hash` | varchar | YES |  |
| 30 | `first_seen_at` | timestamp(3) | YES |  |
| 31 | `last_seen_at` | timestamp(3) | YES |  |
| 32 | `is_active` | boolean | YES |  |
| 33 | `absence_count` | integer | YES |  |
| 34 | `inactivated_at` | timestamp(3) | YES |  |
| 35 | `reactivated_at` | timestamp(3) | YES |  |
| 36 | `last_change_at` | timestamp(3) | YES |  |
| 37 | `created_at` | timestamp(3) | YES |  |
| 38 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.engine_hours_dt

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `principal_id` | varchar | YES |  |
| 4 | `report_time` | timestamp(3) | YES |  |
| 5 | `hours_value` | decimal(12,2) | YES |  |
| 6 | `hours_unit` | varchar | YES |  |
| 7 | `created_at` | timestamp(3) | YES |  |
| 8 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.equipment_dt

**Columnas:** 38

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `api_type` | varchar | YES |  |
| 4 | `name` | varchar | YES |  |
| 5 | `serial_number` | varchar | YES |  |
| 6 | `engine_serial_number` | varchar | YES |  |
| 7 | `is_serial_number_certified` | boolean | YES |  |
| 8 | `model_year` | integer | YES |  |
| 9 | `make_id` | varchar | YES |  |
| 10 | `make_name` | varchar | YES |  |
| 11 | `make_certified` | boolean | YES |  |
| 12 | `make_deere_or_subsidiary` | boolean | YES |  |
| 13 | `type_id` | varchar | YES |  |
| 14 | `type_name` | varchar | YES |  |
| 15 | `isg_type_id` | varchar | YES |  |
| 16 | `isg_type_name` | varchar | YES |  |
| 17 | `model_id` | varchar | YES |  |
| 18 | `model_name` | varchar | YES |  |
| 19 | `model_certified` | boolean | YES |  |
| 20 | `principal_id` | varchar | YES |  |
| 21 | `telematics_capable` | boolean | YES |  |
| 22 | `archived` | boolean | YES |  |
| 23 | `organization_role_type` | varchar | YES |  |
| 24 | `organization_role_effective_ts` | timestamp(3) | YES |  |
| 25 | `organization_role_effective_tz_offset_min` | integer | YES |  |
| 26 | `organization_role_event` | varchar | YES |  |
| 27 | `is_csc` | boolean | YES |  |
| 28 | `erid` | varchar | YES |  |
| 29 | `content_hash` | varchar | YES |  |
| 30 | `first_seen_at` | timestamp(3) | YES |  |
| 31 | `last_seen_at` | timestamp(3) | YES |  |
| 32 | `is_active` | boolean | YES |  |
| 33 | `absence_count` | integer | YES |  |
| 34 | `inactivated_at` | timestamp(3) | YES |  |
| 35 | `reactivated_at` | timestamp(3) | YES |  |
| 36 | `last_change_at` | timestamp(3) | YES |  |
| 37 | `created_at` | timestamp(3) | YES |  |
| 38 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.farm_clients_dt

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `farm_id` | varchar | YES |  |
| 4 | `name` | varchar | YES |  |
| 5 | `archived` | boolean | YES |  |
| 6 | `api_type` | varchar | YES |  |
| 7 | `created_at` | timestamp(3) | YES |  |
| 8 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.farms_dt

**Columnas:** 17

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `name` | varchar | YES |  |
| 4 | `archived` | boolean | YES |  |
| 5 | `client_uri` | varchar | YES |  |
| 6 | `api_type` | varchar | YES |  |
| 7 | `user_creation_timestamp` | timestamp(3) | YES |  |
| 8 | `created_by_user` | varchar | YES |  |
| 9 | `created_by_source_system_uri` | varchar | YES |  |
| 10 | `created_by_source_node` | varchar | YES |  |
| 11 | `user_last_modified_timestamp` | timestamp(3) | YES |  |
| 12 | `last_modified_by_user` | varchar | YES |  |
| 13 | `last_modified_by_source_system_uri` | varchar | YES |  |
| 14 | `last_modified_by_source_node` | varchar | YES |  |
| 15 | `record_metadata_type` | varchar | YES |  |
| 16 | `created_at` | timestamp(3) | YES |  |
| 17 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.field_operation_machine_operators_dt

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `organization_id` | varchar | YES |  |
| 2 | `field_id` | varchar | YES |  |
| 3 | `operation_id` | varchar | YES |  |
| 4 | `machine_id` | varchar | YES |  |
| 5 | `machine_guid` | varchar | YES |  |
| 6 | `machine_erid` | varchar | YES |  |
| 7 | `machine_vin` | varchar | YES |  |
| 8 | `operator_id` | varchar | YES |  |
| 9 | `operator_name` | varchar | YES |  |
| 10 | `request_ts_utc` | timestamp(3) | YES |  |
| 11 | `created_at` | timestamp(3) | YES |  |
| 12 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.field_operation_machines_dt

**Columnas:** 10

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `organization_id` | varchar | YES |  |
| 2 | `field_id` | varchar | YES |  |
| 3 | `operation_id` | varchar | YES |  |
| 4 | `machine_id` | varchar | YES |  |
| 5 | `vin` | varchar | YES |  |
| 6 | `guid` | varchar | YES |  |
| 7 | `erid` | varchar | YES |  |
| 8 | `request_ts_utc` | timestamp(3) | YES |  |
| 9 | `created_at` | timestamp(3) | YES |  |
| 10 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.field_operation_measurement_totals_dt

**Columnas:** 34

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `organization_id` | varchar | YES |  |
| 2 | `operation_id` | varchar | YES |  |
| 3 | `field_id` | varchar | YES |  |
| 4 | `measurement_name` | varchar | YES |  |
| 5 | `measurement_category` | varchar | YES |  |
| 6 | `total_type` | varchar | YES |  |
| 7 | `item_type` | varchar | YES |  |
| 8 | `item_id` | varchar | YES |  |
| 9 | `item_name` | varchar | YES |  |
| 10 | `area_value` | double | YES |  |
| 11 | `area_unit` | varchar | YES |  |
| 12 | `applied_area_value` | double | YES |  |
| 13 | `applied_area_unit` | varchar | YES |  |
| 14 | `average_speed_value` | double | YES |  |
| 15 | `average_speed_unit` | varchar | YES |  |
| 16 | `average_depth_value` | double | YES |  |
| 17 | `average_depth_unit` | varchar | YES |  |
| 18 | `yield_value` | double | YES |  |
| 19 | `yield_unit` | varchar | YES |  |
| 20 | `average_yield_value` | double | YES |  |
| 21 | `average_yield_unit` | varchar | YES |  |
| 22 | `average_moisture_value` | double | YES |  |
| 23 | `average_moisture_unit` | varchar | YES |  |
| 24 | `wet_mass_value` | double | YES |  |
| 25 | `wet_mass_unit` | varchar | YES |  |
| 26 | `average_wet_mass_value` | double | YES |  |
| 27 | `average_wet_mass_unit` | varchar | YES |  |
| 28 | `total_material_value` | double | YES |  |
| 29 | `total_material_unit` | varchar | YES |  |
| 30 | `average_material_value` | double | YES |  |
| 31 | `average_material_unit` | varchar | YES |  |
| 32 | `request_ts_utc` | timestamp(3) | YES |  |
| 33 | `created_at` | timestamp(3) | YES |  |
| 34 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.field_operation_measurements_dt

**Columnas:** 28

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `organization_id` | varchar | YES |  |
| 2 | `operation_id` | varchar | YES |  |
| 3 | `field_id` | varchar | YES |  |
| 4 | `measurement_name` | varchar | YES |  |
| 5 | `measurement_category` | varchar | YES |  |
| 6 | `area_value` | double | YES |  |
| 7 | `area_unit` | varchar | YES |  |
| 8 | `average_speed_value` | double | YES |  |
| 9 | `average_speed_unit` | varchar | YES |  |
| 10 | `average_depth_value` | double | YES |  |
| 11 | `average_depth_unit` | varchar | YES |  |
| 12 | `yield_value` | double | YES |  |
| 13 | `yield_unit` | varchar | YES |  |
| 14 | `average_yield_value` | double | YES |  |
| 15 | `average_yield_unit` | varchar | YES |  |
| 16 | `average_moisture_value` | double | YES |  |
| 17 | `average_moisture_unit` | varchar | YES |  |
| 18 | `wet_mass_value` | double | YES |  |
| 19 | `wet_mass_unit` | varchar | YES |  |
| 20 | `average_wet_mass_value` | double | YES |  |
| 21 | `average_wet_mass_unit` | varchar | YES |  |
| 22 | `total_material_value` | double | YES |  |
| 23 | `total_material_unit` | varchar | YES |  |
| 24 | `average_material_value` | double | YES |  |
| 25 | `average_material_unit` | varchar | YES |  |
| 26 | `request_ts_utc` | timestamp(3) | YES |  |
| 27 | `created_at` | timestamp(3) | YES |  |
| 28 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.field_operation_products_dt

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `organization_id` | varchar | YES |  |
| 2 | `field_id` | varchar | YES |  |
| 3 | `operation_id` | varchar | YES |  |
| 4 | `product_kind` | varchar | YES |  |
| 5 | `item_type` | varchar | YES |  |
| 6 | `guid` | varchar | YES |  |
| 7 | `product_type` | varchar | YES |  |
| 8 | `product_id` | varchar | YES |  |
| 9 | `name` | varchar | YES |  |
| 10 | `brand` | varchar | YES |  |
| 11 | `tank_mix` | boolean | YES |  |
| 12 | `tillage_type` | varchar | YES |  |
| 13 | `request_ts_utc` | timestamp(3) | YES |  |
| 14 | `created_at` | timestamp(3) | YES |  |
| 15 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.field_operations_dt

**Columnas:** 18

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `organization_id` | varchar | YES |  |
| 2 | `field_id` | varchar | YES |  |
| 3 | `operation_id` | varchar | YES |  |
| 4 | `operation_type` | varchar | YES |  |
| 5 | `crop_season` | varchar | YES |  |
| 6 | `dt_modified` | timestamp(3) | YES |  |
| 7 | `dt_modified_raw` | varchar | YES |  |
| 8 | `dt_modified_prev` | timestamp(3) | YES |  |
| 9 | `dt_start` | timestamp(3) | YES |  |
| 10 | `dt_end` | timestamp(3) | YES |  |
| 11 | `treated_crop_name` | varchar | YES |  |
| 12 | `crop_name` | varchar | YES |  |
| 13 | `adapt_machine_type` | varchar | YES |  |
| 14 | `st_changed` | varchar | YES |  |
| 15 | `dt_last_sync` | timestamp(3) | YES |  |
| 16 | `request_ts_utc` | timestamp(3) | YES |  |
| 17 | `created_at` | timestamp(3) | YES |  |
| 18 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.fields_dt

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `name` | varchar | YES |  |
| 4 | `archived` | boolean | YES |  |
| 5 | `last_modified_time` | timestamp(3) | YES |  |
| 6 | `api_type` | varchar | YES |  |
| 7 | `primary_client_id` | varchar | YES |  |
| 8 | `primary_client_name` | varchar | YES |  |
| 9 | `primary_client_type` | varchar | YES |  |
| 10 | `primary_farm_id` | varchar | YES |  |
| 11 | `primary_farm_name` | varchar | YES |  |
| 12 | `primary_farm_client_uri` | varchar | YES |  |
| 13 | `primary_farm_type` | varchar | YES |  |
| 14 | `created_at` | timestamp(3) | YES |  |
| 15 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.flag_geometries_dt

**Columnas:** 7

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `flag_id` | varchar | YES |  |
| 4 | `geometry_type` | varchar | YES |  |
| 5 | `coordinates` | varchar | YES |  |
| 6 | `created_at` | timestamp(3) | YES |  |
| 7 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.flags_dt

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `api_type` | varchar | YES |  |
| 4 | `name` | varchar | YES |  |
| 5 | `color` | varchar | YES |  |
| 6 | `shape` | varchar | YES |  |
| 7 | `archived` | boolean | YES |  |
| 8 | `note` | varchar | YES |  |
| 9 | `created_time` | timestamp(3) | YES |  |
| 10 | `modified_time` | timestamp(3) | YES |  |
| 11 | `created_at` | timestamp(3) | YES |  |
| 12 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.guidance_lines_dt

**Columnas:** 10

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `field_id` | varchar | YES |  |
| 4 | `api_type` | varchar | YES |  |
| 5 | `name` | varchar | YES |  |
| 6 | `guidance_type` | varchar | YES |  |
| 7 | `archived` | boolean | YES |  |
| 8 | `coordinates` | varchar | YES |  |
| 9 | `created_at` | timestamp(3) | YES |  |
| 10 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.hours_of_operation_dt

**Columnas:** 9

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `principal_id` | varchar | YES |  |
| 4 | `start_date` | timestamp(3) | YES |  |
| 5 | `end_date` | timestamp(3) | YES |  |
| 6 | `engine_state` | integer | YES |  |
| 7 | `duration_hours` | decimal(12,6) | YES |  |
| 8 | `created_at` | timestamp(3) | YES |  |
| 9 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.machine_alerts_dt

**Columnas:** 28

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `principal_id` | varchar | YES |  |
| 4 | `alert_id` | varchar | YES |  |
| 5 | `alert_timestamp` | timestamp(3) | YES |  |
| 6 | `alert_type` | varchar | YES |  |
| 7 | `severity` | varchar | YES |  |
| 8 | `description` | varchar | YES |  |
| 9 | `dtc_code` | varchar | YES |  |
| 10 | `source` | varchar | YES |  |
| 11 | `status` | varchar | YES |  |
| 12 | `color` | varchar | YES |  |
| 13 | `location_lat` | double | YES |  |
| 14 | `location_lon` | double | YES |  |
| 15 | `occurrences` | integer | YES |  |
| 16 | `engine_hours_value` | double | YES |  |
| 17 | `engine_hours_unit` | varchar | YES |  |
| 18 | `machine_linear_time` | bigint | YES |  |
| 19 | `three_letter_acronym` | varchar | YES |  |
| 20 | `nm_suspect_parameter` | varchar | YES |  |
| 21 | `failure_mode_indicator` | integer | YES |  |
| 22 | `definition_id` | varchar | YES |  |
| 23 | `ignored` | boolean | YES |  |
| 24 | `invisible` | boolean | YES |  |
| 25 | `duration_value` | integer | YES |  |
| 26 | `duration_unit` | varchar | YES |  |
| 27 | `created_at` | timestamp(3) | YES |  |
| 28 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.machine_breadcrumbs_dt

**Columnas:** 17

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `principal_id` | varchar | YES |  |
| 4 | `event_timestamp` | timestamp(3) | YES |  |
| 5 | `event_sequence` | integer | YES |  |
| 6 | `location_lat` | decimal(10,7) | YES |  |
| 7 | `location_lon` | decimal(10,7) | YES |  |
| 8 | `location_altitude` | decimal(10,2) | YES |  |
| 9 | `heading` | decimal(6,2) | YES |  |
| 10 | `speed` | decimal(8,3) | YES |  |
| 11 | `speed_unit` | varchar | YES |  |
| 12 | `machine_status` | varchar | YES |  |
| 13 | `request_status` | varchar | YES |  |
| 14 | `request_http_code` | integer | YES |  |
| 15 | `request_ts_utc` | timestamp(3) | YES |  |
| 16 | `created_at` | timestamp(3) | YES |  |
| 17 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.machine_device_state_reports_dt

**Columnas:** 9

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `principal_id` | varchar | YES |  |
| 4 | `report_timestamp` | timestamp(3) | YES |  |
| 5 | `device_id` | varchar | YES |  |
| 6 | `state_type` | varchar | YES |  |
| 7 | `state_value` | varchar | YES |  |
| 8 | `created_at` | timestamp(3) | YES |  |
| 9 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.machine_location_history_dt

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `principal_id` | varchar | YES |  |
| 4 | `event_timestamp` | timestamp(3) | YES |  |
| 5 | `location_lat` | decimal(10,7) | YES |  |
| 6 | `location_lon` | decimal(10,7) | YES |  |
| 7 | `location_altitude` | decimal(10,2) | YES |  |
| 8 | `heading` | decimal(6,2) | YES |  |
| 9 | `speed` | decimal(8,3) | YES |  |
| 10 | `speed_unit` | varchar | YES |  |
| 11 | `created_at` | timestamp(3) | YES |  |
| 12 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.machine_measurements_dt

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `equipment_id` | varchar | YES |  |
| 4 | `principal_id` | varchar | YES |  |
| 5 | `measurement_id` | varchar | YES |  |
| 6 | `measurement_name` | varchar | YES |  |
| 7 | `sequence_number` | integer | YES |  |
| 8 | `interval_start_utc` | timestamp(3) | YES |  |
| 9 | `interval_end_utc` | timestamp(3) | YES |  |
| 10 | `actual_start_utc` | timestamp(3) | YES |  |
| 11 | `actual_end_utc` | timestamp(3) | YES |  |
| 12 | `business_date` | date | YES |  |
| 13 | `measurement_value` | double | YES |  |
| 14 | `measurement_count` | integer | YES |  |
| 15 | `measure_unit` | varchar | YES |  |
| 16 | `aggregation_type` | varchar | YES |  |
| 17 | `aggregation_type_id` | varchar | YES |  |
| 18 | `measurement_type` | varchar | YES |  |
| 19 | `ui_visible_indicator` | varchar | YES |  |
| 20 | `definition_description` | varchar | YES |  |
| 21 | `network_type` | varchar | YES |  |
| 22 | `request_start_utc` | timestamp(3) | YES |  |
| 23 | `request_end_utc` | timestamp(3) | YES |  |
| 24 | `request_ts_utc` | timestamp(3) | YES |  |
| 25 | `bucket_sequence_description` | varchar | YES |  |
| 26 | `bucket_range_indicator` | boolean | YES |  |
| 27 | `bucket_min_value` | double | YES |  |
| 28 | `bucket_max_value` | double | YES |  |
| 29 | `created_at` | timestamp(3) | YES |  |
| 30 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.operators_dt

**Columnas:** 20

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `api_type` | varchar | YES |  |
| 4 | `name` | varchar | YES |  |
| 5 | `first_name` | varchar | YES |  |
| 6 | `last_name` | varchar | YES |  |
| 7 | `archived` | boolean | YES |  |
| 8 | `guid` | varchar | YES |  |
| 9 | `date_modified` | timestamp(3) | YES |  |
| 10 | `user_creation_timestamp` | timestamp(3) | YES |  |
| 11 | `created_by_user` | varchar | YES |  |
| 12 | `created_by_source_system_uri` | varchar | YES |  |
| 13 | `created_by_source_node` | varchar | YES |  |
| 14 | `user_last_modified_timestamp` | timestamp(3) | YES |  |
| 15 | `last_modified_by_user` | varchar | YES |  |
| 16 | `last_modified_by_source_system_uri` | varchar | YES |  |
| 17 | `last_modified_by_source_node` | varchar | YES |  |
| 18 | `content_hash` | varchar | YES |  |
| 19 | `created_at` | timestamp(3) | YES |  |
| 20 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.organizations_dt

**Columnas:** 18

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `api_type` | varchar | YES |  |
| 3 | `name` | varchar | YES |  |
| 4 | `type` | varchar | YES |  |
| 5 | `member` | boolean | YES |  |
| 6 | `internal` | boolean | YES |  |
| 7 | `hierarchy_enabled` | boolean | YES |  |
| 8 | `need_connection` | boolean | YES |  |
| 9 | `content_hash` | varchar | YES |  |
| 10 | `first_seen_at` | timestamp(3) | YES |  |
| 11 | `last_seen_at` | timestamp(3) | YES |  |
| 12 | `is_active` | boolean | YES |  |
| 13 | `absence_count` | integer | YES |  |
| 14 | `inactivated_at` | timestamp(3) | YES |  |
| 15 | `reactivated_at` | timestamp(3) | YES |  |
| 16 | `last_change_at` | timestamp(3) | YES |  |
| 17 | `created_at` | timestamp(3) | YES |  |
| 18 | `updated_at` | timestamp(3) | YES |  |

### sonnard_jdoc_data_core.sync_executions_dt

**Columnas:** 13

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `organization_id` | varchar | YES |  |
| 3 | `script_name` | varchar | YES |  |
| 4 | `execution_mode` | varchar | YES |  |
| 5 | `status` | varchar | YES |  |
| 6 | `started_at` | timestamp(3) | YES |  |
| 7 | `finished_at` | timestamp(3) | YES |  |
| 8 | `records_processed` | integer | YES |  |
| 9 | `records_inserted` | integer | YES |  |
| 10 | `records_updated` | integer | YES |  |
| 11 | `error_message` | varchar | YES |  |
| 12 | `created_at` | timestamp(3) | YES |  |
| 13 | `updated_at` | timestamp(3) | YES |  |

## 🥉 spiga

`Capa: Bronce / Raw`

### spiga.dwdms00280_dw_dimcentros

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `skdimcentros` | bigint | YES |  |
| 2 | `pkcentros` | bigint | YES |  |
| 3 | `nombrecentro` | varchar | YES |  |
| 4 | `idproceso` | bigint | YES |  |
| 5 | `idprocesodw` | bigint | YES |  |
| 6 | `versionct` | bigint | YES |  |
| 7 | `hashvaluebi` | bigint | YES |  |
| 8 | `load_date` | varchar | YES |  |

### spiga.dwdms00280_dw_dimempleados

**Columnas:** 20

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `skdimempleados` | bigint | YES |  |
| 2 | `nombre` | varchar | YES |  |
| 3 | `apellido1` | varchar | YES |  |
| 4 | `apellido2` | varchar | YES |  |
| 5 | `pkempleados` | bigint | YES |  |
| 6 | `idproceso` | bigint | YES |  |
| 7 | `idprocesodw` | bigint | YES |  |
| 8 | `versionct` | bigint | YES |  |
| 9 | `hashvaluebi` | bigint | YES |  |
| 10 | `nifcif` | varchar | YES |  |
| 11 | `telefonoprincipal` | varchar | YES |  |
| 12 | `telefonomovil` | varchar | YES |  |
| 13 | `email` | varchar | YES |  |
| 14 | `nombreusuario` | varchar | YES |  |
| 15 | `fechabaja` | timestamp(3) | YES |  |
| 16 | `fechaalta` | timestamp(3) | YES |  |
| 17 | `fkusuarios` | bigint | YES |  |
| 18 | `fkprofesiones` | bigint | YES |  |
| 19 | `nombreprofesion` | varchar | YES |  |
| 20 | `load_date` | varchar | YES |  |

### spiga.dwdms00280_dw_dimempresas

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `skdimempresas` | bigint | YES |  |
| 2 | `nombreempresa` | varchar | YES |  |
| 3 | `pkempresas` | bigint | YES |  |
| 4 | `idproceso` | bigint | YES |  |
| 5 | `idprocesodw` | bigint | YES |  |
| 6 | `versionct` | bigint | YES |  |
| 7 | `hashvaluebi` | bigint | YES |  |
| 8 | `load_date` | varchar | YES |  |

### spiga.dwdms00280_dw_dimmarcasgamas

**Columnas:** 10

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `skdimmarcasgamas` | bigint | YES |  |
| 2 | `nombremarca` | varchar | YES |  |
| 3 | `nombregama` | varchar | YES |  |
| 4 | `pkmarcas` | bigint | YES |  |
| 5 | `pkgamas` | bigint | YES |  |
| 6 | `idproceso` | bigint | YES |  |
| 7 | `idprocesodw` | bigint | YES |  |
| 8 | `versionct` | bigint | YES |  |
| 9 | `hashvaluebi` | bigint | YES |  |
| 10 | `load_date` | varchar | YES |  |

### spiga.dwdms00280_dw_factfinanciacionventas

**Columnas:** 54

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `skfactfinanciacionventas` | bigint | YES |  |
| 2 | `pkempresas` | bigint | YES |  |
| 3 | `pka�oexpediente` | varchar | YES |  |
| 4 | `pknumexpediente` | bigint | YES |  |
| 5 | `pkpagostipos` | bigint | YES |  |
| 6 | `pkseries_expediente` | varchar | YES |  |
| 7 | `pkventas` | bigint | YES |  |
| 8 | `pkventaspagos` | bigint | YES |  |
| 9 | `pkcomprasnumdet` | bigint | YES |  |
| 10 | `pkcentros` | bigint | YES |  |
| 11 | `pktercerosfinanciera` | bigint | YES |  |
| 12 | `nombrefinanciera` | varchar | YES |  |
| 13 | `apellido1financiera` | varchar | YES |  |
| 14 | `apellido2financiera` | varchar | YES |  |
| 15 | `pktercerosagente` | bigint | YES |  |
| 16 | `nombreagente` | varchar | YES |  |
| 17 | `apellido1agente` | varchar | YES |  |
| 18 | `apellido2agente` | varchar | YES |  |
| 19 | `pktercerospropietario` | bigint | YES |  |
| 20 | `nombrepropietario` | varchar | YES |  |
| 21 | `apellido1propietario` | varchar | YES |  |
| 22 | `apellido2propietario` | varchar | YES |  |
| 23 | `nifcifpropietario` | varchar | YES |  |
| 24 | `importefinanciado` | double | YES |  |
| 25 | `comisionfinanciera` | double | YES |  |
| 26 | `pkofertapagos` | bigint | YES |  |
| 27 | `saldofavorcliente` | varchar | YES |  |
| 28 | `vin` | varchar | YES |  |
| 29 | `matricula` | varchar | YES |  |
| 30 | `comisionvehiculo` | varchar | YES |  |
| 31 | `modulo` | varchar | YES |  |
| 32 | `estado` | varchar | YES |  |
| 33 | `fechavencimiento` | timestamp(3) | YES |  |
| 34 | `fechainicio` | timestamp(3) | YES |  |
| 35 | `fechaventa` | timestamp(3) | YES |  |
| 36 | `fechaentregacliente` | timestamp(3) | YES |  |
| 37 | `fechadecorte` | timestamp(3) | YES |  |
| 38 | `idproceso` | bigint | YES |  |
| 39 | `idprocesodw` | bigint | YES |  |
| 40 | `versionct` | bigint | YES |  |
| 41 | `hashvaluebi` | bigint | YES |  |
| 42 | `skdimempresas` | bigint | YES |  |
| 43 | `skdimcentros` | bigint | YES |  |
| 44 | `skdimsecciones` | bigint | YES |  |
| 45 | `skdimmarcasgamas` | bigint | YES |  |
| 46 | `skdimempleados` | bigint | YES |  |
| 47 | `skdimempleadosgestor` | bigint | YES |  |
| 48 | `pkventaspagosdet` | bigint | YES |  |
| 49 | `pkefectosnumdet` | bigint | YES |  |
| 50 | `pka�oasiento` | varchar | YES |  |
| 51 | `pkasientos` | bigint | YES |  |
| 52 | `pka�oasiento_saldar` | varchar | YES |  |
| 53 | `pkasientos_saldar` | bigint | YES |  |
| 54 | `load_date` | varchar | YES |  |

### spiga.spiga_cartera

**Columnas:** 59

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `indice` | double | YES |  |
| 8 | `idterceros` | bigint | YES |  |
| 9 | `idterceros_pagador` | bigint | YES |  |
| 10 | `nombretercero` | varchar | YES |  |
| 11 | `factura` | varchar | YES |  |
| 12 | `fechafactura` | timestamp(3) | YES |  |
| 13 | `fechavencimiento` | timestamp(3) | YES |  |
| 14 | `idpagoformas` | varchar | YES |  |
| 15 | `descripcionpagoformas` | varchar | YES |  |
| 16 | `idsituacionefectos` | bigint | YES |  |
| 17 | `descripcionsituacionefectos` | varchar | YES |  |
| 18 | `departamento` | varchar | YES |  |
| 19 | `nombredepartamento` | varchar | YES |  |
| 20 | `totalfactura` | double | YES |  |
| 21 | `importeefecto` | double | YES |  |
| 22 | `importependiente` | double | YES |  |
| 23 | `diadesde` | bigint | YES |  |
| 24 | `diahasta` | bigint | YES |  |
| 25 | `nombrecentro` | varchar | YES |  |
| 26 | `numdet` | bigint | YES |  |
| 27 | `a�oasiento` | varchar | YES |  |
| 28 | `idasientos` | bigint | YES |  |
| 29 | `descripciontipocalle` | varchar | YES |  |
| 30 | `nombrecalle` | varchar | YES |  |
| 31 | `numero` | varchar | YES |  |
| 32 | `bloque` | varchar | YES |  |
| 33 | `piso` | varchar | YES |  |
| 34 | `puerta` | varchar | YES |  |
| 35 | `complemento` | varchar | YES |  |
| 36 | `complemento2` | varchar | YES |  |
| 37 | `nifcif` | varchar | YES |  |
| 38 | `idpaises` | varchar | YES |  |
| 39 | `ciudad` | varchar | YES |  |
| 40 | `referenciainterna` | varchar | YES |  |
| 41 | `limitecredito` | double | YES |  |
| 42 | `vin` | varchar | YES |  |
| 43 | `descripcionseccion` | varchar | YES |  |
| 44 | `fechasaldado` | timestamp(3) | YES |  |
| 45 | `estadowf` | varchar | YES |  |
| 46 | `pagobloqueado` | bigint | YES |  |
| 47 | `descripciondeudortipos` | varchar | YES |  |
| 48 | `iddeudortipos` | varchar | YES |  |
| 49 | `idcontctasterceropagador` | varchar | YES |  |
| 50 | `fechaentregavo` | timestamp(3) | YES |  |
| 51 | `fechaentregavn` | timestamp(3) | YES |  |
| 52 | `referencia` | varchar | YES |  |
| 53 | `idmonedaorigen` | bigint | YES |  |
| 54 | `factorcambiomoneda` | double | YES |  |
| 55 | `factorcambiomonedacontravalor` | double | YES |  |
| 56 | `descripcionmoneda` | varchar | YES |  |
| 57 | `decimalescalculomoneda` | bigint | YES |  |
| 58 | `telefonos` | varchar | YES |  |
| 59 | `load_date` | varchar | YES |  |

### spiga.spiga_compradeusados

**Columnas:** 100

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacion` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `comprasnumdet` | bigint | YES |  |
| 12 | `idvehiculos` | bigint | YES |  |
| 13 | `idcompratipos` | varchar | YES |  |
| 14 | `importecompra` | double | YES |  |
| 15 | `importetotal` | double | YES |  |
| 16 | `codcompramultiple` | bigint | YES |  |
| 17 | `fechaalta` | timestamp(3) | YES |  |
| 18 | `fechaanulacion` | timestamp(3) | YES |  |
| 19 | `idsecciones` | bigint | YES |  |
| 20 | `fechaabono` | timestamp(3) | YES |  |
| 21 | `comprasnumdetabonado` | bigint | YES |  |
| 22 | `idcompraestados` | varchar | YES |  |
| 23 | `observaciones` | varchar | YES |  |
| 24 | `idregistrotipos` | varchar | YES |  |
| 25 | `reservafecha` | timestamp(3) | YES |  |
| 26 | `reservaimporte` | double | YES |  |
| 27 | `reservaidempleados` | bigint | YES |  |
| 28 | `reservaterceros` | bigint | YES |  |
| 29 | `realizargastoadicionalautomatico` | bigint | YES |  |
| 30 | `nocontabilizardocumentacion` | bigint | YES |  |
| 31 | `idempleadovendedor` | bigint | YES |  |
| 32 | `kms` | bigint | YES |  |
| 33 | `a�oexpedientecambio` | varchar | YES |  |
| 34 | `serieexpedientecambio` | varchar | YES |  |
| 35 | `numexpedientecambio` | bigint | YES |  |
| 36 | `prever` | bigint | YES |  |
| 37 | `visibleweb` | bigint | YES |  |
| 38 | `comercializable` | bigint | YES |  |
| 39 | `generaasiento` | varchar | YES |  |
| 40 | `idmoduloorigen` | varchar | YES |  |
| 41 | `idusuariosanulacion` | bigint | YES |  |
| 42 | `idempleadosanulacion` | bigint | YES |  |
| 43 | `hostanulacion` | varchar | YES |  |
| 44 | `usermod` | bigint | YES |  |
| 45 | `hostmod` | varchar | YES |  |
| 46 | `versionfila` | bigint | YES |  |
| 47 | `a�oexpedientecambiovn` | varchar | YES |  |
| 48 | `serieexpedientecambiovn` | varchar | YES |  |
| 49 | `numexpedientecambiovn` | bigint | YES |  |
| 50 | `idcomprasnumdetcambio` | bigint | YES |  |
| 51 | `idcomprasnumdetcambiovn` | bigint | YES |  |
| 52 | `marcarkm0web` | bigint | YES |  |
| 53 | `fecharecepcion` | timestamp(3) | YES |  |
| 54 | `fechaasiento` | timestamp(3) | YES |  |
| 55 | `seriefactura` | varchar | YES |  |
| 56 | `numfactura` | varchar | YES |  |
| 57 | `a�ofactura` | varchar | YES |  |
| 58 | `fechafactura` | timestamp(3) | YES |  |
| 59 | `idmarcas` | bigint | YES |  |
| 60 | `idgamas` | bigint | YES |  |
| 61 | `codmodelo` | varchar | YES |  |
| 62 | `extmodelo` | varchar | YES |  |
| 63 | `a�omodelo` | varchar | YES |  |
| 64 | `idversiones` | varchar | YES |  |
| 65 | `matricula` | varchar | YES |  |
| 66 | `vin` | varchar | YES |  |
| 67 | `nombremarca` | varchar | YES |  |
| 68 | `nombregama` | varchar | YES |  |
| 69 | `importebi` | double | YES |  |
| 70 | `importe576` | double | YES |  |
| 71 | `importedvn` | double | YES |  |
| 72 | `exentos` | double | YES |  |
| 73 | `vincambio` | varchar | YES |  |
| 74 | `matriculacambio` | varchar | YES |  |
| 75 | `idmarcascambio` | bigint | YES |  |
| 76 | `idgamascambio` | bigint | YES |  |
| 77 | `nombremarcacambio` | varchar | YES |  |
| 78 | `nombregamacambio` | varchar | YES |  |
| 79 | `gastoadicionaldetalles` | double | YES |  |
| 80 | `idterceros` | bigint | YES |  |
| 81 | `nombreterceros` | varchar | YES |  |
| 82 | `nombre` | varchar | YES |  |
| 83 | `idmonedas` | bigint | YES |  |
| 84 | `factorcambiomoneda` | double | YES |  |
| 85 | `monedaorigen` | varchar | YES |  |
| 86 | `centroventavehiculocambio` | varchar | YES |  |
| 87 | `nombreempleadoventavehiculocambio` | varchar | YES |  |
| 88 | `apellido1empleadoventavehiculocambio` | varchar | YES |  |
| 89 | `apellido2empleadoventavehiculocambio` | varchar | YES |  |
| 90 | `nombreempleadocompra` | varchar | YES |  |
| 91 | `apellido1empleadocompra` | varchar | YES |  |
| 92 | `apellido2empleadocompra` | varchar | YES |  |
| 93 | `descripcioncompratipos` | varchar | YES |  |
| 94 | `esinmovilizado` | bigint | YES |  |
| 95 | `nombremodelo` | varchar | YES |  |
| 96 | `descripcionversiones` | varchar | YES |  |
| 97 | `descripcionsecciones` | varchar | YES |  |
| 98 | `descripcionregistrotipos` | varchar | YES |  |
| 99 | `seccionventavehiculocambio` | varchar | YES |  |
| 100 | `load_date` | varchar | YES |  |

### spiga.spiga_compras_sel_stockvn

**Columnas:** 206

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `comprasnumdet` | bigint | YES |  |
| 12 | `idasientos` | bigint | YES |  |
| 13 | `a�oasiento` | varchar | YES |  |
| 14 | `idvehiculos` | bigint | YES |  |
| 15 | `idterceros` | bigint | YES |  |
| 16 | `idcompratipos` | varchar | YES |  |
| 17 | `numexpedientescompramultiple` | bigint | YES |  |
| 18 | `idmarcas` | bigint | YES |  |
| 19 | `idgamas` | bigint | YES |  |
| 20 | `codmodelo` | varchar | YES |  |
| 21 | `extmodelo` | varchar | YES |  |
| 22 | `a�omodelo` | varchar | YES |  |
| 23 | `idversiones` | varchar | YES |  |
| 24 | `idtarifas` | bigint | YES |  |
| 25 | `seriefactura` | varchar | YES |  |
| 26 | `numfactura` | varchar | YES |  |
| 27 | `a�ofactura` | varchar | YES |  |
| 28 | `fechaalta` | timestamp(3) | YES |  |
| 29 | `fechaanulacion` | timestamp(3) | YES |  |
| 30 | `fechacampaalta` | timestamp(3) | YES |  |
| 31 | `fecharecepcion` | timestamp(3) | YES |  |
| 32 | `fechafactura` | timestamp(3) | YES |  |
| 33 | `fechaasiento` | timestamp(3) | YES |  |
| 34 | `fechareserva` | timestamp(3) | YES |  |
| 35 | `importacionrealizada` | bigint | YES |  |
| 36 | `importacionmodificada` | bigint | YES |  |
| 37 | `fechaimportacionrealizada` | timestamp(3) | YES |  |
| 38 | `fechaimportacionmodificada` | timestamp(3) | YES |  |
| 39 | `preciobase` | double | YES |  |
| 40 | `preciopintura` | double | YES |  |
| 41 | `preciotransporte` | double | YES |  |
| 42 | `precioopciones` | double | YES |  |
| 43 | `preciootroscargos` | double | YES |  |
| 44 | `importecompra` | double | YES |  |
| 45 | `baseimponible` | double | YES |  |
| 46 | `idcentrosasignadoventa` | bigint | YES |  |
| 47 | `idseccionesasignadaventa` | bigint | YES |  |
| 48 | `preciolegalizacion` | double | YES |  |
| 49 | `precioisv` | double | YES |  |
| 50 | `precioecovalor` | double | YES |  |
| 51 | `baseexenta` | double | YES |  |
| 52 | `sumadescuentos` | double | YES |  |
| 53 | `idempleadosreserva` | bigint | YES |  |
| 54 | `idagentesreserva` | bigint | YES |  |
| 55 | `idterceros_cedidoconcesionario` | bigint | YES |  |
| 56 | `numfacturamensual` | bigint | YES |  |
| 57 | `idsecciones` | bigint | YES |  |
| 58 | `numexpedicion` | varchar | YES |  |
| 59 | `programa` | varchar | YES |  |
| 60 | `realizargastoadicionalautomatico` | bigint | YES |  |
| 61 | `nocontabilizardocumentacion` | bigint | YES |  |
| 62 | `observaciones` | varchar | YES |  |
| 63 | `comprasnumdet_abonado` | bigint | YES |  |
| 64 | `idcompraestados` | varchar | YES |  |
| 65 | `usermod` | bigint | YES |  |
| 66 | `hostmod` | varchar | YES |  |
| 67 | `versionfila` | bigint | YES |  |
| 68 | `fechaabono` | timestamp(3) | YES |  |
| 69 | `idusuariosanulacion` | bigint | YES |  |
| 70 | `idempleadosanulacion` | bigint | YES |  |
| 71 | `hostanulacion` | varchar | YES |  |
| 72 | `idasientos_polizanoactivo` | bigint | YES |  |
| 73 | `a�oasiento_polizanoactivo` | varchar | YES |  |
| 74 | `nombremarca` | varchar | YES |  |
| 75 | `backcolorcabecerargb` | varchar | YES |  |
| 76 | `backcolordetallergb` | varchar | YES |  |
| 77 | `forecolorcabecerargb` | varchar | YES |  |
| 78 | `forecolordetallergb` | varchar | YES |  |
| 79 | `nombregama` | varchar | YES |  |
| 80 | `preciolegalizacion1` | double | YES |  |
| 81 | `precioisv1` | double | YES |  |
| 82 | `precioecovalor1` | double | YES |  |
| 83 | `activo` | bigint | YES |  |
| 84 | `idcarroceriatipos` | varchar | YES |  |
| 85 | `idclasificaciontipos` | varchar | YES |  |
| 86 | `idmarcatallermodelos` | varchar | YES |  |
| 87 | `idtracciontipos` | varchar | YES |  |
| 88 | `idcambiotipos` | varchar | YES |  |
| 89 | `idtonelajetipos` | varchar | YES |  |
| 90 | `iddistanciaejestipos` | varchar | YES |  |
| 91 | `codexternomodelo` | varchar | YES |  |
| 92 | `potenciafiscal` | varchar | YES |  |
| 93 | `potenciareal` | varchar | YES |  |
| 94 | `cilindrada` | double | YES |  |
| 95 | `aceleracion` | varchar | YES |  |
| 96 | `velocidadmax` | double | YES |  |
| 97 | `par` | varchar | YES |  |
| 98 | `numerocilindros` | bigint | YES |  |
| 99 | `consumointerurbano` | double | YES |  |
| 100 | `consumourbano` | double | YES |  |
| 101 | `consumomedio` | double | YES |  |
| 102 | `emisionesco2interurbano` | double | YES |  |
| 103 | `emisionesco2urbano` | double | YES |  |
| 104 | `emisionesco2medio` | double | YES |  |
| 105 | `importado` | bigint | YES |  |
| 106 | `modificado` | bigint | YES |  |
| 107 | `permiteplanprever` | bigint | YES |  |
| 108 | `visibleweb` | bigint | YES |  |
| 109 | `periodoinspeccion` | bigint | YES |  |
| 110 | `kilometrosinspeccion` | varchar | YES |  |
| 111 | `descripcionmodelotaller` | varchar | YES |  |
| 112 | `vin` | varchar | YES |  |
| 113 | `matricula` | varchar | YES |  |
| 114 | `comision` | varchar | YES |  |
| 115 | `fechamatriculacion` | timestamp(3) | YES |  |
| 116 | `codigofabricacion` | varchar | YES |  |
| 117 | `fechafabricacion` | timestamp(3) | YES |  |
| 118 | `numeromotor` | varchar | YES |  |
| 119 | `nombreempresa` | varchar | YES |  |
| 120 | `nombrecentro` | varchar | YES |  |
| 121 | `diasstock` | bigint | YES |  |
| 122 | `idrecursos` | bigint | YES |  |
| 123 | `idubicacionesultimarealizada` | varchar | YES |  |
| 124 | `fechaexpedientealtaultimarealizada` | timestamp(3) | YES |  |
| 125 | `ubicacionvn` | varchar | YES |  |
| 126 | `fechaubicacion` | timestamp(3) | YES |  |
| 127 | `idubicacionesultima` | varchar | YES |  |
| 128 | `fechaexpedientealtaultima` | timestamp(3) | YES |  |
| 129 | `ubicacionvnprevista` | varchar | YES |  |
| 130 | `fechasalidareal` | timestamp(3) | YES |  |
| 131 | `nombreempleadoreserva` | varchar | YES |  |
| 132 | `nombreagente` | varchar | YES |  |
| 133 | `cedido` | varchar | YES |  |
| 134 | `fechallegadapuerto` | timestamp(3) | YES |  |
| 135 | `fecharetirada` | timestamp(3) | YES |  |
| 136 | `datoscarta` | varchar | YES |  |
| 137 | `preciocompra` | double | YES |  |
| 138 | `precioventa` | double | YES |  |
| 139 | `transportecompra` | double | YES |  |
| 140 | `precioventaopcionales` | bigint | YES |  |
| 141 | `rodajetrimestral` | double | YES |  |
| 142 | `gastosmatriculacion` | double | YES |  |
| 143 | `atipicos` | double | YES |  |
| 144 | `transporteventa` | double | YES |  |
| 145 | `preciolegalizacionventa` | double | YES |  |
| 146 | `impuesto576porc` | double | YES |  |
| 147 | `numpedidovn` | varchar | YES |  |
| 148 | `idtercerospedido` | bigint | YES |  |
| 149 | `fechainiciofranquicia` | timestamp(3) | YES |  |
| 150 | `fechafinalfranquicia` | timestamp(3) | YES |  |
| 151 | `fechaaradefinitiva` | timestamp(3) | YES |  |
| 152 | `fechaentregaconcesionario` | timestamp(3) | YES |  |
| 153 | `fechacompromisoentrega` | timestamp(3) | YES |  |
| 154 | `mesesgarantiaobligatoriavn` | bigint | YES |  |
| 155 | `numpedidofabrica` | varchar | YES |  |
| 156 | `numpedidomarca` | varchar | YES |  |
| 157 | `pedidoobservaciones` | varchar | YES |  |
| 158 | `idpedidolocaltipos` | varchar | YES |  |
| 159 | `fechadespacho` | timestamp(3) | YES |  |
| 160 | `diasestancia` | bigint | YES |  |
| 161 | `observacionubicacion` | varchar | YES |  |
| 162 | `diasdecarenciadocumentacion` | bigint | YES |  |
| 163 | `diascarencia` | bigint | YES |  |
| 164 | `situacion` | varchar | YES |  |
| 165 | `permitirfacturarenotrocentro` | bigint | YES |  |
| 166 | `idpaises_origen` | varchar | YES |  |
| 167 | `importacion` | bigint | YES |  |
| 168 | `factorcambiomonedacontravalor` | double | YES |  |
| 169 | `importepedidoservicios` | double | YES |  |
| 170 | `importegastosadicionales` | double | YES |  |
| 171 | `fechapedido` | timestamp(3) | YES |  |
| 172 | `diasexposicion` | bigint | YES |  |
| 173 | `homologacion` | bigint | YES |  |
| 174 | `nombreprospectoreservapedido` | varchar | YES |  |
| 175 | `nombreclientereservapedido` | varchar | YES |  |
| 176 | `nombreclientereservacompra` | varchar | YES |  |
| 177 | `precioiuc` | double | YES |  |
| 178 | `a�opedidosservicios` | varchar | YES |  |
| 179 | `seriepedidosservicios` | varchar | YES |  |
| 180 | `idpedidosservicios` | bigint | YES |  |
| 181 | `idmonedas` | bigint | YES |  |
| 182 | `factorcambiomoneda` | double | YES |  |
| 183 | `idregimencontable` | varchar | YES |  |
| 184 | `colorcompleto` | varchar | YES |  |
| 185 | `tapiceriacompleta` | varchar | YES |  |
| 186 | `descripcioncambiotipos` | varchar | YES |  |
| 187 | `nombreversion` | varchar | YES |  |
| 188 | `nombretarifa` | varchar | YES |  |
| 189 | `nombremodelo` | varchar | YES |  |
| 190 | `descripcionestadocompra` | varchar | YES |  |
| 191 | `descripciontipocombustible` | varchar | YES |  |
| 192 | `descripcionpedidolocaltipos` | varchar | YES |  |
| 193 | `descripcioncomprausos` | varchar | YES |  |
| 194 | `descripcionestadopedidosservicio` | varchar | YES |  |
| 195 | `idtercerosreserva` | bigint | YES |  |
| 196 | `idcomprausos` | varchar | YES |  |
| 197 | `visualizarenstockcomprausos` | bigint | YES |  |
| 198 | `tipocompra` | varchar | YES |  |
| 199 | `idiventario` | bigint | YES |  |
| 200 | `fechaultimoinventario` | timestamp(3) | YES |  |
| 201 | `documentosinventario` | bigint | YES |  |
| 202 | `documentosrespuestasinventario` | bigint | YES |  |
| 203 | `porcimpuestos_iva` | double | YES |  |
| 204 | `porcimpuestos_con` | double | YES |  |
| 205 | `idcentrosubicacion` | bigint | YES |  |
| 206 | `load_date` | varchar | YES |  |

### spiga.spiga_compras_sel_stockvo

**Columnas:** 122

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `comprasnumdet` | bigint | YES |  |
| 12 | `idvehiculos` | bigint | YES |  |
| 13 | `idcompratipos` | varchar | YES |  |
| 14 | `codcompramultiple` | bigint | YES |  |
| 15 | `fechaalta` | timestamp(3) | YES |  |
| 16 | `fechaanulacion` | timestamp(3) | YES |  |
| 17 | `fecharecepcion` | timestamp(3) | YES |  |
| 18 | `idsecciones` | bigint | YES |  |
| 19 | `fechaabono` | timestamp(3) | YES |  |
| 20 | `comprasnumdetabonado` | bigint | YES |  |
| 21 | `idcompraestados` | varchar | YES |  |
| 22 | `observaciones` | varchar | YES |  |
| 23 | `idregistrotipos` | varchar | YES |  |
| 24 | `reservafecha` | timestamp(3) | YES |  |
| 25 | `reservaidempleados` | bigint | YES |  |
| 26 | `reservaterceros` | bigint | YES |  |
| 27 | `realizargastoadicionalautomatico` | bigint | YES |  |
| 28 | `nocontabilizardocumentacion` | bigint | YES |  |
| 29 | `idempleadovendedor` | bigint | YES |  |
| 30 | `kms` | bigint | YES |  |
| 31 | `a�oexpedientecambio` | varchar | YES |  |
| 32 | `serieexpedientecambio` | varchar | YES |  |
| 33 | `numexpedientecambio` | bigint | YES |  |
| 34 | `fechaasiento` | timestamp(3) | YES |  |
| 35 | `prever` | bigint | YES |  |
| 36 | `generaasiento` | varchar | YES |  |
| 37 | `idmoduloorigen` | varchar | YES |  |
| 38 | `idusuariosanulacion` | bigint | YES |  |
| 39 | `idempleadosanulacion` | bigint | YES |  |
| 40 | `hostanulacion` | varchar | YES |  |
| 41 | `usermod` | bigint | YES |  |
| 42 | `hostmod` | varchar | YES |  |
| 43 | `versionfila` | bigint | YES |  |
| 44 | `reservaimporte` | double | YES |  |
| 45 | `importecompra` | double | YES |  |
| 46 | `precioventaminimo` | double | YES |  |
| 47 | `visibleweb` | bigint | YES |  |
| 48 | `comercializable` | bigint | YES |  |
| 49 | `idcomprausos` | varchar | YES |  |
| 50 | `vin` | varchar | YES |  |
| 51 | `matricula` | varchar | YES |  |
| 52 | `comision` | varchar | YES |  |
| 53 | `fechamatriculacion` | timestamp(3) | YES |  |
| 54 | `idmarcas` | bigint | YES |  |
| 55 | `idgamas` | bigint | YES |  |
| 56 | `codmodelo` | varchar | YES |  |
| 57 | `extmodelo` | varchar | YES |  |
| 58 | `a�omodelo` | varchar | YES |  |
| 59 | `idversiones` | varchar | YES |  |
| 60 | `idmarcasexterna` | bigint | YES |  |
| 61 | `idgamasexterna` | bigint | YES |  |
| 62 | `codmodeloexterna` | varchar | YES |  |
| 63 | `extmodeloexterna` | varchar | YES |  |
| 64 | `a�omodeloexterna` | varchar | YES |  |
| 65 | `idversionesexterna` | varchar | YES |  |
| 66 | `kmsactuales` | bigint | YES |  |
| 67 | `permitirfacturarenotrocentro` | bigint | YES |  |
| 68 | `otrasobservaciones` | varchar | YES |  |
| 69 | `horasusoactual` | bigint | YES |  |
| 70 | `nombremarca` | varchar | YES |  |
| 71 | `nombregama` | varchar | YES |  |
| 72 | `nombremodelo` | varchar | YES |  |
| 73 | `nombregamaexterna` | varchar | YES |  |
| 74 | `nombremodeloexterna` | varchar | YES |  |
| 75 | `descripciontipocombustible` | varchar | YES |  |
| 76 | `descripciontipocombustibleexterna` | varchar | YES |  |
| 77 | `descripcionestadocompra` | varchar | YES |  |
| 78 | `potenciareal` | varchar | YES |  |
| 79 | `potenciarealexterna` | varchar | YES |  |
| 80 | `numeropuertas` | varchar | YES |  |
| 81 | `numeroplazas` | varchar | YES |  |
| 82 | `nombreempresa` | varchar | YES |  |
| 83 | `nombrecentro` | varchar | YES |  |
| 84 | `descripcionseccion` | varchar | YES |  |
| 85 | `descripciontiporegistro` | varchar | YES |  |
| 86 | `idcomprainternatipos` | varchar | YES |  |
| 87 | `descripcioncompratipos` | varchar | YES |  |
| 88 | `descripcioncarroceriatipos` | varchar | YES |  |
| 89 | `diasstock` | bigint | YES |  |
| 90 | `fecharetirada` | timestamp(3) | YES |  |
| 91 | `importeventasugerido` | double | YES |  |
| 92 | `nombreempleadoreserva` | varchar | YES |  |
| 93 | `nombreterceroreserva` | varchar | YES |  |
| 94 | `idrecursos` | bigint | YES |  |
| 95 | `importebi` | double | YES |  |
| 96 | `importedvn` | double | YES |  |
| 97 | `importe576` | double | YES |  |
| 98 | `exentos` | double | YES |  |
| 99 | `importegastosadicionales` | double | YES |  |
| 100 | `importedepreciado` | double | YES |  |
| 101 | `descripcioncomprausos` | varchar | YES |  |
| 102 | `importepedidoservicios` | double | YES |  |
| 103 | `nombrescedentes` | varchar | YES |  |
| 104 | `colorcompleto` | varchar | YES |  |
| 105 | `colorcompletoexterna` | varchar | YES |  |
| 106 | `tapiceriacompleta` | varchar | YES |  |
| 107 | `visualizarenstockcomprausos` | bigint | YES |  |
| 108 | `fechafactura` | timestamp(3) | YES |  |
| 109 | `fechafabricacion` | timestamp(3) | YES |  |
| 110 | `descripcionversion` | varchar | YES |  |
| 111 | `programasmarca` | varchar | YES |  |
| 112 | `idiventario` | bigint | YES |  |
| 113 | `fechaultimoinventario` | timestamp(3) | YES |  |
| 114 | `documentosinventario` | bigint | YES |  |
| 115 | `documentosrespuestasinventario` | bigint | YES |  |
| 116 | `sitiomatricula` | varchar | YES |  |
| 117 | `fechaproximaitv` | timestamp(3) | YES |  |
| 118 | `fechavencimientoseguro` | timestamp(3) | YES |  |
| 119 | `ubicacionvo` | varchar | YES |  |
| 120 | `observacionubicacionvo` | varchar | YES |  |
| 121 | `idubicavno` | varchar | YES |  |
| 122 | `load_date` | varchar | YES |  |

### spiga.spiga_comprasvehiculosvn

**Columnas:** 62

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `comprasnumdet` | bigint | YES |  |
| 12 | `idvehiculos` | bigint | YES |  |
| 13 | `idcompratipos` | varchar | YES |  |
| 14 | `importecompra` | double | YES |  |
| 15 | `idsecciones` | bigint | YES |  |
| 16 | `seriefactura` | varchar | YES |  |
| 17 | `numfactura` | varchar | YES |  |
| 18 | `a�ofactura` | varchar | YES |  |
| 19 | `fechafactura` | timestamp(3) | YES |  |
| 20 | `baseimponible` | double | YES |  |
| 21 | `fechaasiento` | timestamp(3) | YES |  |
| 22 | `fecharegistrorunt` | timestamp(3) | YES |  |
| 23 | `importeiva` | double | YES |  |
| 24 | `descripcioncompratipos` | varchar | YES |  |
| 25 | `idmarcas` | bigint | YES |  |
| 26 | `idgamas` | bigint | YES |  |
| 27 | `codmodelo` | varchar | YES |  |
| 28 | `extmodelo` | varchar | YES |  |
| 29 | `a�omodelo` | varchar | YES |  |
| 30 | `idversiones` | varchar | YES |  |
| 31 | `matricula` | varchar | YES |  |
| 32 | `vin` | varchar | YES |  |
| 33 | `nombremarca` | varchar | YES |  |
| 34 | `nombregama` | varchar | YES |  |
| 35 | `nombremodelo` | varchar | YES |  |
| 36 | `descripcionversiones` | varchar | YES |  |
| 37 | `descripcionsecciones` | varchar | YES |  |
| 38 | `idctabancaria` | bigint | YES |  |
| 39 | `descripcionctabancaria` | varchar | YES |  |
| 40 | `nombre` | varchar | YES |  |
| 41 | `monedaorigen` | varchar | YES |  |
| 42 | `idcomprausos` | varchar | YES |  |
| 43 | `codexternomodelo` | varchar | YES |  |
| 44 | `idincidenciatipos` | varchar | YES |  |
| 45 | `idtercerosactividadincidenciatipos` | bigint | YES |  |
| 46 | `idactividadincidenciatipos` | bigint | YES |  |
| 47 | `idactividadesdetincidenciatipos` | bigint | YES |  |
| 48 | `incidenciatiposdescripcion` | varchar | YES |  |
| 49 | `numproformafabrica` | varchar | YES |  |
| 50 | `idcompraestados` | varchar | YES |  |
| 51 | `idcomprasnumdet_abonado` | bigint | YES |  |
| 52 | `fechaalbaran` | timestamp(3) | YES |  |
| 53 | `fechaasiento_albaran` | timestamp(3) | YES |  |
| 54 | `seriealbaran` | varchar | YES |  |
| 55 | `numalbaran` | varchar | YES |  |
| 56 | `a�oalbaran` | varchar | YES |  |
| 57 | `baseimponible_albaran` | double | YES |  |
| 58 | `factorcambiomoneda_albaran` | double | YES |  |
| 59 | `fecharecepcion` | timestamp(3) | YES |  |
| 60 | `codproveedor` | bigint | YES |  |
| 61 | `proveedor` | varchar | YES |  |
| 62 | `load_date` | varchar | YES |  |

### spiga.spiga_consultamovimientosreferencia_2134111f7d0b06d37293747e962bbdba

**Columnas:** 163

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idtipolinea` | varchar | YES |  |
| 7 | `idmovimientotipos` | varchar | YES |  |
| 8 | `idmr` | varchar | YES |  |
| 9 | `idreferencias` | varchar | YES |  |
| 10 | `fechaalta` | timestamp(3) | YES |  |
| 11 | `idempresas` | bigint | YES |  |
| 12 | `idcentros` | bigint | YES |  |
| 13 | `idsecciones` | bigint | YES |  |
| 14 | `idubicaciones` | varchar | YES |  |
| 15 | `stock` | double | YES |  |
| 16 | `precio` | double | YES |  |
| 17 | `pmc` | double | YES |  |
| 18 | `confirmado` | bigint | YES |  |
| 19 | `unidades` | double | YES |  |
| 20 | `dtoporc` | double | YES |  |
| 21 | `idtarifas` | bigint | YES |  |
| 22 | `idclasificacion1movimiento` | varchar | YES |  |
| 23 | `hostmod` | varchar | YES |  |
| 24 | `usermod` | bigint | YES |  |
| 25 | `fechamod` | timestamp(3) | YES |  |
| 26 | `versionfila` | bigint | YES |  |
| 27 | `fechadocumento` | timestamp(3) | YES |  |
| 28 | `ida�o` | varchar | YES |  |
| 29 | `serie` | varchar | YES |  |
| 30 | `numero` | varchar | YES |  |
| 31 | `idterceros` | bigint | YES |  |
| 32 | `numdet` | bigint | YES |  |
| 33 | `seriefactura` | varchar | YES |  |
| 34 | `factura` | varchar | YES |  |
| 35 | `a�ofactura` | varchar | YES |  |
| 36 | `fechafactura` | timestamp(3) | YES |  |
| 37 | `idusuario` | bigint | YES |  |
| 38 | `loginguardadoautomatico` | bigint | YES |  |
| 39 | `hostguardadoautomatico` | varchar | YES |  |
| 40 | `fechaguardadoautomatico` | timestamp(3) | YES |  |
| 41 | `loginpteconfirmar` | bigint | YES |  |
| 42 | `hostpteconfirmar` | varchar | YES |  |
| 43 | `fechapteconfirmar` | timestamp(3) | YES |  |
| 44 | `idcentrosdestino` | bigint | YES |  |
| 45 | `idseccionesdestino` | bigint | YES |  |
| 46 | `idubicacionesdestino` | varchar | YES |  |
| 47 | `idcausaregularizacion` | bigint | YES |  |
| 48 | `idcausatraspaso` | bigint | YES |  |
| 49 | `a�oot` | varchar | YES |  |
| 50 | `serieot` | varchar | YES |  |
| 51 | `numot` | bigint | YES |  |
| 52 | `idtrabajo` | bigint | YES |  |
| 53 | `idempleadosalta` | bigint | YES |  |
| 54 | `fechacierre` | timestamp(3) | YES |  |
| 55 | `gastosadicionales` | double | YES |  |
| 56 | `gastosadicionalesalbaran` | double | YES |  |
| 57 | `incrementopvp` | double | YES |  |
| 58 | `undenvaseventa` | double | YES |  |
| 59 | `idestadoscompras` | varchar | YES |  |
| 60 | `idincidenciatipos` | varchar | YES |  |
| 61 | `undenvasecompra` | double | YES |  |
| 62 | `codras` | varchar | YES |  |
| 63 | `idimputaciontipos` | bigint | YES |  |
| 64 | `idtipocompra` | bigint | YES |  |
| 65 | `portes` | varchar | YES |  |
| 66 | `embalajes` | varchar | YES |  |
| 67 | `iddepartamentodestino` | varchar | YES |  |
| 68 | `descripcionmovimientotipo` | varchar | YES |  |
| 69 | `nombreempresa` | varchar | YES |  |
| 70 | `nombrecentro` | varchar | YES |  |
| 71 | `descripcionmr` | varchar | YES |  |
| 72 | `descripcionseccion` | varchar | YES |  |
| 73 | `iddepartamentos` | varchar | YES |  |
| 74 | `tipocargotaller` | varchar | YES |  |
| 75 | `ida�oppc` | varchar | YES |  |
| 76 | `idserieppc` | varchar | YES |  |
| 77 | `numeroppc` | varchar | YES |  |
| 78 | `numerodetppc` | varchar | YES |  |
| 79 | `tasas` | varchar | YES |  |
| 80 | `nombretercero` | varchar | YES |  |
| 81 | `nifcif` | varchar | YES |  |
| 82 | `idclientecategorias` | varchar | YES |  |
| 83 | `idmotivosabono` | varchar | YES |  |
| 84 | `descripcioncategoriacliente` | varchar | YES |  |
| 85 | `nombrecentrodestino` | varchar | YES |  |
| 86 | `descripcionsecciondestino` | varchar | YES |  |
| 87 | `iddepartamentosdestino` | varchar | YES |  |
| 88 | `descripcioncausaregularizacion` | varchar | YES |  |
| 89 | `descripciontipocompra` | varchar | YES |  |
| 90 | `descripcioncausaabonotipo` | varchar | YES |  |
| 91 | `descripcionimputaciontipos` | varchar | YES |  |
| 92 | `nombreempleado` | varchar | YES |  |
| 93 | `nombrefabricante` | varchar | YES |  |
| 94 | `descripcionreferencia` | varchar | YES |  |
| 95 | `descripcioncausatraspaso` | varchar | YES |  |
| 96 | `idfabricantes` | varchar | YES |  |
| 97 | `idclasificacion1` | varchar | YES |  |
| 98 | `idclasificacion2` | varchar | YES |  |
| 99 | `idclasificacion3` | varchar | YES |  |
| 100 | `idclasificacion4` | varchar | YES |  |
| 101 | `idclasificacion5` | varchar | YES |  |
| 102 | `idclasificacion6` | varchar | YES |  |
| 103 | `iddescuentos` | varchar | YES |  |
| 104 | `idrutasrecogida` | varchar | YES |  |
| 105 | `hostrecogida` | varchar | YES |  |
| 106 | `fecharecogida` | timestamp(3) | YES |  |
| 107 | `idempleadosrecogida` | varchar | YES |  |
| 108 | `unidadesrecogida` | varchar | YES |  |
| 109 | `idbultos` | varchar | YES |  |
| 110 | `idempleadosconfirmacion` | varchar | YES |  |
| 111 | `fechaconfirmacion` | timestamp(3) | YES |  |
| 112 | `hostconfirmacion` | varchar | YES |  |
| 113 | `unidadesalbaran` | varchar | YES |  |
| 114 | `idempleadosrecepcion` | varchar | YES |  |
| 115 | `hostrecepcion` | varchar | YES |  |
| 116 | `fecharecepcion` | timestamp(3) | YES |  |
| 117 | `unidadesrecibidas` | varchar | YES |  |
| 118 | `fechaubicacion` | timestamp(3) | YES |  |
| 119 | `idempleadosubicacion` | varchar | YES |  |
| 120 | `hostentrega` | varchar | YES |  |
| 121 | `fechaentrega` | timestamp(3) | YES |  |
| 122 | `idempleadosentrega` | varchar | YES |  |
| 123 | `hostubicacion` | varchar | YES |  |
| 124 | `nombreempleadoalta` | varchar | YES |  |
| 125 | `nombreempleadorecogida` | varchar | YES |  |
| 126 | `nombreempleadoconfirmacion` | varchar | YES |  |
| 127 | `nombreempleadorecepcion` | varchar | YES |  |
| 128 | `nombreempleadoubicacion` | varchar | YES |  |
| 129 | `nombreempleadoentrega` | varchar | YES |  |
| 130 | `descripcionincidenciatipos` | varchar | YES |  |
| 131 | `idpedidotipoventas` | varchar | YES |  |
| 132 | `descripcionpedidotipoventas` | varchar | YES |  |
| 133 | `nombremecanico` | varchar | YES |  |
| 134 | `nombretercerotrabajo` | varchar | YES |  |
| 135 | `apellido1tercerotrabajo` | varchar | YES |  |
| 136 | `apellido2tercerotrabajo` | varchar | YES |  |
| 137 | `nombrecomercialtercerotrabajo` | varchar | YES |  |
| 138 | `ventaespecial` | bigint | YES |  |
| 139 | `idtercerostrabajo` | varchar | YES |  |
| 140 | `codigobulto` | varchar | YES |  |
| 141 | `volumen` | double | YES |  |
| 142 | `factorcambiopmcontravalor` | double | YES |  |
| 143 | `descripcionclasificacion1` | varchar | YES |  |
| 144 | `descripcionclasificacion2` | varchar | YES |  |
| 145 | `descripcionclasificacion3` | varchar | YES |  |
| 146 | `descripcionclasificacion4` | varchar | YES |  |
| 147 | `descripcionclasificacion5` | varchar | YES |  |
| 148 | `descripcionclasificacion6` | varchar | YES |  |
| 149 | `descripcionclasificacion1movimiento` | varchar | YES |  |
| 150 | `preciocompra` | varchar | YES |  |
| 151 | `idmonedas` | varchar | YES |  |
| 152 | `factorcambiomoneda` | varchar | YES |  |
| 153 | `idusuariosautorizacion` | varchar | YES |  |
| 154 | `nombreusuarioautorizacion` | varchar | YES |  |
| 155 | `idnegociotipos` | varchar | YES |  |
| 156 | `nombreempleadovendedorrecambios` | varchar | YES |  |
| 157 | `seriefacturataller` | varchar | YES |  |
| 158 | `numerofacturataller` | varchar | YES |  |
| 159 | `a�ofacturataller` | varchar | YES |  |
| 160 | `fechafacturataller` | timestamp(3) | YES |  |
| 161 | `vin` | varchar | YES |  |
| 162 | `descripcionpedidotipocompras` | varchar | YES |  |
| 163 | `load_date` | varchar | YES |  |

### spiga.spiga_cotizacionesvn

**Columnas:** 81

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `fkofertasestados` | bigint | YES |  |
| 7 | `idempresas` | bigint | YES |  |
| 8 | `idcentros` | bigint | YES |  |
| 9 | `idofertas` | bigint | YES |  |
| 10 | `idterceros` | bigint | YES |  |
| 11 | `idclientespotentradas` | bigint | YES |  |
| 12 | `idmodulos` | varchar | YES |  |
| 13 | `totaloferta` | double | YES |  |
| 14 | `nombremarca` | varchar | YES |  |
| 15 | `nombregama` | varchar | YES |  |
| 16 | `fechacontrato` | timestamp(3) | YES |  |
| 17 | `numcontrato` | varchar | YES |  |
| 18 | `idventatipos` | varchar | YES |  |
| 19 | `fechaprevista` | timestamp(3) | YES |  |
| 20 | `numpedidovnreserva` | varchar | YES |  |
| 21 | `observacionesinternas` | varchar | YES |  |
| 22 | `observacionesexternas` | varchar | YES |  |
| 23 | `idmonedas` | bigint | YES |  |
| 24 | `factorcambiomoneda` | double | YES |  |
| 25 | `fechaalta` | timestamp(3) | YES |  |
| 26 | `a�ooferta` | varchar | YES |  |
| 27 | `serieoferta` | varchar | YES |  |
| 28 | `numoferta` | varchar | YES |  |
| 29 | `idcentrospedido` | bigint | YES |  |
| 30 | `idventamarcatipos` | varchar | YES |  |
| 31 | `diasentregafabrica` | bigint | YES |  |
| 32 | `vin` | varchar | YES |  |
| 33 | `matricula` | varchar | YES |  |
| 34 | `nombre` | varchar | YES |  |
| 35 | `idmarcas` | bigint | YES |  |
| 36 | `idgamas` | bigint | YES |  |
| 37 | `codmodelo` | varchar | YES |  |
| 38 | `extmodelo` | varchar | YES |  |
| 39 | `a�omodelo` | varchar | YES |  |
| 40 | `idversiones` | varchar | YES |  |
| 41 | `idtarifas` | bigint | YES |  |
| 42 | `codexternomodelo` | varchar | YES |  |
| 43 | `nombrecentro` | varchar | YES |  |
| 44 | `fechabajacliente` | timestamp(3) | YES |  |
| 45 | `telefonomovil` | varchar | YES |  |
| 46 | `email` | varchar | YES |  |
| 47 | `fechaautorizacion` | timestamp(3) | YES |  |
| 48 | `fechaaceptacion` | timestamp(3) | YES |  |
| 49 | `fechaventa` | timestamp(3) | YES |  |
| 50 | `nombrevendedorasignado` | varchar | YES |  |
| 51 | `importesaldado` | double | YES |  |
| 52 | `idplantillacalculo` | varchar | YES |  |
| 53 | `descripcionplantilla` | varchar | YES |  |
| 54 | `importevoacambio` | double | YES |  |
| 55 | `nifcifclientepot` | varchar | YES |  |
| 56 | `importe` | double | YES |  |
| 57 | `porcentaje` | double | YES |  |
| 58 | `nombrevendedor` | varchar | YES |  |
| 59 | `pkopcionales` | varchar | YES |  |
| 60 | `idimsconcesionarios` | bigint | YES |  |
| 61 | `idimscuentas` | bigint | YES |  |
| 62 | `idimssucursales` | bigint | YES |  |
| 63 | `idimsvendedores` | bigint | YES |  |
| 64 | `nombreimsvendedor` | varchar | YES |  |
| 65 | `idsecciones` | bigint | YES |  |
| 66 | `fechasalida` | timestamp(3) | YES |  |
| 67 | `vosentregados` | bigint | YES |  |
| 68 | `idvehiculos` | bigint | YES |  |
| 69 | `codclientepot` | bigint | YES |  |
| 70 | `descripcion` | varchar | YES |  |
| 71 | `nombremodelo` | varchar | YES |  |
| 72 | `nombreversion` | varchar | YES |  |
| 73 | `descripcionofertasestados` | varchar | YES |  |
| 74 | `descripcionsecciones` | varchar | YES |  |
| 75 | `estadofinanciacion` | varchar | YES |  |
| 76 | `intencionescompradescripcion` | varchar | YES |  |
| 77 | `clientepotclasificaciondescripcion` | varchar | YES |  |
| 78 | `descripcionprocedencia` | varchar | YES |  |
| 79 | `descripcionsalidatipos` | varchar | YES |  |
| 80 | `fechaentrada` | timestamp(3) | YES |  |
| 81 | `load_date` | varchar | YES |  |

### spiga.spiga_cotizacionesvo

**Columnas:** 72

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idvehiculos` | bigint | YES |  |
| 7 | `fkofertasestados` | bigint | YES |  |
| 8 | `idempresas` | bigint | YES |  |
| 9 | `idcentros` | bigint | YES |  |
| 10 | `idofertas` | bigint | YES |  |
| 11 | `idterceros` | bigint | YES |  |
| 12 | `idclientespotentradas` | bigint | YES |  |
| 13 | `idmonedas` | bigint | YES |  |
| 14 | `factorcambiomoneda` | double | YES |  |
| 15 | `a�ooferta` | varchar | YES |  |
| 16 | `serieoferta` | varchar | YES |  |
| 17 | `numoferta` | varchar | YES |  |
| 18 | `idmodulos` | varchar | YES |  |
| 19 | `totaloferta` | double | YES |  |
| 20 | `idmarcas` | bigint | YES |  |
| 21 | `idgamas` | bigint | YES |  |
| 22 | `codmodelo` | varchar | YES |  |
| 23 | `extmodelo` | varchar | YES |  |
| 24 | `a�omodelo` | varchar | YES |  |
| 25 | `idversiones` | varchar | YES |  |
| 26 | `nombremarca` | varchar | YES |  |
| 27 | `nombregama` | varchar | YES |  |
| 28 | `serieexpedientereserva` | varchar | YES |  |
| 29 | `numexpedientereserva` | bigint | YES |  |
| 30 | `a�oexpedientereserva` | varchar | YES |  |
| 31 | `idcentrosexpedientereserva` | bigint | YES |  |
| 32 | `fechareserva` | timestamp(3) | YES |  |
| 33 | `idofertasestados` | bigint | YES |  |
| 34 | `vin` | varchar | YES |  |
| 35 | `matricula` | varchar | YES |  |
| 36 | `nombre` | varchar | YES |  |
| 37 | `nombrecentro` | varchar | YES |  |
| 38 | `fechaautorizacion` | timestamp(3) | YES |  |
| 39 | `fechaaceptacion` | timestamp(3) | YES |  |
| 40 | `nombrevendedorasignado` | varchar | YES |  |
| 41 | `importesaldado` | double | YES |  |
| 42 | `nifcifclientepot` | varchar | YES |  |
| 43 | `idplantillacalculo` | varchar | YES |  |
| 44 | `descripcionplantilla` | varchar | YES |  |
| 45 | `importevoacambio` | double | YES |  |
| 46 | `codclientepot` | bigint | YES |  |
| 47 | `telefonomovil` | varchar | YES |  |
| 48 | `email` | varchar | YES |  |
| 49 | `importe` | double | YES |  |
| 50 | `porcentaje` | double | YES |  |
| 51 | `nombrevendedor` | varchar | YES |  |
| 52 | `idopcionalescolorvo` | varchar | YES |  |
| 53 | `idopcionalestapizadovo` | varchar | YES |  |
| 54 | `nombreempresa` | varchar | YES |  |
| 55 | `tercerointeresado` | bigint | YES |  |
| 56 | `idsecciones` | bigint | YES |  |
| 57 | `descripcionsecciones` | varchar | YES |  |
| 58 | `fechaalta` | timestamp(3) | YES |  |
| 59 | `idopcionales` | varchar | YES |  |
| 60 | `descripcionprocedencia` | varchar | YES |  |
| 61 | `fechasalida` | timestamp(3) | YES |  |
| 62 | `vosentregados` | bigint | YES |  |
| 63 | `nombremodelo` | varchar | YES |  |
| 64 | `nombreversion` | varchar | YES |  |
| 65 | `descripcion` | varchar | YES |  |
| 66 | `descripcioncolorvo` | varchar | YES |  |
| 67 | `descripciontapizadovo` | varchar | YES |  |
| 68 | `descripcionofertaestados` | varchar | YES |  |
| 69 | `intencionescompradescripcion` | varchar | YES |  |
| 70 | `clientepotclasificaciondescripcion` | varchar | YES |  |
| 71 | `descripcionsalidatipos` | varchar | YES |  |
| 72 | `load_date` | varchar | YES |  |

### spiga.spiga_datosterceros

**Columnas:** 50

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `pkfkempresas` | bigint | YES |  |
| 7 | `nombreempresa` | varchar | YES |  |
| 8 | `pkterceros` | bigint | YES |  |
| 9 | `fkpaises` | varchar | YES |  |
| 10 | `fkterceroclases` | bigint | YES |  |
| 11 | `nombreterceroclases` | varchar | YES |  |
| 12 | `nifcif` | varchar | YES |  |
| 13 | `nifcif_fechaexpedicion` | timestamp(3) | YES |  |
| 14 | `nifcif_lugarexpedicion` | varchar | YES |  |
| 15 | `nombre` | varchar | YES |  |
| 16 | `apellido1` | varchar | YES |  |
| 17 | `apellido2` | varchar | YES |  |
| 18 | `nombrecomercial` | varchar | YES |  |
| 19 | `fechaalta` | timestamp(3) | YES |  |
| 20 | `fechabaja` | timestamp(3) | YES |  |
| 21 | `fkdocumentaciontipos` | bigint | YES |  |
| 22 | `descrpciondocumentaciontipos` | varchar | YES |  |
| 23 | `fknaturalezajuridicatipos` | varchar | YES |  |
| 24 | `descripcionnaturalezajuridicatipos` | varchar | YES |  |
| 25 | `tipocontribuyente` | varchar | YES |  |
| 26 | `descripciontipocontribuyente` | varchar | YES |  |
| 27 | `agenteretenedor` | bigint | YES |  |
| 28 | `fechatipocontribuyente` | timestamp(3) | YES |  |
| 29 | `resolucion` | varchar | YES |  |
| 30 | `fkcodigospostales` | varchar | YES |  |
| 31 | `poblacion` | varchar | YES |  |
| 32 | `provincia` | varchar | YES |  |
| 33 | `fkprofesiones` | bigint | YES |  |
| 34 | `descripcionprofesiones` | varchar | YES |  |
| 35 | `fktercerocargos` | bigint | YES |  |
| 36 | `descripcionterceroscargos` | varchar | YES |  |
| 37 | `fkterceroformacionniveles` | bigint | YES |  |
| 38 | `descripcionterceroformacionniveles` | varchar | YES |  |
| 39 | `fechanacimiento` | timestamp(3) | YES |  |
| 40 | `fechacarnet` | timestamp(3) | YES |  |
| 41 | `fechacarnetcaducidad` | timestamp(3) | YES |  |
| 42 | `numerohijos` | bigint | YES |  |
| 43 | `fkestadociviltipos` | varchar | YES |  |
| 44 | `descripcionestadociviltipos` | varchar | YES |  |
| 45 | `sexo` | varchar | YES |  |
| 46 | `fkactividadtipos` | varchar | YES |  |
| 47 | `descripcionactividadtipos` | varchar | YES |  |
| 48 | `claseconcepto` | varchar | YES |  |
| 49 | `numlicenciaconducir` | varchar | YES |  |
| 50 | `load_date` | varchar | YES |  |

### spiga.spiga_empleados

**Columnas:** 33

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempleados` | bigint | YES |  |
| 7 | `idprofesiones` | bigint | YES |  |
| 8 | `idterceros` | bigint | YES |  |
| 9 | `idpagoformasnomina` | varchar | YES |  |
| 10 | `numeross` | varchar | YES |  |
| 11 | `porcretencion` | double | YES |  |
| 12 | `cuentaentidad` | varchar | YES |  |
| 13 | `cuentasucursal` | varchar | YES |  |
| 14 | `cuentadc` | varchar | YES |  |
| 15 | `cuentanumero` | varchar | YES |  |
| 16 | `cuentaidpaises` | varchar | YES |  |
| 17 | `cuentaiban` | varchar | YES |  |
| 18 | `cuentaswift` | varchar | YES |  |
| 19 | `fechaalta` | timestamp(3) | YES |  |
| 20 | `fechabaja` | timestamp(3) | YES |  |
| 21 | `usermod` | bigint | YES |  |
| 22 | `hostmod` | varchar | YES |  |
| 23 | `versionfila` | bigint | YES |  |
| 24 | `idusuarios` | bigint | YES |  |
| 25 | `idempleadocuentabancotipos` | varchar | YES |  |
| 26 | `nombre` | varchar | YES |  |
| 27 | `apellido1` | varchar | YES |  |
| 28 | `apellido2` | varchar | YES |  |
| 29 | `nifcif` | varchar | YES |  |
| 30 | `usermodtercero` | bigint | YES |  |
| 31 | `hostmodtercero` | varchar | YES |  |
| 32 | `versionfilatercero` | bigint | YES |  |
| 33 | `load_date` | varchar | YES |  |

### spiga.spiga_entradasataller_7eaa3eba4b6aac793d37dbec0f09eff4

**Columnas:** 119

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | varchar | YES |  |
| 2 | `idconsecutivo` | varchar | YES |  |
| 3 | `ano_periodo` | varchar | YES |  |
| 4 | `mes_periodo` | varchar | YES |  |
| 5 | `fechadecorte` | varchar | YES |  |
| 6 | `idempresas` | varchar | YES |  |
| 7 | `idcentros` | varchar | YES |  |
| 8 | `a�oot` | varchar | YES |  |
| 9 | `serieot` | varchar | YES |  |
| 10 | `numot` | varchar | YES |  |
| 11 | `numtrabajo` | varchar | YES |  |
| 12 | `idtrabajoestados` | varchar | YES |  |
| 13 | `descripcion` | varchar | YES |  |
| 14 | `idterceros` | varchar | YES |  |
| 15 | `preciohora` | varchar | YES |  |
| 16 | `numeropoliza` | varchar | YES |  |
| 17 | `importefranquicia` | varchar | YES |  |
| 18 | `idmanoobratipos` | varchar | YES |  |
| 19 | `idtrabajotipos` | varchar | YES |  |
| 20 | `idsecciones` | varchar | YES |  |
| 21 | `nombreseccion` | varchar | YES |  |
| 22 | `preciocoste` | varchar | YES |  |
| 23 | `idseccioncargos` | varchar | YES |  |
| 24 | `idcargotipos` | varchar | YES |  |
| 25 | `observaciones` | varchar | YES |  |
| 26 | `fechaalta` | varchar | YES |  |
| 27 | `fechamodificacion` | varchar | YES |  |
| 28 | `fechacierre` | varchar | YES |  |
| 29 | `a�opresupuesto` | varchar | YES |  |
| 30 | `seriepresupuesto` | varchar | YES |  |
| 31 | `idpresupuesto` | varchar | YES |  |
| 32 | `a�ofactura` | varchar | YES |  |
| 33 | `seriefactura` | varchar | YES |  |
| 34 | `numfactura` | varchar | YES |  |
| 35 | `iddepartamentocargointerno` | varchar | YES |  |
| 36 | `idimputaciontipos` | varchar | YES |  |
| 37 | `idseccioncargointerno` | varchar | YES |  |
| 38 | `idcentrosdestino` | varchar | YES |  |
| 39 | `idseriesgarantias` | varchar | YES |  |
| 40 | `numgarantias` | varchar | YES |  |
| 41 | `a�ogarantias` | varchar | YES |  |
| 42 | `idempleadosalta` | varchar | YES |  |
| 43 | `idempleadoscierre` | varchar | YES |  |
| 44 | `fechaenvioinspeccion` | varchar | YES |  |
| 45 | `fechafacturacion` | varchar | YES |  |
| 46 | `numeroautorizacion` | varchar | YES |  |
| 47 | `usermod` | varchar | YES |  |
| 48 | `hostmod` | varchar | YES |  |
| 49 | `versionfila` | varchar | YES |  |
| 50 | `a�oasiento` | varchar | YES |  |
| 51 | `idasiento` | varchar | YES |  |
| 52 | `a�oasiento_garantiafacturada` | varchar | YES |  |
| 53 | `idasiento_garantiafacturada` | varchar | YES |  |
| 54 | `trabajorepetido` | varchar | YES |  |
| 55 | `numsiniestro` | varchar | YES |  |
| 56 | `respuestainspeccion` | varchar | YES |  |
| 57 | `numgarantiamarca` | varchar | YES |  |
| 58 | `importemo` | varchar | YES |  |
| 59 | `importemopresupuesto` | varchar | YES |  |
| 60 | `importemat` | varchar | YES |  |
| 61 | `importematpresupuesto` | varchar | YES |  |
| 62 | `importesub` | varchar | YES |  |
| 63 | `importesubpresupuesto` | varchar | YES |  |
| 64 | `importevar` | varchar | YES |  |
| 65 | `importevarpresupuesto` | varchar | YES |  |
| 66 | `importepint` | varchar | YES |  |
| 67 | `importepintpresupuesto` | varchar | YES |  |
| 68 | `horasmo` | varchar | YES |  |
| 69 | `horasmopresupuesto` | varchar | YES |  |
| 70 | `fechaentrada` | varchar | YES |  |
| 71 | `idcalletipos` | varchar | YES |  |
| 72 | `matricula` | varchar | YES |  |
| 73 | `vin` | varchar | YES |  |
| 74 | `fechamatriculacion` | varchar | YES |  |
| 75 | `idmarcas` | varchar | YES |  |
| 76 | `nombremarca` | varchar | YES |  |
| 77 | `idgamas` | varchar | YES |  |
| 78 | `nombregama` | varchar | YES |  |
| 79 | `nombreasesor` | varchar | YES |  |
| 80 | `nombrepropietario` | varchar | YES |  |
| 81 | `telefonoparticular` | varchar | YES |  |
| 82 | `telefonomovil` | varchar | YES |  |
| 83 | `idempleados` | varchar | YES |  |
| 84 | `descripciontrabajotipos` | varchar | YES |  |
| 85 | `diferenciadias` | varchar | YES |  |
| 86 | `descripcionsegmento` | varchar | YES |  |
| 87 | `email` | varchar | YES |  |
| 88 | `descripciontipocalle` | varchar | YES |  |
| 89 | `nombrecalle` | varchar | YES |  |
| 90 | `numero` | varchar | YES |  |
| 91 | `bloque` | varchar | YES |  |
| 92 | `piso` | varchar | YES |  |
| 93 | `puerta` | varchar | YES |  |
| 94 | `complemento` | varchar | YES |  |
| 95 | `complemento2` | varchar | YES |  |
| 96 | `poblacion` | varchar | YES |  |
| 97 | `idcodigospostales` | varchar | YES |  |
| 98 | `nombreestado` | varchar | YES |  |
| 99 | `esabono` | varchar | YES |  |
| 100 | `esabonogarantia` | varchar | YES |  |
| 101 | `idrecepciontipos` | varchar | YES |  |
| 102 | `kmts` | varchar | YES |  |
| 103 | `fechaprevistaentrega` | varchar | YES |  |
| 104 | `fechaentrega` | varchar | YES |  |
| 105 | `idvehiculos` | varchar | YES |  |
| 106 | `nombretercerocargo` | varchar | YES |  |
| 107 | `apellido1tercerocargo` | varchar | YES |  |
| 108 | `apellido2tercerocargo` | varchar | YES |  |
| 109 | `nombrevendedor` | varchar | YES |  |
| 110 | `apellido1vendedor` | varchar | YES |  |
| 111 | `apellido2vendedor` | varchar | YES |  |
| 112 | `descripcionrecepcion` | varchar | YES |  |
| 113 | `idclientespotclasificaciones` | varchar | YES |  |
| 114 | `horasuso` | varchar | YES |  |
| 115 | `idmotivoentrada` | varchar | YES |  |
| 116 | `descripcionmotivoentrada` | varchar | YES |  |
| 117 | `asesorservicioresponsable` | varchar | YES |  |
| 118 | `vehiculocortesia` | varchar | YES |  |
| 119 | `load_date` | varchar | YES |  |

### spiga.spiga_facturadosnoentregadosvn

**Columnas:** 154

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `numventa` | bigint | YES |  |
| 12 | `fechaventa` | timestamp(3) | YES |  |
| 13 | `comisionagente` | double | YES |  |
| 14 | `idpaisesexportacion` | varchar | YES |  |
| 15 | `a�oasientoentrega` | varchar | YES |  |
| 16 | `idasientosentrega` | bigint | YES |  |
| 17 | `idmonedas` | bigint | YES |  |
| 18 | `factorcambiomoneda` | double | YES |  |
| 19 | `fkterceros_agente` | bigint | YES |  |
| 20 | `nombreagente` | varchar | YES |  |
| 21 | `seriefacturacompra` | varchar | YES |  |
| 22 | `numfacturacompra` | varchar | YES |  |
| 23 | `a�ofacturacompra` | varchar | YES |  |
| 24 | `fechafacturacompra` | timestamp(3) | YES |  |
| 25 | `idcompraestados` | varchar | YES |  |
| 26 | `descripcioncompraestados` | varchar | YES |  |
| 27 | `preciocompra` | double | YES |  |
| 28 | `ventafinal` | bigint | YES |  |
| 29 | `facturaprincipal` | varchar | YES |  |
| 30 | `fechafacturaprincipal` | timestamp(3) | YES |  |
| 31 | `terceroprincipal` | bigint | YES |  |
| 32 | `nifcifprincipal` | varchar | YES |  |
| 33 | `perfilterceroprincipal` | varchar | YES |  |
| 34 | `nombreterceroprincipal` | varchar | YES |  |
| 35 | `direccionterceroprincipal` | varchar | YES |  |
| 36 | `codigopostalterceroprincipal` | varchar | YES |  |
| 37 | `idcodigospostalesterceroprincipal` | varchar | YES |  |
| 38 | `poblacionterceroprincipal` | varchar | YES |  |
| 39 | `provinciaterceroprincipal` | varchar | YES |  |
| 40 | `telefonoprincipalterceroprincipal` | varchar | YES |  |
| 41 | `telefonoparticularterceroprincipal` | varchar | YES |  |
| 42 | `telefonomovilterceroprincipal` | varchar | YES |  |
| 43 | `telefonotrabajoterceroprincipal` | varchar | YES |  |
| 44 | `facturasecundaria` | varchar | YES |  |
| 45 | `fechafacturasecundaria` | timestamp(3) | YES |  |
| 46 | `tercerosecundaria` | bigint | YES |  |
| 47 | `nombretercerosecundaria` | varchar | YES |  |
| 48 | `direcciontercerosecundaria` | varchar | YES |  |
| 49 | `poblaciontercerosecundaria` | varchar | YES |  |
| 50 | `provinciatercerosecundaria` | varchar | YES |  |
| 51 | `fechamatriculacion` | timestamp(3) | YES |  |
| 52 | `fechadespacho` | timestamp(3) | YES |  |
| 53 | `vin` | varchar | YES |  |
| 54 | `matricula` | varchar | YES |  |
| 55 | `sitiomatricula` | varchar | YES |  |
| 56 | `numeromotor` | varchar | YES |  |
| 57 | `idmarcas` | bigint | YES |  |
| 58 | `nombremarca` | varchar | YES |  |
| 59 | `idgamas` | bigint | YES |  |
| 60 | `nombregama` | varchar | YES |  |
| 61 | `codmodelo` | varchar | YES |  |
| 62 | `extmodelo` | varchar | YES |  |
| 63 | `a�omodelo` | varchar | YES |  |
| 64 | `nombremodelo` | varchar | YES |  |
| 65 | `idempleados` | bigint | YES |  |
| 66 | `nombrevendedor` | varchar | YES |  |
| 67 | `idventatipos` | varchar | YES |  |
| 68 | `descripcionventatipos` | varchar | YES |  |
| 69 | `idcompratipos` | varchar | YES |  |
| 70 | `descripcioncompratipos` | varchar | YES |  |
| 71 | `idventamarcatipos` | varchar | YES |  |
| 72 | `descripcionventamarcatipos` | varchar | YES |  |
| 73 | `idventafinanciaciontipos` | varchar | YES |  |
| 74 | `descripcionventafinanciaciontipos` | varchar | YES |  |
| 75 | `idversiones` | varchar | YES |  |
| 76 | `descripcionversion` | varchar | YES |  |
| 77 | `baseimponible` | double | YES |  |
| 78 | `baseexenta` | double | YES |  |
| 79 | `impuestos` | double | YES |  |
| 80 | `acondicionamiento` | double | YES |  |
| 81 | `totalventa` | double | YES |  |
| 82 | `diferencialanticipo` | double | YES |  |
| 83 | `identradatipos` | varchar | YES |  |
| 84 | `provisiondegastosinternos` | double | YES |  |
| 85 | `provisiondegastosexternos` | double | YES |  |
| 86 | `descripcionentradatipos` | varchar | YES |  |
| 87 | `complemento2terceroprincipal` | varchar | YES |  |
| 88 | `idofertas` | bigint | YES |  |
| 89 | `fechaoferta` | timestamp(3) | YES |  |
| 90 | `nombrefinanciera` | varchar | YES |  |
| 91 | `apellido1financiera` | varchar | YES |  |
| 92 | `apellido2financiera` | varchar | YES |  |
| 93 | `nombreconductor` | varchar | YES |  |
| 94 | `apellido1conductor` | varchar | YES |  |
| 95 | `apellido2conductor` | varchar | YES |  |
| 96 | `idclientespotentradas` | bigint | YES |  |
| 97 | `nombrecentro` | varchar | YES |  |
| 98 | `idsecciones` | bigint | YES |  |
| 99 | `nombreseccion` | varchar | YES |  |
| 100 | `idterceroscolaborador` | bigint | YES |  |
| 101 | `nombrecolaborador` | varchar | YES |  |
| 102 | `detallaropcionalesfactura` | bigint | YES |  |
| 103 | `importevehiculoscambio` | double | YES |  |
| 104 | `expedientesvehiculoscambio` | varchar | YES |  |
| 105 | `comision` | varchar | YES |  |
| 106 | `idcalletiposprincipal` | varchar | YES |  |
| 107 | `nombrecalleprincipal` | varchar | YES |  |
| 108 | `numeroprincipal` | varchar | YES |  |
| 109 | `bloqueprincipal` | varchar | YES |  |
| 110 | `pisoprincipal` | varchar | YES |  |
| 111 | `puertaprincipal` | varchar | YES |  |
| 112 | `poblacionprincipal` | varchar | YES |  |
| 113 | `provinciaprincipal` | varchar | YES |  |
| 114 | `idcodigospostalesprincipal` | varchar | YES |  |
| 115 | `fechaentregacliente` | timestamp(3) | YES |  |
| 116 | `versionfila` | bigint | YES |  |
| 117 | `idvehiculos` | bigint | YES |  |
| 118 | `vnfechainiciogarantia` | varchar | YES |  |
| 119 | `mesesgarantiaobligatoriavn` | bigint | YES |  |
| 120 | `mesesgarantiaobligatoriavn_chapa` | bigint | YES |  |
| 121 | `mesesgarantiaobligatoriavn_pintura` | bigint | YES |  |
| 122 | `mesesgarantiaobligatoriavn_motor` | bigint | YES |  |
| 123 | `nombresecundario` | varchar | YES |  |
| 124 | `apellido1secundario` | varchar | YES |  |
| 125 | `apellido2secundario` | varchar | YES |  |
| 126 | `idempleadoscolaborador` | bigint | YES |  |
| 127 | `nombreempleadocolaborador` | varchar | YES |  |
| 128 | `nombrepropietario` | varchar | YES |  |
| 129 | `apellido1propietario` | varchar | YES |  |
| 130 | `apellido2propietario` | varchar | YES |  |
| 131 | `codexternomodelo` | varchar | YES |  |
| 132 | `ubicacion` | varchar | YES |  |
| 133 | `idnegociotipos` | varchar | YES |  |
| 134 | `importependientecobro` | double | YES |  |
| 135 | `fechapazsalvo` | timestamp(3) | YES |  |
| 136 | `a�opazsalvo` | varchar | YES |  |
| 137 | `seriepazsalvo` | varchar | YES |  |
| 138 | `numpazsalvo` | bigint | YES |  |
| 139 | `nombreempleadoemitepse` | varchar | YES |  |
| 140 | `apellido1empleadoemitepse` | varchar | YES |  |
| 141 | `apellido2empleadoemitepse` | varchar | YES |  |
| 142 | `idtercerosalquilador` | bigint | YES |  |
| 143 | `nombrealquilador` | varchar | YES |  |
| 144 | `apellido1alquilador` | varchar | YES |  |
| 145 | `apellido2alquilador` | varchar | YES |  |
| 146 | `detallaropcionalesconcesionfactura` | bigint | YES |  |
| 147 | `detallarcampa�asfactura` | bigint | YES |  |
| 148 | `idseriestransporte` | varchar | YES |  |
| 149 | `idnumtransporte` | bigint | YES |  |
| 150 | `obsinternas` | varchar | YES |  |
| 151 | `nifcifvendedor` | varchar | YES |  |
| 152 | `margenventaimportador` | double | YES |  |
| 153 | `fecharecepcion` | timestamp(3) | YES |  |
| 154 | `load_date` | varchar | YES |  |

### spiga.spiga_facturadosnoentregadosvo

**Columnas:** 138

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `numventa` | bigint | YES |  |
| 12 | `fechaventa` | timestamp(3) | YES |  |
| 13 | `kms` | bigint | YES |  |
| 14 | `idtercerosfinanciera` | bigint | YES |  |
| 15 | `nombrefinanciera` | varchar | YES |  |
| 16 | `idterceroscolaborador` | bigint | YES |  |
| 17 | `nombrecolaborador` | varchar | YES |  |
| 18 | `preciocompra` | double | YES |  |
| 19 | `pkcompraestados` | varchar | YES |  |
| 20 | `descripcioncompraestados` | varchar | YES |  |
| 21 | `ventafinal` | bigint | YES |  |
| 22 | `nombreproveedor` | varchar | YES |  |
| 23 | `facturacompra` | varchar | YES |  |
| 24 | `facturaprincipal` | varchar | YES |  |
| 25 | `terceroprincipal` | bigint | YES |  |
| 26 | `nifcifprincipal` | varchar | YES |  |
| 27 | `perfilterceroprincipal` | varchar | YES |  |
| 28 | `nombreterceroprincipal` | varchar | YES |  |
| 29 | `direccionterceroprincipal` | varchar | YES |  |
| 30 | `codigopostalterceroprincipal` | varchar | YES |  |
| 31 | `idcodigospostalesterceroprincipal` | varchar | YES |  |
| 32 | `poblacionterceroprincipal` | varchar | YES |  |
| 33 | `provinciaterceroprincipal` | varchar | YES |  |
| 34 | `clientecategoriaterceroprincipal` | varchar | YES |  |
| 35 | `telefonoprincipalterceroprincipal` | varchar | YES |  |
| 36 | `telefonoparticularterceroprincipal` | varchar | YES |  |
| 37 | `telefonomovilterceroprincipal` | varchar | YES |  |
| 38 | `telefonotrabajoterceroprincipal` | varchar | YES |  |
| 39 | `facturasecundaria` | varchar | YES |  |
| 40 | `tercerosecundaria` | bigint | YES |  |
| 41 | `nombretercerosecundaria` | varchar | YES |  |
| 42 | `direcciontercerosecundaria` | varchar | YES |  |
| 43 | `codigopostaltercerosecundaria` | varchar | YES |  |
| 44 | `idcodigospostalestercerosecundaria` | varchar | YES |  |
| 45 | `poblaciontercerosecundaria` | varchar | YES |  |
| 46 | `provinciatercerosecundaria` | varchar | YES |  |
| 47 | `telefonoprincipaltercerosecundaria` | varchar | YES |  |
| 48 | `telefonoparticulartercerosecundaria` | varchar | YES |  |
| 49 | `telefonomoviltercerosecundaria` | varchar | YES |  |
| 50 | `telefonotrabajotercerosecundaria` | varchar | YES |  |
| 51 | `fechamatriculacion` | timestamp(3) | YES |  |
| 52 | `fechadespacho` | timestamp(3) | YES |  |
| 53 | `vin` | varchar | YES |  |
| 54 | `matricula` | varchar | YES |  |
| 55 | `numeromotor` | varchar | YES |  |
| 56 | `idmarcas` | bigint | YES |  |
| 57 | `nombremarca` | varchar | YES |  |
| 58 | `idgamas` | bigint | YES |  |
| 59 | `nombregama` | varchar | YES |  |
| 60 | `codmodelo` | varchar | YES |  |
| 61 | `extmodelo` | varchar | YES |  |
| 62 | `a�omodelo` | varchar | YES |  |
| 63 | `nombremodelo` | varchar | YES |  |
| 64 | `idempleados` | bigint | YES |  |
| 65 | `nombrevendedor` | varchar | YES |  |
| 66 | `idventatipos` | varchar | YES |  |
| 67 | `descripcionventatipos` | varchar | YES |  |
| 68 | `idcompratipos` | varchar | YES |  |
| 69 | `descripcioncompratipos` | varchar | YES |  |
| 70 | `idversiones` | varchar | YES |  |
| 71 | `descripcionversion` | varchar | YES |  |
| 72 | `idventainternatipos` | varchar | YES |  |
| 73 | `descripcionventainternatipos` | varchar | YES |  |
| 74 | `baseimponible` | double | YES |  |
| 75 | `baseexenta` | double | YES |  |
| 76 | `importesuplidosgestoria` | double | YES |  |
| 77 | `importeprovision` | double | YES |  |
| 78 | `diferencialanticipo` | double | YES |  |
| 79 | `baseexentaventa` | double | YES |  |
| 80 | `importeimpuestoventa` | double | YES |  |
| 81 | `importegastos` | double | YES |  |
| 82 | `codigoagente` | varchar | YES |  |
| 83 | `expedientecambio` | varchar | YES |  |
| 84 | `esacambio` | bigint | YES |  |
| 85 | `idofertas` | bigint | YES |  |
| 86 | `fechaoferta` | timestamp(3) | YES |  |
| 87 | `localidadterceroprincipal` | varchar | YES |  |
| 88 | `complemento2terceroprincipal` | varchar | YES |  |
| 89 | `nombreconductor` | varchar | YES |  |
| 90 | `apellido1conductor` | varchar | YES |  |
| 91 | `apellido2conductor` | varchar | YES |  |
| 92 | `idclientespotentradasoferta` | bigint | YES |  |
| 93 | `nombrecentro` | varchar | YES |  |
| 94 | `comisioncolaborador` | double | YES |  |
| 95 | `idsecciones` | bigint | YES |  |
| 96 | `nombreseccion` | varchar | YES |  |
| 97 | `diasantiguedadstock` | bigint | YES |  |
| 98 | `mesesantiguedadstock` | bigint | YES |  |
| 99 | `precioventarecomendado` | double | YES |  |
| 100 | `expedientesvehiculoscambio` | varchar | YES |  |
| 101 | `importevehiculoscambio` | double | YES |  |
| 102 | `comision` | varchar | YES |  |
| 103 | `idcalletiposprincipal` | varchar | YES |  |
| 104 | `nombrecalleprincipal` | varchar | YES |  |
| 105 | `numeroprincipal` | varchar | YES |  |
| 106 | `bloqueprincipal` | varchar | YES |  |
| 107 | `pisoprincipal` | varchar | YES |  |
| 108 | `puertaprincipal` | varchar | YES |  |
| 109 | `poblacionprincipal` | varchar | YES |  |
| 110 | `provinciaprincipal` | varchar | YES |  |
| 111 | `idcodigospostalesprincipal` | varchar | YES |  |
| 112 | `fechaentregacliente` | timestamp(3) | YES |  |
| 113 | `fechapazsalvo` | timestamp(3) | YES |  |
| 114 | `a�opazsalvo` | varchar | YES |  |
| 115 | `seriepazsalvo` | varchar | YES |  |
| 116 | `numpazsalvo` | bigint | YES |  |
| 117 | `nombreempleadoemitepse` | varchar | YES |  |
| 118 | `apellido1empleadoemitepse` | varchar | YES |  |
| 119 | `apellido2empleadoemitepse` | varchar | YES |  |
| 120 | `nombresecundario` | varchar | YES |  |
| 121 | `apellido1secundario` | varchar | YES |  |
| 122 | `apellido2secundario` | varchar | YES |  |
| 123 | `idempleadoscolaborador` | bigint | YES |  |
| 124 | `nombreempleadocolaborador` | varchar | YES |  |
| 125 | `nombrepropietario` | varchar | YES |  |
| 126 | `apellido1propietario` | varchar | YES |  |
| 127 | `apellido2propietario` | varchar | YES |  |
| 128 | `totalventa` | double | YES |  |
| 129 | `impuestos` | double | YES |  |
| 130 | `codexternomodelo` | varchar | YES |  |
| 131 | `ubicacion` | varchar | YES |  |
| 132 | `idnegociotipos` | varchar | YES |  |
| 133 | `importependientecobro` | double | YES |  |
| 134 | `nifcifvendedor` | varchar | YES |  |
| 135 | `obsinternas` | varchar | YES |  |
| 136 | `fechafacturacompra` | timestamp(3) | YES |  |
| 137 | `fechafacturaprincipal` | timestamp(3) | YES |  |
| 138 | `load_date` | varchar | YES |  |

### spiga.spiga_fechaprevistacompra

**Columnas:** 45

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresa` | bigint | YES |  |
| 7 | `idterceros` | bigint | YES |  |
| 8 | `nombre` | varchar | YES |  |
| 9 | `apellido1` | varchar | YES |  |
| 10 | `apellido2` | varchar | YES |  |
| 11 | `nifcif` | varchar | YES |  |
| 12 | `nombrecalle` | varchar | YES |  |
| 13 | `numero` | varchar | YES |  |
| 14 | `bloque` | varchar | YES |  |
| 15 | `piso` | varchar | YES |  |
| 16 | `puerta` | varchar | YES |  |
| 17 | `idcodigospostales` | varchar | YES |  |
| 18 | `poblacion` | varchar | YES |  |
| 19 | `provincia` | varchar | YES |  |
| 20 | `complemento` | varchar | YES |  |
| 21 | `complemento2` | varchar | YES |  |
| 22 | `idpaises` | varchar | YES |  |
| 23 | `idcalletipos` | varchar | YES |  |
| 24 | `descripcioncalletipos` | varchar | YES |  |
| 25 | `telefono` | varchar | YES |  |
| 26 | `email` | varchar | YES |  |
| 27 | `fechaprevistacambio` | timestamp(3) | YES |  |
| 28 | `fechaentrada` | timestamp(3) | YES |  |
| 29 | `idempleados` | bigint | YES |  |
| 30 | `nombreempleado` | varchar | YES |  |
| 31 | `descripcionentradatipos` | varchar | YES |  |
| 32 | `nombremodelo` | varchar | YES |  |
| 33 | `fechaalta` | timestamp(3) | YES |  |
| 34 | `idsecciones` | bigint | YES |  |
| 35 | `descripcion` | varchar | YES |  |
| 36 | `nombregama` | varchar | YES |  |
| 37 | `nombrecentro` | varchar | YES |  |
| 38 | `descripcionseccion` | varchar | YES |  |
| 39 | `fechaultimaactividad` | timestamp(3) | YES |  |
| 40 | `idclientespotclasificaciones` | bigint | YES |  |
| 41 | `fechasalida` | timestamp(3) | YES |  |
| 42 | `idsalidatipos` | varchar | YES |  |
| 43 | `idintencionescompra` | varchar | YES |  |
| 44 | `descripcion_intencionescompra` | varchar | YES |  |
| 45 | `load_date` | varchar | YES |  |

### spiga.spiga_financiacionesventasvnvo

**Columnas:** 42

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `idofertapagos` | bigint | YES |  |
| 12 | `saldofavorcliente` | bigint | YES |  |
| 13 | `importefinanciado` | double | YES |  |
| 14 | `fechavencimiento` | timestamp(3) | YES |  |
| 15 | `fechainicio` | timestamp(3) | YES |  |
| 16 | `comisionfinanciera` | double | YES |  |
| 17 | `vin` | varchar | YES |  |
| 18 | `matricula` | varchar | YES |  |
| 19 | `comisionvehiculo` | varchar | YES |  |
| 20 | `idterceros` | bigint | YES |  |
| 21 | `nombrepropietario` | varchar | YES |  |
| 22 | `nifcifpropietario` | varchar | YES |  |
| 23 | `idtercerosfinanciera` | bigint | YES |  |
| 24 | `nombrefinanciera` | varchar | YES |  |
| 25 | `idempleados` | bigint | YES |  |
| 26 | `nombreempleado` | varchar | YES |  |
| 27 | `idtercerosagente` | bigint | YES |  |
| 28 | `nombreagente` | varchar | YES |  |
| 29 | `idmarcas` | bigint | YES |  |
| 30 | `nombremarca` | varchar | YES |  |
| 31 | `idgamas` | bigint | YES |  |
| 32 | `nombregama` | varchar | YES |  |
| 33 | `idempleadosgestor` | bigint | YES |  |
| 34 | `nombregestor` | varchar | YES |  |
| 35 | `fechaventa` | timestamp(3) | YES |  |
| 36 | `nombreempresa` | varchar | YES |  |
| 37 | `nombrecentro` | varchar | YES |  |
| 38 | `idmodulos` | varchar | YES |  |
| 39 | `estado` | varchar | YES |  |
| 40 | `descripcionsecciones` | varchar | YES |  |
| 41 | `fechaentregacliente` | timestamp(3) | YES |  |
| 42 | `load_date` | varchar | YES |  |

### spiga.spiga_habeasdata

**Columnas:** 14

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `pkterceros` | bigint | YES |  |
| 7 | `nombres` | varchar | YES |  |
| 8 | `fechaconsentimiento` | timestamp(3) | YES |  |
| 9 | `mesesvalidezconsentimiento` | bigint | YES |  |
| 10 | `descripcion` | varchar | YES |  |
| 11 | `mesesvalidez` | bigint | YES |  |
| 12 | `valorbool` | bigint | YES |  |
| 13 | `numdocumento` | varchar | YES |  |
| 14 | `load_date` | varchar | YES |  |

### spiga.spiga_informafacturacion

**Columnas:** 131

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `tipo` | varchar | YES |  |
| 7 | `idempresas` | bigint | YES |  |
| 8 | `idcentros` | bigint | YES |  |
| 9 | `a�oot` | varchar | YES |  |
| 10 | `serieot` | varchar | YES |  |
| 11 | `numot` | bigint | YES |  |
| 12 | `numtrabajo` | bigint | YES |  |
| 13 | `idempleadocierre` | bigint | YES |  |
| 14 | `fechaalta` | timestamp(3) | YES |  |
| 15 | `fechacierre` | timestamp(3) | YES |  |
| 16 | `idseriesgarantias` | varchar | YES |  |
| 17 | `numalbaran` | bigint | YES |  |
| 18 | `a�oalbaran` | varchar | YES |  |
| 19 | `numgarantiamarca` | varchar | YES |  |
| 20 | `horasfacturadas` | bigint | YES |  |
| 21 | `importemobruto` | double | YES |  |
| 22 | `descuentomo` | double | YES |  |
| 23 | `importesubbruto` | double | YES |  |
| 24 | `descuentosub` | double | YES |  |
| 25 | `importevarbruto` | double | YES |  |
| 26 | `descuentovar` | double | YES |  |
| 27 | `importepintbruto` | double | YES |  |
| 28 | `descuentopint` | double | YES |  |
| 29 | `importematerialbruto` | double | YES |  |
| 30 | `descuentomaterial` | double | YES |  |
| 31 | `importemoaceptada` | double | YES |  |
| 32 | `importesubaceptada` | double | YES |  |
| 33 | `importevaraceptada` | double | YES |  |
| 34 | `importepintaceptada` | double | YES |  |
| 35 | `importematerialaceptada` | double | YES |  |
| 36 | `idcargotipos` | varchar | YES |  |
| 37 | `idmanoobratipos` | bigint | YES |  |
| 38 | `iddepartamentocargointerno` | varchar | YES |  |
| 39 | `idsecciones` | bigint | YES |  |
| 40 | `idvehiculos` | bigint | YES |  |
| 41 | `matricula` | varchar | YES |  |
| 42 | `vin` | varchar | YES |  |
| 43 | `idmarcas` | bigint | YES |  |
| 44 | `idgamas` | bigint | YES |  |
| 45 | `fechadespacho` | timestamp(3) | YES |  |
| 46 | `nombremarcas` | varchar | YES |  |
| 47 | `nombregamas` | varchar | YES |  |
| 48 | `a�ofactura` | varchar | YES |  |
| 49 | `seriefactura` | varchar | YES |  |
| 50 | `numfactura` | varchar | YES |  |
| 51 | `idtercerofactura` | bigint | YES |  |
| 52 | `nombretercero` | varchar | YES |  |
| 53 | `idterceroaux` | bigint | YES |  |
| 54 | `nombreterceroaux` | varchar | YES |  |
| 55 | `idpagoformatipos` | varchar | YES |  |
| 56 | `idpagoformas` | varchar | YES |  |
| 57 | `descripcionpagoformas` | varchar | YES |  |
| 58 | `descripcionpagoformatipos` | varchar | YES |  |
| 59 | `fechafactura` | timestamp(3) | YES |  |
| 60 | `tipopago` | varchar | YES |  |
| 61 | `costesub` | double | YES |  |
| 62 | `costemo` | double | YES |  |
| 63 | `costemochapa` | double | YES |  |
| 64 | `costemopintura` | double | YES |  |
| 65 | `costemoresto` | varchar | YES |  |
| 66 | `costemat` | double | YES |  |
| 67 | `importetasasmat` | double | YES |  |
| 68 | `diasreparacion` | bigint | YES |  |
| 69 | `costepint` | double | YES |  |
| 70 | `importemochapa` | double | YES |  |
| 71 | `importemopintura` | double | YES |  |
| 72 | `importemoresto` | varchar | YES |  |
| 73 | `idtallerpagotipos` | varchar | YES |  |
| 74 | `descripciontallerpagotipos` | varchar | YES |  |
| 75 | `idempleados` | bigint | YES |  |
| 76 | `descripcionrecepciontipos` | varchar | YES |  |
| 77 | `kmts` | bigint | YES |  |
| 78 | `a�omodelo` | varchar | YES |  |
| 79 | `idterceropropietario` | bigint | YES |  |
| 80 | `descripciontrabajo` | varchar | YES |  |
| 81 | `diasabierto` | double | YES |  |
| 82 | `numeroautorizacion` | varchar | YES |  |
| 83 | `numsiniestro` | varchar | YES |  |
| 84 | `fechaentrega` | timestamp(3) | YES |  |
| 85 | `idtercerocargo` | bigint | YES |  |
| 86 | `nombretercerocargo` | varchar | YES |  |
| 87 | `idseccioncargos` | varchar | YES |  |
| 88 | `idimputaciontipos` | bigint | YES |  |
| 89 | `idseccioncargointerno` | bigint | YES |  |
| 90 | `idcentrosdestino` | bigint | YES |  |
| 91 | `trabajorepetido` | bigint | YES |  |
| 92 | `a�opresupuesto` | varchar | YES |  |
| 93 | `seriepresupuesto` | varchar | YES |  |
| 94 | `idpresupuesto` | bigint | YES |  |
| 95 | `descripcionseccioncargos` | varchar | YES |  |
| 96 | `idempleadosrec` | bigint | YES |  |
| 97 | `idempleadosretirada` | bigint | YES |  |
| 98 | `idempleadosresponsable` | bigint | YES |  |
| 99 | `a�opedidosservicios` | varchar | YES |  |
| 100 | `seriepedidosservicios` | varchar | YES |  |
| 101 | `idpedidosservicios` | bigint | YES |  |
| 102 | `idmarcastallercampa�asbastidoresafectados` | bigint | YES |  |
| 103 | `idcampa�as` | varchar | YES |  |
| 104 | `idcampa�avariante` | varchar | YES |  |
| 105 | `idubicaciones` | varchar | YES |  |
| 106 | `reclamadomo` | double | YES |  |
| 107 | `reclamadomat` | double | YES |  |
| 108 | `reclamadosub` | double | YES |  |
| 109 | `reclamadovar` | double | YES |  |
| 110 | `reclamadopint` | double | YES |  |
| 111 | `idcentrosdeferencia` | bigint | YES |  |
| 112 | `ida�ootdeferencia` | varchar | YES |  |
| 113 | `idseriesdeferencia` | varchar | YES |  |
| 114 | `idnumotdeferencia` | bigint | YES |  |
| 115 | `idnumtrabajodeferencia` | bigint | YES |  |
| 116 | `idserviciotipos` | bigint | YES |  |
| 117 | `idgradosaveria` | bigint | YES |  |
| 118 | `idgradoaveriaordentrabajo` | bigint | YES |  |
| 119 | `idtrabajotipos` | varchar | YES |  |
| 120 | `idtrabajotiposmarca` | varchar | YES |  |
| 121 | `sureferencia` | varchar | YES |  |
| 122 | `horasuso` | bigint | YES |  |
| 123 | `fechaaltaot` | timestamp(3) | YES |  |
| 124 | `numfacturaexterna` | varchar | YES |  |
| 125 | `observaciones` | varchar | YES |  |
| 126 | `idconse` | varchar | YES |  |
| 127 | `descripciondepartamentoimputaciontipos` | varchar | YES |  |
| 128 | `descripcionimputaciontipos` | varchar | YES |  |
| 129 | `descripcionseccionimputaciontipos` | varchar | YES |  |
| 130 | `nombrecentroimputaciontipos` | varchar | YES |  |
| 131 | `load_date` | varchar | YES |  |

### spiga.spiga_inventariovn

**Columnas:** 71

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `comprasnumdet` | bigint | YES |  |
| 12 | `vin` | varchar | YES |  |
| 13 | `matricula` | varchar | YES |  |
| 14 | `comision` | varchar | YES |  |
| 15 | `idsecciones` | bigint | YES |  |
| 16 | `fkcompratipos` | varchar | YES |  |
| 17 | `nombreempresa` | varchar | YES |  |
| 18 | `nombrecentro` | varchar | YES |  |
| 19 | `descripcionseccion` | varchar | YES |  |
| 20 | `descripciontipocompra` | varchar | YES |  |
| 21 | `descripciontipocombustible` | varchar | YES |  |
| 22 | `idmarcas` | bigint | YES |  |
| 23 | `idgamas` | bigint | YES |  |
| 24 | `codmodelo` | varchar | YES |  |
| 25 | `extmodelo` | varchar | YES |  |
| 26 | `a�omodelo` | varchar | YES |  |
| 27 | `nombremarca` | varchar | YES |  |
| 28 | `nombregama` | varchar | YES |  |
| 29 | `nombremodelo` | varchar | YES |  |
| 30 | `a�ofactura` | varchar | YES |  |
| 31 | `seriefactura` | varchar | YES |  |
| 32 | `numfactura` | varchar | YES |  |
| 33 | `fechafactura` | timestamp(3) | YES |  |
| 34 | `idcompraestados` | varchar | YES |  |
| 35 | `a�oalbaran` | varchar | YES |  |
| 36 | `seriealbaran` | varchar | YES |  |
| 37 | `numalbaran` | varchar | YES |  |
| 38 | `fechaalbaran` | timestamp(3) | YES |  |
| 39 | `descripcionestadocompra` | varchar | YES |  |
| 40 | `color` | varchar | YES |  |
| 41 | `tapiceria` | varchar | YES |  |
| 42 | `ultimaubicacionvn` | varchar | YES |  |
| 43 | `ubicacionvnfechainventario` | varchar | YES |  |
| 44 | `baseimponiblecompra` | double | YES |  |
| 45 | `gastosaumentanstock` | double | YES |  |
| 46 | `gastosnoaumentanstock` | double | YES |  |
| 47 | `gastospendientesaumentanstock` | double | YES |  |
| 48 | `gastospendientesnoaumentanstock` | double | YES |  |
| 49 | `totalgastoscontravalor` | double | YES |  |
| 50 | `baseimponiblecompracontravalor` | double | YES |  |
| 51 | `descripcioncompraestados` | varchar | YES |  |
| 52 | `dtoimporte` | double | YES |  |
| 53 | `importereclamado` | double | YES |  |
| 54 | `pedidossinasignaraumentastock` | double | YES |  |
| 55 | `usodestino` | varchar | YES |  |
| 56 | `idversiones` | varchar | YES |  |
| 57 | `idincidenciatipos` | varchar | YES |  |
| 58 | `idtercerosactividadincidenciatipos` | bigint | YES |  |
| 59 | `idactividadincidenciatipos` | bigint | YES |  |
| 60 | `idactividadesdetincidenciatipos` | bigint | YES |  |
| 61 | `incidenciatiposdescripcion` | varchar | YES |  |
| 62 | `descripcionversion` | varchar | YES |  |
| 63 | `idcategoriagamatipos` | varchar | YES |  |
| 64 | `numeromotor` | varchar | YES |  |
| 65 | `numhomologacion` | varchar | YES |  |
| 66 | `fecha` | timestamp(3) | YES |  |
| 67 | `numdeclaracion` | varchar | YES |  |
| 68 | `fechalevante` | timestamp(3) | YES |  |
| 69 | `numlevante` | varchar | YES |  |
| 70 | `observaciones_compra` | varchar | YES |  |
| 71 | `load_date` | varchar | YES |  |

### spiga.spiga_inventariovo

**Columnas:** 59

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `comprasnumdet` | bigint | YES |  |
| 12 | `fechadepreciar` | timestamp(3) | YES |  |
| 13 | `vin` | varchar | YES |  |
| 14 | `matricula` | varchar | YES |  |
| 15 | `idsecciones` | bigint | YES |  |
| 16 | `idcompratipos` | varchar | YES |  |
| 17 | `idregistrotipos` | varchar | YES |  |
| 18 | `fechaasiento` | timestamp(3) | YES |  |
| 19 | `idcomprainternatipos` | varchar | YES |  |
| 20 | `descripcioncomprainternatipo` | varchar | YES |  |
| 21 | `nombreempresa` | varchar | YES |  |
| 22 | `nombrecentro` | varchar | YES |  |
| 23 | `descripcionseccion` | varchar | YES |  |
| 24 | `descripciontipocompra` | varchar | YES |  |
| 25 | `descripciontipocombustible` | varchar | YES |  |
| 26 | `tipocomprainmovilizado` | bigint | YES |  |
| 27 | `idmarcas` | bigint | YES |  |
| 28 | `idgamas` | bigint | YES |  |
| 29 | `codmodelo` | varchar | YES |  |
| 30 | `extmodelo` | varchar | YES |  |
| 31 | `a�omodelo` | varchar | YES |  |
| 32 | `nombremarca` | varchar | YES |  |
| 33 | `nombregama` | varchar | YES |  |
| 34 | `idcompraestados` | varchar | YES |  |
| 35 | `nombremodelo` | varchar | YES |  |
| 36 | `a�ofactura` | varchar | YES |  |
| 37 | `seriefactura` | varchar | YES |  |
| 38 | `numfactura` | varchar | YES |  |
| 39 | `fechafactura` | timestamp(3) | YES |  |
| 40 | `descripcioncompraestados` | varchar | YES |  |
| 41 | `ultimaubicacionvn` | varchar | YES |  |
| 42 | `ubicacionvnfechainventario` | varchar | YES |  |
| 43 | `color` | varchar | YES |  |
| 44 | `tapiceria` | varchar | YES |  |
| 45 | `baseimponiblecompra` | double | YES |  |
| 46 | `depreciacioncompra` | double | YES |  |
| 47 | `compra576` | double | YES |  |
| 48 | `exentos` | double | YES |  |
| 49 | `gastosaumentanstock` | double | YES |  |
| 50 | `gastosnoaumentanstock` | double | YES |  |
| 51 | `gastospendientesaumentanstock` | double | YES |  |
| 52 | `gastospendientesnoaumentanstock` | double | YES |  |
| 53 | `totalgastoscontravalor` | double | YES |  |
| 54 | `importecompracontravalor` | double | YES |  |
| 55 | `pedidossinasignaraumentastock` | double | YES |  |
| 56 | `usodestino` | varchar | YES |  |
| 57 | `importetotaldepreciado` | double | YES |  |
| 58 | `observaciones_compra` | varchar | YES |  |
| 59 | `load_date` | varchar | YES |  |

### spiga.spiga_ofertasdefinanciacionfechamod

**Columnas:** 52

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `ida�oofertasfinanciacion` | varchar | YES |  |
| 8 | `idseriesofertasfinanciacion` | varchar | YES |  |
| 9 | `idnumofertasfinanciacion` | bigint | YES |  |
| 10 | `idcentros` | bigint | YES |  |
| 11 | `nombreempresa` | varchar | YES |  |
| 12 | `nombrecentro` | varchar | YES |  |
| 13 | `nombremarca` | varchar | YES |  |
| 14 | `nombregama` | varchar | YES |  |
| 15 | `codmodelo` | varchar | YES |  |
| 16 | `nombremodelo` | varchar | YES |  |
| 17 | `idterceros` | bigint | YES |  |
| 18 | `nombretercero` | varchar | YES |  |
| 19 | `apellido1tercero` | varchar | YES |  |
| 20 | `apellido2tercero` | varchar | YES |  |
| 21 | `idofertasfinanciacionproductotiposdescripcion` | varchar | YES |  |
| 22 | `idofertasfinanciacionestadosdescripcion` | varchar | YES |  |
| 23 | `fechavalidez` | timestamp(3) | YES |  |
| 24 | `fechainiciofinanciacion` | timestamp(3) | YES |  |
| 25 | `fechafinfinanciacion` | timestamp(3) | YES |  |
| 26 | `importefinanciar` | double | YES |  |
| 27 | `cuotamensual` | double | YES |  |
| 28 | `meses` | bigint | YES |  |
| 29 | `porcsobreimportetotal` | double | YES |  |
| 30 | `capitalpreconcedido` | double | YES |  |
| 31 | `porcintereses` | double | YES |  |
| 32 | `importecomisionapertura` | double | YES |  |
| 33 | `porccomisionapertura` | double | YES |  |
| 34 | `obligaaval` | bigint | YES |  |
| 35 | `aval` | varchar | YES |  |
| 36 | `importecomisionobtencionfinanciacion` | double | YES |  |
| 37 | `porccomisionobtencionfinanciacion` | double | YES |  |
| 38 | `idtercerosfinanciera` | bigint | YES |  |
| 39 | `nombretercerofinanciera` | varchar | YES |  |
| 40 | `apellido1tercerofinanciera` | varchar | YES |  |
| 41 | `apellido2tercerofinanciera` | varchar | YES |  |
| 42 | `idofertasfinanciacionproductotipos` | bigint | YES |  |
| 43 | `idofertasfinanciacionestados` | bigint | YES |  |
| 44 | `fechaalta` | timestamp(3) | YES |  |
| 45 | `idofertasfinanciacionfinanciaciones` | bigint | YES |  |
| 46 | `idempleados` | bigint | YES |  |
| 47 | `nombreempleado` | varchar | YES |  |
| 48 | `apellido1empleado` | varchar | YES |  |
| 49 | `apellido2empleado` | varchar | YES |  |
| 50 | `importefranquicia` | double | YES |  |
| 51 | `fechamod` | timestamp(3) | YES |  |
| 52 | `load_date` | varchar | YES |  |

### spiga.spiga_remisionesderepuestos_b656ba9ac85043876847359b51a1fe1b

**Columnas:** 26

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `empresacentrosecciones` | varchar | YES |  |
| 8 | `idcentros` | bigint | YES |  |
| 9 | `centro` | varchar | YES |  |
| 10 | `idsecciones` | bigint | YES |  |
| 11 | `seccion` | varchar | YES |  |
| 12 | `fechaalta` | timestamp(3) | YES |  |
| 13 | `idmovimientotipos` | varchar | YES |  |
| 14 | `movimientotipos` | varchar | YES |  |
| 15 | `prefijo` | varchar | YES |  |
| 16 | `numero` | varchar | YES |  |
| 17 | `a�o` | varchar | YES |  |
| 18 | `a�oot` | varchar | YES |  |
| 19 | `serieot` | varchar | YES |  |
| 20 | `numot` | bigint | YES |  |
| 21 | `idpedidotipoventas` | bigint | YES |  |
| 22 | `a�opedido` | varchar | YES |  |
| 23 | `seriepedido` | varchar | YES |  |
| 24 | `pedido` | bigint | YES |  |
| 25 | `tipocargo` | varchar | YES |  |
| 26 | `load_date` | varchar | YES |  |

### spiga.spiga_stockrepuestos_6e2c485f758244e77cdb9bb9e2c6d62a

**Columnas:** 61

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `idsecciones` | bigint | YES |  |
| 9 | `idmr` | varchar | YES |  |
| 10 | `idreferencias` | varchar | YES |  |
| 11 | `idtarifas` | bigint | YES |  |
| 12 | `stockmax` | double | YES |  |
| 13 | `preciomedio` | double | YES |  |
| 14 | `clasificacionabc` | varchar | YES |  |
| 15 | `stock` | double | YES |  |
| 16 | `numubicaciones` | bigint | YES |  |
| 17 | `ventasmesactualsalidas` | bigint | YES |  |
| 18 | `undpterecibir` | double | YES |  |
| 19 | `idubicaciones` | varchar | YES |  |
| 20 | `ventasmesactual` | double | YES |  |
| 21 | `ventasmes1` | double | YES |  |
| 22 | `ventasmes2` | double | YES |  |
| 23 | `ventasmes3` | double | YES |  |
| 24 | `ventasmes4` | double | YES |  |
| 25 | `ventasmes5` | double | YES |  |
| 26 | `ventasmes6` | double | YES |  |
| 27 | `ventasmes7` | double | YES |  |
| 28 | `ventasmes8` | double | YES |  |
| 29 | `ventasmes9` | double | YES |  |
| 30 | `ventasmes10` | double | YES |  |
| 31 | `ventasmes11` | double | YES |  |
| 32 | `ventasmes12` | double | YES |  |
| 33 | `descripcion` | varchar | YES |  |
| 34 | `precioventa` | double | YES |  |
| 35 | `observaciones` | varchar | YES |  |
| 36 | `idclasificacion1` | varchar | YES |  |
| 37 | `idclasificacion2` | varchar | YES |  |
| 38 | `idclasificacion3` | varchar | YES |  |
| 39 | `idclasificacion4` | varchar | YES |  |
| 40 | `idclasificacion5` | varchar | YES |  |
| 41 | `idclasificacion6` | varchar | YES |  |
| 42 | `iddescuentos` | varchar | YES |  |
| 43 | `fechaultimaventa` | timestamp(3) | YES |  |
| 44 | `fechaultimacompra` | timestamp(3) | YES |  |
| 45 | `fechaultimaregularizacion` | timestamp(3) | YES |  |
| 46 | `fechatraspasotre` | timestamp(3) | YES |  |
| 47 | `fechatraspasotrs` | timestamp(3) | YES |  |
| 48 | `denominacionclasificacion1` | varchar | YES |  |
| 49 | `denominacionclasificacion2` | varchar | YES |  |
| 50 | `denominacionclasificacion3` | varchar | YES |  |
| 51 | `denominacionclasificacion4` | varchar | YES |  |
| 52 | `denominacionclasificacion5` | varchar | YES |  |
| 53 | `denominacionclasificacion6` | varchar | YES |  |
| 54 | `fechaalta` | timestamp(3) | YES |  |
| 55 | `fechabaja` | timestamp(3) | YES |  |
| 56 | `stockmin` | double | YES |  |
| 57 | `undpteentregar` | double | YES |  |
| 58 | `undreservadaspteentregar` | double | YES |  |
| 59 | `undenvasecompra` | double | YES |  |
| 60 | `undenvaseventa` | double | YES |  |
| 61 | `load_date` | varchar | YES |  |

### spiga.spiga_terceroformacionniveles

**Columnas:** 9

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `pkterceroformacionniveles_iden` | bigint | YES |  |
| 4 | `descripcion` | varchar | YES |  |
| 5 | `usermod` | bigint | YES |  |
| 6 | `hostmod` | varchar | YES |  |
| 7 | `versionfila` | bigint | YES |  |
| 8 | `fechamod` | timestamp(3) | YES |  |
| 9 | `load_date` | varchar | YES |  |

### spiga.spiga_terceros

**Columnas:** 71

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `pkterceros` | bigint | YES |  |
| 7 | `fkpaises` | varchar | YES |  |
| 8 | `fkterceroclases` | bigint | YES |  |
| 9 | `fktratamientos` | bigint | YES |  |
| 10 | `nifcif` | varchar | YES |  |
| 11 | `nombre` | varchar | YES |  |
| 12 | `apellido1` | varchar | YES |  |
| 13 | `apellido2` | varchar | YES |  |
| 14 | `nombrecomercial` | varchar | YES |  |
| 15 | `empresatrabajo` | varchar | YES |  |
| 16 | `fkprofesiones` | bigint | YES |  |
| 17 | `fktercerocargos` | bigint | YES |  |
| 18 | `fkterceroformacionniveles` | bigint | YES |  |
| 19 | `fechanacimiento` | timestamp(3) | YES |  |
| 20 | `fechasanto` | varchar | YES |  |
| 21 | `fechacarnet` | timestamp(3) | YES |  |
| 22 | `numerohijos` | bigint | YES |  |
| 23 | `facturaracliente` | bigint | YES |  |
| 24 | `numeroautorizacion` | bigint | YES |  |
| 25 | `numerosiniestro` | bigint | YES |  |
| 26 | `fechaalta` | timestamp(3) | YES |  |
| 27 | `fechabaja` | timestamp(3) | YES |  |
| 28 | `usermod` | bigint | YES |  |
| 29 | `hostmod` | varchar | YES |  |
| 30 | `versionfila` | bigint | YES |  |
| 31 | `fkdocumentaciontipos` | bigint | YES |  |
| 32 | `fkestadociviltipos` | varchar | YES |  |
| 33 | `fechamod` | timestamp(3) | YES |  |
| 34 | `sexo` | varchar | YES |  |
| 35 | `fknaturalezajuridicatipos` | varchar | YES |  |
| 36 | `numeroempleados` | bigint | YES |  |
| 37 | `a�oconstitucion` | varchar | YES |  |
| 38 | `cifradenegocio` | bigint | YES |  |
| 39 | `fkactividadtipos` | varchar | YES |  |
| 40 | `solvencia` | bigint | YES |  |
| 41 | `codigosociedad` | varchar | YES |  |
| 42 | `robinson` | bigint | YES |  |
| 43 | `numlicenciaconducir` | varchar | YES |  |
| 44 | `billeteidentidad` | varchar | YES |  |
| 45 | `tipocontribuyente` | varchar | YES |  |
| 46 | `retenerdesdecero` | bigint | YES |  |
| 47 | `agenteretenedor` | bigint | YES |  |
| 48 | `robinsonant` | bigint | YES |  |
| 49 | `fechamodrobinson` | timestamp(3) | YES |  |
| 50 | `fkcausabajatercero` | bigint | YES |  |
| 51 | `notieneemail` | bigint | YES |  |
| 52 | `centrocoste` | varchar | YES |  |
| 53 | `fechacarnetcaducidad` | timestamp(3) | YES |  |
| 54 | `norealizaasientodiferenciacambial` | bigint | YES |  |
| 55 | `norealizaasientoconversion` | bigint | YES |  |
| 56 | `fknivelesriesgo` | bigint | YES |  |
| 57 | `fechatipocontribuyente` | timestamp(3) | YES |  |
| 58 | `resolucion` | varchar | YES |  |
| 59 | `cuentabanconacion` | varchar | YES |  |
| 60 | `admitesepab2b` | bigint | YES |  |
| 61 | `requieresureferenciare` | bigint | YES |  |
| 62 | `nifcif_fechaexpedicion` | timestamp(3) | YES |  |
| 63 | `nifcif_lugarexpedicion` | varchar | YES |  |
| 64 | `nifcif_fechacaducidad` | timestamp(3) | YES |  |
| 65 | `licenciaconducir_lugarexpedicion` | varchar | YES |  |
| 66 | `fkdeudortipos` | varchar | YES |  |
| 67 | `fkpaises_documentaciontipos` | varchar | YES |  |
| 68 | `fcnegociado` | bigint | YES |  |
| 69 | `web` | varchar | YES |  |
| 70 | `envioficherosfecomprimidos` | bigint | YES |  |
| 71 | `load_date` | varchar | YES |  |

### spiga.spiga_terceroscargos

**Columnas:** 10

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `pktercerocargos_iden` | bigint | YES |  |
| 4 | `descripcion` | varchar | YES |  |
| 5 | `fechabaja` | timestamp(3) | YES |  |
| 6 | `usermod` | bigint | YES |  |
| 7 | `hostmod` | varchar | YES |  |
| 8 | `versionfila` | bigint | YES |  |
| 9 | `fechamod` | timestamp(3) | YES |  |
| 10 | `load_date` | varchar | YES |  |

### spiga.spiga_terceroscorreos

**Columnas:** 19

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `pkfkterceros` | bigint | YES |  |
| 7 | `pkterceroemails_iden` | bigint | YES |  |
| 8 | `fkemailtipos` | bigint | YES |  |
| 9 | `email` | varchar | YES |  |
| 10 | `fktercerodirecciones` | bigint | YES |  |
| 11 | `fechabaja` | timestamp(3) | YES |  |
| 12 | `usermod` | bigint | YES |  |
| 13 | `hostmod` | varchar | YES |  |
| 14 | `versionfila` | bigint | YES |  |
| 15 | `direccionpadre` | bigint | YES |  |
| 16 | `principal` | bigint | YES |  |
| 17 | `fechamod` | timestamp(3) | YES |  |
| 18 | `fkterceros_direcciones` | bigint | YES |  |
| 19 | `load_date` | varchar | YES |  |

### spiga.spiga_tercerosdirecciones

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `pkfkterceros` | bigint | YES |  |
| 7 | `pktercerodirecciones_iden` | bigint | YES |  |
| 8 | `fkdirecciontipos` | bigint | YES |  |
| 9 | `fkcalletipos` | varchar | YES |  |
| 10 | `nombrecalle` | varchar | YES |  |
| 11 | `numero` | varchar | YES |  |
| 12 | `bloque` | varchar | YES |  |
| 13 | `piso` | varchar | YES |  |
| 14 | `puerta` | varchar | YES |  |
| 15 | `complemento` | varchar | YES |  |
| 16 | `fkpaises` | varchar | YES |  |
| 17 | `fkcodigospostales` | varchar | YES |  |
| 18 | `poblacion` | varchar | YES |  |
| 19 | `provincia` | varchar | YES |  |
| 20 | `fechabaja` | timestamp(3) | YES |  |
| 21 | `usermod` | bigint | YES |  |
| 22 | `hostmod` | varchar | YES |  |
| 23 | `versionfila` | bigint | YES |  |
| 24 | `principal` | bigint | YES |  |
| 25 | `fkestados` | varchar | YES |  |
| 26 | `fkprovincias` | varchar | YES |  |
| 27 | `complemento2` | varchar | YES |  |
| 28 | `fechamod` | timestamp(3) | YES |  |
| 29 | `fkpoblaciones` | bigint | YES |  |
| 30 | `load_date` | varchar | YES |  |

### spiga.spiga_tercerostelefonos

**Columnas:** 23

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `pkfkterceros` | bigint | YES |  |
| 7 | `pktercerotelefonos_iden` | bigint | YES |  |
| 8 | `fktelefonotipos` | bigint | YES |  |
| 9 | `codigotelefonico` | varchar | YES |  |
| 10 | `numero` | varchar | YES |  |
| 11 | `extension` | varchar | YES |  |
| 12 | `fktercerodirecciones` | bigint | YES |  |
| 13 | `direccionpadre` | bigint | YES |  |
| 14 | `horario` | varchar | YES |  |
| 15 | `fechabaja` | timestamp(3) | YES |  |
| 16 | `usermod` | bigint | YES |  |
| 17 | `hostmod` | varchar | YES |  |
| 18 | `versionfila` | bigint | YES |  |
| 19 | `principal` | bigint | YES |  |
| 20 | `fechamod` | timestamp(3) | YES |  |
| 21 | `fkterceros_direcciones` | bigint | YES |  |
| 22 | `fkpaises` | varchar | YES |  |
| 23 | `load_date` | varchar | YES |  |

### spiga.spiga_tiempostallerpicajesots

**Columnas:** 32

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `idempleados` | bigint | YES |  |
| 9 | `fechainicio` | timestamp(3) | YES |  |
| 10 | `fechafin` | timestamp(3) | YES |  |
| 11 | `idpicajetrabajotipos` | varchar | YES |  |
| 12 | `matricula` | varchar | YES |  |
| 13 | `serieot` | varchar | YES |  |
| 14 | `numot` | bigint | YES |  |
| 15 | `a�oot` | varchar | YES |  |
| 16 | `numtrabajo` | bigint | YES |  |
| 17 | `tiempoempleado` | double | YES |  |
| 18 | `fechainicioaux` | timestamp(3) | YES |  |
| 19 | `fechafinaux` | timestamp(3) | YES |  |
| 20 | `tiempoaux` | double | YES |  |
| 21 | `nombreempleado` | varchar | YES |  |
| 22 | `descripcionpicajetrabajotipos` | varchar | YES |  |
| 23 | `idmanoobratipos` | bigint | YES |  |
| 24 | `descripcionmanoobratipos` | varchar | YES |  |
| 25 | `recuperable` | bigint | YES |  |
| 26 | `afectataller` | bigint | YES |  |
| 27 | `idclasificacionincidenciatipos` | bigint | YES |  |
| 28 | `idrevisionpicajetipos` | varchar | YES |  |
| 29 | `useraux` | bigint | YES |  |
| 30 | `idsecciones` | bigint | YES |  |
| 31 | `fechabaja` | timestamp(3) | YES |  |
| 32 | `load_date` | varchar | YES |  |

### spiga.spiga_tipoclasificacionesvehiculos

**Columnas:** 68

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `pkfkmarcas` | bigint | YES |  |
| 4 | `pkfkgamas` | bigint | YES |  |
| 5 | `pkcodmodelo` | varchar | YES |  |
| 6 | `pkanomodelo` | varchar | YES |  |
| 7 | `fkclasificaciontipos` | varchar | YES |  |
| 8 | `nombreclasificacion` | varchar | YES |  |
| 9 | `cantidadpasajeros` | varchar | YES |  |
| 10 | `capacidaddecarga` | varchar | YES |  |
| 11 | `pkextmodelo` | varchar | YES |  |
| 12 | `nombre` | varchar | YES |  |
| 13 | `activo` | bigint | YES |  |
| 14 | `fkcombustibletipos` | varchar | YES |  |
| 15 | `fkcarroceriatipos` | varchar | YES |  |
| 16 | `fkmarcatallermodelos` | varchar | YES |  |
| 17 | `fktracciontipos` | varchar | YES |  |
| 18 | `fkcambiotipos` | varchar | YES |  |
| 19 | `potenciafiscal` | varchar | YES |  |
| 20 | `potenciareal` | varchar | YES |  |
| 21 | `cilindrada` | double | YES |  |
| 22 | `aceleracion` | varchar | YES |  |
| 23 | `velocidadmax` | double | YES |  |
| 24 | `numerocilindros` | bigint | YES |  |
| 25 | `consumointerurbano` | double | YES |  |
| 26 | `consumourbano` | double | YES |  |
| 27 | `consumomedio` | double | YES |  |
| 28 | `emisionesco2medio` | double | YES |  |
| 29 | `importado` | bigint | YES |  |
| 30 | `visibleweb` | bigint | YES |  |
| 31 | `periodoinspeccion` | bigint | YES |  |
| 32 | `kilometrosinspeccion` | varchar | YES |  |
| 33 | `fechabaja` | timestamp(3) | YES |  |
| 34 | `codexternomodelo` | varchar | YES |  |
| 35 | `potenciarealkw` | varchar | YES |  |
| 36 | `propiopeso` | varchar | YES |  |
| 37 | `cargautil` | varchar | YES |  |
| 38 | `numeropuertas` | varchar | YES |  |
| 39 | `numeroplazas` | varchar | YES |  |
| 40 | `fkcajavelocidadtipos` | varchar | YES |  |
| 41 | `neumaticos` | varchar | YES |  |
| 42 | `pma` | varchar | YES |  |
| 43 | `fechamod` | timestamp(3) | YES |  |
| 44 | `longitudexterior` | bigint | YES |  |
| 45 | `anchoexterior` | bigint | YES |  |
| 46 | `altoexterior` | bigint | YES |  |
| 47 | `disposicioncilindros` | varchar | YES |  |
| 48 | `volantealaizquierda` | bigint | YES |  |
| 49 | `fkmonedas` | bigint | YES |  |
| 50 | `factorcambiomoneda` | double | YES |  |
| 51 | `numeroejes` | bigint | YES |  |
| 52 | `fkcategoriagamatipos` | varchar | YES |  |
| 53 | `detalleenfactura` | varchar | YES |  |
| 54 | `porcdtomaxvendedores` | double | YES |  |
| 55 | `kilometrosgarantia` | bigint | YES |  |
| 56 | `numeroruedas` | bigint | YES |  |
| 57 | `numerovelocidades` | bigint | YES |  |
| 58 | `codigohomologacion` | varchar | YES |  |
| 59 | `numeroasientos` | varchar | YES |  |
| 60 | `requierecertificacion` | bigint | YES |  |
| 61 | `horasusoinspeccion` | varchar | YES |  |
| 62 | `potenciapto` | varchar | YES |  |
| 63 | `neumaticosdelanteros` | varchar | YES |  |
| 64 | `neumaticostraseros` | varchar | YES |  |
| 65 | `numcertificadopruebadinamica` | varchar | YES |  |
| 66 | `porcdtomaxjefesventas` | double | YES |  |
| 67 | `fkpaises` | varchar | YES |  |
| 68 | `load_date` | varchar | YES |  |

### spiga.spiga_trasladosderepuestospendientes

**Columnas:** 29

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas_salida` | bigint | YES |  |
| 7 | `idcentros_salida` | bigint | YES |  |
| 8 | `a�otraspaso_salida` | varchar | YES |  |
| 9 | `serietraspaso_salida` | varchar | YES |  |
| 10 | `numtraspaso_salida` | bigint | YES |  |
| 11 | `numdettraspaso_salida` | bigint | YES |  |
| 12 | `idsecciones_salida` | bigint | YES |  |
| 13 | `idempresas_entrada` | bigint | YES |  |
| 14 | `idcentros_entrada` | bigint | YES |  |
| 15 | `a�otraspaso_entrada` | varchar | YES |  |
| 16 | `serietraspaso_entrada` | varchar | YES |  |
| 17 | `numtraspaso_entrada` | bigint | YES |  |
| 18 | `numdettraspaso_entrada` | bigint | YES |  |
| 19 | `idsecciones_entrada` | bigint | YES |  |
| 20 | `idmovimientotipos` | varchar | YES |  |
| 21 | `mr` | varchar | YES |  |
| 22 | `referencia` | varchar | YES |  |
| 23 | `valorbruto` | double | YES |  |
| 24 | `unidades` | double | YES |  |
| 25 | `valorneto` | double | YES |  |
| 26 | `valormediomovimiento` | double | YES |  |
| 27 | `fechaaltasalida` | timestamp(3) | YES |  |
| 28 | `fechaaltaentrada` | timestamp(3) | YES |  |
| 29 | `load_date` | varchar | YES |  |

### spiga.spiga_vehiculos

**Columnas:** 60

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `fechadeactualizacion` | timestamp(3) | YES |  |
| 7 | `placa` | varchar | YES |  |
| 8 | `vin` | varchar | YES |  |
| 9 | `numdocumentopropietario` | varchar | YES |  |
| 10 | `numdocumentoconductor` | varchar | YES |  |
| 11 | `numdocumentoleasingrenting` | varchar | YES |  |
| 12 | `numdocumentoarrendador` | varchar | YES |  |
| 13 | `codigomarca` | bigint | YES |  |
| 14 | `nombremarca` | varchar | YES |  |
| 15 | `codigogama` | bigint | YES |  |
| 16 | `nombregama` | varchar | YES |  |
| 17 | `codmodelo` | varchar | YES |  |
| 18 | `nombremodelo` | varchar | YES |  |
| 19 | `extmodelo` | varchar | YES |  |
| 20 | `a�omodelo` | varchar | YES |  |
| 21 | `version` | varchar | YES |  |
| 22 | `codmodeloexterno` | varchar | YES |  |
| 23 | `potencia` | varchar | YES |  |
| 24 | `torque` | varchar | YES |  |
| 25 | `cilindrada` | double | YES |  |
| 26 | `combustible` | varchar | YES |  |
| 27 | `carroceria` | varchar | YES |  |
| 28 | `modelotaller` | varchar | YES |  |
| 29 | `color` | varchar | YES |  |
| 30 | `tapizado` | varchar | YES |  |
| 31 | `numeromotor` | varchar | YES |  |
| 32 | `codigofabricacion` | varchar | YES |  |
| 33 | `opr` | varchar | YES |  |
| 34 | `modelopv` | varchar | YES |  |
| 35 | `numregistroimportacion` | varchar | YES |  |
| 36 | `numeroprefijo` | varchar | YES |  |
| 37 | `sitioplaca` | varchar | YES |  |
| 38 | `servicio` | varchar | YES |  |
| 39 | `paisorigen` | varchar | YES |  |
| 40 | `fechafingarantiamecanica` | timestamp(3) | YES |  |
| 41 | `fechafingarantialatoneria` | timestamp(3) | YES |  |
| 42 | `fechafingarantiapintura` | timestamp(3) | YES |  |
| 43 | `fechafingarantiamotor` | timestamp(3) | YES |  |
| 44 | `kilometrosfingarantia` | bigint | YES |  |
| 45 | `fechaultimainspeccion` | timestamp(3) | YES |  |
| 46 | `fechaproximainspeccion` | timestamp(3) | YES |  |
| 47 | `kilometrosinspeccion` | varchar | YES |  |
| 48 | `kmsactuales` | bigint | YES |  |
| 49 | `tiposeguro` | varchar | YES |  |
| 50 | `ciaseguros` | varchar | YES |  |
| 51 | `fechaalta` | timestamp(3) | YES |  |
| 52 | `fechavencimiento` | timestamp(3) | YES |  |
| 53 | `valor` | double | YES |  |
| 54 | `deducible` | double | YES |  |
| 55 | `importecomisionventa` | double | YES |  |
| 56 | `numeropoliza` | varchar | YES |  |
| 57 | `tomador` | varchar | YES |  |
| 58 | `gestornegocio` | varchar | YES |  |
| 59 | `idvehiculos` | bigint | YES |  |
| 60 | `load_date` | varchar | YES |  |

### spiga.spiga_vehiculosentregados

**Columnas:** 34

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `a�o` | bigint | YES |  |
| 8 | `mes` | bigint | YES |  |
| 9 | `codigoempresa` | bigint | YES |  |
| 10 | `empresa` | varchar | YES |  |
| 11 | `codigocentro` | bigint | YES |  |
| 12 | `centro` | varchar | YES |  |
| 13 | `codigoseccion` | bigint | YES |  |
| 14 | `seccion` | varchar | YES |  |
| 15 | `codigomarca` | bigint | YES |  |
| 16 | `marca` | varchar | YES |  |
| 17 | `codigogama` | bigint | YES |  |
| 18 | `gama` | varchar | YES |  |
| 19 | `codigomodelo` | varchar | YES |  |
| 20 | `a�omodelo` | varchar | YES |  |
| 21 | `modelo` | varchar | YES |  |
| 22 | `cedulavendedor` | varchar | YES |  |
| 23 | `nombrevendedor` | varchar | YES |  |
| 24 | `nit` | varchar | YES |  |
| 25 | `nombretercero` | varchar | YES |  |
| 26 | `cantidad` | bigint | YES |  |
| 27 | `valor` | double | YES |  |
| 28 | `tipo` | varchar | YES |  |
| 29 | `fechaentregacliente` | timestamp(3) | YES |  |
| 30 | `fechamod` | timestamp(3) | YES |  |
| 31 | `vin` | varchar | YES |  |
| 32 | `fechafactura` | timestamp(3) | YES |  |
| 33 | `fkterceros_alquilador` | varchar | YES |  |
| 34 | `load_date` | varchar | YES |  |

### spiga.spiga_vehiculosseguros

**Columnas:** 87

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idvehiculos` | bigint | YES |  |
| 7 | `idvehiculoseguros` | bigint | YES |  |
| 8 | `idsegurotipos` | varchar | YES |  |
| 9 | `descripcionsegurotipos` | varchar | YES |  |
| 10 | `fechaalta` | timestamp(3) | YES |  |
| 11 | `idterceros` | bigint | YES |  |
| 12 | `fechavencimiento` | timestamp(3) | YES |  |
| 13 | `importe` | double | YES |  |
| 14 | `importefranquicia` | double | YES |  |
| 15 | `fechabaja` | timestamp(3) | YES |  |
| 16 | `idempresasvo` | bigint | YES |  |
| 17 | `idcentrosvo` | bigint | YES |  |
| 18 | `a�oexpedientevo` | varchar | YES |  |
| 19 | `serieexpedientevo` | varchar | YES |  |
| 20 | `numexpedientevo` | bigint | YES |  |
| 21 | `idventas_vo` | bigint | YES |  |
| 22 | `idempresasvn` | bigint | YES |  |
| 23 | `idcentrosvn` | bigint | YES |  |
| 24 | `a�oexpedientevn` | varchar | YES |  |
| 25 | `serieexpedientevn` | varchar | YES |  |
| 26 | `numexpedientevn` | bigint | YES |  |
| 27 | `numventa_vn` | bigint | YES |  |
| 28 | `usermod` | bigint | YES |  |
| 29 | `hostmod` | varchar | YES |  |
| 30 | `versionfila` | bigint | YES |  |
| 31 | `idvehiculoseguros_abonado` | bigint | YES |  |
| 32 | `numeropoliza` | varchar | YES |  |
| 33 | `idpaises` | varchar | YES |  |
| 34 | `idcodigospostales` | varchar | YES |  |
| 35 | `matricula` | varchar | YES |  |
| 36 | `idmarcas` | bigint | YES |  |
| 37 | `nombremarca` | varchar | YES |  |
| 38 | `idgamas` | bigint | YES |  |
| 39 | `nombregama` | varchar | YES |  |
| 40 | `codmodelo` | varchar | YES |  |
| 41 | `extmodelo` | varchar | YES |  |
| 42 | `a�omodelo` | varchar | YES |  |
| 43 | `nombremodelo` | varchar | YES |  |
| 44 | `idversiones` | varchar | YES |  |
| 45 | `descripcionversion` | varchar | YES |  |
| 46 | `idterceros_propietario` | bigint | YES |  |
| 47 | `nifcif` | varchar | YES |  |
| 48 | `nombre` | varchar | YES |  |
| 49 | `apellido1` | varchar | YES |  |
| 50 | `apellido2` | varchar | YES |  |
| 51 | `fechanacimiento` | timestamp(3) | YES |  |
| 52 | `fechacarnet` | timestamp(3) | YES |  |
| 53 | `idtercerodirecciones` | bigint | YES |  |
| 54 | `iddireccionclases` | bigint | YES |  |
| 55 | `idcalletipos` | varchar | YES |  |
| 56 | `nombrecalle` | varchar | YES |  |
| 57 | `numero` | varchar | YES |  |
| 58 | `bloque` | varchar | YES |  |
| 59 | `piso` | varchar | YES |  |
| 60 | `puerta` | varchar | YES |  |
| 61 | `complemento` | varchar | YES |  |
| 62 | `idpaisesdirecciones` | varchar | YES |  |
| 63 | `idcodigospostalesdirecciones` | varchar | YES |  |
| 64 | `poblacion` | varchar | YES |  |
| 65 | `provincia` | varchar | YES |  |
| 66 | `fechabajadirecciones` | timestamp(3) | YES |  |
| 67 | `idestados` | varchar | YES |  |
| 68 | `idprovincias` | varchar | YES |  |
| 69 | `complemento2` | varchar | YES |  |
| 70 | `telefonos` | varchar | YES |  |
| 71 | `nombreseguro` | varchar | YES |  |
| 72 | `nombreempleado` | varchar | YES |  |
| 73 | `apellido1empleado` | varchar | YES |  |
| 74 | `apellido2empleado` | varchar | YES |  |
| 75 | `descripciontipocalle` | varchar | YES |  |
| 76 | `tomador` | varchar | YES |  |
| 77 | `fechacarnetcaducidad` | timestamp(3) | YES |  |
| 78 | `observaciones` | varchar | YES |  |
| 79 | `idmonedas` | bigint | YES |  |
| 80 | `factorcambiomoneda` | double | YES |  |
| 81 | `importecomisionventa` | double | YES |  |
| 82 | `vin` | varchar | YES |  |
| 83 | `nombrecentrovn` | varchar | YES |  |
| 84 | `nombrecentrovo` | varchar | YES |  |
| 85 | `nombrecentrocomprasvn` | varchar | YES |  |
| 86 | `nombrecentrocomprasvo` | varchar | YES |  |
| 87 | `load_date` | varchar | YES |  |

### spiga.unidaddenegocio

**Columnas:** 18

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codempresa` | varchar | YES |  |
| 2 | `codcentro` | varchar | YES |  |
| 3 | `nombrecentro` | varchar | YES |  |
| 4 | `codseccion` | varchar | YES |  |
| 5 | `nombreseccion` | varchar | YES |  |
| 6 | `coddepartamento` | varchar | YES |  |
| 7 | `nombredepartamento` | varchar | YES |  |
| 8 | `codunidadnegocio` | varchar | YES |  |
| 9 | `nombreunidadnegocio` | varchar | YES |  |
| 10 | `sigla` | varchar | YES |  |
| 11 | `division` | varchar | YES |  |
| 12 | `codsedeambiental` | varchar | YES |  |
| 13 | `sedeambiental` | varchar | YES |  |
| 14 | `codsededistcol` | varchar | YES |  |
| 15 | `sededistribucioncolision` | varchar | YES |  |
| 16 | `unidadnegocio_requisicion` | varchar | YES |  |
| 17 | `nombreunidadnegocio_requisicion` | varchar | YES |  |
| 18 | `load_date` | varchar | YES |  |

### spiga.vw_atenea_contactabilidad

**Columnas:** 16

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id_mes` | bigint | YES |  |
| 2 | `a�o` | bigint | YES |  |
| 3 | `linea` | varchar | YES |  |
| 4 | `idlinea` | bigint | YES |  |
| 5 | `sede` | varchar | YES |  |
| 6 | `idsede` | bigint | YES |  |
| 7 | `area` | varchar | YES |  |
| 8 | `idarea` | bigint | YES |  |
| 9 | `mes` | varchar | YES |  |
| 10 | `contactabilidad` | varchar | YES |  |
| 11 | `idcontactabilidad` | bigint | YES |  |
| 12 | `total` | bigint | YES |  |
| 13 | `basescargadas` | bigint | YES |  |
| 14 | `compa�ia` | varchar | YES |  |
| 15 | `porcentaje` | varchar | YES |  |
| 16 | `load_date` | varchar | YES |  |

### spiga.vw_atenea_contactabilidad_detalle

**Columnas:** 19

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id_mes` | bigint | YES |  |
| 2 | `a�o` | bigint | YES |  |
| 3 | `linea` | varchar | YES |  |
| 4 | `idlinea` | bigint | YES |  |
| 5 | `sede` | varchar | YES |  |
| 6 | `idsede` | bigint | YES |  |
| 7 | `compa�ia` | varchar | YES |  |
| 8 | `area` | varchar | YES |  |
| 9 | `idarea` | bigint | YES |  |
| 10 | `mes` | varchar | YES |  |
| 11 | `contactabilidad` | varchar | YES |  |
| 12 | `idcontactabilidad` | bigint | YES |  |
| 13 | `nombrecliente` | varchar | YES |  |
| 14 | `placa` | varchar | YES |  |
| 15 | `vin` | varchar | YES |  |
| 16 | `cedulacliente` | varchar | YES |  |
| 17 | `telefonocontacto` | varchar | YES |  |
| 18 | `nombreasesor` | varchar | YES |  |
| 19 | `load_date` | varchar | YES |  |

### spiga.vw_atenea_nps

**Columnas:** 21

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id_mes` | bigint | YES |  |
| 2 | `a�o` | bigint | YES |  |
| 3 | `id_compa�ia` | varchar | YES |  |
| 4 | `sede` | varchar | YES |  |
| 5 | `idsede` | bigint | YES |  |
| 6 | `linea` | varchar | YES |  |
| 7 | `idlinea` | bigint | YES |  |
| 8 | `area` | varchar | YES |  |
| 9 | `idarea` | bigint | YES |  |
| 10 | `mes` | varchar | YES |  |
| 11 | `promotores` | bigint | YES |  |
| 12 | `neutros` | bigint | YES |  |
| 13 | `detractores` | bigint | YES |  |
| 14 | `total` | bigint | YES |  |
| 15 | `porcentajepromotor` | varchar | YES |  |
| 16 | `porcentajeneutros` | varchar | YES |  |
| 17 | `porcentajedetractores` | varchar | YES |  |
| 18 | `npstotal` | varchar | YES |  |
| 19 | `meta` | varchar | YES |  |
| 20 | `compa�ia` | varchar | YES |  |
| 21 | `load_date` | varchar | YES |  |

### spiga.vw_atenea_nps_detalle

**Columnas:** 40

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `mes` | varchar | YES |  |
| 2 | `idmes` | bigint | YES |  |
| 3 | `a�o` | bigint | YES |  |
| 4 | `nombrecliente` | varchar | YES |  |
| 5 | `cedulacliente` | varchar | YES |  |
| 6 | `numerocelular` | varchar | YES |  |
| 7 | `telefono` | varchar | YES |  |
| 8 | `telefono2` | varchar | YES |  |
| 9 | `ciudad` | varchar | YES |  |
| 10 | `email` | varchar | YES |  |
| 11 | `sede` | varchar | YES |  |
| 12 | `idsede` | bigint | YES |  |
| 13 | `linea` | varchar | YES |  |
| 14 | `idlinea` | bigint | YES |  |
| 15 | `marca` | varchar | YES |  |
| 16 | `area` | varchar | YES |  |
| 17 | `idarea` | bigint | YES |  |
| 18 | `placa` | varchar | YES |  |
| 19 | `descripciontrabajo` | varchar | YES |  |
| 20 | `asesor` | varchar | YES |  |
| 21 | `fechagestion` | timestamp(3) | YES |  |
| 22 | `resultadogestion` | varchar | YES |  |
| 23 | `canal` | varchar | YES |  |
| 24 | `idcanal` | bigint | YES |  |
| 25 | `usuario` | varchar | YES |  |
| 26 | `nombreusuario` | varchar | YES |  |
| 27 | `numerocontactado` | varchar | YES |  |
| 28 | `pregunta` | varchar | YES |  |
| 29 | `respuesta` | varchar | YES |  |
| 30 | `codigocaso` | varchar | YES |  |
| 31 | `tipocaso` | varchar | YES |  |
| 32 | `clasificacioncaso` | varchar | YES |  |
| 33 | `subclasificacioncaso` | varchar | YES |  |
| 34 | `detalle` | varchar | YES |  |
| 35 | `descripcion` | varchar | YES |  |
| 36 | `fechacreacioncaso` | timestamp(3) | YES |  |
| 37 | `fechavencimientocaso` | timestamp(3) | YES |  |
| 38 | `fechacierrecaso` | timestamp(3) | YES |  |
| 39 | `responsablecaso` | varchar | YES |  |
| 40 | `load_date` | varchar | YES |  |

### spiga.vw_atenea_ordenes_asesores_total

**Columnas:** 13

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `advisername` | varchar | YES |  |
| 2 | `totalasesor` | bigint | YES |  |
| 3 | `id_mes` | bigint | YES |  |
| 4 | `mes` | varchar | YES |  |
| 5 | `a�o` | bigint | YES |  |
| 6 | `compa�ia` | varchar | YES |  |
| 7 | `linea` | varchar | YES |  |
| 8 | `idlinea` | bigint | YES |  |
| 9 | `sede` | varchar | YES |  |
| 10 | `idsede` | bigint | YES |  |
| 11 | `area` | varchar | YES |  |
| 12 | `idarea` | bigint | YES |  |
| 13 | `load_date` | varchar | YES |  |

### spiga.vw_atenea_pqr

**Columnas:** 34

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `id_mes` | bigint | YES |  |
| 3 | `a�o` | bigint | YES |  |
| 4 | `mes` | varchar | YES |  |
| 5 | `empresa` | varchar | YES |  |
| 6 | `linea` | varchar | YES |  |
| 7 | `sede` | varchar | YES |  |
| 8 | `proceso` | varchar | YES |  |
| 9 | `identificationnumber` | varchar | YES |  |
| 10 | `nombrecliente` | varchar | YES |  |
| 11 | `placa` | varchar | YES |  |
| 12 | `gamma` | varchar | YES |  |
| 13 | `modelo` | varchar | YES |  |
| 14 | `kilometraje` | varchar | YES |  |
| 15 | `vin` | varchar | YES |  |
| 16 | `marcavehiculo` | varchar | YES |  |
| 17 | `numeromotor` | varchar | YES |  |
| 18 | `telefonocontacto` | varchar | YES |  |
| 19 | `idticket` | bigint | YES |  |
| 20 | `c�digocaso` | varchar | YES |  |
| 21 | `tipocaso` | varchar | YES |  |
| 22 | `clasificacioncaso` | varchar | YES |  |
| 23 | `subclasificacioncaso` | varchar | YES |  |
| 24 | `detalle` | varchar | YES |  |
| 25 | `descripci�n` | varchar | YES |  |
| 26 | `fecharegistro` | timestamp(3) | YES |  |
| 27 | `fecharespuesta` | timestamp(3) | YES |  |
| 28 | `cantidaddiascierre` | bigint | YES |  |
| 29 | `cantidaddiastranscurridos` | bigint | YES |  |
| 30 | `estado` | varchar | YES |  |
| 31 | `origen` | varchar | YES |  |
| 32 | `subclasificaci�n` | varchar | YES |  |
| 33 | `nombreasesor` | varchar | YES |  |
| 34 | `load_date` | varchar | YES |  |

### spiga.vw_atenea_preguntas_detalle

**Columnas:** 40

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `mes` | varchar | YES |  |
| 2 | `idmes` | bigint | YES |  |
| 3 | `a�o` | bigint | YES |  |
| 4 | `nombrecliente` | varchar | YES |  |
| 5 | `cedulacliente` | varchar | YES |  |
| 6 | `numerocelular` | varchar | YES |  |
| 7 | `telefono` | varchar | YES |  |
| 8 | `telefono2` | varchar | YES |  |
| 9 | `ciudad` | varchar | YES |  |
| 10 | `email` | varchar | YES |  |
| 11 | `sede` | varchar | YES |  |
| 12 | `idsede` | bigint | YES |  |
| 13 | `linea` | varchar | YES |  |
| 14 | `idlinea` | bigint | YES |  |
| 15 | `marca` | varchar | YES |  |
| 16 | `area` | varchar | YES |  |
| 17 | `idarea` | bigint | YES |  |
| 18 | `placa` | varchar | YES |  |
| 19 | `descripciontrabajo` | varchar | YES |  |
| 20 | `asesor` | varchar | YES |  |
| 21 | `fechagestion` | timestamp(3) | YES |  |
| 22 | `resultadogestion` | varchar | YES |  |
| 23 | `canal` | varchar | YES |  |
| 24 | `idcanal` | bigint | YES |  |
| 25 | `usuario` | varchar | YES |  |
| 26 | `nombreusuario` | varchar | YES |  |
| 27 | `numerocontactado` | varchar | YES |  |
| 28 | `pregunta` | varchar | YES |  |
| 29 | `respuesta` | varchar | YES |  |
| 30 | `codigocaso` | varchar | YES |  |
| 31 | `tipocaso` | varchar | YES |  |
| 32 | `clasificacioncaso` | varchar | YES |  |
| 33 | `subclasificacioncaso` | varchar | YES |  |
| 34 | `detalle` | varchar | YES |  |
| 35 | `descripcion` | varchar | YES |  |
| 36 | `fechacreacioncaso` | timestamp(3) | YES |  |
| 37 | `fechavencimientocaso` | timestamp(3) | YES |  |
| 38 | `fechacierrecaso` | timestamp(3) | YES |  |
| 39 | `responsablecaso` | varchar | YES |  |
| 40 | `load_date` | varchar | YES |  |

### spiga.vw_atenea_satisfaccion

**Columnas:** 19

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id_mes` | bigint | YES |  |
| 2 | `mes` | varchar | YES |  |
| 3 | `a�o` | bigint | YES |  |
| 4 | `sede` | varchar | YES |  |
| 5 | `idsede` | bigint | YES |  |
| 6 | `linea` | varchar | YES |  |
| 7 | `idlinea` | bigint | YES |  |
| 8 | `area` | varchar | YES |  |
| 9 | `idarea` | bigint | YES |  |
| 10 | `encuestasefectivas` | bigint | YES |  |
| 11 | `res_1` | bigint | YES |  |
| 12 | `res_2` | bigint | YES |  |
| 13 | `res_3` | bigint | YES |  |
| 14 | `res_4` | bigint | YES |  |
| 15 | `res_5` | bigint | YES |  |
| 16 | `satisfaccion` | bigint | YES |  |
| 17 | `meta` | varchar | YES |  |
| 18 | `compa�ia` | varchar | YES |  |
| 19 | `load_date` | varchar | YES |  |

### spiga.vw_atenea_satisfaccion_detalle

**Columnas:** 40

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idmes` | bigint | YES |  |
| 2 | `a�o` | bigint | YES |  |
| 3 | `mes` | varchar | YES |  |
| 4 | `nombrecliente` | varchar | YES |  |
| 5 | `cedulacliente` | varchar | YES |  |
| 6 | `numerocelular` | varchar | YES |  |
| 7 | `telefono` | varchar | YES |  |
| 8 | `telefono2` | varchar | YES |  |
| 9 | `ciudad` | varchar | YES |  |
| 10 | `email` | varchar | YES |  |
| 11 | `sede` | varchar | YES |  |
| 12 | `idsede` | bigint | YES |  |
| 13 | `linea` | varchar | YES |  |
| 14 | `idlinea` | bigint | YES |  |
| 15 | `marca` | varchar | YES |  |
| 16 | `area` | varchar | YES |  |
| 17 | `idarea` | bigint | YES |  |
| 18 | `placa` | varchar | YES |  |
| 19 | `descripciontrabajo` | varchar | YES |  |
| 20 | `asesor` | varchar | YES |  |
| 21 | `fechagestion` | timestamp(3) | YES |  |
| 22 | `resultadogestion` | varchar | YES |  |
| 23 | `canal` | varchar | YES |  |
| 24 | `idcanal` | bigint | YES |  |
| 25 | `usuario` | varchar | YES |  |
| 26 | `nombreusuario` | varchar | YES |  |
| 27 | `numerocontactado` | varchar | YES |  |
| 28 | `pregunta` | varchar | YES |  |
| 29 | `respuesta` | varchar | YES |  |
| 30 | `codigocaso` | varchar | YES |  |
| 31 | `tipocaso` | varchar | YES |  |
| 32 | `clasificacioncaso` | varchar | YES |  |
| 33 | `subclasificacioncaso` | varchar | YES |  |
| 34 | `detalle` | varchar | YES |  |
| 35 | `descripcion` | varchar | YES |  |
| 36 | `fechacreacioncaso` | timestamp(3) | YES |  |
| 37 | `fechavencimientocaso` | timestamp(3) | YES |  |
| 38 | `fechacierrecaso` | timestamp(3) | YES |  |
| 39 | `responsablecaso` | varchar | YES |  |
| 40 | `load_date` | varchar | YES |  |

## 🥉 spiga_dbmlc

`Capa: Bronce / Raw`

### spiga_dbmlc.comisionesspigavn

**Columnas:** 50

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `idcomisionspiga` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `ano_spiga` | integer | YES |  |
| 6 | `mes_spiga` | integer | YES |  |
| 7 | `codigoempresa` | smallint | YES |  |
| 8 | `empresa` | varchar | YES |  |
| 9 | `codigoempresasugerido` | integer | YES |  |
| 10 | `empresasugerida` | varchar | YES |  |
| 11 | `codigocentro` | smallint | YES |  |
| 12 | `centro` | varchar | YES |  |
| 13 | `codigoseccion` | integer | YES |  |
| 14 | `seccion` | varchar | YES |  |
| 15 | `fechafactura` | timestamp(3) | YES |  |
| 16 | `numerofactura` | varchar | YES |  |
| 17 | `vin` | varchar | YES |  |
| 18 | `codigomarca` | smallint | YES |  |
| 19 | `marca` | varchar | YES |  |
| 20 | `codigogama` | smallint | YES |  |
| 21 | `gama` | varchar | YES |  |
| 22 | `codigomodelo` | varchar | YES |  |
| 23 | `extension` | varchar | YES |  |
| 24 | `a�omodelo` | varchar | YES |  |
| 25 | `modelo` | varchar | YES |  |
| 26 | `codigoversion` | varchar | YES |  |
| 27 | `nombreversion` | varchar | YES |  |
| 28 | `cedulavendedor` | bigint | YES |  |
| 29 | `nombrevendedor` | varchar | YES |  |
| 30 | `nit` | varchar | YES |  |
| 31 | `nombretercero` | varchar | YES |  |
| 32 | `preciovehiculo` | decimal(18,4) | YES |  |
| 33 | `preciolista` | decimal(18,4) | YES |  |
| 34 | `valordto` | decimal(18,4) | YES |  |
| 35 | `importeimpuestos` | decimal(38,4) | YES |  |
| 36 | `totalfactura` | decimal(18,4) | YES |  |
| 37 | `fechacancelacionfactura` | timestamp(3) | YES |  |
| 38 | `totalcanceladofactura` | decimal(38,4) | YES |  |
| 39 | `fecharemesa` | timestamp(3) | YES |  |
| 40 | `valorremesado` | decimal(38,4) | YES |  |
| 41 | `fechaentregacliente` | timestamp(3) | YES |  |
| 42 | `descuentopolitica` | decimal(15,9) | YES |  |
| 43 | `numerentregas` | integer | YES |  |
| 44 | `tipo_servicio` | varchar | YES |  |
| 45 | `cuotaretefuente` | decimal(18,4) | YES |  |
| 46 | `entregaefectiva` | integer | YES |  |
| 47 | `procedencia` | varchar | YES |  |
| 48 | `procedenciadetalle` | varchar | YES |  |
| 49 | `tipooportunidad` | varchar | YES |  |
| 50 | `entregainmediata` | boolean | YES |  |

### spiga_dbmlc.comisionesspigavo

**Columnas:** 49

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `idcomisionspiga` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `ano_spiga` | integer | YES |  |
| 6 | `mes_spiga` | integer | YES |  |
| 7 | `codigoempresa` | smallint | YES |  |
| 8 | `empresa` | varchar | YES |  |
| 9 | `codigoempresasugerido` | integer | YES |  |
| 10 | `empresasugerida` | varchar | YES |  |
| 11 | `codigocentro` | smallint | YES |  |
| 12 | `centro` | varchar | YES |  |
| 13 | `codigoseccion` | integer | YES |  |
| 14 | `seccion` | varchar | YES |  |
| 15 | `fechafactura` | timestamp(3) | YES |  |
| 16 | `numerofactura` | varchar | YES |  |
| 17 | `vin` | varchar | YES |  |
| 18 | `codigomarca` | smallint | YES |  |
| 19 | `marca` | varchar | YES |  |
| 20 | `codigogama` | smallint | YES |  |
| 21 | `gama` | varchar | YES |  |
| 22 | `codigomodelo` | varchar | YES |  |
| 23 | `extension` | varchar | YES |  |
| 24 | `a�omodelo` | varchar | YES |  |
| 25 | `modelo` | varchar | YES |  |
| 26 | `codigoversion` | varchar | YES |  |
| 27 | `nombreversion` | varchar | YES |  |
| 28 | `cedulavendedor` | bigint | YES |  |
| 29 | `nombrevendedor` | varchar | YES |  |
| 30 | `nit` | varchar | YES |  |
| 31 | `nombretercero` | varchar | YES |  |
| 32 | `preciovehiculo` | decimal(18,4) | YES |  |
| 33 | `preciolista` | decimal(18,4) | YES |  |
| 34 | `valordto` | decimal(18,4) | YES |  |
| 35 | `importeimpuestos` | decimal(38,4) | YES |  |
| 36 | `totalfactura` | decimal(18,4) | YES |  |
| 37 | `fechacancelacionfactura` | timestamp(3) | YES |  |
| 38 | `totalcanceladofactura` | decimal(38,4) | YES |  |
| 39 | `fecharemesa` | timestamp(3) | YES |  |
| 40 | `valorremesado` | decimal(38,4) | YES |  |
| 41 | `fechaentregacliente` | timestamp(3) | YES |  |
| 42 | `descuentopolitica` | decimal(15,9) | YES |  |
| 43 | `numerentregas` | integer | YES |  |
| 44 | `tipo_servicio` | varchar | YES |  |
| 45 | `cuotaretefuente` | decimal(38,4) | YES |  |
| 46 | `entregaefectiva` | integer | YES |  |
| 47 | `procedencia` | varchar | YES |  |
| 48 | `procedenciadetalle` | varchar | YES |  |
| 49 | `tipooportunidad` | varchar | YES |  |

### spiga_dbmlc.empresas

**Columnas:** 6

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codigoempresa` | smallint | YES |  |
| 2 | `nombreempresa` | varchar | YES |  |
| 3 | `siglaempresa` | varchar | YES |  |
| 4 | `nitempresa` | varchar | YES |  |
| 5 | `activarliquidacion` | boolean | YES |  |
| 6 | `codpais` | smallint | YES |  |

### spiga_dbmlc.spiga_compradeusados

**Columnas:** 99

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacion` | int | YES |  |
| 2 | `idconsecutivo` | int | YES |  |
| 3 | `ano_periodo` | int | YES |  |
| 4 | `mes_periodo` | int | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `idempresas` | smallint | YES |  |
| 7 | `idcentros` | smallint | YES |  |
| 8 | `añoexpediente` | string | YES |  |
| 9 | `serieexpediente` | string | YES |  |
| 10 | `numexpediente` | int | YES |  |
| 11 | `comprasnumdet` | smallint | YES |  |
| 12 | `idvehiculos` | int | YES |  |
| 13 | `idcompratipos` | string | YES |  |
| 14 | `importecompra` | decimal(30,11) | YES |  |
| 15 | `importetotal` | decimal(30,11) | YES |  |
| 16 | `codcompramultiple` | int | YES |  |
| 17 | `fechaalta` | timestamp | YES |  |
| 18 | `fechaanulacion` | timestamp | YES |  |
| 19 | `idsecciones` | int | YES |  |
| 20 | `fechaabono` | timestamp | YES |  |
| 21 | `comprasnumdetabonado` | smallint | YES |  |
| 22 | `idcompraestados` | string | YES |  |
| 23 | `observaciones` | string | YES |  |
| 24 | `idregistrotipos` | string | YES |  |
| 25 | `reservafecha` | timestamp | YES |  |
| 26 | `reservaimporte` | decimal(30,11) | YES |  |
| 27 | `reservaidempleados` | smallint | YES |  |
| 28 | `reservaterceros` | int | YES |  |
| 29 | `realizargastoadicionalautomatico` | boolean | YES |  |
| 30 | `nocontabilizardocumentacion` | boolean | YES |  |
| 31 | `idempleadovendedor` | smallint | YES |  |
| 32 | `kms` | int | YES |  |
| 33 | `añoexpedientecambio` | string | YES |  |
| 34 | `serieexpedientecambio` | string | YES |  |
| 35 | `numexpedientecambio` | int | YES |  |
| 36 | `prever` | boolean | YES |  |
| 37 | `visibleweb` | boolean | YES |  |
| 38 | `comercializable` | boolean | YES |  |
| 39 | `generaasiento` | string | YES |  |
| 40 | `idmoduloorigen` | string | YES |  |
| 41 | `idusuariosanulacion` | smallint | YES |  |
| 42 | `idempleadosanulacion` | smallint | YES |  |
| 43 | `hostanulacion` | string | YES |  |
| 44 | `usermod` | smallint | YES |  |
| 45 | `hostmod` | string | YES |  |
| 46 | `versionfila` | int | YES |  |
| 47 | `añoexpedientecambiovn` | string | YES |  |
| 48 | `serieexpedientecambiovn` | string | YES |  |
| 49 | `numexpedientecambiovn` | int | YES |  |
| 50 | `idcomprasnumdetcambio` | smallint | YES |  |
| 51 | `idcomprasnumdetcambiovn` | smallint | YES |  |
| 52 | `marcarkm0web` | boolean | YES |  |
| 53 | `fecharecepcion` | timestamp | YES |  |
| 54 | `fechaasiento` | timestamp | YES |  |
| 55 | `seriefactura` | string | YES |  |
| 56 | `numfactura` | string | YES |  |
| 57 | `añofactura` | string | YES |  |
| 58 | `fechafactura` | timestamp | YES |  |
| 59 | `idmarcas` | smallint | YES |  |
| 60 | `idgamas` | smallint | YES |  |
| 61 | `codmodelo` | string | YES |  |
| 62 | `extmodelo` | string | YES |  |
| 63 | `añomodelo` | string | YES |  |
| 64 | `idversiones` | string | YES |  |
| 65 | `matricula` | string | YES |  |
| 66 | `vin` | string | YES |  |
| 67 | `nombremarca` | string | YES |  |
| 68 | `nombregama` | string | YES |  |
| 69 | `importebi` | decimal(18,4) | YES |  |
| 70 | `importe576` | decimal(18,4) | YES |  |
| 71 | `importedvn` | decimal(18,4) | YES |  |
| 72 | `exentos` | decimal(18,4) | YES |  |
| 73 | `vincambio` | string | YES |  |
| 74 | `matriculacambio` | string | YES |  |
| 75 | `idmarcascambio` | smallint | YES |  |
| 76 | `idgamascambio` | smallint | YES |  |
| 77 | `nombremarcacambio` | string | YES |  |
| 78 | `nombregamacambio` | string | YES |  |
| 79 | `gastoadicionaldetalles` | decimal(20,6) | YES |  |
| 80 | `idterceros` | int | YES |  |
| 81 | `nombreterceros` | string | YES |  |
| 82 | `nombre` | string | YES |  |
| 83 | `idmonedas` | smallint | YES |  |
| 84 | `factorcambiomoneda` | decimal(28,10) | YES |  |
| 85 | `monedaorigen` | string | YES |  |
| 86 | `centroventavehiculocambio` | string | YES |  |
| 87 | `nombreempleadoventavehiculocambio` | string | YES |  |
| 88 | `apellido1empleadoventavehiculocambio` | string | YES |  |
| 89 | `apellido2empleadoventavehiculocambio` | string | YES |  |
| 90 | `nombreempleadocompra` | string | YES |  |
| 91 | `apellido1empleadocompra` | string | YES |  |
| 92 | `apellido2empleadocompra` | string | YES |  |
| 93 | `descripcioncompratipos` | string | YES |  |
| 94 | `esinmovilizado` | boolean | YES |  |
| 95 | `nombremodelo` | string | YES |  |
| 96 | `descripcionversiones` | string | YES |  |
| 97 | `descripcionsecciones` | string | YES |  |
| 98 | `descripcionregistrotipos` | string | YES |  |
| 99 | `seccionventavehiculocambio` | string | YES |  |

### spiga_dbmlc.spiga_compras_sel_stockvn

**Columnas:** 205

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | int | YES |  |
| 2 | `idconsecutivo` | int | YES |  |
| 3 | `ano_periodo` | int | YES |  |
| 4 | `mes_periodo` | int | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `idempresas` | smallint | YES |  |
| 7 | `idcentros` | smallint | YES |  |
| 8 | `añoexpediente` | string | YES |  |
| 9 | `serieexpediente` | string | YES |  |
| 10 | `numexpediente` | int | YES |  |
| 11 | `comprasnumdet` | smallint | YES |  |
| 12 | `idasientos` | int | YES |  |
| 13 | `añoasiento` | string | YES |  |
| 14 | `idvehiculos` | int | YES |  |
| 15 | `idterceros` | int | YES |  |
| 16 | `idcompratipos` | string | YES |  |
| 17 | `numexpedientescompramultiple` | smallint | YES |  |
| 18 | `idmarcas` | smallint | YES |  |
| 19 | `idgamas` | smallint | YES |  |
| 20 | `codmodelo` | string | YES |  |
| 21 | `extmodelo` | string | YES |  |
| 22 | `añomodelo` | string | YES |  |
| 23 | `idversiones` | string | YES |  |
| 24 | `idtarifas` | smallint | YES |  |
| 25 | `seriefactura` | string | YES |  |
| 26 | `numfactura` | string | YES |  |
| 27 | `añofactura` | string | YES |  |
| 28 | `fechaalta` | timestamp | YES |  |
| 29 | `fechaanulacion` | timestamp | YES |  |
| 30 | `fechacampaalta` | timestamp | YES |  |
| 31 | `fecharecepcion` | timestamp | YES |  |
| 32 | `fechafactura` | timestamp | YES |  |
| 33 | `fechaasiento` | timestamp | YES |  |
| 34 | `fechareserva` | timestamp | YES |  |
| 35 | `importacionrealizada` | boolean | YES |  |
| 36 | `importacionmodificada` | boolean | YES |  |
| 37 | `fechaimportacionrealizada` | timestamp | YES |  |
| 38 | `fechaimportacionmodificada` | timestamp | YES |  |
| 39 | `preciobase` | decimal(18,4) | YES |  |
| 40 | `preciopintura` | decimal(18,4) | YES |  |
| 41 | `preciotransporte` | decimal(18,4) | YES |  |
| 42 | `precioopciones` | decimal(18,4) | YES |  |
| 43 | `preciootroscargos` | decimal(18,4) | YES |  |
| 44 | `importecompra` | decimal(18,4) | YES |  |
| 45 | `baseimponible` | decimal(19,4) | YES |  |
| 46 | `idcentrosasignadoventa` | smallint | YES |  |
| 47 | `idseccionesasignadaventa` | int | YES |  |
| 48 | `preciolegalizacion` | decimal(18,4) | YES |  |
| 49 | `precioisv` | decimal(18,4) | YES |  |
| 50 | `precioecovalor` | decimal(18,4) | YES |  |
| 51 | `baseexenta` | decimal(18,4) | YES |  |
| 52 | `sumadescuentos` | decimal(18,4) | YES |  |
| 53 | `idempleadosreserva` | smallint | YES |  |
| 54 | `idagentesreserva` | int | YES |  |
| 55 | `idterceros_cedidoconcesionario` | int | YES |  |
| 56 | `numfacturamensual` | smallint | YES |  |
| 57 | `idsecciones` | int | YES |  |
| 58 | `numexpedicion` | string | YES |  |
| 59 | `programa` | string | YES |  |
| 60 | `realizargastoadicionalautomatico` | boolean | YES |  |
| 61 | `nocontabilizardocumentacion` | boolean | YES |  |
| 62 | `observaciones` | string | YES |  |
| 63 | `comprasnumdet_abonado` | smallint | YES |  |
| 64 | `idcompraestados` | string | YES |  |
| 65 | `usermod` | smallint | YES |  |
| 66 | `hostmod` | string | YES |  |
| 67 | `versionfila` | int | YES |  |
| 68 | `fechaabono` | timestamp | YES |  |
| 69 | `idusuariosanulacion` | smallint | YES |  |
| 70 | `idempleadosanulacion` | smallint | YES |  |
| 71 | `hostanulacion` | string | YES |  |
| 72 | `idasientos_polizanoactivo` | int | YES |  |
| 73 | `añoasiento_polizanoactivo` | string | YES |  |
| 74 | `nombremarca` | string | YES |  |
| 75 | `backcolorcabecerargb` | string | YES |  |
| 76 | `backcolordetallergb` | string | YES |  |
| 77 | `forecolorcabecerargb` | string | YES |  |
| 78 | `forecolordetallergb` | string | YES |  |
| 79 | `nombregama` | string | YES |  |
| 80 | `preciolegalizacion1` | decimal(18,4) | YES |  |
| 81 | `precioisv1` | decimal(18,4) | YES |  |
| 82 | `precioecovalor1` | decimal(18,4) | YES |  |
| 83 | `activo` | boolean | YES |  |
| 84 | `idcarroceriatipos` | string | YES |  |
| 85 | `idclasificaciontipos` | string | YES |  |
| 86 | `idmarcatallermodelos` | string | YES |  |
| 87 | `idtracciontipos` | string | YES |  |
| 88 | `idcambiotipos` | string | YES |  |
| 89 | `idtonelajetipos` | string | YES |  |
| 90 | `iddistanciaejestipos` | string | YES |  |
| 91 | `codexternomodelo` | string | YES |  |
| 92 | `potenciafiscal` | string | YES |  |
| 93 | `potenciareal` | string | YES |  |
| 94 | `cilindrada` | decimal(8,2) | YES |  |
| 95 | `aceleracion` | string | YES |  |
| 96 | `velocidadmax` | decimal(7,2) | YES |  |
| 97 | `par` | string | YES |  |
| 98 | `numerocilindros` | int | YES |  |
| 99 | `consumointerurbano` | decimal(7,2) | YES |  |
| 100 | `consumourbano` | decimal(7,2) | YES |  |
| 101 | `consumomedio` | decimal(7,2) | YES |  |
| 102 | `emisionesco2interurbano` | decimal(7,2) | YES |  |
| 103 | `emisionesco2urbano` | decimal(7,2) | YES |  |
| 104 | `emisionesco2medio` | decimal(7,2) | YES |  |
| 105 | `importado` | boolean | YES |  |
| 106 | `modificado` | boolean | YES |  |
| 107 | `permiteplanprever` | boolean | YES |  |
| 108 | `visibleweb` | boolean | YES |  |
| 109 | `periodoinspeccion` | smallint | YES |  |
| 110 | `kilometrosinspeccion` | string | YES |  |
| 111 | `descripcionmodelotaller` | string | YES |  |
| 112 | `vin` | string | YES |  |
| 113 | `matricula` | string | YES |  |
| 114 | `comision` | string | YES |  |
| 115 | `fechamatriculacion` | timestamp | YES |  |
| 116 | `codigofabricacion` | string | YES |  |
| 117 | `fechafabricacion` | timestamp | YES |  |
| 118 | `numeromotor` | string | YES |  |
| 119 | `nombreempresa` | string | YES |  |
| 120 | `nombrecentro` | string | YES |  |
| 121 | `diasstock` | int | YES |  |
| 122 | `idrecursos` | int | YES |  |
| 123 | `idubicacionesultimarealizada` | string | YES |  |
| 124 | `fechaexpedientealtaultimarealizada` | timestamp | YES |  |
| 125 | `ubicacionvn` | string | YES |  |
| 126 | `fechaubicacion` | timestamp | YES |  |
| 127 | `idubicacionesultima` | string | YES |  |
| 128 | `fechaexpedientealtaultima` | timestamp | YES |  |
| 129 | `ubicacionvnprevista` | string | YES |  |
| 130 | `fechasalidareal` | timestamp | YES |  |
| 131 | `nombreempleadoreserva` | string | YES |  |
| 132 | `nombreagente` | string | YES |  |
| 133 | `cedido` | string | YES |  |
| 134 | `fechallegadapuerto` | timestamp | YES |  |
| 135 | `fecharetirada` | timestamp | YES |  |
| 136 | `datoscarta` | string | YES |  |
| 137 | `preciocompra` | decimal(18,4) | YES |  |
| 138 | `precioventa` | decimal(18,4) | YES |  |
| 139 | `transportecompra` | decimal(18,4) | YES |  |
| 140 | `precioventaopcionales` | int | YES |  |
| 141 | `rodajetrimestral` | decimal(18,4) | YES |  |
| 142 | `gastosmatriculacion` | decimal(18,4) | YES |  |
| 143 | `atipicos` | decimal(18,4) | YES |  |
| 144 | `transporteventa` | decimal(18,4) | YES |  |
| 145 | `preciolegalizacionventa` | decimal(18,4) | YES |  |
| 146 | `impuesto576porc` | decimal(9,7) | YES |  |
| 147 | `numpedidovn` | string | YES |  |
| 148 | `idtercerospedido` | int | YES |  |
| 149 | `fechainiciofranquicia` | timestamp | YES |  |
| 150 | `fechafinalfranquicia` | timestamp | YES |  |
| 151 | `fechaaradefinitiva` | timestamp | YES |  |
| 152 | `fechaentregaconcesionario` | timestamp | YES |  |
| 153 | `fechacompromisoentrega` | timestamp | YES |  |
| 154 | `mesesgarantiaobligatoriavn` | smallint | YES |  |
| 155 | `numpedidofabrica` | string | YES |  |
| 156 | `numpedidomarca` | string | YES |  |
| 157 | `pedidoobservaciones` | string | YES |  |
| 158 | `idpedidolocaltipos` | string | YES |  |
| 159 | `fechadespacho` | timestamp | YES |  |
| 160 | `diasestancia` | int | YES |  |
| 161 | `observacionubicacion` | string | YES |  |
| 162 | `diasdecarenciadocumentacion` | smallint | YES |  |
| 163 | `diascarencia` | smallint | YES |  |
| 164 | `situacion` | string | YES |  |
| 165 | `permitirfacturarenotrocentro` | boolean | YES |  |
| 166 | `idpaises_origen` | string | YES |  |
| 167 | `importacion` | boolean | YES |  |
| 168 | `factorcambiomonedacontravalor` | decimal(18,10) | YES |  |
| 169 | `importepedidoservicios` | decimal(38,4) | YES |  |
| 170 | `importegastosadicionales` | decimal(38,4) | YES |  |
| 171 | `fechapedido` | timestamp | YES |  |
| 172 | `diasexposicion` | smallint | YES |  |
| 173 | `homologacion` | boolean | YES |  |
| 174 | `nombreprospectoreservapedido` | string | YES |  |
| 175 | `nombreclientereservapedido` | string | YES |  |
| 176 | `nombreclientereservacompra` | string | YES |  |
| 177 | `precioiuc` | decimal(18,4) | YES |  |
| 178 | `añopedidosservicios` | string | YES |  |
| 179 | `seriepedidosservicios` | string | YES |  |
| 180 | `idpedidosservicios` | int | YES |  |
| 181 | `idmonedas` | smallint | YES |  |
| 182 | `factorcambiomoneda` | decimal(18,10) | YES |  |
| 183 | `idregimencontable` | string | YES |  |
| 184 | `colorcompleto` | string | YES |  |
| 185 | `tapiceriacompleta` | string | YES |  |
| 186 | `descripcioncambiotipos` | string | YES |  |
| 187 | `nombreversion` | string | YES |  |
| 188 | `nombretarifa` | string | YES |  |
| 189 | `nombremodelo` | string | YES |  |
| 190 | `descripcionestadocompra` | string | YES |  |
| 191 | `descripciontipocombustible` | string | YES |  |
| 192 | `descripcionpedidolocaltipos` | string | YES |  |
| 193 | `descripcioncomprausos` | string | YES |  |
| 194 | `descripcionestadopedidosservicio` | string | YES |  |
| 195 | `idtercerosreserva` | int | YES |  |
| 196 | `idcomprausos` | string | YES |  |
| 197 | `visualizarenstockcomprausos` | boolean | YES |  |
| 198 | `tipocompra` | string | YES |  |
| 199 | `idiventario` | bigint | YES |  |
| 200 | `fechaultimoinventario` | timestamp | YES |  |
| 201 | `documentosinventario` | smallint | YES |  |
| 202 | `documentosrespuestasinventario` | int | YES |  |
| 203 | `porcimpuestos_iva` | decimal(9,7) | YES |  |
| 204 | `porcimpuestos_con` | decimal(9,7) | YES |  |
| 205 | `idcentrosubicacion` | smallint | YES |  |

### spiga_dbmlc.spiga_compras_sel_stockvo

**Columnas:** 121

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | int | YES |  |
| 2 | `idconsecutivo` | int | YES |  |
| 3 | `ano_periodo` | int | YES |  |
| 4 | `mes_periodo` | int | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `idempresas` | smallint | YES |  |
| 7 | `idcentros` | smallint | YES |  |
| 8 | `añoexpediente` | string | YES |  |
| 9 | `serieexpediente` | string | YES |  |
| 10 | `numexpediente` | int | YES |  |
| 11 | `comprasnumdet` | smallint | YES |  |
| 12 | `idvehiculos` | int | YES |  |
| 13 | `idcompratipos` | string | YES |  |
| 14 | `codcompramultiple` | int | YES |  |
| 15 | `fechaalta` | timestamp | YES |  |
| 16 | `fechaanulacion` | timestamp | YES |  |
| 17 | `fecharecepcion` | timestamp | YES |  |
| 18 | `idsecciones` | int | YES |  |
| 19 | `fechaabono` | timestamp | YES |  |
| 20 | `comprasnumdetabonado` | smallint | YES |  |
| 21 | `idcompraestados` | string | YES |  |
| 22 | `observaciones` | string | YES |  |
| 23 | `idregistrotipos` | string | YES |  |
| 24 | `reservafecha` | timestamp | YES |  |
| 25 | `reservaidempleados` | smallint | YES |  |
| 26 | `reservaterceros` | int | YES |  |
| 27 | `realizargastoadicionalautomatico` | boolean | YES |  |
| 28 | `nocontabilizardocumentacion` | boolean | YES |  |
| 29 | `idempleadovendedor` | smallint | YES |  |
| 30 | `kms` | int | YES |  |
| 31 | `añoexpedientecambio` | string | YES |  |
| 32 | `serieexpedientecambio` | string | YES |  |
| 33 | `numexpedientecambio` | int | YES |  |
| 34 | `fechaasiento` | timestamp | YES |  |
| 35 | `prever` | boolean | YES |  |
| 36 | `generaasiento` | string | YES |  |
| 37 | `idmoduloorigen` | string | YES |  |
| 38 | `idusuariosanulacion` | smallint | YES |  |
| 39 | `idempleadosanulacion` | smallint | YES |  |
| 40 | `hostanulacion` | string | YES |  |
| 41 | `usermod` | smallint | YES |  |
| 42 | `hostmod` | string | YES |  |
| 43 | `versionfila` | int | YES |  |
| 44 | `reservaimporte` | decimal(37,14) | YES |  |
| 45 | `importecompra` | decimal(37,14) | YES |  |
| 46 | `precioventaminimo` | decimal(37,14) | YES |  |
| 47 | `visibleweb` | boolean | YES |  |
| 48 | `comercializable` | boolean | YES |  |
| 49 | `idcomprausos` | string | YES |  |
| 50 | `vin` | string | YES |  |
| 51 | `matricula` | string | YES |  |
| 52 | `comision` | string | YES |  |
| 53 | `fechamatriculacion` | timestamp | YES |  |
| 54 | `idmarcas` | smallint | YES |  |
| 55 | `idgamas` | smallint | YES |  |
| 56 | `codmodelo` | string | YES |  |
| 57 | `extmodelo` | string | YES |  |
| 58 | `añomodelo` | string | YES |  |
| 59 | `idversiones` | string | YES |  |
| 60 | `idmarcasexterna` | smallint | YES |  |
| 61 | `idgamasexterna` | smallint | YES |  |
| 62 | `codmodeloexterna` | string | YES |  |
| 63 | `extmodeloexterna` | string | YES |  |
| 64 | `añomodeloexterna` | string | YES |  |
| 65 | `idversionesexterna` | string | YES |  |
| 66 | `kmsactuales` | int | YES |  |
| 67 | `permitirfacturarenotrocentro` | boolean | YES |  |
| 68 | `otrasobservaciones` | string | YES |  |
| 69 | `horasusoactual` | int | YES |  |
| 70 | `nombremarca` | string | YES |  |
| 71 | `nombregama` | string | YES |  |
| 72 | `nombremodelo` | string | YES |  |
| 73 | `nombregamaexterna` | string | YES |  |
| 74 | `nombremodeloexterna` | string | YES |  |
| 75 | `descripciontipocombustible` | string | YES |  |
| 76 | `descripciontipocombustibleexterna` | string | YES |  |
| 77 | `descripcionestadocompra` | string | YES |  |
| 78 | `potenciareal` | string | YES |  |
| 79 | `potenciarealexterna` | string | YES |  |
| 80 | `numeropuertas` | string | YES |  |
| 81 | `numeroplazas` | string | YES |  |
| 82 | `nombreempresa` | string | YES |  |
| 83 | `nombrecentro` | string | YES |  |
| 84 | `descripcionseccion` | string | YES |  |
| 85 | `descripciontiporegistro` | string | YES |  |
| 86 | `idcomprainternatipos` | string | YES |  |
| 87 | `descripcioncompratipos` | string | YES |  |
| 88 | `descripcioncarroceriatipos` | string | YES |  |
| 89 | `diasstock` | int | YES |  |
| 90 | `fecharetirada` | timestamp | YES |  |
| 91 | `importeventasugerido` | decimal(18,4) | YES |  |
| 92 | `nombreempleadoreserva` | string | YES |  |
| 93 | `nombreterceroreserva` | string | YES |  |
| 94 | `idrecursos` | int | YES |  |
| 95 | `importebi` | decimal(38,14) | YES |  |
| 96 | `importedvn` | decimal(38,14) | YES |  |
| 97 | `importe576` | decimal(38,14) | YES |  |
| 98 | `exentos` | decimal(38,14) | YES |  |
| 99 | `importegastosadicionales` | decimal(38,13) | YES |  |
| 100 | `importedepreciado` | decimal(38,14) | YES |  |
| 101 | `descripcioncomprausos` | string | YES |  |
| 102 | `importepedidoservicios` | decimal(38,14) | YES |  |
| 103 | `nombrescedentes` | string | YES |  |
| 104 | `colorcompleto` | string | YES |  |
| 105 | `colorcompletoexterna` | string | YES |  |
| 106 | `tapiceriacompleta` | string | YES |  |
| 107 | `visualizarenstockcomprausos` | boolean | YES |  |
| 108 | `fechafactura` | timestamp | YES |  |
| 109 | `fechafabricacion` | timestamp | YES |  |
| 110 | `descripcionversion` | string | YES |  |
| 111 | `programasmarca` | string | YES |  |
| 112 | `idiventario` | bigint | YES |  |
| 113 | `fechaultimoinventario` | timestamp | YES |  |
| 114 | `documentosinventario` | smallint | YES |  |
| 115 | `documentosrespuestasinventario` | int | YES |  |
| 116 | `sitiomatricula` | string | YES |  |
| 117 | `fechaproximaitv` | timestamp | YES |  |
| 118 | `fechavencimientoseguro` | timestamp | YES |  |
| 119 | `ubicacionvo` | string | YES |  |
| 120 | `observacionubicacionvo` | string | YES |  |
| 121 | `idubicavno` | string | YES |  |

### spiga_dbmlc.spiga_comprasvehiculosvn

**Columnas:** 61

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | int | YES |  |
| 3 | `ano_periodo` | int | YES |  |
| 4 | `mes_periodo` | int | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `idempresas` | smallint | YES |  |
| 7 | `idcentros` | smallint | YES |  |
| 8 | `añoexpediente` | string | YES |  |
| 9 | `serieexpediente` | string | YES |  |
| 10 | `numexpediente` | int | YES |  |
| 11 | `comprasnumdet` | smallint | YES |  |
| 12 | `idvehiculos` | int | YES |  |
| 13 | `idcompratipos` | string | YES |  |
| 14 | `importecompra` | decimal(37,14) | YES |  |
| 15 | `idsecciones` | int | YES |  |
| 16 | `seriefactura` | string | YES |  |
| 17 | `numfactura` | string | YES |  |
| 18 | `añofactura` | string | YES |  |
| 19 | `fechafactura` | timestamp | YES |  |
| 20 | `baseimponible` | decimal(37,14) | YES |  |
| 21 | `fechaasiento` | timestamp | YES |  |
| 22 | `fecharegistrorunt` | timestamp | YES |  |
| 23 | `importeiva` | decimal(38,12) | YES |  |
| 24 | `descripcioncompratipos` | string | YES |  |
| 25 | `idmarcas` | smallint | YES |  |
| 26 | `idgamas` | smallint | YES |  |
| 27 | `codmodelo` | string | YES |  |
| 28 | `extmodelo` | string | YES |  |
| 29 | `añomodelo` | string | YES |  |
| 30 | `idversiones` | string | YES |  |
| 31 | `matricula` | string | YES |  |
| 32 | `vin` | string | YES |  |
| 33 | `nombremarca` | string | YES |  |
| 34 | `nombregama` | string | YES |  |
| 35 | `nombremodelo` | string | YES |  |
| 36 | `descripcionversiones` | string | YES |  |
| 37 | `descripcionsecciones` | string | YES |  |
| 38 | `idctabancaria` | smallint | YES |  |
| 39 | `descripcionctabancaria` | string | YES |  |
| 40 | `nombre` | string | YES |  |
| 41 | `monedaorigen` | string | YES |  |
| 42 | `idcomprausos` | string | YES |  |
| 43 | `codexternomodelo` | string | YES |  |
| 44 | `idincidenciatipos` | string | YES |  |
| 45 | `idtercerosactividadincidenciatipos` | int | YES |  |
| 46 | `idactividadincidenciatipos` | smallint | YES |  |
| 47 | `idactividadesdetincidenciatipos` | smallint | YES |  |
| 48 | `incidenciatiposdescripcion` | string | YES |  |
| 49 | `numproformafabrica` | string | YES |  |
| 50 | `idcompraestados` | string | YES |  |
| 51 | `idcomprasnumdet_abonado` | smallint | YES |  |
| 52 | `fechaalbaran` | timestamp | YES |  |
| 53 | `fechaasiento_albaran` | timestamp | YES |  |
| 54 | `seriealbaran` | string | YES |  |
| 55 | `numalbaran` | string | YES |  |
| 56 | `añoalbaran` | string | YES |  |
| 57 | `baseimponible_albaran` | decimal(18,4) | YES |  |
| 58 | `factorcambiomoneda_albaran` | decimal(18,4) | YES |  |
| 59 | `fecharecepcion` | timestamp | YES |  |
| 60 | `codproveedor` | int | YES |  |
| 61 | `proveedor` | string | YES |  |

### spiga_dbmlc.spiga_datosterceros

**Columnas:** 50

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | int | YES |  |
| 2 | `idconsecutivo` | int | YES |  |
| 3 | `ano_periodo` | int | YES |  |
| 4 | `mes_periodo` | int | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `pkfkempresas` | smallint | YES |  |
| 7 | `nombreempresa` | string | YES |  |
| 8 | `pkterceros` | int | YES |  |
| 9 | `fkpaises` | string | YES |  |
| 10 | `fkterceroclases` | int | YES |  |
| 11 | `nombreterceroclases` | string | YES |  |
| 12 | `nifcif` | string | YES |  |
| 13 | `nifcif_fechaexpedicion` | timestamp | YES |  |
| 14 | `nifcif_lugarexpedicion` | string | YES |  |
| 15 | `nombre` | string | YES |  |
| 16 | `apellido1` | string | YES |  |
| 17 | `apellido2` | string | YES |  |
| 18 | `nombrecomercial` | string | YES |  |
| 19 | `fechaalta` | timestamp | YES |  |
| 20 | `fechabaja` | timestamp | YES |  |
| 21 | `fkdocumentaciontipos` | int | YES |  |
| 22 | `descrpciondocumentaciontipos` | string | YES |  |
| 23 | `fknaturalezajuridicatipos` | string | YES |  |
| 24 | `descripcionnaturalezajuridicatipos` | string | YES |  |
| 25 | `tipocontribuyente` | string | YES |  |
| 26 | `descripciontipocontribuyente` | string | YES |  |
| 27 | `agenteretenedor` | boolean | YES |  |
| 28 | `fechatipocontribuyente` | timestamp | YES |  |
| 29 | `resolucion` | string | YES |  |
| 30 | `fkcodigospostales` | string | YES |  |
| 31 | `poblacion` | string | YES |  |
| 32 | `provincia` | string | YES |  |
| 33 | `fkprofesiones` | smallint | YES |  |
| 34 | `descripcionprofesiones` | string | YES |  |
| 35 | `fktercerocargos` | int | YES |  |
| 36 | `descripcionterceroscargos` | string | YES |  |
| 37 | `fkterceroformacionniveles` | int | YES |  |
| 38 | `descripcionterceroformacionniveles` | string | YES |  |
| 39 | `fechanacimiento` | timestamp | YES |  |
| 40 | `fechacarnet` | timestamp | YES |  |
| 41 | `fechacarnetcaducidad` | timestamp | YES |  |
| 42 | `numerohijos` | int | YES |  |
| 43 | `fkestadociviltipos` | string | YES |  |
| 44 | `descripcionestadociviltipos` | string | YES |  |
| 45 | `sexo` | string | YES |  |
| 46 | `fkactividadtipos` | string | YES |  |
| 47 | `descripcionactividadtipos` | string | YES |  |
| 48 | `claseconcepto` | string | YES |  |
| 49 | `numlicenciaconducir` | string | YES |  |
| 50 | `codpais` | smallint | YES |  |

### spiga_dbmlc.spiga_facturadosnoentregadosvn

**Columnas:** 153

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | integer | YES |  |
| 2 | `idconsecutivo` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | smallint | YES |  |
| 7 | `idcentros` | smallint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | integer | YES |  |
| 11 | `numventa` | smallint | YES |  |
| 12 | `fechaventa` | timestamp(3) | YES |  |
| 13 | `comisionagente` | decimal(32,14) | YES |  |
| 14 | `idpaisesexportacion` | varchar | YES |  |
| 15 | `a�oasientoentrega` | varchar | YES |  |
| 16 | `idasientosentrega` | integer | YES |  |
| 17 | `idmonedas` | smallint | YES |  |
| 18 | `factorcambiomoneda` | decimal(32,14) | YES |  |
| 19 | `fkterceros_agente` | integer | YES |  |
| 20 | `nombreagente` | varchar | YES |  |
| 21 | `seriefacturacompra` | varchar | YES |  |
| 22 | `numfacturacompra` | varchar | YES |  |
| 23 | `a�ofacturacompra` | varchar | YES |  |
| 24 | `fechafacturacompra` | timestamp(3) | YES |  |
| 25 | `idcompraestados` | varchar | YES |  |
| 26 | `descripcioncompraestados` | varchar | YES |  |
| 27 | `preciocompra` | decimal(32,14) | YES |  |
| 28 | `ventafinal` | integer | YES |  |
| 29 | `facturaprincipal` | varchar | YES |  |
| 30 | `fechafacturaprincipal` | timestamp(3) | YES |  |
| 31 | `terceroprincipal` | integer | YES |  |
| 32 | `nifcifprincipal` | varchar | YES |  |
| 33 | `perfilterceroprincipal` | varchar | YES |  |
| 34 | `nombreterceroprincipal` | varchar | YES |  |
| 35 | `direccionterceroprincipal` | varchar | YES |  |
| 36 | `codigopostalterceroprincipal` | varchar | YES |  |
| 37 | `idcodigospostalesterceroprincipal` | varchar | YES |  |
| 38 | `poblacionterceroprincipal` | varchar | YES |  |
| 39 | `provinciaterceroprincipal` | varchar | YES |  |
| 40 | `telefonoprincipalterceroprincipal` | varchar | YES |  |
| 41 | `telefonoparticularterceroprincipal` | varchar | YES |  |
| 42 | `telefonomovilterceroprincipal` | varchar | YES |  |
| 43 | `telefonotrabajoterceroprincipal` | varchar | YES |  |
| 44 | `facturasecundaria` | varchar | YES |  |
| 45 | `fechafacturasecundaria` | timestamp(3) | YES |  |
| 46 | `tercerosecundaria` | integer | YES |  |
| 47 | `nombretercerosecundaria` | varchar | YES |  |
| 48 | `direcciontercerosecundaria` | varchar | YES |  |
| 49 | `poblaciontercerosecundaria` | varchar | YES |  |
| 50 | `provinciatercerosecundaria` | varchar | YES |  |
| 51 | `fechamatriculacion` | timestamp(3) | YES |  |
| 52 | `fechadespacho` | timestamp(3) | YES |  |
| 53 | `vin` | varchar | YES |  |
| 54 | `matricula` | varchar | YES |  |
| 55 | `sitiomatricula` | varchar | YES |  |
| 56 | `numeromotor` | varchar | YES |  |
| 57 | `idmarcas` | smallint | YES |  |
| 58 | `nombremarca` | varchar | YES |  |
| 59 | `idgamas` | smallint | YES |  |
| 60 | `nombregama` | varchar | YES |  |
| 61 | `codmodelo` | varchar | YES |  |
| 62 | `extmodelo` | varchar | YES |  |
| 63 | `a�omodelo` | varchar | YES |  |
| 64 | `nombremodelo` | varchar | YES |  |
| 65 | `idempleados` | smallint | YES |  |
| 66 | `nombrevendedor` | varchar | YES |  |
| 67 | `idventatipos` | varchar | YES |  |
| 68 | `descripcionventatipos` | varchar | YES |  |
| 69 | `idcompratipos` | varchar | YES |  |
| 70 | `descripcioncompratipos` | varchar | YES |  |
| 71 | `idventamarcatipos` | varchar | YES |  |
| 72 | `descripcionventamarcatipos` | varchar | YES |  |
| 73 | `idventafinanciaciontipos` | varchar | YES |  |
| 74 | `descripcionventafinanciaciontipos` | varchar | YES |  |
| 75 | `idversiones` | varchar | YES |  |
| 76 | `descripcionversion` | varchar | YES |  |
| 77 | `baseimponible` | decimal(32,14) | YES |  |
| 78 | `baseexenta` | decimal(32,14) | YES |  |
| 79 | `impuestos` | decimal(32,14) | YES |  |
| 80 | `acondicionamiento` | decimal(32,14) | YES |  |
| 81 | `totalventa` | decimal(32,14) | YES |  |
| 82 | `diferencialanticipo` | decimal(32,14) | YES |  |
| 83 | `identradatipos` | varchar | YES |  |
| 84 | `provisiondegastosinternos` | decimal(32,14) | YES |  |
| 85 | `provisiondegastosexternos` | decimal(32,14) | YES |  |
| 86 | `descripcionentradatipos` | varchar | YES |  |
| 87 | `complemento2terceroprincipal` | varchar | YES |  |
| 88 | `idofertas` | smallint | YES |  |
| 89 | `fechaoferta` | timestamp(3) | YES |  |
| 90 | `nombrefinanciera` | varchar | YES |  |
| 91 | `apellido1financiera` | varchar | YES |  |
| 92 | `apellido2financiera` | varchar | YES |  |
| 93 | `nombreconductor` | varchar | YES |  |
| 94 | `apellido1conductor` | varchar | YES |  |
| 95 | `apellido2conductor` | varchar | YES |  |
| 96 | `idclientespotentradas` | smallint | YES |  |
| 97 | `nombrecentro` | varchar | YES |  |
| 98 | `idsecciones` | integer | YES |  |
| 99 | `nombreseccion` | varchar | YES |  |
| 100 | `idterceroscolaborador` | integer | YES |  |
| 101 | `nombrecolaborador` | varchar | YES |  |
| 102 | `detallaropcionalesfactura` | boolean | YES |  |
| 103 | `importevehiculoscambio` | decimal(32,14) | YES |  |
| 104 | `expedientesvehiculoscambio` | varchar | YES |  |
| 105 | `comision` | varchar | YES |  |
| 106 | `idcalletiposprincipal` | varchar | YES |  |
| 107 | `nombrecalleprincipal` | varchar | YES |  |
| 108 | `numeroprincipal` | varchar | YES |  |
| 109 | `bloqueprincipal` | varchar | YES |  |
| 110 | `pisoprincipal` | varchar | YES |  |
| 111 | `puertaprincipal` | varchar | YES |  |
| 112 | `poblacionprincipal` | varchar | YES |  |
| 113 | `provinciaprincipal` | varchar | YES |  |
| 114 | `idcodigospostalesprincipal` | varchar | YES |  |
| 115 | `fechaentregacliente` | timestamp(3) | YES |  |
| 116 | `versionfila` | smallint | YES |  |
| 117 | `idvehiculos` | integer | YES |  |
| 118 | `vnfechainiciogarantia` | varchar | YES |  |
| 119 | `mesesgarantiaobligatoriavn` | smallint | YES |  |
| 120 | `mesesgarantiaobligatoriavn_chapa` | smallint | YES |  |
| 121 | `mesesgarantiaobligatoriavn_pintura` | smallint | YES |  |
| 122 | `mesesgarantiaobligatoriavn_motor` | smallint | YES |  |
| 123 | `nombresecundario` | varchar | YES |  |
| 124 | `apellido1secundario` | varchar | YES |  |
| 125 | `apellido2secundario` | varchar | YES |  |
| 126 | `idempleadoscolaborador` | smallint | YES |  |
| 127 | `nombreempleadocolaborador` | varchar | YES |  |
| 128 | `nombrepropietario` | varchar | YES |  |
| 129 | `apellido1propietario` | varchar | YES |  |
| 130 | `apellido2propietario` | varchar | YES |  |
| 131 | `codexternomodelo` | varchar | YES |  |
| 132 | `ubicacion` | varchar | YES |  |
| 133 | `idnegociotipos` | varchar | YES |  |
| 134 | `importependientecobro` | decimal(32,14) | YES |  |
| 135 | `fechapazsalvo` | timestamp(3) | YES |  |
| 136 | `a�opazsalvo` | varchar | YES |  |
| 137 | `seriepazsalvo` | varchar | YES |  |
| 138 | `numpazsalvo` | integer | YES |  |
| 139 | `nombreempleadoemitepse` | varchar | YES |  |
| 140 | `apellido1empleadoemitepse` | varchar | YES |  |
| 141 | `apellido2empleadoemitepse` | varchar | YES |  |
| 142 | `idtercerosalquilador` | integer | YES |  |
| 143 | `nombrealquilador` | varchar | YES |  |
| 144 | `apellido1alquilador` | varchar | YES |  |
| 145 | `apellido2alquilador` | varchar | YES |  |
| 146 | `detallaropcionalesconcesionfactura` | boolean | YES |  |
| 147 | `detallarcampa�asfactura` | boolean | YES |  |
| 148 | `idseriestransporte` | varchar | YES |  |
| 149 | `idnumtransporte` | integer | YES |  |
| 150 | `obsinternas` | varchar | YES |  |
| 151 | `nifcifvendedor` | varchar | YES |  |
| 152 | `margenventaimportador` | decimal(32,14) | YES |  |
| 153 | `fecharecepcion` | timestamp(3) | YES |  |

### spiga_dbmlc.spiga_facturadosnoentregadosvo

**Columnas:** 137

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | integer | YES |  |
| 2 | `idconsecutivo` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | smallint | YES |  |
| 7 | `idcentros` | smallint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | integer | YES |  |
| 11 | `numventa` | smallint | YES |  |
| 12 | `fechaventa` | timestamp(3) | YES |  |
| 13 | `kms` | integer | YES |  |
| 14 | `idtercerosfinanciera` | integer | YES |  |
| 15 | `nombrefinanciera` | varchar | YES |  |
| 16 | `idterceroscolaborador` | integer | YES |  |
| 17 | `nombrecolaborador` | varchar | YES |  |
| 18 | `preciocompra` | decimal(32,14) | YES |  |
| 19 | `pkcompraestados` | varchar | YES |  |
| 20 | `descripcioncompraestados` | varchar | YES |  |
| 21 | `ventafinal` | integer | YES |  |
| 22 | `nombreproveedor` | varchar | YES |  |
| 23 | `facturacompra` | varchar | YES |  |
| 24 | `facturaprincipal` | varchar | YES |  |
| 25 | `terceroprincipal` | integer | YES |  |
| 26 | `nifcifprincipal` | varchar | YES |  |
| 27 | `perfilterceroprincipal` | varchar | YES |  |
| 28 | `nombreterceroprincipal` | varchar | YES |  |
| 29 | `direccionterceroprincipal` | varchar | YES |  |
| 30 | `codigopostalterceroprincipal` | varchar | YES |  |
| 31 | `idcodigospostalesterceroprincipal` | varchar | YES |  |
| 32 | `poblacionterceroprincipal` | varchar | YES |  |
| 33 | `provinciaterceroprincipal` | varchar | YES |  |
| 34 | `clientecategoriaterceroprincipal` | varchar | YES |  |
| 35 | `telefonoprincipalterceroprincipal` | varchar | YES |  |
| 36 | `telefonoparticularterceroprincipal` | varchar | YES |  |
| 37 | `telefonomovilterceroprincipal` | varchar | YES |  |
| 38 | `telefonotrabajoterceroprincipal` | varchar | YES |  |
| 39 | `facturasecundaria` | varchar | YES |  |
| 40 | `tercerosecundaria` | integer | YES |  |
| 41 | `nombretercerosecundaria` | varchar | YES |  |
| 42 | `direcciontercerosecundaria` | varchar | YES |  |
| 43 | `codigopostaltercerosecundaria` | varchar | YES |  |
| 44 | `idcodigospostalestercerosecundaria` | varchar | YES |  |
| 45 | `poblaciontercerosecundaria` | varchar | YES |  |
| 46 | `provinciatercerosecundaria` | varchar | YES |  |
| 47 | `telefonoprincipaltercerosecundaria` | varchar | YES |  |
| 48 | `telefonoparticulartercerosecundaria` | varchar | YES |  |
| 49 | `telefonomoviltercerosecundaria` | varchar | YES |  |
| 50 | `telefonotrabajotercerosecundaria` | varchar | YES |  |
| 51 | `fechamatriculacion` | timestamp(3) | YES |  |
| 52 | `fechadespacho` | timestamp(3) | YES |  |
| 53 | `vin` | varchar | YES |  |
| 54 | `matricula` | varchar | YES |  |
| 55 | `numeromotor` | varchar | YES |  |
| 56 | `idmarcas` | smallint | YES |  |
| 57 | `nombremarca` | varchar | YES |  |
| 58 | `idgamas` | smallint | YES |  |
| 59 | `nombregama` | varchar | YES |  |
| 60 | `codmodelo` | varchar | YES |  |
| 61 | `extmodelo` | varchar | YES |  |
| 62 | `a�omodelo` | varchar | YES |  |
| 63 | `nombremodelo` | varchar | YES |  |
| 64 | `idempleados` | smallint | YES |  |
| 65 | `nombrevendedor` | varchar | YES |  |
| 66 | `idventatipos` | varchar | YES |  |
| 67 | `descripcionventatipos` | varchar | YES |  |
| 68 | `idcompratipos` | varchar | YES |  |
| 69 | `descripcioncompratipos` | varchar | YES |  |
| 70 | `idversiones` | varchar | YES |  |
| 71 | `descripcionversion` | varchar | YES |  |
| 72 | `idventainternatipos` | varchar | YES |  |
| 73 | `descripcionventainternatipos` | varchar | YES |  |
| 74 | `baseimponible` | decimal(32,14) | YES |  |
| 75 | `baseexenta` | decimal(32,14) | YES |  |
| 76 | `importesuplidosgestoria` | decimal(32,14) | YES |  |
| 77 | `importeprovision` | decimal(32,14) | YES |  |
| 78 | `diferencialanticipo` | decimal(32,14) | YES |  |
| 79 | `baseexentaventa` | decimal(32,14) | YES |  |
| 80 | `importeimpuestoventa` | decimal(32,14) | YES |  |
| 81 | `importegastos` | decimal(32,14) | YES |  |
| 82 | `codigoagente` | varchar | YES |  |
| 83 | `expedientecambio` | varchar | YES |  |
| 84 | `esacambio` | integer | YES |  |
| 85 | `idofertas` | smallint | YES |  |
| 86 | `fechaoferta` | timestamp(3) | YES |  |
| 87 | `localidadterceroprincipal` | varchar | YES |  |
| 88 | `complemento2terceroprincipal` | varchar | YES |  |
| 89 | `nombreconductor` | varchar | YES |  |
| 90 | `apellido1conductor` | varchar | YES |  |
| 91 | `apellido2conductor` | varchar | YES |  |
| 92 | `idclientespotentradasoferta` | smallint | YES |  |
| 93 | `nombrecentro` | varchar | YES |  |
| 94 | `comisioncolaborador` | decimal(32,14) | YES |  |
| 95 | `idsecciones` | integer | YES |  |
| 96 | `nombreseccion` | varchar | YES |  |
| 97 | `diasantiguedadstock` | integer | YES |  |
| 98 | `mesesantiguedadstock` | integer | YES |  |
| 99 | `precioventarecomendado` | decimal(32,14) | YES |  |
| 100 | `expedientesvehiculoscambio` | varchar | YES |  |
| 101 | `importevehiculoscambio` | decimal(32,14) | YES |  |
| 102 | `comision` | varchar | YES |  |
| 103 | `idcalletiposprincipal` | varchar | YES |  |
| 104 | `nombrecalleprincipal` | varchar | YES |  |
| 105 | `numeroprincipal` | varchar | YES |  |
| 106 | `bloqueprincipal` | varchar | YES |  |
| 107 | `pisoprincipal` | varchar | YES |  |
| 108 | `puertaprincipal` | varchar | YES |  |
| 109 | `poblacionprincipal` | varchar | YES |  |
| 110 | `provinciaprincipal` | varchar | YES |  |
| 111 | `idcodigospostalesprincipal` | varchar | YES |  |
| 112 | `fechaentregacliente` | timestamp(3) | YES |  |
| 113 | `fechapazsalvo` | timestamp(3) | YES |  |
| 114 | `a�opazsalvo` | varchar | YES |  |
| 115 | `seriepazsalvo` | varchar | YES |  |
| 116 | `numpazsalvo` | integer | YES |  |
| 117 | `nombreempleadoemitepse` | varchar | YES |  |
| 118 | `apellido1empleadoemitepse` | varchar | YES |  |
| 119 | `apellido2empleadoemitepse` | varchar | YES |  |
| 120 | `nombresecundario` | varchar | YES |  |
| 121 | `apellido1secundario` | varchar | YES |  |
| 122 | `apellido2secundario` | varchar | YES |  |
| 123 | `idempleadoscolaborador` | smallint | YES |  |
| 124 | `nombreempleadocolaborador` | varchar | YES |  |
| 125 | `nombrepropietario` | varchar | YES |  |
| 126 | `apellido1propietario` | varchar | YES |  |
| 127 | `apellido2propietario` | varchar | YES |  |
| 128 | `totalventa` | decimal(32,14) | YES |  |
| 129 | `impuestos` | decimal(32,14) | YES |  |
| 130 | `codexternomodelo` | varchar | YES |  |
| 131 | `ubicacion` | varchar | YES |  |
| 132 | `idnegociotipos` | varchar | YES |  |
| 133 | `importependientecobro` | decimal(32,14) | YES |  |
| 134 | `nifcifvendedor` | varchar | YES |  |
| 135 | `obsinternas` | varchar | YES |  |
| 136 | `fechafacturacompra` | timestamp(3) | YES |  |
| 137 | `fechafacturaprincipal` | timestamp(3) | YES |  |

### spiga_dbmlc.spiga_gastosvehiculosvo

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | integer | YES |  |
| 2 | `idconsecutivo` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `vin` | varchar | YES |  |
| 7 | `gis` | decimal(18,4) | YES |  |
| 8 | `gnis` | decimal(18,4) | YES |  |

### spiga_dbmlc.spiga_inventariovn

**Columnas:** 70

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | int | YES |  |
| 2 | `idconsecutivo` | int | YES |  |
| 3 | `ano_periodo` | int | YES |  |
| 4 | `mes_periodo` | int | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `idempresas` | smallint | YES |  |
| 7 | `idcentros` | smallint | YES |  |
| 8 | `añoexpediente` | string | YES |  |
| 9 | `serieexpediente` | string | YES |  |
| 10 | `numexpediente` | int | YES |  |
| 11 | `comprasnumdet` | smallint | YES |  |
| 12 | `vin` | string | YES |  |
| 13 | `matricula` | string | YES |  |
| 14 | `comision` | string | YES |  |
| 15 | `idsecciones` | int | YES |  |
| 16 | `fkcompratipos` | string | YES |  |
| 17 | `nombreempresa` | string | YES |  |
| 18 | `nombrecentro` | string | YES |  |
| 19 | `descripcionseccion` | string | YES |  |
| 20 | `descripciontipocompra` | string | YES |  |
| 21 | `descripciontipocombustible` | string | YES |  |
| 22 | `idmarcas` | smallint | YES |  |
| 23 | `idgamas` | smallint | YES |  |
| 24 | `codmodelo` | string | YES |  |
| 25 | `extmodelo` | string | YES |  |
| 26 | `añomodelo` | string | YES |  |
| 27 | `nombremarca` | string | YES |  |
| 28 | `nombregama` | string | YES |  |
| 29 | `nombremodelo` | string | YES |  |
| 30 | `añofactura` | string | YES |  |
| 31 | `seriefactura` | string | YES |  |
| 32 | `numfactura` | string | YES |  |
| 33 | `fechafactura` | timestamp | YES |  |
| 34 | `idcompraestados` | string | YES |  |
| 35 | `añoalbaran` | string | YES |  |
| 36 | `seriealbaran` | string | YES |  |
| 37 | `numalbaran` | string | YES |  |
| 38 | `fechaalbaran` | timestamp | YES |  |
| 39 | `descripcionestadocompra` | string | YES |  |
| 40 | `color` | string | YES |  |
| 41 | `tapiceria` | string | YES |  |
| 42 | `ultimaubicacionvn` | string | YES |  |
| 43 | `ubicacionvnfechainventario` | string | YES |  |
| 44 | `baseimponiblecompra` | decimal(32,14) | YES |  |
| 45 | `gastosaumentanstock` | decimal(32,14) | YES |  |
| 46 | `gastosnoaumentanstock` | decimal(32,14) | YES |  |
| 47 | `gastospendientesaumentanstock` | decimal(32,14) | YES |  |
| 48 | `gastospendientesnoaumentanstock` | decimal(32,14) | YES |  |
| 49 | `totalgastoscontravalor` | decimal(32,14) | YES |  |
| 50 | `baseimponiblecompracontravalor` | decimal(32,14) | YES |  |
| 51 | `descripcioncompraestados` | string | YES |  |
| 52 | `dtoimporte` | decimal(32,14) | YES |  |
| 53 | `importereclamado` | decimal(32,14) | YES |  |
| 54 | `pedidossinasignaraumentastock` | decimal(32,14) | YES |  |
| 55 | `usodestino` | string | YES |  |
| 56 | `idversiones` | string | YES |  |
| 57 | `idincidenciatipos` | string | YES |  |
| 58 | `idtercerosactividadincidenciatipos` | int | YES |  |
| 59 | `idactividadincidenciatipos` | smallint | YES |  |
| 60 | `idactividadesdetincidenciatipos` | smallint | YES |  |
| 61 | `incidenciatiposdescripcion` | string | YES |  |
| 62 | `descripcionversion` | string | YES |  |
| 63 | `idcategoriagamatipos` | string | YES |  |
| 64 | `numeromotor` | string | YES |  |
| 65 | `numhomologacion` | string | YES |  |
| 66 | `fecha` | timestamp | YES |  |
| 67 | `numdeclaracion` | string | YES |  |
| 68 | `fechalevante` | timestamp | YES |  |
| 69 | `numlevante` | string | YES |  |
| 70 | `observaciones_compra` | string | YES |  |

### spiga_dbmlc.spiga_inventariovo

**Columnas:** 58

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | int | YES |  |
| 2 | `idconsecutivo` | int | YES |  |
| 3 | `ano_periodo` | int | YES |  |
| 4 | `mes_periodo` | int | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `idempresas` | smallint | YES |  |
| 7 | `idcentros` | smallint | YES |  |
| 8 | `añoexpediente` | string | YES |  |
| 9 | `serieexpediente` | string | YES |  |
| 10 | `numexpediente` | int | YES |  |
| 11 | `comprasnumdet` | smallint | YES |  |
| 12 | `fechadepreciar` | timestamp | YES |  |
| 13 | `vin` | string | YES |  |
| 14 | `matricula` | string | YES |  |
| 15 | `idsecciones` | int | YES |  |
| 16 | `idcompratipos` | string | YES |  |
| 17 | `idregistrotipos` | string | YES |  |
| 18 | `fechaasiento` | timestamp | YES |  |
| 19 | `idcomprainternatipos` | string | YES |  |
| 20 | `descripcioncomprainternatipo` | string | YES |  |
| 21 | `nombreempresa` | string | YES |  |
| 22 | `nombrecentro` | string | YES |  |
| 23 | `descripcionseccion` | string | YES |  |
| 24 | `descripciontipocompra` | string | YES |  |
| 25 | `descripciontipocombustible` | string | YES |  |
| 26 | `tipocomprainmovilizado` | boolean | YES |  |
| 27 | `idmarcas` | smallint | YES |  |
| 28 | `idgamas` | smallint | YES |  |
| 29 | `codmodelo` | string | YES |  |
| 30 | `extmodelo` | string | YES |  |
| 31 | `añomodelo` | string | YES |  |
| 32 | `nombremarca` | string | YES |  |
| 33 | `nombregama` | string | YES |  |
| 34 | `idcompraestados` | string | YES |  |
| 35 | `nombremodelo` | string | YES |  |
| 36 | `añofactura` | string | YES |  |
| 37 | `seriefactura` | string | YES |  |
| 38 | `numfactura` | string | YES |  |
| 39 | `fechafactura` | timestamp | YES |  |
| 40 | `descripcioncompraestados` | string | YES |  |
| 41 | `ultimaubicacionvn` | string | YES |  |
| 42 | `ubicacionvnfechainventario` | string | YES |  |
| 43 | `color` | string | YES |  |
| 44 | `tapiceria` | string | YES |  |
| 45 | `baseimponiblecompra` | decimal(32,14) | YES |  |
| 46 | `depreciacioncompra` | decimal(32,14) | YES |  |
| 47 | `compra576` | decimal(32,14) | YES |  |
| 48 | `exentos` | decimal(32,14) | YES |  |
| 49 | `gastosaumentanstock` | decimal(32,14) | YES |  |
| 50 | `gastosnoaumentanstock` | decimal(32,14) | YES |  |
| 51 | `gastospendientesaumentanstock` | decimal(32,14) | YES |  |
| 52 | `gastospendientesnoaumentanstock` | decimal(32,14) | YES |  |
| 53 | `totalgastoscontravalor` | decimal(32,14) | YES |  |
| 54 | `importecompracontravalor` | decimal(32,14) | YES |  |
| 55 | `pedidossinasignaraumentastock` | decimal(32,14) | YES |  |
| 56 | `usodestino` | string | YES |  |
| 57 | `importetotaldepreciado` | decimal(32,14) | YES |  |
| 58 | `observaciones_compra` | string | YES |  |

### spiga_dbmlc.spiga_rentabilidaddetalladavehiculosnuevos

**Columnas:** 52

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | integer | YES |  |
| 2 | `idconsecutivo` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | smallint | YES |  |
| 7 | `a�oexpediente` | varchar | YES |  |
| 8 | `serieexpediente` | varchar | YES |  |
| 9 | `numexpediente` | integer | YES |  |
| 10 | `numventa` | smallint | YES |  |
| 11 | `idventasabonado` | smallint | YES |  |
| 12 | `nombrecentro` | varchar | YES |  |
| 13 | `seccion` | varchar | YES |  |
| 14 | `marca` | varchar | YES |  |
| 15 | `gama` | varchar | YES |  |
| 16 | `codmodelo` | varchar | YES |  |
| 17 | `modelo` | varchar | YES |  |
| 18 | `vin` | varchar | YES |  |
| 19 | `tipocompra` | varchar | YES |  |
| 20 | `idterceroscompra` | integer | YES |  |
| 21 | `nombretercerocompra` | varchar | YES |  |
| 22 | `apellido1tercerocompra` | varchar | YES |  |
| 23 | `apellido2tercerocompra` | varchar | YES |  |
| 24 | `fechafacturacompra` | timestamp(3) | YES |  |
| 25 | `seriefacturacompra` | varchar | YES |  |
| 26 | `numfacturacompra` | varchar | YES |  |
| 27 | `a�ofacturacompra` | varchar | YES |  |
| 28 | `diasstock` | integer | YES |  |
| 29 | `tipoventa` | varchar | YES |  |
| 30 | `fechaventa` | timestamp(3) | YES |  |
| 31 | `seriefacturaventa` | varchar | YES |  |
| 32 | `numfacturaventa` | varchar | YES |  |
| 33 | `a�ofacturaventa` | varchar | YES |  |
| 34 | `nombrevendedor` | varchar | YES |  |
| 35 | `apellido1vendedor` | varchar | YES |  |
| 36 | `apellido2vendedor` | varchar | YES |  |
| 37 | `importecompra` | decimal(38,14) | YES |  |
| 38 | `importegasto` | decimal(38,13) | YES |  |
| 39 | `idcompragastoadicionaltipos` | varchar | YES |  |
| 40 | `idcompragastoadicionaltiposdescripcion` | varchar | YES |  |
| 41 | `otroscargos` | decimal(38,19) | YES |  |
| 42 | `otrosingresos` | decimal(38,19) | YES |  |
| 43 | `importeventa` | decimal(38,6) | YES |  |
| 44 | `importeseguros` | decimal(38,14) | YES |  |
| 45 | `importegarantias` | decimal(38,14) | YES |  |
| 46 | `importematriculacion` | decimal(38,14) | YES |  |
| 47 | `importetransferencia` | decimal(38,14) | YES |  |
| 48 | `importecampa�as` | decimal(38,14) | YES |  |
| 49 | `importeprestamo` | decimal(38,4) | YES |  |
| 50 | `matricula` | varchar | YES |  |
| 51 | `fechaabono` | timestamp(3) | YES |  |
| 52 | `fechamatriculacion` | timestamp(3) | YES |  |

### spiga_dbmlc.spiga_rentabilidaddetalladavehiculosusados

**Columnas:** 51

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | integer | YES |  |
| 2 | `idconsecutivo` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | smallint | YES |  |
| 7 | `serieexpediente` | varchar | YES |  |
| 8 | `numexpediente` | integer | YES |  |
| 9 | `a�oexpediente` | varchar | YES |  |
| 10 | `numventa` | smallint | YES |  |
| 11 | `idventasabonado` | smallint | YES |  |
| 12 | `nombrecentro` | varchar | YES |  |
| 13 | `seccion` | varchar | YES |  |
| 14 | `marca` | varchar | YES |  |
| 15 | `gama` | varchar | YES |  |
| 16 | `codmodelo` | varchar | YES |  |
| 17 | `modelo` | varchar | YES |  |
| 18 | `vin` | varchar | YES |  |
| 19 | `tipocompra` | varchar | YES |  |
| 20 | `idterceroscompra` | integer | YES |  |
| 21 | `nombretercerocompra` | varchar | YES |  |
| 22 | `apellido1tercerocompra` | varchar | YES |  |
| 23 | `apellido2tercerocompra` | varchar | YES |  |
| 24 | `fechafacturacompra` | timestamp(3) | YES |  |
| 25 | `seriefacturacompra` | varchar | YES |  |
| 26 | `numfacturacompra` | varchar | YES |  |
| 27 | `a�ofacturacompra` | varchar | YES |  |
| 28 | `diasstock` | integer | YES |  |
| 29 | `tipoventa` | varchar | YES |  |
| 30 | `fechaventa` | timestamp(3) | YES |  |
| 31 | `seriefacturaventa` | varchar | YES |  |
| 32 | `numfacturaventa` | varchar | YES |  |
| 33 | `a�ofacturaventa` | varchar | YES |  |
| 34 | `nombrevendedor` | varchar | YES |  |
| 35 | `apellido1vendedor` | varchar | YES |  |
| 36 | `apellido2vendedor` | varchar | YES |  |
| 37 | `importecompra` | decimal(38,14) | YES |  |
| 38 | `importegasto` | decimal(38,13) | YES |  |
| 39 | `idcompragastoadicionaltipos` | varchar | YES |  |
| 40 | `idcompragastoadicionaltiposdescripcion` | varchar | YES |  |
| 41 | `otroscargos` | decimal(38,19) | YES |  |
| 42 | `otrosingresos` | decimal(38,19) | YES |  |
| 43 | `importeventa` | decimal(29,4) | YES |  |
| 44 | `importeseguros` | decimal(18,4) | YES |  |
| 45 | `importegarantias` | decimal(18,4) | YES |  |
| 46 | `importematriculacion` | decimal(18,4) | YES |  |
| 47 | `importetransferencia` | decimal(18,4) | YES |  |
| 48 | `importeprestamo` | decimal(38,4) | YES |  |
| 49 | `matricula` | varchar | YES |  |
| 50 | `fechaabono` | timestamp(3) | YES |  |
| 51 | `importeprovisionadogarantias` | decimal(18,4) | YES |  |

### spiga_dbmlc.spiga_terceros

**Columnas:** 70

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | int | YES |  |
| 2 | `idconsecutivo` | int | YES |  |
| 3 | `ano_periodo` | int | YES |  |
| 4 | `mes_periodo` | int | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `pkterceros` | int | YES |  |
| 7 | `fkpaises` | string | YES |  |
| 8 | `fkterceroclases` | int | YES |  |
| 9 | `fktratamientos` | int | YES |  |
| 10 | `nifcif` | string | YES |  |
| 11 | `nombre` | string | YES |  |
| 12 | `apellido1` | string | YES |  |
| 13 | `apellido2` | string | YES |  |
| 14 | `nombrecomercial` | string | YES |  |
| 15 | `empresatrabajo` | string | YES |  |
| 16 | `fkprofesiones` | smallint | YES |  |
| 17 | `fktercerocargos` | int | YES |  |
| 18 | `fkterceroformacionniveles` | int | YES |  |
| 19 | `fechanacimiento` | timestamp | YES |  |
| 20 | `fechasanto` | string | YES |  |
| 21 | `fechacarnet` | timestamp | YES |  |
| 22 | `numerohijos` | int | YES |  |
| 23 | `facturaracliente` | boolean | YES |  |
| 24 | `numeroautorizacion` | boolean | YES |  |
| 25 | `numerosiniestro` | boolean | YES |  |
| 26 | `fechaalta` | timestamp | YES |  |
| 27 | `fechabaja` | timestamp | YES |  |
| 28 | `usermod` | smallint | YES |  |
| 29 | `hostmod` | string | YES |  |
| 30 | `versionfila` | int | YES |  |
| 31 | `fkdocumentaciontipos` | int | YES |  |
| 32 | `fkestadociviltipos` | string | YES |  |
| 33 | `fechamod` | timestamp | YES |  |
| 34 | `sexo` | string | YES |  |
| 35 | `fknaturalezajuridicatipos` | string | YES |  |
| 36 | `numeroempleados` | smallint | YES |  |
| 37 | `añoconstitucion` | string | YES |  |
| 38 | `cifradenegocio` | int | YES |  |
| 39 | `fkactividadtipos` | string | YES |  |
| 40 | `solvencia` | boolean | YES |  |
| 41 | `codigosociedad` | string | YES |  |
| 42 | `robinson` | boolean | YES |  |
| 43 | `numlicenciaconducir` | string | YES |  |
| 44 | `billeteidentidad` | string | YES |  |
| 45 | `tipocontribuyente` | string | YES |  |
| 46 | `retenerdesdecero` | boolean | YES |  |
| 47 | `agenteretenedor` | boolean | YES |  |
| 48 | `robinsonant` | boolean | YES |  |
| 49 | `fechamodrobinson` | timestamp | YES |  |
| 50 | `fkcausabajatercero` | smallint | YES |  |
| 51 | `notieneemail` | boolean | YES |  |
| 52 | `centrocoste` | string | YES |  |
| 53 | `fechacarnetcaducidad` | timestamp | YES |  |
| 54 | `norealizaasientodiferenciacambial` | boolean | YES |  |
| 55 | `norealizaasientoconversion` | boolean | YES |  |
| 56 | `fknivelesriesgo` | int | YES |  |
| 57 | `fechatipocontribuyente` | timestamp | YES |  |
| 58 | `resolucion` | string | YES |  |
| 59 | `cuentabanconacion` | string | YES |  |
| 60 | `admitesepab2b` | boolean | YES |  |
| 61 | `requieresureferenciare` | boolean | YES |  |
| 62 | `nifcif_fechaexpedicion` | timestamp | YES |  |
| 63 | `nifcif_lugarexpedicion` | string | YES |  |
| 64 | `nifcif_fechacaducidad` | timestamp | YES |  |
| 65 | `licenciaconducir_lugarexpedicion` | string | YES |  |
| 66 | `fkdeudortipos` | string | YES |  |
| 67 | `fkpaises_documentaciontipos` | string | YES |  |
| 68 | `fcnegociado` | boolean | YES |  |
| 69 | `web` | string | YES |  |
| 70 | `envioficherosfecomprimidos` | boolean | YES |  |

### spiga_dbmlc.spiga_terceros_peru

**Columnas:** 70

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | integer | YES |  |
| 2 | `idconsecutivo` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `pkterceros` | integer | YES |  |
| 7 | `fkpaises` | varchar | YES |  |
| 8 | `fkterceroclases` | integer | YES |  |
| 9 | `fktratamientos` | integer | YES |  |
| 10 | `nifcif` | varchar | YES |  |
| 11 | `nombre` | varchar | YES |  |
| 12 | `apellido1` | varchar | YES |  |
| 13 | `apellido2` | varchar | YES |  |
| 14 | `nombrecomercial` | varchar | YES |  |
| 15 | `empresatrabajo` | varchar | YES |  |
| 16 | `fkprofesiones` | smallint | YES |  |
| 17 | `fktercerocargos` | integer | YES |  |
| 18 | `fkterceroformacionniveles` | integer | YES |  |
| 19 | `fechanacimiento` | timestamp(3) | YES |  |
| 20 | `fechasanto` | varchar | YES |  |
| 21 | `fechacarnet` | timestamp(3) | YES |  |
| 22 | `numerohijos` | integer | YES |  |
| 23 | `facturaracliente` | boolean | YES |  |
| 24 | `numeroautorizacion` | boolean | YES |  |
| 25 | `numerosiniestro` | boolean | YES |  |
| 26 | `fechaalta` | timestamp(3) | YES |  |
| 27 | `fechabaja` | timestamp(3) | YES |  |
| 28 | `usermod` | smallint | YES |  |
| 29 | `hostmod` | varchar | YES |  |
| 30 | `versionfila` | integer | YES |  |
| 31 | `fkdocumentaciontipos` | integer | YES |  |
| 32 | `fkestadociviltipos` | varchar | YES |  |
| 33 | `fechamod` | timestamp(3) | YES |  |
| 34 | `sexo` | varchar | YES |  |
| 35 | `fknaturalezajuridicatipos` | varchar | YES |  |
| 36 | `numeroempleados` | smallint | YES |  |
| 37 | `a�oconstitucion` | varchar | YES |  |
| 38 | `cifradenegocio` | integer | YES |  |
| 39 | `fkactividadtipos` | varchar | YES |  |
| 40 | `solvencia` | boolean | YES |  |
| 41 | `codigosociedad` | varchar | YES |  |
| 42 | `robinson` | boolean | YES |  |
| 43 | `numlicenciaconducir` | varchar | YES |  |
| 44 | `billeteidentidad` | varchar | YES |  |
| 45 | `tipocontribuyente` | varchar | YES |  |
| 46 | `retenerdesdecero` | boolean | YES |  |
| 47 | `agenteretenedor` | boolean | YES |  |
| 48 | `robinsonant` | boolean | YES |  |
| 49 | `fechamodrobinson` | timestamp(3) | YES |  |
| 50 | `fkcausabajatercero` | smallint | YES |  |
| 51 | `notieneemail` | boolean | YES |  |
| 52 | `centrocoste` | varchar | YES |  |
| 53 | `fechacarnetcaducidad` | timestamp(3) | YES |  |
| 54 | `norealizaasientodiferenciacambial` | boolean | YES |  |
| 55 | `norealizaasientoconversion` | boolean | YES |  |
| 56 | `fknivelesriesgo` | integer | YES |  |
| 57 | `fechatipocontribuyente` | timestamp(3) | YES |  |
| 58 | `resolucion` | varchar | YES |  |
| 59 | `cuentabanconacion` | varchar | YES |  |
| 60 | `admitesepab2b` | boolean | YES |  |
| 61 | `requieresureferenciare` | boolean | YES |  |
| 62 | `nifcif_fechaexpedicion` | timestamp(3) | YES |  |
| 63 | `nifcif_lugarexpedicion` | varchar | YES |  |
| 64 | `nifcif_fechacaducidad` | timestamp(3) | YES |  |
| 65 | `licenciaconducir_lugarexpedicion` | varchar | YES |  |
| 66 | `fkdeudortipos` | varchar | YES |  |
| 67 | `fkpaises_documentaciontipos` | varchar | YES |  |
| 68 | `fcnegociado` | boolean | YES |  |
| 69 | `web` | varchar | YES |  |
| 70 | `envioficherosfecomprimidos` | boolean | YES |  |

### spiga_dbmlc.spiga_terceroscorreos

**Columnas:** 18

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | int | YES |  |
| 2 | `idconsecutivo` | int | YES |  |
| 3 | `ano_periodo` | int | YES |  |
| 4 | `mes_periodo` | int | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `pkfkterceros` | int | YES |  |
| 7 | `pkterceroemails_iden` | smallint | YES |  |
| 8 | `fkemailtipos` | int | YES |  |
| 9 | `email` | string | YES |  |
| 10 | `fktercerodirecciones` | smallint | YES |  |
| 11 | `fechabaja` | timestamp | YES |  |
| 12 | `usermod` | smallint | YES |  |
| 13 | `hostmod` | string | YES |  |
| 14 | `versionfila` | int | YES |  |
| 15 | `direccionpadre` | boolean | YES |  |
| 16 | `principal` | boolean | YES |  |
| 17 | `fechamod` | timestamp | YES |  |
| 18 | `fkterceros_direcciones` | int | YES |  |

### spiga_dbmlc.spiga_terceroscorreos_peru

**Columnas:** 18

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | integer | YES |  |
| 2 | `idconsecutivo` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `pkfkterceros` | integer | YES |  |
| 7 | `pkterceroemails_iden` | smallint | YES |  |
| 8 | `fkemailtipos` | integer | YES |  |
| 9 | `email` | varchar | YES |  |
| 10 | `fktercerodirecciones` | smallint | YES |  |
| 11 | `fechabaja` | timestamp(3) | YES |  |
| 12 | `usermod` | smallint | YES |  |
| 13 | `hostmod` | varchar | YES |  |
| 14 | `versionfila` | integer | YES |  |
| 15 | `direccionpadre` | boolean | YES |  |
| 16 | `principal` | boolean | YES |  |
| 17 | `fechamod` | timestamp(3) | YES |  |
| 18 | `fkterceros_direcciones` | integer | YES |  |

### spiga_dbmlc.spiga_tercerosdirecciones_peru

**Columnas:** 29

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | integer | YES |  |
| 2 | `idconsecutivo` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `pkfkterceros` | integer | YES |  |
| 7 | `pktercerodirecciones_iden` | smallint | YES |  |
| 8 | `fkdirecciontipos` | integer | YES |  |
| 9 | `fkcalletipos` | varchar | YES |  |
| 10 | `nombrecalle` | varchar | YES |  |
| 11 | `numero` | varchar | YES |  |
| 12 | `bloque` | varchar | YES |  |
| 13 | `piso` | varchar | YES |  |
| 14 | `puerta` | varchar | YES |  |
| 15 | `complemento` | varchar | YES |  |
| 16 | `fkpaises` | varchar | YES |  |
| 17 | `fkcodigospostales` | varchar | YES |  |
| 18 | `poblacion` | varchar | YES |  |
| 19 | `provincia` | varchar | YES |  |
| 20 | `fechabaja` | timestamp(3) | YES |  |
| 21 | `usermod` | smallint | YES |  |
| 22 | `hostmod` | varchar | YES |  |
| 23 | `versionfila` | integer | YES |  |
| 24 | `principal` | boolean | YES |  |
| 25 | `fkestados` | varchar | YES |  |
| 26 | `fkprovincias` | varchar | YES |  |
| 27 | `complemento2` | varchar | YES |  |
| 28 | `fechamod` | timestamp(3) | YES |  |
| 29 | `fkpoblaciones` | integer | YES |  |

### spiga_dbmlc.spiga_tercerostelefonos

**Columnas:** 22

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | int | YES |  |
| 2 | `idconsecutivo` | int | YES |  |
| 3 | `ano_periodo` | int | YES |  |
| 4 | `mes_periodo` | int | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `pkfkterceros` | int | YES |  |
| 7 | `pktercerotelefonos_iden` | smallint | YES |  |
| 8 | `fktelefonotipos` | int | YES |  |
| 9 | `codigotelefonico` | string | YES |  |
| 10 | `numero` | string | YES |  |
| 11 | `extension` | string | YES |  |
| 12 | `fktercerodirecciones` | smallint | YES |  |
| 13 | `direccionpadre` | boolean | YES |  |
| 14 | `horario` | string | YES |  |
| 15 | `fechabaja` | timestamp | YES |  |
| 16 | `usermod` | smallint | YES |  |
| 17 | `hostmod` | string | YES |  |
| 18 | `versionfila` | int | YES |  |
| 19 | `principal` | boolean | YES |  |
| 20 | `fechamod` | timestamp | YES |  |
| 21 | `fkterceros_direcciones` | int | YES |  |
| 22 | `fkpaises` | string | YES |  |

### spiga_dbmlc.spiga_tercerostelefonos_peru

**Columnas:** 22

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | integer | YES |  |
| 2 | `idconsecutivo` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `pkfkterceros` | integer | YES |  |
| 7 | `pktercerotelefonos_iden` | smallint | YES |  |
| 8 | `fktelefonotipos` | integer | YES |  |
| 9 | `codigotelefonico` | varchar | YES |  |
| 10 | `numero` | varchar | YES |  |
| 11 | `extension` | varchar | YES |  |
| 12 | `fktercerodirecciones` | smallint | YES |  |
| 13 | `direccionpadre` | boolean | YES |  |
| 14 | `horario` | varchar | YES |  |
| 15 | `fechabaja` | timestamp(3) | YES |  |
| 16 | `usermod` | smallint | YES |  |
| 17 | `hostmod` | varchar | YES |  |
| 18 | `versionfila` | integer | YES |  |
| 19 | `principal` | boolean | YES |  |
| 20 | `fechamod` | timestamp(3) | YES |  |
| 21 | `fkterceros_direcciones` | integer | YES |  |
| 22 | `fkpaises` | varchar | YES |  |

### spiga_dbmlc.spiga_tercerotercerotipos

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | integer | YES |  |
| 2 | `idconsecutivo` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `pkfkempresas` | integer | YES |  |
| 7 | `pkfkcentros` | integer | YES |  |
| 8 | `pkfkterceros` | bigint | YES |  |
| 9 | `pkfktercerotipos` | varchar | YES |  |
| 10 | `usermod` | bigint | YES |  |
| 11 | `fechaalta` | timestamp(3) | YES |  |
| 12 | `fechamod` | timestamp(3) | YES |  |

### spiga_dbmlc.spiga_tipoclasificacionesvehiculos

**Columnas:** 68

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | int | YES |  |
| 2 | `idconsecutivo` | int | YES |  |
| 3 | `pkfkmarcas` | smallint | YES |  |
| 4 | `pkfkgamas` | smallint | YES |  |
| 5 | `pkcodmodelo` | string | YES |  |
| 6 | `pkanomodelo` | string | YES |  |
| 7 | `fkclasificaciontipos` | string | YES |  |
| 8 | `nombreclasificacion` | string | YES |  |
| 9 | `cantidadpasajeros` | string | YES |  |
| 10 | `capacidaddecarga` | string | YES |  |
| 11 | `pkextmodelo` | string | YES |  |
| 12 | `nombre` | string | YES |  |
| 13 | `activo` | boolean | YES |  |
| 14 | `fkcombustibletipos` | string | YES |  |
| 15 | `fkcarroceriatipos` | string | YES |  |
| 16 | `fkmarcatallermodelos` | string | YES |  |
| 17 | `fktracciontipos` | string | YES |  |
| 18 | `fkcambiotipos` | string | YES |  |
| 19 | `potenciafiscal` | string | YES |  |
| 20 | `potenciareal` | string | YES |  |
| 21 | `cilindrada` | decimal(8,2) | YES |  |
| 22 | `aceleracion` | string | YES |  |
| 23 | `velocidadmax` | decimal(7,2) | YES |  |
| 24 | `numerocilindros` | int | YES |  |
| 25 | `consumointerurbano` | decimal(7,2) | YES |  |
| 26 | `consumourbano` | decimal(7,2) | YES |  |
| 27 | `consumomedio` | decimal(7,2) | YES |  |
| 28 | `emisionesco2medio` | decimal(7,2) | YES |  |
| 29 | `importado` | boolean | YES |  |
| 30 | `visibleweb` | boolean | YES |  |
| 31 | `periodoinspeccion` | smallint | YES |  |
| 32 | `kilometrosinspeccion` | string | YES |  |
| 33 | `fechabaja` | timestamp | YES |  |
| 34 | `codexternomodelo` | string | YES |  |
| 35 | `potenciarealkw` | string | YES |  |
| 36 | `propiopeso` | string | YES |  |
| 37 | `cargautil` | string | YES |  |
| 38 | `numeropuertas` | string | YES |  |
| 39 | `numeroplazas` | string | YES |  |
| 40 | `fkcajavelocidadtipos` | string | YES |  |
| 41 | `neumaticos` | string | YES |  |
| 42 | `pma` | string | YES |  |
| 43 | `fechamod` | timestamp | YES |  |
| 44 | `longitudexterior` | smallint | YES |  |
| 45 | `anchoexterior` | smallint | YES |  |
| 46 | `altoexterior` | smallint | YES |  |
| 47 | `disposicioncilindros` | string | YES |  |
| 48 | `volantealaizquierda` | boolean | YES |  |
| 49 | `fkmonedas` | smallint | YES |  |
| 50 | `factorcambiomoneda` | decimal(18,10) | YES |  |
| 51 | `numeroejes` | int | YES |  |
| 52 | `fkcategoriagamatipos` | string | YES |  |
| 53 | `detalleenfactura` | string | YES |  |
| 54 | `porcdtomaxvendedores` | decimal(9,7) | YES |  |
| 55 | `kilometrosgarantia` | int | YES |  |
| 56 | `numeroruedas` | int | YES |  |
| 57 | `numerovelocidades` | int | YES |  |
| 58 | `codigohomologacion` | string | YES |  |
| 59 | `numeroasientos` | string | YES |  |
| 60 | `requierecertificacion` | boolean | YES |  |
| 61 | `horasusoinspeccion` | string | YES |  |
| 62 | `potenciapto` | string | YES |  |
| 63 | `neumaticosdelanteros` | string | YES |  |
| 64 | `neumaticostraseros` | string | YES |  |
| 65 | `numcertificadopruebadinamica` | string | YES |  |
| 66 | `porcdtomaxjefesventas` | decimal(9,7) | YES |  |
| 67 | `fkpaises` | string | YES |  |
| 68 | `codpais` | smallint | YES |  |

### spiga_dbmlc.spiga_tipodeventasvehiculos

**Columnas:** 27

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | integer | YES |  |
| 2 | `idconsecutivo` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | smallint | YES |  |
| 7 | `empresa` | varchar | YES |  |
| 8 | `idcentros` | smallint | YES |  |
| 9 | `centro` | varchar | YES |  |
| 10 | `expediente` | varchar | YES |  |
| 11 | `factura` | varchar | YES |  |
| 12 | `vin` | varchar | YES |  |
| 13 | `placa` | varchar | YES |  |
| 14 | `fechamatriculacion` | timestamp(3) | YES |  |
| 15 | `sitioplaca` | varchar | YES |  |
| 16 | `perfilcliente` | varchar | YES |  |
| 17 | `tiponegocio` | varchar | YES |  |
| 18 | `nombretercero` | varchar | YES |  |
| 19 | `tipoentrada` | varchar | YES |  |
| 20 | `tipoventa` | varchar | YES |  |
| 21 | `tipocompra` | varchar | YES |  |
| 22 | `tipoventamarca` | varchar | YES |  |
| 23 | `tipofinanciacion` | varchar | YES |  |
| 24 | `numerocotizacion` | varchar | YES |  |
| 25 | `fechapazysalvo` | timestamp(3) | YES |  |
| 26 | `numpazysalvo` | integer | YES |  |
| 27 | `estado` | varchar | YES |  |

### spiga_dbmlc.spiga_vehiculos

**Columnas:** 60

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | int | YES |  |
| 2 | `idconsecutivo` | int | YES |  |
| 3 | `ano_periodo` | int | YES |  |
| 4 | `mes_periodo` | int | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `fechadeactualizacion` | timestamp | YES |  |
| 7 | `placa` | string | YES |  |
| 8 | `vin` | string | YES |  |
| 9 | `numdocumentopropietario` | string | YES |  |
| 10 | `numdocumentoconductor` | string | YES |  |
| 11 | `numdocumentoleasingrenting` | string | YES |  |
| 12 | `numdocumentoarrendador` | string | YES |  |
| 13 | `codigomarca` | smallint | YES |  |
| 14 | `nombremarca` | string | YES |  |
| 15 | `codigogama` | smallint | YES |  |
| 16 | `nombregama` | string | YES |  |
| 17 | `codmodelo` | string | YES |  |
| 18 | `nombremodelo` | string | YES |  |
| 19 | `extmodelo` | string | YES |  |
| 20 | `añomodelo` | string | YES |  |
| 21 | `version` | string | YES |  |
| 22 | `codmodeloexterno` | string | YES |  |
| 23 | `potencia` | string | YES |  |
| 24 | `torque` | string | YES |  |
| 25 | `cilindrada` | decimal(8,2) | YES |  |
| 26 | `combustible` | string | YES |  |
| 27 | `carroceria` | string | YES |  |
| 28 | `modelotaller` | string | YES |  |
| 29 | `color` | string | YES |  |
| 30 | `tapizado` | string | YES |  |
| 31 | `numeromotor` | string | YES |  |
| 32 | `codigofabricacion` | string | YES |  |
| 33 | `opr` | string | YES |  |
| 34 | `modelopv` | string | YES |  |
| 35 | `numregistroimportacion` | string | YES |  |
| 36 | `numeroprefijo` | string | YES |  |
| 37 | `sitioplaca` | string | YES |  |
| 38 | `servicio` | string | YES |  |
| 39 | `paisorigen` | string | YES |  |
| 40 | `fechafingarantiamecanica` | timestamp | YES |  |
| 41 | `fechafingarantialatoneria` | timestamp | YES |  |
| 42 | `fechafingarantiapintura` | timestamp | YES |  |
| 43 | `fechafingarantiamotor` | timestamp | YES |  |
| 44 | `kilometrosfingarantia` | int | YES |  |
| 45 | `fechaultimainspeccion` | timestamp | YES |  |
| 46 | `fechaproximainspeccion` | timestamp | YES |  |
| 47 | `kilometrosinspeccion` | string | YES |  |
| 48 | `kmsactuales` | int | YES |  |
| 49 | `tiposeguro` | string | YES |  |
| 50 | `ciaseguros` | string | YES |  |
| 51 | `fechaalta` | timestamp | YES |  |
| 52 | `fechavencimiento` | timestamp | YES |  |
| 53 | `valor` | decimal(32,8) | YES |  |
| 54 | `deducible` | decimal(32,8) | YES |  |
| 55 | `importecomisionventa` | decimal(32,8) | YES |  |
| 56 | `numeropoliza` | string | YES |  |
| 57 | `tomador` | string | YES |  |
| 58 | `gestornegocio` | string | YES |  |
| 59 | `idvehiculos` | int | YES |  |
| 60 | `codpais` | smallint | YES |  |

### spiga_dbmlc.spiga_vehiculosentregados

**Columnas:** 33

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | integer | YES |  |
| 2 | `idconsecutivo` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | smallint | YES |  |
| 7 | `a�o` | integer | YES |  |
| 8 | `mes` | integer | YES |  |
| 9 | `codigoempresa` | smallint | YES |  |
| 10 | `empresa` | varchar | YES |  |
| 11 | `codigocentro` | smallint | YES |  |
| 12 | `centro` | varchar | YES |  |
| 13 | `codigoseccion` | integer | YES |  |
| 14 | `seccion` | varchar | YES |  |
| 15 | `codigomarca` | smallint | YES |  |
| 16 | `marca` | varchar | YES |  |
| 17 | `codigogama` | smallint | YES |  |
| 18 | `gama` | varchar | YES |  |
| 19 | `codigomodelo` | varchar | YES |  |
| 20 | `a�omodelo` | varchar | YES |  |
| 21 | `modelo` | varchar | YES |  |
| 22 | `cedulavendedor` | varchar | YES |  |
| 23 | `nombrevendedor` | varchar | YES |  |
| 24 | `nit` | varchar | YES |  |
| 25 | `nombretercero` | varchar | YES |  |
| 26 | `cantidad` | integer | YES |  |
| 27 | `valor` | decimal(18,2) | YES |  |
| 28 | `tipo` | varchar | YES |  |
| 29 | `fechaentregacliente` | timestamp(3) | YES |  |
| 30 | `fechamod` | timestamp(3) | YES |  |
| 31 | `vin` | varchar | YES |  |
| 32 | `fechafactura` | timestamp(3) | YES |  |
| 33 | `fkterceros_alquilador` | integer | YES |  |

### spiga_dbmlc.spigafichallamadaagendamientodatostercerofechaalta

**Columnas:** 18

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | integer | YES |  |
| 2 | `idconsecutivo` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `pkterceros` | integer | YES |  |
| 6 | `nombre` | varchar | YES |  |
| 7 | `apellido1` | varchar | YES |  |
| 8 | `apellido2` | varchar | YES |  |
| 9 | `celular` | varchar | YES |  |
| 10 | `fijo` | varchar | YES |  |
| 11 | `direccion` | varchar | YES |  |
| 12 | `poblacion` | varchar | YES |  |
| 13 | `tipodocumento` | varchar | YES |  |
| 14 | `nifcif` | varchar | YES |  |
| 15 | `email` | varchar | YES |  |
| 16 | `categoriacliente` | varchar | YES |  |
| 17 | `fechaalta` | timestamp(3) | YES |  |
| 18 | `emailotro` | varchar | YES |  |

### spiga_dbmlc.ubicaciones

**Columnas:** 9

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `pkfkempresas` | smallint | YES |  |
| 2 | `pkfkcentros` | smallint | YES |  |
| 3 | `pkubicataller` | varchar | YES |  |
| 4 | `descripcion` | varchar | YES |  |
| 5 | `operacion` | varchar | YES |  |
| 6 | `hashvaluebi` | bigint | YES |  |
| 7 | `versionct` | integer | YES |  |
| 8 | `fechainsercion` | timestamp(3) | YES |  |
| 9 | `idproceso` | integer | YES |  |

### spiga_dbmlc.v_empleadosactivosretirados

**Columnas:** 49

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `estado` | varchar | YES |  |
| 2 | `codigoempleado` | bigint | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `codigoempresa` | smallint | YES |  |
| 6 | `empresa` | varchar | YES |  |
| 7 | `nombres` | varchar | YES |  |
| 8 | `apellido1` | varchar | YES |  |
| 9 | `apellido2` | varchar | YES |  |
| 10 | `fecha_ingreso` | timestamp(3) | YES |  |
| 11 | `codigomarca` | smallint | YES |  |
| 12 | `marca` | varchar | YES |  |
| 13 | `codigo_centro` | varchar | YES |  |
| 14 | `nombre_centro` | varchar | YES |  |
| 15 | `codigo_seccion` | varchar | YES |  |
| 16 | `nombre_seccion` | varchar | YES |  |
| 17 | `codigo_sucursal` | varchar | YES |  |
| 18 | `nombre_sucursal` | varchar | YES |  |
| 19 | `codigo_departamento` | varchar | YES |  |
| 20 | `nombre_departamento` | varchar | YES |  |
| 21 | `codigo_cargo` | varchar | YES |  |
| 22 | `nombre_cargo` | varchar | YES |  |
| 23 | `codigo_cargo_generico` | varchar | YES |  |
| 24 | `nombre_cargo_generico` | varchar | YES |  |
| 25 | `email` | varchar | YES |  |
| 26 | `email_corporativo` | varchar | YES |  |
| 27 | `codigo_departamento_trabajo` | varchar | YES |  |
| 28 | `nombre_departamento_trabajo` | varchar | YES |  |
| 29 | `codigo_ciudad_trabajo` | varchar | YES |  |
| 30 | `nombre_ciudad_trabajo` | varchar | YES |  |
| 31 | `codigo_cargo_junta` | varchar | YES |  |
| 32 | `nombre_cargo_junta` | varchar | YES |  |
| 33 | `codigo_tipo_contrato` | varchar | YES |  |
| 34 | `nombre_tipo_contrato` | varchar | YES |  |
| 35 | `fecha_retiro` | timestamp(3) | YES |  |
| 36 | `codigo_causa_retiro` | varchar | YES |  |
| 37 | `causaretiro` | varchar | YES |  |
| 38 | `unidad_negocio` | varchar | YES |  |
| 39 | `nombre_unidad_negocio` | varchar | YES |  |
| 40 | `fecha_nacimiento` | timestamp(3) | YES |  |
| 41 | `genero` | varchar | YES |  |
| 42 | `indicador_salario_variable` | smallint | YES |  |
| 43 | `indicador_comisiones` | varchar | YES |  |
| 44 | `prefijo_cuenta_contable` | varchar | YES |  |
| 45 | `codigo_cno` | varchar | YES |  |
| 46 | `descripcion_cno` | varchar | YES |  |
| 47 | `codigo_clase_salario` | smallint | YES |  |
| 48 | `nombre_clase_salario` | varchar | YES |  |
| 49 | `documento` | varchar | YES |  |

### spiga_dbmlc.v_habeas_data

**Columnas:** 4

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `pkterceros` | integer | YES |  |
| 2 | `nombres` | varchar | YES |  |
| 3 | `numdocumento` | varchar | YES |  |
| 4 | `valorbool` | boolean | YES |  |

### spiga_dbmlc.v_segurosvehiculos

**Columnas:** 31

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `ano_periodo` | integer | YES |  |
| 2 | `mes_periodo` | integer | YES |  |
| 3 | `fechadecorte` | timestamp(3) | YES |  |
| 4 | `idvehiculoseguros` | smallint | YES |  |
| 5 | `idsegurotipos` | varchar | YES |  |
| 6 | `descripcionsegurotipos` | varchar | YES |  |
| 7 | `fechaalta` | timestamp(3) | YES |  |
| 8 | `fechavencimiento` | timestamp(3) | YES |  |
| 9 | `importe` | decimal(18,4) | YES |  |
| 10 | `numeropoliza` | varchar | YES |  |
| 11 | `idvehiculos` | integer | YES |  |
| 12 | `vin` | varchar | YES |  |
| 13 | `matricula` | varchar | YES |  |
| 14 | `idmarcas` | integer | YES |  |
| 15 | `nombremarca` | varchar | YES |  |
| 16 | `idgamas` | smallint | YES |  |
| 17 | `nombregama` | varchar | YES |  |
| 18 | `codmodelo` | varchar | YES |  |
| 19 | `a�omodelo` | varchar | YES |  |
| 20 | `nombremodelo` | varchar | YES |  |
| 21 | `idterceros_propietario` | integer | YES |  |
| 22 | `nifcif` | varchar | YES |  |
| 23 | `nombre` | varchar | YES |  |
| 24 | `apellido1` | varchar | YES |  |
| 25 | `apellido2` | varchar | YES |  |
| 26 | `idterceros` | integer | YES |  |
| 27 | `nombreseguro` | varchar | YES |  |
| 28 | `nombreempleado` | varchar | YES |  |
| 29 | `nombrecentrocomprasvn` | varchar | YES |  |
| 30 | `nombrecentrovo` | varchar | YES |  |
| 31 | `centroventa` | varchar | YES |  |

### spiga_dbmlc.vw_comisionesspigavn

**Columnas:** 49

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `idcomisionspiga` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `ano_spiga` | integer | YES |  |
| 6 | `mes_spiga` | integer | YES |  |
| 7 | `codigoempresa` | smallint | YES |  |
| 8 | `empresa` | varchar | YES |  |
| 9 | `codigoempresasugerido` | integer | YES |  |
| 10 | `empresasugerida` | varchar | YES |  |
| 11 | `codigocentro` | smallint | YES |  |
| 12 | `centro` | varchar | YES |  |
| 13 | `codigoseccion` | integer | YES |  |
| 14 | `seccion` | varchar | YES |  |
| 15 | `fechafactura` | timestamp(3) | YES |  |
| 16 | `numerofactura` | varchar | YES |  |
| 17 | `vin` | varchar | YES |  |
| 18 | `codigomarca` | smallint | YES |  |
| 19 | `marca` | varchar | YES |  |
| 20 | `codigogama` | smallint | YES |  |
| 21 | `gama` | varchar | YES |  |
| 22 | `codigomodelo` | varchar | YES |  |
| 23 | `extension` | varchar | YES |  |
| 24 | `a�omodelo` | varchar | YES |  |
| 25 | `modelo` | varchar | YES |  |
| 26 | `codigoversion` | varchar | YES |  |
| 27 | `nombreversion` | varchar | YES |  |
| 28 | `cedulavendedor` | bigint | YES |  |
| 29 | `nombrevendedor` | varchar | YES |  |
| 30 | `nit` | varchar | YES |  |
| 31 | `nombretercero` | varchar | YES |  |
| 32 | `preciovehiculo` | decimal(18,4) | YES |  |
| 33 | `preciolista` | decimal(18,4) | YES |  |
| 34 | `valordto` | decimal(18,4) | YES |  |
| 35 | `importeimpuestos` | decimal(38,4) | YES |  |
| 36 | `totalfactura` | decimal(18,4) | YES |  |
| 37 | `fechacancelacionfactura` | timestamp(3) | YES |  |
| 38 | `totalcanceladofactura` | decimal(38,4) | YES |  |
| 39 | `fecharemesa` | timestamp(3) | YES |  |
| 40 | `valorremesado` | decimal(38,4) | YES |  |
| 41 | `fechaentregacliente` | timestamp(3) | YES |  |
| 42 | `descuentopolitica` | decimal(15,9) | YES |  |
| 43 | `numerentregas` | integer | YES |  |
| 44 | `tipo_servicio` | varchar | YES |  |
| 45 | `cuotaretefuente` | decimal(18,4) | YES |  |
| 46 | `entregaefectiva` | integer | YES |  |
| 47 | `procedencia` | varchar | YES |  |
| 48 | `procedenciadetalle` | varchar | YES |  |
| 49 | `tipooportunidad` | varchar | YES |  |

### spiga_dbmlc.vw_comisionesspigavo

**Columnas:** 49

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `idcomisionspiga` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `ano_spiga` | integer | YES |  |
| 6 | `mes_spiga` | integer | YES |  |
| 7 | `codigoempresa` | smallint | YES |  |
| 8 | `empresa` | varchar | YES |  |
| 9 | `codigoempresasugerido` | integer | YES |  |
| 10 | `empresasugerida` | varchar | YES |  |
| 11 | `codigocentro` | smallint | YES |  |
| 12 | `centro` | varchar | YES |  |
| 13 | `codigoseccion` | integer | YES |  |
| 14 | `seccion` | varchar | YES |  |
| 15 | `fechafactura` | timestamp(3) | YES |  |
| 16 | `numerofactura` | varchar | YES |  |
| 17 | `vin` | varchar | YES |  |
| 18 | `codigomarca` | smallint | YES |  |
| 19 | `marca` | varchar | YES |  |
| 20 | `codigogama` | smallint | YES |  |
| 21 | `gama` | varchar | YES |  |
| 22 | `codigomodelo` | varchar | YES |  |
| 23 | `extension` | varchar | YES |  |
| 24 | `a�omodelo` | varchar | YES |  |
| 25 | `modelo` | varchar | YES |  |
| 26 | `codigoversion` | varchar | YES |  |
| 27 | `nombreversion` | varchar | YES |  |
| 28 | `cedulavendedor` | bigint | YES |  |
| 29 | `nombrevendedor` | varchar | YES |  |
| 30 | `nit` | varchar | YES |  |
| 31 | `nombretercero` | varchar | YES |  |
| 32 | `preciovehiculo` | decimal(18,4) | YES |  |
| 33 | `preciolista` | decimal(18,4) | YES |  |
| 34 | `valordto` | decimal(18,4) | YES |  |
| 35 | `importeimpuestos` | decimal(38,4) | YES |  |
| 36 | `totalfactura` | decimal(18,4) | YES |  |
| 37 | `fechacancelacionfactura` | timestamp(3) | YES |  |
| 38 | `totalcanceladofactura` | decimal(38,4) | YES |  |
| 39 | `fecharemesa` | timestamp(3) | YES |  |
| 40 | `valorremesado` | decimal(38,4) | YES |  |
| 41 | `fechaentregacliente` | timestamp(3) | YES |  |
| 42 | `descuentopolitica` | decimal(15,9) | YES |  |
| 43 | `numerentregas` | integer | YES |  |
| 44 | `tipo_servicio` | varchar | YES |  |
| 45 | `cuotaretefuente` | decimal(38,4) | YES |  |
| 46 | `entregaefectiva` | integer | YES |  |
| 47 | `procedencia` | varchar | YES |  |
| 48 | `procedenciadetalle` | varchar | YES |  |
| 49 | `tipooportunidad` | varchar | YES |  |

### spiga_dbmlc.vw_empleadosactivos

**Columnas:** 48

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codigoempleado` | bigint | YES |  |
| 2 | `ano_periodo` | integer | YES |  |
| 3 | `mes_periodo` | integer | YES |  |
| 4 | `codigoempresa` | smallint | YES |  |
| 5 | `empresa` | varchar | YES |  |
| 6 | `nombres` | varchar | YES |  |
| 7 | `apellido1` | varchar | YES |  |
| 8 | `apellido2` | varchar | YES |  |
| 9 | `nombrecompleto` | varchar | YES |  |
| 10 | `fecha_ingreso` | timestamp(3) | YES |  |
| 11 | `codigomarca` | smallint | YES |  |
| 12 | `marca` | varchar | YES |  |
| 13 | `codigo_centro` | varchar | YES |  |
| 14 | `nombre_centro` | varchar | YES |  |
| 15 | `codigo_seccion` | varchar | YES |  |
| 16 | `nombre_seccion` | varchar | YES |  |
| 17 | `codigo_sucursal` | varchar | YES |  |
| 18 | `nombre_sucursal` | varchar | YES |  |
| 19 | `codigo_departamento` | varchar | YES |  |
| 20 | `nombre_departamento` | varchar | YES |  |
| 21 | `codigo_cargo` | varchar | YES |  |
| 22 | `nombre_cargo` | varchar | YES |  |
| 23 | `codigo_cargo_generico` | varchar | YES |  |
| 24 | `nombre_cargo_generico` | varchar | YES |  |
| 25 | `email` | varchar | YES |  |
| 26 | `codigo_departamento_trabajo` | varchar | YES |  |
| 27 | `nombre_departamento_trabajo` | varchar | YES |  |
| 28 | `codigo_ciudad_trabajo` | varchar | YES |  |
| 29 | `nombre_ciudad_trabajo` | varchar | YES |  |
| 30 | `codigo_cargo_junta` | varchar | YES |  |
| 31 | `nombre_cargo_junta` | varchar | YES |  |
| 32 | `codigo_tipo_contrato` | varchar | YES |  |
| 33 | `nombre_tipo_contrato` | varchar | YES |  |
| 34 | `unidad_negocio` | varchar | YES |  |
| 35 | `nombre_unidad_negocio` | varchar | YES |  |
| 36 | `fecha_nacimiento` | timestamp(3) | YES |  |
| 37 | `genero` | varchar | YES |  |
| 38 | `indicador_salario_variable` | smallint | YES |  |
| 39 | `indicador_comisiones` | varchar | YES |  |
| 40 | `prefijo_cuenta_contable` | varchar | YES |  |
| 41 | `codigo_cno` | varchar | YES |  |
| 42 | `codigo_clase_salario` | smallint | YES |  |
| 43 | `nombre_clase_salario` | varchar | YES |  |
| 44 | `email_corporativo` | varchar | YES |  |
| 45 | `celular` | varchar | YES |  |
| 46 | `telefono_fijo` | varchar | YES |  |
| 47 | `estado` | varchar | YES |  |
| 48 | `documento` | varchar | YES |  |

### spiga_dbmlc.vw_unidaddenegocio

**Columnas:** 19

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | integer | YES |  |
| 2 | `codempresa` | smallint | YES |  |
| 3 | `nombreempresa` | varchar | YES |  |
| 4 | `codcentro` | smallint | YES |  |
| 5 | `nombrecentro` | varchar | YES |  |
| 6 | `codseccion` | smallint | YES |  |
| 7 | `nombreseccion` | varchar | YES |  |
| 8 | `coddepartamento` | varchar | YES |  |
| 9 | `nombredepartamento` | varchar | YES |  |
| 10 | `codunidadnegocio` | smallint | YES |  |
| 11 | `nombreunidadnegocio` | varchar | YES |  |
| 12 | `unidadnegocio_requisicion` | smallint | YES |  |
| 13 | `nombreunidadnegocio_requisicion` | varchar | YES |  |
| 14 | `sigla` | varchar | YES |  |
| 15 | `division` | varchar | YES |  |
| 16 | `codsedeambiental` | smallint | YES |  |
| 17 | `sedeambiental` | varchar | YES |  |
| 18 | `codsededistcol` | varchar | YES |  |
| 19 | `sededistribucioncolision` | varchar | YES |  |

## 🥈 spiga_materialized_data

`Capa: Plata / Materialized`

### spiga_materialized_data.datos_terceros

**Columnas:** 10

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `pkterceros` | bigint | YES |  |
| 2 | `nifcif` | varchar | YES |  |
| 3 | `direccion` | varchar | YES |  |
| 4 | `correo` | varchar | YES |  |
| 5 | `numero` | varchar | YES |  |
| 6 | `id_formacionniveles` | varchar | YES |  |
| 7 | `fktercerocargos` | varchar | YES |  |
| 8 | `fkestadociviltipos` | varchar | YES |  |
| 9 | `id_profesiones` | varchar | YES |  |
| 10 | `fkterceroclases` | varchar | YES |  |

### spiga_materialized_data.datos_terceros_unificado

**Columnas:** 13

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `pkterceros` | bigint | YES |  |
| 2 | `nifcif` | varchar | YES |  |
| 3 | `fechamod` | timestamp(3) | YES |  |
| 4 | `direccion` | varchar | YES |  |
| 5 | `correo` | varchar | YES |  |
| 6 | `numero` | varchar | YES |  |
| 7 | `id_formacionniveles` | varchar | YES |  |
| 8 | `fktercerocargos` | varchar | YES |  |
| 9 | `fkestadociviltipos` | varchar | YES |  |
| 10 | `id_profesiones` | varchar | YES |  |
| 11 | `fkterceroclases` | varchar | YES |  |
| 12 | `pais_origen` | varchar | YES |  |
| 13 | `nombretercero` | varchar | YES |  |

### spiga_materialized_data.entradas_taller

**Columnas:** 38

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idempresas` | varchar | YES |  |
| 2 | `idcentros` | varchar | YES |  |
| 3 | `a�oot` | varchar | YES |  |
| 4 | `serieot` | varchar | YES |  |
| 5 | `numot` | varchar | YES |  |
| 6 | `numtrabajo` | varchar | YES |  |
| 7 | `idtrabajoestados` | varchar | YES |  |
| 8 | `idterceros` | varchar | YES |  |
| 9 | `idtrabajotipos` | varchar | YES |  |
| 10 | `idsecciones` | varchar | YES |  |
| 11 | `idcargotipos` | varchar | YES |  |
| 12 | `fechaalta` | varchar | YES |  |
| 13 | `fechaentrada` | varchar | YES |  |
| 14 | `horasmo` | varchar | YES |  |
| 15 | `matricula` | varchar | YES |  |
| 16 | `vin` | varchar | YES |  |
| 17 | `idmarcas` | varchar | YES |  |
| 18 | `nombremarca` | varchar | YES |  |
| 19 | `idgamas` | varchar | YES |  |
| 20 | `nombregama` | varchar | YES |  |
| 21 | `idempleados` | varchar | YES |  |
| 22 | `descripciontrabajotipos` | varchar | YES |  |
| 23 | `kmts` | varchar | YES |  |
| 24 | `nombretercerocargo` | varchar | YES |  |
| 25 | `udn_codempresa` | varchar | YES |  |
| 26 | `udn_codcentro` | varchar | YES |  |
| 27 | `udn_codseccion` | varchar | YES |  |
| 28 | `nombreempresa` | varchar | YES |  |
| 29 | `nombrecentro` | varchar | YES |  |
| 30 | `nombreseccion` | varchar | YES |  |
| 31 | `codunidadnegocio` | integer | YES |  |
| 32 | `nombreunidadnegocio` | varchar | YES |  |
| 33 | `ecs` | varchar | YES |  |
| 34 | `nccentro` | varchar | YES |  |
| 35 | `ncmarcas` | varchar | YES |  |
| 36 | `sigla` | varchar | YES |  |
| 37 | `eje` | varchar | YES |  |
| 38 | `entradataller` | varchar | YES |  |

### spiga_materialized_data.financiacionesventas_vnvo

**Columnas:** 42

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `idofertapagos` | bigint | YES |  |
| 12 | `saldofavorcliente` | bigint | YES |  |
| 13 | `importefinanciado` | double | YES |  |
| 14 | `fechavencimiento` | timestamp(3) | YES |  |
| 15 | `fechainicio` | timestamp(3) | YES |  |
| 16 | `comisionfinanciera` | double | YES |  |
| 17 | `vin` | varchar | YES |  |
| 18 | `matricula` | varchar | YES |  |
| 19 | `comisionvehiculo` | varchar | YES |  |
| 20 | `idterceros` | bigint | YES |  |
| 21 | `nombrepropietario` | varchar | YES |  |
| 22 | `nifcifpropietario` | varchar | YES |  |
| 23 | `idtercerosfinanciera` | bigint | YES |  |
| 24 | `nombrefinanciera` | varchar | YES |  |
| 25 | `idempleados` | bigint | YES |  |
| 26 | `nombreempleado` | varchar | YES |  |
| 27 | `idtercerosagente` | bigint | YES |  |
| 28 | `nombreagente` | varchar | YES |  |
| 29 | `idmarcas` | bigint | YES |  |
| 30 | `nombremarca` | varchar | YES |  |
| 31 | `idgamas` | bigint | YES |  |
| 32 | `nombregama` | varchar | YES |  |
| 33 | `idempleadosgestor` | bigint | YES |  |
| 34 | `nombregestor` | varchar | YES |  |
| 35 | `fechaventa` | timestamp(3) | YES |  |
| 36 | `nombreempresa` | varchar | YES |  |
| 37 | `nombrecentro` | varchar | YES |  |
| 38 | `idmodulos` | varchar | YES |  |
| 39 | `estado` | varchar | YES |  |
| 40 | `descripcionsecciones` | varchar | YES |  |
| 41 | `fechaentregacliente` | timestamp(3) | YES |  |
| 42 | `load_date` | varchar | YES |  |

### spiga_materialized_data.homologacion_carroya

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codigomodelo` | varchar | YES |  |
| 2 | `anio_modelo` | varchar | YES |  |
| 3 | `marca` | varchar | YES |  |
| 4 | `gama` | varchar | YES |  |
| 5 | `modelo` | varchar | YES |  |
| 6 | `cilindraje` | varchar | YES |  |
| 7 | `combustible` | varchar | YES |  |
| 8 | `traccion` | varchar | YES |  |
| 9 | `codigo_fasecolda` | varchar | YES |  |
| 10 | `confiabilidad` | varchar | YES |  |
| 11 | `intentos_fallidos` | varchar | YES |  |
| 12 | `ultimo_intento` | varchar | YES |  |

### spiga_materialized_data.homologacion_spiga

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codigomodelo` | varchar | YES |  |
| 2 | `anio_modelo` | varchar | YES |  |
| 3 | `marca` | varchar | YES |  |
| 4 | `gama` | varchar | YES |  |
| 5 | `modelo` | varchar | YES |  |
| 6 | `cilindraje` | varchar | YES |  |
| 7 | `combustible` | varchar | YES |  |
| 8 | `traccion` | varchar | YES |  |
| 9 | `codigo_fasecolda` | varchar | YES |  |
| 10 | `confiabilidad` | varchar | YES |  |
| 11 | `intentos_fallidos` | varchar | YES |  |
| 12 | `ultimo_intento` | varchar | YES |  |

### spiga_materialized_data.homologacion_spiga_fc

**Columnas:** 9

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codmodelo` | varchar | YES |  |
| 2 | `nombremodelo` | varchar | YES |  |
| 3 | `extmodelo` | varchar | YES |  |
| 4 | `idmarcas` | bigint | YES |  |
| 5 | `nombremarca` | varchar | YES |  |
| 6 | `idgamas` | bigint | YES |  |
| 7 | `nombregama` | varchar | YES |  |
| 8 | `a�omodelo` | varchar | YES |  |
| 9 | `codigo_fasecolda` | varchar | YES |  |

### spiga_materialized_data.informafacturacion

**Columnas:** 84

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `a�o` | integer | YES |  |
| 2 | `mes` | integer | YES |  |
| 3 | `entradataller` | varchar | YES |  |
| 4 | `ncmarcas` | varchar | YES |  |
| 5 | `tipo` | varchar | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `idsecciones` | bigint | YES |  |
| 9 | `a�oot` | varchar | YES |  |
| 10 | `serieot` | varchar | YES |  |
| 11 | `numot` | bigint | YES |  |
| 12 | `numtrabajo` | bigint | YES |  |
| 13 | `fechaalta` | timestamp(3) | YES |  |
| 14 | `fechacierre` | timestamp(3) | YES |  |
| 15 | `idseriesgarantias` | varchar | YES |  |
| 16 | `horasfacturadas` | bigint | YES |  |
| 17 | `matricula` | varchar | YES |  |
| 18 | `vin` | varchar | YES |  |
| 19 | `idmarcas` | bigint | YES |  |
| 20 | `idgamas` | bigint | YES |  |
| 21 | `fechadespacho` | timestamp(3) | YES |  |
| 22 | `nombremarcas` | varchar | YES |  |
| 23 | `nombregamas` | varchar | YES |  |
| 24 | `a�ofactura` | varchar | YES |  |
| 25 | `seriefactura` | varchar | YES |  |
| 26 | `numfactura` | varchar | YES |  |
| 27 | `idtercerofactura` | bigint | YES |  |
| 28 | `nombretercero` | varchar | YES |  |
| 29 | `fechafactura` | timestamp(3) | YES |  |
| 30 | `idempleados` | bigint | YES |  |
| 31 | `kmts` | bigint | YES |  |
| 32 | `a�omodelo` | varchar | YES |  |
| 33 | `idterceropropietario` | bigint | YES |  |
| 34 | `descripciontrabajo` | varchar | YES |  |
| 35 | `diasabierto` | double | YES |  |
| 36 | `fechaentrega` | timestamp(3) | YES |  |
| 37 | `idtercerocargo` | bigint | YES |  |
| 38 | `nombretercerocargo` | varchar | YES |  |
| 39 | `descripcionseccioncargos` | varchar | YES |  |
| 40 | `idempleadosresponsable` | bigint | YES |  |
| 41 | `idserviciotipos` | bigint | YES |  |
| 42 | `importemobruto` | double | YES |  |
| 43 | `importemoaceptada` | double | YES |  |
| 44 | `importematerialbruto` | double | YES |  |
| 45 | `importematerialaceptada` | double | YES |  |
| 46 | `importesubbruto` | double | YES |  |
| 47 | `importesubaceptada` | double | YES |  |
| 48 | `importevarbruto` | double | YES |  |
| 49 | `importevaraceptada` | double | YES |  |
| 50 | `importepintbruto` | double | YES |  |
| 51 | `importepintaceptada` | double | YES |  |
| 52 | `descuentomo` | double | YES |  |
| 53 | `descuentosub` | double | YES |  |
| 54 | `descuentovar` | double | YES |  |
| 55 | `descuentopint` | double | YES |  |
| 56 | `descuentomaterial` | double | YES |  |
| 57 | `importemobruto2` | double | YES |  |
| 58 | `importematerialbruto2` | double | YES |  |
| 59 | `importesubbruto2` | double | YES |  |
| 60 | `importevarbruto2` | double | YES |  |
| 61 | `importepintbruto2` | double | YES |  |
| 62 | `descuentomo2` | double | YES |  |
| 63 | `descuentosub2` | double | YES |  |
| 64 | `descuentovar2` | double | YES |  |
| 65 | `descuentopint2` | double | YES |  |
| 66 | `descuentomaterial2` | double | YES |  |
| 67 | `factura_total` | double | YES |  |
| 68 | `eje` | varchar | YES |  |
| 69 | `deducible` | integer | YES |  |
| 70 | `salidasp` | integer | YES |  |
| 71 | `udn_codempresa` | varchar | YES |  |
| 72 | `udn_codcentro` | varchar | YES |  |
| 73 | `udn_codseccion` | varchar | YES |  |
| 74 | `nombreempresa` | varchar | YES |  |
| 75 | `nombrecentro` | varchar | YES |  |
| 76 | `nombreseccion` | varchar | YES |  |
| 77 | `codunidadnegocio` | integer | YES |  |
| 78 | `nombreunidadnegocio` | varchar | YES |  |
| 79 | `ecs` | varchar | YES |  |
| 80 | `nccentro` | varchar | YES |  |
| 81 | `sigla` | varchar | YES |  |
| 82 | `conteo` | integer | YES |  |
| 83 | `sum_valida` | bigint | YES |  |
| 84 | `salidas` | bigint | YES |  |

### spiga_materialized_data.movimientos_referencia

**Columnas:** 54

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idreferencias` | varchar | YES |  |
| 2 | `idmovimientotipos` | varchar | YES |  |
| 3 | `idmr` | varchar | YES |  |
| 4 | `idempresas` | bigint | YES |  |
| 5 | `idcentros` | bigint | YES |  |
| 6 | `idsecciones` | bigint | YES |  |
| 7 | `precio` | double | YES |  |
| 8 | `pmc` | double | YES |  |
| 9 | `unidades` | double | YES |  |
| 10 | `dtoporc` | double | YES |  |
| 11 | `ida�o` | varchar | YES |  |
| 12 | `serie` | varchar | YES |  |
| 13 | `numero` | varchar | YES |  |
| 14 | `idterceros` | bigint | YES |  |
| 15 | `seriefactura` | varchar | YES |  |
| 16 | `factura` | varchar | YES |  |
| 17 | `a�ofactura` | varchar | YES |  |
| 18 | `fechafactura` | timestamp(3) | YES |  |
| 19 | `a�oot` | varchar | YES |  |
| 20 | `serieot` | varchar | YES |  |
| 21 | `numot` | bigint | YES |  |
| 22 | `idtrabajo` | bigint | YES |  |
| 23 | `idempleadosalta` | bigint | YES |  |
| 24 | `descripcionmovimientotipo` | varchar | YES |  |
| 25 | `nombreempresa` | varchar | YES |  |
| 26 | `nombrecentro` | varchar | YES |  |
| 27 | `descripcionmr` | varchar | YES |  |
| 28 | `descripcionseccion` | varchar | YES |  |
| 29 | `iddepartamentos` | varchar | YES |  |
| 30 | `tipocargotaller` | varchar | YES |  |
| 31 | `nombretercero` | varchar | YES |  |
| 32 | `nifcif` | varchar | YES |  |
| 33 | `nombreempleado` | varchar | YES |  |
| 34 | `descripcionreferencia` | varchar | YES |  |
| 35 | `idclasificacion1` | varchar | YES |  |
| 36 | `idclasificacion5` | varchar | YES |  |
| 37 | `idclasificacion6` | varchar | YES |  |
| 38 | `nombreempleadoalta` | varchar | YES |  |
| 39 | `idpedidotipoventas` | varchar | YES |  |
| 40 | `descripcionpedidotipoventas` | varchar | YES |  |
| 41 | `nombremecanico` | varchar | YES |  |
| 42 | `nombretercerotrabajo` | varchar | YES |  |
| 43 | `apellido1tercerotrabajo` | varchar | YES |  |
| 44 | `apellido2tercerotrabajo` | varchar | YES |  |
| 45 | `idtercerostrabajo` | varchar | YES |  |
| 46 | `descripcionclasificacion1` | varchar | YES |  |
| 47 | `descripcionclasificacion5` | varchar | YES |  |
| 48 | `descripcionclasificacion6` | varchar | YES |  |
| 49 | `preciocompra` | varchar | YES |  |
| 50 | `seriefacturataller` | varchar | YES |  |
| 51 | `numerofacturataller` | varchar | YES |  |
| 52 | `a�ofacturataller` | varchar | YES |  |
| 53 | `fechafacturataller` | timestamp(3) | YES |  |
| 54 | `vin` | varchar | YES |  |

### spiga_materialized_data.nivel_servicio_informa_facturacion

**Columnas:** 3

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `nombrecentro` | varchar | YES |  |
| 2 | `nombreseccion` | varchar | YES |  |
| 3 | `nivel_servicio` | varchar | YES |  |

### spiga_materialized_data.prenda_runt

**Columnas:** 41

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `placa` | varchar | YES |  |
| 2 | `id_vehiculo` | bigint | YES |  |
| 3 | `a�o_matricula` | bigint | YES |  |
| 4 | `mes_matricula` | bigint | YES |  |
| 5 | `dia_matricula` | bigint | YES |  |
| 6 | `clase` | varchar | YES |  |
| 7 | `vin` | varchar | YES |  |
| 8 | `carroceria` | varchar | YES |  |
| 9 | `chasis` | varchar | YES |  |
| 10 | `linea` | varchar | YES |  |
| 11 | `modelo` | bigint | YES |  |
| 12 | `servicio` | varchar | YES |  |
| 13 | `pais` | varchar | YES |  |
| 14 | `color` | varchar | YES |  |
| 15 | `segmento` | varchar | YES |  |
| 16 | `cilindraje` | bigint | YES |  |
| 17 | `numero_ejes` | bigint | YES |  |
| 18 | `numero_puertas` | bigint | YES |  |
| 19 | `pasajeros_sentados` | bigint | YES |  |
| 20 | `capacidad_carga` | varchar | YES |  |
| 21 | `peso` | bigint | YES |  |
| 22 | `departamento` | varchar | YES |  |
| 23 | `municipio` | varchar | YES |  |
| 24 | `combustible` | varchar | YES |  |
| 25 | `tipo_matricula` | varchar | YES |  |
| 26 | `ciudad_propietario` | varchar | YES |  |
| 27 | `declaracion_importacion` | bigint | YES |  |
| 28 | `motor` | varchar | YES |  |
| 29 | `serie` | varchar | YES |  |
| 30 | `marca` | varchar | YES |  |
| 31 | `blindado` | varchar | YES |  |
| 32 | `nit_empresa_blindaje` | varchar | YES |  |
| 33 | `claraboya_sunroof` | varchar | YES |  |
| 34 | `identificador_combustible` | bigint | YES |  |
| 35 | `archivo` | varchar | YES |  |
| 36 | `acreedor` | varchar | YES |  |
| 37 | `nombre_aseguradora` | varchar | YES |  |
| 38 | `nombre_entidad_prenda` | varchar | YES |  |
| 39 | `prenda_si_no` | varchar | YES |  |
| 40 | `nifcifprincipal` | varchar | YES |  |
| 41 | `nombrecentro` | varchar | YES |  |

### spiga_materialized_data.presentaciones_config

> Reproduce `PresentacionesN` del Dataflow Power BI "PresentacionesComite": 1 fila por `llave_presentacion` con centro, empresa, unidad de negocio y ECS oficiales. Aplica filtro de empresas normalizadas, normalización de sedes, regla de `Limpieza` (selección de la sede-centro oficial), `CodUnidadNegocio` y `ECS`. La consume `bi_materialized_data.presentaciones_comite`. Validado en Athena (807 llaves, ECS 100%).

**Columnas:** 11

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `llave_presentacion` | varchar | YES | `codigopresentacion` + '/' + `nombresede` |
| 2 | `codigopresentacion` | integer | YES |  |
| 3 | `nombrepresentacion` | varchar | YES |  |
| 4 | `codigosede` | integer | YES |  |
| 5 | `nombresede` | varchar | YES | Nombre de sede normalizado |
| 6 | `nombrecentro` | varchar | YES |  |
| 7 | `empresa` | integer | YES |  |
| 8 | `nombreempresa` | varchar | YES |  |
| 9 | `codigocentro` | integer | YES |  |
| 10 | `codunidadnegocio` | integer | YES |  |
| 11 | `ecs` | varchar | YES | Override puntual > empresa+centro+'-'+codunidadnegocio |

### spiga_materialized_data.spiga_homologacion_fasecolda

**Columnas:** 11

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codigomodelo` | varchar | YES |  |
| 2 | `anio_modelo` | varchar | YES |  |
| 3 | `marca` | varchar | YES |  |
| 4 | `clasificacion` | varchar | YES |  |
| 5 | `gama` | varchar | YES |  |
| 6 | `modelo` | varchar | YES |  |
| 7 | `extmodelo` | varchar | YES |  |
| 8 | `cilindraje` | decimal(8,2) | YES |  |
| 9 | `combustible` | varchar | YES |  |
| 10 | `traccion` | varchar | YES |  |
| 11 | `codigo_fasecolda` | varchar | YES |  |

### spiga_materialized_data.tabla_holomologacion_spiga

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codigomodelo` | varchar | YES |  |
| 2 | `a�o` | varchar | YES |  |
| 3 | `marca` | varchar | YES |  |
| 4 | `clasificacion` | varchar | YES |  |
| 5 | `gama` | varchar | YES |  |
| 6 | `modelo` | varchar | YES |  |
| 7 | `extmodelo` | varchar | YES |  |
| 8 | `cilindraje` | double | YES |  |
| 9 | `combustible` | varchar | YES |  |
| 10 | `traccion` | varchar | YES |  |
| 11 | `codigo_fasecolda` | varchar | YES |  |
| 12 | `confiabilidad` | integer | YES |  |
| 13 | `intentos_fallidos` | integer | YES |  |
| 14 | `ultimo_intento` | timestamp(3) | YES |  |
| 15 | `disponible_desde` | timestamp(3) | YES |  |

### spiga_materialized_data.unidadnegocio_def

**Columnas:** 21

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codempresa` | varchar | YES |  |
| 2 | `nombreempresa` | varchar | YES |  |
| 3 | `codcentro` | varchar | YES |  |
| 4 | `nombrecentro` | varchar | YES |  |
| 5 | `codseccion` | varchar | YES |  |
| 6 | `nombreseccion` | varchar | YES |  |
| 7 | `codunidadnegocio` | integer | YES |  |
| 8 | `nombreunidadnegocio` | varchar | YES |  |
| 9 | `nombreemp-centro` | varchar | YES |  |
| 10 | `nombreecseccion` | varchar | YES |  |
| 11 | `ecs` | varchar | YES |  |
| 12 | `nccentro` | varchar | YES |  |
| 13 | `codmarca` | integer | YES |  |
| 14 | `nombremarca` | varchar | YES |  |
| 15 | `ncmarcas1` | varchar | YES |  |
| 16 | `ncmarcas` | varchar | YES |  |
| 17 | `ncgerencias` | varchar | YES |  |
| 18 | `sigla` | varchar | YES |  |
| 19 | `llavelim` | varchar | YES |  |
| 20 | `mj` | varchar | YES |  |
| 21 | `permisos_marcas` | varchar | YES |  |

### spiga_materialized_data.vehiculos_entregados

**Columnas:** 23

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `vin` | varchar | YES |  |
| 2 | `idempresas` | smallint | YES |  |
| 3 | `empresa` | varchar | YES |  |
| 4 | `codigocentro` | smallint | YES |  |
| 5 | `centro` | varchar | YES |  |
| 6 | `codigomarca` | smallint | YES |  |
| 7 | `marca` | varchar | YES |  |
| 8 | `codigogama` | smallint | YES |  |
| 9 | `gama` | varchar | YES |  |
| 10 | `codigomodelo` | varchar | YES |  |
| 11 | `a�omodelo` | varchar | YES |  |
| 12 | `modelo` | varchar | YES |  |
| 13 | `cedulavendedor` | varchar | YES |  |
| 14 | `nombrevendedor` | varchar | YES |  |
| 15 | `nit` | varchar | YES |  |
| 16 | `nombretercero` | varchar | YES |  |
| 17 | `cantidad` | integer | YES |  |
| 18 | `valor` | decimal(18,2) | YES |  |
| 19 | `tipo` | varchar | YES |  |
| 20 | `fechaentregacliente` | timestamp(3) | YES |  |
| 21 | `fechamod` | timestamp(3) | YES |  |
| 22 | `linea` | varchar | YES |  |
| 23 | `combust_nev_categoria` | varchar | YES |  |

### spiga_materialized_data.vehiculos_seguros

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `asesor` | varchar | YES |  |
| 2 | `cantidad2` | varchar | YES |  |
| 3 | `valor` | double | YES |  |
| 4 | `fecha` | date | YES |  |
| 5 | `nombretercero` | varchar | YES |  |
| 6 | `idmarca` | varchar | YES |  |
| 7 | `marca` | varchar | YES |  |
| 8 | `linea` | varchar | YES |  |
| 9 | `centro` | varchar | YES |  |
| 10 | `idgama` | varchar | YES |  |
| 11 | `gama` | varchar | YES |  |
| 12 | `idversion` | varchar | YES |  |
| 13 | `version` | varchar | YES |  |
| 14 | `a�omodelo` | varchar | YES |  |
| 15 | `idterceros` | varchar | YES |  |
| 16 | `vin` | varchar | YES |  |
| 17 | `numeroidentidad` | varchar | YES |  |
| 18 | `fechaentregacliente` | date | YES |  |
| 19 | `codigocentro` | varchar | YES |  |
| 20 | `fechaalta` | date | YES |  |
| 21 | `tipo` | varchar | YES |  |
| 22 | `kmts` | double | YES |  |
| 23 | `tipotrabajo` | varchar | YES |  |
| 24 | `idempresa` | varchar | YES |  |
| 25 | `descripcionreferencia` | varchar | YES |  |
| 26 | `descripcionclasificacion` | varchar | YES |  |
| 27 | `nombrefinanciera` | varchar | YES |  |
| 28 | `comisionvehiculo` | varchar | YES |  |
| 29 | `estado` | varchar | YES |  |
| 30 | `producto` | varchar | YES |  |

### spiga_materialized_data.vw_unidaddenegocio

**Columnas:** 19

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `codempresa` | integer | YES |  |
| 3 | `nombreempresa` | varchar | YES |  |
| 4 | `codcentro` | integer | YES |  |
| 5 | `nombrecentro` | varchar | YES |  |
| 6 | `codseccion` | integer | YES |  |
| 7 | `nombreseccion` | varchar | YES |  |
| 8 | `coddepartamento` | varchar | YES |  |
| 9 | `nombredepartamento` | varchar | YES |  |
| 10 | `codunidadnegocio` | integer | YES |  |
| 11 | `nombreunidadnegocio` | varchar | YES |  |
| 12 | `unidadnegocio_requisicion` | integer | YES |  |
| 13 | `nombreunidadnegocio_requisicion` | varchar | YES |  |
| 14 | `sigla` | varchar | YES |  |
| 15 | `division` | varchar | YES |  |
| 16 | `codsedeambiental` | integer | YES |  |
| 17 | `sedeambiental` | varchar | YES |  |
| 18 | `codsededistcol` | integer | YES |  |
| 19 | `sededistribucioncolision` | varchar | YES |  |

## 🥉 spiga_dbmlc_incremental

`Capa: Bronce / Raw`

> Tablas Spiga **transaccionales por periodo** (particionadas por `anio`/`mes` = `ano_periodo`/`mes_periodo`), extraidas por `migrate-spiga-incremental-extract` desde SQL Server PSCService con cargue incremental (solo se releen los periodos recientes). El esquema se alinea al del seed (catalogo `stage`) para mantener tipos consistentes entre particiones. Los jobs `materialized_*` las consumen desde aqui.

### spiga_dbmlc_incremental.spiga_cartera

**Columnas:** 60

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `indice` | double | YES |  |
| 8 | `idterceros` | bigint | YES |  |
| 9 | `idterceros_pagador` | bigint | YES |  |
| 10 | `nombretercero` | string | YES |  |
| 11 | `factura` | string | YES |  |
| 12 | `fechafactura` | timestamp | YES |  |
| 13 | `fechavencimiento` | timestamp | YES |  |
| 14 | `idpagoformas` | string | YES |  |
| 15 | `descripcionpagoformas` | string | YES |  |
| 16 | `idsituacionefectos` | bigint | YES |  |
| 17 | `descripcionsituacionefectos` | string | YES |  |
| 18 | `departamento` | string | YES |  |
| 19 | `nombredepartamento` | string | YES |  |
| 20 | `totalfactura` | double | YES |  |
| 21 | `importeefecto` | double | YES |  |
| 22 | `importependiente` | double | YES |  |
| 23 | `diadesde` | bigint | YES |  |
| 24 | `diahasta` | bigint | YES |  |
| 25 | `nombrecentro` | string | YES |  |
| 26 | `numdet` | bigint | YES |  |
| 27 | `a±oasiento` | string | YES |  |
| 28 | `idasientos` | bigint | YES |  |
| 29 | `descripciontipocalle` | string | YES |  |
| 30 | `nombrecalle` | string | YES |  |
| 31 | `numero` | string | YES |  |
| 32 | `bloque` | string | YES |  |
| 33 | `piso` | string | YES |  |
| 34 | `puerta` | string | YES |  |
| 35 | `complemento` | string | YES |  |
| 36 | `complemento2` | string | YES |  |
| 37 | `nifcif` | string | YES |  |
| 38 | `idpaises` | string | YES |  |
| 39 | `ciudad` | string | YES |  |
| 40 | `referenciainterna` | string | YES |  |
| 41 | `limitecredito` | double | YES |  |
| 42 | `vin` | string | YES |  |
| 43 | `descripcionseccion` | string | YES |  |
| 44 | `fechasaldado` | timestamp | YES |  |
| 45 | `estadowf` | string | YES |  |
| 46 | `pagobloqueado` | bigint | YES |  |
| 47 | `descripciondeudortipos` | string | YES |  |
| 48 | `iddeudortipos` | string | YES |  |
| 49 | `idcontctasterceropagador` | string | YES |  |
| 50 | `fechaentregavo` | timestamp | YES |  |
| 51 | `fechaentregavn` | timestamp | YES |  |
| 52 | `referencia` | string | YES |  |
| 53 | `idmonedaorigen` | bigint | YES |  |
| 54 | `factorcambiomoneda` | double | YES |  |
| 55 | `factorcambiomonedacontravalor` | double | YES |  |
| 56 | `descripcionmoneda` | string | YES |  |
| 57 | `decimalescalculomoneda` | bigint | YES |  |
| 58 | `telefonos` | string | YES |  |
| 59 | `anio` | string | YES | (particion) |
| 60 | `mes` | string | YES | (particion) |

### spiga_dbmlc_incremental.spiga_consultamovimientosreferencia

**Columnas:** 164

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `idtipolinea` | string | YES |  |
| 7 | `idmovimientotipos` | string | YES |  |
| 8 | `idmr` | string | YES |  |
| 9 | `idreferencias` | string | YES |  |
| 10 | `fechaalta` | timestamp | YES |  |
| 11 | `idempresas` | bigint | YES |  |
| 12 | `idcentros` | bigint | YES |  |
| 13 | `idsecciones` | bigint | YES |  |
| 14 | `idubicaciones` | string | YES |  |
| 15 | `stock` | double | YES |  |
| 16 | `precio` | double | YES |  |
| 17 | `pmc` | double | YES |  |
| 18 | `confirmado` | bigint | YES |  |
| 19 | `unidades` | double | YES |  |
| 20 | `dtoporc` | double | YES |  |
| 21 | `idtarifas` | bigint | YES |  |
| 22 | `idclasificacion1movimiento` | string | YES |  |
| 23 | `hostmod` | string | YES |  |
| 24 | `usermod` | bigint | YES |  |
| 25 | `fechamod` | timestamp | YES |  |
| 26 | `versionfila` | bigint | YES |  |
| 27 | `fechadocumento` | timestamp | YES |  |
| 28 | `ida±o` | string | YES |  |
| 29 | `serie` | string | YES |  |
| 30 | `numero` | string | YES |  |
| 31 | `idterceros` | bigint | YES |  |
| 32 | `numdet` | bigint | YES |  |
| 33 | `seriefactura` | string | YES |  |
| 34 | `factura` | string | YES |  |
| 35 | `a±ofactura` | string | YES |  |
| 36 | `fechafactura` | timestamp | YES |  |
| 37 | `idusuario` | bigint | YES |  |
| 38 | `loginguardadoautomatico` | bigint | YES |  |
| 39 | `hostguardadoautomatico` | string | YES |  |
| 40 | `fechaguardadoautomatico` | timestamp | YES |  |
| 41 | `loginpteconfirmar` | bigint | YES |  |
| 42 | `hostpteconfirmar` | string | YES |  |
| 43 | `fechapteconfirmar` | timestamp | YES |  |
| 44 | `idcentrosdestino` | bigint | YES |  |
| 45 | `idseccionesdestino` | bigint | YES |  |
| 46 | `idubicacionesdestino` | string | YES |  |
| 47 | `idcausaregularizacion` | bigint | YES |  |
| 48 | `idcausatraspaso` | bigint | YES |  |
| 49 | `a±oot` | string | YES |  |
| 50 | `serieot` | string | YES |  |
| 51 | `numot` | bigint | YES |  |
| 52 | `idtrabajo` | bigint | YES |  |
| 53 | `idempleadosalta` | bigint | YES |  |
| 54 | `fechacierre` | timestamp | YES |  |
| 55 | `gastosadicionales` | double | YES |  |
| 56 | `gastosadicionalesalbaran` | double | YES |  |
| 57 | `incrementopvp` | double | YES |  |
| 58 | `undenvaseventa` | double | YES |  |
| 59 | `idestadoscompras` | string | YES |  |
| 60 | `idincidenciatipos` | string | YES |  |
| 61 | `undenvasecompra` | double | YES |  |
| 62 | `codras` | string | YES |  |
| 63 | `idimputaciontipos` | bigint | YES |  |
| 64 | `idtipocompra` | bigint | YES |  |
| 65 | `portes` | string | YES |  |
| 66 | `embalajes` | string | YES |  |
| 67 | `iddepartamentodestino` | string | YES |  |
| 68 | `descripcionmovimientotipo` | string | YES |  |
| 69 | `nombreempresa` | string | YES |  |
| 70 | `nombrecentro` | string | YES |  |
| 71 | `descripcionmr` | string | YES |  |
| 72 | `descripcionseccion` | string | YES |  |
| 73 | `iddepartamentos` | string | YES |  |
| 74 | `tipocargotaller` | string | YES |  |
| 75 | `ida±oppc` | string | YES |  |
| 76 | `idserieppc` | string | YES |  |
| 77 | `numeroppc` | string | YES |  |
| 78 | `numerodetppc` | string | YES |  |
| 79 | `tasas` | string | YES |  |
| 80 | `nombretercero` | string | YES |  |
| 81 | `nifcif` | string | YES |  |
| 82 | `idclientecategorias` | string | YES |  |
| 83 | `idmotivosabono` | string | YES |  |
| 84 | `descripcioncategoriacliente` | string | YES |  |
| 85 | `nombrecentrodestino` | string | YES |  |
| 86 | `descripcionsecciondestino` | string | YES |  |
| 87 | `iddepartamentosdestino` | string | YES |  |
| 88 | `descripcioncausaregularizacion` | string | YES |  |
| 89 | `descripciontipocompra` | string | YES |  |
| 90 | `descripcioncausaabonotipo` | string | YES |  |
| 91 | `descripcionimputaciontipos` | string | YES |  |
| 92 | `nombreempleado` | string | YES |  |
| 93 | `nombrefabricante` | string | YES |  |
| 94 | `descripcionreferencia` | string | YES |  |
| 95 | `descripcioncausatraspaso` | string | YES |  |
| 96 | `idfabricantes` | string | YES |  |
| 97 | `idclasificacion1` | string | YES |  |
| 98 | `idclasificacion2` | string | YES |  |
| 99 | `idclasificacion3` | string | YES |  |
| 100 | `idclasificacion4` | string | YES |  |
| 101 | `idclasificacion5` | string | YES |  |
| 102 | `idclasificacion6` | string | YES |  |
| 103 | `iddescuentos` | string | YES |  |
| 104 | `idrutasrecogida` | string | YES |  |
| 105 | `hostrecogida` | string | YES |  |
| 106 | `fecharecogida` | timestamp | YES |  |
| 107 | `idempleadosrecogida` | string | YES |  |
| 108 | `unidadesrecogida` | string | YES |  |
| 109 | `idbultos` | string | YES |  |
| 110 | `idempleadosconfirmacion` | string | YES |  |
| 111 | `fechaconfirmacion` | timestamp | YES |  |
| 112 | `hostconfirmacion` | string | YES |  |
| 113 | `unidadesalbaran` | string | YES |  |
| 114 | `idempleadosrecepcion` | string | YES |  |
| 115 | `hostrecepcion` | string | YES |  |
| 116 | `fecharecepcion` | timestamp | YES |  |
| 117 | `unidadesrecibidas` | string | YES |  |
| 118 | `fechaubicacion` | timestamp | YES |  |
| 119 | `idempleadosubicacion` | string | YES |  |
| 120 | `hostentrega` | string | YES |  |
| 121 | `fechaentrega` | timestamp | YES |  |
| 122 | `idempleadosentrega` | string | YES |  |
| 123 | `hostubicacion` | string | YES |  |
| 124 | `nombreempleadoalta` | string | YES |  |
| 125 | `nombreempleadorecogida` | string | YES |  |
| 126 | `nombreempleadoconfirmacion` | string | YES |  |
| 127 | `nombreempleadorecepcion` | string | YES |  |
| 128 | `nombreempleadoubicacion` | string | YES |  |
| 129 | `nombreempleadoentrega` | string | YES |  |
| 130 | `descripcionincidenciatipos` | string | YES |  |
| 131 | `idpedidotipoventas` | string | YES |  |
| 132 | `descripcionpedidotipoventas` | string | YES |  |
| 133 | `nombremecanico` | string | YES |  |
| 134 | `nombretercerotrabajo` | string | YES |  |
| 135 | `apellido1tercerotrabajo` | string | YES |  |
| 136 | `apellido2tercerotrabajo` | string | YES |  |
| 137 | `nombrecomercialtercerotrabajo` | string | YES |  |
| 138 | `ventaespecial` | bigint | YES |  |
| 139 | `idtercerostrabajo` | string | YES |  |
| 140 | `codigobulto` | string | YES |  |
| 141 | `volumen` | double | YES |  |
| 142 | `factorcambiopmcontravalor` | double | YES |  |
| 143 | `descripcionclasificacion1` | string | YES |  |
| 144 | `descripcionclasificacion2` | string | YES |  |
| 145 | `descripcionclasificacion3` | string | YES |  |
| 146 | `descripcionclasificacion4` | string | YES |  |
| 147 | `descripcionclasificacion5` | string | YES |  |
| 148 | `descripcionclasificacion6` | string | YES |  |
| 149 | `descripcionclasificacion1movimiento` | string | YES |  |
| 150 | `preciocompra` | string | YES |  |
| 151 | `idmonedas` | string | YES |  |
| 152 | `factorcambiomoneda` | string | YES |  |
| 153 | `idusuariosautorizacion` | string | YES |  |
| 154 | `nombreusuarioautorizacion` | string | YES |  |
| 155 | `idnegociotipos` | string | YES |  |
| 156 | `nombreempleadovendedorrecambios` | string | YES |  |
| 157 | `seriefacturataller` | string | YES |  |
| 158 | `numerofacturataller` | string | YES |  |
| 159 | `a±ofacturataller` | string | YES |  |
| 160 | `fechafacturataller` | timestamp | YES |  |
| 161 | `vin` | string | YES |  |
| 162 | `descripcionpedidotipocompras` | string | YES |  |
| 163 | `anio` | string | YES | (particion) |
| 164 | `mes` | string | YES | (particion) |

### spiga_dbmlc_incremental.spiga_cotizacionesvn

**Columnas:** 82

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `fkofertasestados` | bigint | YES |  |
| 7 | `idempresas` | bigint | YES |  |
| 8 | `idcentros` | bigint | YES |  |
| 9 | `idofertas` | bigint | YES |  |
| 10 | `idterceros` | bigint | YES |  |
| 11 | `idclientespotentradas` | bigint | YES |  |
| 12 | `idmodulos` | string | YES |  |
| 13 | `totaloferta` | double | YES |  |
| 14 | `nombremarca` | string | YES |  |
| 15 | `nombregama` | string | YES |  |
| 16 | `fechacontrato` | timestamp | YES |  |
| 17 | `numcontrato` | string | YES |  |
| 18 | `idventatipos` | string | YES |  |
| 19 | `fechaprevista` | timestamp | YES |  |
| 20 | `numpedidovnreserva` | string | YES |  |
| 21 | `observacionesinternas` | string | YES |  |
| 22 | `observacionesexternas` | string | YES |  |
| 23 | `idmonedas` | bigint | YES |  |
| 24 | `factorcambiomoneda` | double | YES |  |
| 25 | `fechaalta` | timestamp | YES |  |
| 26 | `a±ooferta` | string | YES |  |
| 27 | `serieoferta` | string | YES |  |
| 28 | `numoferta` | string | YES |  |
| 29 | `idcentrospedido` | bigint | YES |  |
| 30 | `idventamarcatipos` | string | YES |  |
| 31 | `diasentregafabrica` | bigint | YES |  |
| 32 | `vin` | string | YES |  |
| 33 | `matricula` | string | YES |  |
| 34 | `nombre` | string | YES |  |
| 35 | `idmarcas` | bigint | YES |  |
| 36 | `idgamas` | bigint | YES |  |
| 37 | `codmodelo` | string | YES |  |
| 38 | `extmodelo` | string | YES |  |
| 39 | `a±omodelo` | string | YES |  |
| 40 | `idversiones` | string | YES |  |
| 41 | `idtarifas` | bigint | YES |  |
| 42 | `codexternomodelo` | string | YES |  |
| 43 | `nombrecentro` | string | YES |  |
| 44 | `fechabajacliente` | timestamp | YES |  |
| 45 | `telefonomovil` | string | YES |  |
| 46 | `email` | string | YES |  |
| 47 | `fechaautorizacion` | timestamp | YES |  |
| 48 | `fechaaceptacion` | timestamp | YES |  |
| 49 | `fechaventa` | timestamp | YES |  |
| 50 | `nombrevendedorasignado` | string | YES |  |
| 51 | `importesaldado` | double | YES |  |
| 52 | `idplantillacalculo` | string | YES |  |
| 53 | `descripcionplantilla` | string | YES |  |
| 54 | `importevoacambio` | double | YES |  |
| 55 | `nifcifclientepot` | string | YES |  |
| 56 | `importe` | double | YES |  |
| 57 | `porcentaje` | double | YES |  |
| 58 | `nombrevendedor` | string | YES |  |
| 59 | `pkopcionales` | string | YES |  |
| 60 | `idimsconcesionarios` | bigint | YES |  |
| 61 | `idimscuentas` | bigint | YES |  |
| 62 | `idimssucursales` | bigint | YES |  |
| 63 | `idimsvendedores` | bigint | YES |  |
| 64 | `nombreimsvendedor` | string | YES |  |
| 65 | `idsecciones` | bigint | YES |  |
| 66 | `fechasalida` | timestamp | YES |  |
| 67 | `vosentregados` | bigint | YES |  |
| 68 | `idvehiculos` | bigint | YES |  |
| 69 | `codclientepot` | bigint | YES |  |
| 70 | `descripcion` | string | YES |  |
| 71 | `nombremodelo` | string | YES |  |
| 72 | `nombreversion` | string | YES |  |
| 73 | `descripcionofertasestados` | string | YES |  |
| 74 | `descripcionsecciones` | string | YES |  |
| 75 | `estadofinanciacion` | string | YES |  |
| 76 | `intencionescompradescripcion` | string | YES |  |
| 77 | `clientepotclasificaciondescripcion` | string | YES |  |
| 78 | `descripcionprocedencia` | string | YES |  |
| 79 | `descripcionsalidatipos` | string | YES |  |
| 80 | `fechaentrada` | timestamp | YES |  |
| 81 | `anio` | string | YES | (particion) |
| 82 | `mes` | string | YES | (particion) |

### spiga_dbmlc_incremental.spiga_cotizacionesvo

**Columnas:** 73

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `idvehiculos` | bigint | YES |  |
| 7 | `fkofertasestados` | bigint | YES |  |
| 8 | `idempresas` | bigint | YES |  |
| 9 | `idcentros` | bigint | YES |  |
| 10 | `idofertas` | bigint | YES |  |
| 11 | `idterceros` | bigint | YES |  |
| 12 | `idclientespotentradas` | bigint | YES |  |
| 13 | `idmonedas` | bigint | YES |  |
| 14 | `factorcambiomoneda` | double | YES |  |
| 15 | `a±ooferta` | string | YES |  |
| 16 | `serieoferta` | string | YES |  |
| 17 | `numoferta` | string | YES |  |
| 18 | `idmodulos` | string | YES |  |
| 19 | `totaloferta` | double | YES |  |
| 20 | `idmarcas` | bigint | YES |  |
| 21 | `idgamas` | bigint | YES |  |
| 22 | `codmodelo` | string | YES |  |
| 23 | `extmodelo` | string | YES |  |
| 24 | `a±omodelo` | string | YES |  |
| 25 | `idversiones` | string | YES |  |
| 26 | `nombremarca` | string | YES |  |
| 27 | `nombregama` | string | YES |  |
| 28 | `serieexpedientereserva` | string | YES |  |
| 29 | `numexpedientereserva` | bigint | YES |  |
| 30 | `a±oexpedientereserva` | string | YES |  |
| 31 | `idcentrosexpedientereserva` | bigint | YES |  |
| 32 | `fechareserva` | timestamp | YES |  |
| 33 | `idofertasestados` | bigint | YES |  |
| 34 | `vin` | string | YES |  |
| 35 | `matricula` | string | YES |  |
| 36 | `nombre` | string | YES |  |
| 37 | `nombrecentro` | string | YES |  |
| 38 | `fechaautorizacion` | timestamp | YES |  |
| 39 | `fechaaceptacion` | timestamp | YES |  |
| 40 | `nombrevendedorasignado` | string | YES |  |
| 41 | `importesaldado` | double | YES |  |
| 42 | `nifcifclientepot` | string | YES |  |
| 43 | `idplantillacalculo` | string | YES |  |
| 44 | `descripcionplantilla` | string | YES |  |
| 45 | `importevoacambio` | double | YES |  |
| 46 | `codclientepot` | bigint | YES |  |
| 47 | `telefonomovil` | string | YES |  |
| 48 | `email` | string | YES |  |
| 49 | `importe` | double | YES |  |
| 50 | `porcentaje` | double | YES |  |
| 51 | `nombrevendedor` | string | YES |  |
| 52 | `idopcionalescolorvo` | string | YES |  |
| 53 | `idopcionalestapizadovo` | string | YES |  |
| 54 | `nombreempresa` | string | YES |  |
| 55 | `tercerointeresado` | bigint | YES |  |
| 56 | `idsecciones` | bigint | YES |  |
| 57 | `descripcionsecciones` | string | YES |  |
| 58 | `fechaalta` | timestamp | YES |  |
| 59 | `idopcionales` | string | YES |  |
| 60 | `descripcionprocedencia` | string | YES |  |
| 61 | `fechasalida` | timestamp | YES |  |
| 62 | `vosentregados` | bigint | YES |  |
| 63 | `nombremodelo` | string | YES |  |
| 64 | `nombreversion` | string | YES |  |
| 65 | `descripcion` | string | YES |  |
| 66 | `descripcioncolorvo` | string | YES |  |
| 67 | `descripciontapizadovo` | string | YES |  |
| 68 | `descripcionofertaestados` | string | YES |  |
| 69 | `intencionescompradescripcion` | string | YES |  |
| 70 | `clientepotclasificaciondescripcion` | string | YES |  |
| 71 | `descripcionsalidatipos` | string | YES |  |
| 72 | `anio` | string | YES | (particion) |
| 73 | `mes` | string | YES | (particion) |

### spiga_dbmlc_incremental.spiga_entradasataller

**Columnas:** 120

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | string | YES |  |
| 2 | `idconsecutivo` | string | YES |  |
| 3 | `ano_periodo` | string | YES |  |
| 4 | `mes_periodo` | string | YES |  |
| 5 | `fechadecorte` | string | YES |  |
| 6 | `idempresas` | string | YES |  |
| 7 | `idcentros` | string | YES |  |
| 8 | `a±oot` | string | YES |  |
| 9 | `serieot` | string | YES |  |
| 10 | `numot` | string | YES |  |
| 11 | `numtrabajo` | string | YES |  |
| 12 | `idtrabajoestados` | string | YES |  |
| 13 | `descripcion` | string | YES |  |
| 14 | `idterceros` | string | YES |  |
| 15 | `preciohora` | string | YES |  |
| 16 | `numeropoliza` | string | YES |  |
| 17 | `importefranquicia` | string | YES |  |
| 18 | `idmanoobratipos` | string | YES |  |
| 19 | `idtrabajotipos` | string | YES |  |
| 20 | `idsecciones` | string | YES |  |
| 21 | `nombreseccion` | string | YES |  |
| 22 | `preciocoste` | string | YES |  |
| 23 | `idseccioncargos` | string | YES |  |
| 24 | `idcargotipos` | string | YES |  |
| 25 | `observaciones` | string | YES |  |
| 26 | `fechaalta` | string | YES |  |
| 27 | `fechamodificacion` | string | YES |  |
| 28 | `fechacierre` | string | YES |  |
| 29 | `a±opresupuesto` | string | YES |  |
| 30 | `seriepresupuesto` | string | YES |  |
| 31 | `idpresupuesto` | string | YES |  |
| 32 | `a±ofactura` | string | YES |  |
| 33 | `seriefactura` | string | YES |  |
| 34 | `numfactura` | string | YES |  |
| 35 | `iddepartamentocargointerno` | string | YES |  |
| 36 | `idimputaciontipos` | string | YES |  |
| 37 | `idseccioncargointerno` | string | YES |  |
| 38 | `idcentrosdestino` | string | YES |  |
| 39 | `idseriesgarantias` | string | YES |  |
| 40 | `numgarantias` | string | YES |  |
| 41 | `a±ogarantias` | string | YES |  |
| 42 | `idempleadosalta` | string | YES |  |
| 43 | `idempleadoscierre` | string | YES |  |
| 44 | `fechaenvioinspeccion` | string | YES |  |
| 45 | `fechafacturacion` | string | YES |  |
| 46 | `numeroautorizacion` | string | YES |  |
| 47 | `usermod` | string | YES |  |
| 48 | `hostmod` | string | YES |  |
| 49 | `versionfila` | string | YES |  |
| 50 | `a±oasiento` | string | YES |  |
| 51 | `idasiento` | string | YES |  |
| 52 | `a±oasiento_garantiafacturada` | string | YES |  |
| 53 | `idasiento_garantiafacturada` | string | YES |  |
| 54 | `trabajorepetido` | string | YES |  |
| 55 | `numsiniestro` | string | YES |  |
| 56 | `respuestainspeccion` | string | YES |  |
| 57 | `numgarantiamarca` | string | YES |  |
| 58 | `importemo` | string | YES |  |
| 59 | `importemopresupuesto` | string | YES |  |
| 60 | `importemat` | string | YES |  |
| 61 | `importematpresupuesto` | string | YES |  |
| 62 | `importesub` | string | YES |  |
| 63 | `importesubpresupuesto` | string | YES |  |
| 64 | `importevar` | string | YES |  |
| 65 | `importevarpresupuesto` | string | YES |  |
| 66 | `importepint` | string | YES |  |
| 67 | `importepintpresupuesto` | string | YES |  |
| 68 | `horasmo` | string | YES |  |
| 69 | `horasmopresupuesto` | string | YES |  |
| 70 | `fechaentrada` | string | YES |  |
| 71 | `idcalletipos` | string | YES |  |
| 72 | `matricula` | string | YES |  |
| 73 | `vin` | string | YES |  |
| 74 | `fechamatriculacion` | string | YES |  |
| 75 | `idmarcas` | string | YES |  |
| 76 | `nombremarca` | string | YES |  |
| 77 | `idgamas` | string | YES |  |
| 78 | `nombregama` | string | YES |  |
| 79 | `nombreasesor` | string | YES |  |
| 80 | `nombrepropietario` | string | YES |  |
| 81 | `telefonoparticular` | string | YES |  |
| 82 | `telefonomovil` | string | YES |  |
| 83 | `idempleados` | string | YES |  |
| 84 | `descripciontrabajotipos` | string | YES |  |
| 85 | `diferenciadias` | string | YES |  |
| 86 | `descripcionsegmento` | string | YES |  |
| 87 | `email` | string | YES |  |
| 88 | `descripciontipocalle` | string | YES |  |
| 89 | `nombrecalle` | string | YES |  |
| 90 | `numero` | string | YES |  |
| 91 | `bloque` | string | YES |  |
| 92 | `piso` | string | YES |  |
| 93 | `puerta` | string | YES |  |
| 94 | `complemento` | string | YES |  |
| 95 | `complemento2` | string | YES |  |
| 96 | `poblacion` | string | YES |  |
| 97 | `idcodigospostales` | string | YES |  |
| 98 | `nombreestado` | string | YES |  |
| 99 | `esabono` | string | YES |  |
| 100 | `esabonogarantia` | string | YES |  |
| 101 | `idrecepciontipos` | string | YES |  |
| 102 | `kmts` | string | YES |  |
| 103 | `fechaprevistaentrega` | string | YES |  |
| 104 | `fechaentrega` | string | YES |  |
| 105 | `idvehiculos` | string | YES |  |
| 106 | `nombretercerocargo` | string | YES |  |
| 107 | `apellido1tercerocargo` | string | YES |  |
| 108 | `apellido2tercerocargo` | string | YES |  |
| 109 | `nombrevendedor` | string | YES |  |
| 110 | `apellido1vendedor` | string | YES |  |
| 111 | `apellido2vendedor` | string | YES |  |
| 112 | `descripcionrecepcion` | string | YES |  |
| 113 | `idclientespotclasificaciones` | string | YES |  |
| 114 | `horasuso` | string | YES |  |
| 115 | `idmotivoentrada` | string | YES |  |
| 116 | `descripcionmotivoentrada` | string | YES |  |
| 117 | `asesorservicioresponsable` | string | YES |  |
| 118 | `vehiculocortesia` | string | YES |  |
| 119 | `anio` | string | YES | (particion) |
| 120 | `mes` | string | YES | (particion) |

### spiga_dbmlc_incremental.spiga_fechaprevistacompra

**Columnas:** 46

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `idempresa` | bigint | YES |  |
| 7 | `idterceros` | bigint | YES |  |
| 8 | `nombre` | string | YES |  |
| 9 | `apellido1` | string | YES |  |
| 10 | `apellido2` | string | YES |  |
| 11 | `nifcif` | string | YES |  |
| 12 | `nombrecalle` | string | YES |  |
| 13 | `numero` | string | YES |  |
| 14 | `bloque` | string | YES |  |
| 15 | `piso` | string | YES |  |
| 16 | `puerta` | string | YES |  |
| 17 | `idcodigospostales` | string | YES |  |
| 18 | `poblacion` | string | YES |  |
| 19 | `provincia` | string | YES |  |
| 20 | `complemento` | string | YES |  |
| 21 | `complemento2` | string | YES |  |
| 22 | `idpaises` | string | YES |  |
| 23 | `idcalletipos` | string | YES |  |
| 24 | `descripcioncalletipos` | string | YES |  |
| 25 | `telefono` | string | YES |  |
| 26 | `email` | string | YES |  |
| 27 | `fechaprevistacambio` | timestamp | YES |  |
| 28 | `fechaentrada` | timestamp | YES |  |
| 29 | `idempleados` | bigint | YES |  |
| 30 | `nombreempleado` | string | YES |  |
| 31 | `descripcionentradatipos` | string | YES |  |
| 32 | `nombremodelo` | string | YES |  |
| 33 | `fechaalta` | timestamp | YES |  |
| 34 | `idsecciones` | bigint | YES |  |
| 35 | `descripcion` | string | YES |  |
| 36 | `nombregama` | string | YES |  |
| 37 | `nombrecentro` | string | YES |  |
| 38 | `descripcionseccion` | string | YES |  |
| 39 | `fechaultimaactividad` | timestamp | YES |  |
| 40 | `idclientespotclasificaciones` | bigint | YES |  |
| 41 | `fechasalida` | timestamp | YES |  |
| 42 | `idsalidatipos` | string | YES |  |
| 43 | `idintencionescompra` | string | YES |  |
| 44 | `descripcion_intencionescompra` | string | YES |  |
| 45 | `anio` | string | YES | (particion) |
| 46 | `mes` | string | YES | (particion) |

### spiga_dbmlc_incremental.spiga_informafacturacion

**Columnas:** 131

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `tipo` | string | YES |  |
| 7 | `idempresas` | bigint | YES |  |
| 8 | `idcentros` | bigint | YES |  |
| 9 | `a±oot` | string | YES |  |
| 10 | `serieot` | string | YES |  |
| 11 | `numot` | bigint | YES |  |
| 12 | `numtrabajo` | bigint | YES |  |
| 13 | `idempleadocierre` | bigint | YES |  |
| 14 | `fechaalta` | timestamp | YES |  |
| 15 | `fechacierre` | timestamp | YES |  |
| 16 | `idseriesgarantias` | string | YES |  |
| 17 | `numalbaran` | bigint | YES |  |
| 18 | `a±oalbaran` | string | YES |  |
| 19 | `numgarantiamarca` | string | YES |  |
| 20 | `horasfacturadas` | bigint | YES |  |
| 21 | `importemobruto` | double | YES |  |
| 22 | `descuentomo` | double | YES |  |
| 23 | `importesubbruto` | double | YES |  |
| 24 | `descuentosub` | double | YES |  |
| 25 | `importevarbruto` | double | YES |  |
| 26 | `descuentovar` | double | YES |  |
| 27 | `importepintbruto` | double | YES |  |
| 28 | `descuentopint` | double | YES |  |
| 29 | `importematerialbruto` | double | YES |  |
| 30 | `descuentomaterial` | double | YES |  |
| 31 | `importemoaceptada` | double | YES |  |
| 32 | `importesubaceptada` | double | YES |  |
| 33 | `importevaraceptada` | double | YES |  |
| 34 | `importepintaceptada` | double | YES |  |
| 35 | `importematerialaceptada` | double | YES |  |
| 36 | `idcargotipos` | string | YES |  |
| 37 | `idmanoobratipos` | bigint | YES |  |
| 38 | `iddepartamentocargointerno` | string | YES |  |
| 39 | `idsecciones` | bigint | YES |  |
| 40 | `idvehiculos` | bigint | YES |  |
| 41 | `matricula` | string | YES |  |
| 42 | `vin` | string | YES |  |
| 43 | `idmarcas` | bigint | YES |  |
| 44 | `idgamas` | bigint | YES |  |
| 45 | `fechadespacho` | timestamp | YES |  |
| 46 | `nombremarcas` | string | YES |  |
| 47 | `nombregamas` | string | YES |  |
| 48 | `a±ofactura` | string | YES |  |
| 49 | `seriefactura` | string | YES |  |
| 50 | `numfactura` | string | YES |  |
| 51 | `idtercerofactura` | bigint | YES |  |
| 52 | `nombretercero` | string | YES |  |
| 53 | `idterceroaux` | bigint | YES |  |
| 54 | `nombreterceroaux` | string | YES |  |
| 55 | `idpagoformatipos` | string | YES |  |
| 56 | `idpagoformas` | string | YES |  |
| 57 | `descripcionpagoformas` | string | YES |  |
| 58 | `descripcionpagoformatipos` | string | YES |  |
| 59 | `fechafactura` | timestamp | YES |  |
| 60 | `tipopago` | string | YES |  |
| 61 | `costesub` | double | YES |  |
| 62 | `costemo` | double | YES |  |
| 63 | `costemochapa` | double | YES |  |
| 64 | `costemopintura` | double | YES |  |
| 65 | `costemoresto` | string | YES |  |
| 66 | `costemat` | double | YES |  |
| 67 | `importetasasmat` | double | YES |  |
| 68 | `diasreparacion` | bigint | YES |  |
| 69 | `costepint` | double | YES |  |
| 70 | `importemochapa` | double | YES |  |
| 71 | `importemopintura` | double | YES |  |
| 72 | `importemoresto` | string | YES |  |
| 73 | `idtallerpagotipos` | string | YES |  |
| 74 | `descripciontallerpagotipos` | string | YES |  |
| 75 | `idempleados` | bigint | YES |  |
| 76 | `descripcionrecepciontipos` | string | YES |  |
| 77 | `kmts` | bigint | YES |  |
| 78 | `a±omodelo` | string | YES |  |
| 79 | `idterceropropietario` | bigint | YES |  |
| 80 | `descripciontrabajo` | string | YES |  |
| 81 | `diasabierto` | double | YES |  |
| 82 | `numeroautorizacion` | string | YES |  |
| 83 | `numsiniestro` | string | YES |  |
| 84 | `fechaentrega` | timestamp | YES |  |
| 85 | `idtercerocargo` | bigint | YES |  |
| 86 | `nombretercerocargo` | string | YES |  |
| 87 | `idseccioncargos` | string | YES |  |
| 88 | `idimputaciontipos` | bigint | YES |  |
| 89 | `idseccioncargointerno` | bigint | YES |  |
| 90 | `idcentrosdestino` | bigint | YES |  |
| 91 | `trabajorepetido` | bigint | YES |  |
| 92 | `a±opresupuesto` | string | YES |  |
| 93 | `seriepresupuesto` | string | YES |  |
| 94 | `idpresupuesto` | bigint | YES |  |
| 95 | `descripcionseccioncargos` | string | YES |  |
| 96 | `idempleadosrec` | bigint | YES |  |
| 97 | `idempleadosretirada` | bigint | YES |  |
| 98 | `idempleadosresponsable` | bigint | YES |  |
| 99 | `a±opedidosservicios` | string | YES |  |
| 100 | `seriepedidosservicios` | string | YES |  |
| 101 | `idpedidosservicios` | bigint | YES |  |
| 102 | `idmarcastallercampa±asbastidoresafectados` | bigint | YES |  |
| 103 | `idcampa±as` | string | YES |  |
| 104 | `idcampa±avariante` | string | YES |  |
| 105 | `idubicaciones` | string | YES |  |
| 106 | `reclamadomo` | double | YES |  |
| 107 | `reclamadomat` | double | YES |  |
| 108 | `reclamadosub` | double | YES |  |
| 109 | `reclamadovar` | double | YES |  |
| 110 | `reclamadopint` | double | YES |  |
| 111 | `idcentrosdeferencia` | bigint | YES |  |
| 112 | `ida±ootdeferencia` | string | YES |  |
| 113 | `idseriesdeferencia` | string | YES |  |
| 114 | `idnumotdeferencia` | bigint | YES |  |
| 115 | `idnumtrabajodeferencia` | bigint | YES |  |
| 116 | `idserviciotipos` | bigint | YES |  |
| 117 | `idgradosaveria` | bigint | YES |  |
| 118 | `idgradoaveriaordentrabajo` | bigint | YES |  |
| 119 | `idtrabajotipos` | string | YES |  |
| 120 | `idtrabajotiposmarca` | string | YES |  |
| 121 | `sureferencia` | string | YES |  |
| 122 | `horasuso` | bigint | YES |  |
| 123 | `fechaaltaot` | timestamp | YES |  |
| 124 | `numfacturaexterna` | string | YES |  |
| 125 | `observaciones` | string | YES |  |
| 126 | `descripciondepartamentoimputaciontipos` | string | YES |  |
| 127 | `descripcionimputaciontipos` | string | YES |  |
| 128 | `descripcionseccionimputaciontipos` | string | YES |  |
| 129 | `nombrecentroimputaciontipos` | string | YES |  |
| 130 | `anio` | string | YES | (particion) |
| 131 | `mes` | string | YES | (particion) |

### spiga_dbmlc_incremental.spiga_ofertasdefinanciacionfechamod

**Columnas:** 53

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `ida±oofertasfinanciacion` | string | YES |  |
| 8 | `idseriesofertasfinanciacion` | string | YES |  |
| 9 | `idnumofertasfinanciacion` | bigint | YES |  |
| 10 | `idcentros` | bigint | YES |  |
| 11 | `nombreempresa` | string | YES |  |
| 12 | `nombrecentro` | string | YES |  |
| 13 | `nombremarca` | string | YES |  |
| 14 | `nombregama` | string | YES |  |
| 15 | `codmodelo` | string | YES |  |
| 16 | `nombremodelo` | string | YES |  |
| 17 | `idterceros` | bigint | YES |  |
| 18 | `nombretercero` | string | YES |  |
| 19 | `apellido1tercero` | string | YES |  |
| 20 | `apellido2tercero` | string | YES |  |
| 21 | `idofertasfinanciacionproductotiposdescripcion` | string | YES |  |
| 22 | `idofertasfinanciacionestadosdescripcion` | string | YES |  |
| 23 | `fechavalidez` | timestamp | YES |  |
| 24 | `fechainiciofinanciacion` | timestamp | YES |  |
| 25 | `fechafinfinanciacion` | timestamp | YES |  |
| 26 | `importefinanciar` | double | YES |  |
| 27 | `cuotamensual` | double | YES |  |
| 28 | `meses` | bigint | YES |  |
| 29 | `porcsobreimportetotal` | double | YES |  |
| 30 | `capitalpreconcedido` | double | YES |  |
| 31 | `porcintereses` | double | YES |  |
| 32 | `importecomisionapertura` | double | YES |  |
| 33 | `porccomisionapertura` | double | YES |  |
| 34 | `obligaaval` | bigint | YES |  |
| 35 | `aval` | string | YES |  |
| 36 | `importecomisionobtencionfinanciacion` | double | YES |  |
| 37 | `porccomisionobtencionfinanciacion` | double | YES |  |
| 38 | `idtercerosfinanciera` | bigint | YES |  |
| 39 | `nombretercerofinanciera` | string | YES |  |
| 40 | `apellido1tercerofinanciera` | string | YES |  |
| 41 | `apellido2tercerofinanciera` | string | YES |  |
| 42 | `idofertasfinanciacionproductotipos` | bigint | YES |  |
| 43 | `idofertasfinanciacionestados` | bigint | YES |  |
| 44 | `fechaalta` | timestamp | YES |  |
| 45 | `idofertasfinanciacionfinanciaciones` | bigint | YES |  |
| 46 | `idempleados` | bigint | YES |  |
| 47 | `nombreempleado` | string | YES |  |
| 48 | `apellido1empleado` | string | YES |  |
| 49 | `apellido2empleado` | string | YES |  |
| 50 | `importefranquicia` | double | YES |  |
| 51 | `fechamod` | timestamp | YES |  |
| 52 | `anio` | string | YES | (particion) |
| 53 | `mes` | string | YES | (particion) |

### spiga_dbmlc_incremental.spiga_remisionesderepuestos

**Columnas:** 27

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `empresacentrosecciones` | string | YES |  |
| 8 | `idcentros` | bigint | YES |  |
| 9 | `centro` | string | YES |  |
| 10 | `idsecciones` | bigint | YES |  |
| 11 | `seccion` | string | YES |  |
| 12 | `fechaalta` | timestamp | YES |  |
| 13 | `idmovimientotipos` | string | YES |  |
| 14 | `movimientotipos` | string | YES |  |
| 15 | `prefijo` | string | YES |  |
| 16 | `numero` | string | YES |  |
| 17 | `a±o` | string | YES |  |
| 18 | `a±oot` | string | YES |  |
| 19 | `serieot` | string | YES |  |
| 20 | `numot` | bigint | YES |  |
| 21 | `idpedidotipoventas` | bigint | YES |  |
| 22 | `a±opedido` | string | YES |  |
| 23 | `seriepedido` | string | YES |  |
| 24 | `pedido` | bigint | YES |  |
| 25 | `tipocargo` | string | YES |  |
| 26 | `anio` | string | YES | (particion) |
| 27 | `mes` | string | YES | (particion) |

### spiga_dbmlc_incremental.spiga_rentabilidaddetalladavehiculosnuevos

**Columnas:** 54

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | int | YES |  |
| 2 | `idconsecutivo` | int | YES |  |
| 3 | `ano_periodo` | int | YES |  |
| 4 | `mes_periodo` | int | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `idempresas` | smallint | YES |  |
| 7 | `a±oexpediente` | string | YES |  |
| 8 | `serieexpediente` | string | YES |  |
| 9 | `numexpediente` | int | YES |  |
| 10 | `numventa` | smallint | YES |  |
| 11 | `idventasabonado` | smallint | YES |  |
| 12 | `nombrecentro` | string | YES |  |
| 13 | `seccion` | string | YES |  |
| 14 | `marca` | string | YES |  |
| 15 | `gama` | string | YES |  |
| 16 | `codmodelo` | string | YES |  |
| 17 | `modelo` | string | YES |  |
| 18 | `vin` | string | YES |  |
| 19 | `tipocompra` | string | YES |  |
| 20 | `idterceroscompra` | int | YES |  |
| 21 | `nombretercerocompra` | string | YES |  |
| 22 | `apellido1tercerocompra` | string | YES |  |
| 23 | `apellido2tercerocompra` | string | YES |  |
| 24 | `fechafacturacompra` | timestamp | YES |  |
| 25 | `seriefacturacompra` | string | YES |  |
| 26 | `numfacturacompra` | string | YES |  |
| 27 | `a±ofacturacompra` | string | YES |  |
| 28 | `diasstock` | int | YES |  |
| 29 | `tipoventa` | string | YES |  |
| 30 | `fechaventa` | timestamp | YES |  |
| 31 | `seriefacturaventa` | string | YES |  |
| 32 | `numfacturaventa` | string | YES |  |
| 33 | `a±ofacturaventa` | string | YES |  |
| 34 | `nombrevendedor` | string | YES |  |
| 35 | `apellido1vendedor` | string | YES |  |
| 36 | `apellido2vendedor` | string | YES |  |
| 37 | `importecompra` | decimal(38,14) | YES |  |
| 38 | `importegasto` | decimal(38,13) | YES |  |
| 39 | `idcompragastoadicionaltipos` | string | YES |  |
| 40 | `idcompragastoadicionaltiposdescripcion` | string | YES |  |
| 41 | `otroscargos` | decimal(38,19) | YES |  |
| 42 | `otrosingresos` | decimal(38,19) | YES |  |
| 43 | `importeventa` | decimal(38,6) | YES |  |
| 44 | `importeseguros` | decimal(38,14) | YES |  |
| 45 | `importegarantias` | decimal(38,14) | YES |  |
| 46 | `importematriculacion` | decimal(38,14) | YES |  |
| 47 | `importetransferencia` | decimal(38,14) | YES |  |
| 48 | `importecampa±as` | decimal(38,14) | YES |  |
| 49 | `importeprestamo` | decimal(38,4) | YES |  |
| 50 | `matricula` | string | YES |  |
| 51 | `fechaabono` | timestamp | YES |  |
| 52 | `fechamatriculacion` | timestamp | YES |  |
| 53 | `anio` | string | YES | (particion) |
| 54 | `mes` | string | YES | (particion) |

### spiga_dbmlc_incremental.spiga_rentabilidaddetalladavehiculosusados

**Columnas:** 53

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | int | YES |  |
| 2 | `idconsecutivo` | int | YES |  |
| 3 | `ano_periodo` | int | YES |  |
| 4 | `mes_periodo` | int | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `idempresas` | smallint | YES |  |
| 7 | `serieexpediente` | string | YES |  |
| 8 | `numexpediente` | int | YES |  |
| 9 | `a±oexpediente` | string | YES |  |
| 10 | `numventa` | smallint | YES |  |
| 11 | `idventasabonado` | smallint | YES |  |
| 12 | `nombrecentro` | string | YES |  |
| 13 | `seccion` | string | YES |  |
| 14 | `marca` | string | YES |  |
| 15 | `gama` | string | YES |  |
| 16 | `codmodelo` | string | YES |  |
| 17 | `modelo` | string | YES |  |
| 18 | `vin` | string | YES |  |
| 19 | `tipocompra` | string | YES |  |
| 20 | `idterceroscompra` | int | YES |  |
| 21 | `nombretercerocompra` | string | YES |  |
| 22 | `apellido1tercerocompra` | string | YES |  |
| 23 | `apellido2tercerocompra` | string | YES |  |
| 24 | `fechafacturacompra` | timestamp | YES |  |
| 25 | `seriefacturacompra` | string | YES |  |
| 26 | `numfacturacompra` | string | YES |  |
| 27 | `a±ofacturacompra` | string | YES |  |
| 28 | `diasstock` | int | YES |  |
| 29 | `tipoventa` | string | YES |  |
| 30 | `fechaventa` | timestamp | YES |  |
| 31 | `seriefacturaventa` | string | YES |  |
| 32 | `numfacturaventa` | string | YES |  |
| 33 | `a±ofacturaventa` | string | YES |  |
| 34 | `nombrevendedor` | string | YES |  |
| 35 | `apellido1vendedor` | string | YES |  |
| 36 | `apellido2vendedor` | string | YES |  |
| 37 | `importecompra` | decimal(38,14) | YES |  |
| 38 | `importegasto` | decimal(38,13) | YES |  |
| 39 | `idcompragastoadicionaltipos` | string | YES |  |
| 40 | `idcompragastoadicionaltiposdescripcion` | string | YES |  |
| 41 | `otroscargos` | decimal(38,19) | YES |  |
| 42 | `otrosingresos` | decimal(38,19) | YES |  |
| 43 | `importeventa` | decimal(29,4) | YES |  |
| 44 | `importeseguros` | decimal(18,4) | YES |  |
| 45 | `importegarantias` | decimal(18,4) | YES |  |
| 46 | `importematriculacion` | decimal(18,4) | YES |  |
| 47 | `importetransferencia` | decimal(18,4) | YES |  |
| 48 | `importeprestamo` | decimal(38,4) | YES |  |
| 49 | `matricula` | string | YES |  |
| 50 | `fechaabono` | timestamp | YES |  |
| 51 | `importeprovisionadogarantias` | decimal(18,4) | YES |  |
| 52 | `anio` | string | YES | (particion) |
| 53 | `mes` | string | YES | (particion) |

### spiga_dbmlc_incremental.spiga_stockrepuestos

**Columnas:** 62

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `idsecciones` | bigint | YES |  |
| 9 | `idmr` | string | YES |  |
| 10 | `idreferencias` | string | YES |  |
| 11 | `idtarifas` | bigint | YES |  |
| 12 | `stockmax` | double | YES |  |
| 13 | `preciomedio` | double | YES |  |
| 14 | `clasificacionabc` | string | YES |  |
| 15 | `stock` | double | YES |  |
| 16 | `numubicaciones` | bigint | YES |  |
| 17 | `ventasmesactualsalidas` | bigint | YES |  |
| 18 | `undpterecibir` | double | YES |  |
| 19 | `idubicaciones` | string | YES |  |
| 20 | `ventasmesactual` | double | YES |  |
| 21 | `ventasmes1` | double | YES |  |
| 22 | `ventasmes2` | double | YES |  |
| 23 | `ventasmes3` | double | YES |  |
| 24 | `ventasmes4` | double | YES |  |
| 25 | `ventasmes5` | double | YES |  |
| 26 | `ventasmes6` | double | YES |  |
| 27 | `ventasmes7` | double | YES |  |
| 28 | `ventasmes8` | double | YES |  |
| 29 | `ventasmes9` | double | YES |  |
| 30 | `ventasmes10` | double | YES |  |
| 31 | `ventasmes11` | double | YES |  |
| 32 | `ventasmes12` | double | YES |  |
| 33 | `descripcion` | string | YES |  |
| 34 | `precioventa` | double | YES |  |
| 35 | `observaciones` | string | YES |  |
| 36 | `idclasificacion1` | string | YES |  |
| 37 | `idclasificacion2` | string | YES |  |
| 38 | `idclasificacion3` | string | YES |  |
| 39 | `idclasificacion4` | string | YES |  |
| 40 | `idclasificacion5` | string | YES |  |
| 41 | `idclasificacion6` | string | YES |  |
| 42 | `iddescuentos` | string | YES |  |
| 43 | `fechaultimaventa` | timestamp | YES |  |
| 44 | `fechaultimacompra` | timestamp | YES |  |
| 45 | `fechaultimaregularizacion` | timestamp | YES |  |
| 46 | `fechatraspasotre` | timestamp | YES |  |
| 47 | `fechatraspasotrs` | timestamp | YES |  |
| 48 | `denominacionclasificacion1` | string | YES |  |
| 49 | `denominacionclasificacion2` | string | YES |  |
| 50 | `denominacionclasificacion3` | string | YES |  |
| 51 | `denominacionclasificacion4` | string | YES |  |
| 52 | `denominacionclasificacion5` | string | YES |  |
| 53 | `denominacionclasificacion6` | string | YES |  |
| 54 | `fechaalta` | timestamp | YES |  |
| 55 | `fechabaja` | timestamp | YES |  |
| 56 | `stockmin` | double | YES |  |
| 57 | `undpteentregar` | double | YES |  |
| 58 | `undreservadaspteentregar` | double | YES |  |
| 59 | `undenvasecompra` | double | YES |  |
| 60 | `undenvaseventa` | double | YES |  |
| 61 | `anio` | string | YES | (particion) |
| 62 | `mes` | string | YES | (particion) |

### spiga_dbmlc_incremental.spiga_tiempostallerpicajesots

**Columnas:** 33

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `idempleados` | bigint | YES |  |
| 9 | `fechainicio` | timestamp | YES |  |
| 10 | `fechafin` | timestamp | YES |  |
| 11 | `idpicajetrabajotipos` | string | YES |  |
| 12 | `matricula` | string | YES |  |
| 13 | `serieot` | string | YES |  |
| 14 | `numot` | bigint | YES |  |
| 15 | `a±oot` | string | YES |  |
| 16 | `numtrabajo` | bigint | YES |  |
| 17 | `tiempoempleado` | double | YES |  |
| 18 | `fechainicioaux` | timestamp | YES |  |
| 19 | `fechafinaux` | timestamp | YES |  |
| 20 | `tiempoaux` | double | YES |  |
| 21 | `nombreempleado` | string | YES |  |
| 22 | `descripcionpicajetrabajotipos` | string | YES |  |
| 23 | `idmanoobratipos` | bigint | YES |  |
| 24 | `descripcionmanoobratipos` | string | YES |  |
| 25 | `recuperable` | bigint | YES |  |
| 26 | `afectataller` | bigint | YES |  |
| 27 | `idclasificacionincidenciatipos` | bigint | YES |  |
| 28 | `idrevisionpicajetipos` | string | YES |  |
| 29 | `useraux` | bigint | YES |  |
| 30 | `idsecciones` | bigint | YES |  |
| 31 | `fechabaja` | timestamp | YES |  |
| 32 | `anio` | string | YES | (particion) |
| 33 | `mes` | string | YES | (particion) |

### spiga_dbmlc_incremental.spiga_trasladosderepuestospendientes

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp | YES |  |
| 6 | `idempresas_salida` | bigint | YES |  |
| 7 | `idcentros_salida` | bigint | YES |  |
| 8 | `a±otraspaso_salida` | string | YES |  |
| 9 | `serietraspaso_salida` | string | YES |  |
| 10 | `numtraspaso_salida` | bigint | YES |  |
| 11 | `numdettraspaso_salida` | bigint | YES |  |
| 12 | `idsecciones_salida` | bigint | YES |  |
| 13 | `idempresas_entrada` | bigint | YES |  |
| 14 | `idcentros_entrada` | bigint | YES |  |
| 15 | `a±otraspaso_entrada` | string | YES |  |
| 16 | `serietraspaso_entrada` | string | YES |  |
| 17 | `numtraspaso_entrada` | bigint | YES |  |
| 18 | `numdettraspaso_entrada` | bigint | YES |  |
| 19 | `idsecciones_entrada` | bigint | YES |  |
| 20 | `idmovimientotipos` | string | YES |  |
| 21 | `mr` | string | YES |  |
| 22 | `referencia` | string | YES |  |
| 23 | `valorbruto` | double | YES |  |
| 24 | `unidades` | double | YES |  |
| 25 | `valorneto` | double | YES |  |
| 26 | `valormediomovimiento` | double | YES |  |
| 27 | `fechaaltasalida` | timestamp | YES |  |
| 28 | `fechaaltaentrada` | timestamp | YES |  |
| 29 | `anio` | string | YES | (particion) |
| 30 | `mes` | string | YES | (particion) |

## 🥉 stage

`Capa: Bronce / Raw`

### stage.comisionesspigavn

**Columnas:** 50

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `idcomisionspiga` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `ano_spiga` | integer | YES |  |
| 6 | `mes_spiga` | integer | YES |  |
| 7 | `codigoempresa` | smallint | YES |  |
| 8 | `empresa` | varchar | YES |  |
| 9 | `codigoempresasugerido` | integer | YES |  |
| 10 | `empresasugerida` | varchar | YES |  |
| 11 | `codigocentro` | smallint | YES |  |
| 12 | `centro` | varchar | YES |  |
| 13 | `codigoseccion` | integer | YES |  |
| 14 | `seccion` | varchar | YES |  |
| 15 | `fechafactura` | timestamp(3) | YES |  |
| 16 | `numerofactura` | varchar | YES |  |
| 17 | `vin` | varchar | YES |  |
| 18 | `codigomarca` | smallint | YES |  |
| 19 | `marca` | varchar | YES |  |
| 20 | `codigogama` | smallint | YES |  |
| 21 | `gama` | varchar | YES |  |
| 22 | `codigomodelo` | varchar | YES |  |
| 23 | `extension` | varchar | YES |  |
| 24 | `a�omodelo` | varchar | YES |  |
| 25 | `modelo` | varchar | YES |  |
| 26 | `codigoversion` | varchar | YES |  |
| 27 | `nombreversion` | varchar | YES |  |
| 28 | `cedulavendedor` | bigint | YES |  |
| 29 | `nombrevendedor` | varchar | YES |  |
| 30 | `nit` | varchar | YES |  |
| 31 | `nombretercero` | varchar | YES |  |
| 32 | `preciovehiculo` | decimal(18,4) | YES |  |
| 33 | `preciolista` | decimal(18,4) | YES |  |
| 34 | `valordto` | decimal(18,4) | YES |  |
| 35 | `importeimpuestos` | decimal(38,4) | YES |  |
| 36 | `totalfactura` | decimal(18,4) | YES |  |
| 37 | `fechacancelacionfactura` | timestamp(3) | YES |  |
| 38 | `totalcanceladofactura` | decimal(38,4) | YES |  |
| 39 | `fecharemesa` | timestamp(3) | YES |  |
| 40 | `valorremesado` | decimal(38,4) | YES |  |
| 41 | `fechaentregacliente` | timestamp(3) | YES |  |
| 42 | `descuentopolitica` | decimal(15,9) | YES |  |
| 43 | `numerentregas` | integer | YES |  |
| 44 | `tipo_servicio` | varchar | YES |  |
| 45 | `cuotaretefuente` | decimal(18,4) | YES |  |
| 46 | `entregaefectiva` | integer | YES |  |
| 47 | `procedencia` | varchar | YES |  |
| 48 | `procedenciadetalle` | varchar | YES |  |
| 49 | `tipooportunidad` | varchar | YES |  |
| 50 | `entregainmediata` | boolean | YES |  |

### stage.comisionesspigavo

**Columnas:** 49

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `idcomisionspiga` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `ano_spiga` | integer | YES |  |
| 6 | `mes_spiga` | integer | YES |  |
| 7 | `codigoempresa` | smallint | YES |  |
| 8 | `empresa` | varchar | YES |  |
| 9 | `codigoempresasugerido` | integer | YES |  |
| 10 | `empresasugerida` | varchar | YES |  |
| 11 | `codigocentro` | smallint | YES |  |
| 12 | `centro` | varchar | YES |  |
| 13 | `codigoseccion` | integer | YES |  |
| 14 | `seccion` | varchar | YES |  |
| 15 | `fechafactura` | timestamp(3) | YES |  |
| 16 | `numerofactura` | varchar | YES |  |
| 17 | `vin` | varchar | YES |  |
| 18 | `codigomarca` | smallint | YES |  |
| 19 | `marca` | varchar | YES |  |
| 20 | `codigogama` | smallint | YES |  |
| 21 | `gama` | varchar | YES |  |
| 22 | `codigomodelo` | varchar | YES |  |
| 23 | `extension` | varchar | YES |  |
| 24 | `a�omodelo` | varchar | YES |  |
| 25 | `modelo` | varchar | YES |  |
| 26 | `codigoversion` | varchar | YES |  |
| 27 | `nombreversion` | varchar | YES |  |
| 28 | `cedulavendedor` | bigint | YES |  |
| 29 | `nombrevendedor` | varchar | YES |  |
| 30 | `nit` | varchar | YES |  |
| 31 | `nombretercero` | varchar | YES |  |
| 32 | `preciovehiculo` | decimal(18,4) | YES |  |
| 33 | `preciolista` | decimal(18,4) | YES |  |
| 34 | `valordto` | decimal(18,4) | YES |  |
| 35 | `importeimpuestos` | decimal(38,4) | YES |  |
| 36 | `totalfactura` | decimal(18,4) | YES |  |
| 37 | `fechacancelacionfactura` | timestamp(3) | YES |  |
| 38 | `totalcanceladofactura` | decimal(38,4) | YES |  |
| 39 | `fecharemesa` | timestamp(3) | YES |  |
| 40 | `valorremesado` | decimal(38,4) | YES |  |
| 41 | `fechaentregacliente` | timestamp(3) | YES |  |
| 42 | `descuentopolitica` | decimal(15,9) | YES |  |
| 43 | `numerentregas` | integer | YES |  |
| 44 | `tipo_servicio` | varchar | YES |  |
| 45 | `cuotaretefuente` | decimal(38,4) | YES |  |
| 46 | `entregaefectiva` | integer | YES |  |
| 47 | `procedencia` | varchar | YES |  |
| 48 | `procedenciadetalle` | varchar | YES |  |
| 49 | `tipooportunidad` | varchar | YES |  |

### stage.datos_terceros_view

**Columnas:** 10

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `pkterceros` | bigint | YES |  |
| 2 | `nifcif` | varchar | YES |  |
| 3 | `direccion` | varchar | YES |  |
| 4 | `correo` | varchar | YES |  |
| 5 | `numero` | varchar | YES |  |
| 6 | `id_formacionniveles` | varchar | YES |  |
| 7 | `fktercerocargos` | varchar | YES |  |
| 8 | `fkestadociviltipos` | varchar | YES |  |
| 9 | `id_profesiones` | varchar | YES |  |
| 10 | `fkterceroclases` | varchar | YES |  |

### stage.dwdms00280_dw_dimcentros

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `skdimcentros` | bigint | YES |  |
| 2 | `pkcentros` | bigint | YES |  |
| 3 | `nombrecentro` | varchar | YES |  |
| 4 | `idproceso` | bigint | YES |  |
| 5 | `idprocesodw` | bigint | YES |  |
| 6 | `versionct` | bigint | YES |  |
| 7 | `hashvaluebi` | bigint | YES |  |
| 8 | `load_date` | varchar | YES |  |

### stage.dwdms00280_dw_dimempleados

**Columnas:** 20

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `skdimempleados` | bigint | YES |  |
| 2 | `nombre` | varchar | YES |  |
| 3 | `apellido1` | varchar | YES |  |
| 4 | `apellido2` | varchar | YES |  |
| 5 | `pkempleados` | bigint | YES |  |
| 6 | `idproceso` | bigint | YES |  |
| 7 | `idprocesodw` | bigint | YES |  |
| 8 | `versionct` | bigint | YES |  |
| 9 | `hashvaluebi` | bigint | YES |  |
| 10 | `nifcif` | varchar | YES |  |
| 11 | `telefonoprincipal` | varchar | YES |  |
| 12 | `telefonomovil` | varchar | YES |  |
| 13 | `email` | varchar | YES |  |
| 14 | `nombreusuario` | varchar | YES |  |
| 15 | `fechabaja` | timestamp(3) | YES |  |
| 16 | `fechaalta` | timestamp(3) | YES |  |
| 17 | `fkusuarios` | bigint | YES |  |
| 18 | `fkprofesiones` | bigint | YES |  |
| 19 | `nombreprofesion` | varchar | YES |  |
| 20 | `load_date` | varchar | YES |  |

### stage.dwdms00280_dw_dimempresas

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `skdimempresas` | bigint | YES |  |
| 2 | `nombreempresa` | varchar | YES |  |
| 3 | `pkempresas` | bigint | YES |  |
| 4 | `idproceso` | bigint | YES |  |
| 5 | `idprocesodw` | bigint | YES |  |
| 6 | `versionct` | bigint | YES |  |
| 7 | `hashvaluebi` | bigint | YES |  |
| 8 | `load_date` | varchar | YES |  |

### stage.dwdms00280_dw_dimmarcasgamas

**Columnas:** 10

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `skdimmarcasgamas` | bigint | YES |  |
| 2 | `nombremarca` | varchar | YES |  |
| 3 | `nombregama` | varchar | YES |  |
| 4 | `pkmarcas` | bigint | YES |  |
| 5 | `pkgamas` | bigint | YES |  |
| 6 | `idproceso` | bigint | YES |  |
| 7 | `idprocesodw` | bigint | YES |  |
| 8 | `versionct` | bigint | YES |  |
| 9 | `hashvaluebi` | bigint | YES |  |
| 10 | `load_date` | varchar | YES |  |

### stage.dwdms00280_dw_factfinanciacionventas

**Columnas:** 54

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `skfactfinanciacionventas` | bigint | YES |  |
| 2 | `pkempresas` | bigint | YES |  |
| 3 | `pka�oexpediente` | varchar | YES |  |
| 4 | `pknumexpediente` | bigint | YES |  |
| 5 | `pkpagostipos` | bigint | YES |  |
| 6 | `pkseries_expediente` | varchar | YES |  |
| 7 | `pkventas` | bigint | YES |  |
| 8 | `pkventaspagos` | bigint | YES |  |
| 9 | `pkcomprasnumdet` | bigint | YES |  |
| 10 | `pkcentros` | bigint | YES |  |
| 11 | `pktercerosfinanciera` | bigint | YES |  |
| 12 | `nombrefinanciera` | varchar | YES |  |
| 13 | `apellido1financiera` | varchar | YES |  |
| 14 | `apellido2financiera` | varchar | YES |  |
| 15 | `pktercerosagente` | bigint | YES |  |
| 16 | `nombreagente` | varchar | YES |  |
| 17 | `apellido1agente` | varchar | YES |  |
| 18 | `apellido2agente` | varchar | YES |  |
| 19 | `pktercerospropietario` | bigint | YES |  |
| 20 | `nombrepropietario` | varchar | YES |  |
| 21 | `apellido1propietario` | varchar | YES |  |
| 22 | `apellido2propietario` | varchar | YES |  |
| 23 | `nifcifpropietario` | varchar | YES |  |
| 24 | `importefinanciado` | double | YES |  |
| 25 | `comisionfinanciera` | double | YES |  |
| 26 | `pkofertapagos` | bigint | YES |  |
| 27 | `saldofavorcliente` | varchar | YES |  |
| 28 | `vin` | varchar | YES |  |
| 29 | `matricula` | varchar | YES |  |
| 30 | `comisionvehiculo` | varchar | YES |  |
| 31 | `modulo` | varchar | YES |  |
| 32 | `estado` | varchar | YES |  |
| 33 | `fechavencimiento` | timestamp(3) | YES |  |
| 34 | `fechainicio` | timestamp(3) | YES |  |
| 35 | `fechaventa` | timestamp(3) | YES |  |
| 36 | `fechaentregacliente` | timestamp(3) | YES |  |
| 37 | `fechadecorte` | timestamp(3) | YES |  |
| 38 | `idproceso` | bigint | YES |  |
| 39 | `idprocesodw` | bigint | YES |  |
| 40 | `versionct` | bigint | YES |  |
| 41 | `hashvaluebi` | bigint | YES |  |
| 42 | `skdimempresas` | bigint | YES |  |
| 43 | `skdimcentros` | bigint | YES |  |
| 44 | `skdimsecciones` | bigint | YES |  |
| 45 | `skdimmarcasgamas` | bigint | YES |  |
| 46 | `skdimempleados` | bigint | YES |  |
| 47 | `skdimempleadosgestor` | bigint | YES |  |
| 48 | `pkventaspagosdet` | bigint | YES |  |
| 49 | `pkefectosnumdet` | bigint | YES |  |
| 50 | `pka�oasiento` | varchar | YES |  |
| 51 | `pkasientos` | bigint | YES |  |
| 52 | `pka�oasiento_saldar` | varchar | YES |  |
| 53 | `pkasientos_saldar` | bigint | YES |  |
| 54 | `load_date` | varchar | YES |  |

### stage.empresas

**Columnas:** 6

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codigoempresa` | smallint | YES |  |
| 2 | `nombreempresa` | varchar | YES |  |
| 3 | `siglaempresa` | varchar | YES |  |
| 4 | `nitempresa` | varchar | YES |  |
| 5 | `activarliquidacion` | boolean | YES |  |
| 6 | `codpais` | smallint | YES |  |

### stage.materialized_leads_tracking

**Columnas:** 41

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `lead_id` | bigint | YES |  |
| 3 | `clasification_id` | bigint | YES |  |
| 4 | `clasification_name` | varchar | YES |  |
| 5 | `action_id` | bigint | YES |  |
| 6 | `action_name` | varchar | YES |  |
| 7 | `status_id` | bigint | YES |  |
| 8 | `status_name` | varchar | YES |  |
| 9 | `campaing_id` | bigint | YES |  |
| 10 | `campaing_name` | varchar | YES |  |
| 11 | `medium_id` | bigint | YES |  |
| 12 | `medium_value` | varchar | YES |  |
| 13 | `category_id` | bigint | YES |  |
| 14 | `category_name` | varchar | YES |  |
| 15 | `country_name` | varchar | YES |  |
| 16 | `company_name` | varchar | YES |  |
| 17 | `brand_id` | bigint | YES |  |
| 18 | `brand_name` | varchar | YES |  |
| 19 | `wholesaler` | bigint | YES |  |
| 20 | `adviser_id` | bigint | YES |  |
| 21 | `adviser_name` | varchar | YES |  |
| 22 | `adviser_email` | varchar | YES |  |
| 23 | `adviser_document_type` | varchar | YES |  |
| 24 | `adviser_document_number` | varchar | YES |  |
| 25 | `adviser_business_type_id` | bigint | YES |  |
| 26 | `adviser_business_type` | varchar | YES |  |
| 27 | `concessionaire_id` | bigint | YES |  |
| 28 | `concessionaire_names` | varchar | YES |  |
| 29 | `client_name` | varchar | YES |  |
| 30 | `client_phone` | varchar | YES |  |
| 31 | `client_email` | varchar | YES |  |
| 32 | `client_document_type_name` | varchar | YES |  |
| 33 | `client_document_number` | varchar | YES |  |
| 34 | `model_id` | bigint | YES |  |
| 35 | `model_name` | varchar | YES |  |
| 36 | `model_year` | varchar | YES |  |
| 37 | `license_plate` | varchar | YES |  |
| 38 | `created_at` | timestamp(3) | YES |  |
| 39 | `updated_at` | timestamp(3) | YES |  |
| 40 | `fecha_cargue` | varchar | YES |  |
| 41 | `load_date` | varchar | YES |  |

### stage.rc_view_entregas

**Columnas:** 13

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `vin` | varchar | YES |  |
| 2 | `gama` | varchar | YES |  |
| 3 | `anio_modelo` | varchar | YES |  |
| 4 | `marca` | varchar | YES |  |
| 5 | `modelo_version` | varchar | YES |  |
| 6 | `cantidad` | bigint | YES |  |
| 7 | `valor` | double | YES |  |
| 8 | `tipo` | varchar | YES |  |
| 9 | `fechaentregacliente` | timestamp(3) | YES |  |
| 10 | `nit` | varchar | YES |  |
| 11 | `nombrevendedor` | varchar | YES |  |
| 12 | `cedulavendedor` | varchar | YES |  |
| 13 | `centro` | varchar | YES |  |

### stage.spiga_cartera

**Columnas:** 59

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `indice` | double | YES |  |
| 8 | `idterceros` | bigint | YES |  |
| 9 | `idterceros_pagador` | bigint | YES |  |
| 10 | `nombretercero` | varchar | YES |  |
| 11 | `factura` | varchar | YES |  |
| 12 | `fechafactura` | timestamp(3) | YES |  |
| 13 | `fechavencimiento` | timestamp(3) | YES |  |
| 14 | `idpagoformas` | varchar | YES |  |
| 15 | `descripcionpagoformas` | varchar | YES |  |
| 16 | `idsituacionefectos` | bigint | YES |  |
| 17 | `descripcionsituacionefectos` | varchar | YES |  |
| 18 | `departamento` | varchar | YES |  |
| 19 | `nombredepartamento` | varchar | YES |  |
| 20 | `totalfactura` | double | YES |  |
| 21 | `importeefecto` | double | YES |  |
| 22 | `importependiente` | double | YES |  |
| 23 | `diadesde` | bigint | YES |  |
| 24 | `diahasta` | bigint | YES |  |
| 25 | `nombrecentro` | varchar | YES |  |
| 26 | `numdet` | bigint | YES |  |
| 27 | `a�oasiento` | varchar | YES |  |
| 28 | `idasientos` | bigint | YES |  |
| 29 | `descripciontipocalle` | varchar | YES |  |
| 30 | `nombrecalle` | varchar | YES |  |
| 31 | `numero` | varchar | YES |  |
| 32 | `bloque` | varchar | YES |  |
| 33 | `piso` | varchar | YES |  |
| 34 | `puerta` | varchar | YES |  |
| 35 | `complemento` | varchar | YES |  |
| 36 | `complemento2` | varchar | YES |  |
| 37 | `nifcif` | varchar | YES |  |
| 38 | `idpaises` | varchar | YES |  |
| 39 | `ciudad` | varchar | YES |  |
| 40 | `referenciainterna` | varchar | YES |  |
| 41 | `limitecredito` | double | YES |  |
| 42 | `vin` | varchar | YES |  |
| 43 | `descripcionseccion` | varchar | YES |  |
| 44 | `fechasaldado` | timestamp(3) | YES |  |
| 45 | `estadowf` | varchar | YES |  |
| 46 | `pagobloqueado` | varchar | YES |  |
| 47 | `descripciondeudortipos` | varchar | YES |  |
| 48 | `iddeudortipos` | varchar | YES |  |
| 49 | `idcontctasterceropagador` | varchar | YES |  |
| 50 | `fechaentregavo` | timestamp(3) | YES |  |
| 51 | `fechaentregavn` | timestamp(3) | YES |  |
| 52 | `referencia` | varchar | YES |  |
| 53 | `idmonedaorigen` | bigint | YES |  |
| 54 | `factorcambiomoneda` | double | YES |  |
| 55 | `factorcambiomonedacontravalor` | double | YES |  |
| 56 | `descripcionmoneda` | varchar | YES |  |
| 57 | `decimalescalculomoneda` | bigint | YES |  |
| 58 | `telefonos` | varchar | YES |  |
| 59 | `load_date` | varchar | YES |  |

### stage.spiga_clientes_terceros

**Columnas:** 31

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `asesor` | varchar | YES |  |
| 2 | `cantidad2` | varchar | YES |  |
| 3 | `valor` | double | YES |  |
| 4 | `fecha` | timestamp(3) | YES |  |
| 5 | `nombretercero` | varchar | YES |  |
| 6 | `idmarca` | varchar | YES |  |
| 7 | `marca` | varchar | YES |  |
| 8 | `linea` | varchar | YES |  |
| 9 | `centro` | varchar | YES |  |
| 10 | `idgama` | varchar | YES |  |
| 11 | `gama` | varchar | YES |  |
| 12 | `idversion` | varchar | YES |  |
| 13 | `version` | varchar | YES |  |
| 14 | `a�omodelo` | varchar | YES |  |
| 15 | `idterceros` | varchar | YES |  |
| 16 | `vin` | varchar | YES |  |
| 17 | `numeroidentidad` | varchar | YES |  |
| 18 | `fechaentregacliente` | timestamp(3) | YES |  |
| 19 | `codigocentro` | varchar | YES |  |
| 20 | `fechaalta` | date | YES |  |
| 21 | `tipo` | varchar | YES |  |
| 22 | `kmts` | double | YES |  |
| 23 | `tipotrabajo` | varchar | YES |  |
| 24 | `idempresa` | varchar | YES |  |
| 25 | `descripcionreferencia` | varchar | YES |  |
| 26 | `descripcionclasificacion` | varchar | YES |  |
| 27 | `nombrefinanciera` | varchar | YES |  |
| 28 | `comisionvehiculo` | varchar | YES |  |
| 29 | `estado` | varchar | YES |  |
| 30 | `producto` | varchar(21) | YES |  |
| 31 | `combustible_categoria` | varchar(15) | YES |  |

### stage.spiga_compradeusados

**Columnas:** 100

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacion` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `comprasnumdet` | bigint | YES |  |
| 12 | `idvehiculos` | bigint | YES |  |
| 13 | `idcompratipos` | varchar | YES |  |
| 14 | `importecompra` | double | YES |  |
| 15 | `importetotal` | double | YES |  |
| 16 | `codcompramultiple` | bigint | YES |  |
| 17 | `fechaalta` | timestamp(3) | YES |  |
| 18 | `fechaanulacion` | timestamp(3) | YES |  |
| 19 | `idsecciones` | bigint | YES |  |
| 20 | `fechaabono` | timestamp(3) | YES |  |
| 21 | `comprasnumdetabonado` | bigint | YES |  |
| 22 | `idcompraestados` | varchar | YES |  |
| 23 | `observaciones` | varchar | YES |  |
| 24 | `idregistrotipos` | varchar | YES |  |
| 25 | `reservafecha` | timestamp(3) | YES |  |
| 26 | `reservaimporte` | double | YES |  |
| 27 | `reservaidempleados` | bigint | YES |  |
| 28 | `reservaterceros` | bigint | YES |  |
| 29 | `realizargastoadicionalautomatico` | varchar | YES |  |
| 30 | `nocontabilizardocumentacion` | varchar | YES |  |
| 31 | `idempleadovendedor` | bigint | YES |  |
| 32 | `kms` | bigint | YES |  |
| 33 | `a�oexpedientecambio` | varchar | YES |  |
| 34 | `serieexpedientecambio` | varchar | YES |  |
| 35 | `numexpedientecambio` | bigint | YES |  |
| 36 | `prever` | varchar | YES |  |
| 37 | `visibleweb` | varchar | YES |  |
| 38 | `comercializable` | varchar | YES |  |
| 39 | `generaasiento` | varchar | YES |  |
| 40 | `idmoduloorigen` | varchar | YES |  |
| 41 | `idusuariosanulacion` | bigint | YES |  |
| 42 | `idempleadosanulacion` | bigint | YES |  |
| 43 | `hostanulacion` | varchar | YES |  |
| 44 | `usermod` | bigint | YES |  |
| 45 | `hostmod` | varchar | YES |  |
| 46 | `versionfila` | bigint | YES |  |
| 47 | `a�oexpedientecambiovn` | varchar | YES |  |
| 48 | `serieexpedientecambiovn` | varchar | YES |  |
| 49 | `numexpedientecambiovn` | bigint | YES |  |
| 50 | `idcomprasnumdetcambio` | bigint | YES |  |
| 51 | `idcomprasnumdetcambiovn` | bigint | YES |  |
| 52 | `marcarkm0web` | varchar | YES |  |
| 53 | `fecharecepcion` | timestamp(3) | YES |  |
| 54 | `fechaasiento` | timestamp(3) | YES |  |
| 55 | `seriefactura` | varchar | YES |  |
| 56 | `numfactura` | varchar | YES |  |
| 57 | `a�ofactura` | varchar | YES |  |
| 58 | `fechafactura` | timestamp(3) | YES |  |
| 59 | `idmarcas` | bigint | YES |  |
| 60 | `idgamas` | bigint | YES |  |
| 61 | `codmodelo` | varchar | YES |  |
| 62 | `extmodelo` | varchar | YES |  |
| 63 | `a�omodelo` | varchar | YES |  |
| 64 | `idversiones` | varchar | YES |  |
| 65 | `matricula` | varchar | YES |  |
| 66 | `vin` | varchar | YES |  |
| 67 | `nombremarca` | varchar | YES |  |
| 68 | `nombregama` | varchar | YES |  |
| 69 | `importebi` | double | YES |  |
| 70 | `importe576` | double | YES |  |
| 71 | `importedvn` | double | YES |  |
| 72 | `exentos` | double | YES |  |
| 73 | `vincambio` | varchar | YES |  |
| 74 | `matriculacambio` | varchar | YES |  |
| 75 | `idmarcascambio` | bigint | YES |  |
| 76 | `idgamascambio` | bigint | YES |  |
| 77 | `nombremarcacambio` | varchar | YES |  |
| 78 | `nombregamacambio` | varchar | YES |  |
| 79 | `gastoadicionaldetalles` | double | YES |  |
| 80 | `idterceros` | bigint | YES |  |
| 81 | `nombreterceros` | varchar | YES |  |
| 82 | `nombre` | varchar | YES |  |
| 83 | `idmonedas` | bigint | YES |  |
| 84 | `factorcambiomoneda` | double | YES |  |
| 85 | `monedaorigen` | varchar | YES |  |
| 86 | `centroventavehiculocambio` | varchar | YES |  |
| 87 | `nombreempleadoventavehiculocambio` | varchar | YES |  |
| 88 | `apellido1empleadoventavehiculocambio` | varchar | YES |  |
| 89 | `apellido2empleadoventavehiculocambio` | varchar | YES |  |
| 90 | `nombreempleadocompra` | varchar | YES |  |
| 91 | `apellido1empleadocompra` | varchar | YES |  |
| 92 | `apellido2empleadocompra` | varchar | YES |  |
| 93 | `descripcioncompratipos` | varchar | YES |  |
| 94 | `esinmovilizado` | varchar | YES |  |
| 95 | `nombremodelo` | varchar | YES |  |
| 96 | `descripcionversiones` | varchar | YES |  |
| 97 | `descripcionsecciones` | varchar | YES |  |
| 98 | `descripcionregistrotipos` | varchar | YES |  |
| 99 | `seccionventavehiculocambio` | varchar | YES |  |
| 100 | `load_date` | varchar | YES |  |

### stage.spiga_compras_sel_stockvn

**Columnas:** 206

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `comprasnumdet` | bigint | YES |  |
| 12 | `idasientos` | bigint | YES |  |
| 13 | `a�oasiento` | varchar | YES |  |
| 14 | `idvehiculos` | bigint | YES |  |
| 15 | `idterceros` | bigint | YES |  |
| 16 | `idcompratipos` | varchar | YES |  |
| 17 | `numexpedientescompramultiple` | bigint | YES |  |
| 18 | `idmarcas` | bigint | YES |  |
| 19 | `idgamas` | bigint | YES |  |
| 20 | `codmodelo` | varchar | YES |  |
| 21 | `extmodelo` | varchar | YES |  |
| 22 | `a�omodelo` | varchar | YES |  |
| 23 | `idversiones` | varchar | YES |  |
| 24 | `idtarifas` | bigint | YES |  |
| 25 | `seriefactura` | varchar | YES |  |
| 26 | `numfactura` | varchar | YES |  |
| 27 | `a�ofactura` | varchar | YES |  |
| 28 | `fechaalta` | timestamp(3) | YES |  |
| 29 | `fechaanulacion` | timestamp(3) | YES |  |
| 30 | `fechacampaalta` | timestamp(3) | YES |  |
| 31 | `fecharecepcion` | timestamp(3) | YES |  |
| 32 | `fechafactura` | timestamp(3) | YES |  |
| 33 | `fechaasiento` | timestamp(3) | YES |  |
| 34 | `fechareserva` | timestamp(3) | YES |  |
| 35 | `importacionrealizada` | varchar | YES |  |
| 36 | `importacionmodificada` | varchar | YES |  |
| 37 | `fechaimportacionrealizada` | timestamp(3) | YES |  |
| 38 | `fechaimportacionmodificada` | timestamp(3) | YES |  |
| 39 | `preciobase` | double | YES |  |
| 40 | `preciopintura` | double | YES |  |
| 41 | `preciotransporte` | double | YES |  |
| 42 | `precioopciones` | double | YES |  |
| 43 | `preciootroscargos` | double | YES |  |
| 44 | `importecompra` | double | YES |  |
| 45 | `baseimponible` | double | YES |  |
| 46 | `idcentrosasignadoventa` | bigint | YES |  |
| 47 | `idseccionesasignadaventa` | bigint | YES |  |
| 48 | `preciolegalizacion` | double | YES |  |
| 49 | `precioisv` | double | YES |  |
| 50 | `precioecovalor` | double | YES |  |
| 51 | `baseexenta` | double | YES |  |
| 52 | `sumadescuentos` | double | YES |  |
| 53 | `idempleadosreserva` | bigint | YES |  |
| 54 | `idagentesreserva` | bigint | YES |  |
| 55 | `idterceros_cedidoconcesionario` | bigint | YES |  |
| 56 | `numfacturamensual` | bigint | YES |  |
| 57 | `idsecciones` | bigint | YES |  |
| 58 | `numexpedicion` | varchar | YES |  |
| 59 | `programa` | varchar | YES |  |
| 60 | `realizargastoadicionalautomatico` | varchar | YES |  |
| 61 | `nocontabilizardocumentacion` | varchar | YES |  |
| 62 | `observaciones` | varchar | YES |  |
| 63 | `comprasnumdet_abonado` | bigint | YES |  |
| 64 | `idcompraestados` | varchar | YES |  |
| 65 | `usermod` | bigint | YES |  |
| 66 | `hostmod` | varchar | YES |  |
| 67 | `versionfila` | bigint | YES |  |
| 68 | `fechaabono` | timestamp(3) | YES |  |
| 69 | `idusuariosanulacion` | bigint | YES |  |
| 70 | `idempleadosanulacion` | bigint | YES |  |
| 71 | `hostanulacion` | varchar | YES |  |
| 72 | `idasientos_polizanoactivo` | bigint | YES |  |
| 73 | `a�oasiento_polizanoactivo` | varchar | YES |  |
| 74 | `nombremarca` | varchar | YES |  |
| 75 | `backcolorcabecerargb` | varchar | YES |  |
| 76 | `backcolordetallergb` | varchar | YES |  |
| 77 | `forecolorcabecerargb` | varchar | YES |  |
| 78 | `forecolordetallergb` | varchar | YES |  |
| 79 | `nombregama` | varchar | YES |  |
| 80 | `preciolegalizacion1` | double | YES |  |
| 81 | `precioisv1` | double | YES |  |
| 82 | `precioecovalor1` | double | YES |  |
| 83 | `activo` | varchar | YES |  |
| 84 | `idcarroceriatipos` | varchar | YES |  |
| 85 | `idclasificaciontipos` | varchar | YES |  |
| 86 | `idmarcatallermodelos` | varchar | YES |  |
| 87 | `idtracciontipos` | varchar | YES |  |
| 88 | `idcambiotipos` | varchar | YES |  |
| 89 | `idtonelajetipos` | varchar | YES |  |
| 90 | `iddistanciaejestipos` | varchar | YES |  |
| 91 | `codexternomodelo` | varchar | YES |  |
| 92 | `potenciafiscal` | varchar | YES |  |
| 93 | `potenciareal` | varchar | YES |  |
| 94 | `cilindrada` | double | YES |  |
| 95 | `aceleracion` | varchar | YES |  |
| 96 | `velocidadmax` | double | YES |  |
| 97 | `par` | varchar | YES |  |
| 98 | `numerocilindros` | bigint | YES |  |
| 99 | `consumointerurbano` | double | YES |  |
| 100 | `consumourbano` | double | YES |  |
| 101 | `consumomedio` | double | YES |  |
| 102 | `emisionesco2interurbano` | double | YES |  |
| 103 | `emisionesco2urbano` | double | YES |  |
| 104 | `emisionesco2medio` | double | YES |  |
| 105 | `importado` | varchar | YES |  |
| 106 | `modificado` | varchar | YES |  |
| 107 | `permiteplanprever` | varchar | YES |  |
| 108 | `visibleweb` | varchar | YES |  |
| 109 | `periodoinspeccion` | bigint | YES |  |
| 110 | `kilometrosinspeccion` | varchar | YES |  |
| 111 | `descripcionmodelotaller` | varchar | YES |  |
| 112 | `vin` | varchar | YES |  |
| 113 | `matricula` | varchar | YES |  |
| 114 | `comision` | varchar | YES |  |
| 115 | `fechamatriculacion` | timestamp(3) | YES |  |
| 116 | `codigofabricacion` | varchar | YES |  |
| 117 | `fechafabricacion` | timestamp(3) | YES |  |
| 118 | `numeromotor` | varchar | YES |  |
| 119 | `nombreempresa` | varchar | YES |  |
| 120 | `nombrecentro` | varchar | YES |  |
| 121 | `diasstock` | bigint | YES |  |
| 122 | `idrecursos` | bigint | YES |  |
| 123 | `idubicacionesultimarealizada` | varchar | YES |  |
| 124 | `fechaexpedientealtaultimarealizada` | timestamp(3) | YES |  |
| 125 | `ubicacionvn` | varchar | YES |  |
| 126 | `fechaubicacion` | timestamp(3) | YES |  |
| 127 | `idubicacionesultima` | varchar | YES |  |
| 128 | `fechaexpedientealtaultima` | timestamp(3) | YES |  |
| 129 | `ubicacionvnprevista` | varchar | YES |  |
| 130 | `fechasalidareal` | timestamp(3) | YES |  |
| 131 | `nombreempleadoreserva` | varchar | YES |  |
| 132 | `nombreagente` | varchar | YES |  |
| 133 | `cedido` | varchar | YES |  |
| 134 | `fechallegadapuerto` | timestamp(3) | YES |  |
| 135 | `fecharetirada` | timestamp(3) | YES |  |
| 136 | `datoscarta` | varchar | YES |  |
| 137 | `preciocompra` | double | YES |  |
| 138 | `precioventa` | double | YES |  |
| 139 | `transportecompra` | double | YES |  |
| 140 | `precioventaopcionales` | bigint | YES |  |
| 141 | `rodajetrimestral` | double | YES |  |
| 142 | `gastosmatriculacion` | double | YES |  |
| 143 | `atipicos` | double | YES |  |
| 144 | `transporteventa` | double | YES |  |
| 145 | `preciolegalizacionventa` | double | YES |  |
| 146 | `impuesto576porc` | double | YES |  |
| 147 | `numpedidovn` | varchar | YES |  |
| 148 | `idtercerospedido` | bigint | YES |  |
| 149 | `fechainiciofranquicia` | timestamp(3) | YES |  |
| 150 | `fechafinalfranquicia` | timestamp(3) | YES |  |
| 151 | `fechaaradefinitiva` | timestamp(3) | YES |  |
| 152 | `fechaentregaconcesionario` | timestamp(3) | YES |  |
| 153 | `fechacompromisoentrega` | timestamp(3) | YES |  |
| 154 | `mesesgarantiaobligatoriavn` | bigint | YES |  |
| 155 | `numpedidofabrica` | varchar | YES |  |
| 156 | `numpedidomarca` | varchar | YES |  |
| 157 | `pedidoobservaciones` | varchar | YES |  |
| 158 | `idpedidolocaltipos` | varchar | YES |  |
| 159 | `fechadespacho` | timestamp(3) | YES |  |
| 160 | `diasestancia` | bigint | YES |  |
| 161 | `observacionubicacion` | varchar | YES |  |
| 162 | `diasdecarenciadocumentacion` | bigint | YES |  |
| 163 | `diascarencia` | bigint | YES |  |
| 164 | `situacion` | varchar | YES |  |
| 165 | `permitirfacturarenotrocentro` | varchar | YES |  |
| 166 | `idpaises_origen` | varchar | YES |  |
| 167 | `importacion` | varchar | YES |  |
| 168 | `factorcambiomonedacontravalor` | double | YES |  |
| 169 | `importepedidoservicios` | double | YES |  |
| 170 | `importegastosadicionales` | double | YES |  |
| 171 | `fechapedido` | timestamp(3) | YES |  |
| 172 | `diasexposicion` | bigint | YES |  |
| 173 | `homologacion` | varchar | YES |  |
| 174 | `nombreprospectoreservapedido` | varchar | YES |  |
| 175 | `nombreclientereservapedido` | varchar | YES |  |
| 176 | `nombreclientereservacompra` | varchar | YES |  |
| 177 | `precioiuc` | double | YES |  |
| 178 | `a�opedidosservicios` | varchar | YES |  |
| 179 | `seriepedidosservicios` | varchar | YES |  |
| 180 | `idpedidosservicios` | bigint | YES |  |
| 181 | `idmonedas` | bigint | YES |  |
| 182 | `factorcambiomoneda` | double | YES |  |
| 183 | `idregimencontable` | varchar | YES |  |
| 184 | `colorcompleto` | varchar | YES |  |
| 185 | `tapiceriacompleta` | varchar | YES |  |
| 186 | `descripcioncambiotipos` | varchar | YES |  |
| 187 | `nombreversion` | varchar | YES |  |
| 188 | `nombretarifa` | varchar | YES |  |
| 189 | `nombremodelo` | varchar | YES |  |
| 190 | `descripcionestadocompra` | varchar | YES |  |
| 191 | `descripciontipocombustible` | varchar | YES |  |
| 192 | `descripcionpedidolocaltipos` | varchar | YES |  |
| 193 | `descripcioncomprausos` | varchar | YES |  |
| 194 | `descripcionestadopedidosservicio` | varchar | YES |  |
| 195 | `idtercerosreserva` | bigint | YES |  |
| 196 | `idcomprausos` | varchar | YES |  |
| 197 | `visualizarenstockcomprausos` | varchar | YES |  |
| 198 | `tipocompra` | varchar | YES |  |
| 199 | `idiventario` | bigint | YES |  |
| 200 | `fechaultimoinventario` | timestamp(3) | YES |  |
| 201 | `documentosinventario` | bigint | YES |  |
| 202 | `documentosrespuestasinventario` | bigint | YES |  |
| 203 | `porcimpuestos_iva` | double | YES |  |
| 204 | `porcimpuestos_con` | double | YES |  |
| 205 | `idcentrosubicacion` | bigint | YES |  |
| 206 | `load_date` | varchar | YES |  |

### stage.spiga_compras_sel_stockvo

**Columnas:** 122

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `comprasnumdet` | bigint | YES |  |
| 12 | `idvehiculos` | bigint | YES |  |
| 13 | `idcompratipos` | varchar | YES |  |
| 14 | `codcompramultiple` | bigint | YES |  |
| 15 | `fechaalta` | timestamp(3) | YES |  |
| 16 | `fechaanulacion` | timestamp(3) | YES |  |
| 17 | `fecharecepcion` | timestamp(3) | YES |  |
| 18 | `idsecciones` | bigint | YES |  |
| 19 | `fechaabono` | timestamp(3) | YES |  |
| 20 | `comprasnumdetabonado` | bigint | YES |  |
| 21 | `idcompraestados` | varchar | YES |  |
| 22 | `observaciones` | varchar | YES |  |
| 23 | `idregistrotipos` | varchar | YES |  |
| 24 | `reservafecha` | timestamp(3) | YES |  |
| 25 | `reservaidempleados` | bigint | YES |  |
| 26 | `reservaterceros` | bigint | YES |  |
| 27 | `realizargastoadicionalautomatico` | varchar | YES |  |
| 28 | `nocontabilizardocumentacion` | varchar | YES |  |
| 29 | `idempleadovendedor` | bigint | YES |  |
| 30 | `kms` | bigint | YES |  |
| 31 | `a�oexpedientecambio` | varchar | YES |  |
| 32 | `serieexpedientecambio` | varchar | YES |  |
| 33 | `numexpedientecambio` | bigint | YES |  |
| 34 | `fechaasiento` | timestamp(3) | YES |  |
| 35 | `prever` | varchar | YES |  |
| 36 | `generaasiento` | varchar | YES |  |
| 37 | `idmoduloorigen` | varchar | YES |  |
| 38 | `idusuariosanulacion` | bigint | YES |  |
| 39 | `idempleadosanulacion` | bigint | YES |  |
| 40 | `hostanulacion` | varchar | YES |  |
| 41 | `usermod` | bigint | YES |  |
| 42 | `hostmod` | varchar | YES |  |
| 43 | `versionfila` | bigint | YES |  |
| 44 | `reservaimporte` | double | YES |  |
| 45 | `importecompra` | double | YES |  |
| 46 | `precioventaminimo` | double | YES |  |
| 47 | `visibleweb` | varchar | YES |  |
| 48 | `comercializable` | varchar | YES |  |
| 49 | `idcomprausos` | varchar | YES |  |
| 50 | `vin` | varchar | YES |  |
| 51 | `matricula` | varchar | YES |  |
| 52 | `comision` | varchar | YES |  |
| 53 | `fechamatriculacion` | timestamp(3) | YES |  |
| 54 | `idmarcas` | bigint | YES |  |
| 55 | `idgamas` | bigint | YES |  |
| 56 | `codmodelo` | varchar | YES |  |
| 57 | `extmodelo` | varchar | YES |  |
| 58 | `a�omodelo` | varchar | YES |  |
| 59 | `idversiones` | varchar | YES |  |
| 60 | `idmarcasexterna` | bigint | YES |  |
| 61 | `idgamasexterna` | bigint | YES |  |
| 62 | `codmodeloexterna` | varchar | YES |  |
| 63 | `extmodeloexterna` | varchar | YES |  |
| 64 | `a�omodeloexterna` | varchar | YES |  |
| 65 | `idversionesexterna` | varchar | YES |  |
| 66 | `kmsactuales` | bigint | YES |  |
| 67 | `permitirfacturarenotrocentro` | varchar | YES |  |
| 68 | `otrasobservaciones` | varchar | YES |  |
| 69 | `horasusoactual` | bigint | YES |  |
| 70 | `nombremarca` | varchar | YES |  |
| 71 | `nombregama` | varchar | YES |  |
| 72 | `nombremodelo` | varchar | YES |  |
| 73 | `nombregamaexterna` | varchar | YES |  |
| 74 | `nombremodeloexterna` | varchar | YES |  |
| 75 | `descripciontipocombustible` | varchar | YES |  |
| 76 | `descripciontipocombustibleexterna` | varchar | YES |  |
| 77 | `descripcionestadocompra` | varchar | YES |  |
| 78 | `potenciareal` | varchar | YES |  |
| 79 | `potenciarealexterna` | varchar | YES |  |
| 80 | `numeropuertas` | varchar | YES |  |
| 81 | `numeroplazas` | varchar | YES |  |
| 82 | `nombreempresa` | varchar | YES |  |
| 83 | `nombrecentro` | varchar | YES |  |
| 84 | `descripcionseccion` | varchar | YES |  |
| 85 | `descripciontiporegistro` | varchar | YES |  |
| 86 | `idcomprainternatipos` | varchar | YES |  |
| 87 | `descripcioncompratipos` | varchar | YES |  |
| 88 | `descripcioncarroceriatipos` | varchar | YES |  |
| 89 | `diasstock` | bigint | YES |  |
| 90 | `fecharetirada` | timestamp(3) | YES |  |
| 91 | `importeventasugerido` | double | YES |  |
| 92 | `nombreempleadoreserva` | varchar | YES |  |
| 93 | `nombreterceroreserva` | varchar | YES |  |
| 94 | `idrecursos` | bigint | YES |  |
| 95 | `importebi` | double | YES |  |
| 96 | `importedvn` | double | YES |  |
| 97 | `importe576` | double | YES |  |
| 98 | `exentos` | double | YES |  |
| 99 | `importegastosadicionales` | double | YES |  |
| 100 | `importedepreciado` | double | YES |  |
| 101 | `descripcioncomprausos` | varchar | YES |  |
| 102 | `importepedidoservicios` | double | YES |  |
| 103 | `nombrescedentes` | varchar | YES |  |
| 104 | `colorcompleto` | varchar | YES |  |
| 105 | `colorcompletoexterna` | varchar | YES |  |
| 106 | `tapiceriacompleta` | varchar | YES |  |
| 107 | `visualizarenstockcomprausos` | varchar | YES |  |
| 108 | `fechafactura` | timestamp(3) | YES |  |
| 109 | `fechafabricacion` | timestamp(3) | YES |  |
| 110 | `descripcionversion` | varchar | YES |  |
| 111 | `programasmarca` | varchar | YES |  |
| 112 | `idiventario` | bigint | YES |  |
| 113 | `fechaultimoinventario` | timestamp(3) | YES |  |
| 114 | `documentosinventario` | bigint | YES |  |
| 115 | `documentosrespuestasinventario` | bigint | YES |  |
| 116 | `sitiomatricula` | varchar | YES |  |
| 117 | `fechaproximaitv` | timestamp(3) | YES |  |
| 118 | `fechavencimientoseguro` | timestamp(3) | YES |  |
| 119 | `ubicacionvo` | varchar | YES |  |
| 120 | `observacionubicacionvo` | varchar | YES |  |
| 121 | `idubicavno` | varchar | YES |  |
| 122 | `load_date` | varchar | YES |  |

### stage.spiga_comprasvehiculosvn

**Columnas:** 62

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `comprasnumdet` | bigint | YES |  |
| 12 | `idvehiculos` | bigint | YES |  |
| 13 | `idcompratipos` | varchar | YES |  |
| 14 | `importecompra` | double | YES |  |
| 15 | `idsecciones` | bigint | YES |  |
| 16 | `seriefactura` | varchar | YES |  |
| 17 | `numfactura` | varchar | YES |  |
| 18 | `a�ofactura` | varchar | YES |  |
| 19 | `fechafactura` | timestamp(3) | YES |  |
| 20 | `baseimponible` | double | YES |  |
| 21 | `fechaasiento` | timestamp(3) | YES |  |
| 22 | `fecharegistrorunt` | timestamp(3) | YES |  |
| 23 | `importeiva` | double | YES |  |
| 24 | `descripcioncompratipos` | varchar | YES |  |
| 25 | `idmarcas` | bigint | YES |  |
| 26 | `idgamas` | bigint | YES |  |
| 27 | `codmodelo` | varchar | YES |  |
| 28 | `extmodelo` | varchar | YES |  |
| 29 | `a�omodelo` | varchar | YES |  |
| 30 | `idversiones` | varchar | YES |  |
| 31 | `matricula` | varchar | YES |  |
| 32 | `vin` | varchar | YES |  |
| 33 | `nombremarca` | varchar | YES |  |
| 34 | `nombregama` | varchar | YES |  |
| 35 | `nombremodelo` | varchar | YES |  |
| 36 | `descripcionversiones` | varchar | YES |  |
| 37 | `descripcionsecciones` | varchar | YES |  |
| 38 | `idctabancaria` | bigint | YES |  |
| 39 | `descripcionctabancaria` | varchar | YES |  |
| 40 | `nombre` | varchar | YES |  |
| 41 | `monedaorigen` | varchar | YES |  |
| 42 | `idcomprausos` | varchar | YES |  |
| 43 | `codexternomodelo` | varchar | YES |  |
| 44 | `idincidenciatipos` | varchar | YES |  |
| 45 | `idtercerosactividadincidenciatipos` | bigint | YES |  |
| 46 | `idactividadincidenciatipos` | bigint | YES |  |
| 47 | `idactividadesdetincidenciatipos` | bigint | YES |  |
| 48 | `incidenciatiposdescripcion` | varchar | YES |  |
| 49 | `numproformafabrica` | varchar | YES |  |
| 50 | `idcompraestados` | varchar | YES |  |
| 51 | `idcomprasnumdet_abonado` | bigint | YES |  |
| 52 | `fechaalbaran` | timestamp(3) | YES |  |
| 53 | `fechaasiento_albaran` | timestamp(3) | YES |  |
| 54 | `seriealbaran` | varchar | YES |  |
| 55 | `numalbaran` | varchar | YES |  |
| 56 | `a�oalbaran` | varchar | YES |  |
| 57 | `baseimponible_albaran` | double | YES |  |
| 58 | `factorcambiomoneda_albaran` | double | YES |  |
| 59 | `fecharecepcion` | timestamp(3) | YES |  |
| 60 | `codproveedor` | bigint | YES |  |
| 61 | `proveedor` | varchar | YES |  |
| 62 | `load_date` | varchar | YES |  |

### stage.spiga_consultamovimientosreferencia

**Columnas:** 163

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idtipolinea` | varchar | YES |  |
| 7 | `idmovimientotipos` | varchar | YES |  |
| 8 | `idmr` | varchar | YES |  |
| 9 | `idreferencias` | varchar | YES |  |
| 10 | `fechaalta` | timestamp(3) | YES |  |
| 11 | `idempresas` | bigint | YES |  |
| 12 | `idcentros` | bigint | YES |  |
| 13 | `idsecciones` | bigint | YES |  |
| 14 | `idubicaciones` | varchar | YES |  |
| 15 | `stock` | double | YES |  |
| 16 | `precio` | double | YES |  |
| 17 | `pmc` | double | YES |  |
| 18 | `confirmado` | bigint | YES |  |
| 19 | `unidades` | double | YES |  |
| 20 | `dtoporc` | double | YES |  |
| 21 | `idtarifas` | bigint | YES |  |
| 22 | `idclasificacion1movimiento` | varchar | YES |  |
| 23 | `hostmod` | varchar | YES |  |
| 24 | `usermod` | bigint | YES |  |
| 25 | `fechamod` | timestamp(3) | YES |  |
| 26 | `versionfila` | bigint | YES |  |
| 27 | `fechadocumento` | timestamp(3) | YES |  |
| 28 | `ida�o` | varchar | YES |  |
| 29 | `serie` | varchar | YES |  |
| 30 | `numero` | varchar | YES |  |
| 31 | `idterceros` | bigint | YES |  |
| 32 | `numdet` | bigint | YES |  |
| 33 | `seriefactura` | varchar | YES |  |
| 34 | `factura` | varchar | YES |  |
| 35 | `a�ofactura` | varchar | YES |  |
| 36 | `fechafactura` | timestamp(3) | YES |  |
| 37 | `idusuario` | bigint | YES |  |
| 38 | `loginguardadoautomatico` | bigint | YES |  |
| 39 | `hostguardadoautomatico` | varchar | YES |  |
| 40 | `fechaguardadoautomatico` | timestamp(3) | YES |  |
| 41 | `loginpteconfirmar` | bigint | YES |  |
| 42 | `hostpteconfirmar` | varchar | YES |  |
| 43 | `fechapteconfirmar` | timestamp(3) | YES |  |
| 44 | `idcentrosdestino` | bigint | YES |  |
| 45 | `idseccionesdestino` | bigint | YES |  |
| 46 | `idubicacionesdestino` | varchar | YES |  |
| 47 | `idcausaregularizacion` | bigint | YES |  |
| 48 | `idcausatraspaso` | bigint | YES |  |
| 49 | `a�oot` | varchar | YES |  |
| 50 | `serieot` | varchar | YES |  |
| 51 | `numot` | bigint | YES |  |
| 52 | `idtrabajo` | bigint | YES |  |
| 53 | `idempleadosalta` | bigint | YES |  |
| 54 | `fechacierre` | timestamp(3) | YES |  |
| 55 | `gastosadicionales` | double | YES |  |
| 56 | `gastosadicionalesalbaran` | double | YES |  |
| 57 | `incrementopvp` | double | YES |  |
| 58 | `undenvaseventa` | double | YES |  |
| 59 | `idestadoscompras` | varchar | YES |  |
| 60 | `idincidenciatipos` | varchar | YES |  |
| 61 | `undenvasecompra` | double | YES |  |
| 62 | `codras` | varchar | YES |  |
| 63 | `idimputaciontipos` | bigint | YES |  |
| 64 | `idtipocompra` | bigint | YES |  |
| 65 | `portes` | varchar | YES |  |
| 66 | `embalajes` | varchar | YES |  |
| 67 | `iddepartamentodestino` | varchar | YES |  |
| 68 | `descripcionmovimientotipo` | varchar | YES |  |
| 69 | `nombreempresa` | varchar | YES |  |
| 70 | `nombrecentro` | varchar | YES |  |
| 71 | `descripcionmr` | varchar | YES |  |
| 72 | `descripcionseccion` | varchar | YES |  |
| 73 | `iddepartamentos` | varchar | YES |  |
| 74 | `tipocargotaller` | varchar | YES |  |
| 75 | `ida�oppc` | varchar | YES |  |
| 76 | `idserieppc` | varchar | YES |  |
| 77 | `numeroppc` | varchar | YES |  |
| 78 | `numerodetppc` | varchar | YES |  |
| 79 | `tasas` | varchar | YES |  |
| 80 | `nombretercero` | varchar | YES |  |
| 81 | `nifcif` | varchar | YES |  |
| 82 | `idclientecategorias` | varchar | YES |  |
| 83 | `idmotivosabono` | varchar | YES |  |
| 84 | `descripcioncategoriacliente` | varchar | YES |  |
| 85 | `nombrecentrodestino` | varchar | YES |  |
| 86 | `descripcionsecciondestino` | varchar | YES |  |
| 87 | `iddepartamentosdestino` | varchar | YES |  |
| 88 | `descripcioncausaregularizacion` | varchar | YES |  |
| 89 | `descripciontipocompra` | varchar | YES |  |
| 90 | `descripcioncausaabonotipo` | varchar | YES |  |
| 91 | `descripcionimputaciontipos` | varchar | YES |  |
| 92 | `nombreempleado` | varchar | YES |  |
| 93 | `nombrefabricante` | varchar | YES |  |
| 94 | `descripcionreferencia` | varchar | YES |  |
| 95 | `descripcioncausatraspaso` | varchar | YES |  |
| 96 | `idfabricantes` | varchar | YES |  |
| 97 | `idclasificacion1` | varchar | YES |  |
| 98 | `idclasificacion2` | varchar | YES |  |
| 99 | `idclasificacion3` | varchar | YES |  |
| 100 | `idclasificacion4` | varchar | YES |  |
| 101 | `idclasificacion5` | varchar | YES |  |
| 102 | `idclasificacion6` | varchar | YES |  |
| 103 | `iddescuentos` | varchar | YES |  |
| 104 | `idrutasrecogida` | varchar | YES |  |
| 105 | `hostrecogida` | varchar | YES |  |
| 106 | `fecharecogida` | timestamp(3) | YES |  |
| 107 | `idempleadosrecogida` | varchar | YES |  |
| 108 | `unidadesrecogida` | varchar | YES |  |
| 109 | `idbultos` | varchar | YES |  |
| 110 | `idempleadosconfirmacion` | varchar | YES |  |
| 111 | `fechaconfirmacion` | timestamp(3) | YES |  |
| 112 | `hostconfirmacion` | varchar | YES |  |
| 113 | `unidadesalbaran` | varchar | YES |  |
| 114 | `idempleadosrecepcion` | varchar | YES |  |
| 115 | `hostrecepcion` | varchar | YES |  |
| 116 | `fecharecepcion` | timestamp(3) | YES |  |
| 117 | `unidadesrecibidas` | varchar | YES |  |
| 118 | `fechaubicacion` | timestamp(3) | YES |  |
| 119 | `idempleadosubicacion` | varchar | YES |  |
| 120 | `hostentrega` | varchar | YES |  |
| 121 | `fechaentrega` | timestamp(3) | YES |  |
| 122 | `idempleadosentrega` | varchar | YES |  |
| 123 | `hostubicacion` | varchar | YES |  |
| 124 | `nombreempleadoalta` | varchar | YES |  |
| 125 | `nombreempleadorecogida` | varchar | YES |  |
| 126 | `nombreempleadoconfirmacion` | varchar | YES |  |
| 127 | `nombreempleadorecepcion` | varchar | YES |  |
| 128 | `nombreempleadoubicacion` | varchar | YES |  |
| 129 | `nombreempleadoentrega` | varchar | YES |  |
| 130 | `descripcionincidenciatipos` | varchar | YES |  |
| 131 | `idpedidotipoventas` | varchar | YES |  |
| 132 | `descripcionpedidotipoventas` | varchar | YES |  |
| 133 | `nombremecanico` | varchar | YES |  |
| 134 | `nombretercerotrabajo` | varchar | YES |  |
| 135 | `apellido1tercerotrabajo` | varchar | YES |  |
| 136 | `apellido2tercerotrabajo` | varchar | YES |  |
| 137 | `nombrecomercialtercerotrabajo` | varchar | YES |  |
| 138 | `ventaespecial` | bigint | YES |  |
| 139 | `idtercerostrabajo` | varchar | YES |  |
| 140 | `codigobulto` | varchar | YES |  |
| 141 | `volumen` | double | YES |  |
| 142 | `factorcambiopmcontravalor` | double | YES |  |
| 143 | `descripcionclasificacion1` | varchar | YES |  |
| 144 | `descripcionclasificacion2` | varchar | YES |  |
| 145 | `descripcionclasificacion3` | varchar | YES |  |
| 146 | `descripcionclasificacion4` | varchar | YES |  |
| 147 | `descripcionclasificacion5` | varchar | YES |  |
| 148 | `descripcionclasificacion6` | varchar | YES |  |
| 149 | `descripcionclasificacion1movimiento` | varchar | YES |  |
| 150 | `preciocompra` | varchar | YES |  |
| 151 | `idmonedas` | varchar | YES |  |
| 152 | `factorcambiomoneda` | varchar | YES |  |
| 153 | `idusuariosautorizacion` | varchar | YES |  |
| 154 | `nombreusuarioautorizacion` | varchar | YES |  |
| 155 | `idnegociotipos` | varchar | YES |  |
| 156 | `nombreempleadovendedorrecambios` | varchar | YES |  |
| 157 | `seriefacturataller` | varchar | YES |  |
| 158 | `numerofacturataller` | varchar | YES |  |
| 159 | `a�ofacturataller` | varchar | YES |  |
| 160 | `fechafacturataller` | timestamp(3) | YES |  |
| 161 | `vin` | varchar | YES |  |
| 162 | `descripcionpedidotipocompras` | varchar | YES |  |
| 163 | `load_date` | varchar | YES |  |

### stage.spiga_cotizacionesvn

**Columnas:** 81

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `fkofertasestados` | bigint | YES |  |
| 7 | `idempresas` | bigint | YES |  |
| 8 | `idcentros` | bigint | YES |  |
| 9 | `idofertas` | bigint | YES |  |
| 10 | `idterceros` | bigint | YES |  |
| 11 | `idclientespotentradas` | bigint | YES |  |
| 12 | `idmodulos` | varchar | YES |  |
| 13 | `totaloferta` | double | YES |  |
| 14 | `nombremarca` | varchar | YES |  |
| 15 | `nombregama` | varchar | YES |  |
| 16 | `fechacontrato` | timestamp(3) | YES |  |
| 17 | `numcontrato` | varchar | YES |  |
| 18 | `idventatipos` | varchar | YES |  |
| 19 | `fechaprevista` | timestamp(3) | YES |  |
| 20 | `numpedidovnreserva` | varchar | YES |  |
| 21 | `observacionesinternas` | varchar | YES |  |
| 22 | `observacionesexternas` | varchar | YES |  |
| 23 | `idmonedas` | bigint | YES |  |
| 24 | `factorcambiomoneda` | double | YES |  |
| 25 | `fechaalta` | timestamp(3) | YES |  |
| 26 | `a�ooferta` | varchar | YES |  |
| 27 | `serieoferta` | varchar | YES |  |
| 28 | `numoferta` | varchar | YES |  |
| 29 | `idcentrospedido` | bigint | YES |  |
| 30 | `idventamarcatipos` | varchar | YES |  |
| 31 | `diasentregafabrica` | bigint | YES |  |
| 32 | `vin` | varchar | YES |  |
| 33 | `matricula` | varchar | YES |  |
| 34 | `nombre` | varchar | YES |  |
| 35 | `idmarcas` | bigint | YES |  |
| 36 | `idgamas` | bigint | YES |  |
| 37 | `codmodelo` | varchar | YES |  |
| 38 | `extmodelo` | varchar | YES |  |
| 39 | `a�omodelo` | varchar | YES |  |
| 40 | `idversiones` | varchar | YES |  |
| 41 | `idtarifas` | bigint | YES |  |
| 42 | `codexternomodelo` | varchar | YES |  |
| 43 | `nombrecentro` | varchar | YES |  |
| 44 | `fechabajacliente` | timestamp(3) | YES |  |
| 45 | `telefonomovil` | varchar | YES |  |
| 46 | `email` | varchar | YES |  |
| 47 | `fechaautorizacion` | timestamp(3) | YES |  |
| 48 | `fechaaceptacion` | timestamp(3) | YES |  |
| 49 | `fechaventa` | timestamp(3) | YES |  |
| 50 | `nombrevendedorasignado` | varchar | YES |  |
| 51 | `importesaldado` | double | YES |  |
| 52 | `idplantillacalculo` | varchar | YES |  |
| 53 | `descripcionplantilla` | varchar | YES |  |
| 54 | `importevoacambio` | double | YES |  |
| 55 | `nifcifclientepot` | varchar | YES |  |
| 56 | `importe` | double | YES |  |
| 57 | `porcentaje` | double | YES |  |
| 58 | `nombrevendedor` | varchar | YES |  |
| 59 | `pkopcionales` | varchar | YES |  |
| 60 | `idimsconcesionarios` | bigint | YES |  |
| 61 | `idimscuentas` | bigint | YES |  |
| 62 | `idimssucursales` | bigint | YES |  |
| 63 | `idimsvendedores` | bigint | YES |  |
| 64 | `nombreimsvendedor` | varchar | YES |  |
| 65 | `idsecciones` | bigint | YES |  |
| 66 | `fechasalida` | timestamp(3) | YES |  |
| 67 | `vosentregados` | bigint | YES |  |
| 68 | `idvehiculos` | bigint | YES |  |
| 69 | `codclientepot` | bigint | YES |  |
| 70 | `descripcion` | varchar | YES |  |
| 71 | `nombremodelo` | varchar | YES |  |
| 72 | `nombreversion` | varchar | YES |  |
| 73 | `descripcionofertasestados` | varchar | YES |  |
| 74 | `descripcionsecciones` | varchar | YES |  |
| 75 | `estadofinanciacion` | varchar | YES |  |
| 76 | `intencionescompradescripcion` | varchar | YES |  |
| 77 | `clientepotclasificaciondescripcion` | varchar | YES |  |
| 78 | `descripcionprocedencia` | varchar | YES |  |
| 79 | `descripcionsalidatipos` | varchar | YES |  |
| 80 | `fechaentrada` | timestamp(3) | YES |  |
| 81 | `load_date` | varchar | YES |  |

### stage.spiga_cotizacionesvo

**Columnas:** 72

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idvehiculos` | bigint | YES |  |
| 7 | `fkofertasestados` | bigint | YES |  |
| 8 | `idempresas` | bigint | YES |  |
| 9 | `idcentros` | bigint | YES |  |
| 10 | `idofertas` | bigint | YES |  |
| 11 | `idterceros` | bigint | YES |  |
| 12 | `idclientespotentradas` | bigint | YES |  |
| 13 | `idmonedas` | bigint | YES |  |
| 14 | `factorcambiomoneda` | double | YES |  |
| 15 | `a�ooferta` | varchar | YES |  |
| 16 | `serieoferta` | varchar | YES |  |
| 17 | `numoferta` | varchar | YES |  |
| 18 | `idmodulos` | varchar | YES |  |
| 19 | `totaloferta` | double | YES |  |
| 20 | `idmarcas` | bigint | YES |  |
| 21 | `idgamas` | bigint | YES |  |
| 22 | `codmodelo` | varchar | YES |  |
| 23 | `extmodelo` | varchar | YES |  |
| 24 | `a�omodelo` | varchar | YES |  |
| 25 | `idversiones` | varchar | YES |  |
| 26 | `nombremarca` | varchar | YES |  |
| 27 | `nombregama` | varchar | YES |  |
| 28 | `serieexpedientereserva` | varchar | YES |  |
| 29 | `numexpedientereserva` | bigint | YES |  |
| 30 | `a�oexpedientereserva` | varchar | YES |  |
| 31 | `idcentrosexpedientereserva` | bigint | YES |  |
| 32 | `fechareserva` | timestamp(3) | YES |  |
| 33 | `idofertasestados` | bigint | YES |  |
| 34 | `vin` | varchar | YES |  |
| 35 | `matricula` | varchar | YES |  |
| 36 | `nombre` | varchar | YES |  |
| 37 | `nombrecentro` | varchar | YES |  |
| 38 | `fechaautorizacion` | timestamp(3) | YES |  |
| 39 | `fechaaceptacion` | timestamp(3) | YES |  |
| 40 | `nombrevendedorasignado` | varchar | YES |  |
| 41 | `importesaldado` | double | YES |  |
| 42 | `nifcifclientepot` | varchar | YES |  |
| 43 | `idplantillacalculo` | varchar | YES |  |
| 44 | `descripcionplantilla` | varchar | YES |  |
| 45 | `importevoacambio` | double | YES |  |
| 46 | `codclientepot` | bigint | YES |  |
| 47 | `telefonomovil` | varchar | YES |  |
| 48 | `email` | varchar | YES |  |
| 49 | `importe` | double | YES |  |
| 50 | `porcentaje` | double | YES |  |
| 51 | `nombrevendedor` | varchar | YES |  |
| 52 | `idopcionalescolorvo` | varchar | YES |  |
| 53 | `idopcionalestapizadovo` | varchar | YES |  |
| 54 | `nombreempresa` | varchar | YES |  |
| 55 | `tercerointeresado` | varchar | YES |  |
| 56 | `idsecciones` | bigint | YES |  |
| 57 | `descripcionsecciones` | varchar | YES |  |
| 58 | `fechaalta` | timestamp(3) | YES |  |
| 59 | `idopcionales` | varchar | YES |  |
| 60 | `descripcionprocedencia` | varchar | YES |  |
| 61 | `fechasalida` | timestamp(3) | YES |  |
| 62 | `vosentregados` | bigint | YES |  |
| 63 | `nombremodelo` | varchar | YES |  |
| 64 | `nombreversion` | varchar | YES |  |
| 65 | `descripcion` | varchar | YES |  |
| 66 | `descripcioncolorvo` | varchar | YES |  |
| 67 | `descripciontapizadovo` | varchar | YES |  |
| 68 | `descripcionofertaestados` | varchar | YES |  |
| 69 | `intencionescompradescripcion` | varchar | YES |  |
| 70 | `clientepotclasificaciondescripcion` | varchar | YES |  |
| 71 | `descripcionsalidatipos` | varchar | YES |  |
| 72 | `load_date` | varchar | YES |  |

### stage.spiga_datosterceros

**Columnas:** 50

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `pkfkempresas` | bigint | YES |  |
| 7 | `nombreempresa` | varchar | YES |  |
| 8 | `pkterceros` | bigint | YES |  |
| 9 | `fkpaises` | varchar | YES |  |
| 10 | `fkterceroclases` | bigint | YES |  |
| 11 | `nombreterceroclases` | varchar | YES |  |
| 12 | `nifcif` | varchar | YES |  |
| 13 | `nifcif_fechaexpedicion` | timestamp(3) | YES |  |
| 14 | `nifcif_lugarexpedicion` | varchar | YES |  |
| 15 | `nombre` | varchar | YES |  |
| 16 | `apellido1` | varchar | YES |  |
| 17 | `apellido2` | varchar | YES |  |
| 18 | `nombrecomercial` | varchar | YES |  |
| 19 | `fechaalta` | timestamp(3) | YES |  |
| 20 | `fechabaja` | timestamp(3) | YES |  |
| 21 | `fkdocumentaciontipos` | bigint | YES |  |
| 22 | `descrpciondocumentaciontipos` | varchar | YES |  |
| 23 | `fknaturalezajuridicatipos` | varchar | YES |  |
| 24 | `descripcionnaturalezajuridicatipos` | varchar | YES |  |
| 25 | `tipocontribuyente` | varchar | YES |  |
| 26 | `descripciontipocontribuyente` | varchar | YES |  |
| 27 | `agenteretenedor` | varchar | YES |  |
| 28 | `fechatipocontribuyente` | timestamp(3) | YES |  |
| 29 | `resolucion` | varchar | YES |  |
| 30 | `fkcodigospostales` | varchar | YES |  |
| 31 | `poblacion` | varchar | YES |  |
| 32 | `provincia` | varchar | YES |  |
| 33 | `fkprofesiones` | bigint | YES |  |
| 34 | `descripcionprofesiones` | varchar | YES |  |
| 35 | `fktercerocargos` | bigint | YES |  |
| 36 | `descripcionterceroscargos` | varchar | YES |  |
| 37 | `fkterceroformacionniveles` | bigint | YES |  |
| 38 | `descripcionterceroformacionniveles` | varchar | YES |  |
| 39 | `fechanacimiento` | timestamp(3) | YES |  |
| 40 | `fechacarnet` | timestamp(3) | YES |  |
| 41 | `fechacarnetcaducidad` | timestamp(3) | YES |  |
| 42 | `numerohijos` | bigint | YES |  |
| 43 | `fkestadociviltipos` | varchar | YES |  |
| 44 | `descripcionestadociviltipos` | varchar | YES |  |
| 45 | `sexo` | varchar | YES |  |
| 46 | `fkactividadtipos` | varchar | YES |  |
| 47 | `descripcionactividadtipos` | varchar | YES |  |
| 48 | `claseconcepto` | varchar | YES |  |
| 49 | `numlicenciaconducir` | varchar | YES |  |
| 50 | `load_date` | varchar | YES |  |

### stage.spiga_empleados

**Columnas:** 33

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempleados` | bigint | YES |  |
| 7 | `idprofesiones` | bigint | YES |  |
| 8 | `idterceros` | bigint | YES |  |
| 9 | `idpagoformasnomina` | varchar | YES |  |
| 10 | `numeross` | varchar | YES |  |
| 11 | `porcretencion` | double | YES |  |
| 12 | `cuentaentidad` | varchar | YES |  |
| 13 | `cuentasucursal` | varchar | YES |  |
| 14 | `cuentadc` | varchar | YES |  |
| 15 | `cuentanumero` | varchar | YES |  |
| 16 | `cuentaidpaises` | varchar | YES |  |
| 17 | `cuentaiban` | varchar | YES |  |
| 18 | `cuentaswift` | varchar | YES |  |
| 19 | `fechaalta` | timestamp(3) | YES |  |
| 20 | `fechabaja` | timestamp(3) | YES |  |
| 21 | `usermod` | bigint | YES |  |
| 22 | `hostmod` | varchar | YES |  |
| 23 | `versionfila` | bigint | YES |  |
| 24 | `idusuarios` | bigint | YES |  |
| 25 | `idempleadocuentabancotipos` | varchar | YES |  |
| 26 | `nombre` | varchar | YES |  |
| 27 | `apellido1` | varchar | YES |  |
| 28 | `apellido2` | varchar | YES |  |
| 29 | `nifcif` | varchar | YES |  |
| 30 | `usermodtercero` | bigint | YES |  |
| 31 | `hostmodtercero` | varchar | YES |  |
| 32 | `versionfilatercero` | bigint | YES |  |
| 33 | `load_date` | varchar | YES |  |

### stage.spiga_entradasataller

**Columnas:** 119

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | varchar | YES |  |
| 2 | `idconsecutivo` | varchar | YES |  |
| 3 | `ano_periodo` | varchar | YES |  |
| 4 | `mes_periodo` | varchar | YES |  |
| 5 | `fechadecorte` | varchar | YES |  |
| 6 | `idempresas` | varchar | YES |  |
| 7 | `idcentros` | varchar | YES |  |
| 8 | `a�oot` | varchar | YES |  |
| 9 | `serieot` | varchar | YES |  |
| 10 | `numot` | varchar | YES |  |
| 11 | `numtrabajo` | varchar | YES |  |
| 12 | `idtrabajoestados` | varchar | YES |  |
| 13 | `descripcion` | varchar | YES |  |
| 14 | `idterceros` | varchar | YES |  |
| 15 | `preciohora` | varchar | YES |  |
| 16 | `numeropoliza` | varchar | YES |  |
| 17 | `importefranquicia` | varchar | YES |  |
| 18 | `idmanoobratipos` | varchar | YES |  |
| 19 | `idtrabajotipos` | varchar | YES |  |
| 20 | `idsecciones` | varchar | YES |  |
| 21 | `nombreseccion` | varchar | YES |  |
| 22 | `preciocoste` | varchar | YES |  |
| 23 | `idseccioncargos` | varchar | YES |  |
| 24 | `idcargotipos` | varchar | YES |  |
| 25 | `observaciones` | varchar | YES |  |
| 26 | `fechaalta` | varchar | YES |  |
| 27 | `fechamodificacion` | varchar | YES |  |
| 28 | `fechacierre` | varchar | YES |  |
| 29 | `a�opresupuesto` | varchar | YES |  |
| 30 | `seriepresupuesto` | varchar | YES |  |
| 31 | `idpresupuesto` | varchar | YES |  |
| 32 | `a�ofactura` | varchar | YES |  |
| 33 | `seriefactura` | varchar | YES |  |
| 34 | `numfactura` | varchar | YES |  |
| 35 | `iddepartamentocargointerno` | varchar | YES |  |
| 36 | `idimputaciontipos` | varchar | YES |  |
| 37 | `idseccioncargointerno` | varchar | YES |  |
| 38 | `idcentrosdestino` | varchar | YES |  |
| 39 | `idseriesgarantias` | varchar | YES |  |
| 40 | `numgarantias` | varchar | YES |  |
| 41 | `a�ogarantias` | varchar | YES |  |
| 42 | `idempleadosalta` | varchar | YES |  |
| 43 | `idempleadoscierre` | varchar | YES |  |
| 44 | `fechaenvioinspeccion` | varchar | YES |  |
| 45 | `fechafacturacion` | varchar | YES |  |
| 46 | `numeroautorizacion` | varchar | YES |  |
| 47 | `usermod` | varchar | YES |  |
| 48 | `hostmod` | varchar | YES |  |
| 49 | `versionfila` | varchar | YES |  |
| 50 | `a�oasiento` | varchar | YES |  |
| 51 | `idasiento` | varchar | YES |  |
| 52 | `a�oasiento_garantiafacturada` | varchar | YES |  |
| 53 | `idasiento_garantiafacturada` | varchar | YES |  |
| 54 | `trabajorepetido` | varchar | YES |  |
| 55 | `numsiniestro` | varchar | YES |  |
| 56 | `respuestainspeccion` | varchar | YES |  |
| 57 | `numgarantiamarca` | varchar | YES |  |
| 58 | `importemo` | varchar | YES |  |
| 59 | `importemopresupuesto` | varchar | YES |  |
| 60 | `importemat` | varchar | YES |  |
| 61 | `importematpresupuesto` | varchar | YES |  |
| 62 | `importesub` | varchar | YES |  |
| 63 | `importesubpresupuesto` | varchar | YES |  |
| 64 | `importevar` | varchar | YES |  |
| 65 | `importevarpresupuesto` | varchar | YES |  |
| 66 | `importepint` | varchar | YES |  |
| 67 | `importepintpresupuesto` | varchar | YES |  |
| 68 | `horasmo` | varchar | YES |  |
| 69 | `horasmopresupuesto` | varchar | YES |  |
| 70 | `fechaentrada` | varchar | YES |  |
| 71 | `idcalletipos` | varchar | YES |  |
| 72 | `matricula` | varchar | YES |  |
| 73 | `vin` | varchar | YES |  |
| 74 | `fechamatriculacion` | varchar | YES |  |
| 75 | `idmarcas` | varchar | YES |  |
| 76 | `nombremarca` | varchar | YES |  |
| 77 | `idgamas` | varchar | YES |  |
| 78 | `nombregama` | varchar | YES |  |
| 79 | `nombreasesor` | varchar | YES |  |
| 80 | `nombrepropietario` | varchar | YES |  |
| 81 | `telefonoparticular` | varchar | YES |  |
| 82 | `telefonomovil` | varchar | YES |  |
| 83 | `idempleados` | varchar | YES |  |
| 84 | `descripciontrabajotipos` | varchar | YES |  |
| 85 | `diferenciadias` | varchar | YES |  |
| 86 | `descripcionsegmento` | varchar | YES |  |
| 87 | `email` | varchar | YES |  |
| 88 | `descripciontipocalle` | varchar | YES |  |
| 89 | `nombrecalle` | varchar | YES |  |
| 90 | `numero` | varchar | YES |  |
| 91 | `bloque` | varchar | YES |  |
| 92 | `piso` | varchar | YES |  |
| 93 | `puerta` | varchar | YES |  |
| 94 | `complemento` | varchar | YES |  |
| 95 | `complemento2` | varchar | YES |  |
| 96 | `poblacion` | varchar | YES |  |
| 97 | `idcodigospostales` | varchar | YES |  |
| 98 | `nombreestado` | varchar | YES |  |
| 99 | `esabono` | varchar | YES |  |
| 100 | `esabonogarantia` | varchar | YES |  |
| 101 | `idrecepciontipos` | varchar | YES |  |
| 102 | `kmts` | varchar | YES |  |
| 103 | `fechaprevistaentrega` | varchar | YES |  |
| 104 | `fechaentrega` | varchar | YES |  |
| 105 | `idvehiculos` | varchar | YES |  |
| 106 | `nombretercerocargo` | varchar | YES |  |
| 107 | `apellido1tercerocargo` | varchar | YES |  |
| 108 | `apellido2tercerocargo` | varchar | YES |  |
| 109 | `nombrevendedor` | varchar | YES |  |
| 110 | `apellido1vendedor` | varchar | YES |  |
| 111 | `apellido2vendedor` | varchar | YES |  |
| 112 | `descripcionrecepcion` | varchar | YES |  |
| 113 | `idclientespotclasificaciones` | varchar | YES |  |
| 114 | `horasuso` | varchar | YES |  |
| 115 | `idmotivoentrada` | varchar | YES |  |
| 116 | `descripcionmotivoentrada` | varchar | YES |  |
| 117 | `asesorservicioresponsable` | varchar | YES |  |
| 118 | `vehiculocortesia` | varchar | YES |  |
| 119 | `load_date` | varchar | YES |  |

### stage.spiga_facturadosnoentregadosvn

**Columnas:** 154

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `numventa` | bigint | YES |  |
| 12 | `fechaventa` | timestamp(3) | YES |  |
| 13 | `comisionagente` | double | YES |  |
| 14 | `idpaisesexportacion` | varchar | YES |  |
| 15 | `a�oasientoentrega` | varchar | YES |  |
| 16 | `idasientosentrega` | bigint | YES |  |
| 17 | `idmonedas` | bigint | YES |  |
| 18 | `factorcambiomoneda` | double | YES |  |
| 19 | `fkterceros_agente` | bigint | YES |  |
| 20 | `nombreagente` | varchar | YES |  |
| 21 | `seriefacturacompra` | varchar | YES |  |
| 22 | `numfacturacompra` | varchar | YES |  |
| 23 | `a�ofacturacompra` | varchar | YES |  |
| 24 | `fechafacturacompra` | timestamp(3) | YES |  |
| 25 | `idcompraestados` | varchar | YES |  |
| 26 | `descripcioncompraestados` | varchar | YES |  |
| 27 | `preciocompra` | double | YES |  |
| 28 | `ventafinal` | bigint | YES |  |
| 29 | `facturaprincipal` | varchar | YES |  |
| 30 | `fechafacturaprincipal` | timestamp(3) | YES |  |
| 31 | `terceroprincipal` | bigint | YES |  |
| 32 | `nifcifprincipal` | varchar | YES |  |
| 33 | `perfilterceroprincipal` | varchar | YES |  |
| 34 | `nombreterceroprincipal` | varchar | YES |  |
| 35 | `direccionterceroprincipal` | varchar | YES |  |
| 36 | `codigopostalterceroprincipal` | varchar | YES |  |
| 37 | `idcodigospostalesterceroprincipal` | varchar | YES |  |
| 38 | `poblacionterceroprincipal` | varchar | YES |  |
| 39 | `provinciaterceroprincipal` | varchar | YES |  |
| 40 | `telefonoprincipalterceroprincipal` | varchar | YES |  |
| 41 | `telefonoparticularterceroprincipal` | varchar | YES |  |
| 42 | `telefonomovilterceroprincipal` | varchar | YES |  |
| 43 | `telefonotrabajoterceroprincipal` | varchar | YES |  |
| 44 | `facturasecundaria` | varchar | YES |  |
| 45 | `fechafacturasecundaria` | timestamp(3) | YES |  |
| 46 | `tercerosecundaria` | bigint | YES |  |
| 47 | `nombretercerosecundaria` | varchar | YES |  |
| 48 | `direcciontercerosecundaria` | varchar | YES |  |
| 49 | `poblaciontercerosecundaria` | varchar | YES |  |
| 50 | `provinciatercerosecundaria` | varchar | YES |  |
| 51 | `fechamatriculacion` | timestamp(3) | YES |  |
| 52 | `fechadespacho` | timestamp(3) | YES |  |
| 53 | `vin` | varchar | YES |  |
| 54 | `matricula` | varchar | YES |  |
| 55 | `sitiomatricula` | varchar | YES |  |
| 56 | `numeromotor` | varchar | YES |  |
| 57 | `idmarcas` | bigint | YES |  |
| 58 | `nombremarca` | varchar | YES |  |
| 59 | `idgamas` | bigint | YES |  |
| 60 | `nombregama` | varchar | YES |  |
| 61 | `codmodelo` | varchar | YES |  |
| 62 | `extmodelo` | varchar | YES |  |
| 63 | `a�omodelo` | varchar | YES |  |
| 64 | `nombremodelo` | varchar | YES |  |
| 65 | `idempleados` | bigint | YES |  |
| 66 | `nombrevendedor` | varchar | YES |  |
| 67 | `idventatipos` | varchar | YES |  |
| 68 | `descripcionventatipos` | varchar | YES |  |
| 69 | `idcompratipos` | varchar | YES |  |
| 70 | `descripcioncompratipos` | varchar | YES |  |
| 71 | `idventamarcatipos` | varchar | YES |  |
| 72 | `descripcionventamarcatipos` | varchar | YES |  |
| 73 | `idventafinanciaciontipos` | varchar | YES |  |
| 74 | `descripcionventafinanciaciontipos` | varchar | YES |  |
| 75 | `idversiones` | varchar | YES |  |
| 76 | `descripcionversion` | varchar | YES |  |
| 77 | `baseimponible` | double | YES |  |
| 78 | `baseexenta` | double | YES |  |
| 79 | `impuestos` | double | YES |  |
| 80 | `acondicionamiento` | double | YES |  |
| 81 | `totalventa` | double | YES |  |
| 82 | `diferencialanticipo` | double | YES |  |
| 83 | `identradatipos` | varchar | YES |  |
| 84 | `provisiondegastosinternos` | double | YES |  |
| 85 | `provisiondegastosexternos` | double | YES |  |
| 86 | `descripcionentradatipos` | varchar | YES |  |
| 87 | `complemento2terceroprincipal` | varchar | YES |  |
| 88 | `idofertas` | bigint | YES |  |
| 89 | `fechaoferta` | timestamp(3) | YES |  |
| 90 | `nombrefinanciera` | varchar | YES |  |
| 91 | `apellido1financiera` | varchar | YES |  |
| 92 | `apellido2financiera` | varchar | YES |  |
| 93 | `nombreconductor` | varchar | YES |  |
| 94 | `apellido1conductor` | varchar | YES |  |
| 95 | `apellido2conductor` | varchar | YES |  |
| 96 | `idclientespotentradas` | bigint | YES |  |
| 97 | `nombrecentro` | varchar | YES |  |
| 98 | `idsecciones` | bigint | YES |  |
| 99 | `nombreseccion` | varchar | YES |  |
| 100 | `idterceroscolaborador` | bigint | YES |  |
| 101 | `nombrecolaborador` | varchar | YES |  |
| 102 | `detallaropcionalesfactura` | varchar | YES |  |
| 103 | `importevehiculoscambio` | double | YES |  |
| 104 | `expedientesvehiculoscambio` | varchar | YES |  |
| 105 | `comision` | varchar | YES |  |
| 106 | `idcalletiposprincipal` | varchar | YES |  |
| 107 | `nombrecalleprincipal` | varchar | YES |  |
| 108 | `numeroprincipal` | varchar | YES |  |
| 109 | `bloqueprincipal` | varchar | YES |  |
| 110 | `pisoprincipal` | varchar | YES |  |
| 111 | `puertaprincipal` | varchar | YES |  |
| 112 | `poblacionprincipal` | varchar | YES |  |
| 113 | `provinciaprincipal` | varchar | YES |  |
| 114 | `idcodigospostalesprincipal` | varchar | YES |  |
| 115 | `fechaentregacliente` | timestamp(3) | YES |  |
| 116 | `versionfila` | bigint | YES |  |
| 117 | `idvehiculos` | bigint | YES |  |
| 118 | `vnfechainiciogarantia` | varchar | YES |  |
| 119 | `mesesgarantiaobligatoriavn` | bigint | YES |  |
| 120 | `mesesgarantiaobligatoriavn_chapa` | bigint | YES |  |
| 121 | `mesesgarantiaobligatoriavn_pintura` | bigint | YES |  |
| 122 | `mesesgarantiaobligatoriavn_motor` | bigint | YES |  |
| 123 | `nombresecundario` | varchar | YES |  |
| 124 | `apellido1secundario` | varchar | YES |  |
| 125 | `apellido2secundario` | varchar | YES |  |
| 126 | `idempleadoscolaborador` | bigint | YES |  |
| 127 | `nombreempleadocolaborador` | varchar | YES |  |
| 128 | `nombrepropietario` | varchar | YES |  |
| 129 | `apellido1propietario` | varchar | YES |  |
| 130 | `apellido2propietario` | varchar | YES |  |
| 131 | `codexternomodelo` | varchar | YES |  |
| 132 | `ubicacion` | varchar | YES |  |
| 133 | `idnegociotipos` | varchar | YES |  |
| 134 | `importependientecobro` | double | YES |  |
| 135 | `fechapazsalvo` | timestamp(3) | YES |  |
| 136 | `a�opazsalvo` | varchar | YES |  |
| 137 | `seriepazsalvo` | varchar | YES |  |
| 138 | `numpazsalvo` | bigint | YES |  |
| 139 | `nombreempleadoemitepse` | varchar | YES |  |
| 140 | `apellido1empleadoemitepse` | varchar | YES |  |
| 141 | `apellido2empleadoemitepse` | varchar | YES |  |
| 142 | `idtercerosalquilador` | bigint | YES |  |
| 143 | `nombrealquilador` | varchar | YES |  |
| 144 | `apellido1alquilador` | varchar | YES |  |
| 145 | `apellido2alquilador` | varchar | YES |  |
| 146 | `detallaropcionalesconcesionfactura` | varchar | YES |  |
| 147 | `detallarcampa�asfactura` | varchar | YES |  |
| 148 | `idseriestransporte` | varchar | YES |  |
| 149 | `idnumtransporte` | bigint | YES |  |
| 150 | `obsinternas` | varchar | YES |  |
| 151 | `nifcifvendedor` | varchar | YES |  |
| 152 | `margenventaimportador` | double | YES |  |
| 153 | `fecharecepcion` | timestamp(3) | YES |  |
| 154 | `load_date` | varchar | YES |  |

### stage.spiga_facturadosnoentregadosvo

**Columnas:** 138

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `numventa` | bigint | YES |  |
| 12 | `fechaventa` | timestamp(3) | YES |  |
| 13 | `kms` | bigint | YES |  |
| 14 | `idtercerosfinanciera` | bigint | YES |  |
| 15 | `nombrefinanciera` | varchar | YES |  |
| 16 | `idterceroscolaborador` | bigint | YES |  |
| 17 | `nombrecolaborador` | varchar | YES |  |
| 18 | `preciocompra` | double | YES |  |
| 19 | `pkcompraestados` | varchar | YES |  |
| 20 | `descripcioncompraestados` | varchar | YES |  |
| 21 | `ventafinal` | bigint | YES |  |
| 22 | `nombreproveedor` | varchar | YES |  |
| 23 | `facturacompra` | varchar | YES |  |
| 24 | `facturaprincipal` | varchar | YES |  |
| 25 | `terceroprincipal` | bigint | YES |  |
| 26 | `nifcifprincipal` | varchar | YES |  |
| 27 | `perfilterceroprincipal` | varchar | YES |  |
| 28 | `nombreterceroprincipal` | varchar | YES |  |
| 29 | `direccionterceroprincipal` | varchar | YES |  |
| 30 | `codigopostalterceroprincipal` | varchar | YES |  |
| 31 | `idcodigospostalesterceroprincipal` | varchar | YES |  |
| 32 | `poblacionterceroprincipal` | varchar | YES |  |
| 33 | `provinciaterceroprincipal` | varchar | YES |  |
| 34 | `clientecategoriaterceroprincipal` | varchar | YES |  |
| 35 | `telefonoprincipalterceroprincipal` | varchar | YES |  |
| 36 | `telefonoparticularterceroprincipal` | varchar | YES |  |
| 37 | `telefonomovilterceroprincipal` | varchar | YES |  |
| 38 | `telefonotrabajoterceroprincipal` | varchar | YES |  |
| 39 | `facturasecundaria` | varchar | YES |  |
| 40 | `tercerosecundaria` | bigint | YES |  |
| 41 | `nombretercerosecundaria` | varchar | YES |  |
| 42 | `direcciontercerosecundaria` | varchar | YES |  |
| 43 | `codigopostaltercerosecundaria` | varchar | YES |  |
| 44 | `idcodigospostalestercerosecundaria` | varchar | YES |  |
| 45 | `poblaciontercerosecundaria` | varchar | YES |  |
| 46 | `provinciatercerosecundaria` | varchar | YES |  |
| 47 | `telefonoprincipaltercerosecundaria` | varchar | YES |  |
| 48 | `telefonoparticulartercerosecundaria` | varchar | YES |  |
| 49 | `telefonomoviltercerosecundaria` | varchar | YES |  |
| 50 | `telefonotrabajotercerosecundaria` | varchar | YES |  |
| 51 | `fechamatriculacion` | timestamp(3) | YES |  |
| 52 | `fechadespacho` | timestamp(3) | YES |  |
| 53 | `vin` | varchar | YES |  |
| 54 | `matricula` | varchar | YES |  |
| 55 | `numeromotor` | varchar | YES |  |
| 56 | `idmarcas` | bigint | YES |  |
| 57 | `nombremarca` | varchar | YES |  |
| 58 | `idgamas` | bigint | YES |  |
| 59 | `nombregama` | varchar | YES |  |
| 60 | `codmodelo` | varchar | YES |  |
| 61 | `extmodelo` | varchar | YES |  |
| 62 | `a�omodelo` | varchar | YES |  |
| 63 | `nombremodelo` | varchar | YES |  |
| 64 | `idempleados` | bigint | YES |  |
| 65 | `nombrevendedor` | varchar | YES |  |
| 66 | `idventatipos` | varchar | YES |  |
| 67 | `descripcionventatipos` | varchar | YES |  |
| 68 | `idcompratipos` | varchar | YES |  |
| 69 | `descripcioncompratipos` | varchar | YES |  |
| 70 | `idversiones` | varchar | YES |  |
| 71 | `descripcionversion` | varchar | YES |  |
| 72 | `idventainternatipos` | varchar | YES |  |
| 73 | `descripcionventainternatipos` | varchar | YES |  |
| 74 | `baseimponible` | double | YES |  |
| 75 | `baseexenta` | double | YES |  |
| 76 | `importesuplidosgestoria` | double | YES |  |
| 77 | `importeprovision` | double | YES |  |
| 78 | `diferencialanticipo` | double | YES |  |
| 79 | `baseexentaventa` | double | YES |  |
| 80 | `importeimpuestoventa` | double | YES |  |
| 81 | `importegastos` | double | YES |  |
| 82 | `codigoagente` | varchar | YES |  |
| 83 | `expedientecambio` | varchar | YES |  |
| 84 | `esacambio` | bigint | YES |  |
| 85 | `idofertas` | bigint | YES |  |
| 86 | `fechaoferta` | timestamp(3) | YES |  |
| 87 | `localidadterceroprincipal` | varchar | YES |  |
| 88 | `complemento2terceroprincipal` | varchar | YES |  |
| 89 | `nombreconductor` | varchar | YES |  |
| 90 | `apellido1conductor` | varchar | YES |  |
| 91 | `apellido2conductor` | varchar | YES |  |
| 92 | `idclientespotentradasoferta` | bigint | YES |  |
| 93 | `nombrecentro` | varchar | YES |  |
| 94 | `comisioncolaborador` | double | YES |  |
| 95 | `idsecciones` | bigint | YES |  |
| 96 | `nombreseccion` | varchar | YES |  |
| 97 | `diasantiguedadstock` | bigint | YES |  |
| 98 | `mesesantiguedadstock` | bigint | YES |  |
| 99 | `precioventarecomendado` | double | YES |  |
| 100 | `expedientesvehiculoscambio` | varchar | YES |  |
| 101 | `importevehiculoscambio` | double | YES |  |
| 102 | `comision` | varchar | YES |  |
| 103 | `idcalletiposprincipal` | varchar | YES |  |
| 104 | `nombrecalleprincipal` | varchar | YES |  |
| 105 | `numeroprincipal` | varchar | YES |  |
| 106 | `bloqueprincipal` | varchar | YES |  |
| 107 | `pisoprincipal` | varchar | YES |  |
| 108 | `puertaprincipal` | varchar | YES |  |
| 109 | `poblacionprincipal` | varchar | YES |  |
| 110 | `provinciaprincipal` | varchar | YES |  |
| 111 | `idcodigospostalesprincipal` | varchar | YES |  |
| 112 | `fechaentregacliente` | timestamp(3) | YES |  |
| 113 | `fechapazsalvo` | timestamp(3) | YES |  |
| 114 | `a�opazsalvo` | varchar | YES |  |
| 115 | `seriepazsalvo` | varchar | YES |  |
| 116 | `numpazsalvo` | bigint | YES |  |
| 117 | `nombreempleadoemitepse` | varchar | YES |  |
| 118 | `apellido1empleadoemitepse` | varchar | YES |  |
| 119 | `apellido2empleadoemitepse` | varchar | YES |  |
| 120 | `nombresecundario` | varchar | YES |  |
| 121 | `apellido1secundario` | varchar | YES |  |
| 122 | `apellido2secundario` | varchar | YES |  |
| 123 | `idempleadoscolaborador` | bigint | YES |  |
| 124 | `nombreempleadocolaborador` | varchar | YES |  |
| 125 | `nombrepropietario` | varchar | YES |  |
| 126 | `apellido1propietario` | varchar | YES |  |
| 127 | `apellido2propietario` | varchar | YES |  |
| 128 | `totalventa` | double | YES |  |
| 129 | `impuestos` | double | YES |  |
| 130 | `codexternomodelo` | varchar | YES |  |
| 131 | `ubicacion` | varchar | YES |  |
| 132 | `idnegociotipos` | varchar | YES |  |
| 133 | `importependientecobro` | double | YES |  |
| 134 | `nifcifvendedor` | varchar | YES |  |
| 135 | `obsinternas` | varchar | YES |  |
| 136 | `fechafacturacompra` | timestamp(3) | YES |  |
| 137 | `fechafacturaprincipal` | timestamp(3) | YES |  |
| 138 | `load_date` | varchar | YES |  |

### stage.spiga_fechaprevistacompra

**Columnas:** 45

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresa` | bigint | YES |  |
| 7 | `idterceros` | bigint | YES |  |
| 8 | `nombre` | varchar | YES |  |
| 9 | `apellido1` | varchar | YES |  |
| 10 | `apellido2` | varchar | YES |  |
| 11 | `nifcif` | varchar | YES |  |
| 12 | `nombrecalle` | varchar | YES |  |
| 13 | `numero` | varchar | YES |  |
| 14 | `bloque` | varchar | YES |  |
| 15 | `piso` | varchar | YES |  |
| 16 | `puerta` | varchar | YES |  |
| 17 | `idcodigospostales` | varchar | YES |  |
| 18 | `poblacion` | varchar | YES |  |
| 19 | `provincia` | varchar | YES |  |
| 20 | `complemento` | varchar | YES |  |
| 21 | `complemento2` | varchar | YES |  |
| 22 | `idpaises` | varchar | YES |  |
| 23 | `idcalletipos` | varchar | YES |  |
| 24 | `descripcioncalletipos` | varchar | YES |  |
| 25 | `telefono` | varchar | YES |  |
| 26 | `email` | varchar | YES |  |
| 27 | `fechaprevistacambio` | timestamp(3) | YES |  |
| 28 | `fechaentrada` | timestamp(3) | YES |  |
| 29 | `idempleados` | bigint | YES |  |
| 30 | `nombreempleado` | varchar | YES |  |
| 31 | `descripcionentradatipos` | varchar | YES |  |
| 32 | `nombremodelo` | varchar | YES |  |
| 33 | `fechaalta` | timestamp(3) | YES |  |
| 34 | `idsecciones` | bigint | YES |  |
| 35 | `descripcion` | varchar | YES |  |
| 36 | `nombregama` | varchar | YES |  |
| 37 | `nombrecentro` | varchar | YES |  |
| 38 | `descripcionseccion` | varchar | YES |  |
| 39 | `fechaultimaactividad` | timestamp(3) | YES |  |
| 40 | `idclientespotclasificaciones` | bigint | YES |  |
| 41 | `fechasalida` | timestamp(3) | YES |  |
| 42 | `idsalidatipos` | varchar | YES |  |
| 43 | `idintencionescompra` | varchar | YES |  |
| 44 | `descripcion_intencionescompra` | varchar | YES |  |
| 45 | `load_date` | varchar | YES |  |

### stage.spiga_financiacionesventasvnvo

**Columnas:** 42

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `idofertapagos` | bigint | YES |  |
| 12 | `saldofavorcliente` | bigint | YES |  |
| 13 | `importefinanciado` | double | YES |  |
| 14 | `fechavencimiento` | timestamp(3) | YES |  |
| 15 | `fechainicio` | timestamp(3) | YES |  |
| 16 | `comisionfinanciera` | double | YES |  |
| 17 | `vin` | varchar | YES |  |
| 18 | `matricula` | varchar | YES |  |
| 19 | `comisionvehiculo` | varchar | YES |  |
| 20 | `idterceros` | bigint | YES |  |
| 21 | `nombrepropietario` | varchar | YES |  |
| 22 | `nifcifpropietario` | varchar | YES |  |
| 23 | `idtercerosfinanciera` | bigint | YES |  |
| 24 | `nombrefinanciera` | varchar | YES |  |
| 25 | `idempleados` | bigint | YES |  |
| 26 | `nombreempleado` | varchar | YES |  |
| 27 | `idtercerosagente` | bigint | YES |  |
| 28 | `nombreagente` | varchar | YES |  |
| 29 | `idmarcas` | bigint | YES |  |
| 30 | `nombremarca` | varchar | YES |  |
| 31 | `idgamas` | bigint | YES |  |
| 32 | `nombregama` | varchar | YES |  |
| 33 | `idempleadosgestor` | bigint | YES |  |
| 34 | `nombregestor` | varchar | YES |  |
| 35 | `fechaventa` | timestamp(3) | YES |  |
| 36 | `nombreempresa` | varchar | YES |  |
| 37 | `nombrecentro` | varchar | YES |  |
| 38 | `idmodulos` | varchar | YES |  |
| 39 | `estado` | varchar | YES |  |
| 40 | `descripcionsecciones` | varchar | YES |  |
| 41 | `fechaentregacliente` | timestamp(3) | YES |  |
| 42 | `load_date` | varchar | YES |  |

### stage.spiga_gastosvehiculosvo

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | integer | YES |  |
| 2 | `idconsecutivo` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `vin` | varchar | YES |  |
| 7 | `gis` | decimal(18,4) | YES |  |
| 8 | `gnis` | decimal(18,4) | YES |  |

### stage.spiga_habeasdata

**Columnas:** 14

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `pkterceros` | bigint | YES |  |
| 7 | `nombres` | varchar | YES |  |
| 8 | `fechaconsentimiento` | timestamp(3) | YES |  |
| 9 | `mesesvalidezconsentimiento` | bigint | YES |  |
| 10 | `descripcion` | varchar | YES |  |
| 11 | `mesesvalidez` | bigint | YES |  |
| 12 | `valorbool` | varchar | YES |  |
| 13 | `numdocumento` | varchar | YES |  |
| 14 | `load_date` | varchar | YES |  |

### stage.spiga_informafacturacion

**Columnas:** 130

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `tipo` | varchar | YES |  |
| 7 | `idempresas` | bigint | YES |  |
| 8 | `idcentros` | bigint | YES |  |
| 9 | `a�oot` | varchar | YES |  |
| 10 | `serieot` | varchar | YES |  |
| 11 | `numot` | bigint | YES |  |
| 12 | `numtrabajo` | bigint | YES |  |
| 13 | `idempleadocierre` | bigint | YES |  |
| 14 | `fechaalta` | timestamp(3) | YES |  |
| 15 | `fechacierre` | timestamp(3) | YES |  |
| 16 | `idseriesgarantias` | varchar | YES |  |
| 17 | `numalbaran` | bigint | YES |  |
| 18 | `a�oalbaran` | varchar | YES |  |
| 19 | `numgarantiamarca` | varchar | YES |  |
| 20 | `horasfacturadas` | bigint | YES |  |
| 21 | `importemobruto` | double | YES |  |
| 22 | `descuentomo` | double | YES |  |
| 23 | `importesubbruto` | double | YES |  |
| 24 | `descuentosub` | double | YES |  |
| 25 | `importevarbruto` | double | YES |  |
| 26 | `descuentovar` | double | YES |  |
| 27 | `importepintbruto` | double | YES |  |
| 28 | `descuentopint` | double | YES |  |
| 29 | `importematerialbruto` | double | YES |  |
| 30 | `descuentomaterial` | double | YES |  |
| 31 | `importemoaceptada` | double | YES |  |
| 32 | `importesubaceptada` | double | YES |  |
| 33 | `importevaraceptada` | double | YES |  |
| 34 | `importepintaceptada` | double | YES |  |
| 35 | `importematerialaceptada` | double | YES |  |
| 36 | `idcargotipos` | varchar | YES |  |
| 37 | `idmanoobratipos` | bigint | YES |  |
| 38 | `iddepartamentocargointerno` | varchar | YES |  |
| 39 | `idsecciones` | bigint | YES |  |
| 40 | `idvehiculos` | bigint | YES |  |
| 41 | `matricula` | varchar | YES |  |
| 42 | `vin` | varchar | YES |  |
| 43 | `idmarcas` | bigint | YES |  |
| 44 | `idgamas` | bigint | YES |  |
| 45 | `fechadespacho` | timestamp(3) | YES |  |
| 46 | `nombremarcas` | varchar | YES |  |
| 47 | `nombregamas` | varchar | YES |  |
| 48 | `a�ofactura` | varchar | YES |  |
| 49 | `seriefactura` | varchar | YES |  |
| 50 | `numfactura` | varchar | YES |  |
| 51 | `idtercerofactura` | bigint | YES |  |
| 52 | `nombretercero` | varchar | YES |  |
| 53 | `idterceroaux` | bigint | YES |  |
| 54 | `nombreterceroaux` | varchar | YES |  |
| 55 | `idpagoformatipos` | varchar | YES |  |
| 56 | `idpagoformas` | varchar | YES |  |
| 57 | `descripcionpagoformas` | varchar | YES |  |
| 58 | `descripcionpagoformatipos` | varchar | YES |  |
| 59 | `fechafactura` | timestamp(3) | YES |  |
| 60 | `tipopago` | varchar | YES |  |
| 61 | `costesub` | double | YES |  |
| 62 | `costemo` | double | YES |  |
| 63 | `costemochapa` | double | YES |  |
| 64 | `costemopintura` | double | YES |  |
| 65 | `costemoresto` | varchar | YES |  |
| 66 | `costemat` | double | YES |  |
| 67 | `importetasasmat` | double | YES |  |
| 68 | `diasreparacion` | bigint | YES |  |
| 69 | `costepint` | double | YES |  |
| 70 | `importemochapa` | double | YES |  |
| 71 | `importemopintura` | double | YES |  |
| 72 | `importemoresto` | varchar | YES |  |
| 73 | `idtallerpagotipos` | varchar | YES |  |
| 74 | `descripciontallerpagotipos` | varchar | YES |  |
| 75 | `idempleados` | bigint | YES |  |
| 76 | `descripcionrecepciontipos` | varchar | YES |  |
| 77 | `kmts` | bigint | YES |  |
| 78 | `a�omodelo` | varchar | YES |  |
| 79 | `idterceropropietario` | bigint | YES |  |
| 80 | `descripciontrabajo` | varchar | YES |  |
| 81 | `diasabierto` | double | YES |  |
| 82 | `numeroautorizacion` | varchar | YES |  |
| 83 | `numsiniestro` | varchar | YES |  |
| 84 | `fechaentrega` | timestamp(3) | YES |  |
| 85 | `idtercerocargo` | bigint | YES |  |
| 86 | `nombretercerocargo` | varchar | YES |  |
| 87 | `idseccioncargos` | varchar | YES |  |
| 88 | `idimputaciontipos` | bigint | YES |  |
| 89 | `idseccioncargointerno` | bigint | YES |  |
| 90 | `idcentrosdestino` | bigint | YES |  |
| 91 | `trabajorepetido` | bigint | YES |  |
| 92 | `a�opresupuesto` | varchar | YES |  |
| 93 | `seriepresupuesto` | varchar | YES |  |
| 94 | `idpresupuesto` | bigint | YES |  |
| 95 | `descripcionseccioncargos` | varchar | YES |  |
| 96 | `idempleadosrec` | bigint | YES |  |
| 97 | `idempleadosretirada` | bigint | YES |  |
| 98 | `idempleadosresponsable` | bigint | YES |  |
| 99 | `a�opedidosservicios` | varchar | YES |  |
| 100 | `seriepedidosservicios` | varchar | YES |  |
| 101 | `idpedidosservicios` | bigint | YES |  |
| 102 | `idmarcastallercampa�asbastidoresafectados` | bigint | YES |  |
| 103 | `idcampa�as` | varchar | YES |  |
| 104 | `idcampa�avariante` | varchar | YES |  |
| 105 | `idubicaciones` | varchar | YES |  |
| 106 | `reclamadomo` | double | YES |  |
| 107 | `reclamadomat` | double | YES |  |
| 108 | `reclamadosub` | double | YES |  |
| 109 | `reclamadovar` | double | YES |  |
| 110 | `reclamadopint` | double | YES |  |
| 111 | `idcentrosdeferencia` | bigint | YES |  |
| 112 | `ida�ootdeferencia` | varchar | YES |  |
| 113 | `idseriesdeferencia` | varchar | YES |  |
| 114 | `idnumotdeferencia` | bigint | YES |  |
| 115 | `idnumtrabajodeferencia` | bigint | YES |  |
| 116 | `idserviciotipos` | bigint | YES |  |
| 117 | `idgradosaveria` | bigint | YES |  |
| 118 | `idgradoaveriaordentrabajo` | bigint | YES |  |
| 119 | `idtrabajotipos` | varchar | YES |  |
| 120 | `idtrabajotiposmarca` | varchar | YES |  |
| 121 | `sureferencia` | varchar | YES |  |
| 122 | `horasuso` | bigint | YES |  |
| 123 | `fechaaltaot` | timestamp(3) | YES |  |
| 124 | `numfacturaexterna` | varchar | YES |  |
| 125 | `observaciones` | varchar | YES |  |
| 126 | `descripciondepartamentoimputaciontipos` | varchar | YES |  |
| 127 | `descripcionimputaciontipos` | varchar | YES |  |
| 128 | `descripcionseccionimputaciontipos` | varchar | YES |  |
| 129 | `nombrecentroimputaciontipos` | varchar | YES |  |
| 130 | `load_date` | varchar | YES |  |

### stage.spiga_inventariovn

**Columnas:** 71

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `comprasnumdet` | bigint | YES |  |
| 12 | `vin` | varchar | YES |  |
| 13 | `matricula` | varchar | YES |  |
| 14 | `comision` | varchar | YES |  |
| 15 | `idsecciones` | bigint | YES |  |
| 16 | `fkcompratipos` | varchar | YES |  |
| 17 | `nombreempresa` | varchar | YES |  |
| 18 | `nombrecentro` | varchar | YES |  |
| 19 | `descripcionseccion` | varchar | YES |  |
| 20 | `descripciontipocompra` | varchar | YES |  |
| 21 | `descripciontipocombustible` | varchar | YES |  |
| 22 | `idmarcas` | bigint | YES |  |
| 23 | `idgamas` | bigint | YES |  |
| 24 | `codmodelo` | varchar | YES |  |
| 25 | `extmodelo` | varchar | YES |  |
| 26 | `a�omodelo` | varchar | YES |  |
| 27 | `nombremarca` | varchar | YES |  |
| 28 | `nombregama` | varchar | YES |  |
| 29 | `nombremodelo` | varchar | YES |  |
| 30 | `a�ofactura` | varchar | YES |  |
| 31 | `seriefactura` | varchar | YES |  |
| 32 | `numfactura` | varchar | YES |  |
| 33 | `fechafactura` | timestamp(3) | YES |  |
| 34 | `idcompraestados` | varchar | YES |  |
| 35 | `a�oalbaran` | varchar | YES |  |
| 36 | `seriealbaran` | varchar | YES |  |
| 37 | `numalbaran` | varchar | YES |  |
| 38 | `fechaalbaran` | timestamp(3) | YES |  |
| 39 | `descripcionestadocompra` | varchar | YES |  |
| 40 | `color` | varchar | YES |  |
| 41 | `tapiceria` | varchar | YES |  |
| 42 | `ultimaubicacionvn` | varchar | YES |  |
| 43 | `ubicacionvnfechainventario` | varchar | YES |  |
| 44 | `baseimponiblecompra` | double | YES |  |
| 45 | `gastosaumentanstock` | double | YES |  |
| 46 | `gastosnoaumentanstock` | double | YES |  |
| 47 | `gastospendientesaumentanstock` | double | YES |  |
| 48 | `gastospendientesnoaumentanstock` | double | YES |  |
| 49 | `totalgastoscontravalor` | double | YES |  |
| 50 | `baseimponiblecompracontravalor` | double | YES |  |
| 51 | `descripcioncompraestados` | varchar | YES |  |
| 52 | `dtoimporte` | double | YES |  |
| 53 | `importereclamado` | double | YES |  |
| 54 | `pedidossinasignaraumentastock` | double | YES |  |
| 55 | `usodestino` | varchar | YES |  |
| 56 | `idversiones` | varchar | YES |  |
| 57 | `idincidenciatipos` | varchar | YES |  |
| 58 | `idtercerosactividadincidenciatipos` | bigint | YES |  |
| 59 | `idactividadincidenciatipos` | bigint | YES |  |
| 60 | `idactividadesdetincidenciatipos` | bigint | YES |  |
| 61 | `incidenciatiposdescripcion` | varchar | YES |  |
| 62 | `descripcionversion` | varchar | YES |  |
| 63 | `idcategoriagamatipos` | varchar | YES |  |
| 64 | `numeromotor` | varchar | YES |  |
| 65 | `numhomologacion` | varchar | YES |  |
| 66 | `fecha` | timestamp(3) | YES |  |
| 67 | `numdeclaracion` | varchar | YES |  |
| 68 | `fechalevante` | timestamp(3) | YES |  |
| 69 | `numlevante` | varchar | YES |  |
| 70 | `observaciones_compra` | varchar | YES |  |
| 71 | `load_date` | varchar | YES |  |

### stage.spiga_inventariovo

**Columnas:** 59

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `comprasnumdet` | bigint | YES |  |
| 12 | `fechadepreciar` | timestamp(3) | YES |  |
| 13 | `vin` | varchar | YES |  |
| 14 | `matricula` | varchar | YES |  |
| 15 | `idsecciones` | bigint | YES |  |
| 16 | `idcompratipos` | varchar | YES |  |
| 17 | `idregistrotipos` | varchar | YES |  |
| 18 | `fechaasiento` | timestamp(3) | YES |  |
| 19 | `idcomprainternatipos` | varchar | YES |  |
| 20 | `descripcioncomprainternatipo` | varchar | YES |  |
| 21 | `nombreempresa` | varchar | YES |  |
| 22 | `nombrecentro` | varchar | YES |  |
| 23 | `descripcionseccion` | varchar | YES |  |
| 24 | `descripciontipocompra` | varchar | YES |  |
| 25 | `descripciontipocombustible` | varchar | YES |  |
| 26 | `tipocomprainmovilizado` | varchar | YES |  |
| 27 | `idmarcas` | bigint | YES |  |
| 28 | `idgamas` | bigint | YES |  |
| 29 | `codmodelo` | varchar | YES |  |
| 30 | `extmodelo` | varchar | YES |  |
| 31 | `a�omodelo` | varchar | YES |  |
| 32 | `nombremarca` | varchar | YES |  |
| 33 | `nombregama` | varchar | YES |  |
| 34 | `idcompraestados` | varchar | YES |  |
| 35 | `nombremodelo` | varchar | YES |  |
| 36 | `a�ofactura` | varchar | YES |  |
| 37 | `seriefactura` | varchar | YES |  |
| 38 | `numfactura` | varchar | YES |  |
| 39 | `fechafactura` | timestamp(3) | YES |  |
| 40 | `descripcioncompraestados` | varchar | YES |  |
| 41 | `ultimaubicacionvn` | varchar | YES |  |
| 42 | `ubicacionvnfechainventario` | varchar | YES |  |
| 43 | `color` | varchar | YES |  |
| 44 | `tapiceria` | varchar | YES |  |
| 45 | `baseimponiblecompra` | double | YES |  |
| 46 | `depreciacioncompra` | double | YES |  |
| 47 | `compra576` | double | YES |  |
| 48 | `exentos` | double | YES |  |
| 49 | `gastosaumentanstock` | double | YES |  |
| 50 | `gastosnoaumentanstock` | double | YES |  |
| 51 | `gastospendientesaumentanstock` | double | YES |  |
| 52 | `gastospendientesnoaumentanstock` | double | YES |  |
| 53 | `totalgastoscontravalor` | double | YES |  |
| 54 | `importecompracontravalor` | double | YES |  |
| 55 | `pedidossinasignaraumentastock` | double | YES |  |
| 56 | `usodestino` | varchar | YES |  |
| 57 | `importetotaldepreciado` | double | YES |  |
| 58 | `observaciones_compra` | varchar | YES |  |
| 59 | `load_date` | varchar | YES |  |

### stage.spiga_ofertasdefinanciacionfechamod

**Columnas:** 52

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `ida�oofertasfinanciacion` | varchar | YES |  |
| 8 | `idseriesofertasfinanciacion` | varchar | YES |  |
| 9 | `idnumofertasfinanciacion` | bigint | YES |  |
| 10 | `idcentros` | bigint | YES |  |
| 11 | `nombreempresa` | varchar | YES |  |
| 12 | `nombrecentro` | varchar | YES |  |
| 13 | `nombremarca` | varchar | YES |  |
| 14 | `nombregama` | varchar | YES |  |
| 15 | `codmodelo` | varchar | YES |  |
| 16 | `nombremodelo` | varchar | YES |  |
| 17 | `idterceros` | bigint | YES |  |
| 18 | `nombretercero` | varchar | YES |  |
| 19 | `apellido1tercero` | varchar | YES |  |
| 20 | `apellido2tercero` | varchar | YES |  |
| 21 | `idofertasfinanciacionproductotiposdescripcion` | varchar | YES |  |
| 22 | `idofertasfinanciacionestadosdescripcion` | varchar | YES |  |
| 23 | `fechavalidez` | timestamp(3) | YES |  |
| 24 | `fechainiciofinanciacion` | timestamp(3) | YES |  |
| 25 | `fechafinfinanciacion` | timestamp(3) | YES |  |
| 26 | `importefinanciar` | double | YES |  |
| 27 | `cuotamensual` | double | YES |  |
| 28 | `meses` | bigint | YES |  |
| 29 | `porcsobreimportetotal` | double | YES |  |
| 30 | `capitalpreconcedido` | double | YES |  |
| 31 | `porcintereses` | double | YES |  |
| 32 | `importecomisionapertura` | double | YES |  |
| 33 | `porccomisionapertura` | double | YES |  |
| 34 | `obligaaval` | varchar | YES |  |
| 35 | `aval` | varchar | YES |  |
| 36 | `importecomisionobtencionfinanciacion` | double | YES |  |
| 37 | `porccomisionobtencionfinanciacion` | double | YES |  |
| 38 | `idtercerosfinanciera` | bigint | YES |  |
| 39 | `nombretercerofinanciera` | varchar | YES |  |
| 40 | `apellido1tercerofinanciera` | varchar | YES |  |
| 41 | `apellido2tercerofinanciera` | varchar | YES |  |
| 42 | `idofertasfinanciacionproductotipos` | bigint | YES |  |
| 43 | `idofertasfinanciacionestados` | bigint | YES |  |
| 44 | `fechaalta` | timestamp(3) | YES |  |
| 45 | `idofertasfinanciacionfinanciaciones` | bigint | YES |  |
| 46 | `idempleados` | bigint | YES |  |
| 47 | `nombreempleado` | varchar | YES |  |
| 48 | `apellido1empleado` | varchar | YES |  |
| 49 | `apellido2empleado` | varchar | YES |  |
| 50 | `importefranquicia` | double | YES |  |
| 51 | `fechamod` | timestamp(3) | YES |  |
| 52 | `load_date` | varchar | YES |  |

### stage.spiga_remisionesderepuestos

**Columnas:** 26

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `empresacentrosecciones` | varchar | YES |  |
| 8 | `idcentros` | bigint | YES |  |
| 9 | `centro` | varchar | YES |  |
| 10 | `idsecciones` | bigint | YES |  |
| 11 | `seccion` | varchar | YES |  |
| 12 | `fechaalta` | timestamp(3) | YES |  |
| 13 | `idmovimientotipos` | varchar | YES |  |
| 14 | `movimientotipos` | varchar | YES |  |
| 15 | `prefijo` | varchar | YES |  |
| 16 | `numero` | varchar | YES |  |
| 17 | `a�o` | varchar | YES |  |
| 18 | `a�oot` | varchar | YES |  |
| 19 | `serieot` | varchar | YES |  |
| 20 | `numot` | bigint | YES |  |
| 21 | `idpedidotipoventas` | bigint | YES |  |
| 22 | `a�opedido` | varchar | YES |  |
| 23 | `seriepedido` | varchar | YES |  |
| 24 | `pedido` | bigint | YES |  |
| 25 | `tipocargo` | varchar | YES |  |
| 26 | `load_date` | varchar | YES |  |

### stage.spiga_rentabilidaddetalladavehiculosnuevos

**Columnas:** 52

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | integer | YES |  |
| 2 | `idconsecutivo` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | smallint | YES |  |
| 7 | `a�oexpediente` | varchar | YES |  |
| 8 | `serieexpediente` | varchar | YES |  |
| 9 | `numexpediente` | integer | YES |  |
| 10 | `numventa` | smallint | YES |  |
| 11 | `idventasabonado` | smallint | YES |  |
| 12 | `nombrecentro` | varchar | YES |  |
| 13 | `seccion` | varchar | YES |  |
| 14 | `marca` | varchar | YES |  |
| 15 | `gama` | varchar | YES |  |
| 16 | `codmodelo` | varchar | YES |  |
| 17 | `modelo` | varchar | YES |  |
| 18 | `vin` | varchar | YES |  |
| 19 | `tipocompra` | varchar | YES |  |
| 20 | `idterceroscompra` | integer | YES |  |
| 21 | `nombretercerocompra` | varchar | YES |  |
| 22 | `apellido1tercerocompra` | varchar | YES |  |
| 23 | `apellido2tercerocompra` | varchar | YES |  |
| 24 | `fechafacturacompra` | timestamp(3) | YES |  |
| 25 | `seriefacturacompra` | varchar | YES |  |
| 26 | `numfacturacompra` | varchar | YES |  |
| 27 | `a�ofacturacompra` | varchar | YES |  |
| 28 | `diasstock` | integer | YES |  |
| 29 | `tipoventa` | varchar | YES |  |
| 30 | `fechaventa` | timestamp(3) | YES |  |
| 31 | `seriefacturaventa` | varchar | YES |  |
| 32 | `numfacturaventa` | varchar | YES |  |
| 33 | `a�ofacturaventa` | varchar | YES |  |
| 34 | `nombrevendedor` | varchar | YES |  |
| 35 | `apellido1vendedor` | varchar | YES |  |
| 36 | `apellido2vendedor` | varchar | YES |  |
| 37 | `importecompra` | decimal(38,14) | YES |  |
| 38 | `importegasto` | decimal(38,13) | YES |  |
| 39 | `idcompragastoadicionaltipos` | varchar | YES |  |
| 40 | `idcompragastoadicionaltiposdescripcion` | varchar | YES |  |
| 41 | `otroscargos` | decimal(38,19) | YES |  |
| 42 | `otrosingresos` | decimal(38,19) | YES |  |
| 43 | `importeventa` | decimal(38,6) | YES |  |
| 44 | `importeseguros` | decimal(38,14) | YES |  |
| 45 | `importegarantias` | decimal(38,14) | YES |  |
| 46 | `importematriculacion` | decimal(38,14) | YES |  |
| 47 | `importetransferencia` | decimal(38,14) | YES |  |
| 48 | `importecampa�as` | decimal(38,14) | YES |  |
| 49 | `importeprestamo` | decimal(38,4) | YES |  |
| 50 | `matricula` | varchar | YES |  |
| 51 | `fechaabono` | timestamp(3) | YES |  |
| 52 | `fechamatriculacion` | timestamp(3) | YES |  |

### stage.spiga_rentabilidaddetalladavehiculosusados

**Columnas:** 51

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | integer | YES |  |
| 2 | `idconsecutivo` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | smallint | YES |  |
| 7 | `serieexpediente` | varchar | YES |  |
| 8 | `numexpediente` | integer | YES |  |
| 9 | `a�oexpediente` | varchar | YES |  |
| 10 | `numventa` | smallint | YES |  |
| 11 | `idventasabonado` | smallint | YES |  |
| 12 | `nombrecentro` | varchar | YES |  |
| 13 | `seccion` | varchar | YES |  |
| 14 | `marca` | varchar | YES |  |
| 15 | `gama` | varchar | YES |  |
| 16 | `codmodelo` | varchar | YES |  |
| 17 | `modelo` | varchar | YES |  |
| 18 | `vin` | varchar | YES |  |
| 19 | `tipocompra` | varchar | YES |  |
| 20 | `idterceroscompra` | integer | YES |  |
| 21 | `nombretercerocompra` | varchar | YES |  |
| 22 | `apellido1tercerocompra` | varchar | YES |  |
| 23 | `apellido2tercerocompra` | varchar | YES |  |
| 24 | `fechafacturacompra` | timestamp(3) | YES |  |
| 25 | `seriefacturacompra` | varchar | YES |  |
| 26 | `numfacturacompra` | varchar | YES |  |
| 27 | `a�ofacturacompra` | varchar | YES |  |
| 28 | `diasstock` | integer | YES |  |
| 29 | `tipoventa` | varchar | YES |  |
| 30 | `fechaventa` | timestamp(3) | YES |  |
| 31 | `seriefacturaventa` | varchar | YES |  |
| 32 | `numfacturaventa` | varchar | YES |  |
| 33 | `a�ofacturaventa` | varchar | YES |  |
| 34 | `nombrevendedor` | varchar | YES |  |
| 35 | `apellido1vendedor` | varchar | YES |  |
| 36 | `apellido2vendedor` | varchar | YES |  |
| 37 | `importecompra` | decimal(38,14) | YES |  |
| 38 | `importegasto` | decimal(38,13) | YES |  |
| 39 | `idcompragastoadicionaltipos` | varchar | YES |  |
| 40 | `idcompragastoadicionaltiposdescripcion` | varchar | YES |  |
| 41 | `otroscargos` | decimal(38,19) | YES |  |
| 42 | `otrosingresos` | decimal(38,19) | YES |  |
| 43 | `importeventa` | decimal(29,4) | YES |  |
| 44 | `importeseguros` | decimal(18,4) | YES |  |
| 45 | `importegarantias` | decimal(18,4) | YES |  |
| 46 | `importematriculacion` | decimal(18,4) | YES |  |
| 47 | `importetransferencia` | decimal(18,4) | YES |  |
| 48 | `importeprestamo` | decimal(38,4) | YES |  |
| 49 | `matricula` | varchar | YES |  |
| 50 | `fechaabono` | timestamp(3) | YES |  |
| 51 | `importeprovisionadogarantias` | decimal(18,4) | YES |  |

### stage.spiga_stockrepuestos

**Columnas:** 61

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `idsecciones` | bigint | YES |  |
| 9 | `idmr` | varchar | YES |  |
| 10 | `idreferencias` | varchar | YES |  |
| 11 | `idtarifas` | bigint | YES |  |
| 12 | `stockmax` | double | YES |  |
| 13 | `preciomedio` | double | YES |  |
| 14 | `clasificacionabc` | varchar | YES |  |
| 15 | `stock` | double | YES |  |
| 16 | `numubicaciones` | bigint | YES |  |
| 17 | `ventasmesactualsalidas` | bigint | YES |  |
| 18 | `undpterecibir` | double | YES |  |
| 19 | `idubicaciones` | varchar | YES |  |
| 20 | `ventasmesactual` | double | YES |  |
| 21 | `ventasmes1` | double | YES |  |
| 22 | `ventasmes2` | double | YES |  |
| 23 | `ventasmes3` | double | YES |  |
| 24 | `ventasmes4` | double | YES |  |
| 25 | `ventasmes5` | double | YES |  |
| 26 | `ventasmes6` | double | YES |  |
| 27 | `ventasmes7` | double | YES |  |
| 28 | `ventasmes8` | double | YES |  |
| 29 | `ventasmes9` | double | YES |  |
| 30 | `ventasmes10` | double | YES |  |
| 31 | `ventasmes11` | double | YES |  |
| 32 | `ventasmes12` | double | YES |  |
| 33 | `descripcion` | varchar | YES |  |
| 34 | `precioventa` | double | YES |  |
| 35 | `observaciones` | varchar | YES |  |
| 36 | `idclasificacion1` | varchar | YES |  |
| 37 | `idclasificacion2` | varchar | YES |  |
| 38 | `idclasificacion3` | varchar | YES |  |
| 39 | `idclasificacion4` | varchar | YES |  |
| 40 | `idclasificacion5` | varchar | YES |  |
| 41 | `idclasificacion6` | varchar | YES |  |
| 42 | `iddescuentos` | varchar | YES |  |
| 43 | `fechaultimaventa` | timestamp(3) | YES |  |
| 44 | `fechaultimacompra` | timestamp(3) | YES |  |
| 45 | `fechaultimaregularizacion` | timestamp(3) | YES |  |
| 46 | `fechatraspasotre` | timestamp(3) | YES |  |
| 47 | `fechatraspasotrs` | timestamp(3) | YES |  |
| 48 | `denominacionclasificacion1` | varchar | YES |  |
| 49 | `denominacionclasificacion2` | varchar | YES |  |
| 50 | `denominacionclasificacion3` | varchar | YES |  |
| 51 | `denominacionclasificacion4` | varchar | YES |  |
| 52 | `denominacionclasificacion5` | varchar | YES |  |
| 53 | `denominacionclasificacion6` | varchar | YES |  |
| 54 | `fechaalta` | timestamp(3) | YES |  |
| 55 | `fechabaja` | timestamp(3) | YES |  |
| 56 | `stockmin` | double | YES |  |
| 57 | `undpteentregar` | double | YES |  |
| 58 | `undreservadaspteentregar` | double | YES |  |
| 59 | `undenvasecompra` | double | YES |  |
| 60 | `undenvaseventa` | double | YES |  |
| 61 | `load_date` | varchar | YES |  |

### stage.spiga_terceroformacionniveles

**Columnas:** 9

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `pkterceroformacionniveles_iden` | bigint | YES |  |
| 4 | `descripcion` | varchar | YES |  |
| 5 | `usermod` | bigint | YES |  |
| 6 | `hostmod` | varchar | YES |  |
| 7 | `versionfila` | bigint | YES |  |
| 8 | `fechamod` | timestamp(3) | YES |  |
| 9 | `load_date` | varchar | YES |  |

### stage.spiga_terceroformacionniveles_39bcb677f2ddb2ad2fd5a425951b5ed5

**Columnas:** 8

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | integer | YES |  |
| 2 | `idconsecutivo` | integer | YES |  |
| 3 | `pkterceroformacionniveles_iden` | integer | YES |  |
| 4 | `descripcion` | varchar | YES |  |
| 5 | `usermod` | smallint | YES |  |
| 6 | `hostmod` | varchar | YES |  |
| 7 | `versionfila` | integer | YES |  |
| 8 | `fechamod` | timestamp(3) | YES |  |

### stage.spiga_terceros

**Columnas:** 71

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `pkterceros` | bigint | YES |  |
| 7 | `fkpaises` | varchar | YES |  |
| 8 | `fkterceroclases` | bigint | YES |  |
| 9 | `fktratamientos` | bigint | YES |  |
| 10 | `nifcif` | varchar | YES |  |
| 11 | `nombre` | varchar | YES |  |
| 12 | `apellido1` | varchar | YES |  |
| 13 | `apellido2` | varchar | YES |  |
| 14 | `nombrecomercial` | varchar | YES |  |
| 15 | `empresatrabajo` | varchar | YES |  |
| 16 | `fkprofesiones` | bigint | YES |  |
| 17 | `fktercerocargos` | bigint | YES |  |
| 18 | `fkterceroformacionniveles` | bigint | YES |  |
| 19 | `fechanacimiento` | timestamp(3) | YES |  |
| 20 | `fechasanto` | varchar | YES |  |
| 21 | `fechacarnet` | timestamp(3) | YES |  |
| 22 | `numerohijos` | bigint | YES |  |
| 23 | `facturaracliente` | bigint | YES |  |
| 24 | `numeroautorizacion` | bigint | YES |  |
| 25 | `numerosiniestro` | bigint | YES |  |
| 26 | `fechaalta` | timestamp(3) | YES |  |
| 27 | `fechabaja` | timestamp(3) | YES |  |
| 28 | `usermod` | bigint | YES |  |
| 29 | `hostmod` | varchar | YES |  |
| 30 | `versionfila` | bigint | YES |  |
| 31 | `fkdocumentaciontipos` | bigint | YES |  |
| 32 | `fkestadociviltipos` | varchar | YES |  |
| 33 | `fechamod` | timestamp(3) | YES |  |
| 34 | `sexo` | varchar | YES |  |
| 35 | `fknaturalezajuridicatipos` | varchar | YES |  |
| 36 | `numeroempleados` | bigint | YES |  |
| 37 | `a�oconstitucion` | varchar | YES |  |
| 38 | `cifradenegocio` | bigint | YES |  |
| 39 | `fkactividadtipos` | varchar | YES |  |
| 40 | `solvencia` | bigint | YES |  |
| 41 | `codigosociedad` | varchar | YES |  |
| 42 | `robinson` | bigint | YES |  |
| 43 | `numlicenciaconducir` | varchar | YES |  |
| 44 | `billeteidentidad` | varchar | YES |  |
| 45 | `tipocontribuyente` | varchar | YES |  |
| 46 | `retenerdesdecero` | bigint | YES |  |
| 47 | `agenteretenedor` | bigint | YES |  |
| 48 | `robinsonant` | bigint | YES |  |
| 49 | `fechamodrobinson` | timestamp(3) | YES |  |
| 50 | `fkcausabajatercero` | bigint | YES |  |
| 51 | `notieneemail` | bigint | YES |  |
| 52 | `centrocoste` | varchar | YES |  |
| 53 | `fechacarnetcaducidad` | timestamp(3) | YES |  |
| 54 | `norealizaasientodiferenciacambial` | bigint | YES |  |
| 55 | `norealizaasientoconversion` | bigint | YES |  |
| 56 | `fknivelesriesgo` | bigint | YES |  |
| 57 | `fechatipocontribuyente` | timestamp(3) | YES |  |
| 58 | `resolucion` | varchar | YES |  |
| 59 | `cuentabanconacion` | varchar | YES |  |
| 60 | `admitesepab2b` | bigint | YES |  |
| 61 | `requieresureferenciare` | bigint | YES |  |
| 62 | `nifcif_fechaexpedicion` | timestamp(3) | YES |  |
| 63 | `nifcif_lugarexpedicion` | varchar | YES |  |
| 64 | `nifcif_fechacaducidad` | timestamp(3) | YES |  |
| 65 | `licenciaconducir_lugarexpedicion` | varchar | YES |  |
| 66 | `fkdeudortipos` | varchar | YES |  |
| 67 | `fkpaises_documentaciontipos` | varchar | YES |  |
| 68 | `fcnegociado` | bigint | YES |  |
| 69 | `web` | varchar | YES |  |
| 70 | `envioficherosfecomprimidos` | bigint | YES |  |
| 71 | `load_date` | varchar | YES |  |

### stage.spiga_terceroscargos

**Columnas:** 10

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `pktercerocargos_iden` | bigint | YES |  |
| 4 | `descripcion` | varchar | YES |  |
| 5 | `fechabaja` | timestamp(3) | YES |  |
| 6 | `usermod` | bigint | YES |  |
| 7 | `hostmod` | varchar | YES |  |
| 8 | `versionfila` | bigint | YES |  |
| 9 | `fechamod` | timestamp(3) | YES |  |
| 10 | `load_date` | varchar | YES |  |

### stage.spiga_terceroscorreos

**Columnas:** 19

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `pkfkterceros` | bigint | YES |  |
| 7 | `pkterceroemails_iden` | bigint | YES |  |
| 8 | `fkemailtipos` | bigint | YES |  |
| 9 | `email` | varchar | YES |  |
| 10 | `fktercerodirecciones` | bigint | YES |  |
| 11 | `fechabaja` | timestamp(3) | YES |  |
| 12 | `usermod` | bigint | YES |  |
| 13 | `hostmod` | varchar | YES |  |
| 14 | `versionfila` | bigint | YES |  |
| 15 | `direccionpadre` | bigint | YES |  |
| 16 | `principal` | bigint | YES |  |
| 17 | `fechamod` | timestamp(3) | YES |  |
| 18 | `fkterceros_direcciones` | bigint | YES |  |
| 19 | `load_date` | varchar | YES |  |

### stage.spiga_tercerosdirecciones

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `pkfkterceros` | bigint | YES |  |
| 7 | `pktercerodirecciones_iden` | bigint | YES |  |
| 8 | `fkdirecciontipos` | bigint | YES |  |
| 9 | `fkcalletipos` | varchar | YES |  |
| 10 | `nombrecalle` | varchar | YES |  |
| 11 | `numero` | varchar | YES |  |
| 12 | `bloque` | varchar | YES |  |
| 13 | `piso` | varchar | YES |  |
| 14 | `puerta` | varchar | YES |  |
| 15 | `complemento` | varchar | YES |  |
| 16 | `fkpaises` | varchar | YES |  |
| 17 | `fkcodigospostales` | varchar | YES |  |
| 18 | `poblacion` | varchar | YES |  |
| 19 | `provincia` | varchar | YES |  |
| 20 | `fechabaja` | timestamp(3) | YES |  |
| 21 | `usermod` | bigint | YES |  |
| 22 | `hostmod` | varchar | YES |  |
| 23 | `versionfila` | bigint | YES |  |
| 24 | `principal` | bigint | YES |  |
| 25 | `fkestados` | varchar | YES |  |
| 26 | `fkprovincias` | varchar | YES |  |
| 27 | `complemento2` | varchar | YES |  |
| 28 | `fechamod` | timestamp(3) | YES |  |
| 29 | `fkpoblaciones` | bigint | YES |  |
| 30 | `load_date` | varchar | YES |  |

### stage.spiga_tercerostelefonos

**Columnas:** 23

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `pkfkterceros` | bigint | YES |  |
| 7 | `pktercerotelefonos_iden` | bigint | YES |  |
| 8 | `fktelefonotipos` | bigint | YES |  |
| 9 | `codigotelefonico` | varchar | YES |  |
| 10 | `numero` | varchar | YES |  |
| 11 | `extension` | varchar | YES |  |
| 12 | `fktercerodirecciones` | bigint | YES |  |
| 13 | `direccionpadre` | bigint | YES |  |
| 14 | `horario` | varchar | YES |  |
| 15 | `fechabaja` | timestamp(3) | YES |  |
| 16 | `usermod` | bigint | YES |  |
| 17 | `hostmod` | varchar | YES |  |
| 18 | `versionfila` | bigint | YES |  |
| 19 | `principal` | bigint | YES |  |
| 20 | `fechamod` | timestamp(3) | YES |  |
| 21 | `fkterceros_direcciones` | bigint | YES |  |
| 22 | `fkpaises` | varchar | YES |  |
| 23 | `load_date` | varchar | YES |  |

### stage.spiga_tercerotercerotipos

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | integer | YES |  |
| 2 | `idconsecutivo` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `pkfkempresas` | integer | YES |  |
| 7 | `pkfkcentros` | integer | YES |  |
| 8 | `pkfkterceros` | bigint | YES |  |
| 9 | `pkfktercerotipos` | varchar | YES |  |
| 10 | `usermod` | bigint | YES |  |
| 11 | `fechaalta` | timestamp(3) | YES |  |
| 12 | `fechamod` | timestamp(3) | YES |  |

### stage.spiga_tiempostallerpicajesots

**Columnas:** 32

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `idempleados` | bigint | YES |  |
| 9 | `fechainicio` | timestamp(3) | YES |  |
| 10 | `fechafin` | timestamp(3) | YES |  |
| 11 | `idpicajetrabajotipos` | varchar | YES |  |
| 12 | `matricula` | varchar | YES |  |
| 13 | `serieot` | varchar | YES |  |
| 14 | `numot` | bigint | YES |  |
| 15 | `a�oot` | varchar | YES |  |
| 16 | `numtrabajo` | bigint | YES |  |
| 17 | `tiempoempleado` | double | YES |  |
| 18 | `fechainicioaux` | timestamp(3) | YES |  |
| 19 | `fechafinaux` | timestamp(3) | YES |  |
| 20 | `tiempoaux` | double | YES |  |
| 21 | `nombreempleado` | varchar | YES |  |
| 22 | `descripcionpicajetrabajotipos` | varchar | YES |  |
| 23 | `idmanoobratipos` | bigint | YES |  |
| 24 | `descripcionmanoobratipos` | varchar | YES |  |
| 25 | `recuperable` | varchar | YES |  |
| 26 | `afectataller` | varchar | YES |  |
| 27 | `idclasificacionincidenciatipos` | bigint | YES |  |
| 28 | `idrevisionpicajetipos` | varchar | YES |  |
| 29 | `useraux` | bigint | YES |  |
| 30 | `idsecciones` | bigint | YES |  |
| 31 | `fechabaja` | timestamp(3) | YES |  |
| 32 | `load_date` | varchar | YES |  |

### stage.spiga_tipoclasificacionesvehiculos

**Columnas:** 68

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `pkfkmarcas` | bigint | YES |  |
| 4 | `pkfkgamas` | bigint | YES |  |
| 5 | `pkcodmodelo` | varchar | YES |  |
| 6 | `pkanomodelo` | varchar | YES |  |
| 7 | `fkclasificaciontipos` | varchar | YES |  |
| 8 | `nombreclasificacion` | varchar | YES |  |
| 9 | `cantidadpasajeros` | varchar | YES |  |
| 10 | `capacidaddecarga` | varchar | YES |  |
| 11 | `pkextmodelo` | varchar | YES |  |
| 12 | `nombre` | varchar | YES |  |
| 13 | `activo` | varchar | YES |  |
| 14 | `fkcombustibletipos` | varchar | YES |  |
| 15 | `fkcarroceriatipos` | varchar | YES |  |
| 16 | `fkmarcatallermodelos` | varchar | YES |  |
| 17 | `fktracciontipos` | varchar | YES |  |
| 18 | `fkcambiotipos` | varchar | YES |  |
| 19 | `potenciafiscal` | varchar | YES |  |
| 20 | `potenciareal` | varchar | YES |  |
| 21 | `cilindrada` | double | YES |  |
| 22 | `aceleracion` | varchar | YES |  |
| 23 | `velocidadmax` | double | YES |  |
| 24 | `numerocilindros` | bigint | YES |  |
| 25 | `consumointerurbano` | double | YES |  |
| 26 | `consumourbano` | double | YES |  |
| 27 | `consumomedio` | double | YES |  |
| 28 | `emisionesco2medio` | double | YES |  |
| 29 | `importado` | varchar | YES |  |
| 30 | `visibleweb` | varchar | YES |  |
| 31 | `periodoinspeccion` | bigint | YES |  |
| 32 | `kilometrosinspeccion` | varchar | YES |  |
| 33 | `fechabaja` | timestamp(3) | YES |  |
| 34 | `codexternomodelo` | varchar | YES |  |
| 35 | `potenciarealkw` | varchar | YES |  |
| 36 | `propiopeso` | varchar | YES |  |
| 37 | `cargautil` | varchar | YES |  |
| 38 | `numeropuertas` | varchar | YES |  |
| 39 | `numeroplazas` | varchar | YES |  |
| 40 | `fkcajavelocidadtipos` | varchar | YES |  |
| 41 | `neumaticos` | varchar | YES |  |
| 42 | `pma` | varchar | YES |  |
| 43 | `fechamod` | timestamp(3) | YES |  |
| 44 | `longitudexterior` | bigint | YES |  |
| 45 | `anchoexterior` | bigint | YES |  |
| 46 | `altoexterior` | bigint | YES |  |
| 47 | `disposicioncilindros` | varchar | YES |  |
| 48 | `volantealaizquierda` | varchar | YES |  |
| 49 | `fkmonedas` | bigint | YES |  |
| 50 | `factorcambiomoneda` | double | YES |  |
| 51 | `numeroejes` | bigint | YES |  |
| 52 | `fkcategoriagamatipos` | varchar | YES |  |
| 53 | `detalleenfactura` | varchar | YES |  |
| 54 | `porcdtomaxvendedores` | double | YES |  |
| 55 | `kilometrosgarantia` | bigint | YES |  |
| 56 | `numeroruedas` | bigint | YES |  |
| 57 | `numerovelocidades` | bigint | YES |  |
| 58 | `codigohomologacion` | varchar | YES |  |
| 59 | `numeroasientos` | varchar | YES |  |
| 60 | `requierecertificacion` | varchar | YES |  |
| 61 | `horasusoinspeccion` | varchar | YES |  |
| 62 | `potenciapto` | varchar | YES |  |
| 63 | `neumaticosdelanteros` | varchar | YES |  |
| 64 | `neumaticostraseros` | varchar | YES |  |
| 65 | `numcertificadopruebadinamica` | varchar | YES |  |
| 66 | `porcdtomaxjefesventas` | double | YES |  |
| 67 | `fkpaises` | varchar | YES |  |
| 68 | `load_date` | varchar | YES |  |

### stage.spiga_tipodeventasvehiculos

**Columnas:** 27

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | integer | YES |  |
| 2 | `idconsecutivo` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | smallint | YES |  |
| 7 | `empresa` | varchar | YES |  |
| 8 | `idcentros` | smallint | YES |  |
| 9 | `centro` | varchar | YES |  |
| 10 | `expediente` | varchar | YES |  |
| 11 | `factura` | varchar | YES |  |
| 12 | `vin` | varchar | YES |  |
| 13 | `placa` | varchar | YES |  |
| 14 | `fechamatriculacion` | timestamp(3) | YES |  |
| 15 | `sitioplaca` | varchar | YES |  |
| 16 | `perfilcliente` | varchar | YES |  |
| 17 | `tiponegocio` | varchar | YES |  |
| 18 | `nombretercero` | varchar | YES |  |
| 19 | `tipoentrada` | varchar | YES |  |
| 20 | `tipoventa` | varchar | YES |  |
| 21 | `tipocompra` | varchar | YES |  |
| 22 | `tipoventamarca` | varchar | YES |  |
| 23 | `tipofinanciacion` | varchar | YES |  |
| 24 | `numerocotizacion` | varchar | YES |  |
| 25 | `fechapazysalvo` | timestamp(3) | YES |  |
| 26 | `numpazysalvo` | integer | YES |  |
| 27 | `estado` | varchar | YES |  |

### stage.spiga_trasladosderepuestospendientes

**Columnas:** 29

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas_salida` | bigint | YES |  |
| 7 | `idcentros_salida` | bigint | YES |  |
| 8 | `a�otraspaso_salida` | varchar | YES |  |
| 9 | `serietraspaso_salida` | varchar | YES |  |
| 10 | `numtraspaso_salida` | bigint | YES |  |
| 11 | `numdettraspaso_salida` | bigint | YES |  |
| 12 | `idsecciones_salida` | bigint | YES |  |
| 13 | `idempresas_entrada` | bigint | YES |  |
| 14 | `idcentros_entrada` | bigint | YES |  |
| 15 | `a�otraspaso_entrada` | varchar | YES |  |
| 16 | `serietraspaso_entrada` | varchar | YES |  |
| 17 | `numtraspaso_entrada` | bigint | YES |  |
| 18 | `numdettraspaso_entrada` | bigint | YES |  |
| 19 | `idsecciones_entrada` | bigint | YES |  |
| 20 | `idmovimientotipos` | varchar | YES |  |
| 21 | `mr` | varchar | YES |  |
| 22 | `referencia` | varchar | YES |  |
| 23 | `valorbruto` | double | YES |  |
| 24 | `unidades` | double | YES |  |
| 25 | `valorneto` | double | YES |  |
| 26 | `valormediomovimiento` | double | YES |  |
| 27 | `fechaaltasalida` | timestamp(3) | YES |  |
| 28 | `fechaaltaentrada` | timestamp(3) | YES |  |
| 29 | `load_date` | varchar | YES |  |

### stage.spiga_vehiculos

**Columnas:** 60

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `fechadeactualizacion` | timestamp(3) | YES |  |
| 7 | `placa` | varchar | YES |  |
| 8 | `vin` | varchar | YES |  |
| 9 | `numdocumentopropietario` | varchar | YES |  |
| 10 | `numdocumentoconductor` | varchar | YES |  |
| 11 | `numdocumentoleasingrenting` | varchar | YES |  |
| 12 | `numdocumentoarrendador` | varchar | YES |  |
| 13 | `codigomarca` | bigint | YES |  |
| 14 | `nombremarca` | varchar | YES |  |
| 15 | `codigogama` | bigint | YES |  |
| 16 | `nombregama` | varchar | YES |  |
| 17 | `codmodelo` | varchar | YES |  |
| 18 | `nombremodelo` | varchar | YES |  |
| 19 | `extmodelo` | varchar | YES |  |
| 20 | `a�omodelo` | varchar | YES |  |
| 21 | `version` | varchar | YES |  |
| 22 | `codmodeloexterno` | varchar | YES |  |
| 23 | `potencia` | varchar | YES |  |
| 24 | `torque` | varchar | YES |  |
| 25 | `cilindrada` | double | YES |  |
| 26 | `combustible` | varchar | YES |  |
| 27 | `carroceria` | varchar | YES |  |
| 28 | `modelotaller` | varchar | YES |  |
| 29 | `color` | varchar | YES |  |
| 30 | `tapizado` | varchar | YES |  |
| 31 | `numeromotor` | varchar | YES |  |
| 32 | `codigofabricacion` | varchar | YES |  |
| 33 | `opr` | varchar | YES |  |
| 34 | `modelopv` | varchar | YES |  |
| 35 | `numregistroimportacion` | varchar | YES |  |
| 36 | `numeroprefijo` | varchar | YES |  |
| 37 | `sitioplaca` | varchar | YES |  |
| 38 | `servicio` | varchar | YES |  |
| 39 | `paisorigen` | varchar | YES |  |
| 40 | `fechafingarantiamecanica` | timestamp(3) | YES |  |
| 41 | `fechafingarantialatoneria` | timestamp(3) | YES |  |
| 42 | `fechafingarantiapintura` | timestamp(3) | YES |  |
| 43 | `fechafingarantiamotor` | timestamp(3) | YES |  |
| 44 | `kilometrosfingarantia` | bigint | YES |  |
| 45 | `fechaultimainspeccion` | timestamp(3) | YES |  |
| 46 | `fechaproximainspeccion` | timestamp(3) | YES |  |
| 47 | `kilometrosinspeccion` | varchar | YES |  |
| 48 | `kmsactuales` | bigint | YES |  |
| 49 | `tiposeguro` | varchar | YES |  |
| 50 | `ciaseguros` | varchar | YES |  |
| 51 | `fechaalta` | timestamp(3) | YES |  |
| 52 | `fechavencimiento` | timestamp(3) | YES |  |
| 53 | `valor` | double | YES |  |
| 54 | `deducible` | double | YES |  |
| 55 | `importecomisionventa` | double | YES |  |
| 56 | `numeropoliza` | varchar | YES |  |
| 57 | `tomador` | varchar | YES |  |
| 58 | `gestornegocio` | varchar | YES |  |
| 59 | `idvehiculos` | bigint | YES |  |
| 60 | `load_date` | varchar | YES |  |

### stage.spiga_vehiculosentregados

**Columnas:** 33

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | integer | YES |  |
| 2 | `idconsecutivo` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | smallint | YES |  |
| 7 | `a�o` | integer | YES |  |
| 8 | `mes` | integer | YES |  |
| 9 | `codigoempresa` | smallint | YES |  |
| 10 | `empresa` | varchar | YES |  |
| 11 | `codigocentro` | smallint | YES |  |
| 12 | `centro` | varchar | YES |  |
| 13 | `codigoseccion` | integer | YES |  |
| 14 | `seccion` | varchar | YES |  |
| 15 | `codigomarca` | smallint | YES |  |
| 16 | `marca` | varchar | YES |  |
| 17 | `codigogama` | smallint | YES |  |
| 18 | `gama` | varchar | YES |  |
| 19 | `codigomodelo` | varchar | YES |  |
| 20 | `a�omodelo` | varchar | YES |  |
| 21 | `modelo` | varchar | YES |  |
| 22 | `cedulavendedor` | varchar | YES |  |
| 23 | `nombrevendedor` | varchar | YES |  |
| 24 | `nit` | varchar | YES |  |
| 25 | `nombretercero` | varchar | YES |  |
| 26 | `cantidad` | integer | YES |  |
| 27 | `valor` | decimal(18,2) | YES |  |
| 28 | `tipo` | varchar | YES |  |
| 29 | `fechaentregacliente` | timestamp(3) | YES |  |
| 30 | `fechamod` | timestamp(3) | YES |  |
| 31 | `vin` | varchar | YES |  |
| 32 | `fechafactura` | timestamp(3) | YES |  |
| 33 | `fkterceros_alquilador` | integer | YES |  |

### stage.spiga_vehiculosentregados_f3121bc8d9f60794fc5fa4f0872c73db

**Columnas:** 34

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `a�o` | bigint | YES |  |
| 8 | `mes` | bigint | YES |  |
| 9 | `codigoempresa` | bigint | YES |  |
| 10 | `empresa` | varchar | YES |  |
| 11 | `codigocentro` | bigint | YES |  |
| 12 | `centro` | varchar | YES |  |
| 13 | `codigoseccion` | bigint | YES |  |
| 14 | `seccion` | varchar | YES |  |
| 15 | `codigomarca` | bigint | YES |  |
| 16 | `marca` | varchar | YES |  |
| 17 | `codigogama` | bigint | YES |  |
| 18 | `gama` | varchar | YES |  |
| 19 | `codigomodelo` | varchar | YES |  |
| 20 | `a�omodelo` | varchar | YES |  |
| 21 | `modelo` | varchar | YES |  |
| 22 | `cedulavendedor` | varchar | YES |  |
| 23 | `nombrevendedor` | varchar | YES |  |
| 24 | `nit` | varchar | YES |  |
| 25 | `nombretercero` | varchar | YES |  |
| 26 | `cantidad` | bigint | YES |  |
| 27 | `valor` | double | YES |  |
| 28 | `tipo` | varchar | YES |  |
| 29 | `fechaentregacliente` | timestamp(3) | YES |  |
| 30 | `fechamod` | timestamp(3) | YES |  |
| 31 | `vin` | varchar | YES |  |
| 32 | `fechafactura` | timestamp(3) | YES |  |
| 33 | `fkterceros_alquilador` | varchar | YES |  |
| 34 | `load_date` | varchar | YES |  |

### stage.spiga_vehiculosseguros

**Columnas:** 87

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idvehiculos` | bigint | YES |  |
| 7 | `idvehiculoseguros` | bigint | YES |  |
| 8 | `idsegurotipos` | varchar | YES |  |
| 9 | `descripcionsegurotipos` | varchar | YES |  |
| 10 | `fechaalta` | timestamp(3) | YES |  |
| 11 | `idterceros` | bigint | YES |  |
| 12 | `fechavencimiento` | timestamp(3) | YES |  |
| 13 | `importe` | double | YES |  |
| 14 | `importefranquicia` | double | YES |  |
| 15 | `fechabaja` | timestamp(3) | YES |  |
| 16 | `idempresasvo` | bigint | YES |  |
| 17 | `idcentrosvo` | bigint | YES |  |
| 18 | `a�oexpedientevo` | varchar | YES |  |
| 19 | `serieexpedientevo` | varchar | YES |  |
| 20 | `numexpedientevo` | bigint | YES |  |
| 21 | `idventas_vo` | bigint | YES |  |
| 22 | `idempresasvn` | bigint | YES |  |
| 23 | `idcentrosvn` | bigint | YES |  |
| 24 | `a�oexpedientevn` | varchar | YES |  |
| 25 | `serieexpedientevn` | varchar | YES |  |
| 26 | `numexpedientevn` | bigint | YES |  |
| 27 | `numventa_vn` | bigint | YES |  |
| 28 | `usermod` | bigint | YES |  |
| 29 | `hostmod` | varchar | YES |  |
| 30 | `versionfila` | bigint | YES |  |
| 31 | `idvehiculoseguros_abonado` | bigint | YES |  |
| 32 | `numeropoliza` | varchar | YES |  |
| 33 | `idpaises` | varchar | YES |  |
| 34 | `idcodigospostales` | varchar | YES |  |
| 35 | `matricula` | varchar | YES |  |
| 36 | `idmarcas` | bigint | YES |  |
| 37 | `nombremarca` | varchar | YES |  |
| 38 | `idgamas` | bigint | YES |  |
| 39 | `nombregama` | varchar | YES |  |
| 40 | `codmodelo` | varchar | YES |  |
| 41 | `extmodelo` | varchar | YES |  |
| 42 | `a�omodelo` | varchar | YES |  |
| 43 | `nombremodelo` | varchar | YES |  |
| 44 | `idversiones` | varchar | YES |  |
| 45 | `descripcionversion` | varchar | YES |  |
| 46 | `idterceros_propietario` | bigint | YES |  |
| 47 | `nifcif` | varchar | YES |  |
| 48 | `nombre` | varchar | YES |  |
| 49 | `apellido1` | varchar | YES |  |
| 50 | `apellido2` | varchar | YES |  |
| 51 | `fechanacimiento` | timestamp(3) | YES |  |
| 52 | `fechacarnet` | timestamp(3) | YES |  |
| 53 | `idtercerodirecciones` | bigint | YES |  |
| 54 | `iddireccionclases` | bigint | YES |  |
| 55 | `idcalletipos` | varchar | YES |  |
| 56 | `nombrecalle` | varchar | YES |  |
| 57 | `numero` | varchar | YES |  |
| 58 | `bloque` | varchar | YES |  |
| 59 | `piso` | varchar | YES |  |
| 60 | `puerta` | varchar | YES |  |
| 61 | `complemento` | varchar | YES |  |
| 62 | `idpaisesdirecciones` | varchar | YES |  |
| 63 | `idcodigospostalesdirecciones` | varchar | YES |  |
| 64 | `poblacion` | varchar | YES |  |
| 65 | `provincia` | varchar | YES |  |
| 66 | `fechabajadirecciones` | timestamp(3) | YES |  |
| 67 | `idestados` | varchar | YES |  |
| 68 | `idprovincias` | varchar | YES |  |
| 69 | `complemento2` | varchar | YES |  |
| 70 | `telefonos` | varchar | YES |  |
| 71 | `nombreseguro` | varchar | YES |  |
| 72 | `nombreempleado` | varchar | YES |  |
| 73 | `apellido1empleado` | varchar | YES |  |
| 74 | `apellido2empleado` | varchar | YES |  |
| 75 | `descripciontipocalle` | varchar | YES |  |
| 76 | `tomador` | varchar | YES |  |
| 77 | `fechacarnetcaducidad` | timestamp(3) | YES |  |
| 78 | `observaciones` | varchar | YES |  |
| 79 | `idmonedas` | bigint | YES |  |
| 80 | `factorcambiomoneda` | double | YES |  |
| 81 | `importecomisionventa` | double | YES |  |
| 82 | `vin` | varchar | YES |  |
| 83 | `nombrecentrovn` | varchar | YES |  |
| 84 | `nombrecentrovo` | varchar | YES |  |
| 85 | `nombrecentrocomprasvn` | varchar | YES |  |
| 86 | `nombrecentrocomprasvo` | varchar | YES |  |
| 87 | `load_date` | varchar | YES |  |

### stage.spigafichallamadaagendamientodatostercerofechaalta

**Columnas:** 18

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | integer | YES |  |
| 2 | `idconsecutivo` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `pkterceros` | integer | YES |  |
| 6 | `nombre` | varchar | YES |  |
| 7 | `apellido1` | varchar | YES |  |
| 8 | `apellido2` | varchar | YES |  |
| 9 | `celular` | varchar | YES |  |
| 10 | `fijo` | varchar | YES |  |
| 11 | `direccion` | varchar | YES |  |
| 12 | `poblacion` | varchar | YES |  |
| 13 | `tipodocumento` | varchar | YES |  |
| 14 | `nifcif` | varchar | YES |  |
| 15 | `email` | varchar | YES |  |
| 16 | `categoriacliente` | varchar | YES |  |
| 17 | `fechaalta` | timestamp(3) | YES |  |
| 18 | `emailotro` | varchar | YES |  |

### stage.unidaddenegocio

**Columnas:** 18

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codempresa` | varchar | YES |  |
| 2 | `codcentro` | varchar | YES |  |
| 3 | `nombrecentro` | varchar | YES |  |
| 4 | `codseccion` | varchar | YES |  |
| 5 | `nombreseccion` | varchar | YES |  |
| 6 | `coddepartamento` | varchar | YES |  |
| 7 | `nombredepartamento` | varchar | YES |  |
| 8 | `codunidadnegocio` | varchar | YES |  |
| 9 | `nombreunidadnegocio` | varchar | YES |  |
| 10 | `sigla` | varchar | YES |  |
| 11 | `division` | varchar | YES |  |
| 12 | `codsedeambiental` | varchar | YES |  |
| 13 | `sedeambiental` | varchar | YES |  |
| 14 | `codsededistcol` | varchar | YES |  |
| 15 | `sededistribucioncolision` | varchar | YES |  |
| 16 | `unidadnegocio_requisicion` | varchar | YES |  |
| 17 | `nombreunidadnegocio_requisicion` | varchar | YES |  |
| 18 | `load_date` | varchar | YES |  |

### stage.v_habeas_data

**Columnas:** 4

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `pkterceros` | integer | YES |  |
| 2 | `nombres` | varchar | YES |  |
| 3 | `numdocumento` | varchar | YES |  |
| 4 | `valorbool` | boolean | YES |  |

### stage.v_segurosvehiculos

**Columnas:** 31

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `ano_periodo` | integer | YES |  |
| 2 | `mes_periodo` | integer | YES |  |
| 3 | `fechadecorte` | timestamp(3) | YES |  |
| 4 | `idvehiculoseguros` | smallint | YES |  |
| 5 | `idsegurotipos` | varchar | YES |  |
| 6 | `descripcionsegurotipos` | varchar | YES |  |
| 7 | `fechaalta` | timestamp(3) | YES |  |
| 8 | `fechavencimiento` | timestamp(3) | YES |  |
| 9 | `importe` | decimal(18,4) | YES |  |
| 10 | `numeropoliza` | varchar | YES |  |
| 11 | `idvehiculos` | integer | YES |  |
| 12 | `vin` | varchar | YES |  |
| 13 | `matricula` | varchar | YES |  |
| 14 | `idmarcas` | integer | YES |  |
| 15 | `nombremarca` | varchar | YES |  |
| 16 | `idgamas` | smallint | YES |  |
| 17 | `nombregama` | varchar | YES |  |
| 18 | `codmodelo` | varchar | YES |  |
| 19 | `a�omodelo` | varchar | YES |  |
| 20 | `nombremodelo` | varchar | YES |  |
| 21 | `idterceros_propietario` | integer | YES |  |
| 22 | `nifcif` | varchar | YES |  |
| 23 | `nombre` | varchar | YES |  |
| 24 | `apellido1` | varchar | YES |  |
| 25 | `apellido2` | varchar | YES |  |
| 26 | `idterceros` | integer | YES |  |
| 27 | `nombreseguro` | varchar | YES |  |
| 28 | `nombreempleado` | varchar | YES |  |
| 29 | `nombrecentrocomprasvn` | varchar | YES |  |
| 30 | `nombrecentrovo` | varchar | YES |  |
| 31 | `centroventa` | varchar | YES |  |

### stage.view_atenea_contactabilidad_detallle

**Columnas:** 20

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `pkterceros` | bigint | YES |  |
| 2 | `id_mes` | bigint | YES |  |
| 3 | `a�o` | bigint | YES |  |
| 4 | `linea` | varchar | YES |  |
| 5 | `idlinea` | bigint | YES |  |
| 6 | `sede` | varchar | YES |  |
| 7 | `idsede` | bigint | YES |  |
| 8 | `compa�ia` | varchar | YES |  |
| 9 | `area` | varchar | YES |  |
| 10 | `idarea` | bigint | YES |  |
| 11 | `mes` | varchar | YES |  |
| 12 | `contactabilidad` | varchar | YES |  |
| 13 | `idcontactabilidad` | bigint | YES |  |
| 14 | `nombrecliente` | varchar | YES |  |
| 15 | `placa` | varchar | YES |  |
| 16 | `vin` | varchar | YES |  |
| 17 | `cedulacliente` | varchar | YES |  |
| 18 | `telefonocontacto` | varchar | YES |  |
| 19 | `nombreasesor` | varchar | YES |  |
| 20 | `load_date` | varchar | YES |  |

### stage.view_atenea_nps_detalle

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `pkterceros` | bigint | YES |  |
| 2 | `mes` | varchar | YES |  |
| 3 | `a�o` | bigint | YES |  |
| 4 | `nombrecliente` | varchar | YES |  |
| 5 | `cedulacliente` | varchar | YES |  |
| 6 | `numerocelular` | varchar | YES |  |
| 7 | `telefono` | varchar | YES |  |
| 8 | `email` | varchar | YES |  |
| 9 | `marca` | varchar | YES |  |
| 10 | `area` | varchar | YES |  |
| 11 | `pregunta` | varchar | YES |  |
| 12 | `respuesta` | varchar | YES |  |

### stage.view_atenea_preguntas_detalle

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `pkterceros` | bigint | YES |  |
| 2 | `mes` | varchar | YES |  |
| 3 | `a�o` | bigint | YES |  |
| 4 | `nombrecliente` | varchar | YES |  |
| 5 | `cedulacliente` | varchar | YES |  |
| 6 | `numerocelular` | varchar | YES |  |
| 7 | `telefono` | varchar | YES |  |
| 8 | `email` | varchar | YES |  |
| 9 | `marca` | varchar | YES |  |
| 10 | `area` | varchar | YES |  |
| 11 | `pregunta` | varchar | YES |  |
| 12 | `respuesta` | varchar | YES |  |

### stage.view_atenea_satisfaccion_detalle

**Columnas:** 12

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `pkterceros` | bigint | YES |  |
| 2 | `mes` | varchar | YES |  |
| 3 | `a�o` | bigint | YES |  |
| 4 | `nombrecliente` | varchar | YES |  |
| 5 | `cedulacliente` | varchar | YES |  |
| 6 | `numerocelular` | varchar | YES |  |
| 7 | `telefono` | varchar | YES |  |
| 8 | `email` | varchar | YES |  |
| 9 | `marca` | varchar | YES |  |
| 10 | `area` | varchar | YES |  |
| 11 | `pregunta` | varchar | YES |  |
| 12 | `respuesta` | varchar | YES |  |

### stage.view_spiga_clientes_tereceros

**Columnas:** 31

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `asesor` | varchar | YES |  |
| 2 | `cantidad2` | varchar | YES |  |
| 3 | `valor` | double | YES |  |
| 4 | `fecha` | timestamp(3) | YES |  |
| 5 | `nombretercero` | varchar | YES |  |
| 6 | `idmarca` | varchar | YES |  |
| 7 | `marca` | varchar | YES |  |
| 8 | `linea` | varchar | YES |  |
| 9 | `centro` | varchar | YES |  |
| 10 | `idgama` | varchar | YES |  |
| 11 | `gama` | varchar | YES |  |
| 12 | `idversion` | varchar | YES |  |
| 13 | `version` | varchar | YES |  |
| 14 | `a�omodelo` | varchar | YES |  |
| 15 | `idterceros` | varchar | YES |  |
| 16 | `vin` | varchar | YES |  |
| 17 | `numeroidentidad` | varchar | YES |  |
| 18 | `fechaentregacliente` | timestamp(3) | YES |  |
| 19 | `codigocentro` | varchar | YES |  |
| 20 | `fechaalta` | date | YES |  |
| 21 | `tipo` | varchar | YES |  |
| 22 | `kmts` | double | YES |  |
| 23 | `tipotrabajo` | varchar | YES |  |
| 24 | `idempresa` | varchar | YES |  |
| 25 | `descripcionreferencia` | varchar | YES |  |
| 26 | `descripcionclasificacion` | varchar | YES |  |
| 27 | `nombrefinanciera` | varchar | YES |  |
| 28 | `comisionvehiculo` | varchar | YES |  |
| 29 | `estado` | varchar | YES |  |
| 30 | `producto` | varchar(21) | YES |  |
| 31 | `combustible_categoria` | varchar(15) | YES |  |

### stage.view_spiga_consultamovimientosreferencia

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `asesor` | varchar | YES |  |
| 2 | `cantidad2` | varchar | YES |  |
| 3 | `valor` | double | YES |  |
| 4 | `fecha` | date | YES |  |
| 5 | `nombretercero` | varchar | YES |  |
| 6 | `idmarca` | varchar | YES |  |
| 7 | `marca` | varchar | YES |  |
| 8 | `linea` | varchar(20) | YES |  |
| 9 | `centro` | varchar | YES |  |
| 10 | `idgama` | varchar | YES |  |
| 11 | `gama` | varchar | YES |  |
| 12 | `idversion` | varchar | YES |  |
| 13 | `version` | varchar | YES |  |
| 14 | `a�omodelo` | varchar | YES |  |
| 15 | `idterceros` | varchar | YES |  |
| 16 | `vin` | varchar | YES |  |
| 17 | `numeroidentidad` | varchar | YES |  |
| 18 | `fechaentregacliente` | date | YES |  |
| 19 | `codigocentro` | varchar | YES |  |
| 20 | `fechaalta` | date | YES |  |
| 21 | `tipo` | varchar | YES |  |
| 22 | `kmts` | double | YES |  |
| 23 | `tipotrabajo` | varchar | YES |  |
| 24 | `idempresa` | varchar | YES |  |
| 25 | `descripcionreferencia` | varchar | YES |  |
| 26 | `descripcionclasificacion` | varchar | YES |  |
| 27 | `nombrefinanciera` | varchar | YES |  |
| 28 | `comisionvehiculo` | varchar | YES |  |
| 29 | `estado` | varchar | YES |  |
| 30 | `producto` | varchar(21) | YES |  |

### stage.view_spiga_cotizacionesvn

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `asesor` | varchar | YES |  |
| 2 | `cantidad2` | varchar | YES |  |
| 3 | `valor` | double | YES |  |
| 4 | `fecha` | date | YES |  |
| 5 | `nombretercero` | varchar | YES |  |
| 6 | `idmarca` | varchar | YES |  |
| 7 | `marca` | varchar | YES |  |
| 8 | `linea` | varchar(20) | YES |  |
| 9 | `centro` | varchar | YES |  |
| 10 | `idgama` | varchar | YES |  |
| 11 | `gama` | varchar | YES |  |
| 12 | `idversion` | varchar | YES |  |
| 13 | `version` | varchar | YES |  |
| 14 | `a�omodelo` | varchar | YES |  |
| 15 | `idterceros` | varchar | YES |  |
| 16 | `vin` | varchar | YES |  |
| 17 | `numeroidentidad` | varchar | YES |  |
| 18 | `fechaentregacliente` | date | YES |  |
| 19 | `codigocentro` | varchar | YES |  |
| 20 | `fechaalta` | date | YES |  |
| 21 | `tipo` | varchar | YES |  |
| 22 | `kmts` | double | YES |  |
| 23 | `tipotrabajo` | varchar | YES |  |
| 24 | `idempresa` | varchar | YES |  |
| 25 | `descripcionreferencia` | varchar | YES |  |
| 26 | `descripcionclasificacion` | varchar | YES |  |
| 27 | `nombrefinanciera` | varchar | YES |  |
| 28 | `comisionvehiculo` | varchar | YES |  |
| 29 | `estado` | varchar | YES |  |
| 30 | `producto` | varchar(15) | YES |  |

### stage.view_spiga_cotizacionesvo

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `asesor` | varchar | YES |  |
| 2 | `cantidad2` | varchar | YES |  |
| 3 | `valor` | double | YES |  |
| 4 | `fecha` | date | YES |  |
| 5 | `nombretercero` | varchar | YES |  |
| 6 | `idmarca` | varchar | YES |  |
| 7 | `marca` | varchar | YES |  |
| 8 | `linea` | varchar(20) | YES |  |
| 9 | `centro` | varchar | YES |  |
| 10 | `idgama` | varchar | YES |  |
| 11 | `gama` | varchar | YES |  |
| 12 | `idversion` | varchar | YES |  |
| 13 | `version` | varchar | YES |  |
| 14 | `a�omodelo` | varchar | YES |  |
| 15 | `idterceros` | varchar | YES |  |
| 16 | `vin` | varchar | YES |  |
| 17 | `numeroidentidad` | varchar | YES |  |
| 18 | `fechaentregacliente` | date | YES |  |
| 19 | `codigocentro` | varchar | YES |  |
| 20 | `fechaalta` | date | YES |  |
| 21 | `tipo` | varchar | YES |  |
| 22 | `kmts` | double | YES |  |
| 23 | `tipotrabajo` | varchar | YES |  |
| 24 | `idempresa` | varchar | YES |  |
| 25 | `descripcionreferencia` | varchar | YES |  |
| 26 | `descripcionclasificacion` | varchar | YES |  |
| 27 | `nombrefinanciera` | varchar | YES |  |
| 28 | `comisionvehiculo` | varchar | YES |  |
| 29 | `estado` | varchar | YES |  |
| 30 | `producto` | varchar(15) | YES |  |

### stage.view_spiga_financiacionesventasvnvo

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `asesor` | varchar | YES |  |
| 2 | `cantidad2` | varchar | YES |  |
| 3 | `valor` | double | YES |  |
| 4 | `fecha` | timestamp(3) | YES |  |
| 5 | `nombretercero` | varchar | YES |  |
| 6 | `idmarca` | varchar | YES |  |
| 7 | `marca` | varchar | YES |  |
| 8 | `linea` | varchar | YES |  |
| 9 | `centro` | varchar | YES |  |
| 10 | `idgama` | varchar | YES |  |
| 11 | `gama` | varchar | YES |  |
| 12 | `idversion` | varchar | YES |  |
| 13 | `version` | varchar | YES |  |
| 14 | `a�omodelo` | varchar | YES |  |
| 15 | `idterceros` | varchar | YES |  |
| 16 | `vin` | varchar | YES |  |
| 17 | `numeroidentidad` | varchar | YES |  |
| 18 | `fechaentregacliente` | timestamp(3) | YES |  |
| 19 | `codigocentro` | varchar | YES |  |
| 20 | `fechaalta` | date | YES |  |
| 21 | `tipo` | varchar | YES |  |
| 22 | `kmts` | double | YES |  |
| 23 | `tipotrabajo` | varchar | YES |  |
| 24 | `idempresa` | varchar | YES |  |
| 25 | `descripcionreferencia` | varchar | YES |  |
| 26 | `descripcionclasificacion` | varchar | YES |  |
| 27 | `nombrefinanciera` | varchar | YES |  |
| 28 | `comisionvehiculo` | varchar | YES |  |
| 29 | `estado` | varchar | YES |  |
| 30 | `producto` | varchar(21) | YES |  |

### stage.view_spiga_informafacturacion

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `asesor` | varchar | YES |  |
| 2 | `cantidad2` | varchar | YES |  |
| 3 | `valor` | double | YES |  |
| 4 | `fecha` | date | YES |  |
| 5 | `nombretercero` | varchar | YES |  |
| 6 | `idmarca` | varchar | YES |  |
| 7 | `marca` | varchar | YES |  |
| 8 | `linea` | varchar(20) | YES |  |
| 9 | `centro` | varchar | YES |  |
| 10 | `idgama` | varchar | YES |  |
| 11 | `gama` | varchar | YES |  |
| 12 | `idversion` | varchar | YES |  |
| 13 | `version` | varchar | YES |  |
| 14 | `a�omodelo` | varchar | YES |  |
| 15 | `idterceros` | varchar | YES |  |
| 16 | `vin` | varchar | YES |  |
| 17 | `numeroidentidad` | varchar | YES |  |
| 18 | `fechaentregacliente` | date | YES |  |
| 19 | `codigocentro` | varchar | YES |  |
| 20 | `fechaalta` | date | YES |  |
| 21 | `tipo` | varchar(12) | YES |  |
| 22 | `kmts` | double | YES |  |
| 23 | `tipotrabajo` | varchar | YES |  |
| 24 | `idempresa` | varchar | YES |  |
| 25 | `descripcionreferencia` | varchar | YES |  |
| 26 | `descripcionclasificacion` | varchar | YES |  |
| 27 | `nombrefinanciera` | varchar | YES |  |
| 28 | `comisionvehiculo` | varchar | YES |  |
| 29 | `estado` | varchar | YES |  |
| 30 | `producto` | varchar(19) | YES |  |

### stage.view_spiga_vehiculos_entregados

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `asesor` | varchar | YES |  |
| 2 | `cantidad2` | varchar | YES |  |
| 3 | `valor` | double | YES |  |
| 4 | `fecha` | date | YES |  |
| 5 | `nombretercero` | varchar | YES |  |
| 6 | `idmarca` | varchar | YES |  |
| 7 | `marca` | varchar | YES |  |
| 8 | `linea` | varchar(20) | YES |  |
| 9 | `centro` | varchar | YES |  |
| 10 | `idgama` | varchar | YES |  |
| 11 | `gama` | varchar | YES |  |
| 12 | `idversion` | varchar | YES |  |
| 13 | `version` | varchar | YES |  |
| 14 | `a�omodelo` | varchar | YES |  |
| 15 | `idterceros` | varchar | YES |  |
| 16 | `vin` | varchar | YES |  |
| 17 | `numeroidentidad` | varchar | YES |  |
| 18 | `fechaentregacliente` | date | YES |  |
| 19 | `codigocentro` | varchar | YES |  |
| 20 | `fechaalta` | date | YES |  |
| 21 | `tipo` | varchar | YES |  |
| 22 | `kmts` | double | YES |  |
| 23 | `tipotrabajo` | varchar | YES |  |
| 24 | `idempresa` | varchar | YES |  |
| 25 | `descripcionreferencia` | varchar | YES |  |
| 26 | `descripcionclasificacion` | varchar | YES |  |
| 27 | `nombrefinanciera` | varchar | YES |  |
| 28 | `comisionvehiculo` | varchar | YES |  |
| 29 | `estado` | varchar | YES |  |
| 30 | `producto` | varchar(20) | YES |  |

### stage.view_spiga_vehiculosseguros

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `asesor` | varchar | YES |  |
| 2 | `cantidad2` | varchar | YES |  |
| 3 | `valor` | double | YES |  |
| 4 | `fecha` | date | YES |  |
| 5 | `nombretercero` | varchar | YES |  |
| 6 | `idmarca` | varchar | YES |  |
| 7 | `marca` | varchar | YES |  |
| 8 | `linea` | varchar | YES |  |
| 9 | `centro` | varchar | YES |  |
| 10 | `idgama` | varchar | YES |  |
| 11 | `gama` | varchar | YES |  |
| 12 | `idversion` | varchar | YES |  |
| 13 | `version` | varchar | YES |  |
| 14 | `a�omodelo` | varchar | YES |  |
| 15 | `idterceros` | varchar | YES |  |
| 16 | `vin` | varchar | YES |  |
| 17 | `numeroidentidad` | varchar | YES |  |
| 18 | `fechaentregacliente` | date | YES |  |
| 19 | `codigocentro` | varchar | YES |  |
| 20 | `fechaalta` | date | YES |  |
| 21 | `tipo` | varchar | YES |  |
| 22 | `kmts` | double | YES |  |
| 23 | `tipotrabajo` | varchar | YES |  |
| 24 | `idempresa` | varchar | YES |  |
| 25 | `descripcionreferencia` | varchar | YES |  |
| 26 | `descripcionclasificacion` | varchar | YES |  |
| 27 | `nombrefinanciera` | varchar | YES |  |
| 28 | `comisionvehiculo` | varchar | YES |  |
| 29 | `estado` | varchar | YES |  |
| 30 | `producto` | varchar(17) | YES |  |

### stage.vista_ecosistema

**Columnas:** 28

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `client_id` | integer | YES |  |
| 2 | `product_services_id` | integer | YES |  |
| 3 | `product_name` | varchar | YES |  |
| 4 | `company` | varchar | YES |  |
| 5 | `company_id` | integer | YES |  |
| 6 | `contract_date` | date | YES |  |
| 7 | `total_compras` | bigint | YES |  |
| 8 | `producto_origen_id` | integer | YES |  |
| 9 | `producto_origen_name` | varchar | YES |  |
| 10 | `producto_origen_company` | varchar | YES |  |
| 11 | `target_id` | integer | YES |  |
| 12 | `dias_entre_compras` | bigint | YES |  |
| 13 | `dias_desde_ultima_compra` | bigint | YES |  |
| 14 | `sale_amount` | double | YES |  |
| 15 | `financed_amount` | double | YES |  |
| 16 | `invoiced_amount` | double | YES |  |
| 17 | `monto_total` | double | YES |  |
| 18 | `age` | integer | YES |  |
| 19 | `gender_name` | varchar | YES |  |
| 20 | `municipality` | varchar | YES |  |
| 21 | `departament` | varchar | YES |  |
| 22 | `country` | varchar | YES |  |
| 23 | `marital_status` | varchar | YES |  |
| 24 | `occupation` | varchar | YES |  |
| 25 | `level_education` | varchar | YES |  |
| 26 | `client_status` | varchar | YES |  |
| 27 | `fecha_primera_compra` | date | YES |  |
| 28 | `dias_desde_primera_compra` | bigint | YES |  |

### stage.vista_final_recompra

**Columnas:** 11

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `nombre_completo` | varchar | YES |  |
| 2 | `correo` | varchar | YES |  |
| 3 | `telefono` | varchar | YES |  |
| 4 | `documento` | varchar | YES |  |
| 5 | `centro` | varchar | YES |  |
| 6 | `anio_modelo_ultima_compra` | varchar | YES |  |
| 7 | `ultimo_vin` | varchar | YES |  |
| 8 | `marca_recomendada` | varchar | YES |  |
| 9 | `modelo_recomendado` | varchar | YES |  |
| 10 | `fecha_estimada` | date | YES |  |
| 11 | `fila_marca` | bigint | YES |  |

### stage.vw_atenea_contactabilidad

**Columnas:** 16

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id_mes` | bigint | YES |  |
| 2 | `a�o` | bigint | YES |  |
| 3 | `linea` | varchar | YES |  |
| 4 | `idlinea` | bigint | YES |  |
| 5 | `sede` | varchar | YES |  |
| 6 | `idsede` | bigint | YES |  |
| 7 | `area` | varchar | YES |  |
| 8 | `idarea` | bigint | YES |  |
| 9 | `mes` | varchar | YES |  |
| 10 | `contactabilidad` | varchar | YES |  |
| 11 | `idcontactabilidad` | bigint | YES |  |
| 12 | `total` | bigint | YES |  |
| 13 | `basescargadas` | bigint | YES |  |
| 14 | `compa�ia` | varchar | YES |  |
| 15 | `porcentaje` | varchar | YES |  |
| 16 | `load_date` | varchar | YES |  |

### stage.vw_atenea_contactabilidad_detalle

**Columnas:** 19

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id_mes` | bigint | YES |  |
| 2 | `a�o` | bigint | YES |  |
| 3 | `linea` | varchar | YES |  |
| 4 | `idlinea` | bigint | YES |  |
| 5 | `sede` | varchar | YES |  |
| 6 | `idsede` | bigint | YES |  |
| 7 | `compa�ia` | varchar | YES |  |
| 8 | `area` | varchar | YES |  |
| 9 | `idarea` | bigint | YES |  |
| 10 | `mes` | varchar | YES |  |
| 11 | `contactabilidad` | varchar | YES |  |
| 12 | `idcontactabilidad` | bigint | YES |  |
| 13 | `nombrecliente` | varchar | YES |  |
| 14 | `placa` | varchar | YES |  |
| 15 | `vin` | varchar | YES |  |
| 16 | `cedulacliente` | varchar | YES |  |
| 17 | `telefonocontacto` | varchar | YES |  |
| 18 | `nombreasesor` | varchar | YES |  |
| 19 | `load_date` | varchar | YES |  |

### stage.vw_atenea_nps

**Columnas:** 21

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id_mes` | bigint | YES |  |
| 2 | `a�o` | bigint | YES |  |
| 3 | `id_compa�ia` | varchar | YES |  |
| 4 | `sede` | varchar | YES |  |
| 5 | `idsede` | bigint | YES |  |
| 6 | `linea` | varchar | YES |  |
| 7 | `idlinea` | bigint | YES |  |
| 8 | `area` | varchar | YES |  |
| 9 | `idarea` | bigint | YES |  |
| 10 | `mes` | varchar | YES |  |
| 11 | `promotores` | bigint | YES |  |
| 12 | `neutros` | bigint | YES |  |
| 13 | `detractores` | bigint | YES |  |
| 14 | `total` | bigint | YES |  |
| 15 | `porcentajepromotor` | varchar | YES |  |
| 16 | `porcentajeneutros` | varchar | YES |  |
| 17 | `porcentajedetractores` | varchar | YES |  |
| 18 | `npstotal` | varchar | YES |  |
| 19 | `meta` | varchar | YES |  |
| 20 | `compa�ia` | varchar | YES |  |
| 21 | `load_date` | varchar | YES |  |

### stage.vw_atenea_nps_detalle

**Columnas:** 40

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `mes` | varchar | YES |  |
| 2 | `idmes` | bigint | YES |  |
| 3 | `a�o` | bigint | YES |  |
| 4 | `nombrecliente` | varchar | YES |  |
| 5 | `cedulacliente` | varchar | YES |  |
| 6 | `numerocelular` | varchar | YES |  |
| 7 | `telefono` | varchar | YES |  |
| 8 | `telefono2` | varchar | YES |  |
| 9 | `ciudad` | varchar | YES |  |
| 10 | `email` | varchar | YES |  |
| 11 | `sede` | varchar | YES |  |
| 12 | `idsede` | bigint | YES |  |
| 13 | `linea` | varchar | YES |  |
| 14 | `idlinea` | bigint | YES |  |
| 15 | `marca` | varchar | YES |  |
| 16 | `area` | varchar | YES |  |
| 17 | `idarea` | bigint | YES |  |
| 18 | `placa` | varchar | YES |  |
| 19 | `descripciontrabajo` | varchar | YES |  |
| 20 | `asesor` | varchar | YES |  |
| 21 | `fechagestion` | timestamp(3) | YES |  |
| 22 | `resultadogestion` | varchar | YES |  |
| 23 | `canal` | varchar | YES |  |
| 24 | `idcanal` | bigint | YES |  |
| 25 | `usuario` | varchar | YES |  |
| 26 | `nombreusuario` | varchar | YES |  |
| 27 | `numerocontactado` | varchar | YES |  |
| 28 | `pregunta` | varchar | YES |  |
| 29 | `respuesta` | varchar | YES |  |
| 30 | `codigocaso` | varchar | YES |  |
| 31 | `tipocaso` | varchar | YES |  |
| 32 | `clasificacioncaso` | varchar | YES |  |
| 33 | `subclasificacioncaso` | varchar | YES |  |
| 34 | `detalle` | varchar | YES |  |
| 35 | `descripcion` | varchar | YES |  |
| 36 | `fechacreacioncaso` | timestamp(3) | YES |  |
| 37 | `fechavencimientocaso` | timestamp(3) | YES |  |
| 38 | `fechacierrecaso` | timestamp(3) | YES |  |
| 39 | `responsablecaso` | varchar | YES |  |
| 40 | `load_date` | varchar | YES |  |

### stage.vw_atenea_ordenes_asesores_total

**Columnas:** 13

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `advisername` | varchar | YES |  |
| 2 | `totalasesor` | bigint | YES |  |
| 3 | `id_mes` | bigint | YES |  |
| 4 | `mes` | varchar | YES |  |
| 5 | `a�o` | bigint | YES |  |
| 6 | `compa�ia` | varchar | YES |  |
| 7 | `linea` | varchar | YES |  |
| 8 | `idlinea` | bigint | YES |  |
| 9 | `sede` | varchar | YES |  |
| 10 | `idsede` | bigint | YES |  |
| 11 | `area` | varchar | YES |  |
| 12 | `idarea` | bigint | YES |  |
| 13 | `load_date` | varchar | YES |  |

### stage.vw_atenea_pqr

**Columnas:** 34

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `id_mes` | bigint | YES |  |
| 3 | `a�o` | bigint | YES |  |
| 4 | `mes` | varchar | YES |  |
| 5 | `empresa` | varchar | YES |  |
| 6 | `linea` | varchar | YES |  |
| 7 | `sede` | varchar | YES |  |
| 8 | `proceso` | varchar | YES |  |
| 9 | `identificationnumber` | varchar | YES |  |
| 10 | `nombrecliente` | varchar | YES |  |
| 11 | `placa` | varchar | YES |  |
| 12 | `gamma` | varchar | YES |  |
| 13 | `modelo` | varchar | YES |  |
| 14 | `kilometraje` | varchar | YES |  |
| 15 | `vin` | varchar | YES |  |
| 16 | `marcavehiculo` | varchar | YES |  |
| 17 | `numeromotor` | varchar | YES |  |
| 18 | `telefonocontacto` | varchar | YES |  |
| 19 | `idticket` | bigint | YES |  |
| 20 | `c�digocaso` | varchar | YES |  |
| 21 | `tipocaso` | varchar | YES |  |
| 22 | `clasificacioncaso` | varchar | YES |  |
| 23 | `subclasificacioncaso` | varchar | YES |  |
| 24 | `detalle` | varchar | YES |  |
| 25 | `descripci�n` | varchar | YES |  |
| 26 | `fecharegistro` | timestamp(3) | YES |  |
| 27 | `fecharespuesta` | timestamp(3) | YES |  |
| 28 | `cantidaddiascierre` | bigint | YES |  |
| 29 | `cantidaddiastranscurridos` | bigint | YES |  |
| 30 | `estado` | varchar | YES |  |
| 31 | `origen` | varchar | YES |  |
| 32 | `subclasificaci�n` | varchar | YES |  |
| 33 | `nombreasesor` | varchar | YES |  |
| 34 | `load_date` | varchar | YES |  |

### stage.vw_atenea_preguntas_detalle

**Columnas:** 40

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `mes` | varchar | YES |  |
| 2 | `idmes` | bigint | YES |  |
| 3 | `a�o` | bigint | YES |  |
| 4 | `nombrecliente` | varchar | YES |  |
| 5 | `cedulacliente` | varchar | YES |  |
| 6 | `numerocelular` | varchar | YES |  |
| 7 | `telefono` | varchar | YES |  |
| 8 | `telefono2` | varchar | YES |  |
| 9 | `ciudad` | varchar | YES |  |
| 10 | `email` | varchar | YES |  |
| 11 | `sede` | varchar | YES |  |
| 12 | `idsede` | bigint | YES |  |
| 13 | `linea` | varchar | YES |  |
| 14 | `idlinea` | bigint | YES |  |
| 15 | `marca` | varchar | YES |  |
| 16 | `area` | varchar | YES |  |
| 17 | `idarea` | bigint | YES |  |
| 18 | `placa` | varchar | YES |  |
| 19 | `descripciontrabajo` | varchar | YES |  |
| 20 | `asesor` | varchar | YES |  |
| 21 | `fechagestion` | timestamp(3) | YES |  |
| 22 | `resultadogestion` | varchar | YES |  |
| 23 | `canal` | varchar | YES |  |
| 24 | `idcanal` | bigint | YES |  |
| 25 | `usuario` | varchar | YES |  |
| 26 | `nombreusuario` | varchar | YES |  |
| 27 | `numerocontactado` | varchar | YES |  |
| 28 | `pregunta` | varchar | YES |  |
| 29 | `respuesta` | varchar | YES |  |
| 30 | `codigocaso` | varchar | YES |  |
| 31 | `tipocaso` | varchar | YES |  |
| 32 | `clasificacioncaso` | varchar | YES |  |
| 33 | `subclasificacioncaso` | varchar | YES |  |
| 34 | `detalle` | varchar | YES |  |
| 35 | `descripcion` | varchar | YES |  |
| 36 | `fechacreacioncaso` | timestamp(3) | YES |  |
| 37 | `fechavencimientocaso` | timestamp(3) | YES |  |
| 38 | `fechacierrecaso` | timestamp(3) | YES |  |
| 39 | `responsablecaso` | varchar | YES |  |
| 40 | `load_date` | varchar | YES |  |

### stage.vw_atenea_satisfaccion

**Columnas:** 19

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id_mes` | bigint | YES |  |
| 2 | `mes` | varchar | YES |  |
| 3 | `a�o` | bigint | YES |  |
| 4 | `sede` | varchar | YES |  |
| 5 | `idsede` | bigint | YES |  |
| 6 | `linea` | varchar | YES |  |
| 7 | `idlinea` | bigint | YES |  |
| 8 | `area` | varchar | YES |  |
| 9 | `idarea` | bigint | YES |  |
| 10 | `encuestasefectivas` | bigint | YES |  |
| 11 | `res_1` | bigint | YES |  |
| 12 | `res_2` | bigint | YES |  |
| 13 | `res_3` | bigint | YES |  |
| 14 | `res_4` | bigint | YES |  |
| 15 | `res_5` | bigint | YES |  |
| 16 | `satisfaccion` | bigint | YES |  |
| 17 | `meta` | varchar | YES |  |
| 18 | `compa�ia` | varchar | YES |  |
| 19 | `load_date` | varchar | YES |  |

### stage.vw_atenea_satisfaccion_detalle

**Columnas:** 40

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idmes` | bigint | YES |  |
| 2 | `a�o` | bigint | YES |  |
| 3 | `mes` | varchar | YES |  |
| 4 | `nombrecliente` | varchar | YES |  |
| 5 | `cedulacliente` | varchar | YES |  |
| 6 | `numerocelular` | varchar | YES |  |
| 7 | `telefono` | varchar | YES |  |
| 8 | `telefono2` | varchar | YES |  |
| 9 | `ciudad` | varchar | YES |  |
| 10 | `email` | varchar | YES |  |
| 11 | `sede` | varchar | YES |  |
| 12 | `idsede` | bigint | YES |  |
| 13 | `linea` | varchar | YES |  |
| 14 | `idlinea` | bigint | YES |  |
| 15 | `marca` | varchar | YES |  |
| 16 | `area` | varchar | YES |  |
| 17 | `idarea` | bigint | YES |  |
| 18 | `placa` | varchar | YES |  |
| 19 | `descripciontrabajo` | varchar | YES |  |
| 20 | `asesor` | varchar | YES |  |
| 21 | `fechagestion` | timestamp(3) | YES |  |
| 22 | `resultadogestion` | varchar | YES |  |
| 23 | `canal` | varchar | YES |  |
| 24 | `idcanal` | bigint | YES |  |
| 25 | `usuario` | varchar | YES |  |
| 26 | `nombreusuario` | varchar | YES |  |
| 27 | `numerocontactado` | varchar | YES |  |
| 28 | `pregunta` | varchar | YES |  |
| 29 | `respuesta` | varchar | YES |  |
| 30 | `codigocaso` | varchar | YES |  |
| 31 | `tipocaso` | varchar | YES |  |
| 32 | `clasificacioncaso` | varchar | YES |  |
| 33 | `subclasificacioncaso` | varchar | YES |  |
| 34 | `detalle` | varchar | YES |  |
| 35 | `descripcion` | varchar | YES |  |
| 36 | `fechacreacioncaso` | timestamp(3) | YES |  |
| 37 | `fechavencimientocaso` | timestamp(3) | YES |  |
| 38 | `fechacierrecaso` | timestamp(3) | YES |  |
| 39 | `responsablecaso` | varchar | YES |  |
| 40 | `load_date` | varchar | YES |  |

### stage.vw_comisionesspigavn

**Columnas:** 49

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `idcomisionspiga` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `ano_spiga` | integer | YES |  |
| 6 | `mes_spiga` | integer | YES |  |
| 7 | `codigoempresa` | smallint | YES |  |
| 8 | `empresa` | varchar | YES |  |
| 9 | `codigoempresasugerido` | integer | YES |  |
| 10 | `empresasugerida` | varchar | YES |  |
| 11 | `codigocentro` | smallint | YES |  |
| 12 | `centro` | varchar | YES |  |
| 13 | `codigoseccion` | integer | YES |  |
| 14 | `seccion` | varchar | YES |  |
| 15 | `fechafactura` | timestamp(3) | YES |  |
| 16 | `numerofactura` | varchar | YES |  |
| 17 | `vin` | varchar | YES |  |
| 18 | `codigomarca` | smallint | YES |  |
| 19 | `marca` | varchar | YES |  |
| 20 | `codigogama` | smallint | YES |  |
| 21 | `gama` | varchar | YES |  |
| 22 | `codigomodelo` | varchar | YES |  |
| 23 | `extension` | varchar | YES |  |
| 24 | `a�omodelo` | varchar | YES |  |
| 25 | `modelo` | varchar | YES |  |
| 26 | `codigoversion` | varchar | YES |  |
| 27 | `nombreversion` | varchar | YES |  |
| 28 | `cedulavendedor` | bigint | YES |  |
| 29 | `nombrevendedor` | varchar | YES |  |
| 30 | `nit` | varchar | YES |  |
| 31 | `nombretercero` | varchar | YES |  |
| 32 | `preciovehiculo` | decimal(18,4) | YES |  |
| 33 | `preciolista` | decimal(18,4) | YES |  |
| 34 | `valordto` | decimal(18,4) | YES |  |
| 35 | `importeimpuestos` | decimal(38,4) | YES |  |
| 36 | `totalfactura` | decimal(18,4) | YES |  |
| 37 | `fechacancelacionfactura` | timestamp(3) | YES |  |
| 38 | `totalcanceladofactura` | decimal(38,4) | YES |  |
| 39 | `fecharemesa` | timestamp(3) | YES |  |
| 40 | `valorremesado` | decimal(38,4) | YES |  |
| 41 | `fechaentregacliente` | timestamp(3) | YES |  |
| 42 | `descuentopolitica` | decimal(15,9) | YES |  |
| 43 | `numerentregas` | integer | YES |  |
| 44 | `tipo_servicio` | varchar | YES |  |
| 45 | `cuotaretefuente` | decimal(18,4) | YES |  |
| 46 | `entregaefectiva` | integer | YES |  |
| 47 | `procedencia` | varchar | YES |  |
| 48 | `procedenciadetalle` | varchar | YES |  |
| 49 | `tipooportunidad` | varchar | YES |  |

### stage.vw_comisionesspigavo

**Columnas:** 49

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `idcomisionspiga` | integer | YES |  |
| 3 | `ano_periodo` | integer | YES |  |
| 4 | `mes_periodo` | integer | YES |  |
| 5 | `ano_spiga` | integer | YES |  |
| 6 | `mes_spiga` | integer | YES |  |
| 7 | `codigoempresa` | smallint | YES |  |
| 8 | `empresa` | varchar | YES |  |
| 9 | `codigoempresasugerido` | integer | YES |  |
| 10 | `empresasugerida` | varchar | YES |  |
| 11 | `codigocentro` | smallint | YES |  |
| 12 | `centro` | varchar | YES |  |
| 13 | `codigoseccion` | integer | YES |  |
| 14 | `seccion` | varchar | YES |  |
| 15 | `fechafactura` | timestamp(3) | YES |  |
| 16 | `numerofactura` | varchar | YES |  |
| 17 | `vin` | varchar | YES |  |
| 18 | `codigomarca` | smallint | YES |  |
| 19 | `marca` | varchar | YES |  |
| 20 | `codigogama` | smallint | YES |  |
| 21 | `gama` | varchar | YES |  |
| 22 | `codigomodelo` | varchar | YES |  |
| 23 | `extension` | varchar | YES |  |
| 24 | `a�omodelo` | varchar | YES |  |
| 25 | `modelo` | varchar | YES |  |
| 26 | `codigoversion` | varchar | YES |  |
| 27 | `nombreversion` | varchar | YES |  |
| 28 | `cedulavendedor` | bigint | YES |  |
| 29 | `nombrevendedor` | varchar | YES |  |
| 30 | `nit` | varchar | YES |  |
| 31 | `nombretercero` | varchar | YES |  |
| 32 | `preciovehiculo` | decimal(18,4) | YES |  |
| 33 | `preciolista` | decimal(18,4) | YES |  |
| 34 | `valordto` | decimal(18,4) | YES |  |
| 35 | `importeimpuestos` | decimal(38,4) | YES |  |
| 36 | `totalfactura` | decimal(18,4) | YES |  |
| 37 | `fechacancelacionfactura` | timestamp(3) | YES |  |
| 38 | `totalcanceladofactura` | decimal(38,4) | YES |  |
| 39 | `fecharemesa` | timestamp(3) | YES |  |
| 40 | `valorremesado` | decimal(38,4) | YES |  |
| 41 | `fechaentregacliente` | timestamp(3) | YES |  |
| 42 | `descuentopolitica` | decimal(15,9) | YES |  |
| 43 | `numerentregas` | integer | YES |  |
| 44 | `tipo_servicio` | varchar | YES |  |
| 45 | `cuotaretefuente` | decimal(38,4) | YES |  |
| 46 | `entregaefectiva` | integer | YES |  |
| 47 | `procedencia` | varchar | YES |  |
| 48 | `procedenciadetalle` | varchar | YES |  |
| 49 | `tipooportunidad` | varchar | YES |  |

### stage.vw_consulta_mov_ref

**Columnas:** 163

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idtipolinea` | varchar | YES |  |
| 7 | `idmovimientotipos` | varchar | YES |  |
| 8 | `idmr` | varchar | YES |  |
| 9 | `idreferencias` | varchar | YES |  |
| 10 | `fechaalta` | timestamp(3) | YES |  |
| 11 | `idempresas` | bigint | YES |  |
| 12 | `idcentros` | bigint | YES |  |
| 13 | `idsecciones` | bigint | YES |  |
| 14 | `idubicaciones` | varchar | YES |  |
| 15 | `stock` | double | YES |  |
| 16 | `precio` | double | YES |  |
| 17 | `pmc` | double | YES |  |
| 18 | `confirmado` | bigint | YES |  |
| 19 | `unidades` | double | YES |  |
| 20 | `dtoporc` | double | YES |  |
| 21 | `idtarifas` | bigint | YES |  |
| 22 | `idclasificacion1movimiento` | varchar | YES |  |
| 23 | `hostmod` | varchar | YES |  |
| 24 | `usermod` | bigint | YES |  |
| 25 | `fechamod` | timestamp(3) | YES |  |
| 26 | `versionfila` | bigint | YES |  |
| 27 | `fechadocumento` | timestamp(3) | YES |  |
| 28 | `ida�o` | varchar | YES |  |
| 29 | `serie` | varchar | YES |  |
| 30 | `numero` | varchar | YES |  |
| 31 | `idterceros` | bigint | YES |  |
| 32 | `numdet` | bigint | YES |  |
| 33 | `seriefactura` | varchar | YES |  |
| 34 | `factura` | varchar | YES |  |
| 35 | `a�ofactura` | varchar | YES |  |
| 36 | `fechafactura` | timestamp(3) | YES |  |
| 37 | `idusuario` | bigint | YES |  |
| 38 | `loginguardadoautomatico` | bigint | YES |  |
| 39 | `hostguardadoautomatico` | varchar | YES |  |
| 40 | `fechaguardadoautomatico` | timestamp(3) | YES |  |
| 41 | `loginpteconfirmar` | bigint | YES |  |
| 42 | `hostpteconfirmar` | varchar | YES |  |
| 43 | `fechapteconfirmar` | timestamp(3) | YES |  |
| 44 | `idcentrosdestino` | bigint | YES |  |
| 45 | `idseccionesdestino` | bigint | YES |  |
| 46 | `idubicacionesdestino` | varchar | YES |  |
| 47 | `idcausaregularizacion` | bigint | YES |  |
| 48 | `idcausatraspaso` | bigint | YES |  |
| 49 | `a�oot` | varchar | YES |  |
| 50 | `serieot` | varchar | YES |  |
| 51 | `numot` | bigint | YES |  |
| 52 | `idtrabajo` | bigint | YES |  |
| 53 | `idempleadosalta` | bigint | YES |  |
| 54 | `fechacierre` | timestamp(3) | YES |  |
| 55 | `gastosadicionales` | double | YES |  |
| 56 | `gastosadicionalesalbaran` | double | YES |  |
| 57 | `incrementopvp` | double | YES |  |
| 58 | `undenvaseventa` | double | YES |  |
| 59 | `idestadoscompras` | varchar | YES |  |
| 60 | `idincidenciatipos` | varchar | YES |  |
| 61 | `undenvasecompra` | double | YES |  |
| 62 | `codras` | varchar | YES |  |
| 63 | `idimputaciontipos` | bigint | YES |  |
| 64 | `idtipocompra` | bigint | YES |  |
| 65 | `portes` | varchar | YES |  |
| 66 | `embalajes` | varchar | YES |  |
| 67 | `iddepartamentodestino` | varchar | YES |  |
| 68 | `descripcionmovimientotipo` | varchar | YES |  |
| 69 | `nombreempresa` | varchar | YES |  |
| 70 | `nombrecentro` | varchar | YES |  |
| 71 | `descripcionmr` | varchar | YES |  |
| 72 | `descripcionseccion` | varchar | YES |  |
| 73 | `iddepartamentos` | varchar | YES |  |
| 74 | `tipocargotaller` | varchar | YES |  |
| 75 | `ida�oppc` | varchar | YES |  |
| 76 | `idserieppc` | varchar | YES |  |
| 77 | `numeroppc` | varchar | YES |  |
| 78 | `numerodetppc` | varchar | YES |  |
| 79 | `tasas` | varchar | YES |  |
| 80 | `nombretercero` | varchar | YES |  |
| 81 | `nifcif` | varchar | YES |  |
| 82 | `idclientecategorias` | varchar | YES |  |
| 83 | `idmotivosabono` | varchar | YES |  |
| 84 | `descripcioncategoriacliente` | varchar | YES |  |
| 85 | `nombrecentrodestino` | varchar | YES |  |
| 86 | `descripcionsecciondestino` | varchar | YES |  |
| 87 | `iddepartamentosdestino` | varchar | YES |  |
| 88 | `descripcioncausaregularizacion` | varchar | YES |  |
| 89 | `descripciontipocompra` | varchar | YES |  |
| 90 | `descripcioncausaabonotipo` | varchar | YES |  |
| 91 | `descripcionimputaciontipos` | varchar | YES |  |
| 92 | `nombreempleado` | varchar | YES |  |
| 93 | `nombrefabricante` | varchar | YES |  |
| 94 | `descripcionreferencia` | varchar | YES |  |
| 95 | `descripcioncausatraspaso` | varchar | YES |  |
| 96 | `idfabricantes` | varchar | YES |  |
| 97 | `idclasificacion1` | varchar | YES |  |
| 98 | `idclasificacion2` | varchar | YES |  |
| 99 | `idclasificacion3` | varchar | YES |  |
| 100 | `idclasificacion4` | varchar | YES |  |
| 101 | `idclasificacion5` | varchar | YES |  |
| 102 | `idclasificacion6` | varchar | YES |  |
| 103 | `iddescuentos` | varchar | YES |  |
| 104 | `idrutasrecogida` | varchar | YES |  |
| 105 | `hostrecogida` | varchar | YES |  |
| 106 | `fecharecogida` | timestamp(3) | YES |  |
| 107 | `idempleadosrecogida` | varchar | YES |  |
| 108 | `unidadesrecogida` | varchar | YES |  |
| 109 | `idbultos` | varchar | YES |  |
| 110 | `idempleadosconfirmacion` | varchar | YES |  |
| 111 | `fechaconfirmacion` | timestamp(3) | YES |  |
| 112 | `hostconfirmacion` | varchar | YES |  |
| 113 | `unidadesalbaran` | varchar | YES |  |
| 114 | `idempleadosrecepcion` | varchar | YES |  |
| 115 | `hostrecepcion` | varchar | YES |  |
| 116 | `fecharecepcion` | timestamp(3) | YES |  |
| 117 | `unidadesrecibidas` | varchar | YES |  |
| 118 | `fechaubicacion` | timestamp(3) | YES |  |
| 119 | `idempleadosubicacion` | varchar | YES |  |
| 120 | `hostentrega` | varchar | YES |  |
| 121 | `fechaentrega` | timestamp(3) | YES |  |
| 122 | `idempleadosentrega` | varchar | YES |  |
| 123 | `hostubicacion` | varchar | YES |  |
| 124 | `nombreempleadoalta` | varchar | YES |  |
| 125 | `nombreempleadorecogida` | varchar | YES |  |
| 126 | `nombreempleadoconfirmacion` | varchar | YES |  |
| 127 | `nombreempleadorecepcion` | varchar | YES |  |
| 128 | `nombreempleadoubicacion` | varchar | YES |  |
| 129 | `nombreempleadoentrega` | varchar | YES |  |
| 130 | `descripcionincidenciatipos` | varchar | YES |  |
| 131 | `idpedidotipoventas` | varchar | YES |  |
| 132 | `descripcionpedidotipoventas` | varchar | YES |  |
| 133 | `nombremecanico` | varchar | YES |  |
| 134 | `nombretercerotrabajo` | varchar | YES |  |
| 135 | `apellido1tercerotrabajo` | varchar | YES |  |
| 136 | `apellido2tercerotrabajo` | varchar | YES |  |
| 137 | `nombrecomercialtercerotrabajo` | varchar | YES |  |
| 138 | `ventaespecial` | bigint | YES |  |
| 139 | `idtercerostrabajo` | varchar | YES |  |
| 140 | `codigobulto` | varchar | YES |  |
| 141 | `volumen` | double | YES |  |
| 142 | `factorcambiopmcontravalor` | double | YES |  |
| 143 | `descripcionclasificacion1` | varchar | YES |  |
| 144 | `descripcionclasificacion2` | varchar | YES |  |
| 145 | `descripcionclasificacion3` | varchar | YES |  |
| 146 | `descripcionclasificacion4` | varchar | YES |  |
| 147 | `descripcionclasificacion5` | varchar | YES |  |
| 148 | `descripcionclasificacion6` | varchar | YES |  |
| 149 | `descripcionclasificacion1movimiento` | varchar | YES |  |
| 150 | `preciocompra` | varchar | YES |  |
| 151 | `idmonedas` | varchar | YES |  |
| 152 | `factorcambiomoneda` | varchar | YES |  |
| 153 | `idusuariosautorizacion` | varchar | YES |  |
| 154 | `nombreusuarioautorizacion` | varchar | YES |  |
| 155 | `idnegociotipos` | varchar | YES |  |
| 156 | `nombreempleadovendedorrecambios` | varchar | YES |  |
| 157 | `seriefacturataller` | varchar | YES |  |
| 158 | `numerofacturataller` | varchar | YES |  |
| 159 | `a�ofacturataller` | varchar | YES |  |
| 160 | `fechafacturataller` | timestamp(3) | YES |  |
| 161 | `vin` | varchar | YES |  |
| 162 | `descripcionpedidotipocompras` | varchar | YES |  |
| 163 | `load_date` | varchar | YES |  |

### stage.vw_empleadosactivos

**Columnas:** 48

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `codigoempleado` | bigint | YES |  |
| 2 | `ano_periodo` | integer | YES |  |
| 3 | `mes_periodo` | integer | YES |  |
| 4 | `codigoempresa` | smallint | YES |  |
| 5 | `empresa` | varchar | YES |  |
| 6 | `nombres` | varchar | YES |  |
| 7 | `apellido1` | varchar | YES |  |
| 8 | `apellido2` | varchar | YES |  |
| 9 | `nombrecompleto` | varchar | YES |  |
| 10 | `fecha_ingreso` | timestamp(3) | YES |  |
| 11 | `codigomarca` | smallint | YES |  |
| 12 | `marca` | varchar | YES |  |
| 13 | `codigo_centro` | varchar | YES |  |
| 14 | `nombre_centro` | varchar | YES |  |
| 15 | `codigo_seccion` | varchar | YES |  |
| 16 | `nombre_seccion` | varchar | YES |  |
| 17 | `codigo_sucursal` | varchar | YES |  |
| 18 | `nombre_sucursal` | varchar | YES |  |
| 19 | `codigo_departamento` | varchar | YES |  |
| 20 | `nombre_departamento` | varchar | YES |  |
| 21 | `codigo_cargo` | varchar | YES |  |
| 22 | `nombre_cargo` | varchar | YES |  |
| 23 | `codigo_cargo_generico` | varchar | YES |  |
| 24 | `nombre_cargo_generico` | varchar | YES |  |
| 25 | `email` | varchar | YES |  |
| 26 | `codigo_departamento_trabajo` | varchar | YES |  |
| 27 | `nombre_departamento_trabajo` | varchar | YES |  |
| 28 | `codigo_ciudad_trabajo` | varchar | YES |  |
| 29 | `nombre_ciudad_trabajo` | varchar | YES |  |
| 30 | `codigo_cargo_junta` | varchar | YES |  |
| 31 | `nombre_cargo_junta` | varchar | YES |  |
| 32 | `codigo_tipo_contrato` | varchar | YES |  |
| 33 | `nombre_tipo_contrato` | varchar | YES |  |
| 34 | `unidad_negocio` | varchar | YES |  |
| 35 | `nombre_unidad_negocio` | varchar | YES |  |
| 36 | `fecha_nacimiento` | timestamp(3) | YES |  |
| 37 | `genero` | varchar | YES |  |
| 38 | `indicador_salario_variable` | smallint | YES |  |
| 39 | `indicador_comisiones` | varchar | YES |  |
| 40 | `prefijo_cuenta_contable` | varchar | YES |  |
| 41 | `codigo_cno` | varchar | YES |  |
| 42 | `codigo_clase_salario` | smallint | YES |  |
| 43 | `nombre_clase_salario` | varchar | YES |  |
| 44 | `email_corporativo` | varchar | YES |  |
| 45 | `celular` | varchar | YES |  |
| 46 | `telefono_fijo` | varchar | YES |  |
| 47 | `estado` | varchar | YES |  |
| 48 | `documento` | varchar | YES |  |

### stage.vw_financiacionesventas_vnvo_dep

**Columnas:** 43

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `idcentros` | bigint | YES |  |
| 8 | `a�oexpediente` | varchar | YES |  |
| 9 | `serieexpediente` | varchar | YES |  |
| 10 | `numexpediente` | bigint | YES |  |
| 11 | `idofertapagos` | bigint | YES |  |
| 12 | `saldofavorcliente` | bigint | YES |  |
| 13 | `importefinanciado` | double | YES |  |
| 14 | `fechavencimiento` | timestamp(3) | YES |  |
| 15 | `fechainicio` | timestamp(3) | YES |  |
| 16 | `comisionfinanciera` | double | YES |  |
| 17 | `vin` | varchar | YES |  |
| 18 | `matricula` | varchar | YES |  |
| 19 | `comisionvehiculo` | varchar | YES |  |
| 20 | `idterceros` | bigint | YES |  |
| 21 | `nombrepropietario` | varchar | YES |  |
| 22 | `nifcifpropietario` | varchar | YES |  |
| 23 | `idtercerosfinanciera` | bigint | YES |  |
| 24 | `nombrefinanciera` | varchar | YES |  |
| 25 | `idempleados` | bigint | YES |  |
| 26 | `nombreempleado` | varchar | YES |  |
| 27 | `idtercerosagente` | bigint | YES |  |
| 28 | `nombreagente` | varchar | YES |  |
| 29 | `idmarcas` | bigint | YES |  |
| 30 | `nombremarca` | varchar | YES |  |
| 31 | `idgamas` | bigint | YES |  |
| 32 | `nombregama` | varchar | YES |  |
| 33 | `idempleadosgestor` | bigint | YES |  |
| 34 | `nombregestor` | varchar | YES |  |
| 35 | `fechaventa` | timestamp(3) | YES |  |
| 36 | `nombreempresa` | varchar | YES |  |
| 37 | `nombrecentro` | varchar | YES |  |
| 38 | `idmodulos` | varchar | YES |  |
| 39 | `estado` | varchar | YES |  |
| 40 | `descripcionsecciones` | varchar | YES |  |
| 41 | `fechaentregacliente` | timestamp(3) | YES |  |
| 42 | `load_date` | varchar | YES |  |
| 43 | `rn` | bigint | YES |  |

### stage.vw_financial_requests

**Columnas:** 106

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `financing_entry_id` | varchar | YES |  |
| 2 | `primer-nombre` | varchar | YES |  |
| 3 | `segundo-nombre` | varchar | YES |  |
| 4 | `primer-apellido` | varchar | YES |  |
| 5 | `segundo-apellido` | varchar | YES |  |
| 6 | `email` | varchar | YES |  |
| 7 | `numero-de-celular` | varchar | YES |  |
| 8 | `tipo-de-identificacion` | varchar | YES |  |
| 9 | `numero-de-identificacion` | varchar | YES |  |
| 10 | `fecha-expedicion` | varchar | YES |  |
| 11 | `ciudad-expedicion` | varchar | YES |  |
| 12 | `fecha-nacimiento` | varchar | YES |  |
| 13 | `lugar-de-nacimiento` | varchar | YES |  |
| 14 | `genero` | varchar | YES |  |
| 15 | `estado-civil` | varchar | YES |  |
| 16 | `edad` | varchar | YES |  |
| 17 | `nacionalidad` | varchar | YES |  |
| 18 | `departamento-residencia` | varchar | YES |  |
| 19 | `ciudad-residencia` | varchar | YES |  |
| 20 | `direccion-residencia` | varchar | YES |  |
| 21 | `informacion-adicional` | varchar | YES |  |
| 22 | `antiguedad-residencia` | varchar | YES |  |
| 23 | `telefono-fijo` | varchar | YES |  |
| 24 | `tipo-vivienda` | varchar | YES |  |
| 25 | `estrato` | varchar | YES |  |
| 26 | `marca-vehiculo` | varchar | YES |  |
| 27 | `linea-vehiculo` | varchar | YES |  |
| 28 | `version-vehiculo` | varchar | YES |  |
| 29 | `vitrina` | varchar | YES |  |
| 30 | `valor-vehiculo` | varchar | YES |  |
| 31 | `plazo-financiacion` | varchar | YES |  |
| 32 | `valor-a-financiar` | varchar | YES |  |
| 33 | `ocupacion` | varchar | YES |  |
| 34 | `nivel-educativo` | varchar | YES |  |
| 35 | `profesiones` | varchar | YES |  |
| 36 | `declara-renta` | varchar | YES |  |
| 37 | `nombre-institucion-donde-estudia` | varchar | YES |  |
| 38 | `numero-semestre-programa` | varchar | YES |  |
| 39 | `nombre-empresa` | varchar | YES |  |
| 40 | `actividad-economica` | varchar | YES |  |
| 41 | `ciudad-empresa` | varchar | YES |  |
| 42 | `direccion-empresa` | varchar | YES |  |
| 43 | `telefono-empresa` | varchar | YES |  |
| 44 | `tipo-de-contrato` | varchar | YES |  |
| 45 | `ingresos-mensuales` | varchar | YES |  |
| 46 | `fecha-inicio-trabajo-actual` | varchar | YES |  |
| 47 | `celular-referencia-personal` | varchar | YES |  |
| 48 | `parentesco-referencia-personal` | varchar | YES |  |
| 49 | `correo-referencia-personal` | varchar | YES |  |
| 50 | `direccion-referencia-personal` | varchar | YES |  |
| 51 | `goza-reconocimiento-publico-politico` | varchar | YES |  |
| 52 | `realiza-operaciones-moneda-extranjera` | varchar | YES |  |
| 53 | `residente-fiscal-pais-diferente-colombia` | varchar | YES |  |
| 54 | `basicos-mensuales` | varchar | YES |  |
| 55 | `variables-mensuales` | varchar | YES |  |
| 56 | `otros-ingresos` | varchar | YES |  |
| 57 | `egresos-mensuales` | varchar | YES |  |
| 58 | `personas-a-cargo` | varchar | YES |  |
| 59 | `valor-total-activos` | varchar | YES |  |
| 60 | `valor-total-vehiculos` | varchar | YES |  |
| 61 | `valor-total-pasivos` | varchar | YES |  |
| 62 | `foto-cedula-frontal` | varchar | YES |  |
| 63 | `foto-cedula-posterior` | varchar | YES |  |
| 64 | `anio-vehiculo` | varchar | YES |  |
| 65 | `pais-de-expedicion` | varchar | YES |  |
| 66 | `departamento-de-expedicion` | varchar | YES |  |
| 67 | `pais-de-residencia` | varchar | YES |  |
| 68 | `pais-de-nacimiento` | varchar | YES |  |
| 69 | `departamento-de-nacimiento` | varchar | YES |  |
| 70 | `pais-de-la-empresa` | varchar | YES |  |
| 71 | `departamento-de-la-empresa` | varchar | YES |  |
| 72 | `estado-del-vehiculo` | varchar | YES |  |
| 73 | `tipo-de-servicio-del-vehiculo` | varchar | YES |  |
| 74 | `nombre-referencia-familiar` | varchar | YES |  |
| 75 | `parentesco-referencia-familiar` | varchar | YES |  |
| 76 | `telefono-referencia-familiar` | varchar | YES |  |
| 77 | `asesores` | varchar | YES |  |
| 78 | `relacion-persona-suma-ingresos` | varchar | YES |  |
| 79 | `sumar-ingresos` | varchar | YES |  |
| 80 | `foto-cedula-frontal-parentesco` | varchar | YES |  |
| 81 | `foto-cedula-posterior-parentesco` | varchar | YES |  |
| 82 | `term-conditions-relationship` | varchar | YES |  |
| 83 | `por-concepto-de` | varchar | YES |  |
| 84 | `total-gastos-mensuales` | varchar | YES |  |
| 85 | `numero-de-celular-parentesco` | varchar | YES |  |
| 86 | `tipo-de-identificacion-suma-ingresos` | varchar | YES |  |
| 87 | `numero-de-identificacion-suma-ingresos` | varchar | YES |  |
| 88 | `correo-electronico-suma-ingresos` | varchar | YES |  |
| 89 | `primer-nombre-suma-ingresos` | varchar | YES |  |
| 90 | `segundo-nombre-suma-ingresos` | varchar | YES |  |
| 91 | `primer-apellido-suma-ingresos` | varchar | YES |  |
| 92 | `segundo-apellido-suma-ingresos` | varchar | YES |  |
| 93 | `fecha-de-nacimiento-suma-ingresos` | varchar | YES |  |
| 94 | `edad-suma-ingresos` | varchar | YES |  |
| 95 | `nombre-empresa-suma-ingresos` | varchar | YES |  |
| 96 | `actividad-economica-suma-ingresos` | varchar | YES |  |
| 97 | `direccion-empresa-suma-ingresos` | varchar | YES |  |
| 98 | `telefono-empresa-suma-ingresos` | varchar | YES |  |
| 99 | `fecha-inicio-trabajo-actual-suma-ingresos` | varchar | YES |  |
| 100 | `ingreso-mensual-suma-ingresos` | varchar | YES |  |
| 101 | `otros-ingresos-suma-ingresos` | varchar | YES |  |
| 102 | `grupo-etnico` | varchar | YES |  |
| 103 | `company` | varchar | YES |  |
| 104 | `headquarter` | varchar | YES |  |
| 105 | `fecha_cargue` | varchar | YES |  |
| 106 | `load_date` | varchar | YES |  |

### stage.vw_financing_entry_values

**Columnas:** 5

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `financing_entry_id` | bigint | YES |  |
| 3 | `field_id` | bigint | YES |  |
| 4 | `field_value` | varchar | YES |  |
| 5 | `load_date` | varchar | YES |  |

### stage.vw_informafacturacion_dep

**Columnas:** 127

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `tipo` | varchar | YES |  |
| 7 | `idempresas` | bigint | YES |  |
| 8 | `idcentros` | bigint | YES |  |
| 9 | `a�oot` | varchar | YES |  |
| 10 | `serieot` | varchar | YES |  |
| 11 | `numot` | bigint | YES |  |
| 12 | `numtrabajo` | bigint | YES |  |
| 13 | `idempleadocierre` | bigint | YES |  |
| 14 | `fechaalta` | timestamp(3) | YES |  |
| 15 | `fechacierre` | timestamp(3) | YES |  |
| 16 | `idseriesgarantias` | varchar | YES |  |
| 17 | `numalbaran` | bigint | YES |  |
| 18 | `a�oalbaran` | varchar | YES |  |
| 19 | `numgarantiamarca` | varchar | YES |  |
| 20 | `horasfacturadas` | bigint | YES |  |
| 21 | `importemobruto` | double | YES |  |
| 22 | `descuentomo` | double | YES |  |
| 23 | `importesubbruto` | double | YES |  |
| 24 | `descuentosub` | double | YES |  |
| 25 | `importevarbruto` | double | YES |  |
| 26 | `descuentovar` | double | YES |  |
| 27 | `importepintbruto` | double | YES |  |
| 28 | `descuentopint` | double | YES |  |
| 29 | `importematerialbruto` | double | YES |  |
| 30 | `descuentomaterial` | double | YES |  |
| 31 | `importemoaceptada` | double | YES |  |
| 32 | `importesubaceptada` | double | YES |  |
| 33 | `importevaraceptada` | double | YES |  |
| 34 | `importepintaceptada` | double | YES |  |
| 35 | `importematerialaceptada` | double | YES |  |
| 36 | `idcargotipos` | varchar | YES |  |
| 37 | `idmanoobratipos` | bigint | YES |  |
| 38 | `iddepartamentocargointerno` | varchar | YES |  |
| 39 | `idsecciones` | bigint | YES |  |
| 40 | `idvehiculos` | bigint | YES |  |
| 41 | `matricula` | varchar | YES |  |
| 42 | `vin` | varchar | YES |  |
| 43 | `idmarcas` | bigint | YES |  |
| 44 | `idgamas` | bigint | YES |  |
| 45 | `fechadespacho` | timestamp(3) | YES |  |
| 46 | `nombremarcas` | varchar | YES |  |
| 47 | `nombregamas` | varchar | YES |  |
| 48 | `a�ofactura` | varchar | YES |  |
| 49 | `seriefactura` | varchar | YES |  |
| 50 | `numfactura` | varchar | YES |  |
| 51 | `idtercerofactura` | bigint | YES |  |
| 52 | `nombretercero` | varchar | YES |  |
| 53 | `idterceroaux` | bigint | YES |  |
| 54 | `nombreterceroaux` | varchar | YES |  |
| 55 | `idpagoformatipos` | varchar | YES |  |
| 56 | `idpagoformas` | varchar | YES |  |
| 57 | `descripcionpagoformas` | varchar | YES |  |
| 58 | `descripcionpagoformatipos` | varchar | YES |  |
| 59 | `fechafactura` | timestamp(3) | YES |  |
| 60 | `tipopago` | varchar | YES |  |
| 61 | `costesub` | double | YES |  |
| 62 | `costemo` | double | YES |  |
| 63 | `costemochapa` | double | YES |  |
| 64 | `costemopintura` | double | YES |  |
| 65 | `costemoresto` | varchar | YES |  |
| 66 | `costemat` | double | YES |  |
| 67 | `importetasasmat` | double | YES |  |
| 68 | `diasreparacion` | bigint | YES |  |
| 69 | `costepint` | double | YES |  |
| 70 | `importemochapa` | double | YES |  |
| 71 | `importemopintura` | double | YES |  |
| 72 | `importemoresto` | varchar | YES |  |
| 73 | `idtallerpagotipos` | varchar | YES |  |
| 74 | `descripciontallerpagotipos` | varchar | YES |  |
| 75 | `idempleados` | bigint | YES |  |
| 76 | `descripcionrecepciontipos` | varchar | YES |  |
| 77 | `kmts` | bigint | YES |  |
| 78 | `a�omodelo` | varchar | YES |  |
| 79 | `idterceropropietario` | bigint | YES |  |
| 80 | `descripciontrabajo` | varchar | YES |  |
| 81 | `diasabierto` | double | YES |  |
| 82 | `numeroautorizacion` | varchar | YES |  |
| 83 | `numsiniestro` | varchar | YES |  |
| 84 | `fechaentrega` | timestamp(3) | YES |  |
| 85 | `idtercerocargo` | bigint | YES |  |
| 86 | `nombretercerocargo` | varchar | YES |  |
| 87 | `idseccioncargos` | varchar | YES |  |
| 88 | `idimputaciontipos` | bigint | YES |  |
| 89 | `idseccioncargointerno` | bigint | YES |  |
| 90 | `idcentrosdestino` | bigint | YES |  |
| 91 | `trabajorepetido` | bigint | YES |  |
| 92 | `a�opresupuesto` | varchar | YES |  |
| 93 | `seriepresupuesto` | varchar | YES |  |
| 94 | `idpresupuesto` | bigint | YES |  |
| 95 | `descripcionseccioncargos` | varchar | YES |  |
| 96 | `idempleadosrec` | bigint | YES |  |
| 97 | `idempleadosretirada` | bigint | YES |  |
| 98 | `idempleadosresponsable` | bigint | YES |  |
| 99 | `a�opedidosservicios` | varchar | YES |  |
| 100 | `seriepedidosservicios` | varchar | YES |  |
| 101 | `idpedidosservicios` | bigint | YES |  |
| 102 | `idmarcastallercampa�asbastidoresafectados` | bigint | YES |  |
| 103 | `idcampa�as` | varchar | YES |  |
| 104 | `idcampa�avariante` | varchar | YES |  |
| 105 | `idubicaciones` | varchar | YES |  |
| 106 | `reclamadomo` | double | YES |  |
| 107 | `reclamadomat` | double | YES |  |
| 108 | `reclamadosub` | double | YES |  |
| 109 | `reclamadovar` | double | YES |  |
| 110 | `reclamadopint` | double | YES |  |
| 111 | `idcentrosdeferencia` | bigint | YES |  |
| 112 | `ida�ootdeferencia` | varchar | YES |  |
| 113 | `idseriesdeferencia` | varchar | YES |  |
| 114 | `idnumotdeferencia` | bigint | YES |  |
| 115 | `idnumtrabajodeferencia` | bigint | YES |  |
| 116 | `idserviciotipos` | bigint | YES |  |
| 117 | `idgradosaveria` | bigint | YES |  |
| 118 | `idgradoaveriaordentrabajo` | bigint | YES |  |
| 119 | `idtrabajotipos` | varchar | YES |  |
| 120 | `idtrabajotiposmarca` | varchar | YES |  |
| 121 | `sureferencia` | varchar | YES |  |
| 122 | `horasuso` | bigint | YES |  |
| 123 | `fechaaltaot` | timestamp(3) | YES |  |
| 124 | `numfacturaexterna` | varchar | YES |  |
| 125 | `observaciones` | varchar | YES |  |
| 126 | `load_date` | varchar | YES |  |
| 127 | `rn` | bigint | YES |  |

### stage.vw_nebula_financial_requests

**Columnas:** 110

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `financing_entry_id` | varchar | YES |  |
| 2 | `primer-nombre` | varchar | YES |  |
| 3 | `segundo-nombre` | varchar | YES |  |
| 4 | `primer-apellido` | varchar | YES |  |
| 5 | `segundo-apellido` | varchar | YES |  |
| 6 | `email` | varchar | YES |  |
| 7 | `numero-de-celular` | varchar | YES |  |
| 8 | `tipo-de-identificacion` | varchar | YES |  |
| 9 | `numero-de-identificacion` | varchar | YES |  |
| 10 | `fecha-expedicion` | varchar | YES |  |
| 11 | `ciudad-expedicion` | varchar | YES |  |
| 12 | `fecha-nacimiento` | varchar | YES |  |
| 13 | `lugar-de-nacimiento` | varchar | YES |  |
| 14 | `genero` | varchar | YES |  |
| 15 | `estado-civil` | varchar | YES |  |
| 16 | `edad` | varchar | YES |  |
| 17 | `nacionalidad` | varchar | YES |  |
| 18 | `departamento-residencia` | varchar | YES |  |
| 19 | `ciudad-residencia` | varchar | YES |  |
| 20 | `direccion-residencia` | varchar | YES |  |
| 21 | `informacion-adicional` | varchar | YES |  |
| 22 | `antiguedad-residencia` | varchar | YES |  |
| 23 | `telefono-fijo` | varchar | YES |  |
| 24 | `tipo-vivienda` | varchar | YES |  |
| 25 | `estrato` | varchar | YES |  |
| 26 | `marca-vehiculo` | varchar | YES |  |
| 27 | `linea-vehiculo` | varchar | YES |  |
| 28 | `version-vehiculo` | varchar | YES |  |
| 29 | `vitrina` | varchar | YES |  |
| 30 | `valor-vehiculo` | varchar | YES |  |
| 31 | `plazo-financiacion` | varchar | YES |  |
| 32 | `valor-a-financiar` | varchar | YES |  |
| 33 | `ocupacion` | varchar | YES |  |
| 34 | `nivel-educativo` | varchar | YES |  |
| 35 | `profesiones` | varchar | YES |  |
| 36 | `declara-renta` | varchar | YES |  |
| 37 | `nombre-institucion-donde-estudia` | varchar | YES |  |
| 38 | `numero-semestre-programa` | varchar | YES |  |
| 39 | `nombre-empresa` | varchar | YES |  |
| 40 | `actividad-economica` | varchar | YES |  |
| 41 | `ciudad-empresa` | varchar | YES |  |
| 42 | `direccion-empresa` | varchar | YES |  |
| 43 | `telefono-empresa` | varchar | YES |  |
| 44 | `tipo-de-contrato` | varchar | YES |  |
| 45 | `ingresos-mensuales` | varchar | YES |  |
| 46 | `fecha-inicio-trabajo-actual` | varchar | YES |  |
| 47 | `celular-referencia-personal` | varchar | YES |  |
| 48 | `parentesco-referencia-personal` | varchar | YES |  |
| 49 | `correo-referencia-personal` | varchar | YES |  |
| 50 | `direccion-referencia-personal` | varchar | YES |  |
| 51 | `goza-reconocimiento-publico-politico` | varchar | YES |  |
| 52 | `realiza-operaciones-moneda-extranjera` | varchar | YES |  |
| 53 | `residente-fiscal-pais-diferente-colombia` | varchar | YES |  |
| 54 | `basicos-mensuales` | varchar | YES |  |
| 55 | `variables-mensuales` | varchar | YES |  |
| 56 | `otros-ingresos` | varchar | YES |  |
| 57 | `egresos-mensuales` | varchar | YES |  |
| 58 | `personas-a-cargo` | varchar | YES |  |
| 59 | `valor-total-activos` | varchar | YES |  |
| 60 | `valor-total-vehiculos` | varchar | YES |  |
| 61 | `valor-total-pasivos` | varchar | YES |  |
| 62 | `foto-cedula-frontal` | varchar | YES |  |
| 63 | `foto-cedula-posterior` | varchar | YES |  |
| 64 | `anio-vehiculo` | varchar | YES |  |
| 65 | `pais-de-expedicion` | varchar | YES |  |
| 66 | `departamento-de-expedicion` | varchar | YES |  |
| 67 | `pais-de-residencia` | varchar | YES |  |
| 68 | `pais-de-nacimiento` | varchar | YES |  |
| 69 | `departamento-de-nacimiento` | varchar | YES |  |
| 70 | `pais-de-la-empresa` | varchar | YES |  |
| 71 | `departamento-de-la-empresa` | varchar | YES |  |
| 72 | `estado-del-vehiculo` | varchar | YES |  |
| 73 | `tipo-de-servicio-del-vehiculo` | varchar | YES |  |
| 74 | `nombre-referencia-familiar` | varchar | YES |  |
| 75 | `parentesco-referencia-familiar` | varchar | YES |  |
| 76 | `telefono-referencia-familiar` | varchar | YES |  |
| 77 | `asesores` | varchar | YES |  |
| 78 | `relacion-persona-suma-ingresos` | varchar | YES |  |
| 79 | `sumar-ingresos` | varchar | YES |  |
| 80 | `foto-cedula-frontal-parentesco` | varchar | YES |  |
| 81 | `foto-cedula-posterior-parentesco` | varchar | YES |  |
| 82 | `term-conditions-relationship` | varchar | YES |  |
| 83 | `por-concepto-de` | varchar | YES |  |
| 84 | `total-gastos-mensuales` | varchar | YES |  |
| 85 | `numero-de-celular-parentesco` | varchar | YES |  |
| 86 | `tipo-de-identificacion-suma-ingresos` | varchar | YES |  |
| 87 | `numero-de-identificacion-suma-ingresos` | varchar | YES |  |
| 88 | `correo-electronico-suma-ingresos` | varchar | YES |  |
| 89 | `primer-nombre-suma-ingresos` | varchar | YES |  |
| 90 | `segundo-nombre-suma-ingresos` | varchar | YES |  |
| 91 | `primer-apellido-suma-ingresos` | varchar | YES |  |
| 92 | `segundo-apellido-suma-ingresos` | varchar | YES |  |
| 93 | `fecha-de-nacimiento-suma-ingresos` | varchar | YES |  |
| 94 | `edad-suma-ingresos` | varchar | YES |  |
| 95 | `nombre-empresa-suma-ingresos` | varchar | YES |  |
| 96 | `actividad-economica-suma-ingresos` | varchar | YES |  |
| 97 | `direccion-empresa-suma-ingresos` | varchar | YES |  |
| 98 | `telefono-empresa-suma-ingresos` | varchar | YES |  |
| 99 | `fecha-inicio-trabajo-actual-suma-ingresos` | varchar | YES |  |
| 100 | `ingreso-mensual-suma-ingresos` | varchar | YES |  |
| 101 | `otros-ingresos-suma-ingresos` | varchar | YES |  |
| 102 | `grupo-etnico` | varchar | YES |  |
| 103 | `company` | varchar | YES |  |
| 104 | `headquarter` | varchar | YES |  |
| 105 | `fecha_cargue` | varchar | YES |  |
| 106 | `load_date` | varchar | YES |  |
| 107 | `pkterceros` | bigint | YES |  |
| 108 | `nifcif` | varchar | YES |  |
| 109 | `correo` | varchar | YES |  |
| 110 | `numero` | varchar | YES |  |

### stage.vw_nebula_materialized_leads_tracking

**Columnas:** 45

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `lead_id` | bigint | YES |  |
| 3 | `clasification_id` | bigint | YES |  |
| 4 | `clasification_name` | varchar | YES |  |
| 5 | `action_id` | bigint | YES |  |
| 6 | `action_name` | varchar | YES |  |
| 7 | `status_id` | bigint | YES |  |
| 8 | `status_name` | varchar | YES |  |
| 9 | `campaing_id` | bigint | YES |  |
| 10 | `campaing_name` | varchar | YES |  |
| 11 | `medium_id` | bigint | YES |  |
| 12 | `medium_value` | varchar | YES |  |
| 13 | `category_id` | bigint | YES |  |
| 14 | `category_name` | varchar | YES |  |
| 15 | `country_name` | varchar | YES |  |
| 16 | `company_name` | varchar | YES |  |
| 17 | `brand_id` | bigint | YES |  |
| 18 | `brand_name` | varchar | YES |  |
| 19 | `wholesaler` | bigint | YES |  |
| 20 | `adviser_id` | bigint | YES |  |
| 21 | `adviser_name` | varchar | YES |  |
| 22 | `adviser_email` | varchar | YES |  |
| 23 | `adviser_document_type` | varchar | YES |  |
| 24 | `adviser_document_number` | varchar | YES |  |
| 25 | `adviser_business_type_id` | bigint | YES |  |
| 26 | `adviser_business_type` | varchar | YES |  |
| 27 | `concessionaire_id` | bigint | YES |  |
| 28 | `concessionaire_names` | varchar | YES |  |
| 29 | `client_name` | varchar | YES |  |
| 30 | `client_phone` | varchar | YES |  |
| 31 | `client_email` | varchar | YES |  |
| 32 | `client_document_type_name` | varchar | YES |  |
| 33 | `client_document_number` | varchar | YES |  |
| 34 | `model_id` | bigint | YES |  |
| 35 | `model_name` | varchar | YES |  |
| 36 | `model_year` | varchar | YES |  |
| 37 | `license_plate` | varchar | YES |  |
| 38 | `created_at` | timestamp(3) | YES |  |
| 39 | `updated_at` | timestamp(3) | YES |  |
| 40 | `fecha_cargue` | varchar | YES |  |
| 41 | `load_date` | varchar | YES |  |
| 42 | `pkterceros` | bigint | YES |  |
| 43 | `nifcif` | varchar | YES |  |
| 44 | `correo` | varchar | YES |  |
| 45 | `numero` | varchar | YES |  |

### stage.vw_nebula_quotation

**Columnas:** 37

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `ad_lead_id` | bigint | YES |  |
| 3 | `channel` | varchar | YES |  |
| 4 | `quotation_serial` | varchar | YES |  |
| 5 | `quotation_version` | bigint | YES |  |
| 6 | `adviser_id` | bigint | YES |  |
| 7 | `adviser_name` | varchar | YES |  |
| 8 | `adviser_document` | varchar | YES |  |
| 9 | `adviser_email` | varchar | YES |  |
| 10 | `adviser_brand` | varchar | YES |  |
| 11 | `adviser_company` | varchar | YES |  |
| 12 | `adviser_city` | varchar | YES |  |
| 13 | `adviser_country` | varchar | YES |  |
| 14 | `adviser_location` | varchar | YES |  |
| 15 | `adviser_center_id` | varchar | YES |  |
| 16 | `adviser_center_name` | varchar | YES |  |
| 17 | `customer_name` | varchar | YES |  |
| 18 | `customer_document_type` | varchar | YES |  |
| 19 | `customer_document` | varchar | YES |  |
| 20 | `customer_email` | varchar | YES |  |
| 21 | `customer_phone` | varchar | YES |  |
| 22 | `car_model` | varchar | YES |  |
| 23 | `car_version` | varchar | YES |  |
| 24 | `quotation_status` | varchar | YES |  |
| 25 | `quotation_views` | bigint | YES |  |
| 26 | `quotation_created_date` | timestamp(3) | YES |  |
| 27 | `quotation_updated_date` | timestamp(3) | YES |  |
| 28 | `quotation_notification_date` | timestamp(3) | YES |  |
| 29 | `channel_id` | bigint | YES |  |
| 30 | `channel_value` | varchar | YES |  |
| 31 | `medium_id` | bigint | YES |  |
| 32 | `medium_value` | varchar | YES |  |
| 33 | `load_date` | varchar | YES |  |
| 34 | `pkterceros` | bigint | YES |  |
| 35 | `nifcif` | varchar | YES |  |
| 36 | `correo` | varchar | YES |  |
| 37 | `numero` | varchar | YES |  |

### stage.vw_quotation

**Columnas:** 33

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `ad_lead_id` | bigint | YES |  |
| 3 | `channel` | varchar | YES |  |
| 4 | `quotation_serial` | varchar | YES |  |
| 5 | `quotation_version` | bigint | YES |  |
| 6 | `adviser_id` | bigint | YES |  |
| 7 | `adviser_name` | varchar | YES |  |
| 8 | `adviser_document` | varchar | YES |  |
| 9 | `adviser_email` | varchar | YES |  |
| 10 | `adviser_brand` | varchar | YES |  |
| 11 | `adviser_company` | varchar | YES |  |
| 12 | `adviser_city` | varchar | YES |  |
| 13 | `adviser_country` | varchar | YES |  |
| 14 | `adviser_location` | varchar | YES |  |
| 15 | `adviser_center_id` | varchar | YES |  |
| 16 | `adviser_center_name` | varchar | YES |  |
| 17 | `customer_name` | varchar | YES |  |
| 18 | `customer_document_type` | varchar | YES |  |
| 19 | `customer_document` | varchar | YES |  |
| 20 | `customer_email` | varchar | YES |  |
| 21 | `customer_phone` | varchar | YES |  |
| 22 | `car_model` | varchar | YES |  |
| 23 | `car_version` | varchar | YES |  |
| 24 | `quotation_status` | varchar | YES |  |
| 25 | `quotation_views` | bigint | YES |  |
| 26 | `quotation_created_date` | timestamp(3) | YES |  |
| 27 | `quotation_updated_date` | timestamp(3) | YES |  |
| 28 | `quotation_notification_date` | timestamp(3) | YES |  |
| 29 | `channel_id` | bigint | YES |  |
| 30 | `channel_value` | varchar | YES |  |
| 31 | `medium_id` | bigint | YES |  |
| 32 | `medium_value` | varchar | YES |  |
| 33 | `load_date` | varchar | YES |  |

### stage.vw_spiga_nebula

**Columnas:** 132

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `pkterceros` | bigint | YES |  |
| 2 | `nifcif` | varchar | YES |  |
| 3 | `correo` | varchar | YES |  |
| 4 | `numero` | varchar | YES |  |
| 5 | `client_name` | varchar | YES |  |
| 6 | `client_phone` | varchar | YES |  |
| 7 | `client_email` | varchar | YES |  |
| 8 | `lead_created_at` | timestamp(3) | YES |  |
| 9 | `brand_name` | varchar | YES |  |
| 10 | `category_name` | varchar | YES |  |
| 11 | `medium_id` | bigint | YES |  |
| 12 | `medium_value` | varchar | YES |  |
| 13 | `financing_entry_id` | varchar | YES |  |
| 14 | `primer-nombre` | varchar | YES |  |
| 15 | `segundo-nombre` | varchar | YES |  |
| 16 | `primer-apellido` | varchar | YES |  |
| 17 | `segundo-apellido` | varchar | YES |  |
| 18 | `email` | varchar | YES |  |
| 19 | `numero-de-celular` | varchar | YES |  |
| 20 | `tipo-de-identificacion` | varchar | YES |  |
| 21 | `numero-de-identificacion` | varchar | YES |  |
| 22 | `fecha-expedicion` | varchar | YES |  |
| 23 | `ciudad-expedicion` | varchar | YES |  |
| 24 | `fecha-nacimiento` | varchar | YES |  |
| 25 | `lugar-de-nacimiento` | varchar | YES |  |
| 26 | `genero` | varchar | YES |  |
| 27 | `estado-civil` | varchar | YES |  |
| 28 | `edad` | varchar | YES |  |
| 29 | `nacionalidad` | varchar | YES |  |
| 30 | `departamento-residencia` | varchar | YES |  |
| 31 | `ciudad-residencia` | varchar | YES |  |
| 32 | `direccion-residencia` | varchar | YES |  |
| 33 | `informacion-adicional` | varchar | YES |  |
| 34 | `antiguedad-residencia` | varchar | YES |  |
| 35 | `telefono-fijo` | varchar | YES |  |
| 36 | `tipo-vivienda` | varchar | YES |  |
| 37 | `estrato` | varchar | YES |  |
| 38 | `marca-vehiculo` | varchar | YES |  |
| 39 | `linea-vehiculo` | varchar | YES |  |
| 40 | `version-vehiculo` | varchar | YES |  |
| 41 | `vitrina` | varchar | YES |  |
| 42 | `valor-vehiculo` | varchar | YES |  |
| 43 | `plazo-financiacion` | varchar | YES |  |
| 44 | `valor-a-financiar` | varchar | YES |  |
| 45 | `ocupacion` | varchar | YES |  |
| 46 | `nivel-educativo` | varchar | YES |  |
| 47 | `profesiones` | varchar | YES |  |
| 48 | `declara-renta` | varchar | YES |  |
| 49 | `nombre-institucion-donde-estudia` | varchar | YES |  |
| 50 | `numero-semestre-programa` | varchar | YES |  |
| 51 | `nombre-empresa` | varchar | YES |  |
| 52 | `actividad-economica` | varchar | YES |  |
| 53 | `ciudad-empresa` | varchar | YES |  |
| 54 | `direccion-empresa` | varchar | YES |  |
| 55 | `telefono-empresa` | varchar | YES |  |
| 56 | `tipo-de-contrato` | varchar | YES |  |
| 57 | `ingresos-mensuales` | varchar | YES |  |
| 58 | `fecha-inicio-trabajo-actual` | varchar | YES |  |
| 59 | `celular-referencia-personal` | varchar | YES |  |
| 60 | `parentesco-referencia-personal` | varchar | YES |  |
| 61 | `correo-referencia-personal` | varchar | YES |  |
| 62 | `direccion-referencia-personal` | varchar | YES |  |
| 63 | `goza-reconocimiento-publico-politico` | varchar | YES |  |
| 64 | `realiza-operaciones-moneda-extranjera` | varchar | YES |  |
| 65 | `residente-fiscal-pais-diferente-colombia` | varchar | YES |  |
| 66 | `basicos-mensuales` | varchar | YES |  |
| 67 | `variables-mensuales` | varchar | YES |  |
| 68 | `otros-ingresos` | varchar | YES |  |
| 69 | `egresos-mensuales` | varchar | YES |  |
| 70 | `personas-a-cargo` | varchar | YES |  |
| 71 | `valor-total-activos` | varchar | YES |  |
| 72 | `valor-total-vehiculos` | varchar | YES |  |
| 73 | `valor-total-pasivos` | varchar | YES |  |
| 74 | `foto-cedula-frontal` | varchar | YES |  |
| 75 | `foto-cedula-posterior` | varchar | YES |  |
| 76 | `anio-vehiculo` | varchar | YES |  |
| 77 | `pais-de-expedicion` | varchar | YES |  |
| 78 | `departamento-de-expedicion` | varchar | YES |  |
| 79 | `pais-de-residencia` | varchar | YES |  |
| 80 | `pais-de-nacimiento` | varchar | YES |  |
| 81 | `departamento-de-nacimiento` | varchar | YES |  |
| 82 | `pais-de-la-empresa` | varchar | YES |  |
| 83 | `departamento-de-la-empresa` | varchar | YES |  |
| 84 | `estado-del-vehiculo` | varchar | YES |  |
| 85 | `tipo-de-servicio-del-vehiculo` | varchar | YES |  |
| 86 | `nombre-referencia-familiar` | varchar | YES |  |
| 87 | `parentesco-referencia-familiar` | varchar | YES |  |
| 88 | `telefono-referencia-familiar` | varchar | YES |  |
| 89 | `asesores` | varchar | YES |  |
| 90 | `relacion-persona-suma-ingresos` | varchar | YES |  |
| 91 | `sumar-ingresos` | varchar | YES |  |
| 92 | `foto-cedula-frontal-parentesco` | varchar | YES |  |
| 93 | `foto-cedula-posterior-parentesco` | varchar | YES |  |
| 94 | `term-conditions-relationship` | varchar | YES |  |
| 95 | `por-concepto-de` | varchar | YES |  |
| 96 | `total-gastos-mensuales` | varchar | YES |  |
| 97 | `numero-de-celular-parentesco` | varchar | YES |  |
| 98 | `tipo-de-identificacion-suma-ingresos` | varchar | YES |  |
| 99 | `numero-de-identificacion-suma-ingresos` | varchar | YES |  |
| 100 | `correo-electronico-suma-ingresos` | varchar | YES |  |
| 101 | `primer-nombre-suma-ingresos` | varchar | YES |  |
| 102 | `segundo-nombre-suma-ingresos` | varchar | YES |  |
| 103 | `primer-apellido-suma-ingresos` | varchar | YES |  |
| 104 | `segundo-apellido-suma-ingresos` | varchar | YES |  |
| 105 | `fecha-de-nacimiento-suma-ingresos` | varchar | YES |  |
| 106 | `edad-suma-ingresos` | varchar | YES |  |
| 107 | `nombre-empresa-suma-ingresos` | varchar | YES |  |
| 108 | `actividad-economica-suma-ingresos` | varchar | YES |  |
| 109 | `direccion-empresa-suma-ingresos` | varchar | YES |  |
| 110 | `telefono-empresa-suma-ingresos` | varchar | YES |  |
| 111 | `fecha-inicio-trabajo-actual-suma-ingresos` | varchar | YES |  |
| 112 | `ingreso-mensual-suma-ingresos` | varchar | YES |  |
| 113 | `otros-ingresos-suma-ingresos` | varchar | YES |  |
| 114 | `grupo-etnico` | varchar | YES |  |
| 115 | `company` | varchar | YES |  |
| 116 | `headquarter` | varchar | YES |  |
| 117 | `fecha_cargue` | varchar | YES |  |
| 118 | `load_date` | varchar | YES |  |
| 119 | `channel` | varchar | YES |  |
| 120 | `channel_id` | bigint | YES |  |
| 121 | `channel_value` | varchar | YES |  |
| 122 | `quotation_medium_id` | bigint | YES |  |
| 123 | `quotation_medium_value` | varchar | YES |  |
| 124 | `customer_name` | varchar | YES |  |
| 125 | `customer_document_type` | varchar | YES |  |
| 126 | `customer_document` | varchar | YES |  |
| 127 | `customer_email` | varchar | YES |  |
| 128 | `customer_phone` | varchar | YES |  |
| 129 | `car_model` | varchar | YES |  |
| 130 | `car_version` | varchar | YES |  |
| 131 | `quotation_status` | varchar | YES |  |
| 132 | `quotation_created_date` | timestamp(3) | YES |  |

### stage.vw_terceros_consolidado

**Columnas:** 87

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `pkterceros` | integer | YES |  |
| 2 | `fkterceroclases` | integer | YES |  |
| 3 | `fktratamientos` | integer | YES |  |
| 4 | `nifcif` | varchar | YES |  |
| 5 | `nombre` | varchar | YES |  |
| 6 | `apellido1` | varchar | YES |  |
| 7 | `apellido2` | varchar | YES |  |
| 8 | `nombre_completo` | varchar | YES |  |
| 9 | `nombrecomercial` | varchar | YES |  |
| 10 | `empresatrabajo` | varchar | YES |  |
| 11 | `fkprofesiones` | smallint | YES |  |
| 12 | `fktercerocargos` | integer | YES |  |
| 13 | `fkterceroformacionniveles` | integer | YES |  |
| 14 | `fechanacimiento` | timestamp(3) | YES |  |
| 15 | `numerohijos` | integer | YES |  |
| 16 | `fecha_alta` | timestamp(3) | YES |  |
| 17 | `fechabaja` | timestamp(3) | YES |  |
| 18 | `usermod` | smallint | YES |  |
| 19 | `fkdocumentaciontipos` | integer | YES |  |
| 20 | `fkestadociviltipos` | varchar | YES |  |
| 21 | `tipodocumento` | varchar | YES |  |
| 22 | `fechamod` | timestamp(3) | YES |  |
| 23 | `sexo` | varchar | YES |  |
| 24 | `fkactividadtipos` | varchar | YES |  |
| 25 | `robinson` | boolean | YES |  |
| 26 | `fknaturalezajuridicatipos` | varchar | YES |  |
| 27 | `tipocontribuyente` | varchar | YES |  |
| 28 | `robinsonant` | boolean | YES |  |
| 29 | `fechamodrobinson` | timestamp(3) | YES |  |
| 30 | `fkcausabajatercero` | smallint | YES |  |
| 31 | `notieneemail` | boolean | YES |  |
| 32 | `centrocoste` | varchar | YES |  |
| 33 | `fknivelesriesgo` | integer | YES |  |
| 34 | `nifcif_fechaexpedicion` | timestamp(3) | YES |  |
| 35 | `nifcif_lugarexpedicion` | varchar | YES |  |
| 36 | `telprincipal` | varchar | YES |  |
| 37 | `extprincipal` | varchar | YES |  |
| 38 | `paistelprincipal` | varchar | YES |  |
| 39 | `telparticular1` | varchar | YES |  |
| 40 | `partext1` | varchar | YES |  |
| 41 | `partpais1` | varchar | YES |  |
| 42 | `telparticular2` | varchar | YES |  |
| 43 | `partext2` | varchar | YES |  |
| 44 | `partpais2` | varchar | YES |  |
| 45 | `celular1` | varchar | YES |  |
| 46 | `celext1` | varchar | YES |  |
| 47 | `celpais1` | varchar | YES |  |
| 48 | `celular2` | varchar | YES |  |
| 49 | `celext2` | varchar | YES |  |
| 50 | `celpais2` | varchar | YES |  |
| 51 | `teltrabajo1` | varchar | YES |  |
| 52 | `traext1` | varchar | YES |  |
| 53 | `trapaises1` | varchar | YES |  |
| 54 | `teltrabajo2` | varchar | YES |  |
| 55 | `traext2` | varchar | YES |  |
| 56 | `trapaises2` | varchar | YES |  |
| 57 | `email_principal` | varchar | YES |  |
| 58 | `email_particular1` | varchar | YES |  |
| 59 | `email_particular2` | varchar | YES |  |
| 60 | `email_facturacion1` | varchar | YES |  |
| 61 | `email_facturacion2` | varchar | YES |  |
| 62 | `email_trabajo1` | varchar | YES |  |
| 63 | `email_trabajo2` | varchar | YES |  |
| 64 | `principalpais` | varchar | YES |  |
| 65 | `ciudadprincipal` | varchar | YES |  |
| 66 | `direccion_principal` | varchar | YES |  |
| 67 | `casadirpais1` | varchar | YES |  |
| 68 | `ciudadcasa1` | varchar | YES |  |
| 69 | `direccion_casa1` | varchar | YES |  |
| 70 | `casadirpais2` | varchar | YES |  |
| 71 | `ciudadcasa2` | varchar | YES |  |
| 72 | `direccion_casa2` | varchar | YES |  |
| 73 | `ofidirpais1` | varchar | YES |  |
| 74 | `ciudadoficina1` | varchar | YES |  |
| 75 | `direccion_oficina1` | varchar | YES |  |
| 76 | `ofidirpais2` | varchar | YES |  |
| 77 | `ciudadoficina2` | varchar | YES |  |
| 78 | `direccion_oficina2` | varchar | YES |  |
| 79 | `otradirpais1` | varchar | YES |  |
| 80 | `ciudadotra1` | varchar | YES |  |
| 81 | `direccion_otra1` | varchar | YES |  |
| 82 | `otradirpais2` | varchar | YES |  |
| 83 | `ciudadotra2` | varchar | YES |  |
| 84 | `direccion_otra2` | varchar | YES |  |
| 85 | `cargo` | varchar | YES |  |
| 86 | `pkterceroformacionniveles_iden` | integer | YES |  |
| 87 | `nivel` | varchar | YES |  |

### stage.vw_traking

**Columnas:** 20

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | varchar | YES |  |
| 2 | `financing_entry_id` | varchar | YES |  |
| 3 | `case_number` | varchar | YES |  |
| 4 | `days_since_creation` | varchar | YES |  |
| 5 | `step_id` | varchar | YES |  |
| 6 | `step_name` | varchar | YES |  |
| 7 | `approved_amount` | varchar | YES |  |
| 8 | `approved_rate` | varchar | YES |  |
| 9 | `approved_terms_months` | varchar | YES |  |
| 10 | `rejection_cause` | varchar | YES |  |
| 11 | `adviser_id` | varchar | YES |  |
| 12 | `adviser_name` | varchar | YES |  |
| 13 | `adviser_email` | varchar | YES |  |
| 14 | `date_time_response` | varchar | YES |  |
| 15 | `financing_entity_id` | varchar | YES |  |
| 16 | `financing_entity_name` | varchar | YES |  |
| 17 | `response_time` | varchar | YES |  |
| 18 | `finished_at` | varchar | YES |  |
| 19 | `created_at` | varchar | YES |  |
| 20 | `load_date` | varchar | YES |  |

### stage.vw_traking_unique

**Columnas:** 20

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `financing_entry_id` | bigint | YES |  |
| 3 | `case_number` | varchar | YES |  |
| 4 | `days_since_creation` | bigint | YES |  |
| 5 | `step_id` | bigint | YES |  |
| 6 | `step_name` | varchar | YES |  |
| 7 | `approved_amount` | double | YES |  |
| 8 | `approved_rate` | double | YES |  |
| 9 | `approved_terms_months` | bigint | YES |  |
| 10 | `rejection_cause` | varchar | YES |  |
| 11 | `adviser_id` | bigint | YES |  |
| 12 | `adviser_name` | varchar | YES |  |
| 13 | `adviser_email` | varchar | YES |  |
| 14 | `date_time_response` | timestamp(3) | YES |  |
| 15 | `financing_entity_id` | bigint | YES |  |
| 16 | `financing_entity_name` | varchar | YES |  |
| 17 | `response_time` | bigint | YES |  |
| 18 | `finished_at` | varchar | YES |  |
| 19 | `created_at` | timestamp(3) | YES |  |
| 20 | `load_date` | varchar | YES |  |

### stage.vw_unidaddenegocio

**Columnas:** 19

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | integer | YES |  |
| 2 | `codempresa` | smallint | YES |  |
| 3 | `nombreempresa` | varchar | YES |  |
| 4 | `codcentro` | smallint | YES |  |
| 5 | `nombrecentro` | varchar | YES |  |
| 6 | `codseccion` | smallint | YES |  |
| 7 | `nombreseccion` | varchar | YES |  |
| 8 | `coddepartamento` | varchar | YES |  |
| 9 | `nombredepartamento` | varchar | YES |  |
| 10 | `codunidadnegocio` | smallint | YES |  |
| 11 | `nombreunidadnegocio` | varchar | YES |  |
| 12 | `unidadnegocio_requisicion` | smallint | YES |  |
| 13 | `nombreunidadnegocio_requisicion` | varchar | YES |  |
| 14 | `sigla` | varchar | YES |  |
| 15 | `division` | varchar | YES |  |
| 16 | `codsedeambiental` | smallint | YES |  |
| 17 | `sedeambiental` | varchar | YES |  |
| 18 | `codsededistcol` | varchar | YES |  |
| 19 | `sededistribucioncolision` | varchar | YES |  |

### stage.vw_vehiculos_entregados_dep

**Columnas:** 34

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idsincronizacionspiga` | bigint | YES |  |
| 2 | `idconsecutivo` | bigint | YES |  |
| 3 | `ano_periodo` | bigint | YES |  |
| 4 | `mes_periodo` | bigint | YES |  |
| 5 | `fechadecorte` | timestamp(3) | YES |  |
| 6 | `idempresas` | bigint | YES |  |
| 7 | `a�o` | bigint | YES |  |
| 8 | `mes` | bigint | YES |  |
| 9 | `codigoempresa` | bigint | YES |  |
| 10 | `empresa` | varchar | YES |  |
| 11 | `codigocentro` | bigint | YES |  |
| 12 | `centro` | varchar | YES |  |
| 13 | `codigoseccion` | bigint | YES |  |
| 14 | `seccion` | varchar | YES |  |
| 15 | `codigomarca` | bigint | YES |  |
| 16 | `marca` | varchar | YES |  |
| 17 | `codigogama` | bigint | YES |  |
| 18 | `gama` | varchar | YES |  |
| 19 | `codigomodelo` | varchar | YES |  |
| 20 | `a�omodelo` | varchar | YES |  |
| 21 | `modelo` | varchar | YES |  |
| 22 | `cedulavendedor` | varchar | YES |  |
| 23 | `nombrevendedor` | varchar | YES |  |
| 24 | `nit` | varchar | YES |  |
| 25 | `nombretercero` | varchar | YES |  |
| 26 | `cantidad` | bigint | YES |  |
| 27 | `valor` | double | YES |  |
| 28 | `tipo` | varchar | YES |  |
| 29 | `fechaentregacliente` | timestamp(3) | YES |  |
| 30 | `fechamod` | timestamp(3) | YES |  |
| 31 | `vin` | varchar | YES |  |
| 32 | `fechafactura` | timestamp(3) | YES |  |
| 33 | `load_date` | varchar | YES |  |
| 34 | `rn` | bigint | YES |  |

## 🥉 taris_db

`Capa: Bronce / Raw`

### taris_db.view_termometro_experiencia

**Columnas:** 25

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idmes` | bigint | YES |  |
| 2 | `a�o` | integer | YES |  |
| 3 | `mes` | varchar | YES |  |
| 4 | `nombrecliente` | varchar | YES |  |
| 5 | `cedulacliente` | varchar | YES |  |
| 6 | `ciudad` | varchar | YES |  |
| 7 | `sede` | varchar | YES |  |
| 8 | `idsede` | varchar | YES |  |
| 9 | `linea` | varchar | YES |  |
| 10 | `idlinea` | bigint | YES |  |
| 11 | `idcompa�ia` | varchar | YES |  |
| 12 | `compa�ia` | varchar | YES |  |
| 13 | `area` | varchar | YES |  |
| 14 | `idarea` | bigint | YES |  |
| 15 | `descripciontrabajo` | varchar | YES |  |
| 16 | `nombreasesorspiga` | varchar | YES |  |
| 17 | `asesor` | varchar | YES |  |
| 18 | `documentoasesor` | varchar | YES |  |
| 19 | `fechacreacioncaso` | timestamp(3) | YES |  |
| 20 | `satisfaccion_general_1_10` | varchar | YES |  |
| 21 | `probabilidad_recomendacion_nps` | varchar | YES |  |
| 22 | `retorno_por_garantia` | varchar | YES |  |
| 23 | `cumplimiento_fecha_entrega` | varchar | YES |  |
| 24 | `probabilidad_volver_taller` | varchar | YES |  |
| 25 | `motivo_calificacion` | varchar | YES |  |

### taris_db.vw_atenea_contactabilidad

**Columnas:** 19

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id_mes` | integer | YES |  |
| 2 | `a�o` | integer | YES |  |
| 3 | `linea` | varchar | YES |  |
| 4 | `idlinea` | decimal(20,0) | YES |  |
| 5 | `sede` | varchar | YES |  |
| 6 | `idsede` | decimal(20,0) | YES |  |
| 7 | `idcompa�ia` | varchar | YES |  |
| 8 | `compa�ia` | varchar | YES |  |
| 9 | `area` | varchar | YES |  |
| 10 | `idarea` | decimal(20,0) | YES |  |
| 11 | `mes` | varchar | YES |  |
| 12 | `contactabilidad` | varchar | YES |  |
| 13 | `idcontactabilidad` | integer | YES |  |
| 14 | `total` | decimal(23,0) | YES |  |
| 15 | `basescargadas` | bigint | YES |  |
| 16 | `porcentaje` | varchar | YES |  |
| 17 | `case_created_at` | timestamp(3) | YES |  |
| 18 | `fecha_actualizacion` | timestamp(3) | YES |  |
| 19 | `origen_db` | varchar | YES |  |

### taris_db.vw_atenea_contactabilidad_detalle

**Columnas:** 23

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id_mes` | integer | YES |  |
| 2 | `a�o` | integer | YES |  |
| 3 | `linea` | varchar | YES |  |
| 4 | `idlinea` | integer | YES |  |
| 5 | `sede` | varchar | YES |  |
| 6 | `idsede` | integer | YES |  |
| 7 | `compa�ia` | varchar | YES |  |
| 8 | `area` | varchar | YES |  |
| 9 | `idarea` | integer | YES |  |
| 10 | `mes` | varchar | YES |  |
| 11 | `contactabilidad` | varchar | YES |  |
| 12 | `idcontactabilidad` | integer | YES |  |
| 13 | `nombrecliente` | varchar | YES |  |
| 14 | `placa` | varchar | YES |  |
| 15 | `vin` | varchar | YES |  |
| 16 | `cedulacliente` | varchar | YES |  |
| 17 | `telefonocontacto` | varchar | YES |  |
| 18 | `nombreasesor` | varchar | YES |  |
| 19 | `origen_db` | varchar | YES |  |
| 20 | `idcompa�ia` | varchar | YES |  |
| 21 | `nombreasesorspiga` | varchar | YES |  |
| 22 | `documentoasesorspiga` | bigint | YES |  |
| 23 | `fecha_actualizacion` | timestamp(3) | YES |  |

### taris_db.vw_atenea_nps

**Columnas:** 22

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id_mes` | integer | YES |  |
| 2 | `a�o` | integer | YES |  |
| 3 | `mes` | varchar | YES |  |
| 4 | `sede` | varchar | YES |  |
| 5 | `idsede` | decimal(20,0) | YES |  |
| 6 | `linea` | varchar | YES |  |
| 7 | `idlinea` | decimal(20,0) | YES |  |
| 8 | `id_compa�ia` | bigint | YES |  |
| 9 | `area` | varchar | YES |  |
| 10 | `idarea` | decimal(20,0) | YES |  |
| 11 | `promotores` | decimal(23,0) | YES |  |
| 12 | `neutros` | decimal(23,0) | YES |  |
| 13 | `detractores` | decimal(23,0) | YES |  |
| 14 | `total` | decimal(23,0) | YES |  |
| 15 | `porcentajepromotor` | varchar | YES |  |
| 16 | `porcentajeneutros` | varchar | YES |  |
| 17 | `porcentajedetractores` | varchar | YES |  |
| 18 | `npstotal` | varchar | YES |  |
| 19 | `meta` | varchar | YES |  |
| 20 | `compa�ia` | varchar | YES |  |
| 21 | `fecha_actualizacion` | timestamp(3) | YES |  |
| 22 | `origen_db` | varchar | YES |  |

### taris_db.vw_atenea_nps_detalle

**Columnas:** 45

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idmes` | integer | YES |  |
| 2 | `a�o` | integer | YES |  |
| 3 | `mes` | varchar | YES |  |
| 4 | `nombrecliente` | varchar | YES |  |
| 5 | `cedulacliente` | varchar | YES |  |
| 6 | `numerocelular` | varchar | YES |  |
| 7 | `telefono` | varchar | YES |  |
| 8 | `telefono2` | varchar | YES |  |
| 9 | `ciudad` | varchar | YES |  |
| 10 | `email` | varchar | YES |  |
| 11 | `sede` | varchar | YES |  |
| 12 | `idsede` | decimal(20,0) | YES |  |
| 13 | `linea` | varchar | YES |  |
| 14 | `idlinea` | decimal(20,0) | YES |  |
| 15 | `compa�ia` | varchar | YES |  |
| 16 | `idcompa�ia` | varchar | YES |  |
| 17 | `marca` | varchar | YES |  |
| 18 | `area` | varchar | YES |  |
| 19 | `idarea` | decimal(20,0) | YES |  |
| 20 | `placa` | varchar | YES |  |
| 21 | `descripciontrabajo` | varchar | YES |  |
| 22 | `nombreasesorspiga` | varchar | YES |  |
| 23 | `asesor` | varchar | YES |  |
| 24 | `fechagestion` | timestamp(3) | YES |  |
| 25 | `resultadogestion` | varchar | YES |  |
| 26 | `canal` | varchar | YES |  |
| 27 | `idcanal` | varchar | YES |  |
| 28 | `usuario` | varchar | YES |  |
| 29 | `nombreusuario` | varchar | YES |  |
| 30 | `numerocontactado` | varchar | YES |  |
| 31 | `pregunta` | varchar | YES |  |
| 32 | `respuesta` | varchar | YES |  |
| 33 | `codigocaso` | varchar | YES |  |
| 34 | `tipocaso` | varchar | YES |  |
| 35 | `clasificacioncaso` | varchar | YES |  |
| 36 | `subclasificacioncaso` | varchar | YES |  |
| 37 | `detalle` | varchar | YES |  |
| 38 | `descripci�n` | varchar | YES |  |
| 39 | `fechacreacioncaso` | timestamp(3) | YES |  |
| 40 | `fechavencimientocaso` | varchar | YES |  |
| 41 | `fechacierrecaso` | timestamp(3) | YES |  |
| 42 | `responsablecaso` | varchar | YES |  |
| 43 | `fecha_actualizacion` | timestamp(3) | YES |  |
| 44 | `origen_db` | varchar | YES |  |
| 45 | `descripcion` | varchar | YES |  |

### taris_db.vw_atenea_ordenes_asesores_total

**Columnas:** 15

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `advisername` | varchar | YES |  |
| 2 | `totalasesor` | bigint | YES |  |
| 3 | `id_mes` | integer | YES |  |
| 4 | `mes` | varchar | YES |  |
| 5 | `anio` | integer | YES |  |
| 6 | `idcompa�ia` | varchar | YES |  |
| 7 | `compania` | varchar | YES |  |
| 8 | `linea` | varchar | YES |  |
| 9 | `idlinea` | decimal(20,0) | YES |  |
| 10 | `sede` | varchar | YES |  |
| 11 | `idsede` | varchar | YES |  |
| 12 | `area` | varchar | YES |  |
| 13 | `idarea` | decimal(20,0) | YES |  |
| 14 | `fecha_actualizacion` | timestamp(3) | YES |  |
| 15 | `origen_db` | varchar | YES |  |

### taris_db.vw_atenea_pqr

**Columnas:** 41

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `id_mes` | integer | YES |  |
| 3 | `a�o` | integer | YES |  |
| 4 | `mes` | varchar | YES |  |
| 5 | `idcompa�ia` | varchar | YES |  |
| 6 | `empresa` | varchar | YES |  |
| 7 | `idlinea` | bigint | YES |  |
| 8 | `linea` | varchar | YES |  |
| 9 | `idsede` | bigint | YES |  |
| 10 | `sede` | varchar | YES |  |
| 11 | `proceso` | varchar | YES |  |
| 12 | `identificationnumber` | varchar | YES |  |
| 13 | `nombrecliente` | varchar | YES |  |
| 14 | `placa` | varchar | YES |  |
| 15 | `gamma` | varchar | YES |  |
| 16 | `modelo` | varchar | YES |  |
| 17 | `kilometraje` | varchar | YES |  |
| 18 | `vin` | varchar | YES |  |
| 19 | `marcavehiculo` | varchar | YES |  |
| 20 | `numeromotor` | varchar | YES |  |
| 21 | `telefonocontacto` | varchar | YES |  |
| 22 | `idticket` | bigint | YES |  |
| 23 | `c�digocaso` | varchar | YES |  |
| 24 | `tipocaso` | varchar | YES |  |
| 25 | `clasificacioncaso` | varchar | YES |  |
| 26 | `subclasificacioncaso` | varchar | YES |  |
| 27 | `detalle` | varchar | YES |  |
| 28 | `descripci�n` | varchar | YES |  |
| 29 | `fecharegistro` | timestamp(3) | YES |  |
| 30 | `fecharespuesta` | timestamp(3) | YES |  |
| 31 | `cantidaddiascierre` | integer | YES |  |
| 32 | `cantidaddiastranscurridos` | integer | YES |  |
| 33 | `estado` | varchar | YES |  |
| 34 | `origen` | varchar | YES |  |
| 35 | `subclasificaci�n` | varchar | YES |  |
| 36 | `nombreasesor` | varchar | YES |  |
| 37 | `nombreasesorspiga` | varchar | YES |  |
| 38 | `fecha_actualizacion` | timestamp(3) | YES |  |
| 39 | `origen_db` | varchar | YES |  |
| 40 | `documentoasesorspiga` | bigint | YES |  |
| 41 | `numerofactura` | varchar | YES |  |

### taris_db.vw_atenea_preguntas_detalle

**Columnas:** 45

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idmes` | integer | YES |  |
| 2 | `a�o` | integer | YES |  |
| 3 | `mes` | varchar | YES |  |
| 4 | `nombrecliente` | varchar | YES |  |
| 5 | `cedulacliente` | varchar | YES |  |
| 6 | `numerocelular` | varchar | YES |  |
| 7 | `telefono` | varchar | YES |  |
| 8 | `telefono2` | varchar | YES |  |
| 9 | `ciudad` | varchar | YES |  |
| 10 | `email` | varchar | YES |  |
| 11 | `sede` | varchar | YES |  |
| 12 | `idsede` | decimal(20,0) | YES |  |
| 13 | `linea` | varchar | YES |  |
| 14 | `idlinea` | decimal(20,0) | YES |  |
| 15 | `idcompa�ia` | varchar | YES |  |
| 16 | `compa�ia` | varchar | YES |  |
| 17 | `marca` | varchar | YES |  |
| 18 | `area` | varchar | YES |  |
| 19 | `idarea` | decimal(20,0) | YES |  |
| 20 | `placa` | varchar | YES |  |
| 21 | `descripciontrabajo` | varchar | YES |  |
| 22 | `nombreasesorspiga` | varchar | YES |  |
| 23 | `asesor` | varchar | YES |  |
| 24 | `fechagestion` | timestamp(3) | YES |  |
| 25 | `resultadogestion` | varchar | YES |  |
| 26 | `canal` | varchar | YES |  |
| 27 | `idcanal` | varchar | YES |  |
| 28 | `usuario` | varchar | YES |  |
| 29 | `nombreusuario` | varchar | YES |  |
| 30 | `numerocontactado` | varchar | YES |  |
| 31 | `pregunta` | varchar | YES |  |
| 32 | `respuesta` | varchar | YES |  |
| 33 | `codigocaso` | varchar | YES |  |
| 34 | `tipocaso` | varchar | YES |  |
| 35 | `clasificacioncaso` | varchar | YES |  |
| 36 | `subclasificacioncaso` | varchar | YES |  |
| 37 | `detalle` | varchar | YES |  |
| 38 | `descripci�n` | varchar | YES |  |
| 39 | `fechacreacioncaso` | timestamp(3) | YES |  |
| 40 | `fechavencimientocaso` | varchar | YES |  |
| 41 | `fechacierrecaso` | timestamp(3) | YES |  |
| 42 | `responsablecaso` | varchar | YES |  |
| 43 | `fecha_actualizacion` | timestamp(3) | YES |  |
| 44 | `origen_db` | varchar | YES |  |
| 45 | `descripcion` | varchar | YES |  |

### taris_db.vw_atenea_satisfaccion

**Columnas:** 26

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id_mes` | integer | YES |  |
| 2 | `a�o` | integer | YES |  |
| 3 | `mes` | varchar | YES |  |
| 4 | `sede` | varchar | YES |  |
| 5 | `idsede` | decimal(20,0) | YES |  |
| 6 | `linea` | varchar | YES |  |
| 7 | `idlinea` | decimal(20,0) | YES |  |
| 8 | `area` | varchar | YES |  |
| 9 | `idarea` | decimal(20,0) | YES |  |
| 10 | `encuestasefectivas` | bigint | YES |  |
| 11 | `res_1` | decimal(23,0) | YES |  |
| 12 | `res_2` | decimal(23,0) | YES |  |
| 13 | `res_3` | decimal(23,0) | YES |  |
| 14 | `res_4` | decimal(23,0) | YES |  |
| 15 | `res_5` | decimal(23,0) | YES |  |
| 16 | `res_6` | decimal(23,0) | YES |  |
| 17 | `res_7` | decimal(23,0) | YES |  |
| 18 | `res_8` | decimal(23,0) | YES |  |
| 19 | `res_9` | decimal(23,0) | YES |  |
| 20 | `res_10` | decimal(23,0) | YES |  |
| 21 | `satisfaccion` | varchar | YES |  |
| 22 | `meta` | varchar | YES |  |
| 23 | `idcompa�ia` | varchar | YES |  |
| 24 | `compa�ia` | varchar | YES |  |
| 25 | `fecha_actualizacion` | timestamp(3) | YES |  |
| 26 | `origen_db` | varchar | YES |  |

### taris_db.vw_atenea_satisfaccion_detalle

**Columnas:** 45

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `idmes` | integer | YES |  |
| 2 | `a�o` | integer | YES |  |
| 3 | `mes` | varchar | YES |  |
| 4 | `nombrecliente` | varchar | YES |  |
| 5 | `cedulacliente` | varchar | YES |  |
| 6 | `numerocelular` | varchar | YES |  |
| 7 | `telefono` | varchar | YES |  |
| 8 | `telefono2` | varchar | YES |  |
| 9 | `ciudad` | varchar | YES |  |
| 10 | `email` | varchar | YES |  |
| 11 | `sede` | varchar | YES |  |
| 12 | `idsede` | decimal(20,0) | YES |  |
| 13 | `linea` | varchar | YES |  |
| 14 | `idlinea` | decimal(20,0) | YES |  |
| 15 | `idcompa�ia` | varchar | YES |  |
| 16 | `compa�ia` | varchar | YES |  |
| 17 | `marca` | varchar | YES |  |
| 18 | `area` | varchar | YES |  |
| 19 | `idarea` | decimal(20,0) | YES |  |
| 20 | `placa` | varchar | YES |  |
| 21 | `descripciontrabajo` | varchar | YES |  |
| 22 | `nombreasesorspiga` | varchar | YES |  |
| 23 | `asesor` | varchar | YES |  |
| 24 | `fechagestion` | timestamp(3) | YES |  |
| 25 | `resultadogestion` | varchar | YES |  |
| 26 | `canal` | varchar | YES |  |
| 27 | `idcanal` | varchar | YES |  |
| 28 | `usuario` | varchar | YES |  |
| 29 | `nombreusuario` | varchar | YES |  |
| 30 | `numerocontactado` | varchar | YES |  |
| 31 | `pregunta` | varchar | YES |  |
| 32 | `respuesta` | varchar | YES |  |
| 33 | `codigocaso` | varchar | YES |  |
| 34 | `tipocaso` | varchar | YES |  |
| 35 | `clasificacioncaso` | varchar | YES |  |
| 36 | `subclasificacioncaso` | varchar | YES |  |
| 37 | `detalle` | varchar | YES |  |
| 38 | `descripci�n` | varchar | YES |  |
| 39 | `fechacreacioncaso` | timestamp(3) | YES |  |
| 40 | `fechavencimientocaso` | varchar | YES |  |
| 41 | `fechacierrecaso` | timestamp(3) | YES |  |
| 42 | `responsablecaso` | varchar | YES |  |
| 43 | `fecha_actualizacion` | timestamp(3) | YES |  |
| 44 | `origen_db` | varchar | YES |  |
| 45 | `descripcion` | varchar | YES |  |

## 🥉 tatooine_prod_core

`Capa: Bronce / Raw`

### tatooine_prod_core.materialized_leads_tracking

**Columnas:** 44

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `lead_id` | bigint | YES |  |
| 3 | `clasification_id` | bigint | YES |  |
| 4 | `clasification_name` | varchar | YES |  |
| 5 | `action_id` | bigint | YES |  |
| 6 | `action_name` | varchar | YES |  |
| 7 | `status_id` | bigint | YES |  |
| 8 | `status_name` | varchar | YES |  |
| 9 | `campaing_id` | bigint | YES |  |
| 10 | `campaing_name` | varchar | YES |  |
| 11 | `channel_id` | bigint | YES |  |
| 12 | `channel_value` | varchar | YES |  |
| 13 | `medium_id` | bigint | YES |  |
| 14 | `medium_value` | varchar | YES |  |
| 15 | `category_id` | bigint | YES |  |
| 16 | `category_name` | varchar | YES |  |
| 17 | `country_name` | varchar | YES |  |
| 18 | `company_id` | bigint | YES |  |
| 19 | `company_name` | varchar | YES |  |
| 20 | `brand_id` | bigint | YES |  |
| 21 | `brand_name` | varchar | YES |  |
| 22 | `wholesaler` | smallint | YES |  |
| 23 | `adviser_id` | bigint | YES |  |
| 24 | `adviser_name` | varchar | YES |  |
| 25 | `adviser_email` | varchar | YES |  |
| 26 | `adviser_document_type` | varchar | YES |  |
| 27 | `adviser_document_number` | varchar | YES |  |
| 28 | `concessionaire_id` | bigint | YES |  |
| 29 | `concessionaire_names` | varchar | YES |  |
| 30 | `client_name` | varchar | YES |  |
| 31 | `client_phone` | varchar | YES |  |
| 32 | `client_email` | varchar | YES |  |
| 33 | `client_document_type_name` | varchar | YES |  |
| 34 | `client_document_number` | varchar | YES |  |
| 35 | `model_id` | bigint | YES |  |
| 36 | `model_name` | varchar | YES |  |
| 37 | `model_year` | varchar | YES |  |
| 38 | `license_plate` | varchar | YES |  |
| 39 | `created_at` | timestamp(3) | YES |  |
| 40 | `updated_at` | timestamp(3) | YES |  |
| 41 | `lead_created_at` | timestamp(3) | YES |  |
| 42 | `management_time` | integer | YES |  |
| 43 | `adviser_business_type_id` | bigint | YES |  |
| 44 | `adviser_business_type` | varchar | YES |  |

## 🥉 usados_casatoro_db

`Capa: Bronce / Raw`

### usados_casatoro_db.csu_solicitudes

**Columnas:** 30

| # | Columna | Tipo | Nullable | Comentario |
|---|---------|------|----------|------------|
| 1 | `id` | bigint | YES |  |
| 2 | `created_at` | timestamp(3) | YES |  |
| 3 | `updated_at` | timestamp(3) | YES |  |
| 4 | `brand_id` | bigint | YES |  |
| 5 | `line_id` | bigint | YES |  |
| 6 | `type_vehicle_id` | bigint | YES |  |
| 7 | `parameter_vehicle_id` | bigint | YES |  |
| 8 | `year` | bigint | YES |  |
| 9 | `mileage` | varchar | YES |  |
| 10 | `plate` | varchar | YES |  |
| 11 | `version` | varchar | YES |  |
| 12 | `transmission_id` | bigint | YES |  |
| 13 | `cilindraje` | varchar | YES |  |
| 14 | `nombre_vendedor` | varchar | YES |  |
| 15 | `email_vendedor` | varchar | YES |  |
| 16 | `celular_vendedor` | varchar | YES |  |
| 17 | `hash_user` | varchar | YES |  |
| 18 | `value_quotation` | integer | YES |  |
| 19 | `value_quotation_with_percentage` | integer | YES |  |
| 20 | `note_quotation` | varchar | YES |  |
| 21 | `note_close` | varchar | YES |  |
| 22 | `new_solicitud_id` | integer | YES |  |
| 23 | `scheduling_workshop` | integer | YES |  |
| 24 | `schedule_date` | varchar | YES |  |
| 25 | `schedule_time` | varchar | YES |  |
| 26 | `status` | varchar | YES |  |
| 27 | `origin` | varchar | YES |  |
| 28 | `fds` | smallint | YES |  |
| 29 | `premium` | smallint | YES |  |
| 30 | `acepta_terminos` | varchar | YES |  |

