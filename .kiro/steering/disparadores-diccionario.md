# Disparadores del diccionario de datos (MCP_POWERBI)

Cuando la persona pida algo sobre fuentes, conexiones, bases de datos, tablas o columnas de los BI, usa el
diccionario de datos. Detalle: `00_dlc/00_diccionario_datos/ai-dlc/disparadores.md`.

## Cómo hablar

Lenguaje sencillo: "tabla", "dato", "tablero", "fuente", "conexión". Sin comandos, códigos de salida ni IDs
técnicos, salvo que los pidan; si hacen falta, van al final como "Referencia: …".

## Menú (DD-00)

Si dice «menú del diccionario», «¿qué puedo hacer?» o su pedido no es claro, muestra esto y espera la elección:

```
📚 Menú del diccionario de datos — escribe el número o la frase

  1. Ver qué fuentes de datos existen ........ «consulta diccionario»
  2. Buscar una tabla o un dato .............. «busca fuente entregas»
  3. Saber qué tableros usan una tabla o dato  «¿qué tableros usan entregas?»
  4. Actualizar con los censos ............... «actualiza censos»
```

## Comando base (desde la raíz `MCP_POWERBI`)

`python 00_dlc/00_diccionario_datos/scripts/diccionario.py <comando> --censos 02_censo --salida 00_dlc/00_diccionario_datos`

Regla obligatoria: antes de responder sobre fuentes, ejecuta `estado`. Si no es `AL_DIA`, ejecuta primero
`actualizar --correo-ejecutor <correo>` (pide el correo una vez por sesión, explicando que es para dejar registro).
Nunca respondas sobre fuentes desde la memoria ni desde un censo individual.

| Opción | Si dice… | Ejecuta |
|---|---|---|
| 1 (DD-02) | «consulta diccionario», «¿qué fuentes hay?» | `estado` (→ `actualizar` si hace falta) y responder desde `00_dlc/00_diccionario_datos/diccionario-datos.md` |
| 2 (DD-04) | «busca fuente X», «¿dónde está el dato X?» | `buscar --texto "X"` (tablas de los tableros + todo el catálogo de Athena); sin resultados en ninguno → fuente nueva (DD-07) |
| 3 (DD-05) | «¿qué tableros usan X?», «impacto de X» | `impacto --objeto "X" [--columna "C"]`; aclarar que la gráfica exacta está en el censo de cada tablero |
| 4 (DD-01) | «actualiza censos», «actualiza diccionario» | `estado`; si cambió algo → `actualizar`; si no → «sin cambios» y no escribir. Normalmente ya lo hizo el censo al registrarse (R60) |
| — (DD-06) | «prepara la conexión de X» (Creación) | `simulacion --objeto "X"` (también para tablas que solo están en el catálogo) |
| — (DD-07) | «fuente nueva X» o búsqueda sin resultados | Pedir datos de conexión sin contraseñas, o las columnas de la tabla; no editar el diccionario |

Códigos de salida (internos, no mostrarlos): 0 ok · 10 desactualizado · 11 sin diccionario · 12 no encontrado o
ambiguo (si es ambiguo, mostrar las opciones con palabras sencillas y pedir que elija).

Al terminar, ofrece en una línea el siguiente paso natural o volver al menú.

Prohibido: pedir o guardar contraseñas, modificar censos, editar el diccionario a mano, crear tablas o vistas,
inventar fuentes o tipos.
