// Versión de práctica: estructura real del origen (catálogo de Athena o, si no está, censos); 0 filas. No contiene datos.
let
    Fuente = #table(
        type table [
            #"lead_id" = type text,
            #"campaing_name" = type text,
            #"medium_value" = type text,
            #"category_name" = type text,
            #"brand_name" = type text,
            #"adviser_name" = type text,
            #"adviser_email" = type text,
            #"client_name" = type text,
            #"client_phone" = type text,
            #"client_email" = type text,
            #"created_at" = type datetime,
            #"updated_at" = type datetime,
            #"lead_created_at" = type datetime,
            #"management_time" = type number,
            #"nombre_origen" = type text,
            #"grupo" = type text,
            #"primer_usuario" = type text,
            #"primer_grupo" = type text,
            #"tipificacion" = type text,
            #"atencion" = type text,
            #"atendido" = type text,
            #"ultima_actualizacion" = type datetime,
            #"fecha_asignacion" = type datetime,
            #"asignado" = type text,
            #"canal" = type text,
            #"fh_primer_mensaje_agente" = type datetime,
            #"fh_asignacion_primera" = type text
        ],
        {}
    )
in
    Fuente
