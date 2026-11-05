# Criterios para hallazgos y puntos de revisión (v2.3.4)

> Reemplaza a `criterios-propuestas.md` (v1). El cambio de nombre refleja la decisión de que el CENSO **describe y señala**, pero no propone cambios: la modificación, creación y depuración son un DLC aparte que usa el CENSO como base.

## 0. Quién los registra

`censo.py borrador` registra los hallazgos detectables en los archivos (filas `H-A*`): referencias rotas agrupadas por entidad, bookmarks y botones con destino inexistente, medidas vacías o duplicadas, segmentaciones repetidas, tarjetas con conteos implícitos, inteligencia de tiempo automática, roles sin RLS, recursos sin uso y DAX con referencias inexistentes. La IA revisa esas filas (certeza, prioridad, impacto) y agrega los hallazgos que requieren lectura funcional, como una tarjeta cuyo título no coincide con lo que calcula.

## 1. Cuándo se registra un punto

Se registra una fila en la tabla maestra (sección 16, «Hallazgos, vacíos y puntos de revisión») cuando el análisis encuentra algo que:

- puede afectar la comprensión del BI o el valor que muestra un KPI;
- presenta una inconsistencia entre lo que un objeto comunica y lo que calcula;
- presenta una referencia rota (entidad, página, visual, bookmark o recurso inexistente);
- presenta una dependencia desconocida o no verificable;
- presenta una regla no documentada o una definición de negocio sin confirmar;
- es un dato técnico que un cambio futuro debe conocer (por ejemplo, una relación inactiva o una columna técnica de carga).

Si no se puede responder “¿qué encontraste que te llevó a registrar esto?”, la fila no se incluye.

## 2. Tipos (CAT-09) y categorías

**Tipos:** `Hallazgo`, `Riesgo`, `Vacío`, `Observación`.

**Categorías:**

| Categoría | Ejemplos |
|---|---|
| Gobierno | Frecuencia de actualización, ambiente de publicación o propietario de una fuente no identificados. El dueño del tablero (R02) es el único responsable registrado. |
| Datos | Fuente sin descripción, granularidad no identificada, transformación compleja sin documentar. |
| Modelo | Relación con lógica no clara, tabla de función desconocida, auto fecha/hora activo, medidas duplicadas o vacías. |
| Métrica | Rótulo que no coincide con el cálculo, agregación implícita, conteo de texto usado como conteo distinto. |
| Reporte | Visual sin propósito claro, slicers repetidos, página oculta sin finalidad. |
| Referencias | Visuales, bookmarks, botones o recursos que apuntan a objetos inexistentes. |
| Presentación | Recurso gráfico sin uso, recurso inexistente, tema no identificado. |
| Actualización | Frecuencia o proceso de refresco desconocido. |
| Seguridad | Rol sin reglas, RLS esperado y ausente. |
| Calidad | Tratamiento inconsistente de nulos, duplicidad potencial. |

## 3. Campos obligatorios de cada fila

| Campo | Contenido |
|---|---|
| `ID` | `H-A01`… y `V-A01`… para los que genera `censo.py`; `H01`… y `V01`… para hallazgos y vacíos que agrega la IA. |
| Tipo | CAT-09. |
| Categoría | Tabla anterior. |
| Descripción concreta | La condición observada, en una o dos frases, con el valor literal (ej.: “la card calcula `Count(año)`”). |
| Página y objeto | Nombre de página y título del objeto. |
| `page_id` | Completo o `No aplica`. |
| `visual_id` / `object_id` | Todos los IDs afectados, completos y con su nombre (`ID · nombre`, R48). |
| `bookmark_id` / estado | Si aplica. |
| Evidencia exacta | Archivo, ruta y propiedad o expresión. |
| Certeza | CAT-01. |
| Objetos afectados y dependencias | Qué otros objetos dependen del afectado (desde las secciones 5, 7, 9, 11 y 12). Es el insumo con el que el DLC de modificación armará su regresión. |
| Impacto | Qué parte de la lectura del BI o de un KPI se ve afectada. |
| Prioridad | CAT-10, según el punto 4. |
| Punto de revisión | Qué debe revisarse o confirmarse, y con quién. |
| Validación requerida | Sí/No y responsable por confirmar. |
| Estado | CAT-11. `Pendiente de validación` hasta que el dueño responda (R55). |
| Respuesta del dueño | Fecha y respuesta del dueño (obligatoria con `Confirmado por el dueño` o `Descartado por el dueño`). Si el dueño realiza el censo y no sabe la respuesta: fecha y constancia de que se preguntó. `—` mientras no se haya preguntado. |

## 4. Prioridad

- **Alta:** puede alterar el valor que lee el usuario en un KPI o una decisión que se toma con el tablero.
- **Media:** afecta una parte del análisis, la navegación o existe una dependencia relevante sin verificar.
- **Baja:** mejora la documentación o el entendimiento, sin efecto visible en el análisis principal.

## 5. Redacción: describir, no prescribir

El punto de revisión dice **qué revisar**, no **qué hacer**. Verbos permitidos: revisar, confirmar, validar, verificar, consultar. Verbos no permitidos en la tabla maestra: cambiar, eliminar, reemplazar, corregir, usar en lugar de, desactivar, retirar, depurar. El validador marca estos verbos como error.

| Correcto | Incorrecto |
|---|---|
| Confirmar con el dueño qué medida debe mostrar la card “Total unidades convenios”, que hoy calcula `Count(año)`. | Cambiar el binding a `[cantidad de maquinas]`. |
| Revisar el propósito de los 2 slicers de `Q` en la página Dashboard_Empresas (`86c38682d276ded8a3ea`, `b2df3c91709631415d59`). | Eliminar el slicer duplicado. |
| Validar visualmente en Power BI el efecto del botón “Conectividad”, cuyo destino `7fe28b006cd3b491a578` no existe. | Corregir el destino o retirar el botón. |

## 6. Bookmarks y estados

Un punto relacionado con un visual, filtro, botón o bookmark indica en qué estado se observa la condición (`page_id + visual_id + bookmark_id`) y si la acción que lo invoca fue encontrada. No se registra un objeto como sin uso por no aparecer en la vista inicial o en una captura; la ausencia se comprueba en todos los estados accesibles.

## 7. Lo que el CENSO entrega al DLC de modificación

Para cada punto: IDs completos, evidencia, objetos afectados y dependencias, prioridad y estado de validación. El DLC de modificación decide si actúa, cómo, con qué matriz de regresión y con qué aprobación.
