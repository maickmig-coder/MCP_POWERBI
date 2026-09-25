/* =====================================================================================
   MIGRACIÓN MODELO SEMÁNTICO "GC - Leads MG"  ->  MODELO DIMENSIONAL EN AMAZON ATHENA
   ---------------------------------------------------------------------------------
   ARCHIVO 01 / 04 : VISTA UNIFICADA (equivalente a la tabla calculada [General])
   ---------------------------------------------------------------------------------
   Motor           : Amazon Athena (Trino / Presto - engine v3)
   Base destino    : gc_leads_mg              (ajustar al database real)
   Origen Orbi     : tatooine_prod_core.materialized_leads_tracking
   Origen Atom     : atom_leads.leads  +  atom_leads.nebula_tiempos_de_agentes
   ---------------------------------------------------------------------------------
   OBJETIVO
   El modelo Power BI construye la tabla [General] como la UNION de dos orígenes
   (Orbi leads y Atom) previamente deduplicados por lead_id. Sobre Atom se aplica un
   criterio de anti-join: un lead de Atom solo entra si su (telefono|mes|anio) y su
   (email|mes|anio) NO existen ya en Orbi. Esta vista replica esa lógica en SQL.

   NOTA SOBRE EL MOTOR
   Athena (Trino) NO admite las funciones estilo Hive year()/month()/date_format()
   dentro de vistas; se usan las funciones nativas de Trino: extract(), date_diff(),
   date_trunc(), try_cast(), split(), transform(), etc.

   NOTA SOBRE "Text.Proper" (Poner en mayúscula cada palabra)
   Trino no tiene función nativa. Se replica inline con:
     array_join(transform(split(lower(col),' '),
                x -> IF(length(x)>0, upper(substr(x,1,1))||substr(x,2), x)), ' ')
   ===================================================================================== */


/* =====================================================================================
   1) SUB-VISTA ORBI  ->  vw_orbi_leads
   Replica la partición M "Orbi leads":
     - Deduplica por lead_id tomando el ÚLTIMO valor por created_at (LAST_VALUE).
     - Join con agregados de fecha_llegada / fecha_primera_gestion / segundos_hasta_gestion.
     - Filtro de marca: brand_name LIKE '%MG%'.
     - Limpieza: trim/lower email, quitar +,-,espacios del teléfono, Proper case.
   ===================================================================================== */
CREATE OR REPLACE VIEW gc_leads_mg.vw_orbi_leads AS
WITH ultima_gestion AS (
    SELECT DISTINCT
           LAST_VALUE(id)                       OVER w AS id,
           LAST_VALUE(clasification_id)         OVER w AS clasification_id,
           LAST_VALUE(clasification_name)       OVER w AS clasification_name,
           LAST_VALUE(action_id)                OVER w AS action_id,
           LAST_VALUE(action_name)              OVER w AS action_name,
           LAST_VALUE(status_id)                OVER w AS status_id,
           LAST_VALUE(status_name)              OVER w AS status_name,
           LAST_VALUE(campaing_id)              OVER w AS campaing_id,
           LAST_VALUE(campaing_name)            OVER w AS campaing_name,
           LAST_VALUE(channel_id)               OVER w AS channel_id,
           LAST_VALUE(channel_value)            OVER w AS channel_value,
           LAST_VALUE(medium_id)                OVER w AS medium_id,
           LAST_VALUE(medium_value)             OVER w AS medium_value,
           LAST_VALUE(category_id)              OVER w AS category_id,
           LAST_VALUE(category_name)            OVER w AS category_name,
           LAST_VALUE(country_name)             OVER w AS country_name,
           LAST_VALUE(company_id)               OVER w AS company_id,
           LAST_VALUE(company_name)             OVER w AS company_name,
           LAST_VALUE(brand_id)                 OVER w AS brand_id,
           LAST_VALUE(brand_name)               OVER w AS brand_name,
           LAST_VALUE(wholesaler)               OVER w AS wholesaler,
           LAST_VALUE(adviser_id)               OVER w AS adviser_id,
           LAST_VALUE(adviser_name)             OVER w AS adviser_name,
           LAST_VALUE(adviser_email)            OVER w AS adviser_email,
           LAST_VALUE(adviser_document_type)    OVER w AS adviser_document_type,
           LAST_VALUE(adviser_document_number)  OVER w AS adviser_document_number,
           LAST_VALUE(concessionaire_id)        OVER w AS concessionaire_id,
           LAST_VALUE(concessionaire_names)     OVER w AS concessionaire_names,
           LAST_VALUE(client_name)              OVER w AS client_name,
           LAST_VALUE(client_phone)             OVER w AS client_phone,
           LAST_VALUE(client_email)             OVER w AS client_email,
           LAST_VALUE(client_document_type_name)OVER w AS client_document_type_name,
           LAST_VALUE(client_document_number)   OVER w AS client_document_number,
           LAST_VALUE(model_id)                 OVER w AS model_id,
           LAST_VALUE(model_name)               OVER w AS model_name,
           LAST_VALUE(model_year)               OVER w AS model_year,
           LAST_VALUE(license_plate)            OVER w AS license_plate,
           LAST_VALUE(created_at)               OVER w AS created_at,
           LAST_VALUE(updated_at)               OVER w AS updated_at,
           LAST_VALUE(lead_created_at)          OVER w AS lead_created_at,
           LAST_VALUE(management_time)          OVER w AS management_time,
           LAST_VALUE(adviser_business_type_id) OVER w AS adviser_business_type_id,
           LAST_VALUE(adviser_business_type)    OVER w AS adviser_business_type,
           lead_id
    FROM tatooine_prod_core.materialized_leads_tracking
    WINDOW w AS (
        PARTITION BY lead_id
        ORDER BY created_at ASC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    )
),
gestion_agg AS (
    SELECT
        lead_id                                    AS lead_id2,
        MIN(lead_created_at)                       AS fecha_llegada,
        MIN(CASE WHEN status_id <> 1 THEN created_at END) AS fecha_primera_gestion,
        date_diff('second',
                  MIN(lead_created_at),
                  MIN(CASE WHEN status_id <> 1 THEN created_at END)
        )                                          AS segundos_hasta_gestion
    FROM tatooine_prod_core.materialized_leads_tracking
    GROUP BY lead_id
),
base AS (
    SELECT a.*,
           k.fecha_llegada,
           k.fecha_primera_gestion,
           k.segundos_hasta_gestion
    FROM ultima_gestion a
    LEFT JOIN gestion_agg k ON k.lead_id2 = a.lead_id
    WHERE upper(a.brand_name) LIKE '%MG%'
)
SELECT
    id,
    clasification_id, clasification_name,
    action_id, action_name,
    status_id, status_name,
    campaing_id,
    -- Text.Proper(campaing_name)
    array_join(transform(split(lower(campaing_name), ' '),
        x -> IF(length(x) > 0, upper(substr(x,1,1)) || substr(x,2), x)), ' ') AS campaing_name,
    channel_id, channel_value,
    medium_id, medium_value,
    category_id,
    -- Text.Proper(category_name)
    array_join(transform(split(lower(category_name), ' '),
        x -> IF(length(x) > 0, upper(substr(x,1,1)) || substr(x,2), x)), ' ') AS category_name,
    country_name,
    company_id, company_name,
    brand_id, brand_name,
    wholesaler,
    adviser_id,
    -- Text.Proper(adviser_name)
    array_join(transform(split(lower(adviser_name), ' '),
        x -> IF(length(x) > 0, upper(substr(x,1,1)) || substr(x,2), x)), ' ') AS adviser_name,
    lower(trim(adviser_email))                                AS adviser_email,
    adviser_document_type, adviser_document_number,
    concessionaire_id, concessionaire_names,
    client_name,
    -- client_phone: quitar +, -, espacios
    replace(replace(replace(trim(client_phone), '+', ''), '-', ''), ' ', '') AS client_phone,
    -- client_email: trim + lower
    lower(trim(client_email))                                 AS client_email,
    client_document_type_name, client_document_number,
    model_id, model_name, model_year, license_plate,
    created_at, updated_at, lead_created_at,
    management_time,
    adviser_business_type_id, adviser_business_type,
    lead_id,
    -- Fecha = date(lead_created_at)
    CAST(lead_created_at AS date)                             AS fecha,
    fecha_llegada, fecha_primera_gestion, segundos_hasta_gestion,
    -- [Orbi gestión]: DATEDIFF(fecha_llegada, fecha_primera_gestion, MINUTE) > 120
    CASE
        WHEN date_diff('minute', fecha_llegada, fecha_primera_gestion) > 120
            THEN 'Mayor a 2 horas'
        ELSE 'Menor a 2 horas'
    END                                                       AS orbi_gestion
FROM base;


/* =====================================================================================
   2) SUB-VISTA ATOM  ->  vw_atom_leads
   Replica la partición M "Atom":
     - Marca MG mediante join de canal.
     - Deduplica por lead_id con LAST_VALUE por fh_asignacion.
     - Deriva status_name (calculado) y atom_gestion.
   ===================================================================================== */
CREATE OR REPLACE VIEW gc_leads_mg.vw_atom_leads AS
WITH canal_mg AS (
    SELECT DISTINCT canal AS canal2
    FROM atom_leads.leads
    WHERE (upper(nombre_campania) LIKE '%MG%' OR upper(grupo) LIKE '%MG%')
      AND (lower(canal) LIKE '%mg%' OR lower(canal) LIKE '%+%')
),
tiempos AS (
    SELECT DISTINCT
           LAST_VALUE(grupo)                    OVER wa  AS grupo,
           LAST_VALUE(agente)                   OVER wa  AS agente,
           LAST_VALUE(email_agente)             OVER wa  AS email_agente,
           LAST_VALUE(fh_asignacion)            OVER wa  AS fh_asignacion,
           LAST_VALUE(fh_asignacion)            OVER wd  AS fh_asignacion_primera,
           LAST_VALUE(channel_name)             OVER wa  AS channel_name,
           LAST_VALUE(tiempo_de_atencion)       OVER wa  AS tiempo_de_atencion,
           LAST_VALUE(ultima_actualizacion)     OVER wa  AS ultima_actualizacion2,
           LAST_VALUE(atencion)                 OVER wa  AS atencion,
           LAST_VALUE(categoria_atencion)       OVER wa  AS categoria_atencion,
           LAST_VALUE(fh_primer_mensaje_agente) OVER wp  AS fh_primer_mensaje_agente,
           lead_id AS lead_id2
    FROM atom_leads.nebula_tiempos_de_agentes
    WINDOW
        wa AS (PARTITION BY lead_id ORDER BY fh_asignacion ASC  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING),
        wd AS (PARTITION BY lead_id ORDER BY fh_asignacion DESC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING),
        wp AS (PARTITION BY lead_id ORDER BY fh_primer_mensaje_agente DESC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
),
base AS (
    SELECT
        l.lead_id,
        upper(l.nombre_campania)                              AS campaing_name,
        CASE
            WHEN trim(split_part(l.canal, '-', 1)) = 'WA' THEN 'Whatsapp'
            WHEN trim(split_part(l.canal, '-', 1)) = 'IG' THEN 'Redes Sociales'
            WHEN trim(split_part(l.canal, '-', 1)) = 'FB' THEN 'Redes Sociales'
        END                                                   AS medium_value,
        CASE
            WHEN lower(l.customtipodenegocio) = 'taller' THEN 'Posventa'
            WHEN trim(l.customtipodenegocio) = ''        THEN 'Sin definir'
            ELSE l.customtipodenegocio
        END                                                   AS category_name,
        CASE WHEN m.canal2 IS NOT NULL THEN 'MG' ELSE NULL END AS brand_name,
        b.agente                                              AS adviser_name,
        b.email_agente                                        AS adviser_email,
        l.nombre_cliente                                      AS client_name,
        l.telefono                                            AS client_phone,
        l.correo                                              AS client_email,
        b.fh_asignacion                                       AS created_at,
        b.ultima_actualizacion2                               AS updated_at,
        l.fecha_inicio_conversacion                           AS lead_created_at,
        b.tiempo_de_atencion                                  AS management_time,
        l.nombre_origen,
        b.grupo,
        b.atencion,
        l.primer_usuario,
        l.primer_grupo,
        l.tipificacion,
        l.atendido,
        l.ultima_actualizacion,
        l.fecha_asignacion,
        l.asignado,
        l.canal,
        b.fh_primer_mensaje_agente,
        b.fh_asignacion_primera
    FROM atom_leads.leads l
    LEFT JOIN canal_mg m ON m.canal2 = l.canal
    LEFT JOIN tiempos  b ON b.lead_id2 = l.lead_id
    WHERE m.canal2 IS NOT NULL          -- equivale a: where not brand_name is null
)
SELECT
    lead_id,
    -- Text.Proper(campaing_name)
    array_join(transform(split(lower(campaing_name), ' '),
        x -> IF(length(x) > 0, upper(substr(x,1,1)) || substr(x,2), x)), ' ') AS campaing_name,
    medium_value,
    -- Text.Proper(category_name)
    array_join(transform(split(lower(category_name), ' '),
        x -> IF(length(x) > 0, upper(substr(x,1,1)) || substr(x,2), x)), ' ') AS category_name,
    brand_name,
    -- Text.Proper(adviser_name)
    array_join(transform(split(lower(adviser_name), ' '),
        x -> IF(length(x) > 0, upper(substr(x,1,1)) || substr(x,2), x)), ' ') AS adviser_name,
    lower(trim(adviser_email))                                AS adviser_email,
    client_name,
    trim(client_phone)                                        AS client_phone,
    lower(trim(client_email))                                 AS client_email,
    -- created_at: "T" -> " " y cast a timestamp
    try_cast(replace(created_at, 'T', ' ') AS timestamp)      AS created_at,
    updated_at,
    lead_created_at,
    -- management_time: número (en el modelo se divide /60 al unificar)
    try_cast(management_time AS double)                       AS management_time,
    nombre_origen,
    grupo,
    atencion,
    primer_usuario,
    primer_grupo,
    tipificacion,
    atendido,
    ultima_actualizacion,
    fecha_asignacion,
    asignado,
    canal,
    try_cast(replace(fh_primer_mensaje_agente, 'T', ' ') AS timestamp) AS fh_primer_mensaje_agente,
    fh_asignacion_primera,
    CAST(lead_created_at AS date)                             AS fecha,
    -- [status_name] calculado en el modelo Atom
    CASE
        WHEN atendido = '1'                                          THEN 'Atendido'
        WHEN atendido = '0' AND atencion = 'Si'                      THEN 'Atendido'
        WHEN atendido = '0' AND tipificacion = 'No tipificado'       THEN 'No Atendido'
        WHEN atendido IS NULL                                        THEN 'Sin Identificar'
        ELSE 'Atendido'
    END                                                       AS status_name,
    -- [atom gestión]: DATEDIFF(fecha_asignacion, fh_primer_mensaje_agente, MINUTE)
    date_diff('minute',
              try_cast(fecha_asignacion AS timestamp),
              try_cast(replace(fh_primer_mensaje_agente, 'T', ' ') AS timestamp)
    )                                                         AS atom_gestion,
    -- claves de cruce para el criterio de deduplicación contra Orbi
    concat(trim(client_phone), '|',
           cast(extract(month FROM lead_created_at) AS varchar), '|',
           cast(extract(year  FROM lead_created_at) AS varchar)) AS cruce_tel,
    concat(lower(trim(client_email)), '|',
           cast(extract(month FROM lead_created_at) AS varchar), '|',
           cast(extract(year  FROM lead_created_at) AS varchar)) AS cruce_email
FROM base;


/* =====================================================================================
   3) VISTA UNIFICADA  ->  vw_general
   Equivale a la tabla calculada [General] = UNION(Orbi, Atom filtrado por Criterio).
   [Criterio] = "Si" cuando el lead de Atom NO se cruza con Orbi por teléfono NI email
   (dentro del mismo mes/año). Solo esos leads de Atom se unen.
   ===================================================================================== */
CREATE OR REPLACE VIEW gc_leads_mg.vw_general AS
WITH orbi AS (
    SELECT * FROM gc_leads_mg.vw_orbi_leads
),
-- Universo de cruces existentes en Orbi (teléfono|mes|año) y (email|mes|año)
orbi_cruce_tel AS (
    SELECT DISTINCT
           concat(client_phone, '|',
                  cast(extract(month FROM lead_created_at) AS varchar), '|',
                  cast(extract(year  FROM lead_created_at) AS varchar)) AS cruce_tel
    FROM orbi
    WHERE client_phone IS NOT NULL
),
orbi_cruce_email AS (
    SELECT DISTINCT
           concat(client_email, '|',
                  cast(extract(month FROM lead_created_at) AS varchar), '|',
                  cast(extract(year  FROM lead_created_at) AS varchar)) AS cruce_email
    FROM orbi
    WHERE client_email IS NOT NULL
),
atom AS (
    SELECT a.*
    FROM gc_leads_mg.vw_atom_leads a
    LEFT JOIN orbi_cruce_tel   ot ON ot.cruce_tel   = a.cruce_tel
    LEFT JOIN orbi_cruce_email oe ON oe.cruce_email = a.cruce_email
    -- Criterio = "Si": ningún cruce en Orbi ni por teléfono ni por email
    WHERE ot.cruce_tel IS NULL
      AND oe.cruce_email IS NULL
),
orbi_norm AS (
    SELECT
        CAST(lead_id AS varchar)          AS lead_id,
        action_name                       AS action_name,
        orbi_gestion                      AS gestion,
        CAST(NULL AS double)              AS tiempo_de_contacto,
        status_name,
        campaing_name,
        medium_value,
        category_name,
        brand_name,
        concessionaire_names              AS centro,
        action_name                       AS tipificacion,
        adviser_name,
        adviser_email,
        client_name,
        client_phone,
        client_email,
        CAST(created_at AS varchar)       AS created_at,
        CAST(updated_at AS varchar)       AS updated_at,
        lead_created_at,
        management_time,
        CAST(NULL AS varchar)             AS nombre_origen,
        CAST(NULL AS varchar)             AS grupo,
        CAST(NULL AS varchar)             AS primer_usuario,
        CAST(NULL AS varchar)             AS primer_grupo,
        fecha,
        'Orbi Leads'                      AS fuente
    FROM orbi
),
atom_norm AS (
    SELECT
        CAST(lead_id AS varchar)          AS lead_id,
        CAST(NULL AS varchar)             AS action_name,
        CAST(NULL AS varchar)             AS gestion,
        CAST(atom_gestion AS double)      AS tiempo_de_contacto,
        status_name,
        campaing_name,
        medium_value,
        category_name,
        brand_name,
        COALESCE(NULLIF(grupo, ''), 'Sin Definir')          AS centro,
        tipificacion,
        COALESCE(NULLIF(adviser_name, ''), 'Sin Definir')   AS adviser_name,
        adviser_email,
        client_name,
        client_phone,
        client_email,
        CAST(created_at AS varchar)       AS created_at,
        CAST(updated_at AS varchar)       AS updated_at,
        lead_created_at,
        management_time / 60.0            AS management_time,   -- [management_time2] = /60
        nombre_origen,
        grupo,
        primer_usuario,
        primer_grupo,
        fecha,
        'Atom'                            AS fuente
    FROM atom
)
SELECT * FROM orbi_norm
UNION ALL
SELECT * FROM atom_norm;
