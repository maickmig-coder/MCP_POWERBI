# CONTROLES REFORZADOS DE DEPURACIÓN

Complementan la base común (`../../00_Base_Compartida/`). Antes estaban como anexos de los documentos 03, 04 y 15 de
la base de Depuración; desde la unificación de la base viven aquí porque solo aplican a este proceso.

## Alcance: Depuración solo depura, no agrega

- Depuración diagnostica y corrige integridad, dependencias, consultas, modelo, DAX y rendimiento de un BI existente.
- **No agrega fuentes, tablas, columnas de origen, páginas ni visuales nuevos.** Si el trabajo necesita algo nuevo,
  se registra como solicitud de Modificación (que sí usa el diccionario de datos, regla 16).
- Para saber qué otros tableros usan una tabla o columna antes de tocar su carga, se puede consultar el diccionario
  («¿qué tableros usan X?»); el diccionario no autoriza cambios.

## Alcance de la regla visual

La depuración no autoriza rediseñar ni homologar visualmente el tablero. Los estándares visuales
(`02_diseno_corporativo.md`) solo se consultan para detectar una inconsistencia cuando afecte la integridad, la
lectura funcional o cuando el analista lo solicite explícitamente. Toda corrección estética se gestiona como una
solicitud de Modificación, salvo que sea una reparación técnica necesaria y aprobada dentro del alcance.

## Integridad y validación (complementa `03_integridad_validacion.md`)

- Capturar estado antes y después con evidencia.
- Verificar KPIs, totales, conteos, filtros y contexto de cálculo afectados.
- Revisar refresh, conexiones, relaciones, RLS y navegación cuando correspondan.
- Revisar visuales ocultos, marcadores, botones y objetos heredados.
- Investigar diferencias no esperadas y no cerrar con pruebas críticas fallidas.
- No declarar mejora de rendimiento sin métrica comparable o evidencia explícita; indicar limitaciones de medición.
- Verificar reversibilidad según el riesgo.

### Inventario y preservación de visuales (V9.5)

Antes de cualquier eliminación de visuales, aplicar el protocolo `16_protocolo_integridad_visuales_eliminacion_segura.md`.

- Inventariar por ID técnico y página; el título no es clave única.
- Tratar búsquedas de texto/regex como localizadores de candidatos, nunca como prueba única.
- Aprobar acciones sobre IDs exactos antes de ejecutar.
- Comparar inventario antes/después por página e ID.
- Bloquear cierre ante cualquier desaparición no autorizada o diferencia no conciliada.
- Informar integridad técnica y funcional por separado.
- Si Power BI Desktop, refresh o una prueba funcional no se ejecutó, dejar constancia de `No validado`.

## Edición segura de archivos (complementa `04_archivos_y_encoding.md`, V9.5)

Antes de modificar un archivo, conservar una copia recuperable y registrar su ruta; cuando sea posible, calcular hash antes/después. Tras escribirlo, volver a leerlo, revisar el diff, comprobar BOM y caracteres acentuados, y validar sintaxis/estructura. Para JSON, el parseo debe terminar sin errores. Para TMDL, validar con herramientas disponibles y declarar las limitaciones.

No hacer reemplazos masivos sobre texto serializado sin comprender el contexto estructural. Una coincidencia textual puede estar en metadatos o en una referencia secundaria. Si se detecta mojibake, truncamiento o estructura alterada, detenerse y restaurar desde una copia íntegra antes de re-aplicar el cambio aprobado.

## Rendimiento (complementa `15_rendimiento_y_DAX.md`)

- Registrar línea base y condiciones de medición (mismo origen, filtros, periodo, ambiente y carga cuando sea posible).
- Priorizar eliminación de trabajo innecesario antes de carga, siempre que conserve semántica y fuente de verdad.
- Evaluar query folding sin asumir que estará disponible.
- Validar exactitud después de mover transformaciones entre SQL, Power Query, modelo y DAX.
- Distinguir beneficio estimado de beneficio observado.
- No prometer reducción de tamaño/tiempo si no se midió o no hay evidencia suficiente.
