# 4. DISEÑO CORPORATIVO

## 4.1 Header

### Header principal
- Tipo: rectángulo.
- Color: `#323131`.
- Alto: `155`.
- Ancho de referencia: `1279`.
- La altura definida debe conservarse.

### Título
- Fuente: Segoe UI.
- Color: `#FFFFFF`.
- Tamaño: 24 px.
- Negrilla.
- Alto: 68 px.
- Ancho: depende del texto.
- Debe identificar claramente BI, módulo o sección.

### Separador
- Forma: línea.
- Remate: plano.
- Borde: `#FFFFFF`.

### Última actualización
- Color: `#FFFFFF`.
- Tamaño: 12 px.
- Negrilla.
- Alto: 68 px.
- Ancho: 226 px.
- Mantener posición/tratamiento consistente.

### Logo Nebula
Fuente oficial:

`C:\dev\NIGGA\00_dlc\02_ai_dlc_creacion_modificacion\00_fuentes\Logo_Nebula.png`

Reglas:
- debe utilizarse la fuente corporativa oficial;
- ubicación: parte superior derecha del Header;
- conservar la posición de referencia;
- no moverlo de lado ni sustituirlo automáticamente;
- si la fuente no está disponible, informar y solicitar la fuente/autorización.

## 4.2 Segmentaciones

- Alto: 69 px.
- Ancho: variable según cantidad.
- Encabezado: 10 px Bold, `#FFFFFF`, fondo `#323131`.
- Selector: 12 px Regular, texto `#323131`, fondo `#FFFFFF`,
  borde `#CDCDD1`.

### Jerarquía

1. Año
2. Mes
3. Campaña
4. Categoría
5. Centro
6. Tipificación
7. Fuente
8. Gestión Leads

Reglas:
- solo ordenar los filtros presentes;
- los faltantes se omiten;
- no crear un filtro faltante solo por cumplir la jerarquía;
- los adicionales van después de los estándar;
- el título debe corresponder al campo real.

## 4.3 Botones

Estándar corporativo vigente:
- texto: 12 px Bold;
- radio: 6 px;
- primario: fondo `#FFFFFF`, borde `#1A73E8`;
- menú: texto `#1A73E8`, fondo `#FFFFFF`;
- elementos azules de acción/navegación: `#1A73E8`.

Nota de control de versión:
Una versión anterior utilizaba radio 4 px. El estándar vigente queda en 6 px.
No deben coexistir ambas reglas en una misma versión oficial.

## 4.4 Gráficos

- Fondo: `#FFFFFF`.
- Título: 14 px Bold, `#323131`.
- Texto/etiquetas: 10 px Regular, `#323131`.
- Radio de referencia: 0 px.
- El tipo se selecciona según propósito.

Ejemplos:
- evolución temporal → líneas;
- comparación → barras;
- proporción → pie/donut cuando sea apropiado;
- KPI → card;
- detalle → tabla;
- cruce → matriz.

## 4.5 Cards

- Fondo: `#FFFFFF`.
- Radio: 6 px.

## 4.6 Datos relevantes / KPI

- Fondo: `#FFFFFF`.
- Radio: 6 px.
- Nombre: 10 px Regular, `#323131`.
- Valor: 16 px Bold.
- Color del valor puede variar según significado.
- La referencia anterior mostraba icono como `00 px`; este valor queda
  pendiente hasta contar con una especificación exacta.

## 4.7 Tipografía general

- H1: 28–32 px.
- H2: 20–24 px.
- H3: 16–18 px.
- KPI: 14–16 px.
- Etiquetas: 12–14 px.
- Auxiliar: 10–12 px.

## 4.8 Paleta

Base definida:
- Header: `#323131`
- Segmentaciones/valores: `#474747`
- Fondo general: `#F6F6F5`
- Tarjetas: `#FFFFFF`
- Encabezados de tablas: `#B8D4F8`
- Principal: `#1A73E8`
- Secundario: `#8943A7`
- Secundario: `#028AB0`
- Secundario: `#E06806`
- Secundario: `#AE0A33`

Principios:
- mismo concepto → mismo color;
- usar color semántico para estados;
- evitar saturación innecesaria;
- considerar contraste/accesibilidad;
- las familias corporativas pueden contemplar blue, violet, red, orange,
  green y neutrales en escalas 50–900 cuando exista definición aplicable.

## 4.9 Estructura de página

Mesa de trabajo:

Header → filtros → KPI → visualizaciones principales → detalle.

No ubicar visuales arbitrariamente.

## 4.10 Leyendas

Cuando existan:
- posición consistente;
- colores de paleta;
- orden consistente de series;
- nombres claros;
- mismo concepto con mismo color.

## 4.11 Tablas

### Encabezado
- fondo `#B8D4F8`;
- texto oscuro;
- negrilla.

### Cuerpo
- fondo blanco o claro;
- lectura limpia;
- alineación consistente.

### Totales
- destacados;
- negrilla cuando corresponda;
- separación clara.

## 4.12 Navegación

- mismo estilo;
- fuente consistente;
- color consistente;
- tamaños consistentes;
- posición consistente entre páginas equivalentes;
- orden lógico.

## 4.13 Consistencia entre páginas

Elementos repetidos deben conservar:
- posición relativa;
- tamaño;
- estilo;
- color;
- nombre;
- función.

Aplica a Header, título, actualización, filtros, KPI, botones, leyendas,
tablas y elementos recurrentes.

## 4.14 Theme JSON

Puede automatizar propiedades compatibles con Power BI Theme JSON, pero no
reemplaza:
- reglas de negocio;
- layout;
- jerarquía;
- dependencias;
- validaciones.


## Ruta oficial actual del logo

La ruta oficial y vigente del logo corporativo es:

`NIGGA\00_dlc\02_ai_dlc_creacion_modificacion\00_fuentes\Logo_Nebula.png`

Esta ruta reemplaza cualquier ruta anterior registrada en versiones previas
del AI-DLC. El logo debe conservar las reglas de ubicación, tamaño y uso
definidas en este documento.
