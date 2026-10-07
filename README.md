# Nebula BI — Repositorio de Business Intelligence y AI-DLC

Repositorio central del ecosistema de Business Intelligence de **Nebula Data Lake**.
Reúne la metodología de trabajo asistido por IA (**AI-DLC**), los tableros de
Power BI, los censos técnico-funcionales y el diccionario de datos del data lake.

## ¿Qué contiene este repositorio?

- **Metodología AI-DLC** para censar, crear, modificar y depurar tableros de BI
  de forma trazable y repetible.
- **Tableros Power BI** versionados (originales y versiones de trabajo).
- **Censos** técnico-funcionales de los tableros existentes.
- **Diccionario de datos** del data lake generado desde AWS Glue Data Catalog.

## Estructura

```text
NIGGA/
│
├── README.md                     ← este archivo
├── diccionario-datos.md          ← diccionario de datos del Nebula Data Lake
│
├── 00_dlc/                       ← metodología AI-DLC
│   ├── 00_originales/            ← paquetes .zip históricos de la metodología
│   ├── 01_ai-dlc-censo/          ← ritual de CENSO (análisis sin modificar BI)
│   └── 02_ai_dlc_creacion_modificacion/
│                                 ← reglas de creación, modificación y depuración
│
├── 01_bi/                        ← tableros Power BI
│   └── 01_versiones/
│       ├── 00_original/          ← tableros originales + trazabilidad
│       └── 01_kiro/              ← versiones de trabajo
│
└── 02_censo/                     ← censos de tableros
    ├── GC - Flotillas.md
    └── GC - Leads MG.md
```

## Metodología AI-DLC

El proyecto trabaja con un ciclo de desarrollo asistido por IA (AI-DLC) dividido
en dos grandes rituales complementarios:

| Ritual | Pregunta que responde | Carpeta |
|--------|-----------------------|---------|
| **CENSO** | ¿Cómo está construido actualmente el BI? | `00_dlc/01_ai-dlc-censo` |
| **Creación / Modificación / Depuración** | ¿Qué debemos construir o cambiar y cómo? | `00_dlc/02_ai_dlc_creacion_modificacion` |

### CENSO
Define un ritual repetible para analizar cualquier BI **sin modificarlo** y
producir un censo estructurado: estructura técnica, finalidad funcional,
elementos utilizados y no utilizados, reglas de negocio, dependencias, vacíos de
información y propuestas de revisión basadas en evidencia.

Toda afirmación se clasifica como **Encontrado** (evidencia directa),
**Inferido** (inferencia razonable) o **Desconocido** (sin información suficiente).

### Creación, Modificación y Depuración
Consolida las reglas para los tres tipos de trabajo sobre tableros:

- **Creación:** BI que no existía previamente.
- **Modificación:** cambio funcional o técnico sobre un BI existente.
- **Depuración y Mejora:** revisión de integridad, datos, modelo, fuentes,
  consultas, DAX, rendimiento y elementos innecesarios.

Principios clave:

- No asumir información que pueda cambiar el resultado; preguntar cuando falte.
- Diferenciar solicitud del usuario, obligación técnica y propuesta de IA; la
  decisión final es del analista.
- Conservar la estética actual salvo solicitud, regla corporativa o necesidad
  técnica justificada.
- No modificar elementos fuera del alcance aprobado.
- Mantener trazabilidad de original, cambios y validaciones en todo momento.

## Trazabilidad de tableros

Cada tablero mantiene un único `README.md` histórico dentro de su carpeta, que
acumula responsable, solicitante, fechas, tipo de trabajo, versiones, cambios,
decisiones, validaciones, alertas y pendientes. Si un tablero se modifica varias
veces no se crea un README nuevo: se continúa la misma historia.

Existe además un registro central en:

```text
01_bi/01_versiones/00_original/REGISTRO_CONTROL_TABLEROS.md
```

El control de personas se simplifica a dos correos: quien trabaja el tablero y
quien lo solicita.

## Diccionario de datos

`diccionario-datos.md` documenta el **Nebula Data Lake** organizado por capas:

- **🥉 Bronce (raw / ingesta):** datos extraídos de sistemas operacionales
  (MySQL, SQL Server, Redshift) sin transformación de negocio, más la sub-capa de
  referencia/maestras.
- **🥈 Plata / Materialized:** datos con lógica de negocio aplicada
  (normalización, joins, agregaciones), consumidos desde Athena y Power BI.

Se genera automáticamente desde el AWS Glue Data Catalog e incluye el detalle de
schemas, tablas y columnas por capa.

## Flujo de trabajo recomendado

1. **Censar** el tablero con el ritual de `00_dlc/01_ai-dlc-censo` para entender
   cómo está construido.
2. **Planear** la creación o el cambio siguiendo las reglas de
   `00_dlc/02_ai_dlc_creacion_modificacion`.
3. **Trabajar** sobre una versión de trabajo en `01_bi/01_versiones/01_kiro`,
   nunca sobre el original.
4. **Validar** el BI completo (modelo, fuentes, DAX, visuales, integridad,
   rendimiento) antes de declararlo listo.
5. **Registrar** responsable, cambios y decisiones en el README del tablero y en
   el registro central.
