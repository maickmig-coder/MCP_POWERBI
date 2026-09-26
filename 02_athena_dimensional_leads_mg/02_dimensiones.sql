/* =====================================================================================
   ARCHIVO 02 / 04 : DIMENSIONES DEL MODELO ESTRELLA  (como VISTAS)
   ---------------------------------------------------------------------------------
   Motor        : Amazon Athena (Trino / Presto - engine v3)
   Base destino : gc_leads_mg
   Depende de   : gc_leads_mg.vw_general  (archivo 01)
   ---------------------------------------------------------------------------------
   Cada dimensión se define como VISTA (CREATE OR REPLACE VIEW). No se materializa
   almacenamiento; las claves surrogadas se generan con row_number() en tiempo de
   consulta. Cada dimensión incluye un miembro "Sin Definir / -1" para preservar la
   integridad referencial de los hechos (evita FKs huérfanas).

   NOTA sobre estabilidad de claves: al ser vistas, las claves surrogadas se
   recalculan en cada consulta. Son estables mientras el conjunto de valores
   distintos no cambie. Si se requiere estabilidad garantizada entre ejecuciones,
   usar un hash determinista del atributo natural (ver README, sección 6).
   ===================================================================================== */


/* -------------------------------------------------------------------------------------
   DIM FECHA  (equivale a la tabla [Calendario] = DISTINCT(General[Fecha]))
   Se genera un calendario contiguo entre la fecha mínima y máxima de los leads.
   Claves: fecha_key = AAAAMMDD (int).
   ------------------------------------------------------------------------------------- */
CREATE OR REPLACE VIEW gc_leads_mg.dim_fecha AS
WITH rango AS (
    SELECT
        COALESCE(MIN(fecha), DATE '2020-01-01') AS fecha_min,
        COALESCE(MAX(fecha), current_date)      AS fecha_max
    FROM gc_leads_mg.vw_general
),
dias AS (
    SELECT s.fecha
    FROM rango r
    CROSS JOIN UNNEST(
        sequence(r.fecha_min, r.fecha_max, INTERVAL '1' DAY)
    ) AS s(fecha)
)
SELECT
    CAST(date_format(fecha, '%Y%m%d') AS integer)             AS fecha_key,
    fecha,
    extract(year  FROM fecha)                                 AS anio,
    extract(month FROM fecha)                                 AS mes,
    CASE extract(month FROM fecha)
        WHEN 1  THEN 'Enero'      WHEN 2  THEN 'Febrero'
        WHEN 3  THEN 'Marzo'      WHEN 4  THEN 'Abril'
        WHEN 5  THEN 'Mayo'       WHEN 6  THEN 'Junio'
        WHEN 7  THEN 'Julio'      WHEN 8  THEN 'Agosto'
        WHEN 9  THEN 'Septiembre' WHEN 10 THEN 'Octubre'
        WHEN 11 THEN 'Noviembre'  WHEN 12 THEN 'Diciembre'
    END                                                       AS nombre_mes,
    extract(day FROM fecha)                                   AS dia,
    date_format(fecha, '%Y-%m')                               AS anio_mes
FROM dias;


/* -------------------------------------------------------------------------------------
   DIM FUENTE  (Orbi Leads / Atom)
   ------------------------------------------------------------------------------------- */
CREATE OR REPLACE VIEW gc_leads_mg.dim_fuente AS
SELECT
    CAST(row_number() OVER (ORDER BY fuente) AS integer) AS fuente_key,
    fuente
FROM (
    SELECT DISTINCT fuente
    FROM gc_leads_mg.vw_general
    WHERE fuente IS NOT NULL
) t;


/* -------------------------------------------------------------------------------------
   DIM ESTADO  (status_name)
   ------------------------------------------------------------------------------------- */
CREATE OR REPLACE VIEW gc_leads_mg.dim_estado AS
SELECT CAST(-1 AS integer) AS estado_key, 'Sin Definir' AS status_name
UNION ALL
SELECT
    CAST(row_number() OVER (ORDER BY status_name) AS integer) AS estado_key,
    status_name
FROM (
    SELECT DISTINCT status_name
    FROM gc_leads_mg.vw_general
    WHERE status_name IS NOT NULL
) t;


/* -------------------------------------------------------------------------------------
   DIM CAMPANIA  (campaing_name)
   ------------------------------------------------------------------------------------- */
CREATE OR REPLACE VIEW gc_leads_mg.dim_campania AS
SELECT CAST(-1 AS integer) AS campania_key, 'Sin Definir' AS campaing_name
UNION ALL
SELECT
    CAST(row_number() OVER (ORDER BY campaing_name) AS integer) AS campania_key,
    campaing_name
FROM (
    SELECT DISTINCT campaing_name
    FROM gc_leads_mg.vw_general
    WHERE campaing_name IS NOT NULL
) t;


/* -------------------------------------------------------------------------------------
   DIM CANAL  (medium_value)
   ------------------------------------------------------------------------------------- */
CREATE OR REPLACE VIEW gc_leads_mg.dim_canal AS
SELECT CAST(-1 AS integer) AS canal_key, 'Sin Definir' AS medium_value
UNION ALL
SELECT
    CAST(row_number() OVER (ORDER BY medium_value) AS integer) AS canal_key,
    medium_value
FROM (
    SELECT DISTINCT medium_value
    FROM gc_leads_mg.vw_general
    WHERE medium_value IS NOT NULL
) t;


/* -------------------------------------------------------------------------------------
   DIM CATEGORIA  (category_name)
   ------------------------------------------------------------------------------------- */
CREATE OR REPLACE VIEW gc_leads_mg.dim_categoria AS
SELECT CAST(-1 AS integer) AS categoria_key, 'Sin Definir' AS category_name
UNION ALL
SELECT
    CAST(row_number() OVER (ORDER BY category_name) AS integer) AS categoria_key,
    category_name
FROM (
    SELECT DISTINCT category_name
    FROM gc_leads_mg.vw_general
    WHERE category_name IS NOT NULL
) t;


/* -------------------------------------------------------------------------------------
   DIM ASESOR  (adviser_name + adviser_email)
   ------------------------------------------------------------------------------------- */
CREATE OR REPLACE VIEW gc_leads_mg.dim_asesor AS
SELECT CAST(-1 AS integer) AS asesor_key, 'Sin Definir' AS adviser_name, CAST(NULL AS varchar) AS adviser_email
UNION ALL
SELECT
    CAST(row_number() OVER (ORDER BY adviser_name, adviser_email) AS integer) AS asesor_key,
    adviser_name,
    adviser_email
FROM (
    SELECT DISTINCT adviser_name, adviser_email
    FROM gc_leads_mg.vw_general
    WHERE adviser_name IS NOT NULL
) t;


/* -------------------------------------------------------------------------------------
   DIM CENTRO  (centro)  + centro_normalizado (SWITCH de salas MG Perú de [centro2])
   ------------------------------------------------------------------------------------- */
CREATE OR REPLACE VIEW gc_leads_mg.dim_centro AS
SELECT CAST(-1 AS integer) AS centro_key, 'Sin Definir' AS centro, 'Sin Definir' AS centro_normalizado
UNION ALL
SELECT
    CAST(row_number() OVER (ORDER BY centro) AS integer) AS centro_key,
    centro,
    CASE centro
        WHEN 'MG Perú Sala Surco'                        THEN 'MGA-Lima-Surco'
        WHEN 'MG Perú Sala Sur Motors - Aviación'        THEN 'Peru - MG Mayorista - Sur Motors - Aviación'
        WHEN 'MG Perú Sala Interamericana Trujillo'      THEN 'Peru - MG Mayorista - Interamericana - Norte Trujillo'
        WHEN 'MG Perú Sala Interamericana Norte - Piura' THEN 'Peru - MG Mayorista - Interamericana Norte - Piura'
        WHEN 'MG Perú Sala Zautos - La Victoria'         THEN 'Peru - MG Mayorista - Zautos - La Victoria'
        WHEN 'MG Perú Sala Satelital - Mall Bellavista'  THEN 'Peru - MG Mayorista - Satelital Mall - Bellavista'
        WHEN 'MG Perú Sala Sur Motors - Dolores'         THEN 'Peru - MG Mayorista - Sur Motors - Dolores'
        WHEN 'MG Perú Sala Interamericana Norte - Chiclayo' THEN 'Peru - MG Mayorista - Interamericana Norte - Chiclayo'
        WHEN 'MG Perú Sala Zual Cars - Huaraz'           THEN 'Peru - MG Mayorista - Zual Cars - Huaraz'
        WHEN 'MG Perú Sala WankaMotors - Huancayo'       THEN 'Peru - MG Mayorista - Wankamotors - Huancayo'
        WHEN 'MG Perú Sala Satelital - Mall Santa Anita' THEN 'Peru - MG Mayorista - Satelital Mall - Santa Anita'
        WHEN 'MG Perú Sala Satelital - Mall Plaza Norte' THEN 'Peru - MG Mayorista - Satelital Mall - Plaza norte'
        WHEN 'MG Perú Sala Autocentro - Tarapoto'        THEN 'Peru - MG Mayorista - Autocentro Tarapoto - Tarapoto'
        WHEN 'MG Perú Sala Zual Cars - Tacna'            THEN 'Peru - MG Mayorista - Zual Cars - Tacna'
        WHEN 'MG Perú Sala Sur Motors - Juliaca'         THEN 'Peru - MG Mayorista - Sur Motors - Juliaca'
        ELSE centro
    END                                                  AS centro_normalizado
FROM (
    SELECT DISTINCT centro
    FROM gc_leads_mg.vw_general
    WHERE centro IS NOT NULL
) t;
