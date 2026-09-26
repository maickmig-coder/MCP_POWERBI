# Censo BI — GC - Leads MG

Documento de inventario (censo) completo del reporte Power BI **GC - Leads MG** (`GC - Leads MG.pbip`). Mapea de punta a punta: orígenes de datos, tablas, columnas (usadas y no usadas), medidas, relaciones, páginas, visuales, campos, colores y KPIs.

> Alcance analizado: proyecto PBIP con `GC - Leads MG.SemanticModel` (modelo, formato TMDL) y `GC - Leads MG.Report` (reporte, formato PBIR). El `.pbip` solo referencia el artefacto Report; el modelo es un artefacto hermano en la misma carpeta.

---

## 1. Resumen ejecutivo (finalidad)

El reporte monitorea la **gestión comercial de leads de la marca MG** (automotriz, mercado Perú). Consolida leads provenientes de dos plataformas de captación/atención y mide **cuántos leads llegan** y **qué porcentaje se gestiona** (se atiende), con cortes por tiempo, centro/sala, campaña, medio de captación, asesor, estado y tipificación.

Dos fuentes se unifican en una sola tabla de análisis (`General`):

- **Orbi Leads** — CRM de leads (`tatooine_prod_core.materialized_leads_tracking`), filtrado a marca MG.
- **Atom** — plataforma de mensajería/atención (`atom_leads.leads` + `atom_leads.nebula_tiempos_de_agentes`).

Para no duplicar, los leads de Atom solo se incorporan si **no existen ya en Orbi** (cruce por teléfono o email dentro del mismo mes/año → columna `Criterio = "Si"`).

### KPIs identificados

| KPI | Definición (DAX) | Lectura de negocio |
|-----|------------------|--------------------|
| **Leads** | `DISTINCTCOUNT(General[lead_id])` | Volumen de leads únicos captados. |
| **Total Leads sin nuevos** (Leads Gestionados) | `CALCULATE(DISTINCTCOUNTNOBLANK(lead_id), status<>"Nuevo" & Fuente="Orbi Leads")` + `CALCULATE(DISTINCTCOUNTNOBLANK(lead_id), status="Atendido" & Fuente="Atom")` | Leads que dejaron de estar "Nuevo" (Orbi) o que fueron "Atendido" (Atom); es decir, leads efectivamente trabajados. |
| **%Gestionados** | `DIVIDE([Total Leads sin nuevos],[Leads])` | Tasa de gestión: proporción de leads trabajados sobre el total. Formato porcentaje. |

KPIs operativos derivados (columnas, alimentan slicers y análisis, no son medidas):

- **Gestión (Orbi gestión)**: clasifica el lead en `Mayor a 2 horas` / `Menor a 2 horas` según el tiempo entre llegada y primera gestión (>120 min).
- **Tiempo de contacto (atom gestión)**: minutos entre asignación y primer mensaje del agente (solo Atom).

---

## 2. Orígenes de datos

Conexión única: **Amazon Athena** vía ODBC, nombre de origen (DSN) **`Athena_ODBC2`**, usando `Value.NativeQuery(...)` con *query folding* habilitado (`EnableFolding=true`).

| Tabla PQ | Motor / esquema origen | Lógica clave |
|----------|------------------------|--------------|
| **Orbi leads** | Athena · `tatooine_prod_core.materialized_leads_tracking` | Deduplica por `lead_id` con `LAST_VALUE(... ORDER BY created_at)`. `LEFT JOIN` con agregado que calcula `fecha_llegada`, `fecha_primera_gestion`, `segundos_hasta_gestion`. Filtro `upper(brand_name) LIKE '%MG%'`. Limpieza M: trim/lower email, quita `+ - espacio` del teléfono, Proper case en `adviser_name`, `category_name`, `campaing_name`. |
| **Atom** | Athena · `atom_leads.leads` + `atom_leads.nebula_tiempos_de_agentes` | Marca MG por join de canal. Deriva `medium_value` (WA→Whatsapp, IG/FB→Redes Sociales), `category_name` (taller→Posventa), `brand_name`. Deduplica tiempos por `lead_id` con `LAST_VALUE` sobre `fh_asignacion`. Convierte `created_at`/`fh_primer_mensaje_agente` de texto ISO (reemplaza `T`→espacio) a datetime. |
| **Parametros** | M puro (sin Athena) | `DateTimeZone.SwitchZone(DateTimeZone.LocalNow(),-5,0)` → una fila con la fecha/hora actual (UTC-5). Alimenta la card "Primera fecha". |
| **Medidas** | Tabla vacía (contenedor de medidas). | — |

---

## 3. Tablas del modelo

### 3.1 Tablas visibles / de negocio

| Tabla | Tipo | Rol |
|-------|------|-----|
| **General** | Calculada (DAX `UNION`) | Tabla central de hechos-análisis. `UNION(Orbi, FILTER(Atom, Criterio="Si"))`. |
| **Calendario** | Calculada | Dimensión de fecha. `DISTINCT(General[Fecha])`. |
| **Medidas** | Tabla de medidas | Contiene los 3 KPIs. |
| **Parametros** | Importada (M) | Marca temporal de referencia. |

### 3.2 Tablas ocultas (staging / apoyo)

| Tabla | Motivo |
|-------|--------|
| **Orbi leads** | Staging de la fuente Orbi (todas sus columnas `isHidden`). |
| **Atom** | Staging de la fuente Atom (todas sus columnas `isHidden`). |
| **Tel_Orbi** | Universo de cruces `telefono\|mes\|año` de Orbi, para calcular `Criterio` de Atom. |
| **Email_Orbi** | Universo de cruces `email\|mes\|año` de Orbi, para calcular `Criterio` de Atom. |
| **DateTableTemplate_…** + 21 × **LocalDateTable_…** | Tablas de *time intelligence* automáticas de Power BI (una por cada columna fecha). No aportan al análisis; candidatas a desactivar. |

---

## 4. Diccionario de la tabla `General` (columnas)

`General` es una tabla calculada; sus columnas provienen del `SELECTCOLUMNS` de cada fuente.

| Columna | Origen Orbi | Origen Atom | ¿Usada en visuales? |
|---------|-------------|-------------|---------------------|
| `lead_id` | `lead_id` | `lead_id` | Sí (base de KPI Leads; tabla Detalle) |
| `Fuente` | `"Orbi Leads"` | `"Atom"` | Sí (slicer en todas las páginas) |
| `status_name` | `status_name` | `status_name` (calc) | Sí (Estado: pivots, pie, barras, slicer) |
| `campaing_name` | Proper(`campaing_name`) | Proper(`campaing_name`) | Sí (Campaña: slicer, pivots, tabla) |
| `medium_value` | `medium_value` | derivado del canal | Sí (Medio: pieChart, tabla) |
| `category_name` | Proper(`category_name`) | derivado | Sí (slicer) |
| `brand_name` | `brand_name` | `"MG"` | Sí (Marca: tabla Detalle) |
| `adviser_name` | Proper(`adviser_name`) | `agente` (o "Sin Definir") | Sí (Asesor: pivot) |
| `adviser_email` | `adviser_email` | `email_agente` | No |
| `client_name` | `client_name` | `nombre_cliente` | Sí (tabla Detalle) |
| `client_phone` | `client_phone` (limpio) | `telefono` | Sí (Celular: tabla Detalle) |
| `client_email` | `client_email` | `correo` | Sí (Email: tabla Detalle) |
| `centro` | `concessionaire_names` | `grupo` (o "Sin Definir") | No directamente (se usa `centro2`) |
| `centro2` | SWITCH normalizador de salas MG Perú | — | Sí (Centro: slicer, barras) |
| `tipificacion` | `action_name` | `tipificacion` | Sí (slicer, barras, tabla) |
| `Action_name` | `action_name` | BLANK | Sí (filtro de página "Cita Agendada") |
| `Gestión` | `Orbi gestión` | BLANK | Sí (slicer en todas las páginas) |
| `Tiempo de contacto` | BLANK | `atom gestión` (min) | Sí (tabla Detalle) |
| `created_at` | `created_at` | `fh_asignacion` | Sí (Fecha última gestión: tabla Detalle) |
| `Fecha` | `date(lead_created_at)` | `date(lead_created_at)` | Solo relación → Calendario |
| `updated_at` | `updated_at` | `ultima_actualizacion2` | No |
| `lead_created_at` | `lead_created_at` | `fecha_inicio_conversacion` | No |
| `management_time` | `management_time` | `management_time/60` | No |
| `nombre_origen` | BLANK | `nombre_origen` | No |
| `grupo` | BLANK | `grupo` | No |
| `primer_usuario` | BLANK | `primer_usuario` | No |
| `primer_grupo` | BLANK | `primer_grupo` | No |

### 4.1 Columnas / campos NO usados en ninguna visual

- **General**: `adviser_email`, `centro` (base; se usa la versión normalizada `centro2`), `updated_at`, `lead_created_at`, `management_time`, `nombre_origen`, `grupo`, `primer_usuario`, `primer_grupo`. La columna `Fecha` solo participa en la relación con `Calendario`.
- **Orbi leads** y **Atom**: todas sus columnas son staging oculto; ninguna se expone directamente en visuales (se consumen a través de `General`).
- **Tel_Orbi** / **Email_Orbi**: solo sirven de insumo al cálculo de `Criterio`; no se visualizan.
- **Calendario**: `Fecha` (usada en relación y jerarquía), `Dia` (solo página Días). `Año`, `Mes`, `NombreMes` sí se usan; `Mes` actúa como *sort by* de `NombreMes`.

---

## 5. Columnas calculadas y su lógica

| Tabla | Columna | Fórmula (resumen) |
|-------|---------|-------------------|
| Orbi leads | `Orbi gestión` | `IF(DATEDIFF(fecha_llegada, fecha_primera_gestion, MINUTE) > 120, "Mayor a 2 horas", "Menor a 2 horas")` |
| Atom | `Cruce_Tel` | `client_phone & "|" & MONTH(lead_created_at) & "|" & YEAR(lead_created_at)` |
| Atom | `Cruce_Email` | `client_email & "|" & MONTH & "|" & YEAR` |
| Atom | `Cruce_Tel_Orbi` | `LOOKUPVALUE(Tel_Orbi[...], Tel_Orbi[Cruce_Tel], Atom[Cruce_Tel])` |
| Atom | `Cruce_Email_Orbi` | `LOOKUPVALUE(Email_Orbi[...], Email_Orbi[Cruce_Email], Atom[Cruce_Email])` |
| Atom | `Criterio` | `IF(Cruce_Tel_Orbi=BLANK() && Cruce_Email_Orbi=BLANK(), "Si", "No")` — anti-join contra Orbi |
| Atom | `status_name` | Anidado: `atendido="1"`→Atendido; `atendido="0" & atencion="Si"`→Atendido; `atendido="0" & tipificacion="No tipificado"`→No Atendido; `ISBLANK`→Sin Identificar; else Atendido |
| Atom | `management_time2` | `management_time / 60` |
| Atom | `atom gestión` | `DATEDIFF(fecha_asignacion, fh_primer_mensaje_agente, MINUTE)` |
| General | `centro2` | `SWITCH(centro, ...)` normaliza 15 salas "MG Perú Sala …" a nomenclatura "Peru - MG Mayorista - …" |
| Calendario | `Año`,`Mes`,`NombreMes`,`Dia` | `YEAR`/`MONTH`/SWITCH nombre de mes (sort por `Mes`)/`DAY` |

---

## 6. Relaciones

### 6.1 Relación de negocio (única activa relevante)

| De | A | Cardinalidad | Notas |
|----|---|--------------|-------|
| `General[Fecha]` | `Calendario[Fecha]` | muchos a uno | Conecta hechos con la dimensión calendario. |

### 6.2 Relaciones automáticas de *time intelligence*

Existen ~21 relaciones adicionales del tipo `variation` que conectan cada columna de fecha (`created_at`, `updated_at`, `lead_created_at`, `fecha_llegada`, `fecha_primera_gestion`, `fecha_asignacion`, `fh_primer_mensaje_agente`, `ultima_actualizacion`, `Parametro`, `Calendario[Fecha]`, etc.) con su respectiva `LocalDateTable_…`. Son generadas por la opción *Auto Date/Time* de Power BI (`__PBI_TimeIntelligenceEnabled = 1`).

> **Observación técnica:** estas tablas y relaciones no aportan al análisis actual e inflan el modelo. Se pueden desactivar (Opciones → Data Load → Auto date/time) sin afectar los visuales, que solo usan `Calendario`.

---

## 7. Reporte: páginas y visuales

Configuración global: lienzo **1280×720**, `displayOption: FitToPage`, fondo de página **`#F6F6F5`**. Tema base **Fluent2-CY26SU08** + tema personalizado **Tema 1_BI_Nebula**. Recurso de imagen: **Logo-Nebula….png**.

| # | Página | Visibilidad | Rol |
|---|--------|-------------|-----|
| 1 | **General** | Visible (activa) | Vista principal / resumen. |
| 2 | **Detalle** | Oculta | Detalle lead a lead + análisis por estado/tipificación. |
| 3 | **Días** | Oculta | Evolución diaria de leads. |
| 4 | **Cita Agendada** | Oculta | Filtrada a `General[Action_name] = "Cita agendada"`. |

> Cada visual con datos se identifica por el **título** que muestra en pantalla (propiedad `title.text`). Los slicers muestran su etiqueta de encabezado entre comillas; los botones/formas/imágenes no tienen título.

### 7.1 Página "General" (25 objetos)

**Tarjetas (cards):**
| Título | Medida |
|--------|--------|
| **Total Leads** | `Leads` |
| **Leads Gestionados** | `Total Leads sin nuevos` |
| **% Gestionados** | `%Gestionados` |
| **Última Actualización** | `Min(Parametros[Parametro])` |

**Gráficos:**
| Título | Tipo | Eje / Categoría | Valor |
|--------|------|-----------------|-------|
| **Leads Por Mes** | Línea | `Calendario[NombreMes]` | `Leads` |
| **Leads por Medio** | Circular (pie) | `General[medium_value]` | `Leads` (color fijo ColorId 5 para "Facebook Pago") |
| **Leads Por Centro** | Barras agrupadas | `centro2` | `Leads` + `Total Leads sin nuevos` (serie "Leads Gestionados") |
| **Estado Actual Por Campaña** | Matriz (pivot) | `status_name` × `campaing_name` | `Leads` |
| **Estado Actual Leads Asesor** | Matriz (pivot) | `status_name` × `adviser_name` | `Leads` |

**Slicers (8):** encabezados **"Año"** (`Calendario[Año]`), **"category_name"** (`General[category_name]`), **"Fuente"** (`General[Fuente]`), **"NombreMes"** (`Calendario[NombreMes]`), **"Gestión"** (`General[Gestión]`), **"Tipificación"** (`General[tipificacion]`), **"campaing_name"** (`General[campaing_name]`), **"centro2"** (`General[centro2]`).

**Navegación / decorado (sin título):** 4 action buttons (botones "Detalle", "Días" y navegación), 2 shapes, 1 image (logo), 1 textbox.

### 7.2 Página "Detalle" (22 objetos)

**Tarjetas (cards):**
| Título | Medida |
|--------|--------|
| **Total Leads** | `Leads` |
| **Leads Gestionados** | `Total Leads sin nuevos` |
| **% Gestionados** | `%Gestionados` |
| **Última Actualización** | `Min(Parametros[Parametro])` |

**Gráficos y tabla:**
| Título | Tipo | Campos |
|--------|------|--------|
| **Detalle** | Tabla | `lead_id`, `client_name` (Nombre Cliente), `brand_name` (Marca), `campaing_name` (Campaña), `client_email` (Email), `client_phone` (Celular), `medium_value` (Medio), `status_name` (Estado), `created_at` (Fecha última gestión), `Sum(Tiempo de contacto)` (min) |
| **Leads Por Estado** | Circular (pie) | `status_name` × `Leads` |
| **Leads Por Mes** | Barras | `Calendario[NombreMes]` × `status_name` × `Leads` |
| **Tipificación Por Estado** | Barras | `Calendario[NombreMes]` × `tipificacion` × `Leads` (serie `#B8D4F8`, fondo `#EEEDED`) |

**Slicers (8):** **"Año"**, **"Centro"** (`centro2`), **"campaing_name"**, **"category_name"**, **"Tipificación"**, **"Gestión"**, **"Fuente"**, **"NombreMes"**.

**Decorado (sin título):** 1 image, botón de navegación **"Días"**.

### 7.3 Página "Días" (19 objetos)

**Tarjetas (cards):**
| Título | Medida |
|--------|--------|
| **Total Leads** | `Leads` |
| **Leads Gestionados** | `Total Leads sin nuevos` |
| **% Gestionados** | `%Gestionados` |
| **Última Actualización** | `Min(Parametros[Parametro])` |

**Gráficos:**
| Título | Tipo | Eje / Serie | Valor |
|--------|------|-------------|-------|
| **Total leads por días del mes** | Línea | `Calendario[Dia]` (eje) × `Calendario[NombreMes]` (serie) | `Leads` |

**Slicers (8):** **"Año"**, **"Tipificación"** (`tipificacion`), **"NombreMes"**, **"Gestión Leads"** (`Gestión`), **"category_name"**, **"Fuente"**, **"Centro"** (`centro2`), **"Campaña"** (`campaing_name`).

**Decorado (sin título):** 2 textbox, 1 shape, 1 image, 1 action button (botón **"Detalle"**).

### 7.4 Página "Cita Agendada" (25 objetos)

Filtro de página: `General[Action_name] = "Cita agendada"`.

**Tarjetas (cards):**
| Título | Medida |
|--------|--------|
| **Total Leads** | `Leads` |
| **Leads Gestionados** | `Total Leads sin nuevos` |
| **% Gestionados** | `%Gestionados` |
| **Última Actualización** | `Min(Parametros[Parametro])` |

**Gráficos:**
| Título | Tipo | Eje / Categoría | Valor |
|--------|------|-----------------|-------|
| **Leads por Medio** | Circular (pie) | `General[medium_value]` | `Leads` |
| **Estado Actual Por Campaña** | Matriz (pivot) | `status_name` × `campaing_name` | `Leads` |
| **Estado Actual Leads Asesor** | Matriz (pivot) | `status_name` × `adviser_name` | `Leads` |
| **Leads Por Mes** / **Leads Por Centro** | Barras agrupadas | `Calendario[NombreMes]` + `Año` | `Leads` |

**Slicers (7):** **"Campaña"** (`campaing_name`), **"Centro"** (`centro2`), **"Gestión Leads"** (`Gestión`), **"Año"**, **"Tipificación"**, **"Fuente"**, **"NombreMes"**.

**Decorado (sin título):** textbox de encabezado (texto blanco `#ffffff`), image, shape, action buttons (botón **"Detalle"**).

---

## 8. Campos usados por el reporte (consolidado)

| Tabla | Campos referenciados en visuales |
|-------|----------------------------------|
| **Medidas** | `Leads`, `Total Leads sin nuevos`, `%Gestionados` |
| **General** | `lead_id`, `Fuente`, `status_name`, `campaing_name`, `medium_value`, `category_name`, `brand_name`, `adviser_name`, `client_name`, `client_email`, `client_phone`, `centro2`, `tipificacion`, `Gestión`, `Tiempo de contacto`, `created_at`, `Action_name` (filtro) |
| **Calendario** | `Año`, `NombreMes` (sort por `Mes`), `Dia` |
| **Parametros** | `Parametro` (card "Primera fecha") |

---

## 9. Colores y estilo

### 9.1 Tema personalizado — "Tema 1_BI_Nebula"

Paleta de datos (`dataColors`) de 256 colores. Colores primarios (los primeros de la serie, aplicados por defecto a las series):

| Orden | Hex | Uso típico |
|-------|-----|------------|
| 1 | `#1A73E8` | Azul principal (primera serie) |
| 2 | `#8943A7` | Morado |
| 3 | `#AE0A33` | Rojo / vino |
| 4 | `#028AB0` | Cian |
| 5 | `#E06806` | Naranja |

Colores semánticos del tema:

| Rol | Hex |
|-----|-----|
| `bad` (malo) | `#FF4E4E` |
| `neutral` | `#CDCDD1` |
| `good` (bueno) | `#6ABA4B` |
| `minimum` | `#F3ECF6` |
| `center` | `#8943A7` |
| `maximum` | `#3A1C46` |

Estilos del tema: fondo de página `#F6F6F5`, fondo de visual `#FFFFFF`, bordes `#FFFFFF` con radio 6, header de visual `#F6F6F5`, fuente `Segoe UI`.

### 9.2 Colores literales fijados en visuales (fuera del tema)

| Hex | Dónde | Función |
|-----|-------|---------|
| `#F6F6F5` | Fondo de todas las páginas | Gris muy claro base. |
| `#474747` | Slicers (texto de items) | Gris oscuro. |
| `#323131` | Slicers (header / valores) y cards | Casi negro. |
| `#ffffff` / `#FFFFFF` | Slicers, cards, títulos | Blanco. |
| `#EEEDED` | Barras (página Detalle) | Fondo/plot area. |
| `#B8D4F8` | Barras (página Detalle) | Azul claro de la serie. |

En los gráficos, el color de serie se referencia por `ThemeDataColor` (ColorId 0, 1, 5…), es decir toma la paleta del tema. Ejemplo: en el pie "Leads por Medio", la categoría **"Facebook Pago"** tiene color fijado a `ColorId 5` (`#E06806`, naranja).

---

## 10. Observaciones y oportunidades

1. **Auto Date/Time activo:** 22 tablas de fecha automáticas + sus relaciones inflan el modelo sin uso analítico. Desactivar reduce tamaño y complejidad; los visuales solo dependen de `Calendario`.
2. **Columnas no consumidas** en `General` (`updated_at`, `lead_created_at`, `management_time`, `nombre_origen`, `grupo`, `primer_usuario`, `primer_grupo`, `adviser_email`, `centro`): se pueden ocultar o eliminar del modelo si no se prevé su uso, para aligerar.
3. **Dependencia de columnas calculadas para deduplicación** (`Criterio`, `Tel_Orbi`, `Email_Orbi`): la lógica de anti-join Atom↔Orbi está en DAX; en la migración a Athena (proyecto `01_athena_dimensional_leads_mg`) se reprodujo como anti-join SQL.
4. **Páginas ocultas** (Detalle, Días, Cita Agendada) se alcanzan por los *action buttons* de navegación de la página General.
5. **`brand_name`** en Atom es constante (`"MG"`); en Orbi ya viene filtrado a MG. El reporte es monomarca.

---

*Censo generado a partir del análisis directo de los archivos TMDL del modelo semántico y los `visual.json` del reporte en el proyecto PBIP.*
