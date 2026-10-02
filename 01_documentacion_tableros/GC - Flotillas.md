# Censo BI — GC - Flotillas

> Estado: En revisión
>
> Fecha del censo: 2026-10-02
>
> Versión analizada: Proyecto PBIP — SemanticModel definition v4.2 (compatibilityLevel 1606), Report PBIR
>
> Ritual aplicado: AI-DLC — Ritual estándar para el censo de BI (`00_dlc/01_ai-dlc-censo`), con el ajuste de **Identificación de visuales por título visible**.
>
> Alcance del ritual: descubrimiento y documentación. No se modificó ningún elemento del BI.

---

# 1. Identificación

| Campo | Valor | Estado/Evidencia |
|---|---|---|
| Nombre BI | GC - Flotillas | Encontrado — `03_ejemplobi/01_versiones/00_original/GC - Flotillas/GC - Flotillas.pbip` |
| Proyecto | `GC - Flotillas.pbip` | Encontrado — archivo raíz del proyecto |
| Área | Gestión Comercial — venta de maquinaria/vehículos (Renting, Convenios y Flotillas empresariales) | Inferido — nombres de páginas, filtros `tipoventa_vista`, columna `RENTING`, `Convenios` |
| Objetivo | Monitoreo de entregas/unidades facturadas por canal (Renting, Convenios, Empresarial) con desgloses trimestrales y de recambio | Inferido — medidas Q1–Q4, recambio, páginas tipo dashboard |
| Responsable funcional | No identificado | Desconocido — sin evidencia en el proyecto |
| Responsable técnico | No identificado | Desconocido — sin evidencia en el proyecto |
| Tecnología | Power BI (modelo TMDL, reporte PBIR/PBIP) | Encontrado — `definition.pbism` v4.2, `database.tmdl` compatibilityLevel 1606 |
| Repositorio | Repositorio Git local (`NIGGA`, GitHub `maickmig-coder/NIGGA`) | Encontrado — carpeta `.git` en la raíz del repo |
| Ambiente | No identificado (fuente Athena esquema `bi_materialized_data`) | Inferido — partición M `AmazonAthena.Databases("Athena_ODBC2", ...)` |
| Versión | SemanticModel v4.2 | Encontrado — `definition.pbism` |
| Fecha del censo | 2026-10-02 | Fecha de ejecución del ritual |

Configuración de modelo (evidencia `model.tmdl`): `culture: es-MX`, `sourceQueryCulture: es-CO`, `defaultPowerBIDataSourceVersion: powerBI_V3`, `dataAccessOptions: legacyRedirects, returnErrorValuesAsNull`, `__PBI_TimeIntelligenceEnabled = 1`, `PBI_QueryOrder = ["Entregas Totales","Fecha De Actualización","Val nombres"]`, `PBI_ProTooling = ["DevMode"]`. Rol de seguridad `Todo` con `modelPermission: read` (evidencia `roles/Todo.tmdl`).

# 2. Objetivo y alcance

## Objetivo del BI

Medir el volumen de **unidades/máquinas entregadas** (filtradas a `tipo = "Nuevos"` y `Cantidad = 1`) provenientes de la fuente Athena `entregas_totales`, con tres vistas de negocio: **Renting** (empresas homologadas), **Convenios** y **Empresarial/Flotillas**. Incluye indicadores de distribución trimestral (Q1–Q4), semestral (S1/S2), tasas de recambio y ticket promedio.

## Alcance del censo

- Modelo semántico completo (`GC - Flotillas.SemanticModel`): fuente, transformaciones M, tablas calculadas DAX, columnas, medidas y relaciones.
- Reporte completo (`GC - Flotillas.Report`): 3 páginas y sus visuales (93 contenedores en total), con identificación del título visible de cada uno; 24 bookmarks y navegación.

## Limitaciones

- No se ejecutó el modelo ni se validaron datos reales; el análisis proviene exclusivamente de las definiciones TMDL/PBIR versionadas.
- No se accedió a la fuente Athena (`bi_materialized_data.entregas_totales`); su contenido, propietario y frecuencia de actualización no pueden confirmarse desde el proyecto.
- **Gran parte de los visuales referencia entidades que no existen en el modelo** (`Cultivos`, `RUNT`, `Importaciones`); no es posible determinar su comportamiento ni su origen desde este proyecto (ver §9 y §18).
- El significado funcional de varios canales, estados y clasificaciones se infiere de la lógica técnica y requiere validación con negocio.

# 3. Fuentes de datos

| Fuente | Tipo | Sistema/Esquema | Tabla/Endpoint/Archivo | Método de conexión | Evidencia |
|---|---|---|---|---|---|
| Entregas Totales | Base de datos analítica | `AwsDataCatalog` → `bi_materialized_data` | `entregas_totales` | Amazon Athena vía ODBC (`AmazonAthena.Databases("Athena_ODBC2", null, [])`) | `Entregas Totales.tmdl` partición `m` |
| Val nombres | Datos embebidos | — | Tabla embebida (base64 `Binary.Decompress`) | Power Query (M), `Table.FromRows` | `Val nombres.tmdl` partición `m` |
| Fecha De Actualización | Cálculo local | — | `DateTimeZone.SwitchZone(DateTimeZone.LocalNow(), -5, 0)` | Power Query (M) | `Fecha De Actualización.tmdl` |

- DSN de conexión identificado: **`Athena_ODBC2`**.
- Entidades `Cultivos`, `RUNT`, `Importaciones` aparecen referenciadas en el reporte pero **no tienen fuente, partición ni tabla** en el modelo (ver §9 y §18).

# 4. Transformaciones

| Elemento | Tecnología | Descripción | Fuente | Destino | Evidencia |
|---|---|---|---|---|---|
| Quitar columna `telefono` | Power Query (M) | `Table.RemoveColumns(..., {"telefono"})` | `entregas_totales` | `Entregas Totales` | `Entregas Totales.tmdl` |
| Renombrado de columnas | Power Query (M) | `Table.RenameColumns` (minúsculas origen → PascalCase, p. ej. `fechadecorte`→`FechaDeCorte`) | `entregas_totales` | `Entregas Totales` | `Entregas Totales.tmdl` |
| Conversión de tipos | Power Query (M) | `Table.TransformColumnTypes` (fechas, enteros, texto, número) | `Entregas Totales` | `Entregas Totales` | `Entregas Totales.tmdl` |
| Filtro de cantidad | Power Query (M) | `Table.SelectRows(each [Cantidad] = 1)` | `Entregas Totales` | `Entregas Totales` | `Entregas Totales.tmdl` |
| Filtro de tipo | Power Query (M) | `Table.SelectRows(each [tipo] = "Nuevos")` | `Entregas Totales` | `Entregas Totales` | `Entregas Totales.tmdl` |
| Capitalización de texto | Power Query (M) | `Text.Proper` en `NombreVendedor`, `NombreTercero`, `Gama`, `Modelo` | `Entregas Totales` | `Entregas Totales` | `Entregas Totales.tmdl` |
| `FechaEntregaCliente` a fecha | Power Query (M) | Conversión final `type date` | `Entregas Totales` | `Entregas Totales` | `Entregas Totales.tmdl` |
| Homologación de terceros | DAX / M (tabla embebida) | `Val nombres` mapea `NombreTercero → Val nombre` (empresa de renting) | datos embebidos | `Val nombres` | `Val nombres.tmdl` |
| `val nombre` (columna calc) | DAX | `LOOKUPVALUE('Val nombres'[Val nombre], ...)`; si vacío → `"OTROS"` | `Val nombres`, `Entregas Totales` | `Entregas Totales[val nombre]` | `Entregas Totales.tmdl` |
| `RENTING` (columna calc) | DAX | `IF(val nombre <> "OTROS", "RENTING", "")` | `Entregas Totales` | `Entregas Totales[RENTING]` | `Entregas Totales.tmdl` |
| `Convenios` (columna calc) | DAX | `IF(procedencia = "Convenios", "CONVENIOS", "")` | `Entregas Totales` | `Entregas Totales[Convenios]` | `Entregas Totales.tmdl` |
| `Linea` (columna calc) | DAX | `SWITCH`/`IF` anidado sobre `Marca` + `left(Centro,2)` → Wirtgen / JD Agricola / JD Construccion / Usados | `Entregas Totales` | `Entregas Totales[Linea]` | `Entregas Totales.tmdl` |
| `Región` (columna calc) | DAX | `IF` anidado sobre `Centro` → ciudad (Barranquilla, Bogotá, Cali, …) | `Entregas Totales` | `Entregas Totales[Región]` | `Entregas Totales.tmdl` |
| `Q` (columna calc) | DAX | `"Q" & SWITCH(MONTH(FechaEntregaCliente), …)` → Q1–Q4 | `Entregas Totales` | `Entregas Totales[Q]` | `Entregas Totales.tmdl` |
| `DIVISION S` (columna calc) | DAX | `"S" & SWITCH(MONTH(FechaEntregaCliente), …)` → S1 (ene–jun) / S2 (jul–dic) | `Entregas Totales` | `Entregas Totales[DIVISION S]` | `Entregas Totales.tmdl` |

# 5. Modelo de datos

## Tablas

| Tabla | Tipo/Rol | Granularidad | Visible/Oculta | Descripción | Evidencia |
|---|---|---|---|---|---|
| `Entregas Totales` | Hechos (central) | 1 fila por entrega de unidad nueva (`Cantidad=1`, `tipo="Nuevos"`) | Visible | Base de todos los visuales válidos; aloja también todas las medidas | `Entregas Totales.tmdl` |
| `Val nombres` | Apoyo / homologación | 1 fila por `NombreTercero` homologado | Visible | Mapea terceros a empresa de renting (`Val nombre`) | `Val nombres.tmdl` |
| `Fecha De Actualización` | Parámetro/apoyo | 1 fila (fecha-hora actual, zona -5) | Visible | Usada en tarjetas "Última Actualización" | `Fecha De Actualización.tmdl` |
| `DateTableTemplate_f19d1d27…` | Automática (Time Intelligence) | — | Oculta (sistema) | Plantilla de tabla de fecha | `model.tmdl` |
| `LocalDateTable_…` (×6) | Automáticas (Time Intelligence) | — | Ocultas (sistema) | Generadas por la función de fecha/hora automática | `model.tmdl`, `relationships.tmdl` |

> No existe tabla de calendario de negocio explícita; el análisis temporal se apoya en columnas (`año`, `Q`, `DIVISION S`) y en las jerarquías de fecha automáticas.

## Relaciones

| Desde | Hacia | Cardinalidad | Dirección | Activa | Evidencia |
|---|---|---|---|---|---|
| `Entregas Totales[FechaDeCorte]` | `LocalDateTable_8f7b7b5e…[Date]` | Automática (variation) | — | Sí | `relationships.tmdl` (`772fc70d…`, `datePartOnly`) |
| `Entregas Totales[FechaEntregaCliente]` | `LocalDateTable_db36dc30…[Date]` | Automática (variation) | — | Sí | `relationships.tmdl` (`4358b4ce…`) |
| `Entregas Totales[FechaFactura]` | `LocalDateTable_ebcf95e2…[Date]` | Automática (variation) | — | Sí | `relationships.tmdl` (`58e448f2…`) |
| `Entregas Totales[FechaMod]` | `LocalDateTable_1bea27a1…[Date]` | Automática (variation) | — | Sí | `relationships.tmdl` (`1ce62867…`) |
| `Entregas Totales[fechamatriculacion]` | `LocalDateTable_da3d9bb4…[Date]` | Automática (variation) | — | Sí | `relationships.tmdl` (`094bc577…`) |
| `Fecha De Actualización[Fecha De Actualización]` | `LocalDateTable_27076615…[Date]` | Automática (variation) | — | Sí | `relationships.tmdl` (`fdbeba49…`) |

> Observación: **las 6 relaciones son automáticas de Time Intelligence** (`joinOnDateBehavior: datePartOnly`). **No existe ninguna relación de negocio explícita** entre `Entregas Totales` y `Val nombres`: el cruce se resuelve por `LOOKUPVALUE` en la columna calculada `val nombre` (ver §14).

## Claves y jerarquías

- No hay claves marcadas explícitamente (`isKey`) en las tablas de negocio. `VIN` / `placa` podrían actuar como identificador físico de la unidad, pero no están declarados como clave.
- Jerarquías: solo las jerarquías de fecha automáticas (`'Jerarquía de fechas'`) de cada `LocalDateTable`. No hay jerarquías de usuario definidas.
- Variaciones de fecha (`variation Variación`, `isDefault`) definidas sobre `FechaDeCorte`, `FechaEntregaCliente`, `FechaFactura`, `FechaMod` y `fechamatriculacion`.

# 6. Columnas

## Tabla `Entregas Totales` — columnas de origen (evidencia `Entregas Totales.tmdl`)

| Tabla | Columna | Tipo | Calculada/Origen | Descripción | Utilizada |
|---|---|---|---|---|---|
| Entregas Totales | FechaDeCorte | dateTime | Origen | Fecha de corte de datos | Solo relación auto-fecha |
| Entregas Totales | año | int64 | Origen | Año | Sí — slicers, medidas Año actual/anterior; ⚠ también sumado en cards (ver §18) |
| Entregas Totales | tipo | string | Origen | Tipo (filtrado a "Nuevos") | Uso técnico (filtro M) |
| Entregas Totales | IdEmpresas | int64 | Origen | Id de empresa | No utilizada en visuales |
| Entregas Totales | CodigoEmpresa | int64 | Origen | Código de empresa | No utilizada en visuales |
| Entregas Totales | Empresa | string | Origen | Empresa | No utilizada en visuales |
| Entregas Totales | CodigoCentro | int64 | Origen | Código de centro | No utilizada en visuales |
| Entregas Totales | Centro | string | Origen | Centro/sede | Insumo de `Linea` y `Región`; slicer |
| Entregas Totales | CodigoSeccion | int64 | Origen | Código de sección | No utilizada en visuales |
| Entregas Totales | Seccion | string | Origen | Sección | No utilizada en visuales |
| Entregas Totales | CodigoMarca | int64 | Origen | Código de marca | No utilizada en visuales |
| Entregas Totales | Marca | string | Origen | Marca | Sí — slicer; insumo de `Linea` |
| Entregas Totales | CodigoGama | int64 | Origen | Código de gama | No utilizada en visuales |
| Entregas Totales | Gama | string | Origen | Gama de producto | Sí — slicers, "Penetración de segmentos por Gama" |
| Entregas Totales | CodigoModelo | string | Origen | Código de modelo | No utilizada en visuales |
| Entregas Totales | AñoModelo | string | Origen | Año del modelo | No utilizada en visuales |
| Entregas Totales | Modelo | string | Origen | Modelo | No utilizada en visuales |
| Entregas Totales | CedulaVendedor | string | Origen | Cédula del vendedor | No utilizada en visuales |
| Entregas Totales | NombreVendedor | string | Origen (Text.Proper) | Nombre del vendedor | No utilizada en visuales |
| Entregas Totales | Nit | int64 | Origen | NIT del tercero | No utilizada en visuales |
| Entregas Totales | NombreTercero | string | Origen (Text.Proper) | Nombre del tercero/cliente | Sí — tabla "Unidades por Gama x Tecnología"; insumo de `val nombre` |
| Entregas Totales | Cantidad | int64 | Origen | Cantidad (filtrada a 1) | Uso técnico (filtro de página y M) |
| Entregas Totales | Valor | double | Origen | Valor monetario de la entrega | Sí — card "Utilidad bruta total"; medida Ticket promedio |
| Entregas Totales | FechaEntregaCliente | dateTime | Origen | Fecha de entrega al cliente | Insumo de `Q` y `DIVISION S`; relación auto-fecha |
| Entregas Totales | FechaFactura | dateTime | Origen | Fecha de factura | Solo relación auto-fecha |
| Entregas Totales | FechaMod | dateTime | Origen | Fecha de modificación | Solo relación auto-fecha |
| Entregas Totales | VIN | string | Origen | VIN de la unidad | No utilizada en visuales |
| Entregas Totales | Entrega | string | Origen | Marca/estado de entrega | No utilizada en visuales |
| Entregas Totales | placa | string | Origen | Placa | No utilizada en visuales |
| Entregas Totales | fechamatriculacion | dateTime | Origen | Fecha de matriculación | Solo relación auto-fecha |
| Entregas Totales | combustible | string | Origen | Tipo de combustible | Sí — slicer |
| Entregas Totales | procedencia | string | Origen | Procedencia (incluye "Convenios") | Filtro de página; insumo de `Convenios` |
| Entregas Totales | procedenciadetalle | string | Origen | Detalle de procedencia/convenio | Sí — slicers, cards, pies y tablas de Convenios |
| Entregas Totales | tipooportunidad | string | Origen | Tipo de oportunidad | No utilizada en visuales |
| Entregas Totales | correo | string | Origen | Correo | No utilizada en visuales |
| Entregas Totales | codunidadnegocio | int64 | Origen | Código unidad de negocio | No utilizada en visuales |
| Entregas Totales | nombreunidadnegocio | string | Origen | Unidad de negocio | No utilizada en visuales |
| Entregas Totales | tipocliente | string | Origen | Tipo de cliente | No utilizada en visuales |
| Entregas Totales | nombrevendedorhomologado | string | Origen | Vendedor homologado | No utilizada en visuales |
| Entregas Totales | clase | string | Origen | Clase de la unidad | No utilizada en visuales |
| Entregas Totales | color | string | Origen | Color | No utilizada en visuales |
| Entregas Totales | esultimamodificacion | int64 | Origen | Bandera última modificación | No utilizada en visuales |
| Entregas Totales | rowhash | string | Origen | Hash de fila | No utilizada en visuales |
| Entregas Totales | extractionid | int64 | Origen | Id de extracción | No utilizada en visuales |
| Entregas Totales | emailvendedor | string | Origen | Email del vendedor | No utilizada en visuales |
| Entregas Totales | tipoventa_vista | string | Origen | Clasificación de tipo de venta (Flotas/Flotilla) | Filtro de página (Empresas) |

## Tabla `Entregas Totales` — columnas calculadas (DAX)

| Tabla | Columna | Definición (resumen) | Rol | Utilizada |
|---|---|---|---|---|
| Entregas Totales | Linea | `SWITCH`/`IF` sobre `Marca` + `left(Centro,2)<>"VO"` → Wirtgen/JD Agricola/JD Construccion/Usados | Clasificación de línea de negocio | No vista en visuales |
| Entregas Totales | Región | `IF` anidado sobre `Centro` → ciudad | Homologación geográfica | Sí — slicer "Región" (pág. Empresas) |
| Entregas Totales | Q | `"Q"&SWITCH(MONTH(FechaEntregaCliente),…)` | Trimestre | Sí — slicers y series Q |
| Entregas Totales | DIVISION S | `"S"&SWITCH(MONTH(FechaEntregaCliente),…)` | Semestre (S1/S2) | Sí — series S (medidas S1/S2) |
| Entregas Totales | val nombre | `LOOKUPVALUE('Val nombres'[Val nombre],…)`, vacío→"OTROS" | Empresa de renting homologada | Sí — tablas/cards Renting, filtros de página |
| Entregas Totales | RENTING | `IF(val nombre<>"OTROS","RENTING","")` | Bandera de renting | No vista en visuales |
| Entregas Totales | Convenios | `IF(procedencia="Convenios","CONVENIOS","")` | Bandera de convenio | No vista en visuales |

## Tabla `Val nombres`

| Tabla | Columna | Tipo | Calculada/Origen | Descripción | Utilizada |
|---|---|---|---|---|---|
| Val nombres | NombreTercero | string | Origen (embebido) | Nombre del tercero | Insumo de `LOOKUPVALUE` |
| Val nombres | Val nombre | string | Origen (embebido) | Empresa de renting homologada | Insumo de `val nombre` |

## Tabla `Fecha De Actualización`

| Tabla | Columna | Tipo | Calculada/Origen | Descripción | Utilizada |
|---|---|---|---|---|---|
| Fecha De Actualización | Fecha De Actualización | dateTime | Origen (M, LocalNow -5) | Fecha-hora de actualización | Sí — cards "Última Actualización" |

# 7. Medidas

Todas las medidas residen en la tabla `Entregas Totales` (evidencia `Entregas Totales.tmdl`).

| Medida | Tabla | Fórmula/Resumen | Uso | KPI/Análisis | Evidencia |
|---|---|---|---|---|---|
| cantidad de maquinas | Entregas Totales | `IF(COUNTROWS('Entregas Totales')=0,0,COUNTROWS('Entregas Totales'))` | Conteo de unidades | KPI principal de volumen | `Entregas Totales.tmdl` |
| Medida | Entregas Totales | (sin expresión; medida vacía) | — | — | `Entregas Totales.tmdl` |
| S1 | Entregas Totales | `CALCULATE([cantidad de maquinas], 'Entregas Totales'[DIVISION S]="S1")` | Unidades 1er semestre | Insumo de recambio semestral | `Entregas Totales.tmdl` |
| S2 | Entregas Totales | `CALCULATE([cantidad de maquinas], 'Entregas Totales'[DIVISION S]="S2")` | Unidades 2do semestre | Insumo de recambio semestral | `Entregas Totales.tmdl` |
| Recambio semestral | Entregas Totales | `(S2-S1)/S2` (con tope en 0) | Variación semestral | KPI de recambio | `Entregas Totales.tmdl` |
| Año actual | Entregas Totales | `CALCULATE([cantidad de maquinas], año=MAX(año))` | Unidades año máximo | Insumo recambio anual | `Entregas Totales.tmdl` |
| Año Anterior | Entregas Totales | `CALCULATE([cantidad de maquinas], año=MAX(año)-1)` | Unidades año previo | Insumo recambio anual | `Entregas Totales.tmdl` |
| Medida 2 | Entregas Totales | `CALCULATE([cantidad de maquinas], año=MAX(año)-1)` (idéntica a "Año Anterior") | — | — (duplicada) | `Entregas Totales.tmdl` |
| Recambio anual (vs año ant.) | Entregas Totales | `(Año actual-Año Anterior)/Año Anterior` (tope 1) | Variación anual | KPI de recambio | `Entregas Totales.tmdl` |
| Q1 / Q2 / Q3 / Q4 | Entregas Totales | `CALCULATE([cantidad de maquinas], 'Entregas Totales'[Q]="Qn")` | Unidades por trimestre | Análisis trimestral | `Entregas Totales.tmdl` |
| Crecimiento Q1→Q4 | Entregas Totales | `(Q4-Q1)/Q1` (tope 1) | Crecimiento trimestral | KPI de crecimiento | `Entregas Totales.tmdl` |
| Ticket promedio | Entregas Totales | `SUM('Entregas Totales'[Valor])/[cantidad de maquinas]` | Valor medio por unidad | KPI de valor | `Entregas Totales.tmdl` |

# 8. Páginas

| Página (displayName) | Visible | Objetivo | Navegación | Evidencia |
|---|---|---|---|---|
| Dashboard_Renting | Visible (activa) | Unidades de renting por empresa homologada, trimestre y KPIs | Interacciones de slicers; sin botones de navegación propios | `pages/ac291ea509382034e4ab/page.json` |
| Dashboard_Convenios | Visible | Unidades por convenio (procedencia="Convenios"), S1 vs S2 y recambio | Interacciones de slicers | `pages/b597e26007760b8239c0/page.json` |
| Dashboard_Empresas | Visible | Ventas empresariales/flotillas por `tipoventa_vista` | Botón "Conectividad" (PageNavigation + bookmark) | `pages/377df594a011ae294444/page.json` |

> `pageOrder = [Renting, Convenios, Empresas]`; `activePageName = ac291ea509382034e4ab` (Renting). Ninguna página está marcada como oculta. Todas aplican el filtro de página `Entregas Totales[Cantidad]` y filtros específicos de canal (ver §11).

# 9. Visuales

> Nombre del visual = **título visible** configurado en el contenedor (`visualContainerObjects.title[0].properties.text.expr.Literal.Value`). Donde no existe título literal se registra `Sin título visible` (no se inventan nombres), conforme al ritual.
>
> ⚠ **Entidades inexistentes:** los campos marcados con `Cultivos[...]`, `RUNT[...]` e `Importaciones[...]` referencian tablas que **no existen** en el modelo semántico de este BI. Esos visuales están rotos/huérfanos (ver §18).

## Página Dashboard_Renting (30 contenedores)

| Página | Nombre del visual | Tipo de visual | Campos/Categorías | Medidas | Filtros | Propósito/Notas |
|---|---|---|---|---|---|---|
| Renting | Matriculas por marca | treemap | ⚠ `RUNT[MARCA]` | ⚠ `RUNT[CTD]` | Slicers | Entidad inexistente |
| Renting | Matriculas por modelo | treemap | ⚠ `RUNT[MODELO]` | ⚠ `RUNT[CTD]` | Slicers | Entidad inexistente |
| Renting | Matriculas Runt | tableEx | ⚠ `RUNT[MUNICIPIO/MERCADO/MARCA/MODELO/CAPACIDAD]` | ⚠ `RUNT[CTD]` | Slicers | Entidad inexistente |
| Renting | Importaciones | lineClusteredColumnComboChart | ⚠ `Importaciones[MARCA]` | ⚠ `Importaciones[CTD]` | Slicers | Entidad inexistente |
| Renting | Importaciones (CIF) | lineClusteredColumnComboChart | ⚠ `Importaciones[MARCA]` | ⚠ `Importaciones[CIF TOTAL USD]` | Slicers | Entidad inexistente |
| Renting | Especificación Importadores | tableEx | ⚠ `Importaciones[IMPORTADOR/MARCA/MERCADO/MODELO/CAPACIDAD]` | ⚠ `Importaciones[CTD]` | Slicers | Entidad inexistente |
| Renting | Rendimiento (t/ha) | lineClusteredColumnComboChart | ⚠ `Cultivos[Municipio/Val periodo/Desagregación cultivo]` | ⚠ `Cultivos[Rendimiento (t/ha)]` | Slicers | Entidad inexistente |
| Renting | Producción (T) | lineClusteredColumnComboChart | ⚠ `Cultivos[Municipio/Val periodo]` | ⚠ `Cultivos[Producción (t)]` | Slicers | Entidad inexistente |
| Renting | Mecanización por regional | barChart | ⚠ `Cultivos[Regional/municipios mecanizables]` | ⚠ `Cultivos[Área sembrada (ha)]` | Slicers | Entidad inexistente |
| Renting | Mecanizacion por departamento | barChart | ⚠ `Cultivos[Departamento/municipios mecanizables]` | ⚠ `Cultivos[Área sembrada (ha)]` | Slicers | Entidad inexistente |
| Renting | Participación por cultivo área sembrada has (TOP 5) | pieChart | ⚠ `Cultivos[Desagregación cultivo]` | ⚠ `Cultivos[Área sembrada (ha)]` | Slicers | Entidad inexistente |
| Renting | Participación por mecanización | pieChart | ⚠ `Cultivos[municipios mecanizables]` | ⚠ `Cultivos[Área sembrada (ha)]` | Slicers | Entidad inexistente |
| Renting | Unidades facturadas por empresa de Renting y trimestre | tableEx | `Entregas Totales[val nombre]` | Q1, Q2, Q3, Q4, cantidad de maquinas, Crecimiento Q1→Q4 | Slicers | **Visual válido** sobre el modelo |
| Renting | Unidades RENTING por empresa y trimestre | lineClusteredColumnComboChart | `Entregas Totales[val nombre]`, `Entregas Totales[Q]` | cantidad de maquinas | Slicers | **Visual válido** |
| Renting | Total unidades renting | card | — | cantidad de maquinas | Slicers | KPI válido |
| Renting | Utilidad bruta total | card | `Sum(Entregas Totales[Valor])` | — | Slicers | KPI válido |
| Renting | Ticket promedio | card | — | Ticket promedio | Slicers | KPI válido |
| Renting | Empresas renting activas | card | `Min(Entregas Totales[val nombre])` | — | Slicers | ⚠ `Min` sobre texto, no cuenta empresas (ver §18) |
| Renting | Última Actualización | card | `Fecha De Actualización` | — | — | Fecha de referencia |
| Renting | Sin título visible | slicer | `Entregas Totales[año]` | — | — | Segmentación por año |
| Renting | Sin título visible | slicer | `Entregas Totales[Marca]` | — | — | Segmentación por marca |
| Renting | Sin título visible | slicer | `Entregas Totales[Centro]` | — | — | Segmentación por centro |
| Renting | Sin título visible | slicer | `Entregas Totales[Gama]` | — | — | Segmentación por gama |
| Renting | Sin título visible | slicer | `Entregas Totales[Q]` | — | — | Segmentación por trimestre |
| Renting | Sin título visible | slicer | `Entregas Totales[combustible]` | — | — | Segmentación por combustible |
| Renting | Sin título visible | image (×2) | — | — | — | Logos/elementos gráficos |
| Renting | Sin título visible | shape (×2) | — | — | — | Elementos gráficos |
| Renting | Sin título visible | textbox | — | — | — | Rótulo |

## Página Dashboard_Convenios (31 contenedores)

| Página | Nombre del visual | Tipo de visual | Campos/Categorías | Medidas | Filtros | Propósito/Notas |
|---|---|---|---|---|---|---|
| Convenios | Unidades por convenio: S1 vs S2 | lineClusteredColumnComboChart | `Entregas Totales[procedenciadetalle]`, `Entregas Totales[DIVISION S]` | cantidad de maquinas | Filtro de página + slicers | **Visual válido** |
| Convenios | Participación por convenio (unidades año) | pieChart | `Entregas Totales[procedenciadetalle]` | cantidad de maquinas | Filtro de página + slicers | **Visual válido** |
| Convenios | Participación por convenio y tasa de recambio | tableEx | `Entregas Totales[procedenciadetalle]` | Q1–Q4, cantidad de maquinas, Recambio semestral, Recambio anual (vs año ant.) | Filtro de página + slicers | **Visual válido** |
| Convenios | Total unidades convenios | card | `Sum(Entregas Totales[año])` | — | Filtro de página | ⚠ Suma el campo `año` (ver §18) |
| Convenios | Convenios vigentes hoy | card | `Min(Entregas Totales[procedenciadetalle])` | — | Filtro de página | ⚠ `Min` sobre texto (ver §18) |
| Convenios | Utilidad bruta total | card | `Sum(Entregas Totales[Valor])` | — | Filtro de página | KPI válido |
| Convenios | Última Actualización | card | `Fecha De Actualización` | — | — | Fecha de referencia |
| Convenios | Matriculas por marca | treemap | ⚠ `RUNT[MARCA]` | ⚠ `RUNT[CTD]` | Slicers | Entidad inexistente |
| Convenios | Matriculas por modelo | treemap | ⚠ `RUNT[MODELO]` | ⚠ `RUNT[CTD]` | Slicers | Entidad inexistente |
| Convenios | Matriculas Runt | tableEx | ⚠ `RUNT[…]` | ⚠ `RUNT[CTD]` | Slicers | Entidad inexistente |
| Convenios | Importaciones | lineClusteredColumnComboChart | ⚠ `Importaciones[MARCA]` | ⚠ `Importaciones[CTD]` | Slicers | Entidad inexistente |
| Convenios | Importaciones (CIF) | lineClusteredColumnComboChart | ⚠ `Importaciones[MARCA]` | ⚠ `Importaciones[CIF TOTAL USD]` | Slicers | Entidad inexistente |
| Convenios | Especificación Importadores | tableEx | ⚠ `Importaciones[…]` | ⚠ `Importaciones[CTD]` | Slicers | Entidad inexistente |
| Convenios | Rendimiento (t/ha) | lineClusteredColumnComboChart | ⚠ `Cultivos[…]` | ⚠ `Cultivos[Rendimiento (t/ha)]` | Slicers | Entidad inexistente |
| Convenios | Producción (T) | lineClusteredColumnComboChart | ⚠ `Cultivos[…]` | ⚠ `Cultivos[Producción (t)]` | Slicers | Entidad inexistente |
| Convenios | Mecanización por regional | barChart | ⚠ `Cultivos[…]` | ⚠ `Cultivos[Área sembrada (ha)]` | Slicers | Entidad inexistente |
| Convenios | Mecanizacion por departamento | barChart | ⚠ `Cultivos[…]` | ⚠ `Cultivos[Área sembrada (ha)]` | Slicers | Entidad inexistente |
| Convenios | Participación por cultivo área sembrada has (TOP 5) | pieChart | ⚠ `Cultivos[Desagregación cultivo]` | ⚠ `Cultivos[Área sembrada (ha)]` | Slicers | Entidad inexistente |
| Convenios | Participación por mecanización | pieChart | ⚠ `Cultivos[municipios mecanizables]` | ⚠ `Cultivos[Área sembrada (ha)]` | Slicers | Entidad inexistente |
| Convenios | Sin título visible | slicer | `Entregas Totales[procedenciadetalle]` | — | — | Segmentación por convenio |
| Convenios | Sin título visible | slicer | `Entregas Totales[año]` | — | — | Segmentación por año |
| Convenios | Sin título visible | slicer | `Entregas Totales[Marca]` | — | — | Segmentación por marca |
| Convenios | Sin título visible | slicer | `Entregas Totales[Centro]` | — | — | Segmentación por centro |
| Convenios | Sin título visible | slicer | `Entregas Totales[Gama]` | — | — | Segmentación por gama |
| Convenios | Sin título visible | slicer | `Entregas Totales[Q]` | — | — | Segmentación por trimestre |
| Convenios | Sin título visible | slicer | `Entregas Totales[combustible]` | — | — | Segmentación por combustible |
| Convenios | Sin título visible | image (×2) | — | — | — | Logos/elementos gráficos |
| Convenios | Sin título visible | shape (×2) | — | — | — | Elementos gráficos |
| Convenios | Sin título visible | textbox | — | — | — | Rótulo |

## Página Dashboard_Empresas (32 contenedores)

| Página | Nombre del visual | Tipo de visual | Campos/Categorías | Medidas | Filtros | Propósito/Notas |
|---|---|---|---|---|---|---|
| Empresas | Unidades por Gama x Tecnología (VENTA EMPRESARIAL) | tableEx | `Entregas Totales[NombreTercero]` | Q1–Q4, cantidad de maquinas | Filtro de página + slicers | **Visual válido** |
| Empresas | Penetración de segmentos por Gama | lineClusteredColumnComboChart | `Entregas Totales[Gama]`, `Entregas Totales[Q]` | cantidad de maquinas | Filtro de página + slicers | **Visual válido** |
| Empresas | Total unidades empresarial | card | `Sum(Entregas Totales[año])` | — | Filtro de página | ⚠ Suma el campo `año` (ver §18) |
| Empresas | Ticket promedio | card | `Sum(Entregas Totales[año])` | — | Filtro de página | ⚠ Título "Ticket promedio" pero suma `año` (ver §18) |
| Empresas | Empresas distintas | card | `Min(Entregas Totales[procedenciadetalle])` | — | Filtro de página | ⚠ `Min` sobre texto (ver §18) |
| Empresas | Utilidad bruta total | card | `Sum(Entregas Totales[Valor])` | — | Filtro de página | KPI válido |
| Empresas | Última Actualización | card | `Fecha De Actualización` | — | — | Fecha de referencia |
| Empresas | Matriculas por marca | treemap | ⚠ `RUNT[MARCA]` | ⚠ `RUNT[CTD]` | Slicers | Entidad inexistente |
| Empresas | Matriculas por modelo | treemap | ⚠ `RUNT[MODELO]` | ⚠ `RUNT[CTD]` | Slicers | Entidad inexistente |
| Empresas | Matriculas Runt | tableEx | ⚠ `RUNT[…]` | ⚠ `RUNT[CTD]` | Slicers | Entidad inexistente |
| Empresas | Importaciones | lineClusteredColumnComboChart | ⚠ `Importaciones[MARCA]` | ⚠ `Importaciones[CTD]` | Slicers | Entidad inexistente |
| Empresas | Importaciones (CIF) | lineClusteredColumnComboChart | ⚠ `Importaciones[MARCA]` | ⚠ `Importaciones[CIF TOTAL USD]` | Slicers | Entidad inexistente |
| Empresas | Especificación Importadores | tableEx | ⚠ `Importaciones[…]` | ⚠ `Importaciones[CTD]` | Slicers | Entidad inexistente |
| Empresas | Rendimiento (t/ha) | lineClusteredColumnComboChart | ⚠ `Cultivos[…]` | ⚠ `Cultivos[Rendimiento (t/ha)]` | Slicers | Entidad inexistente |
| Empresas | Producción (T) | lineClusteredColumnComboChart | ⚠ `Cultivos[…]` | ⚠ `Cultivos[Producción (t)]` | Slicers | Entidad inexistente |
| Empresas | Mecanización por regional | barChart | ⚠ `Cultivos[…]` | ⚠ `Cultivos[Área sembrada (ha)]` | Slicers | Entidad inexistente |
| Empresas | Mecanizacion por departamento | barChart | ⚠ `Cultivos[…]` | ⚠ `Cultivos[Área sembrada (ha)]` | Slicers | Entidad inexistente |
| Empresas | Participación por cultivo área sembrada has (TOP 5) | pieChart | ⚠ `Cultivos[Desagregación cultivo]` | ⚠ `Cultivos[Área sembrada (ha)]` | Slicers | Entidad inexistente |
| Empresas | Participación por mecanización | pieChart | ⚠ `Cultivos[municipios mecanizables]` | ⚠ `Cultivos[Área sembrada (ha)]` | Slicers | Entidad inexistente |
| Empresas | Sin título visible | slicer | `Entregas Totales[año]` | — | — | Segmentación por año |
| Empresas | Sin título visible | slicer | `Entregas Totales[Marca]` | — | — | Segmentación por marca |
| Empresas | Sin título visible | slicer | `Entregas Totales[Gama]` | — | — | Segmentación por gama |
| Empresas | Sin título visible | slicer | `Entregas Totales[Q]` (×2) | — | — | Segmentación por trimestre |
| Empresas | Sin título visible | slicer | `Entregas Totales[combustible]` | — | — | Segmentación por combustible |
| Empresas | Sin título visible | slicer | `Entregas Totales[Región]` | — | — | Segmentación por región |
| Empresas | Sin título visible | actionButton ("Conectividad") | — | — | — | Navegación por bookmark (PageNavigation) |
| Empresas | Sin título visible | image (×2) | — | — | — | Logos/elementos gráficos |
| Empresas | Sin título visible | shape (×2) | — | — | — | Elementos gráficos |
| Empresas | Sin título visible | textbox | — | — | — | Rótulo |

> Nota de método: el título visible se tomó del `title` de cada `visual.json`. El texto del `actionButton` ("Conectividad") proviene de `objects.text` (no de `title`), por eso figura como `Sin título visible` en la columna de título.

# 10. KPIs

| KPI | Fórmula | Definición técnica | Interpretación funcional | Evidencia |
|---|---|---|---|---|
| cantidad de maquinas | `IF(COUNTROWS=0,0,COUNTROWS('Entregas Totales'))` | Conteo de filas de entregas | Unidades/máquinas entregadas | `Entregas Totales.tmdl` |
| Ticket promedio | `SUM(Valor)/[cantidad de maquinas]` | Valor total / unidades | Valor medio por unidad | `Entregas Totales.tmdl` |
| Recambio semestral | `(S2-S1)/S2` | Variación entre semestres | Ritmo de recambio semestral | `Entregas Totales.tmdl` |
| Recambio anual (vs año ant.) | `(Año actual-Año Anterior)/Año Anterior` | Variación interanual (tope 1) | Ritmo de recambio anual | `Entregas Totales.tmdl` |
| Crecimiento Q1→Q4 | `(Q4-Q1)/Q1` | Variación entre Q1 y Q4 (tope 1) | Crecimiento intra-anual | `Entregas Totales.tmdl` |
| Q1–Q4 | `CALCULATE(cantidad de maquinas, Q="Qn")` | Conteo por trimestre | Volumen trimestral | `Entregas Totales.tmdl` |

# 11. Filtros y segmentaciones

| Página | Filtro/Slicer | Campo | Tipo | Impacto | Evidencia |
|---|---|---|---|---|---|
| Todas | Filtro de página | `Entregas Totales[Cantidad]` | Categórico | Presente en las 3 páginas | `page.json` de cada página |
| Dashboard_Renting | Filtro de página | `Entregas Totales[val nombre]` NOT IN "OTROS" (selección invertida) | Categórico | Limita a empresas de renting homologadas | `ac291…/page.json` |
| Dashboard_Convenios | Filtro de página | `Entregas Totales[procedencia]` IN "Convenios" | Categórico | Limita a procedencia Convenios | `b597…/page.json` |
| Dashboard_Convenios | Filtro de página | `Entregas Totales[procedenciadetalle]` NOT IN null (invertido) | Categórico | Excluye convenios sin detalle | `b597…/page.json` |
| Dashboard_Empresas | Filtro de página | `Entregas Totales[tipoventa_vista]` IN "Flotas - Oficial", "Flotas de Proximidad Oficial", "Flotas Oficial", "Flotilla Coorporativa" | Categórico | Limita a ventas de flota/flotilla | `377df…/page.json` |
| Dashboard_Empresas | Filtro de página | `Entregas Totales[val nombre]` IN "OTROS" | Categórico | Excluye empresas de renting (complemento de Renting) | `377df…/page.json` |
| Dashboard_Empresas | Filtro de página | `Entregas Totales[procedencia]` (selección invertida) | Categórico | Exclusión de procedencias | `377df…/page.json` |
| Todas | Slicers | año, Marca, Centro, Gama, Q, combustible, Región, procedenciadetalle | Categórico/lista | Segmentación cruzada | `visual.json` de cada slicer |

> Hallazgo de consistencia: los slicers **no tienen título visible**; su campo se identifica por la proyección `Values`. La definición de "canal" se reparte entre tres columnas distintas (`val nombre`, `procedencia`, `tipoventa_vista`) a nivel de filtro de página (ver §14 y §18).

# 12. Elementos utilizados

| Elemento | Tabla/Objeto | Tipo | Dónde se utiliza | Función | Evidencia |
|---|---|---|---|---|---|
| cantidad de maquinas | Entregas Totales | Medida | Cards, tablas, combo charts | KPI de volumen | `visual.json` varios |
| Ticket promedio | Entregas Totales | Medida | Card "Ticket promedio" (Renting) | Valor medio por unidad | `edd05e9b…` |
| Q1–Q4, Crecimiento Q1→Q4 | Entregas Totales | Medidas | Tablas trimestrales | Análisis trimestral | `3481c97f…`, `eea79056…` |
| Recambio semestral / anual | Entregas Totales | Medidas | Tabla "Participación por convenio y tasa de recambio" | Recambio | `eea79056…` |
| val nombre | Entregas Totales | Columna calc | Tablas/combo Renting, filtro de página | Empresa de renting | `3481c97f…`, `5ce335d4…` |
| procedenciadetalle | Entregas Totales | Columna | Slicers, cards, pies y tablas de Convenios | Convenio | `9fd256fc…`, `2706c287…` |
| NombreTercero | Entregas Totales | Columna | Tabla "Unidades por Gama x Tecnología" | Cliente/empresa | `a9dd82c5…` |
| Gama | Entregas Totales | Columna | Slicers, "Penetración de segmentos por Gama" | Gama de producto | `ff5b3bbb…` |
| Q, DIVISION S | Entregas Totales | Columnas calc | Series de combo charts, slicers | Trimestre/semestre | `5ce335d4…`, `2706c287…` |
| Marca, Centro, combustible, año, Región | Entregas Totales | Columnas | Slicers | Segmentación | `visual.json` varios |
| Valor | Entregas Totales | Columna | Card "Utilidad bruta total" | Valor monetario | `918d2283…`, `5f7e3e00…`, `856aee5d…` |
| Fecha De Actualización | Fecha De Actualización | Columna | Cards "Última Actualización" | Referencia de fecha | `9734d282…`, `9769d855…`, `207ac3ee…` |

# 13. Elementos NO utilizados

| Elemento | Tabla/Objeto | Tipo | Evidencia de no uso | Clasificación | Requiere validación |
|---|---|---|---|---|---|
| Medida (vacía) | Entregas Totales | Medida | Sin expresión y sin `queryRef` en visuales | Posible obsoleto | Sí |
| Medida 2 | Entregas Totales | Medida | Duplica a "Año Anterior"; sin uso en visuales | Posible obsoleto | Sí |
| Año actual / Año Anterior / S1 / S2 | Entregas Totales | Medidas | Solo se usan dentro de otras medidas, no directamente en visuales | Uso técnico (intermedio) | No |
| Linea | Entregas Totales | Columna calc | Sin `queryRef` en visuales | No utilizado | Sí |
| RENTING | Entregas Totales | Columna calc | Sin `queryRef` (el canal se filtra por `val nombre`) | No utilizado | Sí |
| Convenios | Entregas Totales | Columna calc | Sin `queryRef` (el canal se filtra por `procedencia`) | No utilizado | Sí |
| IdEmpresas, CodigoEmpresa, Empresa, CodigoCentro, CodigoSeccion, Seccion, CodigoMarca, CodigoGama, CodigoModelo, AñoModelo, Modelo, CedulaVendedor, NombreVendedor, Nit | Entregas Totales | Columnas | Sin `queryRef` en visuales | No utilizado | Sí |
| VIN, Entrega, placa, tipooportunidad, correo, codunidadnegocio, nombreunidadnegocio, tipocliente, nombrevendedorhomologado, clase, color, esultimamodificacion, rowhash, extractionid, emailvendedor | Entregas Totales | Columnas | Sin `queryRef` en visuales | No utilizado | Sí |
| FechaDeCorte, FechaFactura, FechaMod, fechamatriculacion | Entregas Totales | Columnas | Solo en relaciones auto-fecha; no en visuales | Uso técnico | Sí |
| LocalDateTable_* (×6), DateTableTemplate_* | Tablas auto | Tabla oculta | Generadas por Time Intelligence | Uso técnico / posible obsoleto | Sí |
| Visuales `shape`/`image`/`textbox` sin título | Reporte | Contenedores | Sin datos ni consumo de medida | Uso técnico (decorativo) | No |
| Visuales de `Cultivos` / `RUNT` / `Importaciones` | Reporte | Contenedores | Referencian entidades inexistentes | **Rotos / huérfanos** | Sí |
| Custom visuals `PBI_CV_EB3A4088…` y `deneb…` | Reporte | Visuales declarados | Declarados en `report.json` pero sin contenedor que los use | Posible obsoleto | Sí |

> Nota: "No utilizado" no implica que el elemento deba eliminarse. Es un hallazgo del censo que requiere validación funcional/técnica.

# 14. Reglas de negocio

| Regla | Implementación técnica | Interpretación funcional | Evidencia | Estado |
|---|---|---|---|---|
| Universo = unidades nuevas | `Table.SelectRows([Cantidad]=1)` + `Table.SelectRows([tipo]="Nuevos")` | El BI solo considera entregas de unidades nuevas, una por fila | `Entregas Totales.tmdl` | Encontrado |
| Homologación de empresa de renting | `val nombre = LOOKUPVALUE('Val nombres'[Val nombre], ...)`; vacío → "OTROS" | Un tercero se asocia a una empresa de renting; si no está mapeado, "OTROS" | `Entregas Totales.tmdl`, `Val nombres.tmdl` | Encontrado |
| Canal Renting | Filtro de página `val nombre <> "OTROS"` | La vista Renting excluye terceros no homologados | `ac291…/page.json` | Encontrado |
| Canal Convenios | Filtro de página `procedencia = "Convenios"` | La vista Convenios se limita a procedencia Convenios | `b597…/page.json` | Encontrado |
| Canal Empresarial/Flotilla | Filtro de página `tipoventa_vista IN (Flotas…, Flotilla Coorporativa)` + `val nombre = "OTROS"` | Ventas de flota oficial/flotilla no clasificadas como renting | `377df…/page.json` | Encontrado |
| Trimestre (Q) | `"Q"&SWITCH(MONTH(FechaEntregaCliente), …)` | Mapea mes de entrega a trimestre calendario | `Entregas Totales.tmdl` | Encontrado |
| Semestre (DIVISION S) | `"S"&SWITCH(MONTH(FechaEntregaCliente), …)` | S1 = ene–jun, S2 = jul–dic | `Entregas Totales.tmdl` | Encontrado |
| Línea de negocio | `SWITCH`/`IF` sobre `Marca` + `left(Centro,2)<>"VO"` | Agrupa marcas en Wirtgen / JD Agricola / JD Construccion / Usados | `Entregas Totales.tmdl` | Encontrado (no usada en visuales) |
| Homologación geográfica (Región) | `IF` anidado sobre `Centro` → ciudad | Normaliza centros a ciudad/región | `Entregas Totales.tmdl` | Encontrado |
| Recambio semestral | `(S2-S1)/S2`, con piso en 0 | Variación de volumen entre semestres | `Entregas Totales.tmdl` | Encontrado |
| Recambio anual | `(Año actual-Año Anterior)/Año Anterior`, tope en 1 | Variación interanual acotada al 100% | `Entregas Totales.tmdl` | Encontrado |

# 15. Dependencias

```text
Athena (ODBC "Athena_ODBC2")
   └─ AwsDataCatalog > bi_materialized_data > entregas_totales
        └─ Power Query: quita 'telefono' → renombra → tipos → filtra (Cantidad=1, tipo="Nuevos") → Text.Proper
             └─ Tabla 'Entregas Totales'
                  ├─ Columnas origen (año, Valor, Marca, Centro, Gama, procedencia, procedenciadetalle, tipoventa_vista, NombreTercero, FechaEntregaCliente, …)
                  ├─ Columnas calc:
                  │     ├─ Q, DIVISION S           ← FechaEntregaCliente
                  │     ├─ Linea, Región           ← Marca, Centro
                  │     ├─ val nombre              ← LOOKUPVALUE('Val nombres')
                  │     ├─ RENTING                 ← val nombre
                  │     └─ Convenios               ← procedencia
                  └─ Medidas:
                        ├─ cantidad de maquinas    → cards, tablas, combos
                        ├─ S1/S2 → Recambio semestral
                        ├─ Año actual/Anterior → Recambio anual
                        ├─ Q1–Q4 → Crecimiento Q1→Q4
                        └─ Ticket promedio ← SUM(Valor) / cantidad de maquinas

'Val nombres' (datos embebidos)  ──(LOOKUPVALUE)──►  Entregas Totales[val nombre]
'Fecha De Actualización' (M, LocalNow-5)  ──►  cards "Última Actualización"

Páginas:
   Dashboard_Renting   ← filtro val nombre<>OTROS   → visuales válidos (val nombre × Q)
   Dashboard_Convenios ← filtro procedencia=Convenios→ visuales válidos (procedenciadetalle × S/Q)
   Dashboard_Empresas  ← filtro tipoventa_vista + val nombre=OTROS → visuales válidos (NombreTercero/Gama × Q)

⚠ Dependencias ROTAS (sin origen en el modelo):
   Cultivos[…], RUNT[…], Importaciones[…]  → ~57 visuales (treemaps, combos, tablas, pies) en las 3 páginas
```

# 16. Vacíos de información

| Vacío | Por qué es relevante | Evidencia | Impacto | Requiere validación |
|---|---|---|---|---|
| Propietario/responsable del BI | No hay gobierno identificado | Sin metadatos de autor | Medio | Sí |
| Origen de `Cultivos`, `RUNT`, `Importaciones` | ~57 visuales dependen de ellas y no existen en el modelo | `grep` sin coincidencias; listado de `tables/` | Alto | Sí |
| Frecuencia de actualización | No se puede inferir del proyecto | Partición import, sin schedule | Medio | Sí |
| Definición funcional de canales | "Renting", "Convenios", "Empresarial" se derivan de 3 columnas distintas | Filtros de página | Alto | Sí |
| Granularidad real de `entregas_totales` | Se asume 1 fila = 1 unidad por `Cantidad=1`, no confirmado con datos | Filtro M | Medio | Sí |
| Significado de `tipoventa_vista` y sus valores | Determina el universo de la página Empresas | `377df…/page.json` | Medio | Sí |
| Propósito de las tarjetas con `Min`/`Sum(año)` | Los cálculos no corresponden al título | `visual.json` cards | Alto | Sí |

# 17. Propuestas de revisión IA

| Propuesta | Categoría | Motivo | Evidencia | Impacto | Prioridad | Requiere validación |
|---|---|---|---|---|---|---|
| Revisar los visuales que referencian `Cultivos`, `RUNT` e `Importaciones` | E. Reporte / B. Datos | Esas tablas no existen en el modelo; los visuales no pueden renderizar datos | `grep` sin coincidencias; 57 visuales afectados | Alto | Alta | Sí |
| Revisar las tarjetas "Total unidades …", "Ticket promedio" (Empresas), "Empresas …", "Convenios vigentes hoy" | D. Negocio / E. Reporte | El cálculo (`Sum(año)` o `Min(texto)`) no corresponde al título; el KPI mostrado sería incorrecto | `visual.json` de cada card | Alto | Alta | Sí |
| Confirmar la definición funcional de los tres canales (Renting/Convenios/Empresarial) | D. Negocio | Se derivan de columnas distintas (`val nombre`, `procedencia`, `tipoventa_vista`); posible solape o huecos | Filtros de página | Alto | Alta | Sí |
| Revisar medidas sin uso ni expresión ("Medida", "Medida 2") | C. Modelo | "Medida" está vacía y "Medida 2" duplica "Año Anterior" | `Entregas Totales.tmdl` | Bajo | Media | Sí |
| Revisar los custom visuals declarados sin uso | E. Reporte | `report.json` declara 2 custom visuals (incl. Deneb) sin contenedor que los consuma | `report.json` `publicCustomVisuals` | Bajo | Baja | Sí |
| Documentar origen y frecuencia de `entregas_totales` | F. Actualización / B. Datos | No hay información de refresco ni propietario | Partición M | Medio | Media | Sí |
| Añadir títulos visibles a los slicers | E. Reporte / G. Calidad | Ningún slicer tiene título; dificulta la lectura | `visual.json` de slicers | Bajo | Baja | No |
| Evaluar relación de negocio `Entregas Totales`–`Val nombres` | C. Modelo | El cruce se hace por `LOOKUPVALUE` y no por relación; conviene validar correctitud/rendimiento | `relationships.tmdl`, `Entregas Totales.tmdl` | Medio | Media | Sí |

# 18. Hallazgos

| Hallazgo | Categoría | Descripción | Evidencia | Impacto |
|---|---|---|---|---|
| Visuales huérfanos de otro dominio | Reporte/Datos | ~57 visuales (treemaps "Matriculas…", combos "Importaciones/Rendimiento/Producción", barras "Mecanización…", pies de cultivo) referencian `Cultivos`, `RUNT`, `Importaciones`, inexistentes en el modelo. Sugiere una plantilla copiada de un reporte agrícola | `grep` sin coincidencias; `tables/` solo tiene 3 tablas de negocio | Alto |
| Tarjetas con cálculo incoherente con el título | Negocio/Reporte | "Total unidades empresarial", "Total unidades convenios" y "Ticket promedio" (Empresas) usan `Sum(Entregas Totales[año])`; "Empresas renting activas", "Convenios vigentes hoy" y "Empresas distintas" usan `Min(texto)` | `visual.json` de las cards | Alto |
| Medida vacía y medida duplicada | Modelo | "Medida" no tiene expresión; "Medida 2" es idéntica a "Año Anterior" | `Entregas Totales.tmdl` | Bajo |
| Sin relación de negocio explícita | Modelo | Las 6 relaciones son automáticas de fecha; `Val nombres` se cruza por `LOOKUPVALUE` | `relationships.tmdl` | Medio |
| Slicers sin título | Reporte | Ningún slicer define título visible | `visual.json` de slicers | Bajo |
| Canal definido por 3 columnas distintas | Negocio | Renting (`val nombre`), Convenios (`procedencia`), Empresarial (`tipoventa_vista` + `val nombre=OTROS`) | Filtros de página | Medio |
| Columnas calc de bandera sin uso | Modelo | `RENTING`, `Convenios`, `Linea` no se consumen en visuales | `Entregas Totales.tmdl` | Bajo |

# 19. Limitaciones del censo

- Análisis estático sobre definiciones TMDL/PBIR; no se ejecutó el modelo ni se validaron datos reales.
- No se accedió a Athena (`bi_materialized_data.entregas_totales`): contenido, volúmenes, propietario y frecuencia de refresco no verificables desde el proyecto.
- Las entidades `Cultivos`, `RUNT`, `Importaciones` no están en el modelo, por lo que no se puede documentar su estructura, origen ni comportamiento; solo se registra que los visuales las referencian.
- La interpretación funcional de canales, `tipoventa_vista` y las tarjetas con cálculos incoherentes requiere confirmación con negocio.
- El `linguisticMetadata` de `cultures/es-MX.tmdl` es autogenerado y no aporta reglas de negocio adicionales.

# 20. Validación final

- [x] Cobertura revisada — modelo (3 tablas de negocio + auto date tables), 93 visuales de 3 páginas, 24 bookmarks, relaciones, medidas y columnas.
- [x] Consistencia revisada — afirmaciones alineadas con TMDL/PBIR; discrepancias título/cálculo documentadas como hallazgos.
- [x] Trazabilidad revisada — cada tabla, columna, medida y visual cita su archivo de evidencia.
- [x] Elementos no utilizados revisados — columnas, medidas, columnas calc, custom visuals y visuales huérfanos clasificados.
- [x] Vacíos revisados — gobierno, origen de entidades inexistentes, frecuencia, definición de canales.
- [x] Propuestas revisadas — 8 propuestas, todas sustentadas en evidencia.
- [x] Limitaciones documentadas.

## Resultado

Censo técnico y funcional de **GC - Flotillas** en estado **En revisión**. El modelo es simple y coherente (una tabla de hechos `Entregas Totales` desde Athena, apoyada por `Val nombres` y `Fecha De Actualización`), con lógica de canal (Renting/Convenios/Empresarial) resuelta por filtros de página y columnas calculadas. El reporte, sin embargo, presenta dos hallazgos de alto impacto que deben validarse antes de dar el censo por cerrado: (1) una gran proporción de visuales referencia tablas inexistentes en el modelo (`Cultivos`, `RUNT`, `Importaciones`), señal de una plantilla reutilizada; y (2) varias tarjetas muestran cálculos que no corresponden a su título (`Sum(año)`, `Min(texto)`). Ambos puntos están registrados en §16–§18 con su evidencia.
