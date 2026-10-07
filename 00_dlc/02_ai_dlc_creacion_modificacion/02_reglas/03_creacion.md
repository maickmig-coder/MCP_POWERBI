# 5. REGLAS DE CREACIÓN

## Levantamiento obligatorio

Solicitar:
- nombre;
- contexto;
- finalidad;
- qué se requiere medir;
- decisión que debe apoyar;
- público objetivo;
- fuentes/servidores;
- páginas y propósito;
- KPIs;
- filtros;
- navegación;
- actualización;
- seguridad;
- interacciones cuando apliquen.

## KPIs

Preguntar:
"¿Deseas definir los KPIs o quieres que proponga opciones?"

Si propone IA:
- nombre;
- qué mide;
- campos requeridos;
- lógica;
- utilidad;
- posibles dependencias.

El usuario/analista decide.

## Visuales

Preguntar:
"¿Deseas definir los gráficos o quieres que proponga opciones?"

Si propone IA:
- visual;
- propósito;
- campos/medidas;
- página;
- justificación.

El usuario/analista decide.

## Fuentes

Registrar cuando esté disponible:
- servidor;
- motor;
- base de datos;
- esquema;
- tablas/vistas;
- método de conexión.

No solicitar credenciales como parte del levantamiento.

## Modelo

Definir/proponer:
- modelo estrella u otra estructura;
- hechos/dimensiones;
- granularidad;
- claves;
- relaciones;
- calendario;
- medidas;
- columnas/tablas calculadas;
- transformaciones;
- DAX.

## Páginas

Solicitar cantidad y propósito.

## Layout

Usar mesa de trabajo corporativa, instrucciones del usuario y estándar visual.
No ubicar arbitrariamente.

## Otros

Contemplar cuando aplique:
- RLS;
- actualización;
- drill-through;
- drill-down;
- tooltips;
- bookmarks;
- interacciones;
- exportaciones.


## Registro obligatorio desde el inicio

Antes de iniciar la construcción:

1. crear la carpeta:
   `NIGGA\01_bi\01_versiones\00_original\[Nombre exacto BI]`;
2. crear `README.md` usando la plantilla de control por tablero;
3. registrar responsable, solicitante, fecha de inicio, estado y objetivo;
4. actualizar `REGISTRO_CONTROL_TABLEROS.md`.

En una creación nueva, el README comienza la historia del tablero. Cuando el
BI sea entregado, su versión base debe quedar identificada en el histórico para
que futuras modificaciones continúen sobre la misma trazabilidad.


## Identificación por correo desde el inicio

Antes de iniciar una creación se deben registrar únicamente:

- correo de quien trabaja/modifica el tablero;
- correo de quien solicita/es dueño del requerimiento.

El registro queda en el README del tablero y en el registro central.
