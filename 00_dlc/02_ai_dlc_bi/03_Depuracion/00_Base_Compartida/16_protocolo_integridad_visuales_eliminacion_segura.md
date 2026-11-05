# Protocolo obligatorio — Inventario, protección y eliminación segura de elementos

**Versión incorporada:** V9.5 — Depuración y Mejora  
**Alcance:** controles operativos exclusivos de `03_Depuracion`. Este protocolo no modifica ni sustituye el ritual ni las plantillas del DLC de CENSO. El CENSO disponible se consulta como referencia de estado actual; la decisión de cambio siempre se valida contra el proyecto PBIP real y la aprobación explícita del analista.

## 1. Propósito y regla principal

Evitar falsos positivos que eliminen visuales, medidas, columnas, marcadores, botones u otros objetos válidos por encontrar una referencia textual aislada, una coincidencia de nombre o metadatos residuales.

> **Prohibido eliminar un objeto únicamente porque una búsqueda de texto, expresión regular o coincidencia de nombre encontró una entidad, campo o medida que parece inválida.** Una búsqueda textual sirve para localizar candidatos; no demuestra que el objeto esté roto ni autoriza su eliminación.

Toda eliminación debe tener evidencia semántica, identificación inequívoca, revisión de dependencias, autorización exacta y comparación antes/después.

## 2. Inventario previo obligatorio de visuales

Antes de modificar visuales, generar un inventario previo desde el proyecto PBIP/PBIR disponible. Para cada elemento registrar, cuando la estructura lo permita:

- nombre exacto de la página y su identificador técnico;
- título visible exacto; si no tiene título, `Sin título visible`;
- tipo de visual;
- identificador estable del visual y ruta del archivo `visual.json`;
- estado visible/oculto y página visible/oculta, si se puede determinar;
- campos, medidas, entidades y roles de consulta realmente proyectados;
- filtros, formato condicional, ordenamiento, tooltips, drill-through e interacciones relevantes;
- relación con bookmarks, botones, navegación y estados alternativos;
- resultado de la revisión: válido, roto confirmado, candidato por revisar o desconocido;
- evidencia técnica que sustenta la clasificación;
- acción propuesta, riesgo, dependencias y decisión del analista.

Los identificadores se consideran la clave primaria del inventario; el título visible es descriptivo y no es una clave única. Dos visuales pueden tener títulos iguales. Un título distinto tampoco demuestra que sean objetos diferentes si el identificador/ruta indica lo contrario.

Si el proyecto no permite extraer alguno de estos datos, marcarlo como `Desconocido` y explicar la limitación. No inventar identificadores ni completar por suposición.

## 3. Cómo analizar referencias sospechosas

Una coincidencia textual con una tabla/entidad/campo/medida inexistente se clasifica inicialmente como **candidato**, no como visual roto confirmado.

El análisis debe:

1. Abrir y parsear el JSON completo; comprobar que es válido antes de interpretar su contenido.
2. Ubicar la referencia exacta y el contexto estructural donde aparece.
3. Distinguir las proyecciones/roles de consulta activos de filtros, formato, metadatos, configuración heredada u otras referencias secundarias.
4. Verificar el objeto contra el modelo real disponible (TMDL/definiciones) y sus dependencias.
5. Comprobar si el visual sigue usando campos/medidas existentes y si la referencia sospechosa realmente impide renderizarlo o altera su resultado.
6. Correlacionar el hallazgo con título, página, tipo, ID y evidencia de ejecución si existe.
7. Registrar cualquier incertidumbre. Si no puede determinarse si la referencia es activa o residual, no eliminar: solicitar revisión/aprobación con la limitación explícita.

Las expresiones regulares pueden usarse para localizar archivos candidatos, nunca como única prueba de eliminación ni como autorización para ejecutar `Remove-Item` recursivo.

## 4. Lista positiva de cambios aprobados

Antes de eliminar o modificar un objeto, crear una lista positiva de acciones autorizadas. Cada registro debe incluir:

- ID único de hallazgo y propuesta;
- página y su ID;
- título visible y tipo;
- ID técnico/ruta del objeto;
- causa demostrada y evidencia;
- dependencias y riesgo;
- acción exacta aprobada (`eliminar`, `reparar`, `conservar`, `pendiente`);
- fecha/versión o referencia de aprobación.

Solo se pueden ejecutar las acciones que aparezcan de forma inequívoca como `Aprobado`. No se puede ampliar una aprobación por similitud de nombre, misma página, mismo tipo o coincidencia con el mismo patrón. Un objeto no incluido en la lista aprobada se conserva.

Si la identidad del objeto no es inequívoca, hay discrepancia entre inventario y proyecto, o la evidencia no permite separar una referencia activa de una residual, detener esa acción y escalarla al analista.

## 5. Aprobación granular y alcance

Presentar al analista la lista exacta de objetos y cambios propuestos antes de ejecutar. Para cada uno explicar: dónde está, qué evidencia existe, por qué se considera defectuoso, dependencias, impacto, riesgo, alternativa de reparación y rollback.

Una aprobación grupal solo cubre los objetos enumerados en ese grupo. No autoriza objetos nuevos descubiertos después. Los nuevos hallazgos se agregan a una nueva lista y requieren decisión.

## 6. Bookmarks, botones y estados: análisis separado

Los bookmarks, botones, paneles de selección, estados alternativos, navegación, tooltips y páginas ocultas se inventarían y analizan como objetos con dependencias propias. No se deben borrar todos los bookmarks por el hecho de que algunos apunten a visuales rotos.

Para cada bookmark/estado:

- identificar su nombre/ID y el estado de visibilidad/selección que controla;
- enumerar los objetos y páginas afectados;
- determinar si puede repararse, actualizarse o si está confirmado como obsoleto;
- presentar la lista exacta y obtener aprobación antes de eliminarlo;
- validar navegación, visibilidad y estados después del cambio.

Vaciar una colección completa (por ejemplo `items: []`) o borrar en lote bookmarks/botones sin aprobación individual explícita está prohibido.

## 7. Comparación antes/después y conservación

Generar inventario antes y después de los cambios. Comparar por IDs estables, con un resumen por página y tipo:

- elementos conservados;
- elementos reparados/modificados;
- elementos eliminados con aprobación;
- elementos nuevos;
- elementos que desaparecieron sin acción aprobada;
- diferencias que no se pudieron resolver.

**Bloqueo de cierre:** cualquier visual que existía antes y desaparezca después sin una acción exacta aprobada debe tratarse como incidente bloqueante. Restaurar desde la copia de referencia o revertir el cambio antes de continuar, salvo que el analista autorice una resolución distinta y quede documentada.

Los conteos globales no bastan. La conciliación debe ser por página y por ID; cada diferencia se explica individualmente. Una diferencia de conteo no explicada bloquea la entrega.

## 8. Integridad técnica vs. integridad funcional

Validar por separado:

**Integridad técnica:** estructura de carpetas, JSON parseable, referencias de objetos, sintaxis TMDL/PBIR, codificación, archivos esperados y consistencia de identificadores.

**Integridad funcional:** visuales y KPIs que deben mantenerse, valores y totales, filtros/contexto, interacciones, navegación, bookmarks, botones, drill-through, tooltips, seguridad/RLS y refresh según aplique.

Que los archivos JSON sean válidos o que no haya referencias rotas no demuestra que el tablero conserve su comportamiento. Si Power BI Desktop no se abrió, el refresh no se ejecutó o una prueba funcional no pudo realizarse, dejarlo expresamente como `No validado` y no declarar integridad funcional completa.

## 9. Ejecución por etapas y reversibilidad

Trabajar en la copia `01_kiro`, nunca en `00_original`. Aplicar cambios en grupos pequeños y rastreables:

1. guardar inventario/línea base;
2. validar lista de acciones aprobadas;
3. ejecutar un grupo pequeño;
4. validar estructura, dependencias y comportamiento afectado;
5. comparar contra la línea base;
6. registrar resultado;
7. continuar solo si no hay diferencias inesperadas.

Ante un fallo, corrupción, diferencia inesperada o pérdida de un objeto no aprobado: detener la secuencia, preservar evidencia, revertir desde la versión de trabajo conocida como válida y volver a probar. No encadenar más cambios sobre un estado incierto.

## 10. Codificación y edición de archivos

En cada archivo de texto modificado:

- conservar una copia recuperable antes del cambio;
- registrar ruta y hash antes/después cuando sea posible;
- utilizar codificación compatible con el archivo original y el requisito de Power BI;
- comprobar BOM explícitamente;
- revisar caracteres acentuados y texto conocido para detectar mojibake (`año` no debe convertirse en `aÃ±o`);
- parsear JSON y validar sintaxis/estructura TMDL cuando corresponda;
- volver a abrir/leer el archivo después de escribirlo y revisar el diff.

No asumir que `Set-Content -Encoding UTF8` produce UTF-8 sin BOM en todas las versiones de PowerShell. Si hay corrupción, no reparar cadenas a ciegas: restaurar desde el original o copia íntegra y volver a aplicar el cambio aprobado con un método validado.

## 11. Dependencias para otros elementos

Antes de eliminar columnas, medidas, tablas, consultas, transformaciones o custom visuals, revisar las dependencias disponibles: visuales visibles/ocultos, filtros, bookmarks/estados, relaciones, jerarquías, ordenamiento por columna, formato condicional, RLS, medidas dependientes, SQL/M/Power Query, refresh y consumidores externos conocidos. La falta de referencia directa no prueba ausencia de dependencia.

Si no se puede revisar una dependencia crítica, clasificar el cambio como `Pendiente` o `Bloqueado`; no eliminar.

## 12. Incidente de referencia para prevención

Durante la prueba de depuración de `GC - Flotillas`, se eliminó el visual `Participación por convenio (unidades año)` de `Dashboard_Convenios`, aunque era un gráfico válido según la información funcional disponible. La instrucción usada para buscar visuales candidatos coincidía con cualquier aparición textual de entidades como `Cultivos`, `RUNT` o `Importaciones` en todo el `visual.json`, y después eliminaba recursivamente la carpeta completa del visual.

La evidencia disponible respalda que el criterio de selección era demasiado amplio; no demuestra que el nombre duplicado del gráfico fuera la causa. La causa exacta por archivo debe confirmarse comparando el PBIP original, el `visual.json` original y la lista exacta de rutas seleccionadas por el comando.

**Lección preventiva:** una coincidencia textual no demuestra que un visual esté roto. El inventario por ID, la lectura semántica de la referencia, la lista positiva de IDs aprobados y el diff antes/después son controles obligatorios. El visual debe conservarse o restaurarse si no existe aprobación inequívoca para eliminarlo.

## 13. Criterios de cierre específicos

No cerrar la depuración como lista si ocurre cualquiera de estos casos:

- visual válido desaparecido sin aprobación exacta;
- objetos eliminados que no figuran en la lista positiva;
- diferencia de inventario/conteo sin explicación por página e ID;
- JSON/TMDL/archivos con errores de sintaxis o codificación;
- diferencias funcionales inesperadas;
- dependencias críticas desconocidas en un cambio destructivo;
- pruebas críticas pendientes o fallidas presentadas como si hubieran pasado;
- original modificado;
- documentación o historial no actualizado.
