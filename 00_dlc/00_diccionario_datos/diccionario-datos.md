# Diccionario de datos — Fuentes de los tableros

> diccionario_id: 20261120T144231-diccionario · generado 2026-11-20T14:42:31-05:00 por miguel.b@nebula.com.co · versión 2.4.1
>
> Censos usados: GC - Flotillas (20261113T213106-gc-flotillas), GC - Leads MG (20261120T143932-gc-leads-mg)

La estructura es la **real de la base**, antes de cualquier ajuste de un tablero: si la tabla está en el catálogo de Athena, columnas y tipos salen de ahí; si no (fuente aún no migrada), salen del censo y se marcan «no verificado en catálogo». En una consulta SQL, las columnas son las que devuelve el SQL (según el censo); cada una toma su tipo real de la tabla del catálogo que lee el SQL, o se marca «calculada o renombrada en el SQL». No se registran datos ni contraseñas. Aquí aparecen las tablas que algún tablero censado usa.

**Para tableros nuevos:** el catálogo de Athena tiene además **653 tablas que ningún tablero usa todavía**. No se listan aquí, pero se encuentran con «busca fuente …» y se puede preparar su versión de práctica igual que las demás.

## 1. Conexiones

| Conexión | Tipo de conexión | Servidor / DSN | Tablas | Tableros que la usan |
|---|---|---|---:|---|
| `amazon_athena:Athena_ODBC2` | Amazon Athena (`AmazonAthena.Databases`) | Athena_ODBC2 | 3 | GC - Flotillas, GC - Leads MG |

## 2. Tablas

| Tabla | Conexión | Ruta | Columnas | Estructura tomada de | Tableros que la usan |
|---|---|---|---:|---|---|
| **entregas_totales** | `amazon_athena:Athena_ODBC2` | AwsDataCatalog / bi_materialized_data / entregas_totales | 47 | Catálogo Athena (diccionario-datos.md) | GC - Flotillas |
| **Consulta Orbi leads 7251fe** | `amazon_athena:Athena_ODBC2` | Consulta nativa | 48 | Consulta SQL: columnas del censo; lee del catálogo tatooine_prod_core.materialized_leads_tracking | GC - Leads MG |
| **Consulta Atom c1cfb0** | `amazon_athena:Athena_ODBC2` | Consulta nativa | 27 | Consulta SQL: columnas del censo; lee del catálogo atom_leads.leads, atom_leads.nebula_tiempos_de_agentes | GC - Leads MG |

## 3. Columnas por tabla

### 3.1 entregas_totales

Referencia: `amazon_athena:Athena_ODBC2/AwsDataCatalog/bi_materialized_data/entregas_totales` · versión de práctica `simulacion/Sim_entregas_totales.m` · conexión real `simulacion/Real_entregas_totales.m`

| Columna | Tipo real | Nombre en los tableros | Posible dato personal |
|---|---|---|---|
| `fechadecorte` | timestamp | FechaDeCorte (GC - Flotillas) | — |
| `idempresas` | int | IdEmpresas (GC - Flotillas) | — |
| `año` | int | año (GC - Flotillas) | — |
| `codigoempresa` | int | CodigoEmpresa (GC - Flotillas) | — |
| `empresa` | string | Empresa (GC - Flotillas) | — |
| `codigocentro` | int | CodigoCentro (GC - Flotillas) | — |
| `centro` | string | Centro (GC - Flotillas) | — |
| `codigoseccion` | int | CodigoSeccion (GC - Flotillas) | — |
| `seccion` | string | Seccion (GC - Flotillas) | — |
| `codigomarca` | int | CodigoMarca (GC - Flotillas) | — |
| `marca` | string | Marca (GC - Flotillas) | — |
| `codigogama` | int | CodigoGama (GC - Flotillas) | — |
| `gama` | string | Gama (GC - Flotillas) | — |
| `codigomodelo` | string | CodigoModelo (GC - Flotillas) | — |
| `añomodelo` | string | AñoModelo (GC - Flotillas) | — |
| `modelo` | string | Modelo (GC - Flotillas) | — |
| `cedulavendedor` | string | CedulaVendedor (GC - Flotillas) | Sí (por el nombre) |
| `nombrevendedor` | string | NombreVendedor (GC - Flotillas) | — |
| `nit` | string | Nit (GC - Flotillas, lo cambia a int64) | Sí (por el nombre) |
| `nombretercero` | string | NombreTercero (GC - Flotillas) | Sí (por el nombre) |
| `cantidad` | int | Cantidad (GC - Flotillas) | — |
| `valor` | double | Valor (GC - Flotillas) | — |
| `tipo` | string | tipo (GC - Flotillas) | — |
| `fechaentregacliente` | timestamp | FechaEntregaCliente (GC - Flotillas) | — |
| `fechafactura` | timestamp | FechaFactura (GC - Flotillas) | — |
| `fechamod` | timestamp | FechaMod (GC - Flotillas) | — |
| `vin` | string | VIN (GC - Flotillas) | — |
| `entrega` | string | Entrega (GC - Flotillas) | — |
| `placa` | string | placa (GC - Flotillas) | Sí (por el nombre) |
| `fechamatriculacion` | timestamp | fechamatriculacion (GC - Flotillas) | — |
| `combustible` | string | combustible (GC - Flotillas) | — |
| `procedencia` | string | procedencia (GC - Flotillas) | — |
| `procedenciadetalle` | string | procedenciadetalle (GC - Flotillas) | — |
| `tipooportunidad` | string | tipooportunidad (GC - Flotillas) | — |
| `correo` | string | correo (GC - Flotillas) | Sí (por el nombre) |
| `telefono` | string | quitada en GC - Flotillas | Sí (por el nombre) |
| `codunidadnegocio` | int | codunidadnegocio (GC - Flotillas) | — |
| `nombreunidadnegocio` | string | nombreunidadnegocio (GC - Flotillas) | — |
| `tipocliente` | string | tipocliente (GC - Flotillas) | — |
| `nombrevendedorhomologado` | string | nombrevendedorhomologado (GC - Flotillas) | — |
| `clase` | string | clase (GC - Flotillas) | — |
| `color` | string | color (GC - Flotillas) | — |
| `esultimamodificacion` | int | esultimamodificacion (GC - Flotillas) | — |
| `emailvendedor` | string | emailvendedor (GC - Flotillas) | Sí (por el nombre) |
| `tipoventa_vista` | string | tipoventa_vista (GC - Flotillas) | — |
| `rowhash` | string | rowhash (GC - Flotillas) | — |
| `extractionid` | bigint | extractionid (GC - Flotillas) | — |

Tableros que la usan (sus filtros son reglas de ese tablero; no se heredan sin aprobación):

- **GC - Flotillas** (tabla «Entregas Totales»): filtros de carga: ([Cantidad] = 1); ([tipo] = "Nuevos")

### 3.2 Consulta Orbi leads 7251fe

Referencia: `amazon_athena:Athena_ODBC2/consulta:7251fe3e02` · versión de práctica `simulacion/Sim_Consulta_Orbi_leads_7251fe.m` · conexión real `simulacion/Real_Consulta_Orbi_leads_7251fe.m`

Consulta nativa:

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

| Columna | Tipo real | Nombre en los tableros | Posible dato personal |
|---|---|---|---|
| `id` | bigint | id (GC - Leads MG) | — |
| `clasification_id` | bigint | clasification_id (GC - Leads MG) | — |
| `clasification_name` | string | clasification_name (GC - Leads MG) | — |
| `action_id` | bigint | action_id (GC - Leads MG) | — |
| `action_name` | string | action_name (GC - Leads MG) | — |
| `status_id` | bigint | status_id (GC - Leads MG) | — |
| `status_name` | string | status_name (GC - Leads MG) | — |
| `campaing_id` | bigint | campaing_id (GC - Leads MG) | — |
| `campaing_name` | string | campaing_name (GC - Leads MG) | — |
| `channel_id` | bigint | channel_id (GC - Leads MG) | — |
| `channel_value` | string | channel_value (GC - Leads MG) | — |
| `medium_id` | bigint | medium_id (GC - Leads MG) | — |
| `medium_value` | string | medium_value (GC - Leads MG) | — |
| `category_id` | bigint | category_id (GC - Leads MG) | — |
| `category_name` | string | category_name (GC - Leads MG) | — |
| `country_name` | string | country_name (GC - Leads MG) | — |
| `company_id` | bigint | company_id (GC - Leads MG) | — |
| `company_name` | string | company_name (GC - Leads MG) | — |
| `brand_id` | bigint | brand_id (GC - Leads MG) | — |
| `brand_name` | string | brand_name (GC - Leads MG) | — |
| `wholesaler` | smallint | wholesaler (GC - Leads MG) | — |
| `adviser_id` | bigint | adviser_id (GC - Leads MG) | — |
| `adviser_name` | string | adviser_name (GC - Leads MG) | — |
| `adviser_email` | string | adviser_email (GC - Leads MG) | Sí (por el nombre) |
| `adviser_document_type` | string | adviser_document_type (GC - Leads MG) | — |
| `adviser_document_number` | string | adviser_document_number (GC - Leads MG) | — |
| `concessionaire_id` | bigint | concessionaire_id (GC - Leads MG) | — |
| `concessionaire_names` | string | concessionaire_names (GC - Leads MG) | — |
| `client_name` | string | client_name (GC - Leads MG) | — |
| `client_phone` | string | client_phone (GC - Leads MG) | — |
| `client_email` | string | client_email (GC - Leads MG) | Sí (por el nombre) |
| `client_document_type_name` | string | client_document_type_name (GC - Leads MG) | — |
| `client_document_number` | string | client_document_number (GC - Leads MG) | — |
| `model_id` | bigint | model_id (GC - Leads MG) | — |
| `model_name` | string | model_name (GC - Leads MG) | — |
| `model_year` | string | model_year (GC - Leads MG) | — |
| `license_plate` | string | license_plate (GC - Leads MG) | — |
| `created_at` | timestamp | created_at (GC - Leads MG) | — |
| `updated_at` | timestamp | updated_at (GC - Leads MG) | — |
| `lead_created_at` | timestamp | lead_created_at (GC - Leads MG) | — |
| `management_time` | int | management_time (GC - Leads MG) | — |
| `adviser_business_type_id` | bigint | adviser_business_type_id (GC - Leads MG) | — |
| `adviser_business_type` | string | adviser_business_type (GC - Leads MG) | — |
| `lead_id` | bigint | lead_id (GC - Leads MG) | — |
| `lead_id2` | Calculada o renombrada en el SQL (en el tablero: int64) | lead_id2 (GC - Leads MG) | — |
| `fecha_llegada` | Calculada o renombrada en el SQL (en el tablero: datetime) | fecha_llegada (GC - Leads MG) | — |
| `fecha_primera_gestion` | Calculada o renombrada en el SQL (en el tablero: datetime) | fecha_primera_gestion (GC - Leads MG) | — |
| `segundos_hasta_gestion` | Calculada o renombrada en el SQL (en el tablero: int64) | segundos_hasta_gestion (GC - Leads MG) | — |

Tableros que la usan (sus filtros son reglas de ese tablero; no se heredan sin aprobación):

- **GC - Leads MG** (tabla «Orbi leads»): filtros de carga: sin filtros

### 3.3 Consulta Atom c1cfb0

Referencia: `amazon_athena:Athena_ODBC2/consulta:c1cfb0c4c1` · versión de práctica `simulacion/Sim_Consulta_Atom_c1cfb0.m` · conexión real `simulacion/Real_Consulta_Atom_c1cfb0.m`

Consulta nativa:

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

| Columna | Tipo real | Nombre en los tableros | Posible dato personal |
|---|---|---|---|
| `lead_id` | string | lead_id (GC - Leads MG) | — |
| `campaing_name` | Calculada o renombrada en el SQL (en el tablero: string) | campaing_name (GC - Leads MG) | — |
| `medium_value` | Calculada o renombrada en el SQL (en el tablero: string) | medium_value (GC - Leads MG) | — |
| `category_name` | Calculada o renombrada en el SQL (en el tablero: string) | category_name (GC - Leads MG) | — |
| `brand_name` | Calculada o renombrada en el SQL (en el tablero: string) | brand_name (GC - Leads MG) | — |
| `adviser_name` | Calculada o renombrada en el SQL (en el tablero: string) | adviser_name (GC - Leads MG) | — |
| `adviser_email` | Calculada o renombrada en el SQL (en el tablero: string) | adviser_email (GC - Leads MG) | Sí (por el nombre) |
| `client_name` | Calculada o renombrada en el SQL (en el tablero: string) | client_name (GC - Leads MG) | — |
| `client_phone` | Calculada o renombrada en el SQL (en el tablero: string) | client_phone (GC - Leads MG) | — |
| `client_email` | Calculada o renombrada en el SQL (en el tablero: string) | client_email (GC - Leads MG) | Sí (por el nombre) |
| `created_at` | Calculada o renombrada en el SQL (en el tablero: datetime) | created_at (GC - Leads MG) | — |
| `updated_at` | Calculada o renombrada en el SQL (en el tablero: datetime) | updated_at (GC - Leads MG) | — |
| `lead_created_at` | Calculada o renombrada en el SQL (en el tablero: datetime) | lead_created_at (GC - Leads MG) | — |
| `management_time` | Calculada o renombrada en el SQL (en el tablero: double) | management_time (GC - Leads MG) | — |
| `nombre_origen` | string | nombre_origen (GC - Leads MG) | — |
| `grupo` | string | grupo (GC - Leads MG) | — |
| `primer_usuario` | string | primer_usuario (GC - Leads MG) | — |
| `primer_grupo` | string | primer_grupo (GC - Leads MG) | — |
| `tipificacion` | string | tipificacion (GC - Leads MG) | — |
| `atencion` | string | atencion (GC - Leads MG) | — |
| `atendido` | string | atendido (GC - Leads MG) | — |
| `ultima_actualizacion` | timestamp | ultima_actualizacion (GC - Leads MG) | — |
| `fecha_asignacion` | timestamp | fecha_asignacion (GC - Leads MG) | — |
| `asignado` | string | asignado (GC - Leads MG) | — |
| `canal` | string | canal (GC - Leads MG) | — |
| `fh_primer_mensaje_agente` | timestamp | fh_primer_mensaje_agente (GC - Leads MG) | — |
| `fh_asignacion_primera` | Calculada o renombrada en el SQL (en el tablero: string) | fh_asignacion_primera (GC - Leads MG) | — |

Tableros que la usan (sus filtros son reglas de ese tablero; no se heredan sin aprobación):

- **GC - Leads MG** (tabla «Atom»): filtros de carga: sin filtros

