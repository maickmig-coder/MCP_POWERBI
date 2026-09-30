# AI-DLC --- Creación, Modificación y Estandarización de BI

## 1. Propósito

Este documento define las reglas que debe seguir un agente de IA para la
**creación, modificación y estandarización visual de reportes Power
BI**.

El objetivo es que los BI nuevos y las modificaciones realizadas sobre
BI existentes mantengan una estructura visual, una jerarquía y un
formato consistente.

### Relación con AI-DLC-CENSO

-   **AI-DLC-CENSO:** identifica y documenta cómo está construido
    actualmente un BI.
-   **AI-DLC-CREACIÓN/MODIFICACIÓN:** define qué debe construirse o
    modificarse.
-   **AI-DLC-FORMATO:** define cómo debe verse y organizarse visualmente
    el BI.

------------------------------------------------------------------------

## 2. Principios generales

1.  Todo BI nuevo debe aplicar el estándar visual definido en este
    documento.
2.  Todo BI existente que sea modificado debe conservar el estándar
    visual, salvo que exista una justificación funcional documentada.
3.  Antes de modificar un BI existente, el agente debe consultar el
    CENSO correspondiente.
4.  Los colores, posiciones, jerarquías, tamaños y estilos definidos en
    este documento deben tratarse como reglas del estándar.
5.  Los elementos particulares de un BI que no estén contemplados en el
    estándar deben ubicarse después de los elementos estandarizados.
6.  Toda modificación debe validarse técnica y visualmente antes de
    considerarse terminada.
7.  El agente no debe improvisar posiciones, colores o estilos cuando
    exista una regla definida.

------------------------------------------------------------------------

## 3. Flujo general de trabajo

### Creación de BI

``` text
Requerimiento
    ↓
Entender requerimiento
    ↓
Diseñar estructura
    ↓
Aplicar estándar visual
    ↓
Construir BI
    ↓
Validar
    ↓
Documentar
    ↓
Entregar
```

### Modificación de BI existente

``` text
Requerimiento
    ↓
Consultar CENSO
    ↓
Identificar estado actual
    ↓
Identificar elementos afectados
    ↓
Diseñar modificación
    ↓
Aplicar modificación
    ↓
Conservar estándar visual
    ↓
Validar
    ↓
Actualizar documentación/CENSO cuando corresponda
```

------------------------------------------------------------------------

## 4. Uso del CENSO como punto de partida

Cuando se modifique un BI existente, el CENSO debe utilizarse como
referencia del estado actual.

El agente debe consultar, como mínimo:

-   Páginas existentes.
-   Visuales existentes.
-   Campos utilizados.
-   Medidas utilizadas.
-   Filtros y segmentaciones.
-   Modelo de datos.
-   Elementos no utilizados.
-   Reglas de negocio.
-   Dependencias.
-   Hallazgos.
-   Propuestas previamente identificadas.
-   Limitaciones conocidas.

El CENSO no autoriza automáticamente una modificación. Los elementos
identificados como hallazgos o propuestas deben validarse según
corresponda.

------------------------------------------------------------------------

# 5. Estándar de Header

El Header debe conservar una estructura uniforme en los BI que utilicen
este estándar.

### 5.1 Header principal

  Elemento   Especificación
  ---------- ----------------
  Tipo       Rectángulo
  Color      `#323131`
  Alto       `155`
  Ancho      `1279`

### 5.2 Título

  Elemento   Especificación
  ---------- -------------------
  Fuente     Segoe
  Color      `#FFFFFF`
  Tamaño     `24`
  Estilo     Negrilla
  Alto       `68`
  Ancho      Depende del texto

El título debe identificar claramente el BI, módulo o sección
correspondiente.

### 5.3 Separador

  Elemento         Especificación
  ---------------- ----------------
  Tipo             Forma línea
  Tipo de remate   Remate plano
  Borde            `#FFFFFF`

### 5.4 Última actualización

  Elemento   Especificación
  ---------- ----------------
  Color      `#FFFFFF`
  Tamaño     `12`
  Estilo     Negrilla
  Alto       `68`
  Ancho      `226`

Cuando el BI disponga de información de actualización, debe conservar
una posición y tratamiento visual consistente dentro del Header.

------------------------------------------------------------------------

### 5.5 Logo Nebula

El logo corporativo **Nebula** debe estar presente en el Header de los BI que utilicen este estándar.

| Elemento | Especificación |
|---|---|
| Archivo fuente | `C:\dev\NIGGA\00_dlc\02_ai_dlc_creacion_modificacion\01_fuentes\Logo_Nebula.png` |
| Ubicación | Parte superior derecha del Header |
| Posición | Debe conservarse de forma consistente con el diseño de referencia |
| Función | Identificación visual corporativa |

### Regla obligatoria del logo

El logo **Nebula debe permanecer siempre en la misma zona del Header: la esquina superior derecha**, siguiendo la posición visual mostrada en el BI de referencia.

El agente **no debe mover el logo, cambiarlo de lado ni ubicarlo en otra zona del Header** salvo que exista una instrucción explícita y documentada que indique lo contrario.

El archivo fuente debe utilizarse desde:

`C:\dev\NIGGA\00_dlc\02_ai_dlc_creacion_modificacion\01_fuentes\Logo_Nebula.png`

# 6. Estándar de segmentaciones

  Elemento           Especificación
  ------------------ ----------------
  Tipo               Desplegable
  Alto               `69`
  Ancho              `135`
  Fondo              `#474747`
  Borde              `#323131`
  Esquinas           Redondeadas
  Color de fuente    `#FFFFFF`
  Fondo de valores   `#474747`

Las segmentaciones deben conservar el mismo estilo dentro de las páginas
que utilicen el estándar.

------------------------------------------------------------------------

# 7. Jerarquía estándar de segmentaciones

La jerarquía principal de filtros es:

1.  **Año**
2.  **Mes**
3.  **Campaña**
4.  **Categoría**
5.  **Centro**
6.  **Tipificación**
7.  **Fuente**
8.  **Gestión Leads**

### Regla

Si una segmentación de la jerarquía estándar no aplica al BI, se omite.

Las segmentaciones adicionales que no pertenezcan a la jerarquía
estándar se colocan **después de las segmentaciones estándar**.

Ejemplo:

``` text
Año
Mes
Campaña
Categoría
Centro
Tipificación
Fuente
Gestión Leads
Asesor
Marca
Sucursal
```

La regla general es:

``` text
Filtros estándar
        ↓
Filtros adicionales
```

------------------------------------------------------------------------

# 8. Regla de títulos de segmentaciones

El título de una segmentación debe corresponder al campo que realmente
está utilizando.

Ejemplo correcto:

``` text
Campo utilizado: Campaña
Título: Campaña
```

No:

``` text
Campo utilizado: Campaña
Título: Año
```

La identificación del campo debe validarse contra la configuración real
del visual.

------------------------------------------------------------------------

# 9. Estándar de botones

  Elemento           Especificación
  ------------------ ----------------
  Tipo               Rectángulo
  Esquinas           Redondeadas
  Radio de esquina   `4`
  Color de fuente    `#1A73E8`
  Fondo              `#FFFFFF`

Los botones de navegación deben mantener el mismo estilo, posición y
tamaño cuando cumplan la misma función.

------------------------------------------------------------------------

# 10. Estructura visual de la página

``` text
┌─────────────────────────────────────────────────────────┐
│                         HEADER                          │
├─────────────────────────────────────────────────────────┤
│ Año │ Mes │ Campaña │ Categoría │ Centro │ ...         │
├─────────────────────────────────────────────────────────┤
│                    KPIs / TARJETAS                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│                  VISUALES PRINCIPALES                   │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                    TABLAS / DETALLE                     │
└─────────────────────────────────────────────────────────┘
```

La estructura exacta puede adaptarse a las necesidades funcionales, pero
debe conservar la jerarquía visual general.

------------------------------------------------------------------------

# 11. Estándar de colores

  Uso                        Color            HEX
  -------------------------- ---------------- -----------
  Header                     Gris carbón      `#323131`
  Segmentaciones / valores   Gris oscuro      `#474747`
  Fondo general              Gris muy claro   `#F6F6F5`
  Tarjetas                   Blanco           `#FFFFFF`
  Encabezados de tablas      Azul claro       `#B8D4F8`
  Color principal            Azul             `#1A73E8`
  Color secundario           Morado           `#8943A7`
  Color secundario           Cian             `#028AB0`
  Color secundario           Naranja          `#E06806`
  Color secundario           Rojo/Borgoña     `#AE0A33`

### Regla de consistencia

Cuando un mismo concepto aparezca en diferentes visuales, debe conservar
el mismo color siempre que sea funcionalmente posible.

Ejemplo:

``` text
Leads             → Azul
Leads Gestionados → Morado
```

------------------------------------------------------------------------

# 12. Estándar de gráficos

  Necesidad                   Visual estándar
  --------------------------- --------------------------------
  Evolución temporal          Gráfico de líneas
  Comparación de categorías   Gráfico de barras
  Distribución proporcional   Pie/Donut cuando sea apropiado
  Indicador/KPI               Card
  Detalle de registros        Tabla
  Cruce de categorías         Matriz/Pivot
  Selección de valores        Segmentación/Slicer

La selección puede variar cuando el requerimiento funcional lo
justifique.

------------------------------------------------------------------------

# 13. Estándar de tablas

### Encabezado

-   Fondo: `#B8D4F8`
-   Texto: oscuro
-   Peso: negrilla

### Cuerpo

-   Fondo blanco o claro.
-   Lectura limpia.
-   Alineación consistente.

### Totales

-   Destacados visualmente.
-   Negrilla cuando corresponda.
-   Separación clara respecto al cuerpo.

Las tablas que cumplen la misma función deben utilizar el mismo
tratamiento visual.

------------------------------------------------------------------------

# 14. Estándar de tarjetas KPI

Las tarjetas deben mantener:

-   Dimensiones homogéneas dentro de una misma página.
-   Alineación consistente.
-   Título centrado.
-   Valor principal destacado.
-   Fondo blanco cuando corresponda.
-   Separación uniforme.

Ejemplo:

``` text
┌─────────────────────────┐
│       Total Leads       │
│                         │
│         91,317          │
└─────────────────────────┘
```

------------------------------------------------------------------------

# 15. Estándar de leyendas

Cuando un visual utilice leyenda:

1.  La posición debe ser consistente.
2.  Los colores deben corresponder a la paleta definida.
3.  El orden de las series debe mantenerse cuando representen los mismos
    conceptos.
4.  Los nombres deben ser claros y consistentes.
5.  No deben utilizarse colores diferentes para un mismo concepto sin
    justificación.

------------------------------------------------------------------------

# 16. Estándar de navegación

Los botones de navegación deben mantener:

-   Mismo estilo.
-   Mismo tratamiento de fuente.
-   Mismo color.
-   Tamaños consistentes.
-   Posiciones consistentes entre páginas equivalentes.
-   Orden lógico y uniforme.

------------------------------------------------------------------------

# 17. Regla de consistencia entre páginas

Cuando un elemento se repita en varias páginas del mismo BI, debe
mantener:

-   Misma posición relativa.
-   Mismo tamaño.
-   Mismo estilo.
-   Mismo color.
-   Mismo nombre.
-   Misma función.

Esto aplica especialmente a:

-   Header.
-   Título.
-   Última actualización.
-   Segmentaciones.
-   KPIs.
-   Botones.
-   Leyendas.
-   Tablas.
-   Elementos gráficos recurrentes.

------------------------------------------------------------------------

# 18. Creación de un BI nuevo

Antes de construir un BI nuevo, el agente debe definir:

-   Nombre.
-   Objetivo.
-   Páginas necesarias.
-   KPIs.
-   Filtros.
-   Visuales.
-   Jerarquía de filtros.
-   Paleta.
-   Estructura del Header.
-   Navegación.
-   Tablas.
-   Gráficos.
-   Reglas de negocio.

El estándar visual debe aplicarse desde el inicio.

------------------------------------------------------------------------

# 19. Modificación de un BI existente

Cuando se solicite una modificación:

1.  Consultar el CENSO.
2.  Identificar el elemento que se debe modificar.
3.  Identificar dependencias.
4.  Determinar el impacto.
5.  Aplicar el cambio.
6.  Mantener el estándar visual.
7.  Revisar elementos relacionados.
8.  Validar visualmente.
9.  Validar técnicamente.
10. Documentar el resultado.

Una modificación no debe limitarse al visual directamente mencionado si
el cambio puede afectar medidas, campos, filtros, relaciones, páginas u
otros elementos dependientes.

------------------------------------------------------------------------

# 20. Validación visual

-   [ ] Header con dimensiones y color estándar.
-   [ ] Título con fuente, tamaño, color y negrilla estándar.
-   [ ] Separador correctamente configurado.
-   [ ] Última actualización con formato estándar.
-   [ ] Segmentaciones con dimensiones y colores estándar.
-   [ ] Segmentaciones ubicadas en la jerarquía correcta.
-   [ ] Segmentaciones adicionales después de las estándar.
-   [ ] Botones con formato estándar.
-   [ ] KPIs alineados y homogéneos.
-   [ ] Tablas con encabezados estándar.
-   [ ] Gráficos adecuados a su propósito.
-   [ ] Colores consistentes.
-   [ ] Leyendas consistentes.
-   [ ] Navegación consistente.
-   [ ] Elementos repetidos conservan el mismo formato.
-   [ ] No existen títulos incorrectos respecto al campo utilizado.

------------------------------------------------------------------------

# 21. Validación técnica

-   [ ] Estructura del proyecto.
-   [ ] Archivos TMDL.
-   [ ] Archivos PBIR.
-   [ ] JSON.
-   [ ] Referencias internas.
-   [ ] Extensiones.
-   [ ] Sintaxis.
-   [ ] Codificación.
-   [ ] Compatibilidad con Power BI.
-   [ ] Archivos UTF-8 cuando corresponda.
-   [ ] Ausencia de BOM cuando Power BI requiera UTF-8 sin BOM.
-   [ ] Integridad del proyecto.
-   [ ] Elementos modificados correctamente.
-   [ ] Dependencias afectadas revisadas.

------------------------------------------------------------------------

# 22. Error conocido: UTF-8 con BOM

## Problema

Durante la generación de archivos del proyecto Power BI puede ocurrir
que archivos creados mediante determinadas instrucciones de PowerShell
queden en **UTF-8 con BOM**.

Power BI puede requerir archivos en **UTF-8 sin BOM**.

## Regla preventiva

No asumir que:

``` text
Set-Content -Encoding UTF8
```

garantiza UTF-8 sin BOM.

Cuando se generen o modifiquen archivos de texto del proyecto, se debe
validar su codificación.

## Control

El agente debe:

1.  Identificar los archivos creados o modificados.
2.  Identificar el método utilizado para generarlos.
3.  Validar la codificación.
4.  Comprobar si existe BOM.
5.  Corregirlo cuando corresponda.
6.  Volver a validar antes de finalizar.

------------------------------------------------------------------------

# 23. Errores y lecciones aprendidas

Cada error encontrado durante la creación o modificación debe
convertirse en conocimiento reutilizable.

``` text
Error
  ↓
Causa
  ↓
Impacto
  ↓
Solución
  ↓
Regla preventiva
  ↓
Validación automática
```

El objetivo es que un error corregido no vuelva a repetirse en futuras
ejecuciones del AI-DLC.

------------------------------------------------------------------------

# 24. Validación final

Antes de considerar terminado un BI nuevo o una modificación, el agente
debe comprobar:

1.  ¿Entendí correctamente el requerimiento?
2.  ¿Consulté el CENSO cuando el BI ya existía?
3.  ¿Identifiqué los elementos afectados?
4.  ¿Apliqué el estándar visual?
5.  ¿Respeté la jerarquía de filtros?
6.  ¿Mantuve los colores estandarizados?
7.  ¿Mantuve la estructura del Header?
8.  ¿Mantuve consistencia entre páginas?
9.  ¿Validé los visuales?
10. ¿Validé técnicamente los archivos?
11. ¿Revisé codificación y BOM?
12. ¿Documenté errores o lecciones aprendidas?
13. ¿El resultado final cumple el requerimiento?

------------------------------------------------------------------------

# 25. Principio general

> **Crear no significa improvisar. Modificar no significa alterar sin
> revisar. Cada cambio debe respetar el estándar, validar su impacto y
> dejar el BI en un estado técnicamente y visualmente consistente.**

> **El AI-DLC utiliza el CENSO como fuente del estado actual del BI y
> este estándar como referencia para su creación, modificación y
> presentación visual.**
