# Censo BI — GC - Leads MG

> Estado: En revisión
>
> Fecha del censo: 2026-09-25
>
> Versión analizada: Proyecto PBIP — SemanticModel definition v4.2 (compatibilityLevel 1606), Report PBIR
>
> Ritual aplicado: AI-DLC — Ritual estándar para el censo de BI (`00_Censos/00_ai-dlc-censo`), con el ajuste de **Identificación de visuales por título visible**.
>
> Alcance del ritual: descubrimiento y documentación. No se modificó ningún elemento del BI.

---

# 1. Identificación

| Campo | Valor | Estado/Evidencia |
|---|---|---|
| Nombre BI | GC - Leads MG | Encontrado — `01_ejemplobi/GC - Leads MG.pbip`, `displayName` de páginas |
| Proyecto | `GC - Leads MG.pbip` | Encontrado — archivo raíz del proyecto |
| Área | Gestión Comercial (leads marca MG, sector automotriz Perú) | Inferido — nombres de salas "MG Perú Sala ..." en `General[centro2]`, filtro `brand_name like '%MG%'` |
| Objetivo | Monitoreo de captación y gestión de leads de la marca MG | Inferido — KPIs, páginas y campos del reporte |
| Responsable funcional | No identificado | Desconocido — sin evidencia en el proyecto |
| Responsable técnico | No identificado | Desconocido — sin evidencia en el proyecto |
| Tecnología | Power BI (modelo TMDL, reporte PBIR/PBIP) | Encontrado — `definition.pbism` v4.2, `database.tmdl` compatibilityLevel 1606 |
| Repositorio | Repositorio Git local en `c:\dev\NIGGA` | Encontrado — carpeta `.git` en la raíz |
| Ambiente | No identificado (fuente productiva Athena: esquemas `*_prod_*`) | Inferido — `tatooine_prod_core`, DSN `Athena_ODBC2` |
| Versión | SemanticModel v4.2 | Encontrado — `definition.pbism` |
| Fecha del censo | 2026-09-25 | Fecha de ejecución del ritual |

Configuración de modelo (evidencia `model.tmdl`): `culture: es-ES`, `sourceQueryCulture: es-CO`, `defaultPowerBIDataSourceVersion: powerBI_V3`, `valueFilterBehavior: independent`, `__PBI_TimeIntelligenceEnabled = 1`, `PBI_QueryOrder = ["Parametros","Orbi leads","Atom","Medidas"]`, `PBI_ProTooling = ["DevMode"]`.

# 2. Objetivo y alcance

## Objetivo del BI

Consolidar los leads de la marca **MG** provenientes de dos plataformas de captación/atención (**Orbi** y **Atom**), deduplicarlos y medir el volumen de leads y el porcentaje gestionado, con desgloses por tiempo, centro/sala, campaña, medio, categoría, asesor, estado y tipificación.

## Alcance del censo

- Modelo semántico completo (`GC - Leads MG.SemanticModel`): fuentes, transformaciones M, tablas calculadas DAX, columnas, medidas y relaciones.
- Reporte completo (`GC - Leads MG.Report`): 4 páginas y sus visuales (90 contenedores en total), con identificación del título visible de cada uno.

## Limitaciones

- No se ejecutó el modelo ni se validaron datos reales; el análisis proviene exclusivamente de las definiciones TMDL/PBIR versionadas.
- No se accedió a las fuentes Athena (`tatooine_prod_core`, `atom_leads`); su contenido, propietarios y frecuencia de actualización no pueden confirmarse desde el proyecto.
- El significado funcional de algunos estados y clasificaciones se infiere de la lógica técnica y requiere validación con negocio.

# 3. Fuentes de datos

| Fuente | Tipo | Sistema/Esquema | Tabla/Endpoint/Archivo | Método de conexión | Evidencia |
|---|---|---|---|---|---|
| Orbi Leads | Base de datos analítica | `tatooine_prod_core` | `materialized_leads_tracking` | Amazon Athena vía ODBC, `Value.NativeQuery` (EnableFolding) | `Orbi leads.tmdl` partition `m` |
| Atom (leads) | Base de datos analítica | `atom_leads` | `leads` | Amazon Athena vía ODBC, `Value.NativeQuery` | `Atom.tmdl` partition `m` |
| Atom (tiempos) | Base de datos analítica | `atom_leads` | `nebula_tiempos_de_agentes` | `left join` dentro del mismo `NativeQuery` | `Atom.tmdl` partition `m` |
| Parámetro fecha | Cálculo local | — | `DateTimeZone.SwitchZone(DateTimeZone.LocalNow(), -5, 0)` | Power Query (M) | `Parametros.tmdl` |
| Medidas | Tabla vacía contenedora | — | Tabla sin columnas | Power Query (M) | `Medidas.tmdl` |

- DSN de conexión identificado: **`Athena_ODBC2`** (`AmazonAthena.Databases("Athena_ODBC2", null, [])`).
- Filtro de marca aplicado en origen: Orbi `where upper(brand_name) like '%MG%'`; Atom `where not brand_name is null` con marca derivada por join de canal MG.

# 4. Transformaciones

| Elemento | Tecnología | Descripción | Fuente | Destino | Evidencia |
|---|---|---|---|---|---|
| Deduplicación por lead (Orbi) | SQL (Athena) | `LAST_VALUE(...) OVER (PARTITION BY lead_id ORDER BY created_at)` sobre todas las columnas | `materialized_leads_tracking` | `Orbi leads` | `Orbi leads.tmdl` |
| Cálculo de gestión (Orbi) | SQL (Athena) | Subconsulta `GROUP BY lead_id` con `fecha_llegada`, `fecha_primera_gestion` (primer `created_at` con `status_id <> 1`) y `segundos_hasta_gestion` | `materialized_leads_tracking` | `Orbi leads` | `Orbi leads.tmdl` |
| Deduplicación por lead (Atom) | SQL (Athena) | `LAST_VALUE(...) OVER (PARTITION BY lead_id ORDER BY fh_asignacion)`; join de canal MG y última gestión | `atom_leads.leads` + `nebula_tiempos_de_agentes` | `Atom` | `Atom.tmdl` |
| Normalización de canal → medio (Atom) | SQL (Athena) | `CASE` sobre `split_part(canal,'-',1)`: WA→Whatsapp, IG/FB→Redes Sociales | `atom_leads.leads` | `Atom.medium_value` | `Atom.tmdl` |
| Normalización categoría (Atom) | SQL (Athena) | `taller`→`Posventa`, vacío→`Sin definir` | `atom_leads.leads` | `Atom.category_name` | `Atom.tmdl` |
| Limpieza de texto (Orbi/Atom) | Power Query (M) | `Text.Trim`, `Text.Lower` (email), `Text.Proper` (asesor/categoría/campaña), reemplazos en `client_phone` (`+`, `-`, espacio) | Orbi/Atom | Orbi/Atom | `Orbi leads.tmdl`, `Atom.tmdl` |
| Conversión de tipos y `Fecha` | Power Query (M) | Duplicar `lead_created_at` → `Fecha` (tipo date); parseo de `created_at`/`fh_primer_mensaje_agente` (reemplazo `T`→espacio) | Orbi/Atom | Orbi/Atom | `Orbi leads.tmdl`, `Atom.tmdl` |
| `management_time` (Atom) | Power Query (M) | Reemplazo decimal `.`→`,` y cambio a número | Atom | `Atom.management_time` | `Atom.tmdl` |
| Tabla `General` | DAX (tabla calculada) | `UNION` de proyección Orbi + proyección Atom filtrada por `Criterio="Si"` | `Orbi leads`, `Atom` | `General` | `General.tmdl` |
| `Calendario` | DAX (tabla calculada) | `DISTINCT(General[Fecha])` + columnas Año/Mes/NombreMes/Dia | `General` | `Calendario` | `Calendario.tmdl` |
| `Tel_Orbi` / `Email_Orbi` | DAX (tablas calculadas) | `DISTINCT` de teléfono/email + Mes + Año de Orbi (insumo de deduplicación) | `Orbi leads` | `Tel_Orbi`, `Email_Orbi` | `Tel_Orbi.tmdl`, `Email_Orbi.tmdl` |

# 5. Modelo de datos

## Tablas

| Tabla | Tipo/Rol | Granularidad | Visible/Oculta | Descripción | Evidencia |
|---|---|---|---|---|---|
| `General` | Hechos (central) | 1 fila por lead consolidado (Orbi + Atom no duplicado) | Visible | `UNION` de Orbi y Atom; base de todos los visuales | `General.tmdl` |
| `Calendario` | Dimensión fecha | 1 fila por fecha distinta de `General[Fecha]` | Visible | Fechas derivadas de los leads | `Calendario.tmdl` |
| `Medidas` | Contenedor de medidas | Sin filas | Visible | Aloja las 3 medidas del modelo | `Medidas.tmdl` |
| `Parametros` | Parámetro/apoyo | 1 fila (fecha-hora actual, zona -5) | Visible | Usada como "Última Actualización" en tarjetas | `Parametros.tmdl` |
| `Orbi leads` | Staging origen | 1 fila por lead Orbi | Oculta | Query SQL a Athena | `Orbi leads.tmdl` (`isHidden`) |
| `Atom` | Staging origen | 1 fila por lead Atom | Oculta | Query SQL a Athena | `Atom.tmdl` (`isHidden`) |
| `Tel_Orbi` | Apoyo deduplicación | teléfono+mes+año distinto (Orbi) | Oculta | Insumo del anti-join Atom vs Orbi | `Tel_Orbi.tmdl` (`isHidden`) |
| `Email_Orbi` | Apoyo deduplicación | email+mes+año distinto (Orbi) | Oculta | Insumo del anti-join Atom vs Orbi | `Email_Orbi.tmdl` (`isHidden`) |
| `DateTableTemplate_...` | Automática (Time Intelligence) | — | Oculta (sistema) | Plantilla de tabla de fecha | `model.tmdl` |
| `LocalDateTable_...` (×20) | Automáticas (Time Intelligence) | — | Ocultas (sistema) | Generadas por la función de fecha/hora automática | `model.tmdl`, `relationships.tmdl` |

## Relaciones

| Desde | Hacia | Cardinalidad | Dirección | Activa | Evidencia |
|---|---|---|---|---|---|
| `General[Fecha]` | `Calendario[Fecha]` | Muchos a uno (implícita) | Sencilla (implícita) | Sí | `relationships.tmdl` (`29990a5a-...`) |
| `Parametros[Parametro]` | `LocalDateTable_...[Date]` | Automática (variation) | — | Sí | `relationships.tmdl` (`82534416-...`) |
| Columnas de fecha de `Orbi leads`, `Atom`, `General`, `Calendario` | `LocalDateTable_...[Date]` | Automáticas (variations Time Intelligence) | — | Sí | `relationships.tmdl` (18 relaciones `joinOnDateBehavior: datePartOnly`) |

> Observación: la única relación de negocio explícita es `General[Fecha] → Calendario[Fecha]`. El resto (19) son relaciones automáticas de jerarquías de fecha generadas por la función de Time Intelligence.

## Claves y jerarquías

- No hay claves marcadas explícitamente (`isKey`) en las tablas de negocio; `lead_id` actúa como identificador lógico del lead pero no está declarado como clave.
- Jerarquías: solo las jerarquías de fecha automáticas (`'Jerarquía de fechas'`) de cada `LocalDateTable`. No hay jerarquías de usuario definidas.
- `Calendario[NombreMes]` ordena por `Calendario[Mes]` (`sortByColumn: Mes`).

# 6. Columnas

## Tabla `General` (evidencia `General.tmdl`)

| Tabla | Columna | Tipo | Calculada/Origen | Descripción | Utilizada |
|---|---|---|---|---|---|
| General | lead_id | (inferido texto) | Origen (UNION) | Identificador del lead | Sí — visual "Detalle" |
| General | Fuente | texto | Origen (literal "Orbi Leads"/"Atom") | Plataforma de origen | Sí — slicers/leyendas |
| General | status_name | texto | Origen | Estado del lead | Sí — múltiples visuales |
| General | campaing_name | texto | Origen | Campaña | Sí — slicers/pivots |
| General | medium_value | texto | Origen | Medio de contacto | Sí — "Leads por Medio" |
| General | category_name | texto | Origen | Categoría/tipo de negocio | Sí — slicers |
| General | brand_name | texto | Origen | Marca | Sí — "Detalle" |
| General | adviser_name | texto | Origen | Asesor | Sí — "Estado Actual Leads Asesor" |
| General | adviser_email | texto | Origen | Email del asesor | No utilizada en visuales |
| General | client_name | texto | Origen | Nombre del cliente | Sí — "Detalle" |
| General | client_phone | texto | Origen | Teléfono del cliente | Sí — "Detalle" |
| General | client_email | texto | Origen | Email del cliente | Sí — "Detalle" |
| General | created_at | string | Origen | Fecha última gestión | Sí — "Detalle" |
| General | updated_at | fecha | Origen | Fecha de actualización | No utilizada en visuales |
| General | lead_created_at | fecha | Origen | Fecha de creación del lead | No utilizada en visuales |
| General | management_time | número | Origen | Tiempo de gestión | No utilizada en visuales |
| General | Fecha | fecha | Origen | Fecha del lead (base de `Calendario`) | Solo en relación, no en visual |
| General | centro | texto | Origen | Centro/sala (valor crudo) | No (se usa `centro2`) |
| General | centro2 | texto | Calculada (SWITCH homologación) | Centro/sala homologado | Sí — "Leads Por Centro" |
| General | tipificacion | texto | Origen | Tipificación de la gestión | Sí — slicers/pivots |
| General | Action_name | texto | Origen | Acción registrada | Solo en filtro página "Cita Agendada" |
| General | Gestión | texto | Origen | Clasificación de gestión Orbi (>2h / <2h) | Sí — slicers |
| General | Tiempo de contacto | número | Origen | Tiempo de contacto (Atom, minutos) | Sí — "Detalle" (Sum) |
| General | nombre_origen | texto | Origen | Origen (solo Atom) | No utilizada en visuales |
| General | grupo | texto | Origen | Grupo (solo Atom) | No utilizada en visuales |
| General | primer_usuario | texto | Origen | Primer usuario (solo Atom) | No utilizada en visuales |
| General | primer_grupo | texto | Origen | Primer grupo (solo Atom) | No utilizada en visuales |

## Tabla `Calendario`

| Tabla | Columna | Tipo | Calculada/Origen | Descripción | Utilizada |
|---|---|---|---|---|---|
| Calendario | Fecha | fecha | `DISTINCT(General[Fecha])` | Fecha | Relación |
| Calendario | Año | entero | `YEAR(Fecha)` | Año | Sí — slicers/eje |
| Calendario | Mes | entero | `MONTH(Fecha)` | Mes (número) | Solo ordena `NombreMes` |
| Calendario | NombreMes | texto | `SWITCH(Mes,...)` | Nombre de mes | Sí — "Leads Por Mes" |
| Calendario | Dia | entero | `DAY(Fecha)` | Día | Sí — "Total leads por días del mes" |

## Columnas calculadas de staging

| Tabla | Columna | Definición | Rol |
|---|---|---|---|
| Orbi leads | Orbi gestión | `IF(DATEDIFF(fecha_llegada,fecha_primera_gestion,MINUTE)>120,"Mayor a 2 horas","Menor a 2 horas")` | Clasificación de tiempo de gestión |
| Atom | atom gestión | `DATEDIFF(fecha_asignacion, fh_primer_mensaje_agente, MINUTE)` | Tiempo de contacto (min) |
| Atom | Cruce_Tel / Cruce_Email | `client_phone/email & "|" & MONTH(lead_created_at) & "|" & YEAR(...)` | Llaves de cruce mensual |
| Atom | Cruce_Tel_Orbi / Cruce_Email_Orbi | `LOOKUPVALUE` contra `Tel_Orbi`/`Email_Orbi` | Detección de coincidencia con Orbi |
| Atom | Criterio | `IF(Cruce_Tel_Orbi=BLANK() && Cruce_Email_Orbi=BLANK(),"Si","No")` | Bandera de inclusión (anti-join) |
| Atom | management_time2 | `management_time/60` | Conversión a minutos |
| Atom | status_name | `SWITCH`/`IF` sobre `atendido`, `atencion`, `tipificacion` | Estado derivado del lead Atom |

# 7. Medidas

| Medida | Tabla | Fórmula/Resumen | Uso | KPI/Análisis | Evidencia |
|---|---|---|---|---|---|
| Leads | Medidas | `DISTINCTCOUNT(General[lead_id])` | Conteo de leads únicos | KPI principal de volumen | `Medidas.tmdl` |
| Total Leads sin nuevos | Medidas | `CALCULATE(DISTINCTCOUNTNOBLANK(General[lead_id]), status_name<>"Nuevo" && Fuente="Orbi Leads")` + `CALCULATE(..., status_name="Atendido" && Fuente="Atom")` | Leads gestionados según reglas por fuente | KPI de gestión | `Medidas.tmdl` |
| %Gestionados | Medidas | `DIVIDE([Total Leads sin nuevos],[Leads])` | Porcentaje de gestión | KPI de eficiencia | `Medidas.tmdl` |

# 8. Páginas

| Página | Visible | Objetivo | Navegación | Evidencia |
|---|---|---|---|---|
| General | Visible (activa) | Vista principal: volumen y gestión de leads con desgloses | Botones "Detalle", "Días", "Centro", "Campaña" | `pages/5a5f1a6f0cc9bb4020bc/page.json` |
| Detalle | Oculta (`HiddenInViewMode`) | Detalle por lead (tabla) y distribución por estado/tipificación | Botones "General", "Días" | `pages/5530a675c4ec857bce9b/page.json` |
| Días | Oculta (`HiddenInViewMode`) | Evolución diaria/mensual de leads y gestión | Botones "General", "Detalle" | `pages/62aebec2a6e955dde5c4/page.json` |
| Cita Agendada | Oculta (`HiddenInViewMode`) | Leads con `Action_name = "Cita agendada"` por centro y medio | Botones "Detalle", "Días", "Centro", "Campaña" | `pages/512599bb0a5a991b53db/page.json` (filtro de página) |

# 9. Visuales

> Nombre del visual = **título visible** configurado en el contenedor. Donde no existe título literal se registra `Sin título visible` (no se inventan nombres), conforme al ritual.

## Página General

| Página | Nombre del visual | Tipo de visual | Campos/Categorías | Medidas | Filtros | Propósito/Notas |
|---|---|---|---|---|---|---|
| General | Leads Por Centro | clusteredBarChart | General[centro2] | Leads, Total Leads sin nuevos | Slicers de página | Leads y gestionados por sala/centro. ⚠ Reglas de color huérfanas (ver §18) |
| General | Leads Por Mes | lineChart | Calendario[NombreMes], Calendario[Año] | Leads | Slicers de página | Evolución mensual |
| General | Leads por Medio | pieChart | General[medium_value] | Leads | Slicers de página | Distribución por medio |
| General | Estado Actual Por Campaña | pivotTable | General[status_name], General[campaing_name] | Leads | Slicers de página | Estado × campaña |
| General | Estado Actual Leads Asesor | pivotTable | General[status_name], General[adviser_name] | Leads | Slicers de página | Estado por asesor |
| General | Total Leads | card | — | Leads | Slicers de página | KPI volumen |
| General | Leads Gestionados | card | — | Total Leads sin nuevos | Slicers de página | KPI gestión |
| General | % Gestionados | card | — | %Gestionados | Slicers de página | KPI eficiencia |
| General | Última Actualización | card | Min(Parametros[Parametro]) | — | — | Fecha de referencia |
| General | Año | slicer | Calendario[Año] | — | — | Segmentación por año |
| General | Año | slicer | Calendario[NombreMes] | — | — | ⚠ Título "Año" pero segmenta por Mes |
| General | Año | slicer | General[Fuente] | — | — | ⚠ Título "Año" pero segmenta por Fuente |
| General | Año | slicer | General[category_name] | — | — | ⚠ Título "Año" pero segmenta por Categoría |
| General | Año | slicer | General[campaing_name] | — | — | ⚠ Título "Año" pero segmenta por Campaña |
| General | Año | slicer | General[centro2] | — | — | ⚠ Título "Año" pero segmenta por Centro |
| General | Año | slicer | General[Gestión] | — | — | ⚠ Título "Año" pero segmenta por Gestión |
| General | Sin título visible | slicer | General[tipificacion] | — | — | Segmentación por tipificación |
| General | Texto: "Leads" | textbox | — | — | — | Rótulo |
| General | Botón "Detalle" | actionButton | — | — | — | Navegación → página Detalle |
| General | Botón "Días" | actionButton | — | — | — | Navegación → página Días |
| General | Botón "Centro" | actionButton | — | — | — | Navegación por Bookmark (página Días) |
| General | Botón "Campaña" | actionButton | — | — | — | Navegación por Bookmark (página Días) |
| General | Sin título visible | image | — | — | — | Elemento gráfico |
| General | Sin título visible | shape (×2) | — | — | — | Elementos gráficos |

## Página Detalle

| Página | Nombre del visual | Tipo de visual | Campos/Categorías | Medidas | Filtros | Propósito/Notas |
|---|---|---|---|---|---|---|
| Detalle | Detalle | tableEx | lead_id, client_name, brand_name, campaing_name, client_email, client_phone, medium_value, status_name, created_at | Sum(General[Tiempo de contacto]) | Slicers de página | Detalle por lead |
| Detalle | Leads Por Estado | pieChart | General[status_name] | Leads | Slicers de página | ⚠ Reglas de color huérfanas (ver §18) |
| Detalle | Leads Por Mes | clusteredBarChart | Calendario (mes) | Leads | Slicers de página | Barras por mes |
| Detalle | Tipificación Por Estado | pivotTable | Calendario[NombreMes], General[tipificacion] | Leads | Slicers de página | Tipificación por estado/mes |
| Detalle | Total Leads | card | — | Leads | Slicers de página | KPI volumen |
| Detalle | Leads Gestionados | card | — | Total Leads sin nuevos | Slicers de página | KPI gestión |
| Detalle | % Gestionados | card | — | %Gestionados | Slicers de página | KPI eficiencia |
| Detalle | Última Actualización | card | Min(Parametros[Parametro]) | — | — | Fecha de referencia |
| Detalle | Año | slicer (×6) | Calendario[Año], General[category_name], General[Fuente], y otros | — | — | ⚠ Varios slicers con título "Año" segmentan por otros campos |
| Detalle | Sin título visible | slicer | General[tipificacion] | — | — | Segmentación por tipificación |
| Detalle | Texto: "Leads" | textbox | — | — | — | Rótulo |
| Detalle | Botón "General" | actionButton | — | — | — | Navegación → página General |
| Detalle | Botón "Días" | actionButton | — | — | — | Navegación → página Días |
| Detalle | Sin título visible | image | — | — | — | Elemento gráfico |
| Detalle | Sin título visible | shape (×2) | — | — | — | Elementos gráficos |

## Página Días

| Página | Nombre del visual | Tipo de visual | Campos/Categorías | Medidas | Filtros | Propósito/Notas |
|---|---|---|---|---|---|---|
| Días | Total leads por días del mes | lineChart | Calendario[Dia], Calendario[NombreMes] | Leads | Slicers de página | Evolución diaria. ⚠ Reglas de color huérfanas |
| Días | Total Leads | card | — | Leads | Slicers de página | KPI volumen |
| Días | Leads Gestionados | card | — | Total Leads sin nuevos | Slicers de página | KPI gestión |
| Días | % Gestionados | card | — | %Gestionados | Slicers de página | KPI eficiencia |
| Días | Última Actualización | card | Min(Parametros[Parametro]) | — | — | Fecha de referencia |
| Días | Año | slicer (×7) | Calendario[Año], Calendario[NombreMes], General[campaing_name], General[category_name], General[centro2], General[Gestión], General[Fuente] | — | — | ⚠ Varios slicers con título "Año" segmentan por otros campos |
| Días | Sin título visible | slicer | General[tipificacion] | — | — | Segmentación por tipificación |
| Días | Botón "General" | actionButton | — | — | — | Navegación → página General |
| Días | Botón "Detalle" | actionButton | — | — | — | Navegación → página Detalle |
| Días | Texto: "Leads" | textbox | — | — | — | Rótulo |
| Días | Sin título visible | image | — | — | — | Elemento gráfico |
| Días | Sin título visible | shape (×2) | — | — | — | Elementos gráficos |

## Página Cita Agendada

> Filtro de página aplicado: `General[Action_name]` IN "Cita agendada".

| Página | Nombre del visual | Tipo de visual | Campos/Categorías | Medidas | Filtros | Propósito/Notas |
|---|---|---|---|---|---|---|
| Cita Agendada | Leads Por Centro | clusteredBarChart | General[centro2] | Leads, Total Leads sin nuevos | Filtro de página + slicers | ⚠ Reglas de color huérfanas |
| Cita Agendada | Leads por Medio | pieChart | General[medium_value] | Leads | Filtro de página + slicers | ⚠ Reglas de color huérfanas |
| Cita Agendada | Leads Por Mes | lineChart | Calendario (mes) | Leads | Filtro de página + slicers | Evolución mensual |
| Cita Agendada | Estado Actual Leads Asesor | pivotTable | General[status_name], General[adviser_name] | Leads | Filtro de página + slicers | Estado por asesor |
| Cita Agendada | Estado Actual Por Campaña | pivotTable | General[status_name], General[campaing_name] | Leads | Filtro de página + slicers | Estado × campaña |
| Cita Agendada | Total Leads | card | — | Leads | Filtro de página + slicers | KPI volumen |
| Cita Agendada | Leads Gestionados | card | — | Total Leads sin nuevos | Filtro de página + slicers | KPI gestión |
| Cita Agendada | % Gestionados | card | — | %Gestionados | Filtro de página + slicers | KPI eficiencia |
| Cita Agendada | Última Actualización | card | Min(Parametros[Parametro]) | — | — | Fecha de referencia |
| Cita Agendada | Año | slicer (×7) | Calendario[Año], General[campaing_name] y otros | — | — | ⚠ Varios slicers con título "Año" segmentan por otros campos |
| Cita Agendada | Sin título visible | slicer (×2) | General[tipificacion] y otro | — | — | Segmentación |
| Cita Agendada | Texto: "Leads" | textbox | — | — | — | Rótulo |
| Cita Agendada | Botón "Detalle" | actionButton | — | — | — | Navegación → página Detalle |
| Cita Agendada | Botón "Días" | actionButton | — | — | — | Navegación → página Días |
| Cita Agendada | Botón "Centro" | actionButton | — | — | — | Navegación por Bookmark (página Días) |
| Cita Agendada | Botón "Campaña" | actionButton | — | — | — | Navegación por Bookmark (página Días) |
| Cita Agendada | Sin título visible | image | — | — | — | Elemento gráfico |
| Cita Agendada | Sin título visible | shape (×2) | — | — | — | Elementos gráficos |

> Nota de método: el título visible se tomó de `visualContainerObjects.title[0].properties.text.expr.Literal.Value` de cada `visual.json`. Total de contenedores por página: General 24, Detalle 23 (incluye textbox interno), Días 18, Cita Agendada 25.

# 10. KPIs

| KPI | Fórmula | Definición técnica | Interpretación funcional | Evidencia |
|---|---|---|---|---|
| Leads | `DISTINCTCOUNT(General[lead_id])` | Conteo distinto de `lead_id` | Cantidad de leads únicos captados | `Medidas.tmdl` |
| Total Leads sin nuevos (Leads Gestionados) | Suma de dos `CALCULATE` por fuente | Orbi: estado ≠ "Nuevo"; Atom: estado = "Atendido" | Leads considerados gestionados | `Medidas.tmdl` |
| %Gestionados | `DIVIDE([Total Leads sin nuevos],[Leads])` | Ratio gestionados/total | Eficiencia de gestión | `Medidas.tmdl` |

# 11. Filtros y segmentaciones

| Página | Filtro/Slicer | Campo | Tipo | Impacto | Evidencia |
|---|---|---|---|---|---|
| Cita Agendada | Filtro de página | `General[Action_name]` IN "Cita agendada" | Categórico | Limita la página a leads con cita agendada | `pages/512599.../page.json` |
| General/Detalle/Días/Cita Agendada | Slicers | Año, NombreMes, Fuente, category_name, campaing_name, centro2, tipificacion, Gestión | Categórico/lista | Segmentación cruzada de los visuales | `visual.json` de cada slicer |

> Hallazgo de consistencia: la mayoría de slicers muestran el título "Año" aunque segmenten por otro campo (Fuente, Categoría, Campaña, Centro, Mes, Gestión). El título del slicer no refleja su campo real (ver §18).

# 12. Elementos utilizados

| Elemento | Tabla/Objeto | Tipo | Dónde se utiliza | Función | Evidencia |
|---|---|---|---|---|---|
| lead_id | General | Columna | "Detalle" + todas las medidas | Identificar/contar leads | `visual.json` 83542d; `Medidas.tmdl` |
| Fuente | General | Columna | Slicers, medida gestión | Distinguir Orbi/Atom | varios `visual.json` |
| status_name | General | Columna | "Leads Por Estado", pivots, "Detalle" | Estado del lead | varios `visual.json` |
| campaing_name | General | Columna | "Estado Actual Por Campaña", slicers | Campaña | varios `visual.json` |
| medium_value | General | Columna | "Leads por Medio", "Detalle" | Medio | varios `visual.json` |
| category_name | General | Columna | Slicers | Categoría | varios `visual.json` |
| brand_name | General | Columna | "Detalle" | Marca | 83542d |
| adviser_name | General | Columna | "Estado Actual Leads Asesor" | Asesor | df2da0 / 3e8e50 |
| client_name/email/phone | General | Columnas | "Detalle" | Datos de contacto | 83542d |
| created_at | General | Columna | "Detalle" (Fecha última gestión) | Fecha de gestión | 83542d |
| centro2 | General | Columna calc. | "Leads Por Centro", slicers | Centro/sala homologado | varios |
| tipificacion | General | Columna | Slicers, "Tipificación Por Estado" | Tipificación | varios |
| Gestión | General | Columna | Slicers | Clasificación de tiempo Orbi | 69d41e / fe53f0 |
| Tiempo de contacto | General | Columna | "Detalle" (Sum) | Minutos de contacto | 83542d |
| Año, NombreMes, Dia | Calendario | Columnas | Slicers, "Leads Por Mes", "Total leads por días del mes" | Análisis temporal | varios |
| Parametro | Parametros | Columna | Cards "Última Actualización" (Min) | Referencia de fecha | bfe063/60a8d6/f4328e/fd6649 |
| Leads, Total Leads sin nuevos, %Gestionados | Medidas | Medidas | Cards, tablas, gráficos | KPIs | varios |

# 13. Elementos NO utilizados

| Elemento | Tabla/Objeto | Tipo | Evidencia de no uso | Clasificación | Requiere validación |
|---|---|---|---|---|---|
| adviser_email | General | Columna | Sin `queryRef` en ningún visual | No utilizado | Sí |
| updated_at | General | Columna | Sin `queryRef` en visuales | No utilizado | Sí |
| lead_created_at | General | Columna | Sin `queryRef` en visuales | No utilizado | Sí |
| management_time | General | Columna | Sin `queryRef` en visuales | No utilizado | Sí |
| nombre_origen | General | Columna | Sin `queryRef`; sólo poblada en Atom | No utilizado | Sí |
| grupo | General | Columna | Sin `queryRef`; sólo Atom | No utilizado | Sí |
| primer_usuario | General | Columna | Sin `queryRef`; sólo Atom | No utilizado | Sí |
| primer_grupo | General | Columna | Sin `queryRef`; sólo Atom | No utilizado | Sí |
| centro | General | Columna | Reemplazada por `centro2` en visuales | Uso técnico (insumo de `centro2`) | Sí |
| Action_name | General | Columna | Sólo en filtro de página "Cita Agendada" | Uso técnico (filtro), no en visual | Sí |
| Calendario[Mes] | Calendario | Columna | Sólo `sortByColumn` de NombreMes | Uso técnico | No |
| Orbi leads / Atom | Tablas staging | Tabla oculta | No expuestas en visuales | Uso técnico (origen) | No |
| Tel_Orbi / Email_Orbi | Tablas apoyo | Tabla oculta | Sólo insumo de deduplicación | Uso técnico | No |
| LocalDateTable_* (×20), DateTableTemplate_* | Tablas auto | Tabla oculta | Generadas por Time Intelligence | Uso técnico / posible obsoleto | Sí |
| Visuales `shape`/`image` sin título | Reporte | Contenedor | Sin datos ni consumo de medida | Uso técnico (decorativo) | No |

> Nota: la clasificación "No utilizado" no implica que el elemento deba eliminarse. Es un hallazgo del censo que requiere validación funcional/técnica.

# 14. Reglas de negocio

| Regla | Implementación técnica | Interpretación funcional | Evidencia | Estado |
|---|---|---|---|---|
| Deduplicación Atom vs Orbi | `Criterio = IF(Cruce_Tel_Orbi=BLANK() && Cruce_Email_Orbi=BLANK(),"Si","No")`; `General` incluye Atom sólo si `Criterio="Si"` | Un lead de Atom se cuenta sólo si no existe ya en Orbi por teléfono o email en el mismo mes/año | `Atom.tmdl`, `General.tmdl`, `Tel_Orbi.tmdl`, `Email_Orbi.tmdl` | Encontrado |
| Clasificación de gestión Orbi | `IF(DATEDIFF(fecha_llegada,fecha_primera_gestion,MINUTE)>120,"Mayor a 2 horas","Menor a 2 horas")` | Se distingue si el primer contacto ocurrió antes o después de 2 horas | `Orbi leads.tmdl` | Encontrado |
| Estado del lead Atom | `SWITCH`/`IF` sobre `atendido`, `atencion`, `tipificacion` → Atendido / No Atendido / Sin Identificar | Deriva el estado cuando la fuente no lo entrega explícito | `Atom.tmdl` (`status_name`) | Encontrado (interpretación a validar) |
| Leads gestionados | Orbi: `status_name<>"Nuevo"`; Atom: `status_name="Atendido"` | Definición de "gestionado" difiere por fuente | `Medidas.tmdl` | Encontrado (definición funcional a validar) |
| Homologación de salas/centros | `SWITCH(General[centro], ...)` → nombres "Peru - MG Mayorista - ..." | Unifica nomenclatura de salas MG | `General.tmdl` (`centro2`) | Encontrado |
| Fecha primera gestión (Orbi) | `MIN(CASE WHEN status_id <> 1 THEN created_at END)` | Primera gestión = primer evento con estado distinto de "nuevo" (status_id 1) | `Orbi leads.tmdl` (SQL) | Inferido |
| Marca MG | Orbi `upper(brand_name) like '%MG%'`; Atom join por canal/campaña con MG | Alcance limitado a la marca MG | `Orbi leads.tmdl`, `Atom.tmdl` | Encontrado |
| Última versión por lead | `LAST_VALUE(...) OVER (PARTITION BY lead_id ORDER BY created_at/fh_asignacion)` | Se conserva el último estado conocido del lead | `Orbi leads.tmdl`, `Atom.tmdl` | Encontrado |

# 15. Dependencias

```text
Athena tatooine_prod_core.materialized_leads_tracking
   └─ (M/SQL, LAST_VALUE + subconsulta gestión) → [Orbi leads] (oculta)
        ├─ (DAX DISTINCT) → [Tel_Orbi], [Email_Orbi]  ── insumo de deduplicación
        └─ columna calc [Orbi gestión]

Athena atom_leads.leads + atom_leads.nebula_tiempos_de_agentes
   └─ (M/SQL, LAST_VALUE + joins) → [Atom] (oculta)
        ├─ columnas calc: Cruce_Tel/Email → Cruce_*_Orbi (LOOKUPVALUE a Tel_Orbi/Email_Orbi)
        │     → Criterio ("Si"/"No")  [regla de anti-join]
        ├─ status_name (derivado), atom gestión, management_time2
        └─ FILTER(Atom, Criterio="Si")

[Orbi leads] + FILTER([Atom]) ── UNION (DAX) ──► [General]  (tabla central)
        ├─ columna calc [centro2] (homologación)
        ├─ [Fecha] ── DISTINCT ──► [Calendario] (Año/Mes/NombreMes/Dia)
        └─ [lead_id] ──► Medidas: Leads → Total Leads sin nuevos → %Gestionados

[General] / [Calendario] / [Parametros] / [Medidas]
        └─► Visuales (slicers, cards, tablas, pie, line, bar, pivot)
              └─► Páginas: General (visible), Detalle, Días, Cita Agendada (ocultas)

Parametros (M: LocalNow zona -5) ──► cards "Última Actualización"
```

Concentraciones de lógica: la tabla `General` (UNION + homologación) y la tabla `Atom` (deduplicación con múltiples columnas calculadas) son los puntos de mayor densidad de reglas.

# 16. Vacíos de información

| Vacío | Por qué es relevante | Evidencia | Impacto | Requiere validación |
|---|---|---|---|---|
| Propietarios de las fuentes Athena | No hay gobierno de datos identificable desde el proyecto | Sin metadatos de propietario | Medio | Sí |
| Frecuencia y proceso de actualización | No hay configuración de refresh en el PBIP versionado | `Parametros` usa `LocalNow` pero no define refresh | Medio | Sí |
| Definición funcional de estados Atom | La lógica técnica deriva estados; falta confirmación de negocio | `Atom.status_name` (SWITCH) | Alto (afecta KPI gestión) | Sí |
| Umbral de 2 horas en gestión Orbi | No documentado el origen del umbral (120 min) | `Orbi gestión` | Medio | Sí |
| Definición de "gestionado" distinta por fuente | Orbi por `<>"Nuevo"`, Atom por `="Atendido"` | `Total Leads sin nuevos` | Alto | Sí |
| Títulos de slicers no representativos | Casi todos los slicers muestran "Año" sin importar su campo | §9, §11 | Bajo/Medio (usabilidad) | Sí |
| Propósito de columnas no utilizadas | 8+ columnas sin consumo en visuales | §13 | Bajo/Medio | Sí |
| Función de las tablas automáticas de fecha | 20 LocalDateTable pueden ser innecesarias | `model.tmdl` | Bajo | Sí |

# 17. Propuestas de revisión IA

| Propuesta | Categoría | Motivo | Evidencia | Impacto | Prioridad | Requiere validación |
|---|---|---|---|---|---|---|
| Revisar reglas de color huérfanas que apuntan a tablas inexistentes | Reporte | Varios visuales tienen selectores de color `dataPoint` con `SourceRef` a `VehiculosEntregados[Gama]` y `Funnel Digital[Origen]`, tablas que no existen en el modelo, y literales de modelos de vehículos (CX-30, Mazda 2, etc.) | `visual.json` 41b98b (Detalle), 4ccd33 y 230203 (Cita Agendada), 9eee60 (Días) | Reglas de formato inertes; ruido y posible copia desde otro reporte | Media | Sí |
| Corregir/estandarizar los títulos de los slicers | Reporte | Casi todos los slicers muestran el título literal "Año" aunque segmenten por Fuente, Categoría, Campaña, Centro, Mes o Gestión | §9 (títulos por visual) | Confusión para el usuario final | Media | Sí |
| Confirmar la definición funcional de "Leads gestionados" | Negocio | El criterio difiere por fuente (Orbi `<>"Nuevo"`, Atom `="Atendido"`), lo que puede afectar la comparabilidad del KPI | `Medidas.tmdl` | Afecta el KPI %Gestionados | Alta | Sí |
| Validar el umbral de 120 minutos de la clasificación de gestión Orbi | Negocio | El valor 120 min está embebido en DAX sin documentación | `Orbi leads.tmdl` (`Orbi gestión`) | Afecta segmentación por tiempo de respuesta | Media | Sí |
| Revisar la lógica de deduplicación Atom vs Orbi | Modelo | El anti-join por teléfono/email + mes/año es una regla compleja que determina qué leads se cuentan | `Atom.tmdl`, `Tel_Orbi`, `Email_Orbi` | Afecta directamente el conteo de Leads | Alta | Sí |
| Evaluar desactivar la fecha/hora automática (Time Intelligence) | Modelo | Existen 20 `LocalDateTable` + plantilla que sólo aportan jerarquías automáticas y 19 relaciones | `model.tmdl`, `relationships.tmdl` | Reduce complejidad y tamaño del modelo | Baja | Sí |
| Documentar propietario y frecuencia de actualización | Gobierno / Actualización | No hay evidencia de responsables ni de proceso de refresh | Proyecto PBIP | Trazabilidad y operación | Media | Sí |
| Revisar columnas sin consumo | Datos | 8+ columnas de `General` no aparecen en ningún visual | §13 | Limpieza/documentación del modelo | Baja | Sí |

# 18. Hallazgos

| Hallazgo | Categoría | Descripción | Evidencia | Impacto |
|---|---|---|---|---|
| Referencias huérfanas en formato condicional | Reporte | Visuales con reglas de color por `dataPoint` que referencian `VehiculosEntregados[Gama]` y `Funnel Digital[Origen]` (tablas ausentes) y modelos de vehículos | `visual.json` 41b98b, 4ccd33, 230203, 9eee60 | Formato inerte; indicio de reutilización de plantilla |
| Títulos de slicers no representativos | Reporte | La mayoría de slicers muestran "Año" sin corresponder a su campo real | §9 | Usabilidad/claridad para el usuario |
| Modelo con doble deduplicación | Modelo/Datos | Deduplicación en SQL (LAST_VALUE) + deduplicación DAX (anti-join Atom vs Orbi) | `Orbi leads.tmdl`, `Atom.tmdl`, `General.tmdl` | Lógica de conteo concentrada y sensible |
| Definición de KPI dependiente de la fuente | Negocio | "Gestionado" se define distinto para Orbi y Atom | `Medidas.tmdl` | Riesgo de interpretación del %Gestionados |
| Time Intelligence automático activo | Modelo | 20 tablas de fecha automáticas | `model.tmdl` | Complejidad/tamaño |
| Página `Cita Agendada` filtrada a nivel de página | Reporte | Filtro `Action_name = "Cita agendada"` | `pages/512599.../page.json` | Vista especializada oculta |
| `Parametros` basada en `LocalNow` | Datos | La "Última Actualización" se calcula con la hora local (zona -5) al refrescar | `Parametros.tmdl` | Depende del momento de actualización |

# 19. Limitaciones del censo

- Análisis realizado exclusivamente sobre los archivos del proyecto (TMDL y PBIR); no se ejecutó el modelo ni se inspeccionaron datos.
- No se validó el contenido de las fuentes Athena ni sus permisos, propietarios o volúmenes.
- Las interpretaciones funcionales (estados, "gestionado", umbral 2h) se infieren de la lógica técnica y quedan marcadas como pendientes de validación con negocio.
- No se documenta la configuración de actualización porque no forma parte del PBIP versionado revisado.
- Los campos exactos de algunos slicers/gráficos con título "Año" se consolidan por página; el campo real se determinó por `queryRef` de cada visual.

# 20. Validación final

- [x] Cobertura revisada — modelo (tablas de negocio/apoyo + auto) y reporte (4 páginas, 90 contenedores) recorridos.
- [x] Consistencia revisada — hallazgos soportados por archivos TMDL/PBIR citados.
- [x] Trazabilidad revisada — cada afirmación relevante indica su evidencia.
- [x] Identificación de visuales revisada — título visible por visual; sin título → `Sin título visible` (sin inventar nombres).
- [x] Elementos no utilizados revisados — §13.
- [x] Vacíos revisados — §16.
- [x] Propuestas revisadas — §17, todas con evidencia.
- [x] Limitaciones documentadas — §19.

## Resultado

Censo técnico y funcional del BI **GC - Leads MG** consolidado con el ajuste del ritual: cada visual se documenta por su **título visible** (o `Sin título visible` cuando no lo tiene, sin inventar nombres). El BI integra leads de **Orbi** y **Atom** desde Amazon Athena, aplica deduplicación en SQL y DAX (anti-join Atom vs Orbi por teléfono/email + mes/año) y expone tres KPIs (Leads, Total Leads sin nuevos, %Gestionados) sobre la tabla central `General` con dimensión `Calendario`. Se identificaron elementos utilizados y no utilizados, reglas de negocio con su implementación, dependencias, vacíos y propuestas basadas en evidencia. Hallazgos destacados: (1) reglas de color en varios visuales apuntan a tablas inexistentes (`VehiculosEntregados`, `Funnel Digital`), y (2) casi todos los slicers muestran el título "Año" aunque segmenten por otros campos. El ritual no contempló ninguna modificación del BI.
