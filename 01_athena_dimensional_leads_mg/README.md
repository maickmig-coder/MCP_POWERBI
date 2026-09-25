# Migración del modelo semántico "GC - Leads MG" a un modelo dimensional en Amazon Athena

Este entregable migra el modelo semántico de Power BI ubicado en `00_ejemplobi/GC - Leads MG.SemanticModel` a un **modelo dimensional (esquema estrella)** implementado íntegramente en **SQL de Amazon Athena (motor Trino / Presto, engine v3)**.

El enfoque tiene dos capas:

1. **Vista unificada** que reproduce la tabla calculada `General` del modelo original (la única tabla visible que alimenta las medidas y el calendario).
2. **Esquema estrella** construido a partir de esa vista: dimensiones + hecho + vista de KPIs.

**Todo el modelo se implementa con vistas** (`CREATE OR REPLACE VIEW`): no se materializa almacenamiento en S3. Las dimensiones, el hecho y los KPIs se recomputan en tiempo de consulta a partir de las vistas de origen.

---

## 1. Estructura de archivos

| Orden | Archivo | Contenido |
|-------|---------|-----------|
| 1 | `01_vista_unificada.sql` | `vw_orbi_leads`, `vw_atom_leads` y `vw_general` (equivalente a `[General]`). |
| 2 | `02_dimensiones.sql` | Vistas `dim_fecha`, `dim_fuente`, `dim_estado`, `dim_campania`, `dim_canal`, `dim_categoria`, `dim_asesor`, `dim_centro`. |
| 3 | `03_hechos.sql` | Vista `fact_leads` (hecho) y vista `vw_kpis_leads` (medidas). |
| — | `README.md` | Este documento. |

> **Antes de ejecutar:** reemplazar el placeholder `gc_leads_mg` por el database real. Al ser todo vistas, no se requieren rutas S3.

---

## 2. Modelo origen (Power BI)

El modelo tenía una tabla visible (`General`) y varias ocultas de apoyo:

- **`Orbi leads`** (Power Query / M): consulta nativa contra `tatooine_prod_core.materialized_leads_tracking`. Deduplica por `lead_id` quedándose con el último registro por `created_at` (`LAST_VALUE ... ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`) y hace un `LEFT JOIN` con un agregado que calcula `fecha_llegada`, `fecha_primera_gestion` y `segundos_hasta_gestion`. Filtro de marca: `brand_name LIKE '%MG%'`.
- **`Atom`** (Power Query / M): consulta contra `atom_leads.leads` + `atom_leads.nebula_tiempos_de_agentes`. Marca los leads MG mediante un join de canal y deduplica por `lead_id` con `LAST_VALUE` por `fh_asignacion`.
- **`General`** (tabla calculada DAX): `UNION` de una proyección de `Orbi leads` y una proyección de `Atom` **filtrada por `Criterio = "Si"`**.
- **`Tel_Orbi` / `Email_Orbi`**: tablas auxiliares que materializan los cruces `telefono|mes|año` y `email|mes|año` presentes en Orbi. Sirven para calcular el `Criterio` de Atom.
- **`Calendario`**: `DISTINCT(General[Fecha])` con `Año`, `Mes`, `NombreMes`, `Día`.
- **`Medidas`**: `Leads`, `Total Leads sin nuevos`, `%Gestionados`.
- Las tablas `LocalDateTable_*` y `DateTableTemplate_*` son las tablas de tiempo automáticas de Power BI: **no se migran** (se sustituyen por `dim_fecha`).

### Criterio de deduplicación entre fuentes

En el modelo, la columna `Atom[Criterio]` es `"Si"` cuando el lead **no** existe ya en Orbi:

```
Cruce_Tel_Orbi   = LOOKUPVALUE(Tel_Orbi[...], Tel_Orbi[Cruce_Tel],   Atom[Cruce_Tel])
Cruce_Email_Orbi = LOOKUPVALUE(Email_Orbi[...], Email_Orbi[Cruce_Email], Atom[Cruce_Email])
Criterio = IF(Cruce_Tel_Orbi = BLANK() && Cruce_Email_Orbi = BLANK(), "Si", "No")
```

En SQL se traduce a un **anti-join** contra el universo de cruces de Orbi (`vw_general`, CTEs `orbi_cruce_tel` / `orbi_cruce_email`). Solo los leads de Atom sin coincidencia por teléfono **ni** por email se unen.

---

## 3. Esquema estrella resultante

```
                         ┌───────────────┐
                         │   dim_fecha   │
                         └───────┬───────┘
                                 │ fecha_key
   ┌────────────┐   ┌────────────┴────────────┐   ┌──────────────┐
   │ dim_fuente │───┤                         ├───│ dim_campania │
   └────────────┘   │                         │   └──────────────┘
   ┌────────────┐   │       fact_leads        │   ┌──────────────┐
   │ dim_estado │───┤   (1 fila por lead      ├───│  dim_canal   │
   └────────────┘   │    unificado)           │   └──────────────┘
   ┌────────────┐   │                         │   ┌──────────────┐
   │ dim_asesor │───┤                         ├───│ dim_categoria│
   └────────────┘   └────────────┬────────────┘   └──────────────┘
                                 │ centro_key
                         ┌───────┴───────┐
                         │  dim_centro   │
                         └───────────────┘
```

### Hecho `fact_leads` (vista)

- **Grano:** un lead unificado (`lead_id` + `fuente`), tal como queda `General` tras el `UNION`.
- **Claves foráneas:** `fecha_key`, `fuente_key`, `estado_key`, `campania_key`, `canal_key`, `categoria_key`, `asesor_key`, `centro_key`. Se resuelven con `LEFT JOIN` contra cada dimensión y `COALESCE(..., -1)` para no dejar FKs huérfanas.
- **Dimensión degenerada:** `lead_id`.
- **Métricas:** `management_time`, `tiempo_de_contacto` (`[atom gestión]` en minutos).
- **Bandera:** `es_gestionado` para reproducir `Total Leads sin nuevos`.
- **Periodo:** columna `anio_mes` (`AAAA-MM`), disponible para filtrar/agrupar.

---

## 4. Mapeo DAX / M → SQL de Athena

| Origen (Power BI) | Destino (Athena / Trino) |
|-------------------|--------------------------|
| `LAST_VALUE(col) OVER (PARTITION BY lead_id ORDER BY created_at ...)` | Idéntico; se usa `WINDOW` con nombre para no repetir el frame. |
| `DATEDIFF(a, b, MINUTE)` | `date_diff('minute', a, b)` |
| `DATEDIFF(a, b, SECOND)` | `date_diff('second', a, b)` |
| `YEAR(x)` / `MONTH(x)` / `DAY(x)` | `extract(year FROM x)` / `extract(month FROM x)` / `extract(day FROM x)` |
| `Text.Proper(col)` (M) | `array_join(transform(split(lower(col),' '), x -> IF(length(x)>0, upper(substr(x,1,1))\|\|substr(x,2), x)), ' ')` |
| `Text.Trim` / `Text.Lower` (M) | `trim(...)` / `lower(...)` |
| `Table.ReplaceValue(...,"+","")` (limpieza de teléfono) | `replace(replace(replace(trim(col),'+',''),'-',''),' ','')` |
| `[Orbi gestión]` (`>120` min) | `CASE WHEN date_diff('minute', fecha_llegada, fecha_primera_gestion) > 120 THEN 'Mayor a 2 horas' ELSE 'Menor a 2 horas' END` |
| `[status_name]` de Atom (IF anidado) | `CASE` sobre `atendido` / `atencion` / `tipificacion`. |
| `[centro2]` (SWITCH de salas) | `CASE centro WHEN ... THEN ... END` en `dim_centro.centro_normalizado`. |
| `[management_time2] = management_time/60` | `management_time / 60.0` en la rama Atom de `vw_general`. |
| `UNION(Orbi, Ato)` (DAX) | `UNION ALL` de `orbi_norm` y `atom_norm`. |
| `Calendario = DISTINCT(General[Fecha])` | `dim_fecha` (calendario contiguo por `sequence`). |

### Medidas

| Medida (DAX) | Equivalente SQL (`vw_kpis_leads`) |
|--------------|-----------------------------------|
| `Leads = DISTINCTCOUNT(General[lead_id])` | `COUNT(DISTINCT lead_id)` |
| `Total Leads sin nuevos` = `(Orbi status<>"Nuevo") + (Atom status="Atendido")` | `COUNT(DISTINCT CASE WHEN es_gestionado = 1 THEN lead_id END)` |
| `%Gestionados = DIVIDE([Total sin nuevos],[Leads])` | `total_leads_sin_nuevos / NULLIF(leads, 0)` |

> `es_gestionado` se calcula en `fact_leads`: `1` si (`fuente = 'Orbi Leads'` y `status_name <> 'Nuevo'`) o (`fuente = 'Atom'` y `status_name = 'Atendido'`).

---

## 5. Orden de ejecución

El orden importa porque las vistas dependen unas de otras (las dimensiones y el hecho leen de `vw_general`, y `vw_kpis_leads` lee del hecho y las dimensiones):

```text
1. CREATE DATABASE IF NOT EXISTS gc_leads_mg;      -- si no existe
2. 01_vista_unificada.sql   -> vw_orbi_leads, vw_atom_leads, vw_general
3. 02_dimensiones.sql       -> dim_* (vistas)
4. 03_hechos.sql            -> fact_leads (vista) y vw_kpis_leads (vista)
```

Todo el modelo se define con `CREATE OR REPLACE VIEW`. No hay materialización: cada consulta a `fact_leads` / `vw_kpis_leads` recomputa los `JOIN` contra las vistas de origen.

### Refresco

Al ser vistas, **no requieren refresco**: siempre reflejan el estado actual de las tablas de origen (`tatooine_prod_core.materialized_leads_tracking`, `atom_leads.*`). Para modificar la lógica basta con volver a ejecutar el `CREATE OR REPLACE VIEW` correspondiente.

### Materializar si se necesita rendimiento

Si el volumen hace lentas las consultas (las vistas reejecutan las window functions y anti-joins cada vez), cualquier vista puede materializarse puntualmente con `CREATE TABLE ... AS SELECT * FROM <vista>` (Parquet/Snappy). En ese caso, tener presente el límite de **100 particiones por CTAS** de Athena si se decide particionar por `anio_mes` ([CTAS en Athena](https://docs.aws.amazon.com/athena/latest/ug/create-table-as.html)) — *contenido reformulado para cumplir con las restricciones de licencia*.

---

## 6. Consideraciones específicas de Athena

- **Motor:** el SQL usa sintaxis Trino (engine v3). Las funciones tipo Hive (`year()`, `month()`, `date_format(date,fmt)` como función Hive) **no** están soportadas dentro de vistas Hive de Athena; por eso se usa `extract()` y `date_format(timestamp, '%Y%m%d')` de Trino.
- **`try_cast`:** en Atom, `created_at` y `fh_primer_mensaje_agente` vienen como texto con `T` (formato ISO). Se limpia con `replace(col,'T',' ')` y se convierte con `try_cast(... AS timestamp)` para tolerar valores nulos/mal formados.
- **Claves surrogadas:** generadas con `row_number()` dentro de cada vista de dimensión. Como son vistas, la clave se recalcula en cada consulta y es estable mientras no cambie el conjunto de valores distintos. Si se requiere una clave estable e independiente del conjunto (p. ej. para SCD o para materializar), sustituir por un hash determinista del atributo natural: `abs(from_big_endian_64(xxhash64(to_utf8(atributo))))`.
- **Tipos de `lead_id`:** en Orbi es entero y en Atom es texto; en `vw_general` ambos se normalizan a `varchar` para poder unirlos.

---

## 7. Validación sugerida

Tras ejecutar los tres archivos, verificar que los conteos cuadran con el modelo Power BI:

```sql
-- Total de leads unificados
SELECT COUNT(DISTINCT lead_id) AS leads FROM gc_leads_mg.fact_leads;

-- Que ninguna FK quedó huérfana salvo el miembro -1 esperado
SELECT
    SUM(CASE WHEN estado_key   = -1 THEN 1 ELSE 0 END) AS estado_sin_match,
    SUM(CASE WHEN campania_key = -1 THEN 1 ELSE 0 END) AS campania_sin_match,
    SUM(CASE WHEN centro_key   = -1 THEN 1 ELSE 0 END) AS centro_sin_match
FROM gc_leads_mg.fact_leads;

-- KPIs por mes/fuente
SELECT * FROM gc_leads_mg.vw_kpis_leads ORDER BY anio, mes, fuente;
```

> Los nombres de columnas de los orígenes (`tatooine_prod_core.materialized_leads_tracking`, `atom_leads.leads`, `atom_leads.nebula_tiempos_de_agentes`) se tomaron **directamente de las consultas nativas** del modelo Power BI. Si algún nombre físico difiere en el data lake actual, ajustarlo en `01_vista_unificada.sql`.
