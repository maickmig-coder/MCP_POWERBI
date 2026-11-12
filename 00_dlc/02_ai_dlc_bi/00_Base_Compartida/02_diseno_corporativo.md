# 4. DISEÑO CORPORATIVO

Versión del estándar: V10 (decisiones del 2026-11-09).
Toda medida está expresada en px, como en el mockup corporativo. Ver 4.16 sobre la conversión a pt.

**Aplicación por proceso:** en **Creación** el estándar se aplica completo. En **Modificación** se conserva el diseño
existente y el estándar se aplica a lo que el cambio crea o rediseña con aprobación. En **Depuración** no se rediseña:
el estándar solo sirve para detectar inconsistencias que afecten la integridad o la lectura (ver
`03_Depuracion/01_Reglas_del_Proceso/controles_reforzados_depuracion.md`).

## 4.0 Lienzo y mesa de trabajo

- Página: 1280 × 720, ajuste `FitToPage`.
- Fondo de página: `#F6F6F5` (token `neutral-bg`).
- Fondo de secciones/contenedores: `#FFFFFF` (token `neutral-surface`).
- Orden vertical obligatorio:
  Header (con segmentaciones) → fila de KPI / datos relevantes → visualizaciones principales → detalle.
- Composición de referencia del mockup:
  - fila de KPI: hasta 6 tarjetas del mismo tamaño;
  - visualizaciones principales: 3 contenedores iguales;
  - detalle: 2 contenedores (tabla/matriz u otro detalle).
- La grilla de Power BI del mockup reparte el alto en tres zonas: header, cuerpo y detalle.
  Se conserva la proporción entre páginas equivalentes.
- No ubicar visuales arbitrariamente. Si el BI requiere otra composición, registrarla como decisión aprobada.

## 4.1 Header

### Contenedor
- Tipo: rectángulo.
- Color: `#323131`.
- Alto: 155. Ancho de referencia: 1279 (todo el ancho del lienzo).
- La altura definida debe conservarse.
- El header contiene: título, separador, última actualización, logo y la fila de segmentaciones (4.2).

### Título
- Fuente: Segoe UI, negrilla, 24 px, `#FFFFFF`.
- Alto: 68. Ancho: depende del texto.
- Debe identificar claramente BI, módulo o sección.

### Separador
- Forma: línea vertical, remate plano.
- Borde: `#FFFFFF`.
- Ubicación: entre el título y el bloque de última actualización.

### Última actualización (dos líneas)
- Etiqueta "Última actualización:": Segoe UI regular, 10 px, `#FFFFFF`.
- Valor (fecha y hora): Segoe UI negrilla, 12 px, `#FFFFFF`.
- Bloque: alto 68, ancho 226.
- El valor proviene de la tabla auxiliar de fecha de actualización del modelo
  (patrón de referencia: `DateTimeZone.SwitchZone(DateTimeZone.LocalNow(), -5, 0)`; ver tablas auxiliares del diccionario de datos).

### Logo
- Se usa **únicamente el logo Nebula**, como en el mockup corporativo.
- Fuente oficial: `MCP_POWERBI\00_dlc\02_ai_dlc_bi\00_fuentes\Logo_Nebula.png`
- Ubicación: parte superior derecha del header.
- No agregar logos de marca (CasaToro, Motorysa u otros) en un BI nuevo, salvo una excepción aprobada y registrada.
- No sustituirlo ni moverlo de lado. Si la fuente no está disponible, informar y solicitar la fuente o autorización.

## 4.2 Segmentaciones (estilo oscuro — vigente)

Estilo decidido: segmentación tipo **desplegable oscuro**, dentro del header.

| Propiedad | Valor |
|---|---|
| Tipo | Desplegable (dropdown) |
| Alto | 69 |
| Ancho | 135 (ajustable solo si el número de filtros no cabe en el ancho del header; registrar la excepción) |
| Fondo del contenedor | `#474747` |
| Borde | `#323131` |
| Esquinas | Redondeadas (radio exacto: pendiente, ver 4.17) |
| Encabezado (nombre del campo) | Segoe UI negrilla, 10 px, `#FFFFFF` |
| Texto del selector y de los valores | Segoe UI regular, 12 px, `#FFFFFF` |
| Fondo de la lista de valores | `#474747` |

Sustituye la versión anterior de selector blanco (fondo `#FFFFFF`, texto `#323131`, borde `#CDCDD1`).
Esa variante no debe usarse en versiones oficiales.

### Jerarquía de orden

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
- el título debe corresponder al campo real;
- no repetir el mismo campo en dos segmentaciones de la misma página.

Nota: esta jerarquía proviene del dominio Leads. Para otros dominios ver la decisión pendiente en 4.17.

## 4.3 Botones

Regla común a todas las variantes: texto Segoe UI negrilla 12 px; **radio 6 px**; azul de acción `#1A73E8`.
El radio de 4 px queda descartado y no debe aparecer en ninguna versión oficial.

| Variante | Fondo | Borde | Texto / ícono | Uso |
|---|---|---|---|---|
| Primario | `#FFFFFF` | `#1A73E8` | `#1A73E8` | Acción principal dentro del cuerpo (ej.: "Por convertir") |
| Menú | `#1A73E8` | — | `#FFFFFF` | Navegación entre páginas o secciones |
| Texto (enlace) | Sin relleno | — | `#1A73E8` | Acción secundaria de bajo peso visual |

Botón de solo ícono: misma variante y colores que su versión con texto (ej.: primario = ícono `#1A73E8` sobre `#FFFFFF` con borde `#1A73E8`; menú = ícono `#FFFFFF` sobre `#1A73E8`).

Nota de control: la anotación del mockup que indica texto `#FFFFFF` en el botón primario es un error del mockup;
el dibujo y los tableros de referencia muestran texto azul sobre blanco.

## 4.4 Gráficos

| Propiedad | Valor |
|---|---|
| Fondo | `#FFFFFF` |
| Esquinas | 0 px |
| Título | Segoe UI negrilla, 14 px, `#323131` |
| Espacio entre título y área del gráfico | 10 px |
| Ejes, categorías y leyendas | Segoe UI regular, 10 px, `#323131` |
| Etiquetas de datos | Segoe UI regular, 10 px, texto `#323131`, fondo `#F5F5FA` |

El tipo se selecciona según propósito:
- evolución temporal → líneas;
- comparación → barras;
- proporción → pie/donut cuando sea apropiado (pocas categorías);
- KPI → tarjeta;
- detalle → tabla;
- cruce → matriz.

## 4.5 Cards (tarjeta con imagen)

- Fondo `#FFFFFF`; radio 6 px.
- Composición: imagen o ilustración arriba (con esquinas redondeadas) y botón de acción abajo (variante menú, 4.3).

## 4.6 Datos relevantes / KPI

| Propiedad | Valor |
|---|---|
| Fondo | `#FFFFFF` |
| Radio | 6 px |
| Nombre del dato | Segoe UI regular, 10 px, `#323131` |
| Valor | Segoe UI negrilla, 16 px, `#323131` por defecto |
| Ícono / ilustración | A la izquierda; tamaño pendiente (el mockup indica `00 px`, ver 4.17) |

El color del valor puede cambiar según lo que comunique:
- neutro → `#323131`;
- informativo → `#1A73E8`;
- positivo / negativo → tokens de feedback (4.9), respetando el contraste de 4.12.

## 4.7 Tipografía general

Familia única: Segoe UI (en el tema: `'Segoe UI', wf_segoe-ui_normal, helvetica, arial, sans-serif`).

| Nivel | Tamaño | Uso |
|---|---|---|
| H1 | 28–32 px | Título principal del tablero o página |
| H2 | 20–24 px | Secciones importantes (el título del header usa 24 px) |
| H3 | 16–18 px | Encabezados de gráficos o tarjetas cuando no aplica la regla de 4.4 |
| KPI | 14–16 px | Valores clave (el estándar de 4.6 usa 16 px) |
| Etiquetas | 12–14 px | Descripciones, leyendas, etiquetas |
| Auxiliar | 10–12 px | Notas, fuentes de datos, información de soporte |

Cuando un componente tiene una especificación propia (4.1–4.6), esa especificación prevalece sobre la tabla general.

## 4.8 Paleta de datos (dataColors del tema)

Orden obligatorio, igual al tema `Tema_1_BI_Nebula` usado en producción:

| Posición | Token | Hex | Familia |
|---:|---|---|---|
| 1 | `blue-500` | `#1A73E8` | Principal |
| 2 | `violet-500` | `#8943A7` | Secundario |
| 3 | `red-500` | `#AE0A33` | Secundario |
| 4 | `teal-500` | `#028AB0` | Secundario |
| 5 | `orange-500` | `#E06806` | Secundario |
| 6 | `blue-500` | `#1A73E8` | Repite posición 1 (ver 4.17) |
| 7 | `violet-500` | `#8943A7` | Repite posición 2 (ver 4.17) |
| 8 | `red-500` | `#AE0A33` | Repite posición 3 (ver 4.17) |

Nota de nombres: el mockup llama "blue" tanto a `#1A73E8` como a `#028AB0`.
En este estándar la segunda familia se llama **teal** para evitar confusiones.

### Escalas 50–900 (tonos y variaciones)

Usar tonos de una misma familia para niveles o series de un mismo concepto, en lugar de mezclar familias.

| Tono | blue | violet | red | teal | orange |
|---|---|---|---|---|---|
| 50 | `#E8F1FD` | `#F3ECF6` | `#F7E7EB` | `#E6F3F7` | `#FCF0E6` |
| 100 | `#B8D4F8` | `#DAC5E4` | `#E6B3C0` | `#B1DBE7` | `#F5D0B2` |
| 200 | `#96BFF4` | `#C9A9D7` | `#DA8EA1` | `#8BC9DB` | `#F1BA8C` |
| 300 | `#66A1F0` | `#B081C4` | `#C95B76` | `#55B1CA` | `#EA9A58` |
| 400 | `#488FED` | `#A169B9` | `#BE3B5C` | `#35A1C0` | `#E68638` |
| 500 | `#1A73E8` | `#8943A7` | `#AE0A33` | `#028AB0` | `#E06806` |
| 600 | `#1869D3` | `#7D3D98` | `#9E092E` | `#027EA0` | `#CC5F05` |
| 700 | `#1252A5` | `#613077` | `#7C0724` | `#01627D` | `#9F4A04` |
| 800 | `#0E3F80` | `#4B255C` | `#60061C` | `#014C61` | `#7B3903` |
| 900 | `#0B3061` | `#3A1C46` | `#490415` | `#013A4A` | `#5E2C03` |

## 4.9 Colores de feedback (estado)

Reservados para estados, alertas y KPI críticos; no usarlos como colores de serie.

| Tono | success (green) | error (red-feedback) |
|---|---|---|
| 50 | `#F0F8ED` | `#FFEDED` |
| 100 | `#D1EAC7` | `#FFC8C8` |
| 200 | `#BADFAC` | `#FFAEAE` |
| 300 | `#9BD186` | `#FF8888` |
| 400 | `#88C86F` | `#FF7171` |
| 500 | `#6ABA4B` | `#FF4E4E` |
| 600 | `#60A944` | `#E84747` |
| 700 | `#4B8435` | `#B53737` |
| 800 | `#3A6629` | `#8C2B2B` |
| 900 | `#2D4E20` | `#6B2121` |

Nota de nombres: el mockup llama "orange" a la familia de error; en este estándar se llama **red-feedback**
para no confundirla con `orange` (4.8).

Daltonismo: no depender solo de rojo/verde para diferenciar estados; acompañar con ícono, signo (+/−) o texto.

## 4.10 Neutrales y colores secundarios

| Token | Hex | Uso | Nivel en el tema (Advanced) |
|---|---|---|---|
| `neutral-text` | `#323131` | Texto principal, títulos de gráficos, header | Primer nivel |
| `neutral-text-3` | `#898C93` | Texto de tercer nivel, anotaciones | Tercer nivel |
| `neutral-line` | `#CDCDD1` | Líneas de división, bordes suaves, cuadrícula | Cuarto nivel |
| `neutral-dark-bg` | `#474747` | Fondo de segmentaciones | — |
| `neutral-bg` | `#F6F6F5` | Fondo de página | Fondo secundario |
| `neutral-surface` | `#FFFFFF` | Fondo de visuales, tarjetas y secciones | Fondo |
| `table-header` | `#B8D4F8` | Encabezado de tablas (= `blue-100`) | — |
| `label-bg` | `#F5F5FA` | Fondo de etiquetas de datos | — |

## 4.11 Principios de uso del color

Basados en la guía de Microsoft (Fluent) adoptada por la compañía. Los hex de ejemplo de esa guía
(`#0078D4`, `#107C10`, `#F7630C`, `#16C60C`, `#D83B01`, `#FFB900`, `#F3F3F3`, `#333333`) **no** son colores corporativos y no se usan.

- Entre 5 y 8 colores activos por tablero, organizados en:
  - primario (1–2): `blue-500` y una variación de su escala;
  - secundarios (2–3): `violet`, `red`, `teal`, `orange`;
  - estado (feedback): `success` y `error` (ver 4.17 sobre advertencia);
  - neutros (1–2): 4.10.
- Mismo concepto → mismo color en todo el tablero.
- Los colores de estado se reservan para métricas críticas, alertas y mensajes clave.
- Para series de un mismo concepto, usar tonos de una misma familia (claro → oscuro).
- Evitar el exceso de colores saturados.

## 4.12 Contraste y accesibilidad

- Texto normal: contraste mínimo 4.5:1 con su fondo.
- Texto grande (≥ 24 px regular o ≥ 18.66 px negrilla): mínimo 3:1.
- El valor de un KPI (16 px negrilla) **no** es texto grande: requiere 4.5:1.

Contraste sobre `#FFFFFF` de los colores 500, tomado del mockup:

| Token | Contraste | Texto normal | Solo gráficos / texto grande |
|---|---:|---|---|
| `blue-500` | 4.51 | Cumple | Cumple |
| `violet-500` | 6.13 | Cumple | Cumple |
| `red-500` | 7.26 | Cumple | Cumple |
| `teal-500` | 3.99 | No cumple | Cumple |
| `orange-500` | 3.41 | No cumple | Cumple |
| `success-500` | 2.40 | No cumple | No cumple |
| `red-feedback-500` | 3.25 | No cumple | Cumple |

Tonos que sí cumplen como texto sobre blanco: `teal-600` (4.67), `orange-700` (6.08),
`success-700` (4.52), `red-feedback-700` (5.89).
Cuál tono usar en los valores de KPI es una decisión pendiente (4.17). Mientras no se decida, la IA debe
advertir el incumplimiento de contraste cuando un texto use un color marcado "No cumple".

## 4.13 Leyendas, tablas y navegación

### Leyendas
- posición consistente; colores de paleta; orden de series consistente; nombres claros.

### Tablas
- Encabezado: fondo `#B8D4F8`, texto `#323131`, negrilla.
- Cuerpo: fondo `#FFFFFF`, líneas `#CDCDD1`, alineación consistente (números a la derecha).
- Totales: negrilla y separación clara.

### Navegación
- Botones variante menú (4.3); mismo estilo, tamaño y posición en páginas equivalentes; orden lógico.

## 4.14 Consistencia entre páginas

Los elementos repetidos conservan posición relativa, tamaño, estilo, color, nombre y función:
header, título, última actualización, logo, segmentaciones, KPI, botones, leyendas, tablas y elementos recurrentes.

## 4.15 Theme JSON

- Tema base corporativo: `Tema_1_BI_Nebula` (registrado en los BI existentes; ver sección «Tema» de sus censos).
  Para un BI nuevo, reutilizar ese archivo como punto de partida y ajustar solo lo que este estándar cambie.
- Valores mínimos que debe contener el tema:
  - `dataColors` en el orden de 4.8;
  - `foreground` `#323131`, `foregroundNeutralTertiary` `#898C93`, `background` `#FFFFFF`,
    `backgroundLight` `#F6F6F5`, `tableAccent` `#B8D4F8`;
  - `good` `#4B8435`*, `bad` `#B53737`* (*sujetos a la decisión 4.17-4);
  - familia tipográfica Segoe UI;
  - fondo de página `#F6F6F5`; fondo de visuales `#FFFFFF`.
- Las capturas de "Customize theme" del material de referencia son de un tutorial externo: sus valores
  (radio 5 px, verde del panel de filtros, etc.) **no** son estándar corporativo.
- El tema no reemplaza las reglas de layout, jerarquía, dependencias ni validaciones.

## 4.16 Unidades px y pt

El mockup usa px; Power BI formatea texto en pt (1 pt = 1.333 px a 96 ppp).
Equivalencias de referencia: 10 px ≈ 7.5 pt, 12 px = 9 pt, 14 px ≈ 10.5 pt, 16 px = 12 pt, 24 px = 18 pt.
La regla de aplicación está pendiente (4.17-1). Hasta decidirla, la IA debe declarar en el registro de construcción
qué interpretación aplicó.

## 4.17 Decisiones pendientes

| # | Tema | Opciones | Estado |
|---:|---|---|---|
| 1 | Unidades | Aplicar el número tal cual en pt / convertir px → pt | Pendiente |
| 2 | dataColors 6–8 repiten 1–3 | Mantener / sustituir por tonos 300 o 700 de las familias | Pendiente |
| 3 | Color de advertencia (estado intermedio) | `orange-500` / otra familia / no usar | Pendiente |
| 4 | Tono para valores KPI de feedback | 500 (no cumple contraste) / 700 (cumple) | Pendiente |
| 5 | Jerarquía de filtros fuera de Leads | Genérica (tiempo → organización → negocio → específicos) / una por dominio | Pendiente |
| 6 | Radio de esquinas de segmentaciones | Valor exacto | Pendiente |
| 7 | Tamaño del ícono en Datos relevantes | Valor exacto | Pendiente |

Mientras una decisión esté pendiente, la IA no la resuelve por su cuenta: la pregunta en el levantamiento
o registra el supuesto aplicado.

## Ruta oficial actual del logo

`MCP_POWERBI\00_dlc\02_ai_dlc_bi\00_fuentes\Logo_Nebula.png`

Esta ruta reemplaza cualquier ruta anterior registrada en versiones previas del AI-DLC.
