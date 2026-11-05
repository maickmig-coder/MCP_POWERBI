# 7. DEPURACIÓN Y MEJORA

## Objetivo

Mejorar integridad, eficiencia y mantenibilidad del BI.

No es una etapa de "mejora estética". La meta es corregir problemas de integridad, reducir complejidad o consumo de recursos y mejorar mantenibilidad con evidencia. No cambiar la apariencia, distribución, paleta, tipografía ni navegación solo por preferencia estética. Si se detecta una necesidad visual no técnica, registrarla como solicitud separada de Modificación.

## 7.1 Integridad

Revisar:
- visuales rotos;
- visuales ocultos;
- bookmarks;
- botones;
- estados alternativos;
- navegación;
- objetos heredados de copias;
- tablas/columnas/medidas inexistentes;
- dependencias;
- elementos aparentemente sin uso.

## 7.2 Fuentes y consultas

Contemplar:
- SQL;
- Power Query;
- Power BI Dataflows/flows;
- Excel;
- vistas;
- archivos;
- otras fuentes.

Preguntar cuando corresponda:

"¿Deseas que revisemos también las consultas y fuentes para identificar
información que no se utiliza y evaluar si puede eliminarse antes de cargarla
a Power BI para reducir volumen y tiempo de carga?"

## 7.3 Optimizar antes de cargar

Evaluar:
- columnas no necesarias;
- filtros de filas en origen;
- SELECT de SQL;
- joins innecesarios;
- transformaciones redundantes;
- datos que luego serán descartados.

Lección formal:
> Antes de cargar grandes volúmenes, optimizar la fuente/consulta para
> traer únicamente la información necesaria.

Ejemplo del proyecto:
un BI que cargaba aproximadamente 20 millones de filas y unas 60 columnas
fue optimizado en SQL hasta aproximadamente 1,3 millones de filas y se
eliminaron columnas no utilizadas.

## 7.4 Columnas aparentemente no utilizadas

Una columna es candidata si no se detecta uso en:
- medidas;
- visuales;
- filtros;
- relaciones;
- cálculos;
- transformaciones conocidas.

Pero "no usada en Power BI" no significa automáticamente "seguro eliminar".

Regla:
1. detectar;
2. explicar dependencias;
3. estimar impacto;
4. proponer eliminación;
5. obtener validación del analista;
6. ejecutar solo con autorización.

## 7.5 Modelo

Revisar:
- tablas;
- columnas;
- medidas;
- relaciones;
- granularidad;
- claves;
- redundancias;
- cardinalidad;
- dependencias;
- columnas/medidas aparentemente no utilizadas.

## 7.6 DAX

Revisar opcionalmente todo el conjunto de DAX.

Detectar:
- fórmulas complejas;
- lógica duplicada;
- medidas reutilizables;
- conversiones innecesarias;
- filtros repetidos;
- cadenas excesivas de medidas;
- cálculos que podrían resolverse antes;
- oportunidades de CALCULATE;
- lógica que debería vivir en SQL/Power Query/modelo.

Antes de crear una medida/columna:
> comprobar si existe una lógica equivalente que pueda reutilizarse o
> simplificarse.

Ejemplo de propuesta:
"Encontré esta fórmula. Podemos simplificarla con la siguiente metodología
para reducir complejidad y evitar generar más peso al tablero."

## 7.7 Rendimiento

Revisar cuando aplique:
- consultas pesadas;
- medidas costosas;
- exceso de columnas;
- cardinalidad;
- tamaño del modelo;
- tiempos de carga;
- visuales con consultas costosas;
- transformaciones innecesarias.

## 7.8 Regla de aprobación

Depuración:
Detectar → evidenciar → explicar → identificar dependencias → clasificar riesgo → estimar beneficio/impacto → obtener decisión del analista → ejecutar solo lo aprobado → validar → documentar.

No hacer limpieza automática. `Encontrado`, `Inferido` y `Desconocido` deben distinguirse. No convertir una inferencia en hecho ni una falta de evidencia en prueba de no uso.

## 7.9 Línea base, pruebas y reversibilidad

Antes de cambiar, registrar cuando sea posible: tamaño del modelo/proyecto, filas/columnas relevantes, duración de refresh, consultas o visuales de referencia y resultados de KPIs/totales/conteos afectados. Si una métrica no puede obtenerse, declararlo; no inventar valores.

Cada cambio debe tener criterio de aceptación y pruebas antes/después. Las diferencias no esperadas se investigan antes de cerrar. Para riesgo medio/alto, documentar versión de origen, procedimiento de reversión y condiciones que disparan rollback. Si una prueba crítica falla, detener la entrega y corregir o revertir.

## 7.10 Integridad funcional y técnica

Validar, según los componentes afectados: refresh/conexión, resultados numéricos, filtros/contexto, relaciones, medidas, visuales, marcadores, botones, tooltips, navegación, RLS, exportaciones e integraciones. No todos aplican a todos los tableros: marcar `No aplica` con motivo.

## 7.11 Fuentes de verdad y query folding

Al mover lógica entre origen, SQL, Power Query, modelo o DAX, confirmar que se conservan filtros, granularidad, tratamiento de nulos/BLANK, tipos, fechas, zona horaria, duplicados y reglas de negocio. Evaluar query folding cuando corresponda; no asumir que mover una transformación al origen siempre es posible o mejora el resultado.

## 7.12 Alcance de revisión de consultas

Si la revisión de consultas y fuentes no está explícitamente incluida, preguntar al analista si desea incorporarla. No ampliar el alcance en silencio. Si el analista acepta, registrar esa decisión y las capas a revisar.


## Registro de la depuración/mejora

Antes de iniciar:

- abrir el README existente;
- registrar responsable y solicitante;
- registrar el objetivo de la depuración;
- registrar fecha de inicio;
- agregar la intervención al histórico.

Al finalizar, registrar qué se detectó, qué se propuso, qué fue aprobado,
qué se ejecutó, qué beneficio se obtuvo y qué quedó pendiente.


## Identificación por correo desde el inicio

Antes de iniciar una depuración o mejora se deben registrar únicamente:

- correo de quien trabaja/modifica el tablero;
- correo de quien solicita/es dueño del requerimiento.

El registro queda en el README del tablero y en el registro central.


# REGLA BLOQUEANTE — CONTEXTO/CENSO OBLIGATORIO PARA DEPURACIÓN Y MEJORA

## Principio

La depuración y mejora de un BI existente requiere conocer su estado actual.
Por lo tanto, **no se debe entrar a depurar sin contexto suficiente**.

Para un BI existente, el CENSO es la referencia principal del estado actual.

## Cuando no existe CENSO

Si se solicita depurar/mejorar un BI existente y no existe su CENSO en:

```text
MCP_POWERBI\02_censo
```

la depuración/mejora **DEBE QUEDAR BLOQUEADA**.

No se debe comenzar a eliminar, simplificar, optimizar, reorganizar,
reemplazar o modificar elementos del BI sin haber levantado primero el
contexto requerido.

### Procedimiento obligatorio

1. Solicitar el nombre exacto del BI.
2. Registrar:
   - correo de quien trabaja/modifica;
   - correo de quien solicita/es dueño.
3. Buscar el CENSO correspondiente en:

```text
MCP_POWERBI\02_censo
```

4. Verificar que el CENSO corresponde al nombre exacto del BI y que su contenido permite comprender el estado que se va a depurar. Un CENSO de otro BI o claramente desactualizado no satisface el bloqueo; registrar la limitación y actualizar/repetir el CENSO según corresponda.

5. Si no existe o no es válido, establecer el estado:

```text
BLOQUEADO — CENSO REQUERIDO
```

6. Conservar el BI original como PBIP en:

```text
MCP_POWERBI\01_bi\01_versiones\00_original\[Nombre exacto BI]\
```

7. Ejecutar el ritual de CENSO definido en:

```text
MCP_POWERBI\00_dlc\01_ai-dlc-censo
```

8. Guardar el resultado del CENSO en:

```text
MCP_POWERBI\02_censo
```

9. Verificar que el CENSO corresponde al BI exacto y quedó disponible.
10. Preparar la copia de trabajo en `MCP_POWERBI\01_bi\01_versiones\01_kiro\[Nombre exacto BI]`.
11. Solo después habilitar la depuración/mejora.

## Cuando el CENSO sí existe

1. Cargar el CENSO como contexto.
2. Verificar que corresponde al BI exacto.
3. Conservar el PBIP original sin modificarlo.
4. Analizar oportunidades de depuración/mejora.
5. Identificar dependencias e impacto.
6. Proponer acciones.
7. Obtener decisión del analista.
8. Ejecutar únicamente lo aprobado.
9. Comparar antes/después.
10. Validar integridad y rendimiento cuando aplique.
11. Documentar cambios, beneficios, alertas y pendientes.

## Regla de seguridad

El AI-DLC no debe interpretar la ausencia de CENSO como autorización para
"reconstruir" el estado actual por inferencia.

Si el contexto necesario no existe, primero se debe levantar el CENSO.

## Registro

La situación de bloqueo por ausencia de CENSO debe quedar registrada en el
README y, cuando corresponda, en el Registro de Cambio.


## 7.13 Evidencia, severidad y cierre

Cada hallazgo debe indicar ubicación concreta y evidencia. Clasificar severidad como `Bloqueante`, `Advertencia` o `Información`; un bloqueante impide declarar el trabajo listo. El mensaje debe explicar qué se encontró, dónde, por qué importa y qué acción se recomienda.

La depuración se considera `Listo para entrega` únicamente cuando las acciones aprobadas fueron probadas, las diferencias están explicadas, no hay bloqueantes abiertos y el README histórico, Registro de Cambio y registro central quedaron actualizados. Si las métricas de beneficio no se midieron, reportarlas como no medidas, no como logradas.


## 7.13 Control obligatorio de visuales y eliminación segura (V9.5)

Antes de eliminar o reparar visuales, se debe aplicar el protocolo `00_Base_Compartida/16_protocolo_integridad_visuales_eliminacion_segura.md` y registrar los candidatos en `02_Plantillas/04_inventario_visual_y_eliminacion_segura.md`.

- No usar coincidencias textuales, expresiones regulares ni títulos como criterio único para confirmar que un visual está roto.
- Identificar el objeto por página, ID técnico, ruta, título y tipo; revisar la referencia dentro de su contexto semántico.
- Crear una lista positiva de IDs/objetos exactos aprobados. No se ejecutan elementos no incluidos en ella.
- Analizar bookmarks, botones y estados alternativos de forma independiente; no vaciar colecciones ni eliminar grupos completos por defecto.
- Comparar inventarios antes/después por ID y por página. Toda desaparición no aprobada o diferencia no explicada bloquea el cierre.
- Separar integridad técnica de funcional. JSON válido no demuestra que el tablero funcione ni que haya conservado todos sus visuales.
- Ejecutar por etapas en la copia de trabajo y revertir ante corrupción o diferencias inesperadas.
- Revisar dependencias críticas antes de borrar columnas, medidas, consultas u otros objetos; si una dependencia no puede determinarse, dejar pendiente/bloqueado.
