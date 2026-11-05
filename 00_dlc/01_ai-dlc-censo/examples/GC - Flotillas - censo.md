# 0. Control obligatorio previo

- **Correo de quien realiza el CENSO:** miguel.b@nebula.com.co
- **Correo del dueño/responsable del tablero:** edgar.p@nebula.com.co

Ambos correos se registraron antes de leer el PBIP (R02).

---

# Censo BI — GC - Flotillas

> Estado: Completado pendiente de validación
>
> census_id: 20261105T111744-gc-flotillas
>
> Fecha y hora de ejecución: 2026-11-05T11:17:44-05:00
>
> Versión analizada: 00_original
>
> Tipo de CENSO: Inicial
>
> Versión del ritual: 2.2.3 (sección 14 corregida con v2.2.4; formato v2.3)

Convenciones de todo el documento: los IDs son nativos y completos (CAT-15); `—` = no aplica o no disponible; las rutas de evidencia se indican una vez por tabla, relativas a la carpeta del BI. Cada dato aparece en un solo lugar; las demás secciones lo citan por su ID.

---

# 1. Identificación

| Campo | Valor |
|---|---|
| census_id | 20261105T111744-gc-flotillas |
| census_id del censo anterior | No aplica |
| Nombre BI | GC - Flotillas |
| Archivo .pbip | GC - Flotillas.pbip |
| Área | Comercial / ventas de flotillas y renting de maquinaria y vehículos — Grupo CasaToro / Nebula (Inferido: a partir de las entidades del modelo —entregas, convenios, renting, procedencia— y los nombres de las páginas Dashboard_Empresas, Dashboard_Convenios y Dashboard_Renting; no hay un campo explícito de área en el PBIP) |
| Tecnología | Power BI PBIP — reporte PBIR, modelo TMDL, compatibilityLevel 1606 |
| Repositorio | No identificado en el PBIP |
| Ambiente | No identificado en el PBIP |
| Archivos de salida | `GC - Flotillas - censo.md`, `historial-censos.md` |

# 2. Objetivo y alcance

## 2.1 Objetivo del BI

El tablero entrega el seguimiento comercial de entregas de unidades (vehículos y maquinaria) por tres líneas de negocio: empresas/flotillas, convenios y renting. A partir de la tabla de hechos `Entregas Totales` (origen Athena `bi_materialized_data.entregas_totales`, filtrada a registros de carga con `Cantidad = 1` y `tipo = "Nuevos"`), presenta por línea el conteo de unidades entregadas, el ticket promedio y el valor (`Entregas Totales[Valor]`, definición pendiente: V01), segmentables por marca, región, trimestre (`Q`), procedencia y tipo de venta. El grano de dato es la entrega individual (una fila por unidad entregada). Dirigido al área comercial y a la dirección del negocio de flotillas/renting. Certeza: Inferido en cuanto a la audiencia y el propósito (el PBIP no documenta objetivo ni destinatarios); Encontrado en cuanto a las entidades, el origen y el grano, que se leen directamente del modelo (secciones 3, 4 y 5).

## 2.2 Pregunta central

¿Cuántas unidades se entregaron y con qué valor y ticket promedio en cada línea de negocio (empresas, convenios y renting), y cómo se distribuyen por marca, región, trimestre y procedencia?

## 2.3 Alcance del censo

Lectura de solo lectura de todo el PBIP con `scripts/censo.py borrador`: modelo TMDL (tablas, columnas, medidas, relaciones, jerarquías, roles, particiones M), reporte PBIR (páginas, visuales, bindings, filtros, interacciones, bookmarks, botones, recursos y tema). No incluye datos (filas), el servicio Power BI, la fuente de datos ni consumidores externos.

## 2.4 Fuentes inspeccionadas

| Elemento | Ruta | Objetos leídos |
|---|---|---:|
| Tablas TMDL | GC - Flotillas.SemanticModel/definition/tables/ | 10 |
| Relaciones | GC - Flotillas.SemanticModel/definition/relationships.tmdl | 6 |
| Roles | GC - Flotillas.SemanticModel/definition/roles/ | 1 |
| Páginas | GC - Flotillas.Report/definition/pages/ | 3 |
| Visuales | GC - Flotillas.Report/definition/pages/*/visuals/ | 93 |
| Bookmarks | GC - Flotillas.Report/definition/bookmarks/ | 24 |
| Recursos | GC - Flotillas.Report/StaticResources/ | 4 |

# 3. Fuentes de datos y conexiones

Evidencia: particiones en `GC - Flotillas.SemanticModel/definition/tables/<Tabla>.tmdl`.

| fuente_id | Tabla del modelo | Partición | Modo | Tipo | Conector | Navegación |
|---|---|---|---|---|---|---|
| F01 | Entregas Totales | Entregas Totales | import | Origen | AmazonAthena.Databases("Athena_ODBC2") | AwsDataCatalog / bi_materialized_data / entregas_totales |
| F02 | Fecha De Actualización | Fecha De Actualización | import | Origen (DateTimeZone.SwitchZone) | DateTimeZone.SwitchZone | — |
| F03 | Val nombres | Val nombres | import | Tabla embebida | Tabla embebida (base64) | — |

El código M completo de cada consulta está en la sección 4.

Las 7 tablas de fecha automáticas son tablas calculadas que genera Power BI (ver 6.2); no son fuentes.

**Parámetros M:** No aplica (sin `expressions.tmdl`).

Credenciales: el PBIP no contiene credenciales; no se registran (R06). Frecuencia de actualización y propietario: ver sección 16.

# 4. Transformaciones (Power Query/M)

El código M completo de cada consulta está aquí una sola vez. Los renombres y tipos finales por columna están en la Matriz A (columnas «Nombre en origen» y «Tipo»), no se repiten en la tabla de pasos.

## 4.1 Entregas Totales (partición `Entregas Totales`, 15 pasos)

Evidencia: `GC - Flotillas.SemanticModel/definition/tables/Entregas Totales.tmdl`.

```m
let

    Origen = AmazonAthena.Databases("Athena_ODBC2", null, []),
    AwsDataCatalog_Database = Origen{[Name="AwsDataCatalog",Kind="Database"]}[Data],
    bi_materialized_data_Schema = AwsDataCatalog_Database{[Name="bi_materialized_data",Kind="Schema"]}[Data],
    entregas_totales_Table = bi_materialized_data_Schema{[Name="entregas_totales",Kind="Table"]}[Data],
    #"Columnas quitadas" = Table.RemoveColumns(entregas_totales_Table,{"telefono"}),

    #"Columnas renombradas" = Table.RenameColumns(#"Columnas quitadas", {
        {"fechadecorte", "FechaDeCorte"}, {"idempresas", "IdEmpresas"},
        {"año", "año"}, {"codigoempresa", "CodigoEmpresa"},
        {"empresa", "Empresa"}, {"codigocentro", "CodigoCentro"},
        {"centro", "Centro"}, {"codigoseccion", "CodigoSeccion"},
        {"seccion", "Seccion"}, {"codigomarca", "CodigoMarca"},
        {"marca", "Marca"}, {"codigogama", "CodigoGama"},
        {"gama", "Gama"}, {"codigomodelo", "CodigoModelo"},
        {"añomodelo", "AñoModelo"}, {"modelo", "Modelo"},
        {"cedulavendedor", "CedulaVendedor"}, {"nombrevendedor", "NombreVendedor"},
        {"nit", "Nit"}, {"nombretercero", "NombreTercero"},
        {"cantidad", "Cantidad"}, {"valor", "Valor"}, {"tipo", "tipo"},
        {"fechaentregacliente", "FechaEntregaCliente"},
        {"fechafactura", "FechaFactura"}, {"fechamod", "FechaMod"},
        {"vin", "VIN"}, {"entrega", "Entrega"}
    }),


    #"Tipo cambiado inicial" = Table.TransformColumnTypes(#"Columnas renombradas", {
        {"FechaDeCorte", type date}, {"IdEmpresas", Int64.Type},
        {"año", Int64.Type}, {"CodigoEmpresa", Int64.Type},
        {"Empresa", type text}, {"CodigoCentro", Int64.Type},
        {"Centro", type text}, {"CodigoSeccion", Int64.Type},
        {"Seccion", type text}, {"CodigoMarca", Int64.Type},
        {"Marca", type text}, {"CodigoGama", Int64.Type},
        {"Gama", type text}, {"CodigoModelo", type text},
        {"AñoModelo", type text}, {"Modelo", type text},
        {"CedulaVendedor", type text}, {"NombreVendedor", type text},
        {"Nit", type text}, {"NombreTercero", type text},
        {"Cantidad", Int64.Type}, {"Valor", type number},
        {"tipo", type text}, {"FechaEntregaCliente", type datetime},
        {"FechaFactura", type datetime}, {"FechaMod", type datetime},
        {"VIN", type text}, {"Entrega", type text}
    }),

    #"Filtro Cantidad" = Table.SelectRows(#"Tipo cambiado inicial", each ([Cantidad] = 1)),

    #"Poner En Mayúsculas Cada Palabra" = Table.TransformColumns(#"Filtro Cantidad", {
        {"NombreVendedor", Text.Proper, type text}
    }),

    #"Filas filtradas1" = Table.SelectRows(#"Poner En Mayúsculas Cada Palabra", each ([tipo] = "Nuevos")),


    #"Poner En Mayúsculas Cada Palabra1" = Table.TransformColumns(#"Filas filtradas1", {
        {"NombreTercero", Text.Proper, type text}
    }),
    #"Poner En Mayúsculas Cada Palabra2" = Table.TransformColumns(#"Poner En Mayúsculas Cada Palabra1", {
        {"Gama", Text.Proper, type text}
    }),

    #"Tipo cambiado" = Table.TransformColumnTypes(#"Poner En Mayúsculas Cada Palabra2", {{"Nit", Int64.Type}}),


    #"Poner En Mayúsculas Cada Palabra3" = Table.TransformColumns(#"Tipo cambiado", {
        {"Modelo", Text.Proper, type text}
    }),
    #"Tipo cambiado1" = Table.TransformColumnTypes(#"Poner En Mayúsculas Cada Palabra3",{{"FechaEntregaCliente", type date}})
in
    #"Tipo cambiado1"
```

| # | Paso | Operación | Columnas afectadas |
|---:|---|---|---|
| 1 | Origen | Origen | — |
| 2 | AwsDataCatalog_Database | Navegación | — |
| 3 | bi_materialized_data_Schema | Navegación | — |
| 4 | entregas_totales_Table | Navegación | — |
| 5 | Columnas quitadas | Eliminación de columnas | Elimina: telefono |
| 6 | Columnas renombradas | Renombrado | 28 renombre(s) |
| 7 | Tipo cambiado inicial | Cambio de tipo | 28 cambios de tipo |
| 8 | Filtro Cantidad | Filtro de filas | Cantidad |
| 9 | Poner En Mayúsculas Cada Palabra | Transformación de columnas | NombreVendedor |
| 10 | Filas filtradas1 | Filtro de filas | tipo |
| 11 | Poner En Mayúsculas Cada Palabra1 | Transformación de columnas | NombreTercero |
| 12 | Poner En Mayúsculas Cada Palabra2 | Transformación de columnas | Gama |
| 13 | Tipo cambiado | Cambio de tipo | 1 cambio(s) de tipo: Nit |
| 14 | Poner En Mayúsculas Cada Palabra3 | Transformación de columnas | Modelo |
| 15 | Tipo cambiado1 | Cambio de tipo | 1 cambio(s) de tipo: FechaEntregaCliente |

## 4.2 Fecha De Actualización (partición `Fecha De Actualización`, 4 pasos)

Evidencia: `GC - Flotillas.SemanticModel/definition/tables/Fecha De Actualización.tmdl`.

```m
let
    Origen = DateTimeZone.SwitchZone(DateTimeZone.LocalNow(),-5,0),
    #"Convertida en tabla" = #table(1, {{Origen}}),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Convertida en tabla",{{"Column1", type datetimezone}}),
    #"Columnas con nombre cambiado" = Table.RenameColumns(#"Tipo cambiado",{{"Column1", "Fecha De Actualización"}})
in
    #"Columnas con nombre cambiado"
```

| # | Paso | Operación | Columnas afectadas |
|---:|---|---|---|
| 1 | Origen | Origen (DateTimeZone.SwitchZone) | — |
| 2 | Convertida en tabla | Tabla literal | — |
| 3 | Tipo cambiado | Cambio de tipo | 1 cambio(s) de tipo: Column1 |
| 4 | Columnas con nombre cambiado | Renombrado | 1 renombre(s) |

## 4.3 Val nombres (partición `Val nombres`, 2 pasos)

Evidencia: `GC - Flotillas.SemanticModel/definition/tables/Val nombres.tmdl`.

```m
let
    Origen = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("[[literal de 340 caracteres omitido; ver GC - Flotillas.SemanticModel/definition/tables/Val nombres.tmdl]]", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [NombreTercero = _t, #"Val nombre" = _t]),
    #"Tipo cambiado" = Table.TransformColumnTypes(Origen,{{"NombreTercero", type text}, {"Val nombre", type text}})
in
    #"Tipo cambiado"
```

| # | Paso | Operación | Columnas afectadas |
|---:|---|---|---|
| 1 | Origen | Tabla embebida | — |
| 2 | Tipo cambiado | Cambio de tipo | 2 cambio(s) de tipo: NombreTercero, Val nombre |

# 5. Modelo de datos

## 5.1 Tablas

Evidencia: `GC - Flotillas.SemanticModel/definition/tables/<Tabla>.tmdl`.

| table_id | Tabla | Origen | Visibilidad | Columnas | Medidas | Particiones (modo) |
|---|---|---|---|---:|---:|---|
| 93060b2a-375c-4d50-968b-1547fed5fa65 | Entregas Totales | Importada (M) | Visible | 53 | 15 | Entregas Totales (import) |
| 6b97fbbd-9f96-46d2-a0c1-268a68ffc23b | Fecha De Actualización | Importada (M) | Visible | 1 | 0 | Fecha De Actualización (import) |
| 81048dff-8a9d-470a-84cf-65448a0e4ff3 | Val nombres | Importada (M) | Visible | 2 | 0 | Val nombres (import) |

Además, 7 tablas de fecha automáticas (inventario en 6.2).

- `93060b2a-375c-4d50-968b-1547fed5fa65` · Entregas Totales — **hechos**. Granularidad: una fila por unidad/entrega (filtrada a `Cantidad = 1` y `tipo = "Nuevos"`); concentra las 15 medidas y las dimensiones embebidas como columnas (marca, región, trimestre `Q`, procedencia, tipo de venta).
- `81048dff-8a9d-470a-84cf-65448a0e4ff3` · Val nombres — **dimensión** de homologación de nombres. Granularidad: una fila por nombre a homologar; sin relación física con la tabla de hechos (se consume por `LOOKUPVALUE`, ver secciones 4 y 15).
- `6b97fbbd-9f96-46d2-a0c1-268a68ffc23b` · Fecha De Actualización — **auxiliar**. Granularidad: una sola fila con la marca de tiempo de refresco (reloj M con `DateTimeZone.SwitchZone(..., -5, ...)`); no aporta dimensión de negocio.
- Las 7 tablas `LocalDateTable_*` (inventario en 6.2) son **auxiliares** de fecha generadas automáticamente por Power BI; granularidad de un día por fila, una por cada columna de fecha de `Entregas Totales` y de `Fecha De Actualización`.

## 5.2 Relaciones

Evidencia: `GC - Flotillas.SemanticModel/definition/relationships.tmdl`.

| relationship_id | Desde | Hacia | Cardinalidad | Filtro | Activa | joinOnDateBehavior |
|---|---|---|---|---|---|---|
| 772fc70d-213d-4770-ada6-d83317f52bbe | Entregas Totales[FechaDeCorte] | LocalDateTable_8f7b7b5e-ad22-4ad1-8cc1-80b84c190664[Date] | many:one | oneDirection | Sí | datePartOnly |
| 4358b4ce-3356-471e-b092-abd140fccb2c | Entregas Totales[FechaEntregaCliente] | LocalDateTable_db36dc30-cffa-4632-baeb-6977b4539a2b[Date] | many:one | oneDirection | Sí | datePartOnly |
| 58e448f2-3711-4623-bdbb-986096830730 | Entregas Totales[FechaFactura] | LocalDateTable_ebcf95e2-ffd9-4b81-ad25-765b67aa04be[Date] | many:one | oneDirection | Sí | datePartOnly |
| 1ce62867-0b58-4dc2-a890-6ed7aad4924c | Entregas Totales[FechaMod] | LocalDateTable_1bea27a1-b01a-406b-b09d-312a3807684b[Date] | many:one | oneDirection | Sí | datePartOnly |
| fdbeba49-c009-45c3-8ba8-c6f674c25df5 | Fecha De Actualización[Fecha De Actualización] | LocalDateTable_27076615-e8ea-4cd4-9388-415e2ab86793[Date] | many:one | oneDirection | Sí | datePartOnly |
| 094bc577-7ce9-452b-bd59-7627a499b8c0 | Entregas Totales[fechamatriculacion] | LocalDateTable_da3d9bb4-8ca6-4cba-b3ff-391ced20ca41[Date] | many:one | oneDirection | Sí | datePartOnly |

## 5.3 Jerarquías y ordenamiento

_Sin registros._

Ordenamiento (`sortByColumn`): ninguno. Las 7 tablas automáticas tienen su jerarquía de fechas propia.

## 5.4 Propiedades del modelo

| Propiedad | Valor |
|---|---|
| culture | es-MX |
| defaultPowerBIDataSourceVersion | powerBI_V3 |
| sourceQueryCulture | es-CO |
| dataAccessOptions.legacyRedirects | Sí |
| dataAccessOptions.returnErrorValuesAsNull | Sí |
| compatibilityLevel | 1606 |

## 5.5 Seguridad

| Rol | Permiso | Tabla | Expresión RLS |
|---|---|---|---|
| Todo | read | — | Sin reglas RLS |

# 6. Columnas

Clases de dependencia (CAT-03): V visuales · F filtros y segmentaciones · D DAX · M relaciones, jerarquías y ordenamiento · PQ pasos de Power Query · BK bookmarks · SEC seguridad.
Valor de cada celda (CAT-04): número = referencias encontradas · `0` = no encontrada en el alcance revisado · `NA` = no aplica · `NV` = no verificable · `P` = pendiente. SQL: no aplica (no hay consulta nativa en el PBIP). El detalle de cada referencia está en su sección de origen (V → 9, F → 11, D → 6.1 expresiones y 7, M → 5, BK → 12).

## 6.1 Matriz A — columnas por tabla

### Entregas Totales (53 columnas)

Evidencia: `GC - Flotillas.SemanticModel/definition/tables/Entregas Totales.tmdl`.

| column_id | Columna | Nombre en origen | Tipo | Clase | Visibilidad | V | F | D | M | PQ | BK | SEC | Estado de uso | Nota |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4d67ac97-fa32-4205-8b65-977e7a85b52a | año | año | int64 | Origen | Visible | 3 | 3 | 3 | 0 | 0 | 0 | 0 | En uso | — |
| 37221089-abf2-44ce-86ee-a142b152470a | tipo | tipo | string | Origen | Visible | 0 | 0 | 0 | 0 | 1 | 0 | 0 | Uso técnico | — |
| 2708d650-1f2e-4c3c-bd68-5537046823ca | Linea | — | — | Calculada DAX | Visible | 0 | 0 | 0 | 0 | NA | 0 | 0 | Sin uso interno identificado | — |
| a51b8392-6e78-4915-a6e5-26529e05e6b4 | Región | — | — | Calculada DAX | Visible | 0 | 1 | 0 | 0 | NA | 0 | 0 | En uso | — |
| 424b3603-4b25-469b-a7c7-cac1d20477d1 | FechaDeCorte | fechadecorte | dateTime | Origen | Visible | 0 | 0 | 1 | 1 | 0 | 0 | 0 | Uso técnico | — |
| 8e1eec6d-2100-4451-b7be-092f74b77aee | IdEmpresas | idempresas | int64 | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| 55eb0c15-3bfa-4c07-8d92-210a84bff343 | CodigoEmpresa | codigoempresa | int64 | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| c6a74202-6da6-40a0-8a20-426ec13b551b | Empresa | empresa | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| e29f126d-d0c9-4d1b-b382-189c0a69873b | CodigoCentro | codigocentro | int64 | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| 97662241-a909-406f-bfc8-8b9f95e68a76 | Centro | centro | string | Origen | Visible | 0 | 2 | 2 | 0 | 0 | 0 | 0 | En uso | — |
| 1ae04e8e-0ff3-48d7-b9c2-ac89a6dd98d8 | CodigoSeccion | codigoseccion | int64 | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| 1f382698-d1b3-4e6a-9423-884746ef0966 | Seccion | seccion | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| 92faf536-a44f-498b-af27-fbf3a2102f87 | CodigoMarca | codigomarca | int64 | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| 39f01624-37ff-4b52-a8df-ebf8206b0106 | Marca | marca | string | Origen | Visible | 0 | 3 | 1 | 0 | 0 | 0 | 0 | En uso | — |
| cf67ef9b-4a69-457a-9df7-fc078e087c4a | CodigoGama | codigogama | int64 | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| 08707750-d58c-4b65-ae17-b0720bf5265c | Gama | gama | string | Origen | Visible | 1 | 3 | 0 | 0 | 0 | 0 | 0 | En uso | — |
| 6b284f60-f9c8-4243-8621-98e747ac1490 | CodigoModelo | codigomodelo | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| 7721f26c-91f1-4e98-ac2c-e81c76cfcf93 | AñoModelo | añomodelo | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| f262bdaa-ee85-4e87-9fd9-3cad5fab6f33 | Modelo | modelo | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| 3207f566-fbc3-4776-9435-3ece08642f00 | CedulaVendedor | cedulavendedor | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| 47633825-94f6-41a8-a4e1-88ec933239dc | NombreVendedor | nombrevendedor | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| 576abc15-8686-4c32-a229-182c113e5324 | Nit | nit | int64 | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| eb0442ee-18d4-4134-88a9-631d81e1b142 | NombreTercero | nombretercero | string | Origen | Visible | 1 | 0 | 2 | 0 | 0 | 0 | 0 | En uso | — |
| 2711850f-324f-4d29-b96e-63d2b9376e15 | Cantidad | cantidad | int64 | Origen | Visible | 0 | 3 | 0 | 0 | 1 | 0 | 0 | En uso | — |
| 89f0ac09-9836-4791-9b16-5b7ed99ec8ad | Valor | valor | double | Origen | Visible | 3 | 0 | 1 | 0 | 0 | 0 | 0 | En uso | — |
| fccd1d98-4406-4b70-9e38-5667b3dc7c29 | FechaEntregaCliente | fechaentregacliente | dateTime | Origen | Visible | 0 | 0 | 3 | 1 | 0 | 0 | 0 | En uso | Uso indirecto vía DIVISION S, Q |
| 08b85943-ba76-4d3f-befa-d633db47a666 | FechaFactura | fechafactura | dateTime | Origen | Visible | 0 | 0 | 1 | 1 | 0 | 0 | 0 | Uso técnico | — |
| f5786e8b-74ef-4f00-969d-1ebf45c6331e | FechaMod | fechamod | dateTime | Origen | Visible | 0 | 0 | 1 | 1 | 0 | 0 | 0 | Uso técnico | — |
| 99d30921-c2b5-4c63-91f0-899ccfc15ecc | VIN | vin | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| 93162a6a-96c7-4c1d-9779-2d8c5c0ff097 | Entrega | entrega | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| 9d44a9c8-fee6-41e2-b462-3e4cc4dec7a6 | placa | placa | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| a2f598b1-5a0e-4e34-bc37-b1790709e220 | fechamatriculacion | fechamatriculacion | dateTime | Origen | Visible | 0 | 0 | 1 | 1 | 0 | 0 | 0 | Uso técnico | — |
| f3498df1-ea60-4988-ad3f-01264c0cd682 | combustible | combustible | string | Origen | Visible | 0 | 3 | 0 | 0 | 0 | 0 | 0 | En uso | — |
| 76028578-37db-4e0e-b94d-33da7e11da14 | procedencia | procedencia | string | Origen | Visible | 0 | 2 | 1 | 0 | 0 | 0 | 0 | En uso | — |
| 749ed097-b14e-447c-b459-66589e78d303 | procedenciadetalle | procedenciadetalle | string | Origen | Visible | 5 | 3 | 0 | 0 | 0 | 0 | 0 | En uso | — |
| 7173d367-afb7-4df9-9e5d-4696920a1596 | tipooportunidad | tipooportunidad | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| fff50d4e-3578-43e2-8c45-d73fa10c2565 | correo | correo | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| 3892cac9-e567-451f-90b9-94061a948254 | codunidadnegocio | codunidadnegocio | int64 | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| 4af06471-46d8-470c-9a3f-d7ae1796198c | nombreunidadnegocio | nombreunidadnegocio | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| e2f242e9-bb6d-46ba-a88b-c5452ce0348e | tipocliente | tipocliente | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| 69af02df-4586-4eab-b02c-09becd2577fc | nombrevendedorhomologado | nombrevendedorhomologado | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| 1788f9fa-aa12-4927-b3e6-6d6033ff6d11 | clase | clase | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| d96d9bb5-2858-4953-8cec-edf95d0c68a9 | color | color | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| 26a41a2c-2321-4b16-802b-816bf9384e49 | esultimamodificacion | esultimamodificacion | int64 | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| 1612656f-b1d3-4dcf-b173-ab0d08ec21ef | rowhash | rowhash | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| 3b82c226-f373-44f0-8fe8-e3b85de25b88 | extractionid | extractionid | int64 | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| ce7be861-2482-405a-8e8d-d8d72d361e53 | Q | — | — | Calculada DAX | Visible | 3 | 4 | 4 | 0 | NA | 0 | 0 | En uso | — |
| ad5aafbd-3cad-4e7d-a0fa-01c6fba23632 | DIVISION S | — | — | Calculada DAX | Visible | 1 | 0 | 2 | 0 | NA | 0 | 0 | En uso | — |
| 4e3d84d5-402a-4b45-ae57-f7bfe58ac128 | val nombre | — | — | Calculada DAX | Visible | 3 | 3 | 0 | 0 | NA | 0 | 0 | En uso | — |
| 4786567f-9f0e-4063-8aea-5f1801f181dc | RENTING | — | — | Calculada DAX | Visible | 0 | 0 | 0 | 0 | NA | 0 | 0 | Sin uso interno identificado | — |
| 1996f16a-30b2-4c1c-a526-9cf4a7810a85 | Convenios | — | — | Calculada DAX | Visible | 0 | 0 | 0 | 0 | NA | 0 | 0 | Sin uso interno identificado | — |
| 5b443a28-0fbb-4cc8-9975-8915f264fbfa | emailvendedor | emailvendedor | string | Origen | Visible | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Sin uso interno identificado | — |
| 3191ec45-db99-40fc-944e-a536a2210df0 | tipoventa_vista | tipoventa_vista | string | Origen | Visible | 0 | 1 | 0 | 0 | 0 | 0 | 0 | En uso | — |

Expresiones de columnas calculadas de Entregas Totales:

```dax
-- Linea
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="ciber","Wirtgen",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="Hamm","Wirtgen",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="Implementos","JD Agricola",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="vibromax","JD Agricola",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="hyundai","JD Agricola",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="tcm","JD Agricola",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="mitsubishi","JD Agricola",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="Volkswagen Comerciales","JD Agricola",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="John Deere Agrícola","JD Agricola",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="komatsu","JD Construccion",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="gesmet","JD Construccion",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="mazda","JD Construccion",
IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="John Deere Construccion","JD Construccion",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="John Deere Golf & Turf","JD Agricola",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="Kleemann","Wirtgen",                                  IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="New Holland Construction","JD Construccion",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="VOGELE","Wirtgen",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="VÖGELE","Wirtgen",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="Volvo","JD Construccion",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="Wacker Neuson","JD Construccion",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="Wirtgen","Wirtgen",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="bomag","Wirtgen",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="Dynapac","Usados",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="Caterpillar","Usados",
      IF(left('Entregas Totales'[Centro],2)<>"VO" && [Marca]="Yanmar","JD Agricola")))))))))))))))))))))))))

-- Región
IF('Entregas Totales'[Centro]="JD-B/Quilla-Cl.110", "Barranquilla",
         IF('Entregas Totales'[Centro]="JD-Bta-P. Aranda", "Bogotá",
         IF('Entregas Totales'[Centro]="JD-Cali-Palmira", "Cali",
         IF('Entregas Totales'[Centro]="JD-Chia-Mayorista", "Chia Mayorista",
         IF('Entregas Totales'[Centro]="JD-Chia-Yerbabuena", "Bogotá",
         IF('Entregas Totales'[Centro]="JD-Ibague-ZI Mirolindo", "Ibagué",
         IF('Entregas Totales'[Centro]="JD-Itagui-Cra 92", "Medellín", 
         IF('Entregas Totales'[Centro]="JD-Monteria-Via Cereté", "Montería",
         IF('Entregas Totales'[Centro]="JD-Neiva-Cra 5", "Neiva",
         IF('Entregas Totales'[Centro]="JD-Ruta 40", "Ruta 40",
         IF('Entregas Totales'[Centro]="JD-Villavo-Anillo Vial 1", "Villavicencio",
         IF('Entregas Totales'[Centro]="JD-Yopal-Yopal", "Yopal",
         IF('Entregas Totales'[Centro]="JD B/manga B/manga", "Bucaramanga",
         IF('Entregas Totales'[Centro]="JD-Villavo-Ag Del Llano", "Agricola De Los Llanos",
         IF('Entregas Totales'[Centro]="JD-Grupo Ortiz", "Grupo Ortiz",
         'Entregas Totales'[Centro])))))))))))))))

-- Q
"Q"&SWITCH(MONTH('Entregas Totales'[FechaEntregaCliente]),1,1,2,1,3,1,4,2,5,2,6,2,7,3,8,3,9,3,10,4,11,4,12,4)

-- DIVISION S
"S"&SWITCH(MONTH('Entregas Totales'[FechaEntregaCliente]),1,1,2,1,3,1,4,1,5,1,6,1,7,2,8,2,9,2,10,2,11,2,12,2)

-- val nombre
IF(LOOKUPVALUE('Val nombres'[Val nombre],'Val nombres'[NombreTercero],'Entregas Totales'[NombreTercero])="","OTROS",LOOKUPVALUE('Val nombres'[Val nombre],'Val nombres'[NombreTercero],'Entregas Totales'[NombreTercero]))

-- RENTING
IF(IF(LOOKUPVALUE('Val nombres'[Val nombre],'Val nombres'[NombreTercero],'Entregas Totales'[NombreTercero])="","OTROS",LOOKUPVALUE('Val nombres'[Val nombre],'Val nombres'[NombreTercero],'Entregas Totales'[NombreTercero]))<>"OTROS","RENTING","")

-- Convenios
IF('Entregas Totales'[procedencia]="Convenios","CONVENIOS","")
```

### Fecha De Actualización (1 columnas)

Evidencia: `GC - Flotillas.SemanticModel/definition/tables/Fecha De Actualización.tmdl`.

| column_id | Columna | Nombre en origen | Tipo | Clase | Visibilidad | V | F | D | M | PQ | BK | SEC | Estado de uso | Nota |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 7773f156-ad3a-4929-a157-638ff76eb302 | Fecha De Actualización | Column1 | dateTime | Origen | Visible | 3 | 0 | 1 | 1 | 0 | 10 | 0 | En uso | — |

### Val nombres (2 columnas)

Evidencia: `GC - Flotillas.SemanticModel/definition/tables/Val nombres.tmdl`.

| column_id | Columna | Nombre en origen | Tipo | Clase | Visibilidad | V | F | D | M | PQ | BK | SEC | Estado de uso | Nota |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4972aa03-fb59-4b14-b929-b3fcfa9b0c9f | NombreTercero | NombreTercero | string | Origen | Visible | 0 | 0 | 2 | 0 | 0 | 0 | 0 | En uso | Uso indirecto vía val nombre |
| 42402c09-7590-4097-85cb-d7e9f11c7ac6 | Val nombre | Val nombre | string | Origen | Visible | 0 | 0 | 2 | 0 | 0 | 0 | 0 | En uso | Uso indirecto vía val nombre |

## 6.2 Tablas de fecha automáticas

Las genera Power BI por la inteligencia de tiempo automática; tienen la misma estructura. Se listan sus IDs completos por columna.

| table_id | Tabla | Origen (relación) | Columnas | column_id por columna | Estado de uso |
|---|---|---|---:|---|---|
| 86af2be4-b1fb-41ec-ad27-795e3362bdf7 | DateTableTemplate_f19d1d27-b424-47df-bd6f-ec6f68132e7d | Plantilla (sin relación) | 7 | Date=ce5df6bc-10bb-46f5-aa4a-5a07ce3a15c0; Año=e1360a5b-267c-4507-a10a-7b8b80e70f3f; NroMes=db304d92-1450-4665-8efd-f7a5d754e6e2; Mes=e3ae71e5-392f-4cca-adda-f994b73f4eaa; NroTrimestre=0975f067-45eb-40ab-91c3-6bdc6ab41a37; Trimestre=06bf2b78-d844-415f-94b2-27d4871ca423; Día=b760aabd-edeb-474e-b380-361504dca86a | En uso 3, Uso técnico 4 |
| 4820f7f5-ab09-4ae2-bc0f-392e925642da | LocalDateTable_1bea27a1-b01a-406b-b09d-312a3807684b | Entregas Totales[FechaMod] | 7 | Date=0565a8e7-5559-4ec8-beb2-67c7b21fbaef; Año=d3b3b65f-b5df-4545-a05e-7f431bd30954; NroMes=15ee94d7-54ef-4098-9073-be9065f9142e; Mes=e634648c-c170-4f92-b29f-33974d6522d7; NroTrimestre=5b6d081b-f640-4472-83cb-72b1c3650931; Trimestre=f3774821-e866-41b1-8a9f-4e2e878577d2; Día=98188607-93e9-4ff0-9bae-3457a32d2b6d | En uso 3, Uso técnico 4 |
| c2e20a67-6711-477b-bf61-6472a1ec5317 | LocalDateTable_27076615-e8ea-4cd4-9388-415e2ab86793 | Fecha De Actualización[Fecha De Actualización] | 7 | Date=ea68ce7b-8b4e-4436-9496-985964d8ae63; Año=c477a53b-f381-4dca-972b-6b8a8ab75c31; NroMes=806f5903-9de9-43d2-a8a9-a30a2c32bce3; Mes=f8fa57e5-d044-4677-8a4e-b643d4f668bf; NroTrimestre=0bb7d175-c44f-43d6-9ac0-a31adef988d6; Trimestre=d42f280c-faf3-4137-9d92-74f934bc0f94; Día=ab2f3d36-426e-4a02-ac32-301bf82a97b0 | En uso 3, Uso técnico 4 |
| 856d0b26-9b5c-4f85-98da-b16bebd2c7f4 | LocalDateTable_8f7b7b5e-ad22-4ad1-8cc1-80b84c190664 | Entregas Totales[FechaDeCorte] | 7 | Date=90bde3c1-672f-46b9-b37d-d3516896595b; Año=b89504e6-c4da-4c99-9704-53ba469bd12a; NroMes=7c5143a7-1cf3-49f0-8bdb-d085e6ed64d7; Mes=ac8bed0e-c8e3-4de9-9812-6ade886e287b; NroTrimestre=f50944d0-7a8d-4b33-93a6-9533a749159c; Trimestre=b85df1db-6ae2-49a8-bfa5-a0365dab445c; Día=f2faecd8-5803-4928-9e8c-ffab2aa35916 | En uso 3, Uso técnico 4 |
| 04ef76c1-4566-4038-b4c3-8024b80b22ba | LocalDateTable_da3d9bb4-8ca6-4cba-b3ff-391ced20ca41 | Entregas Totales[fechamatriculacion] | 7 | Date=6c4c80bf-8a7c-4fa7-acf5-4758e7270d1c; Año=c133e76d-3031-4a2f-9620-4896137c570f; NroMes=9669cf93-7013-4676-8d73-f672f685954a; Mes=bcdea45f-e098-4509-86a8-442178f1f2fd; NroTrimestre=dda96874-6240-4c44-8755-ab735b939bf9; Trimestre=6068251e-b4f5-496c-b87c-13635821411d; Día=8f9a153a-0025-4b66-82db-1ae7c35f82a4 | En uso 3, Uso técnico 4 |
| 249ffd0d-b86f-4575-8f15-cbf73854b748 | LocalDateTable_db36dc30-cffa-4632-baeb-6977b4539a2b | Entregas Totales[FechaEntregaCliente] | 7 | Date=de444ffd-0000-4f98-9474-ee4442c4ddb4; Año=9f5c2a01-8284-4d02-8ae2-a19e8e303412; NroMes=321b5f16-bc50-4f2c-9d5c-1f8dbc741e42; Mes=19b7f026-0e3b-423d-83b8-309bf3a7c27c; NroTrimestre=84b98f0e-8bf3-4bd2-a077-083b8dc8c7d5; Trimestre=c2097d5b-070d-4cdc-9f52-05c45e3df0e1; Día=4d5b05fb-3bcf-45b9-ab78-88b13fd79c47 | En uso 3, Uso técnico 4 |
| a48f42ec-6fd1-4c6f-ac00-ceb5d2eb2729 | LocalDateTable_ebcf95e2-ffd9-4b81-ad25-765b67aa04be | Entregas Totales[FechaFactura] | 7 | Date=a13690df-59e1-4465-941a-e270e039a888; Año=dd3b0959-74b0-4671-bd56-c6d6a7ba9e61; NroMes=63ce6a46-c5b5-4537-b393-7ab0c4d503cc; Mes=e1c18d63-fb61-4931-9fe3-66e2f235bfd9; NroTrimestre=0659d05a-de73-4eef-8d46-3f091ce226f8; Trimestre=0f7a1c03-202c-4a00-9480-d9af397d4e4c; Día=c81c5cfd-a5fa-4528-941e-49bc1a3f9de8 | En uso 3, Uso técnico 4 |

# 7. Medidas

Evidencia: `GC - Flotillas.SemanticModel/definition/tables/<Tabla>.tmdl`. Las expresiones completas están en el bloque de código al final de la sección.

| measure_id | Medida | Tabla | Formato | Usa | V | F | BK | D | Estado de uso | Nota |
|---|---|---|---|---|---|---|---|---|---|---|
| bf1225e0-e20f-4b78-92af-7b1716c7f12e | cantidad de maquinas | Entregas Totales | #,0 | — | 10 | 3 | 0 | 12 | En uso | — |
| 8e2854d0-05a5-4afa-b723-e627a276907b | Medida | Entregas Totales | — | — | 0 | 0 | 0 | 0 | Sin uso interno identificado | Sin expresión |
| b416919b-0793-4867-8b37-933b454de8fb | S1 | Entregas Totales | #,0 | cantidad de maquinas, Entregas Totales[DIVISION S] | 0 | 1 | 0 | 1 | En uso | — |
| 49f6cace-cdaa-4343-b937-54f3566072d4 | S2 | Entregas Totales | #,0 | cantidad de maquinas, Entregas Totales[DIVISION S] | 0 | 1 | 0 | 1 | En uso | — |
| af443139-00f4-4345-b9ee-b847f2babfab | Recambio semestral | Entregas Totales | 0.0\ %;-0.0\ %;0.0\ % | cantidad de maquinas, S2, S1 | 1 | 1 | 0 | 0 | En uso | — |
| fcf33b75-6f4e-46bd-8e6a-189513deadb9 | Recambio anual (vs año ant.) | Entregas Totales | 0.00\ %;-0.00\ %;0.00\ % | cantidad de maquinas, Año actual, Año Anterior | 1 | 1 | 0 | 0 | En uso | — |
| cace1f24-fd56-4655-a098-3b24d13e78b8 | Año actual | Entregas Totales | 0 | cantidad de maquinas, Entregas Totales[año] | 0 | 0 | 0 | 1 | En uso | — |
| 5e65ec2b-b63c-4038-8140-d68832f20c73 | Año Anterior | Entregas Totales | 0 | cantidad de maquinas, Entregas Totales[año] | 0 | 0 | 0 | 1 | En uso | Misma expresión que Medida 2 |
| d96eb974-557d-4111-9838-b22f90197c83 | Medida 2 | Entregas Totales | 0 | cantidad de maquinas, Entregas Totales[año] | 0 | 0 | 0 | 0 | Sin uso interno identificado | Misma expresión que Año Anterior |
| 7e67ca90-bf72-4fe8-b562-2f2a1546a1cf | Q1 | Entregas Totales | #,0 | cantidad de maquinas, Entregas Totales[Q] | 3 | 2 | 0 | 1 | En uso | — |
| 672472d1-723e-4c64-bbf6-2396df0f84b7 | Q2 | Entregas Totales | #,0 | cantidad de maquinas, Entregas Totales[Q] | 3 | 2 | 0 | 0 | En uso | — |
| f3616dc2-c871-4bc2-a680-bd14517e80bb | Q3 | Entregas Totales | #,0 | cantidad de maquinas, Entregas Totales[Q] | 3 | 2 | 0 | 0 | En uso | — |
| aba32d58-0bb4-4436-8a38-2f443bcfb31d | Q4 | Entregas Totales | #,0 | cantidad de maquinas, Entregas Totales[Q] | 3 | 2 | 0 | 1 | En uso | — |
| 48bb01d7-3243-4200-a84a-14ba38ef6138 | Crecimiento Q1→Q4 | Entregas Totales | 0.00\ %;-0.00\ %;0.00\ % | Q4, Q1 | 1 | 1 | 0 | 0 | En uso | — |
| 8a477545-83ea-4fc9-ab75-e12f341f139e | Ticket promedio | Entregas Totales | \$#,0.###############;(\$#,0.###############);\$#,0.############### | Entregas Totales[Valor], cantidad de maquinas | 1 | 0 | 0 | 0 | En uso | — |

```dax
-- Entregas Totales[cantidad de maquinas]
IF(COUNTROWS('Entregas Totales')=0,0,COUNTROWS('Entregas Totales'))

-- Entregas Totales[Medida]
(sin expresión)

-- Entregas Totales[S1]
IF(CALCULATE([cantidad de maquinas],'Entregas Totales'[DIVISION S]="S1")=0,0,CALCULATE([cantidad de maquinas],'Entregas Totales'[DIVISION S]="S1"))

-- Entregas Totales[S2]
IF(CALCULATE([cantidad de maquinas],'Entregas Totales'[DIVISION S]="S2")=0,0,CALCULATE([cantidad de maquinas],'Entregas Totales'[DIVISION S]="S2"))

-- Entregas Totales[Recambio semestral]
IF('Entregas Totales'[cantidad de maquinas]=0,0,IF(([S2]-[S1])/[S2]<=0,0,([S2]-[S1])/[S2]))

-- Entregas Totales[Recambio anual (vs año ant.)]
IF(IF([cantidad de maquinas]=0,0,([Año actual]-[Año Anterior])/[Año Anterior])>1,1,IF([cantidad de maquinas]=0,0,([Año actual]-[Año Anterior])/[Año Anterior]))

-- Entregas Totales[Año actual]
CALCULATE([cantidad de maquinas],'Entregas Totales'[año]=MAX('Entregas Totales'[año]))

-- Entregas Totales[Año Anterior]
CALCULATE([cantidad de maquinas],'Entregas Totales'[año]=MAX('Entregas Totales'[año])-1)

-- Entregas Totales[Medida 2]
CALCULATE([cantidad de maquinas],'Entregas Totales'[año]=MAX('Entregas Totales'[año])-1)

-- Entregas Totales[Q1]
IF(CALCULATE([cantidad de maquinas],'Entregas Totales'[Q]="Q1")=0,0,CALCULATE([cantidad de maquinas],'Entregas Totales'[Q]="Q1"))

-- Entregas Totales[Q2]
IF(CALCULATE([cantidad de maquinas],'Entregas Totales'[Q]="Q2")=0,0,CALCULATE([cantidad de maquinas],'Entregas Totales'[Q]="Q2"))

-- Entregas Totales[Q3]
IF(CALCULATE([cantidad de maquinas],'Entregas Totales'[Q]="Q3")=0,0,CALCULATE([cantidad de maquinas],'Entregas Totales'[Q]="Q3"))

-- Entregas Totales[Q4]
IF(CALCULATE([cantidad de maquinas],'Entregas Totales'[Q]="Q4")=0,0,CALCULATE([cantidad de maquinas],'Entregas Totales'[Q]="Q4"))

-- Entregas Totales[Crecimiento Q1→Q4]
IF([Q4]=0,0,IF(([Q4]-[Q1])/[Q1]>1,1,([Q4]-[Q1])/[Q1]))

-- Entregas Totales[Ticket promedio]
SUM('Entregas Totales'[Valor])/[cantidad de maquinas]
```

# 8. Páginas

Evidencia: `GC - Flotillas.Report/definition/pages/<page_id>/page.json`.

| page_id | Página | Orden | Visibilidad | Tamaño | Ajuste | Fondo | Tipo | Visuales |
|---|---|---:|---|---|---|---|---|---:|
| ac291ea509382034e4ab | Dashboard_Renting | 1 | Visible | 1280×720 | FitToPage | #F6F6F5 | Normal | 30 |
| b597e26007760b8239c0 | Dashboard_Convenios | 2 | Visible | 1280×720 | FitToPage | #F6F6F5 | Normal | 31 |
| 377df594a011ae294444 | Dashboard_Empresas | 3 | Visible | 1280×720 | FitToPage | #F6F6F5 | Normal | 32 |

**Páginas referenciadas que no existen:**

| page_id | Bookmarks que la usan | Botones que navegan a ella |
|---|---|---|
| 6acb58945104d5318733 | 0340d676b7e24e06b31d · Grafica imp; 0e8fa233336b7005c554 · Resumen matriculas; 32318b42c9d3954d5e19 · Participacion; 73126f0c2c300ec3c0d6 · Marca; 9ab9f550c06d5e43709b · Importadores; aa98c6807620b2365ea7 · CIF; d66c5cc860884db34063 · Modelo; d9c095c65d1a6600d67b · Capacidad | — |
| 7adad99113991d0e3e3e | 598a9e8ed007000d0750 · Intencion; 6a7dad0d996da4853d64 · Regional; 7052bcd3da2e11b02291 · Tipo de cliente; c2e908097e6ad07bc67a · Cultivo; de6e833a9e73fa72fe5a · Departamento; fc32d496129c0a4cf7cf · Maquina | — |
| 7fe28b006cd3b491a578 | — | ab3e643b10d65600d211 · Conectividad |

# 9. Visuales

Evidencia: `GC - Flotillas.Report/definition/pages/<page_id>/visuals/<visual_id>/visual.json`. Posición y tamaño en píxeles enteros del lienzo.

Por cada página hay dos tablas: la primera dice **qué es y dónde está** cada visual (una fila por visual); la segunda, **qué datos usa** (una fila por campo). Clases: «Con binding válido» = muestra datos y todos sus campos existen; «Decorativo» = imagen, forma o texto sin datos; «Botón/acción»; «Referencia rota» = algún campo de datos apunta a una entidad que no existe, por lo que el visual no puede dibujarse. Un «Formato huérfano» es una regla de formato (colores por categoría, formato condicional) que apunta a una entidad inexistente: no impide que el visual funcione y no lo convierte en referencia rota.

## 9.1 Dashboard_Renting (`ac291ea509382034e4ab`) — 30 visuales

| visual_id | Nombre | Tipo | Oculto | x | y | Ancho | Alto | z | Grupo | Clase | Formato huérfano | Estado de uso |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| 0de40f160ad554410865 | Matriculas por marca | treemap | Sí | 6 | 477 | 514 | 231 | 5000 | — | Referencia rota | No | Referencia rota |
| 1a394380135072c054c8 | Rendimiento (t/ha) | lineClusteredColumnComboChart | Sí | 369 | 484 | 439 | 226 | 6000 | — | Referencia rota | No | Referencia rota |
| 2b6d4c39222aa4000302 | Mecanización por regional | barChart | Sí | 814 | 244 | 459 | 234 | 2000 | — | Referencia rota | No | Referencia rota |
| 3481c97f911715717734 | Unidades facturadas por empresa de Renting y trimestre | tableEx | No | 10 | 250 | 644 | 452 | 23000 | — | Con binding válido | No | En uso |
| 44e4621d600343c70058 | Matriculas por modelo | treemap | Sí | 6 | 477 | 514 | 231 | 4000 | — | Referencia rota | No | Referencia rota |
| 4a086741483d06edbbe1 | Especificación Importadores | tableEx | Sí | 526 | 477 | 746 | 232 | 16000 | — | Referencia rota | No | Referencia rota |
| 4caed66b2e79ca489edc | Total unidades renting | card | No | 219 | 163 | 221 | 74 | 24000 | — | Con binding válido | No | En uso |
| 5225a970b0de27434ed1 | Imagen: Logo-Nebula_(1)8124617426694213.png | image | No | 1028 | 27 | 121 | 29 | 22000 | — | Decorativo | No | En uso |
| 5ce335d4e237c11a70e2 | Unidades RENTING por empresa y trimestre | lineClusteredColumnComboChart | No | 660 | 250 | 609 | 452 | 28000 | — | Con binding válido | No | En uso |
| 647df1e1caca5a76abc8 | Producción (T) | lineClusteredColumnComboChart | Sí | 369 | 484 | 439 | 227 | 7000 | — | Referencia rota | No | Referencia rota |
| 69b6e056895903ee070d | Forma sin título | shape | No | 150 | 22 | 15 | 42 | 11000 | — | Decorativo | No | En uso |
| 6e17130e3d82a640b8c5 | Renting | textbox | No | 14 | 11 | 142 | 54 | 9000 | — | Decorativo | No | En uso |
| 710b4bdd807785877d66 | Importaciones (CIF) | lineClusteredColumnComboChart | Sí | 526 | 477 | 746 | 231 | 3000 | — | Referencia rota | Sí | Referencia rota |
| 7372de39e4387230a26c | Mecanizacion por departamento | barChart | Sí | 814 | 244 | 459 | 234 | 1000 | — | Referencia rota | No | Referencia rota |
| 8106d7c0e70d14e3cc6e | Importaciones | lineClusteredColumnComboChart | Sí | 526 | 477 | 746 | 231 | 17000 | — | Referencia rota | Sí | Referencia rota |
| 86925930b70b966b6025 | Segmentación: Entregas Totales[Gama] | slicer | No | 363 | 79 | 170 | 65 | 19000 | — | Con binding válido | No | En uso |
| 8b1429e26c4c808079c8 | Segmentación: Entregas Totales[Centro] | slicer | No | 536 | 79 | 163 | 65 | 21000 | — | Con binding válido | No | En uso |
| 918d228ab18d5045e510 | Utilidad bruta total | card | No | 901 | 163 | 236 | 74 | 26000 | — | Con binding válido | No | En uso |
| 943ad7553bad0a0283bb | Segmentación: Entregas Totales[Marca] | slicer | No | 142 | 80 | 216 | 65 | 13000 | — | Con binding válido | No | En uso |
| 9734d2820ecd3ae8a0a0 | Última Actualización | card | No | 172 | 17 | 207 | 51 | 12000 | — | Con binding válido | No | En uso |
| 9c9f9e7740ae80a69e13 | Participación por cultivo área sembrada has (TOP 5) | pieChart | Sí | 369 | 243 | 439 | 235 | 14000 | — | Referencia rota | Sí | Referencia rota |
| 9ec59c0900c0ad3cecaa | Matriculas Runt | tableEx | Sí | 6 | 477 | 514 | 234 | 15000 | — | Referencia rota | No | Referencia rota |
| b17bc88120b65a105648 | Segmentación: Trimestre (Entregas Totales[Q]) | slicer | No | 871 | 80 | 162 | 65 | 29000 | — | Con binding válido | No | En uso |
| b932373a0b2007733b39 | Imagen: Logo-CasaToro4243506339860492.png | image | No | 1138 | 23 | 112 | 38 | 10000 | — | Decorativo | No | En uso |
| c71b214a210160202d5d | Forma sin título | shape | No | 0 | 0 | 1280 | 157 | 8000 | — | Decorativo | No | En uso |
| de06c3fb442c76b90246 | Empresas renting activas | card | No | 448 | 163 | 221 | 74 | 20000 | — | Con binding válido | No | En uso |
| edd05e9bad4b3666886d | Ticket promedio | card | No | 675 | 163 | 221 | 74 | 25000 | — | Con binding válido | No | En uso |
| f190480c104bb03dd85d | Segmentación: Año (Entregas Totales[año]) | slicer | No | 9 | 79 | 127 | 65 | 18000 | — | Con binding válido | No | En uso |
| f1b741b023b29010d540 | Segmentación: Tecnología (Entregas Totales[combustible]) | slicer | No | 705 | 79 | 163 | 66 | 27000 | — | Con binding válido | No | En uso |
| f95237a70a2b397ab6c0 | Participación por mecanización | pieChart | Sí | 814 | 244 | 459 | 234 | 0 | — | Referencia rota | No | Referencia rota |

Bindings de Dashboard_Renting (63):

| visual_id | Visual | Rol | Campo | Agregación | Referencia |
|---|---|---|---|---|---|
| 0de40f160ad554410865 | Matriculas por marca | Group | RUNT[MARCA] | — | Rota |
| 0de40f160ad554410865 | Matriculas por marca | Values | RUNT[CTD] | Sum | Rota |
| 1a394380135072c054c8 | Rendimiento (t/ha) | Category | Cultivos[Municipio] | — | Rota |
| 1a394380135072c054c8 | Rendimiento (t/ha) | Category | Cultivos[Val periodo] | — | Rota |
| 1a394380135072c054c8 | Rendimiento (t/ha) | Series | Cultivos[Desagregación cultivo] | — | Rota |
| 1a394380135072c054c8 | Rendimiento (t/ha) | Y | Cultivos[Rendimiento (t/ha)] | Sum | Rota |
| 2b6d4c39222aa4000302 | Mecanización por regional | Category | Cultivos[Regional] | — | Rota |
| 2b6d4c39222aa4000302 | Mecanización por regional | Series | Cultivos[municipios mecanizables] | — | Rota |
| 2b6d4c39222aa4000302 | Mecanización por regional | Y | Cultivos[Área sembrada (ha)] | Sum | Rota |
| 3481c97f911715717734 | Unidades facturadas por empresa de Renting y trimestre | Values | Entregas Totales[val nombre] | — | Válida |
| 3481c97f911715717734 | Unidades facturadas por empresa de Renting y trimestre | Values | Entregas Totales[Q1] | — | Válida |
| 3481c97f911715717734 | Unidades facturadas por empresa de Renting y trimestre | Values | Entregas Totales[Q2] | — | Válida |
| 3481c97f911715717734 | Unidades facturadas por empresa de Renting y trimestre | Values | Entregas Totales[Q3] | — | Válida |
| 3481c97f911715717734 | Unidades facturadas por empresa de Renting y trimestre | Values | Entregas Totales[Q4] | — | Válida |
| 3481c97f911715717734 | Unidades facturadas por empresa de Renting y trimestre | Values | Entregas Totales[cantidad de maquinas] | — | Válida |
| 3481c97f911715717734 | Unidades facturadas por empresa de Renting y trimestre | Values | Entregas Totales[Crecimiento Q1→Q4] | — | Válida |
| 44e4621d600343c70058 | Matriculas por modelo | Group | RUNT[MODELO] | — | Rota |
| 44e4621d600343c70058 | Matriculas por modelo | Values | RUNT[CTD] | Sum | Rota |
| 4a086741483d06edbbe1 | Especificación Importadores | Values | Importaciones[IMPORTADOR] | — | Rota |
| 4a086741483d06edbbe1 | Especificación Importadores | Values | Importaciones[MARCA] | — | Rota |
| 4a086741483d06edbbe1 | Especificación Importadores | Values | Importaciones[MERCADO] | — | Rota |
| 4a086741483d06edbbe1 | Especificación Importadores | Values | Importaciones[MODELO] | — | Rota |
| 4a086741483d06edbbe1 | Especificación Importadores | Values | Importaciones[CAPACIDAD] | — | Rota |
| 4a086741483d06edbbe1 | Especificación Importadores | Values | Importaciones[CTD] | Sum | Rota |
| 4caed66b2e79ca489edc | Total unidades renting | Values | Entregas Totales[cantidad de maquinas] | — | Válida |
| 5ce335d4e237c11a70e2 | Unidades RENTING por empresa y trimestre | Category | Entregas Totales[val nombre] | — | Válida |
| 5ce335d4e237c11a70e2 | Unidades RENTING por empresa y trimestre | Series | Entregas Totales[Q] | — | Válida |
| 5ce335d4e237c11a70e2 | Unidades RENTING por empresa y trimestre | Y | Entregas Totales[cantidad de maquinas] | — | Válida |
| 647df1e1caca5a76abc8 | Producción (T) | Category | Cultivos[Municipio] | — | Rota |
| 647df1e1caca5a76abc8 | Producción (T) | Category | Cultivos[Val periodo] | — | Rota |
| 647df1e1caca5a76abc8 | Producción (T) | Y | Cultivos[Producción (t)] | Sum | Rota |
| 710b4bdd807785877d66 | Importaciones (CIF) | Category | Importaciones[MARCA] | — | Rota |
| 710b4bdd807785877d66 | Importaciones (CIF) | Y | Importaciones[CIF TOTAL USD] | Sum | Rota |
| 710b4bdd807785877d66 | Importaciones (CIF) | Formato/propiedad | Importaciones[IMPORTADOR] | — | Formato huérfano |
| 7372de39e4387230a26c | Mecanizacion por departamento | Category | Cultivos[Departamento] | — | Rota |
| 7372de39e4387230a26c | Mecanizacion por departamento | Series | Cultivos[municipios mecanizables] | — | Rota |
| 7372de39e4387230a26c | Mecanizacion por departamento | Y | Cultivos[Área sembrada (ha)] | Sum | Rota |
| 8106d7c0e70d14e3cc6e | Importaciones | Category | Importaciones[MARCA] | — | Rota |
| 8106d7c0e70d14e3cc6e | Importaciones | Y | Importaciones[CTD] | Sum | Rota |
| 8106d7c0e70d14e3cc6e | Importaciones | Formato/propiedad | Importaciones[IMPORTADOR] | — | Formato huérfano |
| 86925930b70b966b6025 | Segmentación: Entregas Totales[Gama] | Values | Entregas Totales[Gama] | — | Válida |
| 8b1429e26c4c808079c8 | Segmentación: Entregas Totales[Centro] | Values | Entregas Totales[Centro] | — | Válida |
| 918d228ab18d5045e510 | Utilidad bruta total | Values | Entregas Totales[Valor] | Sum | Válida |
| 943ad7553bad0a0283bb | Segmentación: Entregas Totales[Marca] | Values | Entregas Totales[Marca] | — | Válida |
| 9734d2820ecd3ae8a0a0 | Última Actualización | Values | Fecha De Actualización[Fecha De Actualización] | Min | Válida |
| 9c9f9e7740ae80a69e13 | Participación por cultivo área sembrada has (TOP 5) | Category | Cultivos[Desagregación cultivo] | — | Rota |
| 9c9f9e7740ae80a69e13 | Participación por cultivo área sembrada has (TOP 5) | Y | Cultivos[Área sembrada (ha)] | Sum | Rota |
| 9c9f9e7740ae80a69e13 | Participación por cultivo área sembrada has (TOP 5) | Formato/propiedad | spiga_CotizacionesVN[IntencionesCompraDescripcion] | — | Formato huérfano |
| 9c9f9e7740ae80a69e13 | Participación por cultivo área sembrada has (TOP 5) | Formato/propiedad | spiga_CotizacionesVN[Ganadas perdidas] | — | Formato huérfano |
| 9c9f9e7740ae80a69e13 | Participación por cultivo área sembrada has (TOP 5) | Formato/propiedad | Cultivos[Cultivo] | — | Formato huérfano |
| 9ec59c0900c0ad3cecaa | Matriculas Runt | Values | RUNT[MUNICIPIO] | — | Rota |
| 9ec59c0900c0ad3cecaa | Matriculas Runt | Values | RUNT[MERCADO] | — | Rota |
| 9ec59c0900c0ad3cecaa | Matriculas Runt | Values | RUNT[MARCA] | — | Rota |
| 9ec59c0900c0ad3cecaa | Matriculas Runt | Values | RUNT[MODELO] | — | Rota |
| 9ec59c0900c0ad3cecaa | Matriculas Runt | Values | RUNT[CAPACIDAD] | — | Rota |
| 9ec59c0900c0ad3cecaa | Matriculas Runt | Values | RUNT[CTD] | Sum | Rota |
| b17bc88120b65a105648 | Segmentación: Trimestre (Entregas Totales[Q]) | Values | Entregas Totales[Q] | — | Válida |
| de06c3fb442c76b90246 | Empresas renting activas | Values | Entregas Totales[val nombre] | Count | Válida |
| edd05e9bad4b3666886d | Ticket promedio | Values | Entregas Totales[Ticket promedio] | — | Válida |
| f190480c104bb03dd85d | Segmentación: Año (Entregas Totales[año]) | Values | Entregas Totales[año] | — | Válida |
| f1b741b023b29010d540 | Segmentación: Tecnología (Entregas Totales[combustible]) | Values | Entregas Totales[combustible] | — | Válida |
| f95237a70a2b397ab6c0 | Participación por mecanización | Category | Cultivos[municipios mecanizables] | — | Rota |
| f95237a70a2b397ab6c0 | Participación por mecanización | Y | Cultivos[Área sembrada (ha)] | Sum | Rota |

## 9.2 Dashboard_Convenios (`b597e26007760b8239c0`) — 31 visuales

| visual_id | Nombre | Tipo | Oculto | x | y | Ancho | Alto | z | Grupo | Clase | Formato huérfano | Estado de uso |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| 021d4850b3401880b984 | Matriculas Runt | tableEx | Sí | 6 | 477 | 514 | 234 | 15000 | — | Referencia rota | No | Referencia rota |
| 0c7758c3cc20d57abc42 | Segmentación: Convenio (Entregas Totales[procedenciadetalle]) | slicer | No | 803 | 80 | 162 | 67 | 29000 | — | Con binding válido | No | En uso |
| 164619eb8a032ec27532 | Matriculas por modelo | treemap | Sí | 6 | 477 | 514 | 231 | 4000 | — | Referencia rota | No | Referencia rota |
| 1e6271e61744ac760b0a | Importaciones | lineClusteredColumnComboChart | Sí | 526 | 477 | 746 | 231 | 17000 | — | Referencia rota | Sí | Referencia rota |
| 2706c287d7d0e875d946 | Unidades por convenio: S1 vs S2 | lineClusteredColumnComboChart | No | 662 | 243 | 608 | 232 | 28000 | — | Con binding válido | No | En uso |
| 3627bccc9714708ee3dd | Matriculas por marca | treemap | Sí | 6 | 477 | 514 | 231 | 5000 | — | Referencia rota | No | Referencia rota |
| 3895cca635d3a5b0eaaa | Imagen: Logo-CasaToro4243506339860492.png | image | No | 1138 | 23 | 112 | 38 | 10000 | — | Decorativo | No | En uso |
| 461e004b2d94001390d3 | Segmentación: Entregas Totales[Gama] | slicer | No | 295 | 80 | 170 | 65 | 19000 | — | Con binding válido | No | En uso |
| 516e2b982c4c10399c17 | Segmentación: Trimestre (Entregas Totales[Q]) | slicer | No | 970 | 80 | 162 | 67 | 30000 | — | Con binding válido | No | En uso |
| 54b7ca7d26135b942cd9 | Segmentación: Entregas Totales[Centro] | slicer | No | 469 | 80 | 163 | 65 | 21000 | — | Con binding válido | No | En uso |
| 5f7e3e000ac60870579e | Utilidad bruta total | card | No | 786 | 163 | 221 | 74 | 25000 | — | Con binding válido | No | En uso |
| 6dd1451dbdca03ca528e | Producción (T) | lineClusteredColumnComboChart | Sí | 369 | 484 | 439 | 227 | 7000 | — | Referencia rota | No | Referencia rota |
| 6e4fc275427d71c147c7 | Rendimiento (t/ha) | lineClusteredColumnComboChart | Sí | 369 | 484 | 439 | 226 | 6000 | — | Referencia rota | No | Referencia rota |
| 7d4ca467440bb30d6806 | Mecanizacion por departamento | barChart | Sí | 814 | 244 | 459 | 234 | 1000 | — | Referencia rota | No | Referencia rota |
| 9769d8556306a6bbd114 | Última Actualización | card | No | 209 | 17 | 207 | 51 | 12000 | — | Con binding válido | No | En uso |
| 98932c329244ca1c0423 | Forma sin título | shape | No | 0 | 0 | 1280 | 157 | 8000 | — | Decorativo | No | En uso |
| 9a88093ab5402c6e7a10 | Convenios vigentes hoy | card | No | 557 | 163 | 221 | 74 | 20000 | — | Con binding válido | No | En uso |
| 9fd256fc444b2ac5015b | Participación por convenio (unidades año) | pieChart | No | 662 | 480 | 608 | 231 | 27000 | — | Con binding válido | Sí | En uso |
| ac23df6f245ac18edcee | Convenios | textbox | No | 14 | 11 | 178 | 54 | 9000 | — | Decorativo | No | En uso |
| b0bdeb16560aa2033e76 | Total unidades convenios | card | No | 329 | 163 | 221 | 74 | 24000 | — | Con binding válido | No | En uso |
| b754c1660bd8235ebd7d | Participación por cultivo área sembrada has (TOP 5) | pieChart | Sí | 369 | 243 | 439 | 235 | 14000 | — | Referencia rota | Sí | Referencia rota |
| bb6805c59a193b8553d0 | Imagen: Logo-Nebula_(1)8124617426694213.png | image | No | 1028 | 27 | 121 | 29 | 22000 | — | Decorativo | No | En uso |
| bdbd9cf43aebce83d659 | Segmentación: Entregas Totales[Marca] | slicer | No | 135 | 80 | 157 | 65 | 13000 | — | Con binding válido | No | En uso |
| c5aed3df5c828c0e0f50 | Segmentación: Año (Entregas Totales[año]) | slicer | No | 3 | 80 | 127 | 65 | 18000 | — | Con binding válido | No | En uso |
| d1c4d3f2924268689638 | Mecanización por regional | barChart | Sí | 814 | 244 | 459 | 234 | 2000 | — | Referencia rota | No | Referencia rota |
| d556fd700091e6362812 | Forma sin título | shape | No | 187 | 22 | 15 | 42 | 11000 | — | Decorativo | No | En uso |
| d63f39364345bc22e6ea | Especificación Importadores | tableEx | Sí | 526 | 477 | 746 | 232 | 16000 | — | Referencia rota | No | Referencia rota |
| d94300db464811900cc6 | Segmentación: Combustible (Entregas Totales[combustible]) | slicer | No | 637 | 79 | 163 | 66 | 26000 | — | Con binding válido | No | En uso |
| ed7dcba836dbc5a82b07 | Importaciones (CIF) | lineClusteredColumnComboChart | Sí | 526 | 477 | 746 | 231 | 3000 | — | Referencia rota | Sí | Referencia rota |
| eea7905600e9569dd64e | Participación por convenio y tasa de recambio | tableEx | No | 24 | 243 | 630 | 468 | 23000 | — | Con binding válido | No | En uso |
| fd63ac47e9e00c202bcd | Participación por mecanización | pieChart | Sí | 814 | 244 | 459 | 234 | 0 | — | Referencia rota | No | Referencia rota |

Bindings de Dashboard_Convenios (70):

| visual_id | Visual | Rol | Campo | Agregación | Referencia |
|---|---|---|---|---|---|
| 021d4850b3401880b984 | Matriculas Runt | Values | RUNT[MUNICIPIO] | — | Rota |
| 021d4850b3401880b984 | Matriculas Runt | Values | RUNT[MERCADO] | — | Rota |
| 021d4850b3401880b984 | Matriculas Runt | Values | RUNT[MARCA] | — | Rota |
| 021d4850b3401880b984 | Matriculas Runt | Values | RUNT[MODELO] | — | Rota |
| 021d4850b3401880b984 | Matriculas Runt | Values | RUNT[CAPACIDAD] | — | Rota |
| 021d4850b3401880b984 | Matriculas Runt | Values | RUNT[CTD] | Sum | Rota |
| 0c7758c3cc20d57abc42 | Segmentación: Convenio (Entregas Totales[procedenciadetalle]) | Values | Entregas Totales[procedenciadetalle] | — | Válida |
| 164619eb8a032ec27532 | Matriculas por modelo | Group | RUNT[MODELO] | — | Rota |
| 164619eb8a032ec27532 | Matriculas por modelo | Values | RUNT[CTD] | Sum | Rota |
| 1e6271e61744ac760b0a | Importaciones | Category | Importaciones[MARCA] | — | Rota |
| 1e6271e61744ac760b0a | Importaciones | Y | Importaciones[CTD] | Sum | Rota |
| 1e6271e61744ac760b0a | Importaciones | Formato/propiedad | Importaciones[IMPORTADOR] | — | Formato huérfano |
| 2706c287d7d0e875d946 | Unidades por convenio: S1 vs S2 | Category | Entregas Totales[procedenciadetalle] | — | Válida |
| 2706c287d7d0e875d946 | Unidades por convenio: S1 vs S2 | Series | Entregas Totales[DIVISION S] | — | Válida |
| 2706c287d7d0e875d946 | Unidades por convenio: S1 vs S2 | Y | Entregas Totales[cantidad de maquinas] | — | Válida |
| 3627bccc9714708ee3dd | Matriculas por marca | Group | RUNT[MARCA] | — | Rota |
| 3627bccc9714708ee3dd | Matriculas por marca | Values | RUNT[CTD] | Sum | Rota |
| 461e004b2d94001390d3 | Segmentación: Entregas Totales[Gama] | Values | Entregas Totales[Gama] | — | Válida |
| 516e2b982c4c10399c17 | Segmentación: Trimestre (Entregas Totales[Q]) | Values | Entregas Totales[Q] | — | Válida |
| 54b7ca7d26135b942cd9 | Segmentación: Entregas Totales[Centro] | Values | Entregas Totales[Centro] | — | Válida |
| 5f7e3e000ac60870579e | Utilidad bruta total | Values | Entregas Totales[Valor] | Sum | Válida |
| 6dd1451dbdca03ca528e | Producción (T) | Category | Cultivos[Municipio] | — | Rota |
| 6dd1451dbdca03ca528e | Producción (T) | Category | Cultivos[Val periodo] | — | Rota |
| 6dd1451dbdca03ca528e | Producción (T) | Y | Cultivos[Producción (t)] | Sum | Rota |
| 6e4fc275427d71c147c7 | Rendimiento (t/ha) | Category | Cultivos[Municipio] | — | Rota |
| 6e4fc275427d71c147c7 | Rendimiento (t/ha) | Category | Cultivos[Val periodo] | — | Rota |
| 6e4fc275427d71c147c7 | Rendimiento (t/ha) | Series | Cultivos[Desagregación cultivo] | — | Rota |
| 6e4fc275427d71c147c7 | Rendimiento (t/ha) | Y | Cultivos[Rendimiento (t/ha)] | Sum | Rota |
| 7d4ca467440bb30d6806 | Mecanizacion por departamento | Category | Cultivos[Departamento] | — | Rota |
| 7d4ca467440bb30d6806 | Mecanizacion por departamento | Series | Cultivos[municipios mecanizables] | — | Rota |
| 7d4ca467440bb30d6806 | Mecanizacion por departamento | Y | Cultivos[Área sembrada (ha)] | Sum | Rota |
| 9769d8556306a6bbd114 | Última Actualización | Values | Fecha De Actualización[Fecha De Actualización] | Min | Válida |
| 9a88093ab5402c6e7a10 | Convenios vigentes hoy | Values | Entregas Totales[procedenciadetalle] | Count | Válida |
| 9fd256fc444b2ac5015b | Participación por convenio (unidades año) | Category | Entregas Totales[procedenciadetalle] | — | Válida |
| 9fd256fc444b2ac5015b | Participación por convenio (unidades año) | Y | Entregas Totales[cantidad de maquinas] | — | Válida |
| 9fd256fc444b2ac5015b | Participación por convenio (unidades año) | Formato/propiedad | spiga_CotizacionesVN[IntencionesCompraDescripcion] | — | Formato huérfano |
| 9fd256fc444b2ac5015b | Participación por convenio (unidades año) | Formato/propiedad | spiga_CotizacionesVN[Ganadas perdidas] | — | Formato huérfano |
| 9fd256fc444b2ac5015b | Participación por convenio (unidades año) | Formato/propiedad | Cultivos[Cultivo] | — | Formato huérfano |
| b0bdeb16560aa2033e76 | Total unidades convenios | Values | Entregas Totales[año] | CountNonNull | Válida |
| b754c1660bd8235ebd7d | Participación por cultivo área sembrada has (TOP 5) | Category | Cultivos[Desagregación cultivo] | — | Rota |
| b754c1660bd8235ebd7d | Participación por cultivo área sembrada has (TOP 5) | Y | Cultivos[Área sembrada (ha)] | Sum | Rota |
| b754c1660bd8235ebd7d | Participación por cultivo área sembrada has (TOP 5) | Formato/propiedad | spiga_CotizacionesVN[IntencionesCompraDescripcion] | — | Formato huérfano |
| b754c1660bd8235ebd7d | Participación por cultivo área sembrada has (TOP 5) | Formato/propiedad | spiga_CotizacionesVN[Ganadas perdidas] | — | Formato huérfano |
| b754c1660bd8235ebd7d | Participación por cultivo área sembrada has (TOP 5) | Formato/propiedad | Cultivos[Cultivo] | — | Formato huérfano |
| bdbd9cf43aebce83d659 | Segmentación: Entregas Totales[Marca] | Values | Entregas Totales[Marca] | — | Válida |
| c5aed3df5c828c0e0f50 | Segmentación: Año (Entregas Totales[año]) | Values | Entregas Totales[año] | — | Válida |
| d1c4d3f2924268689638 | Mecanización por regional | Category | Cultivos[Regional] | — | Rota |
| d1c4d3f2924268689638 | Mecanización por regional | Series | Cultivos[municipios mecanizables] | — | Rota |
| d1c4d3f2924268689638 | Mecanización por regional | Y | Cultivos[Área sembrada (ha)] | Sum | Rota |
| d63f39364345bc22e6ea | Especificación Importadores | Values | Importaciones[IMPORTADOR] | — | Rota |
| d63f39364345bc22e6ea | Especificación Importadores | Values | Importaciones[MARCA] | — | Rota |
| d63f39364345bc22e6ea | Especificación Importadores | Values | Importaciones[MERCADO] | — | Rota |
| d63f39364345bc22e6ea | Especificación Importadores | Values | Importaciones[MODELO] | — | Rota |
| d63f39364345bc22e6ea | Especificación Importadores | Values | Importaciones[CAPACIDAD] | — | Rota |
| d63f39364345bc22e6ea | Especificación Importadores | Values | Importaciones[CTD] | Sum | Rota |
| d94300db464811900cc6 | Segmentación: Combustible (Entregas Totales[combustible]) | Values | Entregas Totales[combustible] | — | Válida |
| ed7dcba836dbc5a82b07 | Importaciones (CIF) | Category | Importaciones[MARCA] | — | Rota |
| ed7dcba836dbc5a82b07 | Importaciones (CIF) | Y | Importaciones[CIF TOTAL USD] | Sum | Rota |
| ed7dcba836dbc5a82b07 | Importaciones (CIF) | Formato/propiedad | Importaciones[IMPORTADOR] | — | Formato huérfano |
| eea7905600e9569dd64e | Participación por convenio y tasa de recambio | Values | Entregas Totales[procedenciadetalle] | — | Válida |
| eea7905600e9569dd64e | Participación por convenio y tasa de recambio | Values | Entregas Totales[Q1] | — | Válida |
| eea7905600e9569dd64e | Participación por convenio y tasa de recambio | Values | Entregas Totales[Q2] | — | Válida |
| eea7905600e9569dd64e | Participación por convenio y tasa de recambio | Values | Entregas Totales[Q3] | — | Válida |
| eea7905600e9569dd64e | Participación por convenio y tasa de recambio | Values | Entregas Totales[Q4] | — | Válida |
| eea7905600e9569dd64e | Participación por convenio y tasa de recambio | Values | Entregas Totales[cantidad de maquinas] | — | Válida |
| eea7905600e9569dd64e | Participación por convenio y tasa de recambio | Values | Expresión «%Participacion» | Cálculo visual | Válida |
| eea7905600e9569dd64e | Participación por convenio y tasa de recambio | Values | Entregas Totales[Recambio semestral] | — | Válida |
| eea7905600e9569dd64e | Participación por convenio y tasa de recambio | Values | Entregas Totales[Recambio anual (vs año ant.)] | — | Válida |
| fd63ac47e9e00c202bcd | Participación por mecanización | Category | Cultivos[municipios mecanizables] | — | Rota |
| fd63ac47e9e00c202bcd | Participación por mecanización | Y | Cultivos[Área sembrada (ha)] | Sum | Rota |

## 9.3 Dashboard_Empresas (`377df594a011ae294444`) — 32 visuales

| visual_id | Nombre | Tipo | Oculto | x | y | Ancho | Alto | z | Grupo | Clase | Formato huérfano | Estado de uso |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| 1ab49030c00e0a200aa4 | Empresas distintas | card | No | 448 | 166 | 221 | 74 | 21000 | — | Con binding válido | No | En uso |
| 1bef27578e3349425a36 | Forma sin título | shape | No | 0 | 0 | 1280 | 157 | 8000 | — | Decorativo | No | En uso |
| 207ac3eed23edebbbe0c | Última Actualización | card | No | 199 | 17 | 207 | 51 | 12000 | — | Con binding válido | No | En uso |
| 37a787e9cc28cd09e57b | Matriculas Runt | tableEx | Sí | 6 | 477 | 514 | 234 | 15000 | — | Referencia rota | No | Referencia rota |
| 47d666fc117c70ae6c77 | Participación por mecanización | pieChart | Sí | 814 | 244 | 459 | 234 | 0 | — | Referencia rota | No | Referencia rota |
| 4d5f0482cc10734db587 | Segmentación: Tecnología (Entregas Totales[combustible]) | slicer | No | 875 | 80 | 162 | 65 | 27000 | — | Con binding válido | No | En uso |
| 531799925cdc0008407b | Segmentación: Año (Entregas Totales[año]) | slicer | No | 3 | 80 | 127 | 65 | 18000 | — | Con binding válido | No | En uso |
| 6e32a80f73419213d127 | Matriculas por marca | treemap | Sí | 6 | 477 | 514 | 231 | 5000 | — | Referencia rota | No | Referencia rota |
| 71f234fbb753194aa2e1 | Forma sin título | shape | No | 177 | 22 | 15 | 42 | 11000 | — | Decorativo | No | En uso |
| 7342d316766131600462 | Imagen: Logo-Nebula_(1)8124617426694213.png | image | No | 1028 | 27 | 121 | 29 | 23000 | — | Decorativo | No | En uso |
| 742a219cd1940a983530 | Importaciones | lineClusteredColumnComboChart | Sí | 526 | 477 | 746 | 231 | 17000 | — | Referencia rota | Sí | Referencia rota |
| 816c99a0a95005aa56b5 | Matriculas por modelo | treemap | Sí | 6 | 477 | 514 | 231 | 4000 | — | Referencia rota | No | Referencia rota |
| 81cdeccbcb7940787603 | Especificación Importadores | tableEx | Sí | 526 | 477 | 746 | 232 | 16000 | — | Referencia rota | No | Referencia rota |
| 856aee5d89c35b6c0aeb | Utilidad bruta total | card | No | 902 | 166 | 221 | 74 | 26000 | — | Con binding válido | No | En uso |
| 86c38682d276ded8a3ea | Segmentación: Trimestre (Entregas Totales[Q]) | slicer | No | 533 | 80 | 170 | 65 | 30000 | — | Con binding válido | No | En uso |
| 86f85bbed000b2922793 | Producción (T) | lineClusteredColumnComboChart | Sí | 369 | 484 | 439 | 227 | 7000 | — | Referencia rota | No | Referencia rota |
| 94deb273c33108980691 | Total unidades empresarial | card | No | 199 | 166 | 242 | 74 | 24000 | — | Con binding válido | No | En uso |
| 970c1dc21e6ec9001edd | Segmentación: Entregas Totales[Gama] | slicer | No | 358 | 80 | 170 | 65 | 20000 | — | Con binding válido | No | En uso |
| 9f04b9ce6587b5610998 | Rendimiento (t/ha) | lineClusteredColumnComboChart | Sí | 369 | 484 | 439 | 226 | 6000 | — | Referencia rota | No | Referencia rota |
| 9fe797a57a507ed03c40 | Segmentación: Entregas Totales[Marca] | slicer | No | 135 | 80 | 218 | 65 | 13000 | — | Con binding válido | No | En uso |
| a5ac6067ea2db9bdb8a7 | Imagen: Logo-CasaToro4243506339860492.png | image | No | 1138 | 23 | 112 | 38 | 10000 | — | Decorativo | No | En uso |
| a9dd82c51e4ab46d544b | Unidades por Gama x Tecnología (VENTA EMPRESARIAL) | tableEx | No | 11 | 250 | 619 | 452 | 28000 | — | Con binding válido | No | En uso |
| ab3e643b10d65600d211 | Conectividad | actionButton | No | 1170 | 212 | 100 | 28 | 19000 | — | Botón/acción | No | En uso |
| aff3f4a45ab91a74047e | Importaciones (CIF) | lineClusteredColumnComboChart | Sí | 526 | 477 | 746 | 231 | 3000 | — | Referencia rota | Sí | Referencia rota |
| b2df3c91709631415d59 | Segmentación: Trimestre (Entregas Totales[Q]) | slicer | No | 1042 | 80 | 162 | 65 | 31000 | — | Con binding válido | No | En uso |
| b43695b0ad1280b26827 | Participación por cultivo área sembrada has (TOP 5) | pieChart | Sí | 369 | 243 | 439 | 235 | 14000 | — | Referencia rota | Sí | Referencia rota |
| e47ca6b0e42237a8ec22 | Mecanizacion por departamento | barChart | Sí | 814 | 244 | 459 | 234 | 1000 | — | Referencia rota | No | Referencia rota |
| f5ee68ca0ec050ca9ab2 | Empresas | textbox | No | 14 | 11 | 162 | 54 | 9000 | — | Decorativo | No | En uso |
| f78d86067470b0166e17 | Segmentación: Centro (Entregas Totales[Región]) | slicer | No | 708 | 80 | 162 | 65 | 22000 | — | Con binding válido | No | En uso |
| f8afa36aecb1ce0d8a16 | Ticket promedio | card | No | 675 | 166 | 221 | 74 | 25000 | — | Con binding válido | No | En uso |
| fcae268396d974c397bd | Mecanización por regional | barChart | Sí | 814 | 244 | 459 | 234 | 2000 | — | Referencia rota | No | Referencia rota |
| ff5b3bbb168650c17461 | Penetración de segmentos por Gama | lineClusteredColumnComboChart | No | 639 | 250 | 630 | 452 | 29000 | — | Con binding válido | No | En uso |

Bindings de Dashboard_Empresas (65):

| visual_id | Visual | Rol | Campo | Agregación | Referencia |
|---|---|---|---|---|---|
| 1ab49030c00e0a200aa4 | Empresas distintas | Values | Entregas Totales[procedenciadetalle] | Count | Válida |
| 207ac3eed23edebbbe0c | Última Actualización | Values | Fecha De Actualización[Fecha De Actualización] | Min | Válida |
| 37a787e9cc28cd09e57b | Matriculas Runt | Values | RUNT[MUNICIPIO] | — | Rota |
| 37a787e9cc28cd09e57b | Matriculas Runt | Values | RUNT[MERCADO] | — | Rota |
| 37a787e9cc28cd09e57b | Matriculas Runt | Values | RUNT[MARCA] | — | Rota |
| 37a787e9cc28cd09e57b | Matriculas Runt | Values | RUNT[MODELO] | — | Rota |
| 37a787e9cc28cd09e57b | Matriculas Runt | Values | RUNT[CAPACIDAD] | — | Rota |
| 37a787e9cc28cd09e57b | Matriculas Runt | Values | RUNT[CTD] | Sum | Rota |
| 47d666fc117c70ae6c77 | Participación por mecanización | Category | Cultivos[municipios mecanizables] | — | Rota |
| 47d666fc117c70ae6c77 | Participación por mecanización | Y | Cultivos[Área sembrada (ha)] | Sum | Rota |
| 4d5f0482cc10734db587 | Segmentación: Tecnología (Entregas Totales[combustible]) | Values | Entregas Totales[combustible] | — | Válida |
| 531799925cdc0008407b | Segmentación: Año (Entregas Totales[año]) | Values | Entregas Totales[año] | — | Válida |
| 6e32a80f73419213d127 | Matriculas por marca | Group | RUNT[MARCA] | — | Rota |
| 6e32a80f73419213d127 | Matriculas por marca | Values | RUNT[CTD] | Sum | Rota |
| 742a219cd1940a983530 | Importaciones | Category | Importaciones[MARCA] | — | Rota |
| 742a219cd1940a983530 | Importaciones | Y | Importaciones[CTD] | Sum | Rota |
| 742a219cd1940a983530 | Importaciones | Formato/propiedad | Importaciones[IMPORTADOR] | — | Formato huérfano |
| 816c99a0a95005aa56b5 | Matriculas por modelo | Group | RUNT[MODELO] | — | Rota |
| 816c99a0a95005aa56b5 | Matriculas por modelo | Values | RUNT[CTD] | Sum | Rota |
| 81cdeccbcb7940787603 | Especificación Importadores | Values | Importaciones[IMPORTADOR] | — | Rota |
| 81cdeccbcb7940787603 | Especificación Importadores | Values | Importaciones[MARCA] | — | Rota |
| 81cdeccbcb7940787603 | Especificación Importadores | Values | Importaciones[MERCADO] | — | Rota |
| 81cdeccbcb7940787603 | Especificación Importadores | Values | Importaciones[MODELO] | — | Rota |
| 81cdeccbcb7940787603 | Especificación Importadores | Values | Importaciones[CAPACIDAD] | — | Rota |
| 81cdeccbcb7940787603 | Especificación Importadores | Values | Importaciones[CTD] | Sum | Rota |
| 856aee5d89c35b6c0aeb | Utilidad bruta total | Values | Entregas Totales[Valor] | Sum | Válida |
| 86c38682d276ded8a3ea | Segmentación: Trimestre (Entregas Totales[Q]) | Values | Entregas Totales[Q] | — | Válida |
| 86f85bbed000b2922793 | Producción (T) | Category | Cultivos[Municipio] | — | Rota |
| 86f85bbed000b2922793 | Producción (T) | Category | Cultivos[Val periodo] | — | Rota |
| 86f85bbed000b2922793 | Producción (T) | Y | Cultivos[Producción (t)] | Sum | Rota |
| 94deb273c33108980691 | Total unidades empresarial | Values | Entregas Totales[año] | CountNonNull | Válida |
| 970c1dc21e6ec9001edd | Segmentación: Entregas Totales[Gama] | Values | Entregas Totales[Gama] | — | Válida |
| 9f04b9ce6587b5610998 | Rendimiento (t/ha) | Category | Cultivos[Municipio] | — | Rota |
| 9f04b9ce6587b5610998 | Rendimiento (t/ha) | Category | Cultivos[Val periodo] | — | Rota |
| 9f04b9ce6587b5610998 | Rendimiento (t/ha) | Series | Cultivos[Desagregación cultivo] | — | Rota |
| 9f04b9ce6587b5610998 | Rendimiento (t/ha) | Y | Cultivos[Rendimiento (t/ha)] | Sum | Rota |
| 9fe797a57a507ed03c40 | Segmentación: Entregas Totales[Marca] | Values | Entregas Totales[Marca] | — | Válida |
| a9dd82c51e4ab46d544b | Unidades por Gama x Tecnología (VENTA EMPRESARIAL) | Values | Entregas Totales[NombreTercero] | — | Válida |
| a9dd82c51e4ab46d544b | Unidades por Gama x Tecnología (VENTA EMPRESARIAL) | Values | Entregas Totales[Q1] | — | Válida |
| a9dd82c51e4ab46d544b | Unidades por Gama x Tecnología (VENTA EMPRESARIAL) | Values | Entregas Totales[Q2] | — | Válida |
| a9dd82c51e4ab46d544b | Unidades por Gama x Tecnología (VENTA EMPRESARIAL) | Values | Entregas Totales[Q3] | — | Válida |
| a9dd82c51e4ab46d544b | Unidades por Gama x Tecnología (VENTA EMPRESARIAL) | Values | Entregas Totales[Q4] | — | Válida |
| a9dd82c51e4ab46d544b | Unidades por Gama x Tecnología (VENTA EMPRESARIAL) | Values | Entregas Totales[cantidad de maquinas] | — | Válida |
| a9dd82c51e4ab46d544b | Unidades por Gama x Tecnología (VENTA EMPRESARIAL) | Values | Expresión «%Participacion» | Cálculo visual | Válida |
| a9dd82c51e4ab46d544b | Unidades por Gama x Tecnología (VENTA EMPRESARIAL) | Formato/propiedad | Entregas Totales[Q] | — | Válida |
| aff3f4a45ab91a74047e | Importaciones (CIF) | Category | Importaciones[MARCA] | — | Rota |
| aff3f4a45ab91a74047e | Importaciones (CIF) | Y | Importaciones[CIF TOTAL USD] | Sum | Rota |
| aff3f4a45ab91a74047e | Importaciones (CIF) | Formato/propiedad | Importaciones[IMPORTADOR] | — | Formato huérfano |
| b2df3c91709631415d59 | Segmentación: Trimestre (Entregas Totales[Q]) | Values | Entregas Totales[Q] | — | Válida |
| b43695b0ad1280b26827 | Participación por cultivo área sembrada has (TOP 5) | Category | Cultivos[Desagregación cultivo] | — | Rota |
| b43695b0ad1280b26827 | Participación por cultivo área sembrada has (TOP 5) | Y | Cultivos[Área sembrada (ha)] | Sum | Rota |
| b43695b0ad1280b26827 | Participación por cultivo área sembrada has (TOP 5) | Formato/propiedad | spiga_CotizacionesVN[IntencionesCompraDescripcion] | — | Formato huérfano |
| b43695b0ad1280b26827 | Participación por cultivo área sembrada has (TOP 5) | Formato/propiedad | spiga_CotizacionesVN[Ganadas perdidas] | — | Formato huérfano |
| b43695b0ad1280b26827 | Participación por cultivo área sembrada has (TOP 5) | Formato/propiedad | Cultivos[Cultivo] | — | Formato huérfano |
| e47ca6b0e42237a8ec22 | Mecanizacion por departamento | Category | Cultivos[Departamento] | — | Rota |
| e47ca6b0e42237a8ec22 | Mecanizacion por departamento | Series | Cultivos[municipios mecanizables] | — | Rota |
| e47ca6b0e42237a8ec22 | Mecanizacion por departamento | Y | Cultivos[Área sembrada (ha)] | Sum | Rota |
| f78d86067470b0166e17 | Segmentación: Centro (Entregas Totales[Región]) | Values | Entregas Totales[Región] | — | Válida |
| f8afa36aecb1ce0d8a16 | Ticket promedio | Values | Entregas Totales[año] | CountNonNull | Válida |
| fcae268396d974c397bd | Mecanización por regional | Category | Cultivos[Regional] | — | Rota |
| fcae268396d974c397bd | Mecanización por regional | Series | Cultivos[municipios mecanizables] | — | Rota |
| fcae268396d974c397bd | Mecanización por regional | Y | Cultivos[Área sembrada (ha)] | Sum | Rota |
| ff5b3bbb168650c17461 | Penetración de segmentos por Gama | Category | Entregas Totales[Gama] | — | Válida |
| ff5b3bbb168650c17461 | Penetración de segmentos por Gama | Series | Entregas Totales[Q] | — | Válida |
| ff5b3bbb168650c17461 | Penetración de segmentos por Gama | Y | Entregas Totales[cantidad de maquinas] | — | Válida |

## 9.4 Conciliación por página

| page_id | Página | visual.json en PBIP | Fichas | Con binding válido | Decorativos | Botones/acciones | Con referencia rota | Suma | Con formato huérfano (informativo) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ac291ea509382034e4ab | Dashboard_Renting | 30 | 30 | 13 | 5 | 0 | 12 | 30 | 3 |
| b597e26007760b8239c0 | Dashboard_Convenios | 31 | 31 | 14 | 5 | 0 | 12 | 31 | 4 |
| 377df594a011ae294444 | Dashboard_Empresas | 32 | 32 | 14 | 5 | 1 | 12 | 32 | 3 |
| Total | — | 93 | 93 | 41 | 15 | 1 | 36 | 93 | 10 |

La columna «Suma» debe ser igual a «visual.json en PBIP». «Con formato huérfano» no suma: esos visuales ya están contados en su clase.

# 10. KPIs

Se listan los visuales de tipo tarjeta o indicador con lo que calculan realmente.

| Página | visual_id | Título | Calcula | Oculto | Interpretación funcional |
|---|---|---|---|---|---|
| Dashboard_Empresas | 1ab49030c00e0a200aa4 | Empresas distintas | Count(Entregas Totales[procedenciadetalle]) | No | Pretende contar empresas distintas, pero calcula un conteo implícito de filas de la columna `procedenciadetalle`, no un conteo de valores únicos ni una medida; el valor puede no coincidir con el título (ver H-A11). |
| Dashboard_Empresas | 207ac3eed23edebbbe0c | Última Actualización | Min(Fecha De Actualización[Fecha De Actualización]) | No | Muestra la marca de tiempo del último refresco (reloj M de la tabla auxiliar Fecha De Actualización); coherente con el título. |
| Dashboard_Empresas | 856aee5d89c35b6c0aeb | Utilidad bruta total | Sum(Entregas Totales[Valor]) | No | Suma la columna `Entregas Totales[Valor]`; el título la rotula como «utilidad bruta», pero no se conoce la definición de `Valor` (ver V01), por lo que no puede confirmarse que corresponda a utilidad. |
| Dashboard_Empresas | 94deb273c33108980691 | Total unidades empresarial | CountNonNull(Entregas Totales[año]) | No | Pretende el total de unidades empresariales, pero cuenta filas no nulas de la columna `año`; coincide con el total de entregas solo si `año` nunca es nulo, y no es una medida (ver H-A12). |
| Dashboard_Empresas | f8afa36aecb1ce0d8a16 | Ticket promedio | CountNonNull(Entregas Totales[año]) | No | El título dice «ticket promedio», pero calcula un conteo de filas no nulas de `año`, no un promedio de valor por unidad; el valor no corresponde al título (ver H-A12). |
| Dashboard_Renting | 4caed66b2e79ca489edc | Total unidades renting | [cantidad de maquinas] | No | Usa la medida explícita [cantidad de maquinas]; coherente con el título (total de unidades en renting). |
| Dashboard_Renting | 918d228ab18d5045e510 | Utilidad bruta total | Sum(Entregas Totales[Valor]) | No | Suma `Entregas Totales[Valor]`; mismo caso que la tarjeta de Empresas: la definición de `Valor` no se conoce (ver V01), así que no se confirma que sea utilidad bruta. |
| Dashboard_Renting | 9734d2820ecd3ae8a0a0 | Última Actualización | Min(Fecha De Actualización[Fecha De Actualización]) | No | Marca de tiempo del último refresco; coherente con el título. |
| Dashboard_Renting | de06c3fb442c76b90246 | Empresas renting activas | Count(Entregas Totales[val nombre]) | No | Pretende contar empresas de renting activas, pero calcula un conteo implícito de filas de `val nombre`, no de valores únicos ni una medida; el valor puede no coincidir con el título (ver H-A13). |
| Dashboard_Renting | edd05e9bad4b3666886d | Ticket promedio | [Ticket promedio] | No | Usa la medida explícita [Ticket promedio]; coherente con el título. |
| Dashboard_Convenios | 5f7e3e000ac60870579e | Utilidad bruta total | Sum(Entregas Totales[Valor]) | No | Suma `Entregas Totales[Valor]`; igual que las otras dos tarjetas homónimas: la definición de `Valor` no se conoce (ver V01). |
| Dashboard_Convenios | 9769d8556306a6bbd114 | Última Actualización | Min(Fecha De Actualización[Fecha De Actualización]) | No | Marca de tiempo del último refresco; coherente con el título. |
| Dashboard_Convenios | 9a88093ab5402c6e7a10 | Convenios vigentes hoy | Count(Entregas Totales[procedenciadetalle]) | No | El título sugiere convenios vigentes a la fecha, pero calcula un conteo implícito de filas de `procedenciadetalle`, sin filtro de vigencia ni medida; el valor puede no coincidir con el título (ver H-A11). |
| Dashboard_Convenios | b0bdeb16560aa2033e76 | Total unidades convenios | CountNonNull(Entregas Totales[año]) | No | Pretende el total de unidades de convenios, pero cuenta filas no nulas de `año`; coincide con el total de entregas solo si `año` nunca es nulo, y no es una medida (ver H-A12). |

# 11. Filtros, segmentaciones e interacciones

## 11.1 Filtros (57)

Evidencia: `filterConfig` de `report.json` (Informe), `page.json` (Página) y `visual.json` (Visual).

| filter_id | Ámbito | Página | Visual | Campo | Tipo | Condición | Oculto | Bloqueado | Invertido |
|---|---|---|---|---|---|---|---|---|---|
| d41622559cc142bcc680 | Página | 377df594a011ae294444 · Dashboard_Empresas | — | Entregas Totales[Cantidad] | Categorical | Sin condición guardada | No | No | No |
| 569ba6f7876046e008bb | Página | 377df594a011ae294444 · Dashboard_Empresas | — | Entregas Totales[tipoventa_vista] | Categorical | IN (Flotas - Oficial, Flotas de Proximidad Oficial, Flotas Oficial, Flotilla Coorporativa) | No | No | No |
| b9e3f918c85149bec155 | Página | 377df594a011ae294444 · Dashboard_Empresas | — | Entregas Totales[val nombre] | Categorical | IN (OTROS) | No | No | No |
| ca0559980de30b75005c | Página | 377df594a011ae294444 · Dashboard_Empresas | — | Entregas Totales[procedencia] | Categorical | Sin condición guardada | No | No | true |
| 1c9f3cb585427a3b47a2 | Visual | 377df594a011ae294444 · Dashboard_Empresas | 47d666fc117c70ae6c77 · Participación por mecanización | Cultivos[municipios mecanizables] | Categorical | NOT IN (null) | No | No | true |
| db063270c737e05d5b70 | Visual | 377df594a011ae294444 · Dashboard_Empresas | 6e32a80f73419213d127 · Matriculas por marca | RUNT[MARCA] | TopN | TopN 10 | No | No | No |
| 62394049577f7b240bc6 | Visual | 377df594a011ae294444 · Dashboard_Empresas | 816c99a0a95005aa56b5 · Matriculas por modelo | RUNT[MODELO] | TopN | TopN 10 | No | No | No |
| b32d4a00c1cf0776efd0 | Visual | 377df594a011ae294444 · Dashboard_Empresas | 816c99a0a95005aa56b5 · Matriculas por modelo | RUNT[CTD] | Advanced | Sin condición guardada | No | No | No |
| 0dd984ebf688fa84ebbd | Visual | 377df594a011ae294444 · Dashboard_Empresas | b43695b0ad1280b26827 · Participación por cultivo área sembrada has (TOP 5) | Cultivos[val] | Advanced | Sin condición guardada | No | No | No |
| dbd31fbbc24a312b54ad | Visual | 377df594a011ae294444 · Dashboard_Empresas | b43695b0ad1280b26827 · Participación por cultivo área sembrada has (TOP 5) | Cultivos[Área sembrada (ha)] | Advanced | Sin condición guardada | No | No | No |
| 0934c9ddd0f02f56fd71 | Visual | 377df594a011ae294444 · Dashboard_Empresas | b43695b0ad1280b26827 · Participación por cultivo área sembrada has (TOP 5) | Cultivos[Desagregación cultivo] | TopN | TopN 5 | No | No | No |
| e41d2082933850a0ed80 | Visual | 377df594a011ae294444 · Dashboard_Empresas | e47ca6b0e42237a8ec22 · Mecanizacion por departamento | Cultivos[municipios mecanizables] | Categorical | NOT IN (null) | No | No | true |
| c45052fd23be11e1c569 | Visual | 377df594a011ae294444 · Dashboard_Empresas | fcae268396d974c397bd · Mecanización por regional | Cultivos[Regional] | Categorical | NOT IN (null) | No | No | true |
| e292f9044059e209a094 | Visual | 377df594a011ae294444 · Dashboard_Empresas | fcae268396d974c397bd · Mecanización por regional | Cultivos[municipios mecanizables] | Categorical | NOT IN (null) | No | No | true |
| d41622559cc142bcc680 | Página | ac291ea509382034e4ab · Dashboard_Renting | — | Entregas Totales[Cantidad] | Categorical | Sin condición guardada | No | No | No |
| 5967654bebb0c4008a32 | Página | ac291ea509382034e4ab · Dashboard_Renting | — | Entregas Totales[val nombre] | Categorical | NOT IN (OTROS) | No | No | true |
| d67d49bf38e596ce5020 | Visual | ac291ea509382034e4ab · Dashboard_Renting | 0de40f160ad554410865 · Matriculas por marca | RUNT[MARCA] | TopN | TopN 10 | No | No | No |
| c45052fd23be11e1c569 | Visual | ac291ea509382034e4ab · Dashboard_Renting | 2b6d4c39222aa4000302 · Mecanización por regional | Cultivos[Regional] | Categorical | NOT IN (null) | No | No | true |
| e292f9044059e209a094 | Visual | ac291ea509382034e4ab · Dashboard_Renting | 2b6d4c39222aa4000302 · Mecanización por regional | Cultivos[municipios mecanizables] | Categorical | NOT IN (null) | No | No | true |
| 8c3df5a668005eda4a9c | Visual | ac291ea509382034e4ab · Dashboard_Renting | 3481c97f911715717734 · Unidades facturadas por empresa de Renting y trimestre | Entregas Totales[val nombre] | Categorical | Sin condición guardada | No | No | No |
| c61619e04624c817a83b | Visual | ac291ea509382034e4ab · Dashboard_Renting | 3481c97f911715717734 · Unidades facturadas por empresa de Renting y trimestre | Entregas Totales[Q1] | Advanced | Sin condición guardada | No | No | No |
| fe32cfc0961ded23a284 | Visual | ac291ea509382034e4ab · Dashboard_Renting | 3481c97f911715717734 · Unidades facturadas por empresa de Renting y trimestre | Entregas Totales[Q2] | Advanced | Sin condición guardada | No | No | No |
| cdf3fe160e70a0bcb0aa | Visual | ac291ea509382034e4ab · Dashboard_Renting | 3481c97f911715717734 · Unidades facturadas por empresa de Renting y trimestre | Entregas Totales[Q3] | Advanced | Sin condición guardada | No | No | No |
| 06474567469a713bd291 | Visual | ac291ea509382034e4ab · Dashboard_Renting | 3481c97f911715717734 · Unidades facturadas por empresa de Renting y trimestre | Entregas Totales[Q4] | Advanced | Sin condición guardada | No | No | No |
| 8a85af10ea0798e11080 | Visual | ac291ea509382034e4ab · Dashboard_Renting | 3481c97f911715717734 · Unidades facturadas por empresa de Renting y trimestre | Entregas Totales[cantidad de maquinas] | Advanced | Sin condición guardada | No | No | No |
| 1d6cc7c3da1e10b47b19 | Visual | ac291ea509382034e4ab · Dashboard_Renting | 3481c97f911715717734 · Unidades facturadas por empresa de Renting y trimestre | Entregas Totales[Crecimiento Q1→Q4] | Advanced | Sin condición guardada | No | No | No |
| 62394049577f7b240bc6 | Visual | ac291ea509382034e4ab · Dashboard_Renting | 44e4621d600343c70058 · Matriculas por modelo | RUNT[MODELO] | TopN | TopN 10 | No | No | No |
| b32d4a00c1cf0776efd0 | Visual | ac291ea509382034e4ab · Dashboard_Renting | 44e4621d600343c70058 · Matriculas por modelo | RUNT[CTD] | Advanced | Sin condición guardada | No | No | No |
| e41d2082933850a0ed80 | Visual | ac291ea509382034e4ab · Dashboard_Renting | 7372de39e4387230a26c · Mecanizacion por departamento | Cultivos[municipios mecanizables] | Categorical | NOT IN (null) | No | No | true |
| 0dd984ebf688fa84ebbd | Visual | ac291ea509382034e4ab · Dashboard_Renting | 9c9f9e7740ae80a69e13 · Participación por cultivo área sembrada has (TOP 5) | Cultivos[val] | Advanced | Sin condición guardada | No | No | No |
| dbd31fbbc24a312b54ad | Visual | ac291ea509382034e4ab · Dashboard_Renting | 9c9f9e7740ae80a69e13 · Participación por cultivo área sembrada has (TOP 5) | Cultivos[Área sembrada (ha)] | Advanced | Sin condición guardada | No | No | No |
| 0934c9ddd0f02f56fd71 | Visual | ac291ea509382034e4ab · Dashboard_Renting | 9c9f9e7740ae80a69e13 · Participación por cultivo área sembrada has (TOP 5) | Cultivos[Desagregación cultivo] | TopN | TopN 5 | No | No | No |
| 1c9f3cb585427a3b47a2 | Visual | ac291ea509382034e4ab · Dashboard_Renting | f95237a70a2b397ab6c0 · Participación por mecanización | Cultivos[municipios mecanizables] | Categorical | NOT IN (null) | No | No | true |
| d41622559cc142bcc680 | Página | b597e26007760b8239c0 · Dashboard_Convenios | — | Entregas Totales[Cantidad] | Categorical | Sin condición guardada | No | No | No |
| 9735a5b6184a47d3e9cd | Página | b597e26007760b8239c0 · Dashboard_Convenios | — | Entregas Totales[procedencia] | Categorical | IN (Convenios) | No | No | No |
| fe62f9fc0877e0ca25c0 | Página | b597e26007760b8239c0 · Dashboard_Convenios | — | Entregas Totales[procedenciadetalle] | Categorical | NOT IN (null) | No | No | true |
| 62394049577f7b240bc6 | Visual | b597e26007760b8239c0 · Dashboard_Convenios | 164619eb8a032ec27532 · Matriculas por modelo | RUNT[MODELO] | TopN | TopN 10 | No | No | No |
| b32d4a00c1cf0776efd0 | Visual | b597e26007760b8239c0 · Dashboard_Convenios | 164619eb8a032ec27532 · Matriculas por modelo | RUNT[CTD] | Advanced | Sin condición guardada | No | No | No |
| 734463603b4417d425e4 | Visual | b597e26007760b8239c0 · Dashboard_Convenios | 3627bccc9714708ee3dd · Matriculas por marca | RUNT[MARCA] | TopN | TopN 10 | No | No | No |
| e41d2082933850a0ed80 | Visual | b597e26007760b8239c0 · Dashboard_Convenios | 7d4ca467440bb30d6806 · Mecanizacion por departamento | Cultivos[municipios mecanizables] | Categorical | NOT IN (null) | No | No | true |
| 0dd984ebf688fa84ebbd | Visual | b597e26007760b8239c0 · Dashboard_Convenios | b754c1660bd8235ebd7d · Participación por cultivo área sembrada has (TOP 5) | Cultivos[val] | Advanced | Sin condición guardada | No | No | No |
| dbd31fbbc24a312b54ad | Visual | b597e26007760b8239c0 · Dashboard_Convenios | b754c1660bd8235ebd7d · Participación por cultivo área sembrada has (TOP 5) | Cultivos[Área sembrada (ha)] | Advanced | Sin condición guardada | No | No | No |
| 0934c9ddd0f02f56fd71 | Visual | b597e26007760b8239c0 · Dashboard_Convenios | b754c1660bd8235ebd7d · Participación por cultivo área sembrada has (TOP 5) | Cultivos[Desagregación cultivo] | TopN | TopN 5 | No | No | No |
| c45052fd23be11e1c569 | Visual | b597e26007760b8239c0 · Dashboard_Convenios | d1c4d3f2924268689638 · Mecanización por regional | Cultivos[Regional] | Categorical | NOT IN (null) | No | No | true |
| e292f9044059e209a094 | Visual | b597e26007760b8239c0 · Dashboard_Convenios | d1c4d3f2924268689638 · Mecanización por regional | Cultivos[municipios mecanizables] | Categorical | NOT IN (null) | No | No | true |
| 59a022566ac1e0101d8b | Visual | b597e26007760b8239c0 · Dashboard_Convenios | eea7905600e9569dd64e · Participación por convenio y tasa de recambio | Entregas Totales[cantidad de maquinas] | Advanced | Sin condición guardada | No | No | No |
| d45cb94c85e3ceb30990 | Visual | b597e26007760b8239c0 · Dashboard_Convenios | eea7905600e9569dd64e · Participación por convenio y tasa de recambio | Entregas Totales[procedenciadetalle] | Categorical | Sin condición guardada | No | No | No |
| b7ecc5053a920d805093 | Visual | b597e26007760b8239c0 · Dashboard_Convenios | eea7905600e9569dd64e · Participación por convenio y tasa de recambio | Entregas Totales[Recambio anual (vs año ant.)] | Advanced | Sin condición guardada | No | No | No |
| 849edb3a20c599d7080c | Visual | b597e26007760b8239c0 · Dashboard_Convenios | eea7905600e9569dd64e · Participación por convenio y tasa de recambio | Entregas Totales[Recambio semestral] | Advanced | Sin condición guardada | No | No | No |
| 8bfcca4e901c2c67096a | Visual | b597e26007760b8239c0 · Dashboard_Convenios | eea7905600e9569dd64e · Participación por convenio y tasa de recambio | Entregas Totales[S1] | Advanced | Sin condición guardada | No | No | No |
| 69fa4adbe89127028ae8 | Visual | b597e26007760b8239c0 · Dashboard_Convenios | eea7905600e9569dd64e · Participación por convenio y tasa de recambio | Entregas Totales[S2] | Advanced | Sin condición guardada | No | No | No |
| e3a727342100202650b8 | Visual | b597e26007760b8239c0 · Dashboard_Convenios | eea7905600e9569dd64e · Participación por convenio y tasa de recambio | Entregas Totales[cantidad de maquinas] | Advanced | Sin condición guardada | No | No | No |
| 27d4e0499d3a6d0a0808 | Visual | b597e26007760b8239c0 · Dashboard_Convenios | eea7905600e9569dd64e · Participación por convenio y tasa de recambio | Entregas Totales[Q1] | Advanced | Sin condición guardada | No | No | No |
| 1a325f58db0c08501037 | Visual | b597e26007760b8239c0 · Dashboard_Convenios | eea7905600e9569dd64e · Participación por convenio y tasa de recambio | Entregas Totales[Q2] | Advanced | Sin condición guardada | No | No | No |
| 76061fe1ed006dcb3e9e | Visual | b597e26007760b8239c0 · Dashboard_Convenios | eea7905600e9569dd64e · Participación por convenio y tasa de recambio | Entregas Totales[Q3] | Advanced | Sin condición guardada | No | No | No |
| cdb6cc810b2334080ad3 | Visual | b597e26007760b8239c0 · Dashboard_Convenios | eea7905600e9569dd64e · Participación por convenio y tasa de recambio | Entregas Totales[Q4] | Advanced | Sin condición guardada | No | No | No |
| 1c9f3cb585427a3b47a2 | Visual | b597e26007760b8239c0 · Dashboard_Convenios | fd63ac47e9e00c202bcd · Participación por mecanización | Cultivos[municipios mecanizables] | Categorical | NOT IN (null) | No | No | true |

## 11.2 Segmentaciones (20)

| visual_id | Segmentación | Página | Modo | Selección única | Grupo de sincronización |
|---|---|---|---|---|---|
| 4d5f0482cc10734db587 | Segmentación: Tecnología (Entregas Totales[combustible]) | 377df594a011ae294444 · Dashboard_Empresas | Dropdown | true | — |
| 531799925cdc0008407b | Segmentación: Año (Entregas Totales[año]) | 377df594a011ae294444 · Dashboard_Empresas | Dropdown | true | Año |
| 86c38682d276ded8a3ea | Segmentación: Trimestre (Entregas Totales[Q]) | 377df594a011ae294444 · Dashboard_Empresas | Dropdown | true | — |
| 970c1dc21e6ec9001edd | Segmentación: Entregas Totales[Gama] | 377df594a011ae294444 · Dashboard_Empresas | Dropdown | true | — |
| 9fe797a57a507ed03c40 | Segmentación: Entregas Totales[Marca] | 377df594a011ae294444 · Dashboard_Empresas | Dropdown | true | — |
| b2df3c91709631415d59 | Segmentación: Trimestre (Entregas Totales[Q]) | 377df594a011ae294444 · Dashboard_Empresas | Dropdown | true | Q |
| f78d86067470b0166e17 | Segmentación: Centro (Entregas Totales[Región]) | 377df594a011ae294444 · Dashboard_Empresas | Dropdown | true | — |
| 86925930b70b966b6025 | Segmentación: Entregas Totales[Gama] | ac291ea509382034e4ab · Dashboard_Renting | Dropdown | true | — |
| 8b1429e26c4c808079c8 | Segmentación: Entregas Totales[Centro] | ac291ea509382034e4ab · Dashboard_Renting | Dropdown | true | — |
| 943ad7553bad0a0283bb | Segmentación: Entregas Totales[Marca] | ac291ea509382034e4ab · Dashboard_Renting | Dropdown | true | — |
| b17bc88120b65a105648 | Segmentación: Trimestre (Entregas Totales[Q]) | ac291ea509382034e4ab · Dashboard_Renting | Dropdown | true | — |
| f190480c104bb03dd85d | Segmentación: Año (Entregas Totales[año]) | ac291ea509382034e4ab · Dashboard_Renting | Dropdown | true | Año |
| f1b741b023b29010d540 | Segmentación: Tecnología (Entregas Totales[combustible]) | ac291ea509382034e4ab · Dashboard_Renting | Dropdown | true | — |
| 0c7758c3cc20d57abc42 | Segmentación: Convenio (Entregas Totales[procedenciadetalle]) | b597e26007760b8239c0 · Dashboard_Convenios | Dropdown | true | — |
| 461e004b2d94001390d3 | Segmentación: Entregas Totales[Gama] | b597e26007760b8239c0 · Dashboard_Convenios | Dropdown | true | — |
| 516e2b982c4c10399c17 | Segmentación: Trimestre (Entregas Totales[Q]) | b597e26007760b8239c0 · Dashboard_Convenios | Dropdown | true | Q |
| 54b7ca7d26135b942cd9 | Segmentación: Entregas Totales[Centro] | b597e26007760b8239c0 · Dashboard_Convenios | Dropdown | true | — |
| bdbd9cf43aebce83d659 | Segmentación: Entregas Totales[Marca] | b597e26007760b8239c0 · Dashboard_Convenios | Dropdown | true | — |
| c5aed3df5c828c0e0f50 | Segmentación: Año (Entregas Totales[año]) | b597e26007760b8239c0 · Dashboard_Convenios | Dropdown | true | Año |
| d94300db464811900cc6 | Segmentación: Combustible (Entregas Totales[combustible]) | b597e26007760b8239c0 · Dashboard_Convenios | Dropdown | true | — |

## 11.3 Interacciones (21)

Evidencia: `visualInteractions` de cada `page.json`.

| Página | Visual origen | Visual destino | Tipo |
|---|---|---|---|
| 377df594a011ae294444 · Dashboard_Empresas | 531799925cdc0008407b · Segmentación: Año (Entregas Totales[año]) | b43695b0ad1280b26827 · Participación por cultivo área sembrada has (TOP 5) | DataFilter |
| 377df594a011ae294444 · Dashboard_Empresas | 531799925cdc0008407b · Segmentación: Año (Entregas Totales[año]) | 1bef27578e3349425a36 · Forma sin título | NoFilter |
| 377df594a011ae294444 · Dashboard_Empresas | 531799925cdc0008407b · Segmentación: Año (Entregas Totales[año]) | 9f04b9ce6587b5610998 · Rendimiento (t/ha) | DataFilter |
| 377df594a011ae294444 · Dashboard_Empresas | 531799925cdc0008407b · Segmentación: Año (Entregas Totales[año]) | 86f85bbed000b2922793 · Producción (T) | DataFilter |
| 377df594a011ae294444 · Dashboard_Empresas | 9fe797a57a507ed03c40 · Segmentación: Entregas Totales[Marca] | 742a219cd1940a983530 · Importaciones | NoFilter |
| 377df594a011ae294444 · Dashboard_Empresas | 9fe797a57a507ed03c40 · Segmentación: Entregas Totales[Marca] | aff3f4a45ab91a74047e · Importaciones (CIF) | NoFilter |
| 377df594a011ae294444 · Dashboard_Empresas | 9fe797a57a507ed03c40 · Segmentación: Entregas Totales[Marca] | 81cdeccbcb7940787603 · Especificación Importadores | NoFilter |
| ac291ea509382034e4ab · Dashboard_Renting | f190480c104bb03dd85d · Segmentación: Año (Entregas Totales[año]) | 9c9f9e7740ae80a69e13 · Participación por cultivo área sembrada has (TOP 5) | DataFilter |
| ac291ea509382034e4ab · Dashboard_Renting | f190480c104bb03dd85d · Segmentación: Año (Entregas Totales[año]) | c71b214a210160202d5d · Forma sin título | NoFilter |
| ac291ea509382034e4ab · Dashboard_Renting | f190480c104bb03dd85d · Segmentación: Año (Entregas Totales[año]) | 1a394380135072c054c8 · Rendimiento (t/ha) | DataFilter |
| ac291ea509382034e4ab · Dashboard_Renting | f190480c104bb03dd85d · Segmentación: Año (Entregas Totales[año]) | 647df1e1caca5a76abc8 · Producción (T) | DataFilter |
| ac291ea509382034e4ab · Dashboard_Renting | 943ad7553bad0a0283bb · Segmentación: Entregas Totales[Marca] | 8106d7c0e70d14e3cc6e · Importaciones | NoFilter |
| ac291ea509382034e4ab · Dashboard_Renting | 943ad7553bad0a0283bb · Segmentación: Entregas Totales[Marca] | 710b4bdd807785877d66 · Importaciones (CIF) | NoFilter |
| ac291ea509382034e4ab · Dashboard_Renting | 943ad7553bad0a0283bb · Segmentación: Entregas Totales[Marca] | 4a086741483d06edbbe1 · Especificación Importadores | NoFilter |
| b597e26007760b8239c0 · Dashboard_Convenios | c5aed3df5c828c0e0f50 · Segmentación: Año (Entregas Totales[año]) | b754c1660bd8235ebd7d · Participación por cultivo área sembrada has (TOP 5) | DataFilter |
| b597e26007760b8239c0 · Dashboard_Convenios | c5aed3df5c828c0e0f50 · Segmentación: Año (Entregas Totales[año]) | 98932c329244ca1c0423 · Forma sin título | NoFilter |
| b597e26007760b8239c0 · Dashboard_Convenios | c5aed3df5c828c0e0f50 · Segmentación: Año (Entregas Totales[año]) | 6e4fc275427d71c147c7 · Rendimiento (t/ha) | DataFilter |
| b597e26007760b8239c0 · Dashboard_Convenios | c5aed3df5c828c0e0f50 · Segmentación: Año (Entregas Totales[año]) | 6dd1451dbdca03ca528e · Producción (T) | DataFilter |
| b597e26007760b8239c0 · Dashboard_Convenios | bdbd9cf43aebce83d659 · Segmentación: Entregas Totales[Marca] | 1e6271e61744ac760b0a · Importaciones | NoFilter |
| b597e26007760b8239c0 · Dashboard_Convenios | bdbd9cf43aebce83d659 · Segmentación: Entregas Totales[Marca] | ed7dcba836dbc5a82b07 · Importaciones (CIF) | NoFilter |
| b597e26007760b8239c0 · Dashboard_Convenios | bdbd9cf43aebce83d659 · Segmentación: Entregas Totales[Marca] | d63f39364345bc22e6ea · Especificación Importadores | NoFilter |

# 12. Bookmarks, botones y navegación

Evidencia: `GC - Flotillas.Report/definition/bookmarks/<bookmark_id>.bookmark.json`.

## 12.1 Bookmarks (24)

Opciones comunes a la mayoría de los bookmarks: `applyOnlyToTargetVisuals=True, suppressData=True`. Solo se indican en la tabla las que difieren.

«Targets» son los visuales a los que se aplica el bookmark (`targetVisualNames`). Un target puede **existir** en el PBIP y aun así **no funcionar** (referencia rota de datos). El estado del bookmark considera ambas cosas.

| bookmark_id | Nombre | Página | Opciones distintas | Targets: total / existen / funcionan | Invocado por | Estado de uso | Motivo |
|---|---|---|---|---|---|---|---|
| 0340d676b7e24e06b31d | Grafica imp | 6acb58945104d5318733 · no existe en el PBIP | — | 4 / 0 / 0 | — | Referencia rota | La página del bookmark no existe |
| 056202b7179ab3579a5d | Mecanización regional | b597e26007760b8239c0 · Dashboard_Convenios | — | 4 / 3 / 0 | — | Referencia rota | Todos sus targets están rotos o no existen |
| 0e8fa233336b7005c554 | Resumen matriculas | 6acb58945104d5318733 · no existe en el PBIP | — | 4 / 0 / 0 | — | Referencia rota | La página del bookmark no existe |
| 1432afe915c833a1d898 | Sembrado | b597e26007760b8239c0 · Dashboard_Convenios | — | 2 / 1 / 0 | — | Referencia rota | Todos sus targets están rotos o no existen |
| 149b0ada0237e9634a0e | Rendimiento periodo | b597e26007760b8239c0 · Dashboard_Convenios | — | 4 / 2 / 0 | — | Referencia rota | Todos sus targets están rotos o no existen |
| 179c088255033bc80d1e | Mecanización dep | b597e26007760b8239c0 · Dashboard_Convenios | — | 4 / 3 / 0 | — | Referencia rota | Todos sus targets están rotos o no existen |
| 2956125ff44a3e8bed0b | Rendimiento | b597e26007760b8239c0 · Dashboard_Convenios | — | 3 / 2 / 0 | ab3e643b10d65600d211 · Conectividad | Referencia rota | Todos sus targets están rotos o no existen |
| 32318b42c9d3954d5e19 | Participacion | 6acb58945104d5318733 · no existe en el PBIP | — | 4 / 0 / 0 | — | Referencia rota | La página del bookmark no existe |
| 598a9e8ed007000d0750 | Intencion | 7adad99113991d0e3e3e · no existe en el PBIP | — | 10 / 0 / 0 | — | Referencia rota | La página del bookmark no existe |
| 6a7dad0d996da4853d64 | Regional | 7adad99113991d0e3e3e · no existe en el PBIP | — | 10 / 0 / 0 | — | Referencia rota | La página del bookmark no existe |
| 7052bcd3da2e11b02291 | Tipo de cliente | 7adad99113991d0e3e3e · no existe en el PBIP | — | 10 / 0 / 0 | — | Referencia rota | La página del bookmark no existe |
| 73126f0c2c300ec3c0d6 | Marca | 6acb58945104d5318733 · no existe en el PBIP | — | 4 / 0 / 0 | — | Referencia rota | La página del bookmark no existe |
| 99730fcf006ee5428731 | Produccion | b597e26007760b8239c0 · Dashboard_Convenios | — | 3 / 2 / 0 | — | Referencia rota | Todos sus targets están rotos o no existen |
| 9ab9f550c06d5e43709b | Importadores | 6acb58945104d5318733 · no existe en el PBIP | — | 4 / 0 / 0 | — | Referencia rota | La página del bookmark no existe |
| aa98c6807620b2365ea7 | CIF | 6acb58945104d5318733 · no existe en el PBIP | — | 4 / 0 / 0 | — | Referencia rota | La página del bookmark no existe |
| c2e908097e6ad07bc67a | Cultivo | 7adad99113991d0e3e3e · no existe en el PBIP | — | 4 / 0 / 0 | — | Referencia rota | La página del bookmark no existe |
| c6c5e695dd35e1557b51 | Participación | b597e26007760b8239c0 · Dashboard_Convenios | — | 4 / 3 / 0 | — | Referencia rota | Todos sus targets están rotos o no existen |
| c75c33bbd31e25d2730d | Area C+S | b597e26007760b8239c0 · Dashboard_Convenios | — | 3 / 2 / 0 | — | Referencia rota | Todos sus targets están rotos o no existen |
| d2df5f2304dd79671498 | Resumen | b597e26007760b8239c0 · Dashboard_Convenios | — | 4 / 3 / 0 | — | Referencia rota | Todos sus targets están rotos o no existen |
| d66c5cc860884db34063 | Modelo | 6acb58945104d5318733 · no existe en el PBIP | — | 4 / 0 / 0 | — | Referencia rota | La página del bookmark no existe |
| d9c095c65d1a6600d67b | Capacidad | 6acb58945104d5318733 · no existe en el PBIP | — | 4 / 0 / 0 | — | Referencia rota | La página del bookmark no existe |
| de6e833a9e73fa72fe5a | Departamento | 7adad99113991d0e3e3e · no existe en el PBIP | — | 10 / 0 / 0 | — | Referencia rota | La página del bookmark no existe |
| f769f2b49e137d3a2026 | Cosechado | b597e26007760b8239c0 · Dashboard_Convenios | — | 2 / 1 / 0 | — | Referencia rota | Todos sus targets están rotos o no existen |
| fc32d496129c0a4cf7cf | Maquina | 7adad99113991d0e3e3e · no existe en el PBIP | — | 4 / 0 / 0 | — | Referencia rota | La página del bookmark no existe |

## 12.2 Detalle de cada bookmark

Una fila por bookmark y efecto. «Se aplica» = lo que realmente pasa al activar el bookmark. «Guardado sin efecto» = estados que Power BI guardó al crear el bookmark (foto de toda la página) pero que no se aplican porque el bookmark solo actúa sobre sus targets (`applyOnlyToTargetVisuals`). Cada visual se lista como `visual_id · nombre · funciona/roto`.

| bookmark_id | Bookmark | Página | Efecto | Cantidad | Visuales (visual_id · nombre · estado) |
|---|---|---|---|---:|---|
| 0340d676b7e24e06b31d | Grafica imp | 6acb58945104d5318733 · no existe en el PBIP | Target inexistente | 4 | 9b4b97db823a26683090 · no existe en el PBIP; 56200e56200816806097 · no existe en el PBIP; 8aaf6970db4d56025203 · no existe en el PBIP; 9401d28e9694cbb061a9 · no existe en el PBIP |
| 056202b7179ab3579a5d | Mecanización regional | b597e26007760b8239c0 · Dashboard_Convenios | Se aplica: muestra | 1 | d1c4d3f2924268689638 · Mecanización por regional · roto |
| 056202b7179ab3579a5d | Mecanización regional | b597e26007760b8239c0 · Dashboard_Convenios | Se aplica: oculta | 2 | 7d4ca467440bb30d6806 · Mecanizacion por departamento · roto; fd63ac47e9e00c202bcd · Participación por mecanización · roto |
| 056202b7179ab3579a5d | Mecanización regional | b597e26007760b8239c0 · Dashboard_Convenios | Target inexistente | 1 | b37ca9e18140a4608e4d · no existe en el PBIP |
| 056202b7179ab3579a5d | Mecanización regional | b597e26007760b8239c0 · Dashboard_Convenios | Guardado sin efecto | 16 | Detalle por visual en 12.3 |
| 0e8fa233336b7005c554 | Resumen matriculas | 6acb58945104d5318733 · no existe en el PBIP | Target inexistente | 4 | bb66da96d1500bc05b35 · no existe en el PBIP; 728a535d748782ba0e11 · no existe en el PBIP; e3f3b8db9cecbd4d2696 · no existe en el PBIP; 5c66afadc51798034036 · no existe en el PBIP |
| 1432afe915c833a1d898 | Sembrado | b597e26007760b8239c0 · Dashboard_Convenios | Se aplica: muestra | 1 | b754c1660bd8235ebd7d · Participación por cultivo área sembrada has (TOP 5) · roto |
| 1432afe915c833a1d898 | Sembrado | b597e26007760b8239c0 · Dashboard_Convenios | Target inexistente | 1 | 617c29c73140265f44c4 · no existe en el PBIP |
| 1432afe915c833a1d898 | Sembrado | b597e26007760b8239c0 · Dashboard_Convenios | Guardado sin efecto | 15 | Detalle por visual en 12.3 |
| 149b0ada0237e9634a0e | Rendimiento periodo | b597e26007760b8239c0 · Dashboard_Convenios | Se aplica: oculta | 2 | 6e4fc275427d71c147c7 · Rendimiento (t/ha) · roto; 6dd1451dbdca03ca528e · Producción (T) · roto |
| 149b0ada0237e9634a0e | Rendimiento periodo | b597e26007760b8239c0 · Dashboard_Convenios | Target inexistente | 2 | 352167a790462613a7e1 · no existe en el PBIP; a3d2756f99c5055f4d4d · no existe en el PBIP |
| 149b0ada0237e9634a0e | Rendimiento periodo | b597e26007760b8239c0 · Dashboard_Convenios | Guardado sin efecto | 20 | Detalle por visual en 12.3 |
| 179c088255033bc80d1e | Mecanización dep | b597e26007760b8239c0 · Dashboard_Convenios | Se aplica: muestra | 1 | 7d4ca467440bb30d6806 · Mecanizacion por departamento · roto |
| 179c088255033bc80d1e | Mecanización dep | b597e26007760b8239c0 · Dashboard_Convenios | Se aplica: oculta | 2 | d1c4d3f2924268689638 · Mecanización por regional · roto; fd63ac47e9e00c202bcd · Participación por mecanización · roto |
| 179c088255033bc80d1e | Mecanización dep | b597e26007760b8239c0 · Dashboard_Convenios | Target inexistente | 1 | b37ca9e18140a4608e4d · no existe en el PBIP |
| 179c088255033bc80d1e | Mecanización dep | b597e26007760b8239c0 · Dashboard_Convenios | Guardado sin efecto | 16 | Detalle por visual en 12.3 |
| 2956125ff44a3e8bed0b | Rendimiento | b597e26007760b8239c0 · Dashboard_Convenios | Se aplica: muestra | 1 | 6e4fc275427d71c147c7 · Rendimiento (t/ha) · roto |
| 2956125ff44a3e8bed0b | Rendimiento | b597e26007760b8239c0 · Dashboard_Convenios | Se aplica: oculta | 1 | 6dd1451dbdca03ca528e · Producción (T) · roto |
| 2956125ff44a3e8bed0b | Rendimiento | b597e26007760b8239c0 · Dashboard_Convenios | Target inexistente | 1 | 352167a790462613a7e1 · no existe en el PBIP |
| 2956125ff44a3e8bed0b | Rendimiento | b597e26007760b8239c0 · Dashboard_Convenios | Guardado sin efecto | 14 | Detalle por visual en 12.3 |
| 32318b42c9d3954d5e19 | Participacion | 6acb58945104d5318733 · no existe en el PBIP | Target inexistente | 4 | 8aaf6970db4d56025203 · no existe en el PBIP; 9401d28e9694cbb061a9 · no existe en el PBIP; 9b4b97db823a26683090 · no existe en el PBIP; 56200e56200816806097 · no existe en el PBIP |
| 598a9e8ed007000d0750 | Intencion | 7adad99113991d0e3e3e · no existe en el PBIP | Target inexistente | 10 | 7afdee63638301e049a0 · no existe en el PBIP; 08bd4e37d62819441e76 · no existe en el PBIP; 23476a9fe01e04d27034 · no existe en el PBIP; b36bbb9191b3992d02ab · no existe en el PBIP; e668f567460e38d091a3 · no existe en el PBIP; 06b0e5efd0895764d000 · no existe en el PBIP; caa505871e2e13b08507 · no existe en el PBIP; 40ebde3d2e2a318955d6 · no existe en el PBIP; f6877ec8da2a493a0b51 · no existe en el PBIP; f3d58265a33001938d52 · no existe en el PBIP |
| 6a7dad0d996da4853d64 | Regional | 7adad99113991d0e3e3e · no existe en el PBIP | Target inexistente | 10 | f3d58265a33001938d52 · no existe en el PBIP; 7afdee63638301e049a0 · no existe en el PBIP; 08bd4e37d62819441e76 · no existe en el PBIP; 23476a9fe01e04d27034 · no existe en el PBIP; b36bbb9191b3992d02ab · no existe en el PBIP; e668f567460e38d091a3 · no existe en el PBIP; 06b0e5efd0895764d000 · no existe en el PBIP; caa505871e2e13b08507 · no existe en el PBIP; 40ebde3d2e2a318955d6 · no existe en el PBIP; f6877ec8da2a493a0b51 · no existe en el PBIP |
| 7052bcd3da2e11b02291 | Tipo de cliente | 7adad99113991d0e3e3e · no existe en el PBIP | Target inexistente | 10 | 7afdee63638301e049a0 · no existe en el PBIP; 08bd4e37d62819441e76 · no existe en el PBIP; 23476a9fe01e04d27034 · no existe en el PBIP; b36bbb9191b3992d02ab · no existe en el PBIP; e668f567460e38d091a3 · no existe en el PBIP; 06b0e5efd0895764d000 · no existe en el PBIP; caa505871e2e13b08507 · no existe en el PBIP; 40ebde3d2e2a318955d6 · no existe en el PBIP; f6877ec8da2a493a0b51 · no existe en el PBIP; f3d58265a33001938d52 · no existe en el PBIP |
| 73126f0c2c300ec3c0d6 | Marca | 6acb58945104d5318733 · no existe en el PBIP | Target inexistente | 4 | bb66da96d1500bc05b35 · no existe en el PBIP; 728a535d748782ba0e11 · no existe en el PBIP; e3f3b8db9cecbd4d2696 · no existe en el PBIP; 5c66afadc51798034036 · no existe en el PBIP |
| 99730fcf006ee5428731 | Produccion | b597e26007760b8239c0 · Dashboard_Convenios | Se aplica: muestra | 1 | 6dd1451dbdca03ca528e · Producción (T) · roto |
| 99730fcf006ee5428731 | Produccion | b597e26007760b8239c0 · Dashboard_Convenios | Se aplica: oculta | 1 | 6e4fc275427d71c147c7 · Rendimiento (t/ha) · roto |
| 99730fcf006ee5428731 | Produccion | b597e26007760b8239c0 · Dashboard_Convenios | Target inexistente | 1 | 352167a790462613a7e1 · no existe en el PBIP |
| 99730fcf006ee5428731 | Produccion | b597e26007760b8239c0 · Dashboard_Convenios | Guardado sin efecto | 14 | Detalle por visual en 12.3 |
| 9ab9f550c06d5e43709b | Importadores | 6acb58945104d5318733 · no existe en el PBIP | Target inexistente | 4 | 9401d28e9694cbb061a9 · no existe en el PBIP; 9b4b97db823a26683090 · no existe en el PBIP; 56200e56200816806097 · no existe en el PBIP; 8aaf6970db4d56025203 · no existe en el PBIP |
| aa98c6807620b2365ea7 | CIF | 6acb58945104d5318733 · no existe en el PBIP | Target inexistente | 4 | 56200e56200816806097 · no existe en el PBIP; 8aaf6970db4d56025203 · no existe en el PBIP; 9401d28e9694cbb061a9 · no existe en el PBIP; 9b4b97db823a26683090 · no existe en el PBIP |
| c2e908097e6ad07bc67a | Cultivo | 7adad99113991d0e3e3e · no existe en el PBIP | Target inexistente | 4 | 1f7332b38db3e773d2a7 · no existe en el PBIP; 9b3570d21abeff1b051f · no existe en el PBIP; 9f76ae3b14f296f58953 · no existe en el PBIP; d6a224435004d4826108 · no existe en el PBIP |
| c6c5e695dd35e1557b51 | Participación | b597e26007760b8239c0 · Dashboard_Convenios | Se aplica: muestra | 1 | fd63ac47e9e00c202bcd · Participación por mecanización · roto |
| c6c5e695dd35e1557b51 | Participación | b597e26007760b8239c0 · Dashboard_Convenios | Se aplica: oculta | 2 | 7d4ca467440bb30d6806 · Mecanizacion por departamento · roto; d1c4d3f2924268689638 · Mecanización por regional · roto |
| c6c5e695dd35e1557b51 | Participación | b597e26007760b8239c0 · Dashboard_Convenios | Target inexistente | 1 | b37ca9e18140a4608e4d · no existe en el PBIP |
| c6c5e695dd35e1557b51 | Participación | b597e26007760b8239c0 · Dashboard_Convenios | Guardado sin efecto | 16 | Detalle por visual en 12.3 |
| c75c33bbd31e25d2730d | Area C+S | b597e26007760b8239c0 · Dashboard_Convenios | Se aplica: oculta | 2 | 6dd1451dbdca03ca528e · Producción (T) · roto; 6e4fc275427d71c147c7 · Rendimiento (t/ha) · roto |
| c75c33bbd31e25d2730d | Area C+S | b597e26007760b8239c0 · Dashboard_Convenios | Target inexistente | 1 | 352167a790462613a7e1 · no existe en el PBIP |
| c75c33bbd31e25d2730d | Area C+S | b597e26007760b8239c0 · Dashboard_Convenios | Guardado sin efecto | 14 | Detalle por visual en 12.3 |
| d2df5f2304dd79671498 | Resumen | b597e26007760b8239c0 · Dashboard_Convenios | Se aplica: oculta | 3 | fd63ac47e9e00c202bcd · Participación por mecanización · roto; 7d4ca467440bb30d6806 · Mecanizacion por departamento · roto; d1c4d3f2924268689638 · Mecanización por regional · roto |
| d2df5f2304dd79671498 | Resumen | b597e26007760b8239c0 · Dashboard_Convenios | Target inexistente | 1 | fbf8d821279a102ee94a · no existe en el PBIP |
| d2df5f2304dd79671498 | Resumen | b597e26007760b8239c0 · Dashboard_Convenios | Guardado sin efecto | 16 | Detalle por visual en 12.3 |
| d66c5cc860884db34063 | Modelo | 6acb58945104d5318733 · no existe en el PBIP | Target inexistente | 4 | bb66da96d1500bc05b35 · no existe en el PBIP; 728a535d748782ba0e11 · no existe en el PBIP; e3f3b8db9cecbd4d2696 · no existe en el PBIP; 5c66afadc51798034036 · no existe en el PBIP |
| d9c095c65d1a6600d67b | Capacidad | 6acb58945104d5318733 · no existe en el PBIP | Target inexistente | 4 | bb66da96d1500bc05b35 · no existe en el PBIP; 728a535d748782ba0e11 · no existe en el PBIP; 5c66afadc51798034036 · no existe en el PBIP; e3f3b8db9cecbd4d2696 · no existe en el PBIP |
| de6e833a9e73fa72fe5a | Departamento | 7adad99113991d0e3e3e · no existe en el PBIP | Target inexistente | 10 | f3d58265a33001938d52 · no existe en el PBIP; 7afdee63638301e049a0 · no existe en el PBIP; 08bd4e37d62819441e76 · no existe en el PBIP; 23476a9fe01e04d27034 · no existe en el PBIP; b36bbb9191b3992d02ab · no existe en el PBIP; e668f567460e38d091a3 · no existe en el PBIP; 06b0e5efd0895764d000 · no existe en el PBIP; caa505871e2e13b08507 · no existe en el PBIP; 40ebde3d2e2a318955d6 · no existe en el PBIP; f6877ec8da2a493a0b51 · no existe en el PBIP |
| f769f2b49e137d3a2026 | Cosechado | b597e26007760b8239c0 · Dashboard_Convenios | Se aplica: oculta | 1 | b754c1660bd8235ebd7d · Participación por cultivo área sembrada has (TOP 5) · roto |
| f769f2b49e137d3a2026 | Cosechado | b597e26007760b8239c0 · Dashboard_Convenios | Target inexistente | 1 | 617c29c73140265f44c4 · no existe en el PBIP |
| f769f2b49e137d3a2026 | Cosechado | b597e26007760b8239c0 · Dashboard_Convenios | Guardado sin efecto | 15 | Detalle por visual en 12.3 |
| fc32d496129c0a4cf7cf | Maquina | 7adad99113991d0e3e3e · no existe en el PBIP | Target inexistente | 4 | 9f76ae3b14f296f58953 · no existe en el PBIP; d6a224435004d4826108 · no existe en el PBIP; 9b3570d21abeff1b051f · no existe en el PBIP; 1f7332b38db3e773d2a7 · no existe en el PBIP |

## 12.3 Estados guardados sin efecto

Matriz por página: una fila por visual y una columna por bookmark. `O` = guardado oculto, `V` = guardado visible, `·` = sin estado guardado en ese bookmark. Son estados que Power BI guardó en la foto de la página pero que no se aplican porque el bookmark solo actúa sobre sus targets (12.2). Se mapean para que un cambio futuro sobre el bookmark (por ejemplo, quitar `applyOnlyToTargetVisuals`) conozca su efecto.

### b597e26007760b8239c0 · Dashboard_Convenios

Columnas: **B1** = 056202b7179ab3579a5d · Mecanización regional; **B2** = 1432afe915c833a1d898 · Sembrado; **B3** = 149b0ada0237e9634a0e · Rendimiento periodo; **B4** = 179c088255033bc80d1e · Mecanización dep; **B5** = 2956125ff44a3e8bed0b · Rendimiento; **B6** = 99730fcf006ee5428731 · Produccion; **B7** = c6c5e695dd35e1557b51 · Participación; **B8** = c75c33bbd31e25d2730d · Area C+S; **B9** = d2df5f2304dd79671498 · Resumen; **B10** = f769f2b49e137d3a2026 · Cosechado.

| Visual (visual_id · nombre · estado) | B1 | B2 | B3 | B4 | B5 | B6 | B7 | B8 | B9 | B10 |
|---|---|---|---|---|---|---|---|---|---|---|
| ac23df6f245ac18edcee · Convenios · funciona | V | V | V | V | V | V | V | V | V | V |
| 9a88093ab5402c6e7a10 · Convenios vigentes hoy · funciona | · | · | V | · | · | · | · | · | · | · |
| d63f39364345bc22e6ea · Especificación Importadores · roto | O | V | O | O | V | V | O | V | O | V |
| d556fd700091e6362812 · Forma sin título · funciona | V | V | V | V | V | V | V | V | V | V |
| 98932c329244ca1c0423 · Forma sin título · funciona | V | V | V | V | V | V | V | V | V | V |
| 3895cca635d3a5b0eaaa · Imagen: Logo-CasaToro4243506339860492.png · funciona | V | V | V | V | V | V | V | V | V | V |
| 1e6271e61744ac760b0a · Importaciones · roto | O | V | O | O | O | O | O | O | O | V |
| ed7dcba836dbc5a82b07 · Importaciones (CIF) · roto | O | V | O | O | V | V | O | V | O | V |
| 021d4850b3401880b984 · Matriculas Runt · roto | O | V | O | O | V | V | O | V | O | V |
| 3627bccc9714708ee3dd · Matriculas por marca · roto | O | V | O | O | V | V | O | V | O | V |
| 164619eb8a032ec27532 · Matriculas por modelo · roto | O | V | O | O | V | V | O | V | O | V |
| 7d4ca467440bb30d6806 · Mecanizacion por departamento · roto | · | · | O | · | · | · | · | · | · | · |
| d1c4d3f2924268689638 · Mecanización por regional · roto | · | · | O | · | · | · | · | · | · | · |
| b754c1660bd8235ebd7d · Participación por cultivo área sembrada has (TOP 5) · roto | V | · | O | V | O | O | V | O | V | · |
| fd63ac47e9e00c202bcd · Participación por mecanización · roto | · | · | O | · | · | · | · | · | · | · |
| 6dd1451dbdca03ca528e · Producción (T) · roto | O | O | · | O | · | · | O | · | O | O |
| 6e4fc275427d71c147c7 · Rendimiento (t/ha) · roto | O | V | · | O | · | · | O | · | O | V |
| c5aed3df5c828c0e0f50 · Segmentación: Año (Entregas Totales[año]) · funciona | V | V | V | V | V | V | V | V | V | V |
| 54b7ca7d26135b942cd9 · Segmentación: Entregas Totales[Centro] · funciona | · | · | V | · | · | · | · | · | · | · |
| 461e004b2d94001390d3 · Segmentación: Entregas Totales[Gama] · funciona | · | · | V | · | · | · | · | · | · | · |
| bdbd9cf43aebce83d659 · Segmentación: Entregas Totales[Marca] · funciona | V | V | V | V | V | V | V | V | V | V |
| 9769d8556306a6bbd114 · Última Actualización · funciona | V | V | V | V | V | V | V | V | V | V |

## 12.4 Botones y acciones

| Botón (visual_id · nombre) | Página | Acción | Destino | Bookmark asociado |
|---|---|---|---|---|
| ab3e643b10d65600d211 · Conectividad | 377df594a011ae294444 · Dashboard_Empresas | PageNavigation | 7fe28b006cd3b491a578 · no existe en el PBIP | 2956125ff44a3e8bed0b · Rendimiento |

## 12.5 Tooltips y drillthrough

No encontrado: ninguna página es de tipo Tooltip o Drillthrough.

El efecto real al activar cada bookmark o botón no se ve en los archivos; se declara en 17.1.

# 13. Recursos, tema y presentación

Sección de estética: archivos gráficos, dónde está ubicado cada elemento visual de diseño (banners, logos, formas, textos) y el tema.

## 13.1 Archivos de recursos (4)

Rutas relativas a la carpeta del BI (`C:/dev/MCP_POWERBI/01_bi/01_versiones/00_original/GC - Flotillas`).

| resource_id | Tipo | Ruta del archivo | Peso (bytes) | Tamaño original (px) | Usos | Estado de uso |
|---|---|---|---:|---|---:|---|
| CY24SU10 | BaseTheme | GC - Flotillas.Report/StaticResources/SharedResources/BaseThemes/CY24SU10.json | 14168 | — | 0 | Uso técnico |
| Logo-CasaToro4243506339860492.png | Image | GC - Flotillas.Report/StaticResources/RegisteredResources/Logo-CasaToro4243506339860492.png | 3529 | 160×62 | 3 | En uso |
| Logo-Nebula_(1)8124617426694213.png | Image | GC - Flotillas.Report/StaticResources/RegisteredResources/Logo-Nebula_(1)8124617426694213.png | 3487 | 320×71 | 3 | En uso |
| Tema_1_BI_Nebula2861464806860662.json | CustomTheme | GC - Flotillas.Report/StaticResources/RegisteredResources/Tema_1_BI_Nebula2861464806860662.json | 10050 | — | 0 | Uso técnico |

## 13.2 Ubicación de los elementos de diseño por página

Incluye todo lo que está dentro de un banner (también tarjetas y segmentaciones, porque forman parte de su composición) y, fuera del banner, las imágenes, formas, textos y botones. Un banner es una forma que ocupa al menos el 80 % del ancho de la página; pertenecen a él los elementos que quedan dentro de su franja vertical. Tamaño colocado frente al original indica la escala de cada imagen.

### Dashboard_Renting (`ac291ea509382034e4ab`)

| Zona | visual_id | Elemento | Rol en el diseño | x | y | Ancho | Alto | z | Oculto | Imagen (archivo · original → colocado) |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|
| Banner superior | c71b214a210160202d5d | Forma sin título | Fondo del banner | 0 | 0 | 1280 | 157 | 8000 | No | — |
| Banner superior | 6e17130e3d82a640b8c5 | Renting | Título / texto | 14 | 11 | 142 | 54 | 9000 | No | — |
| Banner superior | 9734d2820ecd3ae8a0a0 | Última Actualización | Contenido: Tarjeta | 172 | 17 | 207 | 51 | 12000 | No | — |
| Banner superior | 69b6e056895903ee070d | Forma sin título | Separador / forma | 150 | 22 | 15 | 42 | 11000 | No | — |
| Banner superior | b932373a0b2007733b39 | Imagen: Logo-CasaToro4243506339860492.png | Logo / imagen | 1138 | 23 | 112 | 38 | 10000 | No | Logo-CasaToro4243506339860492.png · 160×62 → 112×38 (70 %) · GC - Flotillas.Report/StaticResources/RegisteredResources/Logo-CasaToro4243506339860492.png |
| Banner superior | 5225a970b0de27434ed1 | Imagen: Logo-Nebula_(1)8124617426694213.png | Logo / imagen | 1028 | 27 | 121 | 29 | 22000 | No | Logo-Nebula_(1)8124617426694213.png · 320×71 → 121×29 (38 %) · GC - Flotillas.Report/StaticResources/RegisteredResources/Logo-Nebula_(1)8124617426694213.png |
| Banner superior | f190480c104bb03dd85d | Segmentación: Año (Entregas Totales[año]) | Contenido: Segmentación | 9 | 79 | 127 | 65 | 18000 | No | — |
| Banner superior | 86925930b70b966b6025 | Segmentación: Entregas Totales[Gama] | Contenido: Segmentación | 363 | 79 | 170 | 65 | 19000 | No | — |
| Banner superior | 8b1429e26c4c808079c8 | Segmentación: Entregas Totales[Centro] | Contenido: Segmentación | 536 | 79 | 163 | 65 | 21000 | No | — |
| Banner superior | f1b741b023b29010d540 | Segmentación: Tecnología (Entregas Totales[combustible]) | Contenido: Segmentación | 705 | 79 | 163 | 66 | 27000 | No | — |
| Banner superior | 943ad7553bad0a0283bb | Segmentación: Entregas Totales[Marca] | Contenido: Segmentación | 142 | 80 | 216 | 65 | 13000 | No | — |
| Banner superior | b17bc88120b65a105648 | Segmentación: Trimestre (Entregas Totales[Q]) | Contenido: Segmentación | 871 | 80 | 162 | 65 | 29000 | No | — |

### Dashboard_Convenios (`b597e26007760b8239c0`)

| Zona | visual_id | Elemento | Rol en el diseño | x | y | Ancho | Alto | z | Oculto | Imagen (archivo · original → colocado) |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|
| Banner superior | 98932c329244ca1c0423 | Forma sin título | Fondo del banner | 0 | 0 | 1280 | 157 | 8000 | No | — |
| Banner superior | ac23df6f245ac18edcee | Convenios | Título / texto | 14 | 11 | 178 | 54 | 9000 | No | — |
| Banner superior | 9769d8556306a6bbd114 | Última Actualización | Contenido: Tarjeta | 209 | 17 | 207 | 51 | 12000 | No | — |
| Banner superior | d556fd700091e6362812 | Forma sin título | Separador / forma | 187 | 22 | 15 | 42 | 11000 | No | — |
| Banner superior | 3895cca635d3a5b0eaaa | Imagen: Logo-CasaToro4243506339860492.png | Logo / imagen | 1138 | 23 | 112 | 38 | 10000 | No | Logo-CasaToro4243506339860492.png · 160×62 → 112×38 (70 %) · GC - Flotillas.Report/StaticResources/RegisteredResources/Logo-CasaToro4243506339860492.png |
| Banner superior | bb6805c59a193b8553d0 | Imagen: Logo-Nebula_(1)8124617426694213.png | Logo / imagen | 1028 | 27 | 121 | 29 | 22000 | No | Logo-Nebula_(1)8124617426694213.png · 320×71 → 121×29 (38 %) · GC - Flotillas.Report/StaticResources/RegisteredResources/Logo-Nebula_(1)8124617426694213.png |
| Banner superior | d94300db464811900cc6 | Segmentación: Combustible (Entregas Totales[combustible]) | Contenido: Segmentación | 637 | 79 | 163 | 66 | 26000 | No | — |
| Banner superior | c5aed3df5c828c0e0f50 | Segmentación: Año (Entregas Totales[año]) | Contenido: Segmentación | 3 | 80 | 127 | 65 | 18000 | No | — |
| Banner superior | bdbd9cf43aebce83d659 | Segmentación: Entregas Totales[Marca] | Contenido: Segmentación | 135 | 80 | 157 | 65 | 13000 | No | — |
| Banner superior | 461e004b2d94001390d3 | Segmentación: Entregas Totales[Gama] | Contenido: Segmentación | 295 | 80 | 170 | 65 | 19000 | No | — |
| Banner superior | 54b7ca7d26135b942cd9 | Segmentación: Entregas Totales[Centro] | Contenido: Segmentación | 469 | 80 | 163 | 65 | 21000 | No | — |
| Banner superior | 0c7758c3cc20d57abc42 | Segmentación: Convenio (Entregas Totales[procedenciadetalle]) | Contenido: Segmentación | 803 | 80 | 162 | 67 | 29000 | No | — |
| Banner superior | 516e2b982c4c10399c17 | Segmentación: Trimestre (Entregas Totales[Q]) | Contenido: Segmentación | 970 | 80 | 162 | 67 | 30000 | No | — |

### Dashboard_Empresas (`377df594a011ae294444`)

| Zona | visual_id | Elemento | Rol en el diseño | x | y | Ancho | Alto | z | Oculto | Imagen (archivo · original → colocado) |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|
| Banner superior | 1bef27578e3349425a36 | Forma sin título | Fondo del banner | 0 | 0 | 1280 | 157 | 8000 | No | — |
| Banner superior | f5ee68ca0ec050ca9ab2 | Empresas | Título / texto | 14 | 11 | 162 | 54 | 9000 | No | — |
| Banner superior | 207ac3eed23edebbbe0c | Última Actualización | Contenido: Tarjeta | 199 | 17 | 207 | 51 | 12000 | No | — |
| Banner superior | 71f234fbb753194aa2e1 | Forma sin título | Separador / forma | 177 | 22 | 15 | 42 | 11000 | No | — |
| Banner superior | a5ac6067ea2db9bdb8a7 | Imagen: Logo-CasaToro4243506339860492.png | Logo / imagen | 1138 | 23 | 112 | 38 | 10000 | No | Logo-CasaToro4243506339860492.png · 160×62 → 112×38 (70 %) · GC - Flotillas.Report/StaticResources/RegisteredResources/Logo-CasaToro4243506339860492.png |
| Banner superior | 7342d316766131600462 | Imagen: Logo-Nebula_(1)8124617426694213.png | Logo / imagen | 1028 | 27 | 121 | 29 | 23000 | No | Logo-Nebula_(1)8124617426694213.png · 320×71 → 121×29 (38 %) · GC - Flotillas.Report/StaticResources/RegisteredResources/Logo-Nebula_(1)8124617426694213.png |
| Banner superior | 531799925cdc0008407b | Segmentación: Año (Entregas Totales[año]) | Contenido: Segmentación | 3 | 80 | 127 | 65 | 18000 | No | — |
| Banner superior | 9fe797a57a507ed03c40 | Segmentación: Entregas Totales[Marca] | Contenido: Segmentación | 135 | 80 | 218 | 65 | 13000 | No | — |
| Banner superior | 970c1dc21e6ec9001edd | Segmentación: Entregas Totales[Gama] | Contenido: Segmentación | 358 | 80 | 170 | 65 | 20000 | No | — |
| Banner superior | 86c38682d276ded8a3ea | Segmentación: Trimestre (Entregas Totales[Q]) | Contenido: Segmentación | 533 | 80 | 170 | 65 | 30000 | No | — |
| Banner superior | f78d86067470b0166e17 | Segmentación: Centro (Entregas Totales[Región]) | Contenido: Segmentación | 708 | 80 | 162 | 65 | 22000 | No | — |
| Banner superior | 4d5f0482cc10734db587 | Segmentación: Tecnología (Entregas Totales[combustible]) | Contenido: Segmentación | 875 | 80 | 162 | 65 | 27000 | No | — |
| Banner superior | b2df3c91709631415d59 | Segmentación: Trimestre (Entregas Totales[Q]) | Contenido: Segmentación | 1042 | 80 | 162 | 65 | 31000 | No | — |
| Cuerpo de la página | ab3e643b10d65600d211 | Conectividad | Botón | 1170 | 212 | 100 | 28 | 19000 | No | — |

## 13.3 Tema

| Tema | Nombre | Archivo | dataColors | Fondo | Primer plano | Fuentes |
|---|---|---|---|---|---|---|
| base | CY24SU10 | SharedResources/BaseThemes/CY24SU10.json | #118DFF, #12239E, #E66C37, #6B007B, #E044A7, #744EC2, #D9B300, #D64550, #197278, #1AAB40, #15C6F4, #4092FF | #FFFFFF | #252423 | DIN, Segoe UI, Segoe UI Semibold |
| personalizado | Tema 1_BI_Nebula | RegisteredResources/Tema_1_BI_Nebula2861464806860662.json | #1A73E8, #8943A7, #AE0A33, #028AB0, #E06806, #1A73E8, #8943A7, #AE0A33, #3599B8, #DFBFBF, #4AC5BB, #5F6B6D | — | — | 'Segoe UI', wf_segoe-ui_normal, helvetica, arial, sans-serif |

## 13.4 Metadatos del proyecto

| Elemento | Valor |
|---|---|
| Archivo .pbip | GC - Flotillas.pbip |
| Modelo referenciado por el reporte | ../GC - Flotillas.SemanticModel |
| Versión PBIR | 4.0 |
| logicalId del reporte | 6b7b24a7-9281-4d32-aac8-d12eae8ce8b3 |
| logicalId del modelo | b8f3a499-7b45-40c3-b480-9da92145c76c |
| Página activa al abrir | ac291ea509382034e4ab · Dashboard_Renting |

# 14. Reglas de negocio

La implementación remite al objeto que la contiene; el código está en las secciones 4, 6.1 y 11. Los filtros sin condición guardada no son reglas (siguen inventariados en 11.1).

| rule_id | Regla | Implementación (dónde) | Interpretación funcional | Certeza | Validación del dueño | Respuesta del dueño |
|---|---|---|---|---|---|---|
| RN01 | Filtro de carga en Entregas Totales | Paso 8 «Filtro Cantidad» (4): Table.SelectRows(#"Tipo cambiado inicial", each ([Cantidad] = 1)) | Solo entran a la tabla de hechos las filas con `Cantidad = 1`, dejando una fila por unidad; fija la granularidad de entrega individual. | Encontrado (código M) | No requerida | — |
| RN02 | Filtro de carga en Entregas Totales | Paso 10 «Filas filtradas1» (4): Table.SelectRows(#"Poner En Mayúsculas Cada Palabra", each ([tipo] = "Nuevos")) | Solo se consideran entregas de tipo «Nuevos»; se excluye cualquier otro tipo (p. ej. usados) del tablero. | Encontrado (código M) | No requerida | — |
| RN03 | Columna calculada Linea | Entregas Totales[Linea] (6.1) | Asigna una línea (Wirtgen, JD Agricola, JD Construccion o Usados) según la marca, solo para centros cuyo código no empieza por «VO»; las demás filas quedan en blanco. Sin uso interno identificado: ningún visual, filtro ni medida la usa (17.2, n.º 1). Lógica exacta en 6.1. | Inferido (lógica leída en 6.1) | Pendiente de validación | — |
| RN04 | Columna calculada Región | Entregas Totales[Región] (6.1) | Asigna la región geográfica de cada entrega para los cortes regionales. Lógica exacta en 6.1. | Inferido (lógica leída en 6.1) | Pendiente de validación | — |
| RN05 | Columna calculada Q | Entregas Totales[Q] (6.1) | Deriva el trimestre de la entrega; alimenta la segmentación por trimestre. Lógica exacta en 6.1. | Inferido (lógica leída en 6.1) | Pendiente de validación | — |
| RN06 | Columna calculada DIVISION S | Entregas Totales[DIVISION S] (6.1) | Deriva el semestre de la entrega desde el mes de `FechaEntregaCliente`: S1 = enero a junio, S2 = julio a diciembre. Base de las medidas [S1] y [S2] y del visual 2706c287d7d0e875d946 · Unidades por convenio: S1 vs S2. Lógica exacta en 6.1. | Inferido (lógica leída en 6.1) | Pendiente de validación | — |
| RN07 | Columna calculada val nombre | Entregas Totales[val nombre] (6.1) | Homologa el nombre del cliente/entidad vía `LOOKUPVALUE` contra la dimensión Val nombres (sin relación física). Lógica exacta en 6.1 y sección 15. | Inferido (lógica leída en 6.1) | Pendiente de validación | — |
| RN08 | Columna calculada RENTING | Entregas Totales[RENTING] (6.1) | Marca «RENTING» las entregas cuyo tercero está homologado en Val nombres (el mismo criterio de `val nombre` distinto de «OTROS»); las demás quedan vacías. Sin uso interno identificado: la página Renting se separa con el filtro RN12 sobre `val nombre`, no con esta columna (17.2, n.º 30). Lógica exacta en 6.1. | Inferido (lógica leída en 6.1) | Pendiente de validación | — |
| RN09 | Columna calculada Convenios | Entregas Totales[Convenios] (6.1) | Marca «CONVENIOS» las entregas con `procedencia` = «Convenios»; las demás quedan vacías. Sin uso interno identificado: la página Convenios se separa con el filtro RN13 sobre `procedencia`, no con esta columna (17.2, n.º 31). Lógica exacta en 6.1. | Inferido (lógica leída en 6.1) | Pendiente de validación | — |
| RN10 | Filtro de página en Dashboard_Empresas | 569ba6f7876046e008bb: Entregas Totales[tipoventa_vista] IN (Flotas - Oficial, Flotas de Proximidad Oficial, Flotas Oficial, Flotilla Coorporativa) (11.1) | La página de Empresas solo muestra ventas de los tipos de flotilla/flota oficial listados; acota el universo a flotillas corporativas. | Encontrado (filtro de página) | No requerida | — |
| RN11 | Filtro de página en Dashboard_Empresas | b9e3f918c85149bec155: Entregas Totales[val nombre] IN (OTROS) (11.1) | Restringe, además, la página de Empresas al valor homologado «OTROS» de `val nombre`; conviene confirmar con el dueño si este filtro es intencional, porque acota fuertemente el universo. | Encontrado (filtro de página); interpretación del propósito: Inferido | Pendiente de validación | — |
| RN12 | Filtro de página en Dashboard_Renting | 5967654bebb0c4008a32: Entregas Totales[val nombre] NOT IN (OTROS) (11.1) | La página de Renting excluye el valor «OTROS» de `val nombre`; complementaria de RN11. | Encontrado (filtro de página) | No requerida | — |
| RN13 | Filtro de página en Dashboard_Convenios | 9735a5b6184a47d3e9cd: Entregas Totales[procedencia] IN (Convenios) (11.1) | La página de Convenios solo muestra entregas cuya `procedencia` es «Convenios». | Encontrado (filtro de página) | No requerida | — |
| RN14 | Filtro de página en Dashboard_Convenios | fe62f9fc0877e0ca25c0: Entregas Totales[procedenciadetalle] NOT IN (null) (11.1) | Excluye de Convenios las filas sin `procedenciadetalle`; evita registros sin detalle de convenio. | Encontrado (filtro de página) | No requerida | — |
| RN15 | Segmentación del tablero por línea de negocio (regla de conjunto) | Filtros de página RN10–RN14 sobre 377df594a011ae294444 · Dashboard_Empresas, ac291ea509382034e4ab · Dashboard_Renting y b597e26007760b8239c0 · Dashboard_Convenios | A nivel de conjunto, el tablero parte el universo de entregas «Nuevos» en tres vistas de negocio (empresas/flotillas, renting y convenios) mediante filtros de página sobre `tipoventa_vista`, `procedencia`, `procedenciadetalle` y `val nombre`; no hay una sola columna que defina la línea, sino la intersección de estos filtros por página. Las columnas RENTING y Convenios (RN08, RN09) reproducen parte de ese criterio, pero no se usan. | Inferido (deducida de la combinación de reglas y páginas) | Pendiente de validación | — |

# 15. Dependencias

- Medidas más referenciadas por otras medidas: [cantidad de maquinas] (12), [S2] (1), [S1] (1).
- Tablas sin relaciones con otras tablas: Val nombres.

```text
Fuente: Athena bi_materialized_data.entregas_totales
  -> Consulta M "Entregas Totales" (filtros de carga RN01 Cantidad=1 y RN02 tipo="Nuevos")
     -> Tabla 93060b2a-375c-4d50-968b-1547fed5fa65 · Entregas Totales (hechos)
        -> Columnas calculadas en uso: Región (RN04), Q (RN05), DIVISION S (RN06, semestre),
           val nombre (RN07, homologa contra la dim por LOOKUPVALUE); sin uso: Linea, RENTING, Convenios (RN03, RN08, RN09)
        -> Medidas: [cantidad de maquinas] (base de 12 medidas), [Ticket promedio], [S1], [S2]
           -> Visuales tarjeta: 4caed66b2e79ca489edc · Total unidades renting (KPI unidades renting);
              edd05e9bad4b3666886d · Ticket promedio (KPI ticket renting)
           -> Páginas: ac291ea509382034e4ab · Dashboard_Renting (RN12);
              377df594a011ae294444 · Dashboard_Empresas (RN10, RN11);
              b597e26007760b8239c0 · Dashboard_Convenios (RN13, RN14)
  Dimensión embebida 81048dff-8a9d-470a-84cf-65448a0e4ff3 · Val nombres: sin relación física;
     solo se consume por LOOKUPVALUE desde Entregas Totales[val nombre].
  Auxiliar 6b97fbbd-9f96-46d2-a0c1-268a68ffc23b · Fecha De Actualización: reloj M del refresco
     -> tarjetas "Última Actualización" (207ac3eed23edebbbe0c, 9734d2820ecd3ae8a0a0, 9769d8556306a6bbd114).
  Nota: varias tarjetas KPI calculan conteos implícitos en lugar de medidas (ver H-A11, H-A12, H-A13)
  y la columna Entregas Totales[Valor] alimenta las tarjetas "Utilidad bruta total" sin definición confirmada (ver V01).
```

# 16. Hallazgos, vacíos y puntos de revisión

Tabla maestra única (R45): hallazgos, riesgos, observaciones y vacíos de información, una fila por asunto. Las filas `H-A*` y `V-A*` las genera el script; la IA revisa certeza, prioridad e impacto y agrega las de negocio (`H01`, `V01`…). No se repite un asunto que ya cubre otra fila: se ajusta esa fila. La columna «Punto de revisión» no usa verbos de cambio (R47).

| ID | Tipo | Categoría | Descripción concreta | Página y objeto | page_id | visual_id / object_id (con nombre) | bookmark_id / estado | Evidencia exacta | Certeza | Objetos afectados y dependencias | Impacto | Prioridad | Punto de revisión | Validación requerida | Estado | Respuesta del dueño |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H-A01 | Riesgo | Referencias | 9 visuales (9 ocultos) muestran datos de la entidad «RUNT», que no existe en el modelo; no pueden dibujarse. | Dashboard_Convenios, Dashboard_Empresas, Dashboard_Renting | 377df594a011ae294444, ac291ea509382034e4ab, b597e26007760b8239c0 | 37a787e9cc28cd09e57b · Matriculas Runt; 6e32a80f73419213d127 · Matriculas por marca; 816c99a0a95005aa56b5 · Matriculas por modelo; 0de40f160ad554410865 · Matriculas por marca; 44e4621d600343c70058 · Matriculas por modelo; 9ec59c0900c0ad3cecaa · Matriculas Runt; 021d4850b3401880b984 · Matriculas Runt; 164619eb8a032ec27532 · Matriculas por modelo; 3627bccc9714708ee3dd · Matriculas por marca | — | Bindings de datos en visual.json (sección 9) | Encontrado | Bookmarks de 12.2 que los incluyen | Mantenimiento y confusión; error si se muestran | Media | Validar con el dueño si los visuales que usan «RUNT» pertenecen a este tablero. | Sí | Pendiente de validación | — |
| H-A02 | Riesgo | Referencias | 18 visuales (18 ocultos) muestran datos de la entidad «Cultivos», que no existe en el modelo; no pueden dibujarse. | Dashboard_Convenios, Dashboard_Empresas, Dashboard_Renting | 377df594a011ae294444, ac291ea509382034e4ab, b597e26007760b8239c0 | 47d666fc117c70ae6c77 · Participación por mecanización; 86f85bbed000b2922793 · Producción (T); 9f04b9ce6587b5610998 · Rendimiento (t/ha); b43695b0ad1280b26827 · Participación por cultivo área sembrada has (TOP 5); e47ca6b0e42237a8ec22 · Mecanizacion por departamento; fcae268396d974c397bd · Mecanización por regional; 1a394380135072c054c8 · Rendimiento (t/ha); 2b6d4c39222aa4000302 · Mecanización por regional; 647df1e1caca5a76abc8 · Producción (T); 7372de39e4387230a26c · Mecanizacion por departamento; 9c9f9e7740ae80a69e13 · Participación por cultivo área sembrada has (TOP 5); f95237a70a2b397ab6c0 · Participación por mecanización; 6dd1451dbdca03ca528e · Producción (T); 6e4fc275427d71c147c7 · Rendimiento (t/ha); 7d4ca467440bb30d6806 · Mecanizacion por departamento; b754c1660bd8235ebd7d · Participación por cultivo área sembrada has (TOP 5); d1c4d3f2924268689638 · Mecanización por regional; fd63ac47e9e00c202bcd · Participación por mecanización | — | Bindings de datos en visual.json (sección 9) | Encontrado | Bookmarks de 12.2 que los incluyen | Mantenimiento y confusión; error si se muestran | Media | Validar con el dueño si los visuales que usan «Cultivos» pertenecen a este tablero. | Sí | Pendiente de validación | — |
| H-A03 | Riesgo | Referencias | 9 visuales (9 ocultos) muestran datos de la entidad «Importaciones», que no existe en el modelo; no pueden dibujarse. | Dashboard_Convenios, Dashboard_Empresas, Dashboard_Renting | 377df594a011ae294444, ac291ea509382034e4ab, b597e26007760b8239c0 | 742a219cd1940a983530 · Importaciones; 81cdeccbcb7940787603 · Especificación Importadores; aff3f4a45ab91a74047e · Importaciones (CIF); 4a086741483d06edbbe1 · Especificación Importadores; 710b4bdd807785877d66 · Importaciones (CIF); 8106d7c0e70d14e3cc6e · Importaciones; 1e6271e61744ac760b0a · Importaciones; d63f39364345bc22e6ea · Especificación Importadores; ed7dcba836dbc5a82b07 · Importaciones (CIF) | — | Bindings de datos en visual.json (sección 9) | Encontrado | Bookmarks de 12.2 que los incluyen | Mantenimiento y confusión; error si se muestran | Media | Validar con el dueño si los visuales que usan «Importaciones» pertenecen a este tablero. | Sí | Pendiente de validación | — |
| H-A04 | Observación | Presentación | 1 visual que funciona conserva reglas de formato que apuntan a entidades inexistentes (Cultivos, Importaciones, spiga_CotizacionesVN). Otros 9 visuales con formato huérfano ya están rotos por sus datos y se cubren en los hallazgos de referencias; todos figuran como «Formato huérfano» en los bindings de la sección 9. | Dashboard_Convenios | b597e26007760b8239c0 | 9fd256fc444b2ac5015b · Participación por convenio (unidades año) | — | Filas «Formato huérfano» en los bindings (sección 9) | Encontrado | Ninguno: la regla no se aplica | Bajo: no afecta los datos mostrados | Baja | Revisar con el dueño si estos formatos heredados de la plantilla deben conservarse. | Sí | Pendiente de validación | — |
| H-A05 | Riesgo | Referencias | 14 bookmarks apuntan a páginas que no existen (6acb58945104d5318733, 7adad99113991d0e3e3e). | Reporte | — | 0340d676b7e24e06b31d · Grafica imp; 0e8fa233336b7005c554 · Resumen matriculas; 32318b42c9d3954d5e19 · Participacion; 598a9e8ed007000d0750 · Intencion; 6a7dad0d996da4853d64 · Regional; 7052bcd3da2e11b02291 · Tipo de cliente; 73126f0c2c300ec3c0d6 · Marca; 9ab9f550c06d5e43709b · Importadores; aa98c6807620b2365ea7 · CIF; c2e908097e6ad07bc67a · Cultivo; d66c5cc860884db34063 · Modelo; d9c095c65d1a6600d67b · Capacidad; de6e833a9e73fa72fe5a · Departamento; fc32d496129c0a4cf7cf · Maquina | activeSection | bookmark.json (sección 12.1) | Encontrado | Botones o navegadores que los invoquen (12.4) | Navegación sin destino | Media | Validar visualmente en Power BI qué ocurre al activar estos bookmarks. | Sí | Pendiente de validación | — |
| H-A06 | Riesgo | Referencias | 10 bookmarks de páginas existentes solo actúan sobre visuales rotos o inexistentes: al activarlos muestran u ocultan visuales que no funcionan. | Reporte | b597e26007760b8239c0 | 056202b7179ab3579a5d · Mecanización regional; 1432afe915c833a1d898 · Sembrado; 149b0ada0237e9634a0e · Rendimiento periodo; 179c088255033bc80d1e · Mecanización dep; 2956125ff44a3e8bed0b · Rendimiento; 99730fcf006ee5428731 · Produccion; c6c5e695dd35e1557b51 · Participación; c75c33bbd31e25d2730d · Area C+S; d2df5f2304dd79671498 · Resumen; f769f2b49e137d3a2026 · Cosechado | Targets (12.2) | bookmark.json (sección 12.2) | Encontrado | Visuales rotos de la sección 9 | Puede mostrar mensajes de error al usuario | Media | Validar visualmente en Power BI cada bookmark con el dueño. | Sí | Pendiente de validación | — |
| H-A07 | Riesgo | Referencias | El botón «Conectividad» navega a la página 7fe28b006cd3b491a578, que no existe. | Dashboard_Empresas | 377df594a011ae294444 | ab3e643b10d65600d211 · Conectividad | 2956125ff44a3e8bed0b · Rendimiento | visualLink en visual.json (12.4) | Encontrado | Bookmark asociado: 2956125ff44a3e8bed0b · Rendimiento | Botón sin destino | Media | Validar visualmente en Power BI a dónde lleva el botón. | Sí | Pendiente de validación | — |
| H-A08 | Observación | Modelo | Medidas sin expresión: Medida. | Modelo | — | 8e2854d0-05a5-4afa-b723-e627a276907b · Medida | — | TMDL (sección 7) | Encontrado | Ninguno | Bajo | Baja | Confirmar con el dueño si estas medidas se necesitan. | Sí | Pendiente de validación | — |
| H-A09 | Observación | Modelo | Medidas con la misma expresión: Año Anterior, Medida 2. | Modelo | — | 5e65ec2b-b63c-4038-8140-d68832f20c73 · Año Anterior; d96eb974-557d-4111-9838-b22f90197c83 · Medida 2 | — | TMDL (sección 7) | Encontrado | Ver columna «Usa» de la sección 7 | Bajo | Baja | Confirmar con el dueño cuál de las medidas es la vigente. | Sí | Pendiente de validación | — |
| H-A10 | Observación | Reporte | 2 segmentaciones visibles de Entregas Totales[Q] en la misma página. | Dashboard_Empresas | 377df594a011ae294444 | 86c38682d276ded8a3ea · Segmentación: Trimestre (Entregas Totales[Q]); b2df3c91709631415d59 · Segmentación: Trimestre (Entregas Totales[Q]) | — | Bindings (sección 9) y 11.2 | Encontrado | Interacciones de 11.3 | Bajo | Baja | Revisar con el dueño el propósito de cada segmentación. | Sí | Pendiente de validación | — |
| H-A11 | Hallazgo | Métrica | 2 tarjeta(s) calculan Count(Entregas Totales[procedenciadetalle]), un conteo implícito de filas y no una medida. | Dashboard_Convenios, Dashboard_Empresas | 377df594a011ae294444, b597e26007760b8239c0 | 1ab49030c00e0a200aa4 · Empresas distintas; 9a88093ab5402c6e7a10 · Convenios vigentes hoy | — | Bindings en visual.json (secciones 9 y 10) | Encontrado | Columna Entregas Totales[procedenciadetalle] | El valor puede no corresponder al título de la tarjeta | Media | Confirmar con el dueño qué debe mostrar cada tarjeta y si el título coincide con lo calculado. | Sí | Pendiente de validación | — |
| H-A12 | Hallazgo | Métrica | 3 tarjeta(s) calculan CountNonNull(Entregas Totales[año]), un conteo implícito de filas y no una medida. Incluye una tarjeta rotulada «Ticket promedio» (f8afa36aecb1ce0d8a16) que muestra un conteo, no un promedio: el valor no corresponde al concepto del título. | Dashboard_Convenios, Dashboard_Empresas | 377df594a011ae294444, b597e26007760b8239c0 | 94deb273c33108980691 · Total unidades empresarial; f8afa36aecb1ce0d8a16 · Ticket promedio; b0bdeb16560aa2033e76 · Total unidades convenios | — | Bindings en visual.json (secciones 9 y 10) | Encontrado | Columna Entregas Totales[año] | Un KPI rotulado «Ticket promedio» muestra un conteo; riesgo de lectura errónea del valor | Alta | Confirmar con el dueño qué debe mostrar cada tarjeta y si el título coincide con lo calculado, en especial la tarjeta «Ticket promedio». | Sí | Pendiente de validación | — |
| H-A13 | Hallazgo | Métrica | 1 tarjeta(s) calculan Count(Entregas Totales[val nombre]), un conteo implícito de filas y no una medida. | Dashboard_Renting | ac291ea509382034e4ab | de06c3fb442c76b90246 · Empresas renting activas | — | Bindings en visual.json (secciones 9 y 10) | Encontrado | Columna Entregas Totales[val nombre] | El valor puede no corresponder al título de la tarjeta | Media | Confirmar con el dueño qué debe mostrar cada tarjeta y si el título coincide con lo calculado. | Sí | Pendiente de validación | — |
| H-A14 | Observación | Seguridad | El rol «Todo» no tiene reglas RLS. | Modelo | — | Todo | — | GC - Flotillas.SemanticModel/definition/roles/Todo.tmdl | Encontrado | Todas las tablas | Acceso total a las filas | Baja | Confirmar con el dueño si corresponde seguridad por filas. | Sí | Pendiente de validación | — |
| V-A01 | Vacío | Gobierno | No se conoce: Frecuencia y proceso de actualización. | BI | — | — | — | El PBIP no guarda la programación de refresco | Desconocido | — | Vigencia del dato | Media | Confirmar con el dueño. | Sí (edgar.p@nebula.com.co) | Pendiente de validación | — |
| V-A02 | Vacío | Gobierno | No se conoce: Ambiente y workspace de publicación. | BI | — | — | — | Sin evidencia en el PBIP | Desconocido | — | Dónde se consume | Media | Confirmar con el dueño. | Sí (edgar.p@nebula.com.co) | Pendiente de validación | — |
| V-A03 | Vacío | Gobierno | No se conoce: Propietario de cada fuente de la sección 3. | BI | — | — | — | No está en el PBIP | Desconocido | — | Gobierno del dato | Media | Confirmar con el dueño. | Sí (edgar.p@nebula.com.co) | Pendiente de validación | — |
| V01 | Vacío | Métrica | No se conoce la definición de la columna Entregas Totales[Valor]: tres tarjetas la suman y la rotulan «Utilidad bruta total», pero no hay evidencia de que sea utilidad bruta (podría ser precio, costo, importe facturado u otro). | Dashboard_Empresas, Dashboard_Renting, Dashboard_Convenios | 377df594a011ae294444, ac291ea509382034e4ab, b597e26007760b8239c0 | 856aee5d89c35b6c0aeb · Utilidad bruta total; 918d228ab18d5045e510 · Utilidad bruta total; 5f7e3e000ac60870579e · Utilidad bruta total | — | Columna Entregas Totales[Valor] en el modelo (secciones 6.1 y 10); no hay descripción en el TMDL | Desconocido | Tarjetas «Utilidad bruta total» de las tres páginas | Un KPI financiero puede estar mal rotulado | Media | Confirmar con el dueño qué representa Entregas Totales[Valor] y si «Utilidad bruta total» es el título correcto. | Sí (edgar.p@nebula.com.co) | Pendiente de validación | — |

# 17. Limitaciones y control para DLC posteriores

## 17.1 Limitaciones

1. Censo estructural: no se ejecutó el modelo ni se vieron datos; un binding correcto no garantiza el valor mostrado.
2. La fuente de datos (sección 3) no se consultó; el uso de columnas fuera del PBIP no es verificable.
3. El efecto en ejecución de bookmarks y botones requiere validación visual en Power BI Desktop.
4. Literales de más de 300 caracteres en M (por ejemplo, tablas embebidas en base64) se omiten en la sección 4; están en el TMDL. Del contenido de esas tablas (por ejemplo, un mapeo de homologación) solo se documenta su efecto en el modelo.
5. El censo describe solo la versión analizada del PBIP; los cambios respecto a versiones anteriores están en «[BI] - cambios.md» (R52).

Sin limitaciones adicionales.

## 17.2 Candidatas a depuración

Objetos con estado `Sin uso interno identificado` o `Referencia rota`. Su detalle está en la sección de origen; aquí solo lo que necesita el DLC de depuración. Aprobación de todas: **Pendiente; el CENSO no autoriza eliminar** (R27). Los objetos `En uso` y `Uso técnico` se consideran protegidos. Los formatos huérfanos no son candidatos: su visual funciona.

Riesgo y pruebas por defecto según el tipo de objeto (la IA puede precisarlos en la columna «Nota» de cada fila):

| Tipo | Riesgo por defecto | Pruebas sugeridas |
|---|---|---|
| Bookmark | Bajo | Probar navegación y botones |
| Columna | Medio: puede tener uso fuera del PBIP (fuente, otros reportes) | Confirmar con el dueño y con la fuente; comparar totales de visuales antes y después |
| Columna calculada | Bajo: sin consumidores en el PBIP | Comparar visuales y medidas antes y después |
| Medida | Bajo: sin consumidores en el PBIP | Abrir todas las páginas y revisar errores |
| Visual | Bajo si está oculto; medio si es visible | Comparar la página en cada bookmark antes y después |

| # | Tipo | Objeto | ID | Sección | Estado de uso | Nota |
|---:|---|---|---|---|---|---|
| 1 | Columna calculada | Entregas Totales[Linea] | 2708d650-1f2e-4c3c-bd68-5537046823ca | 6.1 | Sin uso interno identificado | — |
| 2 | Columna | Entregas Totales[IdEmpresas] | 8e1eec6d-2100-4451-b7be-092f74b77aee | 6.1 | Sin uso interno identificado | — |
| 3 | Columna | Entregas Totales[CodigoEmpresa] | 55eb0c15-3bfa-4c07-8d92-210a84bff343 | 6.1 | Sin uso interno identificado | — |
| 4 | Columna | Entregas Totales[Empresa] | c6a74202-6da6-40a0-8a20-426ec13b551b | 6.1 | Sin uso interno identificado | — |
| 5 | Columna | Entregas Totales[CodigoCentro] | e29f126d-d0c9-4d1b-b382-189c0a69873b | 6.1 | Sin uso interno identificado | — |
| 6 | Columna | Entregas Totales[CodigoSeccion] | 1ae04e8e-0ff3-48d7-b9c2-ac89a6dd98d8 | 6.1 | Sin uso interno identificado | — |
| 7 | Columna | Entregas Totales[Seccion] | 1f382698-d1b3-4e6a-9423-884746ef0966 | 6.1 | Sin uso interno identificado | — |
| 8 | Columna | Entregas Totales[CodigoMarca] | 92faf536-a44f-498b-af27-fbf3a2102f87 | 6.1 | Sin uso interno identificado | — |
| 9 | Columna | Entregas Totales[CodigoGama] | cf67ef9b-4a69-457a-9df7-fc078e087c4a | 6.1 | Sin uso interno identificado | — |
| 10 | Columna | Entregas Totales[CodigoModelo] | 6b284f60-f9c8-4243-8621-98e747ac1490 | 6.1 | Sin uso interno identificado | — |
| 11 | Columna | Entregas Totales[AñoModelo] | 7721f26c-91f1-4e98-ac2c-e81c76cfcf93 | 6.1 | Sin uso interno identificado | — |
| 12 | Columna | Entregas Totales[Modelo] | f262bdaa-ee85-4e87-9fd9-3cad5fab6f33 | 6.1 | Sin uso interno identificado | — |
| 13 | Columna | Entregas Totales[CedulaVendedor] | 3207f566-fbc3-4776-9435-3ece08642f00 | 6.1 | Sin uso interno identificado | — |
| 14 | Columna | Entregas Totales[NombreVendedor] | 47633825-94f6-41a8-a4e1-88ec933239dc | 6.1 | Sin uso interno identificado | — |
| 15 | Columna | Entregas Totales[Nit] | 576abc15-8686-4c32-a229-182c113e5324 | 6.1 | Sin uso interno identificado | — |
| 16 | Columna | Entregas Totales[VIN] | 99d30921-c2b5-4c63-91f0-899ccfc15ecc | 6.1 | Sin uso interno identificado | — |
| 17 | Columna | Entregas Totales[Entrega] | 93162a6a-96c7-4c1d-9779-2d8c5c0ff097 | 6.1 | Sin uso interno identificado | — |
| 18 | Columna | Entregas Totales[placa] | 9d44a9c8-fee6-41e2-b462-3e4cc4dec7a6 | 6.1 | Sin uso interno identificado | — |
| 19 | Columna | Entregas Totales[tipooportunidad] | 7173d367-afb7-4df9-9e5d-4696920a1596 | 6.1 | Sin uso interno identificado | — |
| 20 | Columna | Entregas Totales[correo] | fff50d4e-3578-43e2-8c45-d73fa10c2565 | 6.1 | Sin uso interno identificado | — |
| 21 | Columna | Entregas Totales[codunidadnegocio] | 3892cac9-e567-451f-90b9-94061a948254 | 6.1 | Sin uso interno identificado | — |
| 22 | Columna | Entregas Totales[nombreunidadnegocio] | 4af06471-46d8-470c-9a3f-d7ae1796198c | 6.1 | Sin uso interno identificado | — |
| 23 | Columna | Entregas Totales[tipocliente] | e2f242e9-bb6d-46ba-a88b-c5452ce0348e | 6.1 | Sin uso interno identificado | — |
| 24 | Columna | Entregas Totales[nombrevendedorhomologado] | 69af02df-4586-4eab-b02c-09becd2577fc | 6.1 | Sin uso interno identificado | — |
| 25 | Columna | Entregas Totales[clase] | 1788f9fa-aa12-4927-b3e6-6d6033ff6d11 | 6.1 | Sin uso interno identificado | — |
| 26 | Columna | Entregas Totales[color] | d96d9bb5-2858-4953-8cec-edf95d0c68a9 | 6.1 | Sin uso interno identificado | — |
| 27 | Columna | Entregas Totales[esultimamodificacion] | 26a41a2c-2321-4b16-802b-816bf9384e49 | 6.1 | Sin uso interno identificado | — |
| 28 | Columna | Entregas Totales[rowhash] | 1612656f-b1d3-4dcf-b173-ab0d08ec21ef | 6.1 | Sin uso interno identificado | — |
| 29 | Columna | Entregas Totales[extractionid] | 3b82c226-f373-44f0-8fe8-e3b85de25b88 | 6.1 | Sin uso interno identificado | — |
| 30 | Columna calculada | Entregas Totales[RENTING] | 4786567f-9f0e-4063-8aea-5f1801f181dc | 6.1 | Sin uso interno identificado | — |
| 31 | Columna calculada | Entregas Totales[Convenios] | 1996f16a-30b2-4c1c-a526-9cf4a7810a85 | 6.1 | Sin uso interno identificado | — |
| 32 | Columna | Entregas Totales[emailvendedor] | 5b443a28-0fbb-4cc8-9975-8915f264fbfa | 6.1 | Sin uso interno identificado | — |
| 33 | Medida | [Medida] | 8e2854d0-05a5-4afa-b723-e627a276907b | 7 | Sin uso interno identificado | — |
| 34 | Medida | [Medida 2] | d96eb974-557d-4111-9838-b22f90197c83 | 7 | Sin uso interno identificado | — |
| 35 | Visual | Matriculas Runt (Dashboard_Empresas) | 37a787e9cc28cd09e57b | 9 | Referencia rota | — |
| 36 | Visual | Participación por mecanización (Dashboard_Empresas) | 47d666fc117c70ae6c77 | 9 | Referencia rota | — |
| 37 | Visual | Matriculas por marca (Dashboard_Empresas) | 6e32a80f73419213d127 | 9 | Referencia rota | — |
| 38 | Visual | Importaciones (Dashboard_Empresas) | 742a219cd1940a983530 | 9 | Referencia rota | — |
| 39 | Visual | Matriculas por modelo (Dashboard_Empresas) | 816c99a0a95005aa56b5 | 9 | Referencia rota | — |
| 40 | Visual | Especificación Importadores (Dashboard_Empresas) | 81cdeccbcb7940787603 | 9 | Referencia rota | — |
| 41 | Visual | Producción (T) (Dashboard_Empresas) | 86f85bbed000b2922793 | 9 | Referencia rota | — |
| 42 | Visual | Rendimiento (t/ha) (Dashboard_Empresas) | 9f04b9ce6587b5610998 | 9 | Referencia rota | — |
| 43 | Visual | Importaciones (CIF) (Dashboard_Empresas) | aff3f4a45ab91a74047e | 9 | Referencia rota | — |
| 44 | Visual | Participación por cultivo área sembrada has (TOP 5) (Dashboard_Empresas) | b43695b0ad1280b26827 | 9 | Referencia rota | — |
| 45 | Visual | Mecanizacion por departamento (Dashboard_Empresas) | e47ca6b0e42237a8ec22 | 9 | Referencia rota | — |
| 46 | Visual | Mecanización por regional (Dashboard_Empresas) | fcae268396d974c397bd | 9 | Referencia rota | — |
| 47 | Visual | Matriculas por marca (Dashboard_Renting) | 0de40f160ad554410865 | 9 | Referencia rota | — |
| 48 | Visual | Rendimiento (t/ha) (Dashboard_Renting) | 1a394380135072c054c8 | 9 | Referencia rota | — |
| 49 | Visual | Mecanización por regional (Dashboard_Renting) | 2b6d4c39222aa4000302 | 9 | Referencia rota | — |
| 50 | Visual | Matriculas por modelo (Dashboard_Renting) | 44e4621d600343c70058 | 9 | Referencia rota | — |
| 51 | Visual | Especificación Importadores (Dashboard_Renting) | 4a086741483d06edbbe1 | 9 | Referencia rota | — |
| 52 | Visual | Producción (T) (Dashboard_Renting) | 647df1e1caca5a76abc8 | 9 | Referencia rota | — |
| 53 | Visual | Importaciones (CIF) (Dashboard_Renting) | 710b4bdd807785877d66 | 9 | Referencia rota | — |
| 54 | Visual | Mecanizacion por departamento (Dashboard_Renting) | 7372de39e4387230a26c | 9 | Referencia rota | — |
| 55 | Visual | Importaciones (Dashboard_Renting) | 8106d7c0e70d14e3cc6e | 9 | Referencia rota | — |
| 56 | Visual | Participación por cultivo área sembrada has (TOP 5) (Dashboard_Renting) | 9c9f9e7740ae80a69e13 | 9 | Referencia rota | — |
| 57 | Visual | Matriculas Runt (Dashboard_Renting) | 9ec59c0900c0ad3cecaa | 9 | Referencia rota | — |
| 58 | Visual | Participación por mecanización (Dashboard_Renting) | f95237a70a2b397ab6c0 | 9 | Referencia rota | — |
| 59 | Visual | Matriculas Runt (Dashboard_Convenios) | 021d4850b3401880b984 | 9 | Referencia rota | — |
| 60 | Visual | Matriculas por modelo (Dashboard_Convenios) | 164619eb8a032ec27532 | 9 | Referencia rota | — |
| 61 | Visual | Importaciones (Dashboard_Convenios) | 1e6271e61744ac760b0a | 9 | Referencia rota | — |
| 62 | Visual | Matriculas por marca (Dashboard_Convenios) | 3627bccc9714708ee3dd | 9 | Referencia rota | — |
| 63 | Visual | Producción (T) (Dashboard_Convenios) | 6dd1451dbdca03ca528e | 9 | Referencia rota | — |
| 64 | Visual | Rendimiento (t/ha) (Dashboard_Convenios) | 6e4fc275427d71c147c7 | 9 | Referencia rota | — |
| 65 | Visual | Mecanizacion por departamento (Dashboard_Convenios) | 7d4ca467440bb30d6806 | 9 | Referencia rota | — |
| 66 | Visual | Participación por cultivo área sembrada has (TOP 5) (Dashboard_Convenios) | b754c1660bd8235ebd7d | 9 | Referencia rota | — |
| 67 | Visual | Mecanización por regional (Dashboard_Convenios) | d1c4d3f2924268689638 | 9 | Referencia rota | — |
| 68 | Visual | Especificación Importadores (Dashboard_Convenios) | d63f39364345bc22e6ea | 9 | Referencia rota | — |
| 69 | Visual | Importaciones (CIF) (Dashboard_Convenios) | ed7dcba836dbc5a82b07 | 9 | Referencia rota | — |
| 70 | Visual | Participación por mecanización (Dashboard_Convenios) | fd63ac47e9e00c202bcd | 9 | Referencia rota | — |
| 71 | Bookmark | Grafica imp | 0340d676b7e24e06b31d | 12 | Referencia rota | — |
| 72 | Bookmark | Mecanización regional | 056202b7179ab3579a5d | 12 | Referencia rota | — |
| 73 | Bookmark | Resumen matriculas | 0e8fa233336b7005c554 | 12 | Referencia rota | — |
| 74 | Bookmark | Sembrado | 1432afe915c833a1d898 | 12 | Referencia rota | — |
| 75 | Bookmark | Rendimiento periodo | 149b0ada0237e9634a0e | 12 | Referencia rota | — |
| 76 | Bookmark | Mecanización dep | 179c088255033bc80d1e | 12 | Referencia rota | — |
| 77 | Bookmark | Rendimiento | 2956125ff44a3e8bed0b | 12 | Referencia rota | — |
| 78 | Bookmark | Participacion | 32318b42c9d3954d5e19 | 12 | Referencia rota | — |
| 79 | Bookmark | Intencion | 598a9e8ed007000d0750 | 12 | Referencia rota | — |
| 80 | Bookmark | Regional | 6a7dad0d996da4853d64 | 12 | Referencia rota | — |
| 81 | Bookmark | Tipo de cliente | 7052bcd3da2e11b02291 | 12 | Referencia rota | — |
| 82 | Bookmark | Marca | 73126f0c2c300ec3c0d6 | 12 | Referencia rota | — |
| 83 | Bookmark | Produccion | 99730fcf006ee5428731 | 12 | Referencia rota | — |
| 84 | Bookmark | Importadores | 9ab9f550c06d5e43709b | 12 | Referencia rota | — |
| 85 | Bookmark | CIF | aa98c6807620b2365ea7 | 12 | Referencia rota | — |
| 86 | Bookmark | Cultivo | c2e908097e6ad07bc67a | 12 | Referencia rota | — |
| 87 | Bookmark | Participación | c6c5e695dd35e1557b51 | 12 | Referencia rota | — |
| 88 | Bookmark | Area C+S | c75c33bbd31e25d2730d | 12 | Referencia rota | — |
| 89 | Bookmark | Resumen | d2df5f2304dd79671498 | 12 | Referencia rota | — |
| 90 | Bookmark | Modelo | d66c5cc860884db34063 | 12 | Referencia rota | — |
| 91 | Bookmark | Capacidad | d9c095c65d1a6600d67b | 12 | Referencia rota | — |
| 92 | Bookmark | Departamento | de6e833a9e73fa72fe5a | 12 | Referencia rota | — |
| 93 | Bookmark | Cosechado | f769f2b49e137d3a2026 | 12 | Referencia rota | — |
| 94 | Bookmark | Maquina | fc32d496129c0a4cf7cf | 12 | Referencia rota | — |

# 18. Validación final

## 18.1 Conciliación contra el PBIP

| Inventario | En PBIP | En este documento | Diferencia |
|---|---:|---:|---:|
| Tablas | 10 | 10 | 0 |
| Columnas | 105 | 105 | 0 |
| Medidas | 15 | 15 | 0 |
| Relaciones | 6 | 6 | 0 |
| Páginas | 3 | 3 | 0 |
| Visuales | 93 | 93 | 0 |
| Filtros | 57 | 57 | 0 |
| Segmentaciones | 20 | 20 | 0 |
| Interacciones | 21 | 21 | 0 |
| Bookmarks | 24 | 24 | 0 |
| Recursos | 4 | 4 | 0 |

`censo.py validar` recalcula esta tabla desde el documento y el PBIP. El resultado de la validación queda en `historial-censos.md`.

## 18.2 Estado final

El censo cubrió por completo el PBIP en lectura (modelo TMDL, consultas M, DAX, reporte PBIR, filtros, interacciones, bookmarks, botones y recursos) y todos los marcadores quedaron resueltos. El estado es «Completado pendiente de validación» porque los 14 hallazgos (H-A01–H-A14) y los 4 vacíos (V-A01–V-A03 y V01) requieren confirmación del dueño del tablero y validación visual en Power BI Desktop; el ritual no autoriza eliminar objetos ni cerrar como validado sin esa confirmación.
