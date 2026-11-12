let
    Origen = AmazonAthena.Databases("Athena_ODBC2", null, []),
    Nav1_AwsDataCatalog = Origen{[Name="AwsDataCatalog",Kind="Database"]}[Data],
    Nav2_bi_materialized_data = Nav1_AwsDataCatalog{[Name="bi_materialized_data",Kind="Schema"]}[Data],
    Nav3_entregas_totales = Nav2_bi_materialized_data{[Name="entregas_totales",Kind="Table"]}[Data]
in
    Nav3_entregas_totales
