# Ejemplo de referencia

## Contenido

| Archivo | Qué es |
|---|---|
| `GC - Flotillas - censo.md` | Censo real del tablero GC - Flotillas (PBIP `00_original`), generado por Kiro con el ritual v2.2.3, con la sección 14 corregida según R51 (v2.2.4) y migrado al formato v2.3 (columnas «Validación del dueño» y «Respuesta del dueño»). |

Datos del ejemplo: 325 IDs nativos, cada uno con su nombre; `censo.py validar` sin errores; estado «Completado pendiente de validación», con 27 puntos esperando la respuesta del dueño (9 reglas inferidas de la sección 14 y 18 filas de la sección 16). Aún no tiene huella del PBIP: se agrega en su próxima ejecución con el tablero (`iniciar-validacion` o un censo nuevo).

## Para qué sirve

- **Modelo de profundidad y redacción:** muestra cómo queda cada sección completa, cómo se redactan los marcadores de la IA (2.1, 5.1, 10, 14, 15 y 16) y cómo se citan los vacíos sin afirmar lo que declaran desconocido.
- **Comparación:** si un censo nuevo se aparta mucho de este en extensión o en forma, conviene revisarlo contra el ritual.
- **Pruebas del ritual:** al cambiar `scripts/` o las reglas, `censo.py validar --markdown "examples/GC - Flotillas - censo.md"` debe seguir sin errores ni advertencias de contenido.

Kiro **no** lee este archivo durante un censo (el steering lo excluye para no gastar tokens); es referencia para personas y para revisar resultados.

## Límites del ejemplo

- Es un ejemplo de forma, no de datos: los IDs, nombres y hallazgos son de GC - Flotillas y no aplican a otro tablero.
- Se validó como texto. La conciliación contra el PBIP (`validar --pbip`) se ejecuta en el repositorio, donde está el tablero; si encuentra diferencias, se reemplaza este archivo por la versión corregida.
- Cuando cambie el ritual de forma que afecte la estructura del censo, se reemplaza por un censo nuevo ejecutado con esa versión.
