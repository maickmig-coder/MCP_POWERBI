# REGLAS DEL PROCESO — CREACIÓN DE BI

## 1. Alcance y clasificación

Aplicar este proceso solo cuando se construya un BI nuevo. Si se parte de un BI existente, una copia funcional o un modelo ya publicado que requiere cambios, detenerse y confirmar si corresponde Modificación o Depuración/Mejora. No usar Creación para evitar el CENSO obligatorio de los otros procesos.

## 2. Levantamiento obligatorio

Antes de diseñar o construir, obtener y registrar:
- nombre exacto del BI;
- contexto y problema de negocio;
- finalidad y decisiones que debe apoyar;
- preguntas que debe responder y qué se requiere medir;
- público y perfiles de uso;
- alcance incluido y excluido;
- criterios de aceptación;
- fuentes, servidores, propietarios disponibles y método de conexión;
- reglas de negocio, excepciones y fuente de verdad;
- KPIs y medidas;
- páginas y propósito de cada página;
- filtros, navegación e interacciones;
- actualización y operación;
- seguridad, RLS y restricciones cuando apliquen;
- riesgos, dependencias y limitaciones conocidas.

Si falta información que pueda alterar cifras, seguridad, modelo o alcance, preguntar antes de implementar. Registrar explícitamente los supuestos pendientes; no convertirlos en hechos.

## 3. Identificación por correo

Antes de iniciar, solicitar únicamente:
- correo de quien trabaja/modifica el tablero;
- correo de quien solicita/es dueño del requerimiento.

Guardar ambos en README y registro central. No pedir nombre, cargo, teléfono ni otros datos personales para este control.

## 4. KPIs y reglas de negocio

Preguntar literalmente: **“¿Deseas definir los KPIs o quieres que proponga opciones?”**

Si el usuario solicita propuestas, para cada KPI presentar nombre, qué mide, utilidad, fórmula/lógica, campos requeridos, granularidad, filtros/periodos relevantes, fuente, dependencias y limitaciones. Marcar la propuesta como pendiente hasta que el usuario/analista la apruebe. No inventar definiciones de negocio ni cambiar una fórmula aprobada silenciosamente.

Documentar reglas para fechas, periodos, estados, duplicados, nulos, monedas, zonas horarias, inclusiones/exclusiones y conciliación cuando correspondan.

## 5. Visualizaciones y páginas

Preguntar: **“¿Deseas definir los gráficos o quieres que proponga opciones?”**

Si solicita opciones, presentar para cada una tipo de visual, pregunta que responde, campos/medidas, página sugerida, motivo, ventajas/limitaciones y dependencias. Esperar aprobación. Solicitar propósito y criterio de aceptación de cada página. No ubicar visuales arbitrariamente; aplicar la mesa de trabajo corporativa y las instrucciones explícitas del usuario.

## 6. Fuentes y seguridad de conexión

Registrar servidor, motor, base, esquema, tablas/vistas/archivos, método de conexión, entorno, frecuencia de actualización y dependencias técnicas cuando se conozcan. No solicitar ni escribir contraseñas, tokens, secretos ni cadenas con credenciales en los archivos del DLC. Usar mecanismos autorizados de acceso y documentar únicamente referencias no secretas.

Validar permisos, gateway, actualización y propietario de fuente cuando apliquen. No afirmar que una conexión o actualización funciona sin prueba o evidencia.

## 7. Modelo semántico y transformación

Definir con el analista la granularidad, tablas de hechos/dimensiones, claves, relaciones, cardinalidad, dirección de filtro, calendario, medidas, columnas/tablas calculadas, transformaciones y DAX. Evaluar el diseño apropiado (por ejemplo, estrella cuando aplique), sin imponer un patrón si el caso requiere otra estructura justificada.

Antes de crear lógica nueva, revisar si existe medida, columna, tabla o transformación reutilizable. Seleccionar columnas y filtrar datos por necesidad funcional y rendimiento, pero no eliminar información ni cambiar lógica sin autorización explícita. Validar tipos de datos, claves, nulos, duplicados y relaciones.

## 8. Diseño corporativo

Aplicar `00_Base_Compartida/02_diseno_corporativo.md` y usar la fuente oficial del logo:
`MCP_POWERBI\00_dlc\02_ai_dlc_creacion_modificacion\00_fuentes\Logo_Nebula.png`

Si el logo no está disponible, informar y solicitar la fuente o autorización; no sustituirlo automáticamente. Mantener jerarquía de filtros, header, tipografía, paleta, cards, botones, gráficos, tablas, leyendas, navegación y consistencia entre páginas según la regla corporativa vigente. No confundir Theme JSON con un reemplazo de las reglas de layout.

## 9. Seguridad y operación

Evaluar RLS, permisos de acceso, actualización, gateway, parámetros por entorno, exportación y sensibilidad de datos cuando apliquen. Probar seguridad con perfiles autorizados. No publicar ni dar por lista una configuración crítica no validada.

## 10. Trazabilidad y repositorio de trabajo

Desde el inicio:
1. confirmar nombre exacto;
2. crear/localizar `MCP_POWERBI\01_bi\01_versiones\00_original\[Nombre exacto BI]\` para el README histórico y la trazabilidad;
3. crear el README y actualizar `MCP_POWERBI\01_bi\01_versiones\00_original\REGISTRO_CONTROL_TABLEROS.md`;
4. crear y usar la carpeta de trabajo `MCP_POWERBI\01_bi\01_versiones\01_kiro\[Nombre exacto BI]\`;
5. construir exclusivamente en Kiro;
6. al aprobarse la entrega, identificar la versión base liberada y conservarla protegida en `00_original` según el mecanismo autorizado;
7. actualizar documentación, decisiones, evidencias, versión y estado final.

Para una creación nueva, CENSO se marca `No aplica`. Si se determina que el trabajo parte de un BI existente, reclasificarlo antes de continuar.

## 11. Pruebas y criterios de aceptación

Antes de declarar la entrega:
- conciliar KPIs y totales con fuente de verdad o evidencia aprobada;
- probar filtros, periodos, relaciones, medidas, navegación e interacciones;
- revisar visuales ocultos, marcadores, botones y estados alternativos cuando apliquen;
- comprobar actualización y RLS cuando sean requisitos;
- evaluar rendimiento según volumen y disponibilidad de medición;
- registrar diferencias, limitaciones y pendientes;
- comprobar la versión entregada y su reversibilidad.

Marcar controles no aplicables con justificación. No declarar `Listo para entrega` con bloqueantes abiertos.

## 12. Propuestas y decisiones

La IA puede analizar y proponer KPIs, visuales, modelo, DAX, consultas y optimizaciones. Cada propuesta que cambie la lógica de negocio, el alcance, la seguridad o los resultados requiere decisión explícita del analista. Registrar `Aprobado`, `Rechazado` o `Pendiente`, con motivo cuando corresponda. Ejecutar solo lo aprobado.

## 13. Entregables mínimos

- BI en la copia de trabajo Kiro;
- versión/referencia entregada;
- README histórico y registro central actualizados;
- levantamiento de requerimientos y decisiones;
- documentación funcional/técnica pertinente;
- evidencia de pruebas y validación;
- alertas, riesgos y pendientes;
- versión base protegida según el mecanismo de liberación autorizado.
