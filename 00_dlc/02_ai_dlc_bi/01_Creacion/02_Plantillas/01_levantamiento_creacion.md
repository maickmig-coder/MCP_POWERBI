# PLANTILLA — LEVANTAMIENTO DE BI NUEVO

Completar lo conocido; dejar explícito `Pendiente`, `No aplica` o `Por confirmar` cuando corresponda. No inventar respuestas.

## 1. Identificación y trazabilidad
- Nombre exacto del BI:
- Correo de quien trabaja/modifica:
- Correo de quien solicita/es dueño:
- Fecha de inicio:
- Estado inicial:
- CENSO: `No aplica` para BI nuevo / `Reclasificar solicitud` si parte de un BI existente.
- Ruta README histórico: `MCP_POWERBI\01_bi\01_versiones\00_original\[Nombre exacto BI]\README.md`
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
| Fuente/servidor | Motor | Base/esquema | Tablas/vistas/archivos | Método de conexión | Entorno | Dueño/permiso | Frecuencia de actualización |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

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
- Logo oficial disponible en `MCP_POWERBI\00_dlc\02_ai_dlc_creacion_modificacion\00_fuentes\Logo_Nebula.png`:
- Header y última actualización:
- Filtros corporativos aplicables:
- Botones, cards, gráficos y tablas:
- Colores/leyendas/navegación:
- Excepciones solicitadas por el usuario y aprobación:

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
- Versión base protegida en `00_original`:
- README actualizado:
- Registro central actualizado:
- Documentación funcional/técnica:
- Estado final: `En construcción / Bloqueado / Validado / Listo para entrega`
