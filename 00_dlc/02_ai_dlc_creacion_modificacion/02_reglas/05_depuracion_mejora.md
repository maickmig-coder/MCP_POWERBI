# 7. DEPURACIÓN Y MEJORA

## Objetivo

Mejorar integridad, eficiencia y mantenibilidad del BI.

No es una etapa de "mejora estética".

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
Detectar → explicar → proponer → estimar beneficio/impacto → aprobar →
ejecutar → validar.

No hacer limpieza automática.


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
NIGGA\02_censo
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
NIGGA\02_censo
```

4. Si no existe, establecer el estado:

```text
BLOQUEADO — CENSO REQUERIDO
```

5. Conservar el BI original como PBIP en:

```text
NIGGA\01_bi\01_versiones\00_original\[Nombre exacto BI]\
```

6. Ejecutar el ritual de CENSO definido en:

```text
NIGGA\00_dlc\01_ai-dlc-censo
```

7. Guardar el resultado del CENSO en:

```text
NIGGA\02_censo
```

8. Verificar que el CENSO corresponde al BI exacto y quedó disponible.
9. Solo después habilitar la depuración/mejora.

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
