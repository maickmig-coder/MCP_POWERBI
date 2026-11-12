# Diccionario de datos — Fuentes de los tableros

> diccionario_id: 20261112T172206-diccionario · generado 2026-11-12T17:22:06-05:00 por miguel.b@nebula.com.co · versión 2.3
>
> Censos usados: GC - Flotillas (20261105T124212-gc-flotillas)

La estructura es la **real de la base**, antes de cualquier ajuste de un tablero: si la tabla está en el catálogo de Athena, columnas y tipos salen de ahí; si no (fuente aún no migrada), salen del censo y se marcan «no verificado en catálogo». No se registran datos ni contraseñas. Aquí aparecen las tablas que algún tablero censado usa.

**Para tableros nuevos:** el catálogo de Athena tiene además **653 tablas que ningún tablero usa todavía**. No se listan aquí, pero se encuentran con «busca fuente …» y se puede preparar su versión de práctica igual que las demás.

## 1. Conexiones

| Conexión | Tipo de conexión | Servidor / DSN | Tablas | Tableros que la usan |
|---|---|---|---:|---|
| `amazon_athena:Athena_ODBC2` | Amazon Athena (`AmazonAthena.Databases`) | Athena_ODBC2 | 1 | GC - Flotillas |

## 2. Tablas

| Tabla | Conexión | Ruta | Columnas | Estructura tomada de | Tableros que la usan |
|---|---|---|---:|---|---|
| **entregas_totales** | `amazon_athena:Athena_ODBC2` | AwsDataCatalog / bi_materialized_data / entregas_totales | 47 | Catálogo Athena (diccionario-datos.md) | GC - Flotillas |

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

