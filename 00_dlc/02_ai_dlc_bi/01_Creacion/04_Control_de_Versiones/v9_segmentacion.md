# V9.3 — Auditoría profunda del DLC de Creación

## Base de revisión
Se revisó el contenido de Creación de la V9/V9.2 segmentada contra las entregas históricas consolidadas V1 y V2–V8, con énfasis en los cambios acumulados hasta V8 — Repositorio Kiro. Se conservaron las decisiones previas y se hicieron explícitas las reglas necesarias para que Creación opere de forma autónoma.

## Cambios registrados

| Archivo/área | Clasificación | Hallazgo y acción |
|---|---|---|
| README de Creación | MODIFICADA | Se retiraron instrucciones que mezclaban los otros procesos y se estableció orden de lectura. |
| Rutas y activos | MODIFICADA | Se corrigió la ruta del logo a `00_fuentes`; se separó trazabilidad (`00_original`) de desarrollo (`01_kiro`). |
| CENSO | ACLARADA | En creación genuinamente nueva se marca `No aplica`; si el trabajo parte de un BI existente, se reclasifica. No se relajó la regla CENSO para modificación/depuración. |
| Reglas de Creación | AMPLIADA | Se reforzaron clasificación, criterios de aceptación, reglas de negocio, fuente de verdad, seguridad, acceso, operación y aprobación de propuestas. |
| Levantamiento | MODIFICADA | Se eliminaron campos ambiguos de persona/área y se hicieron explícitos los dos correos obligatorios. Se añadieron campos de aceptación, granularidad, conciliación, conexión, actualización, seguridad y decisiones. |
| Flujo | MODIFICADA | Se ordenó clasificación → trazabilidad → levantamiento → aprobación → construcción Kiro → validación → liberación. |
| Checklist | REEMPLAZADA en esta carpeta | El checklist genérico de V8 incluía controles bloqueantes de Modificación/Depuración y una sección de registro de cambio ajena a una creación nueva. Se sustituyó por checklist específico de Creación, manteniendo controles transversales de integridad, rendimiento, seguridad, documentación y entrega. |
| Diseño corporativo | CONSERVADA con corrección de ruta | Se conservaron las especificaciones de header, logo, segmentaciones, botones, gráficos, cards, KPIs, tipografía, paleta, tablas, navegación y Theme JSON. |
| Integridad, encoding, trazabilidad, alertas, registro de cambios, evolución de reglas y rendimiento/DAX | CONSERVADAS | Se mantienen las reglas de validación, UTF-8 sin BOM cuando corresponda, historial, decisiones, riesgos, dependencias y lecciones aprendidas. |
| Kiro | CONSERVADA y aclarada | El desarrollo siempre ocurre en `01_kiro`; la versión base liberada se protege en `00_original` tras aprobación. No se afirma que exista un original antes de que la creación haya sido aprobada. |

## Reglas históricas conservadas
- Preguntar si el usuario define KPIs o desea propuestas de IA.
- Preguntar si el usuario define visuales o desea propuestas de IA.
- No solicitar credenciales en el levantamiento.
- Definir fuentes, modelo, granularidad, relaciones, calendario, medidas, DAX y transformaciones.
- Contemplar RLS, actualización, drill-through, drill-down, tooltips, bookmarks, interacciones y exportaciones cuando aplique.
- Usar el estándar visual corporativo y la ruta oficial del logo.
- Mantener README acumulativo y registro central por tablero.
- Registrar solo los dos correos para la trazabilidad de personas.
- Revisar integridad, objetos ocultos, archivos y codificación.
- Aplicar control de versiones, dependencias, riesgo, pruebas y cierre formal.
- Trabajar en la copia `01_kiro` y proteger la versión aprobada en `00_original`.

## Hallazgos que se corrigieron
1. La ruta dentro de la base de Creación refería `01_fuentes`, en contradicción con la ruta oficial `00_fuentes`.
2. README de Creación daba instrucciones conjuntas para creación, modificación y depuración.
3. El checklist de Creación contenía secciones bloqueantes de CENSO específicas de modificación y depuración.
4. La plantilla de levantamiento usaba `Área` y `Responsable` de manera ambigua y no separaba los dos correos obligatorios.
5. El flujo no definía de forma precisa cuándo se crea y protege la primera versión base de un BI nuevo.
6. Faltaban campos explícitos para criterios de aceptación, reglas de negocio, fuente de verdad, conciliación, entorno, seguridad y evidencia de pruebas.

## Validaciones ejecutadas sobre este paquete
- Inventario de archivos revisado.
- Se verificó que el checklist de Creación no contenga controles bloqueantes específicos de Modificación o Depuración.
- Se verificaron referencias a `00_fuentes`, `01_kiro`, `00_original` y la ruta de trazabilidad.
- Se comprobó consistencia entre README, reglas, plantilla, flujo y checklist.
- Se comprobó que los archivos Markdown se guardan en UTF-8 sin BOM.
- La revisión es documental/estructural; no equivale a una prueba de ejecución sobre un PBIP real ni sobre el repositorio MCP_POWERBI.

## Pendiente operativo explícito
La promoción de una creación aprobada a la versión base protegida en `00_original` debe ejecutarse mediante el mecanismo real de versionado autorizado por el equipo. Si ese mecanismo no está disponible, la IA debe reportarlo y no afirmar que la promoción se completó.
