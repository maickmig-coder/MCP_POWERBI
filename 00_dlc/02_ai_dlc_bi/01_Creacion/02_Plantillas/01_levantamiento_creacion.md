# PLANTILLA — LEVANTAMIENTO DE BI NUEVO

Completar lo conocido; dejar explícito `Pendiente`, `No aplica` o `Por confirmar` cuando corresponda. No inventar respuestas.

## 1. Identificación y trazabilidad
- Nombre exacto del BI:
- Correo de quien trabaja/modifica:
- Correo de quien solicita/es dueño:
- Fecha de inicio:
- Estado inicial:
- CENSO del BI: `No aplica` para BI nuevo / `Reclasificar solicitud` si parte de un BI existente.
- Diccionario de datos usado: `diccionario_id` / `No vigente — solicitado` (obligatorio; ver sección 5).
- Ruta README histórico: `MCP_POWERBI\02_censo\[Nombre exacto BI]\README.md`
- Ruta de trabajo Kiro: `MCP_POWERBI\01_bi\01_versiones\01_kiro\[Nombre exacto BI]\`

## 2. Contexto y finalidad
- ¿De qué trata el BI?
- ¿Qué problema/necesidad busca resolver?
- ¿Cuál es la finalidad?
- ¿Qué decisiones debe apoyar?
- ¿Qué preguntas debe responder?
- Público objetivo y perfiles de uso:
- Alcance incluido:
- Fuera de alcance:
- Criterios de aceptación:
- Restricciones y supuestos pendientes:

## 3. KPIs y reglas de negocio
- ¿El usuario define los KPIs o desea propuestas de IA?: `Usuario define / Desea propuestas IA / Pendiente`

| KPI | Qué mide | Fórmula/lógica | Campos | Granularidad | Fuente | Filtros/periodo | Criterio de validación | Decisión |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

- Reglas/excepciones de negocio:
- Definición de periodos/fechas:
- Tratamiento de nulos/duplicados:
- Moneda/zona horaria/unidades, cuando aplique:
- Fuente de verdad y método de conciliación:

## 4. Visualizaciones y páginas
- ¿El usuario define los gráficos o desea propuestas de IA?: `Usuario define / Desea propuestas IA / Pendiente`

| Página | Propósito | Pregunta que responde | Visual | Campos/medidas | Filtros | Ubicación sugerida | Decisión |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

- Cantidad de páginas:
- Requisitos explícitos de layout:
- Navegación:
- Jerarquía de filtros corporativos presentes:
- Filtros adicionales:
- Botones, bookmarks y estados alternativos:
- Drill-down / drill-through:
- Tooltips:
- Exportaciones:
- Requisitos de accesibilidad/lectura:

## 5. Fuentes y conexiones

Fuente pedida por el usuario (en sus palabras):

| Fuente/servidor | Motor | Base/esquema | Tablas/vistas/archivos | Método de conexión | Entorno | Dueño/permiso | Frecuencia de actualización | Origen del dato de conexión | Verificación en conexión real |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | `Diccionario (objeto_id)` / `Catálogo de Athena, sin uso previo (esquema.tabla)` / `Nueva — esquema suministrado por [correo]` | `Simulación` / `Verificada [fecha]` / `No verificada` |

Ejemplo: "Athena, Entregas Totales" → objeto `amazon_athena:Athena_ODBC2/AwsDataCatalog/bi_materialized_data/entregas_totales` del diccionario; consultas `Sim_entregas_totales` / `Real_entregas_totales` / `Src_entregas_totales`.

- Filtros de carga del BI de referencia que se aplican / no se aplican (con decisión):
- Columnas incluidas y excluidas (con justificación; atención a datos personales):
- Filtros de carga de otros BI listados en la ficha y decisión para este BI:
- Puntos abiertos de la ficha que afectan KPI de este BI y tratamiento:
- Diferencias encontradas entre el diccionario y la conexión real (reportadas para actualizar censo/diccionario):
- Fuentes no encontradas en el diccionario y responsable de suministrar sus datos o esquema:
- Dependencias externas (tablas/vistas que no existen en origen):

- Gateway/servicio requerido:
- Parámetros por entorno:
- Restricciones de acceso:
- No registrar contraseñas, tokens, secretos ni credenciales.

## 6. Modelo semántico
- Tipo de modelo y justificación:
- Granularidad de cada tabla:
- Hechos:
- Dimensiones:
- Claves:
- Relaciones/cardinalidad/dirección de filtro:
- Calendario y relaciones de fecha:
- Medidas existentes reutilizables:
- Medidas nuevas aprobadas:
- Columnas/tablas calculadas:
- Transformaciones Power Query/SQL:
- Tipos de datos, nulos, duplicados y controles de calidad:
- Volumen aproximado y necesidades de rendimiento:

## 7. Seguridad y operación
- RLS/perfiles/restricciones:
- Sensibilidad de datos:
- Permisos de acceso/publicación:
- Frecuencia y ventana de actualización:
- Gateway/credenciales administradas:
- Exportación/retención:
- Evidencia de prueba de actualización:
- Evidencia de prueba de seguridad:

## 8. Diseño corporativo
- Logo oficial disponible en `MCP_POWERBI\00_dlc\02_ai_dlc_bi\00_fuentes\Logo_Nebula.png`:
- Header y última actualización:
- Filtros corporativos aplicables:
- Botones, cards, gráficos y tablas:
- Colores/leyendas/navegación:
- Excepciones solicitadas por el usuario y aprobación:
- Decisiones pendientes del estándar (sección 4.17 del diseño) que afectan este BI y respuesta:
  - unidades px/pt:
  - colores 6–8 del tema:
  - color de advertencia:
  - tono de valores KPI de feedback:
  - jerarquía de filtros (si no es dominio Leads):

## 9. Riesgos, dependencias y pruebas
- Riesgo inicial: `Bajo / Medio / Alto`
- Dependencias principales:
- Riesgos de datos/modelo/seguridad:
- Pruebas de KPIs/totales:
- Pruebas de filtros e interacciones:
- Pruebas de actualización/RLS:
- Pruebas de rendimiento:
- Evidencia disponible:

## 10. Registro de decisiones
| Fecha | Tema | Requisito o propuesta IA | Impacto/riesgo | Decisión | Correo decisor | Motivo/evidencia |
|---|---|---|---|---|---|---|
| | | | | `Aprobado / Rechazado / Pendiente` | | |

## 11. Entrega
- Ruta Kiro:
- Versión/referencia candidata:
- Validaciones completadas:
- Validaciones pendientes y responsable:
- Alertas:
- Versión base guardada en `01_versiones\00_original\[BI]` y census_id del censo Inicial:
- README actualizado:
- Registro central actualizado:
- Documentación funcional/técnica:
- Estado final: `En construcción / Bloqueado / Validado / Listo para entrega`
