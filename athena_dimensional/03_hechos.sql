/* =====================================================================================
   ARCHIVO 03 / 04 : TABLA DE HECHOS DEL MODELO ESTRELLA  +  MEDIDAS  (como VISTAS)
   ---------------------------------------------------------------------------------
   Motor        : Amazon Athena (Trino / Presto - engine v3)
   Base destino : gc_leads_mg
   Depende de   : gc_leads_mg.vw_general  y  las dim_* (archivos 01 y 02)
   ---------------------------------------------------------------------------------
   Grano del hecho: 1 fila por lead unificado (lead_id + fuente), tal como queda la
   tabla [General] después del UNION/deduplicación.

   fact_leads se define como VISTA (CREATE OR REPLACE VIEW): no se materializa, se
   recomputa en cada consulta uniendo vw_general contra cada dimensión por su atributo
   natural. Si no hay coincidencia se asigna la clave -1 ('Sin Definir').
   ===================================================================================== */


/* -------------------------------------------------------------------------------------
   FACT LEADS  (vista)
   ------------------------------------------------------------------------------------- */
CREATE OR REPLACE VIEW gc_leads_mg.fact_leads AS
SELECT
    -- ---------- Claves foráneas (surrogate keys) ----------
    COALESCE(df.fecha_key,      CAST(date_format(g.fecha, '%Y%m%d') AS integer)) AS fecha_key,
    COALESCE(dfu.fuente_key,    -1)  AS fuente_key,
    COALESCE(de.estado_key,     -1)  AS estado_key,
    COALESCE(dcmp.campania_key, -1)  AS campania_key,
    COALESCE(dcn.canal_key,     -1)  AS canal_key,
    COALESCE(dcat.categoria_key,-1)  AS categoria_key,
    COALESCE(da.asesor_key,     -1)  AS asesor_key,
    COALESCE(dce.centro_key,    -1)  AS centro_key,

    -- ---------- Clave de negocio (degenerate dimension) ----------
    g.lead_id,

    -- ---------- Atributos operativos que quedan en el hecho ----------
    g.action_name,
    g.tipificacion,
    g.gestion,                       -- [Orbi gestión]  (solo Orbi)
    g.client_name,
    g.client_phone,
    g.client_email,
    g.created_at,
    g.updated_at,
    g.lead_created_at,
    g.nombre_origen,
    g.grupo,
    g.primer_usuario,
    g.primer_grupo,

    -- ---------- Métricas (hechos aditivos / semi-aditivos) ----------
    g.management_time,               -- Orbi: seg | Atom: management_time/60
    g.tiempo_de_contacto,            -- [atom gestión] en minutos (solo Atom)

    -- ---------- Banderas de apoyo para las medidas ----------
    -- Contribuye a [Total Leads sin nuevos]:
    --   Orbi -> status <> 'Nuevo'      Atom -> status = 'Atendido'
    CASE
        WHEN g.fuente = 'Orbi Leads' AND g.status_name <> 'Nuevo'    THEN 1
        WHEN g.fuente = 'Atom'       AND g.status_name = 'Atendido'  THEN 1
        ELSE 0
    END                                                              AS es_gestionado,

    -- ---------- Periodo (AAAA-MM) ----------
    date_format(g.fecha, '%Y-%m')                                    AS anio_mes
FROM gc_leads_mg.vw_general g
LEFT JOIN gc_leads_mg.dim_fecha     df   ON df.fecha         = g.fecha
LEFT JOIN gc_leads_mg.dim_fuente    dfu  ON dfu.fuente       = g.fuente
LEFT JOIN gc_leads_mg.dim_estado    de   ON de.status_name   = g.status_name
LEFT JOIN gc_leads_mg.dim_campania  dcmp ON dcmp.campaing_name = g.campaing_name
LEFT JOIN gc_leads_mg.dim_canal     dcn  ON dcn.medium_value = g.medium_value
LEFT JOIN gc_leads_mg.dim_categoria dcat ON dcat.category_name = g.category_name
LEFT JOIN gc_leads_mg.dim_asesor    da   ON da.adviser_name  = g.adviser_name
                                        AND (da.adviser_email = g.adviser_email
                                             OR (da.adviser_email IS NULL AND g.adviser_email IS NULL))
LEFT JOIN gc_leads_mg.dim_centro    dce  ON dce.centro       = g.centro;


/* =====================================================================================
   MEDIDAS DE NEGOCIO  (equivalen a la tabla [Medidas] del modelo Power BI)
   ---------------------------------------------------------------------------------
   Se exponen como una vista de agregación reutilizable. En Power BI eran:
     Leads                  = DISTINCTCOUNT(General[lead_id])
     Total Leads sin nuevos = (Orbi status<>'Nuevo') + (Atom status='Atendido')  [distinct]
     %Gestionados           = Total Leads sin nuevos / Leads
   ---------------------------------------------------------------------------------
   Esta vista entrega los KPIs por periodo/fuente/centro; ajustar el GROUP BY según
   el nivel de análisis deseado o consumir fact_leads directamente desde Power BI /
   QuickSight y recrear las medidas allí.
   ===================================================================================== */
CREATE OR REPLACE VIEW gc_leads_mg.vw_kpis_leads AS
SELECT
    d.anio,
    d.mes,
    d.nombre_mes,
    fu.fuente,
    ce.centro_normalizado                              AS centro,
    -- Leads = conteo distinto de lead_id
    COUNT(DISTINCT f.lead_id)                          AS leads,
    -- Total Leads sin nuevos = leads distintos marcados como gestionados
    COUNT(DISTINCT CASE WHEN f.es_gestionado = 1 THEN f.lead_id END) AS total_leads_sin_nuevos,
    -- %Gestionados
    CAST(COUNT(DISTINCT CASE WHEN f.es_gestionado = 1 THEN f.lead_id END) AS double)
        / NULLIF(COUNT(DISTINCT f.lead_id), 0)         AS pct_gestionados
FROM gc_leads_mg.fact_leads f
JOIN gc_leads_mg.dim_fecha  d  ON d.fecha_key  = f.fecha_key
JOIN gc_leads_mg.dim_fuente fu ON fu.fuente_key = f.fuente_key
JOIN gc_leads_mg.dim_centro ce ON ce.centro_key = f.centro_key
GROUP BY 1,2,3,4,5;
