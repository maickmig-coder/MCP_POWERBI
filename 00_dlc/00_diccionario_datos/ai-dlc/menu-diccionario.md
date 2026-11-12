# 📚 Menú del diccionario de datos

Aquí puedes consultar **de dónde salen los datos de nuestros tableros de Power BI**: qué conexiones usamos, qué
tablas hay y qué columnas tiene cada una.

**¿Cómo se usa?** Escribe el **número** de la opción o la **frase de ejemplo**. No necesitas saber programar:
el asistente hace el trabajo y te explica el resultado. Para volver a ver este menú: **«menú del diccionario»**.

---

### 1. Ver qué fuentes de datos existen
**Dime:** «consulta diccionario» o «¿qué fuentes tenemos?»

Te muestro las conexiones, las tablas de cada una y qué tableros las usan. Antes reviso que la información esté
al día; si hay un censo nuevo, la actualizo primero.

### 2. Buscar una tabla o un dato
**Dime:** «busca fuente entregas» o «¿dónde está el dato NIT?»

Busco la palabra en los nombres de las tablas y de sus columnas, sin importar mayúsculas ni tildes: primero en
las tablas que ya usan nuestros tableros y después en **todo el catálogo de Athena**, incluidas las tablas que
ningún tablero usa todavía (ideal para un tablero nuevo).
Si no aparece en ninguno, te explico qué datos necesito para conectarnos a esa fuente nueva (**nunca contraseñas**).

### 3. Saber qué tableros usan una tabla o un dato
**Dime:** «¿qué tableros usan entregas?» o «impacto del dato valor»

Te digo qué tableros traen esa tabla o ese dato, con qué nombre y con qué filtros. Para saber en qué gráfica
exacta aparece, hay que mirar el censo de ese tablero.

### 4. Actualizar el diccionario
**Dime:** «actualiza censos»

Reviso todos los censos. Si alguno es nuevo o cambió, actualizo el diccionario; si no, te aviso y no toco nada.
Te pido tu correo una sola vez, para dejar registro de quién lo actualizó.

> Normalmente no lo necesitas: **cada censo actualiza el diccionario al terminar**. Úsalo si el censo avisó que
> no pudo actualizarlo, o si hay una versión nueva del catálogo de Athena.

---

**¿Vas a crear un tablero nuevo?** No necesitas este menú: el proceso de Creación toma del diccionario la
"versión de práctica" de cada tabla (mismas columnas, sin datos ni contraseñas).

## 📖 Palabras que vas a ver

| Palabra | Qué significa |
|---|---|
| **Diccionario de datos** | El documento que reúne las conexiones, tablas y columnas de nuestros tableros. |
| **Censo** | La "radiografía" de un tablero. El diccionario se arma juntando todos los censos. |
| **Conexión** | El lugar de donde salen los datos, por ejemplo una base de datos en Athena. |
| **Tabla / columna** | Un conjunto de datos y cada uno de sus campos, como una hoja de Excel y sus columnas. |
| **Versión de práctica** | Una copia vacía de la tabla, con sus mismas columnas, para construir sin datos reales. |
| **Posible dato personal** | Columna cuyo nombre sugiere que identifica a una persona (cédula, correo, teléfono). Se usa solo si el dueño lo aprueba. |

## 🔒 Lo que el asistente nunca hará

Pedir o guardar contraseñas · cambiar censos o tableros · crear o borrar tablas en las bases de datos ·
inventar información que no esté en los censos.
