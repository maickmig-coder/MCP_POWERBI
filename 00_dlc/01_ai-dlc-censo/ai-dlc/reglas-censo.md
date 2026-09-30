# Reglas del censo AI-DLC

Estas reglas son obligatorias durante el análisis de cualquier BI.

## Regla 1 — No asumir

La IA no debe presentar como hecho información que no pueda sustentar.

Clasificar la información como:

- `Encontrado`
- `Inferido`
- `Desconocido`

## Regla 2 — Evidencia

Cada hallazgo relevante debe indicar de dónde proviene la evidencia.

Ejemplos de evidencia:

- Archivo.
- Tabla.
- Columna.
- Medida.
- Consulta.
- Visual.
- Configuración.
- Código.
- Relación.

## Regla 3 — No modificar

El proceso de censo es únicamente de descubrimiento y documentación.

No:

- Modificar código.
- Eliminar campos.
- Crear medidas.
- Cambiar relaciones.
- Modificar visuales.
- Desplegar cambios.

## Regla 4 — Identificar uso y no uso

La IA debe identificar tanto:

- Elementos utilizados.
- Elementos no utilizados.

No asumir que un elemento no utilizado es innecesario.

## Regla 5 — Separar no uso de desconocimiento

`No utilizado` significa que no se encontró consumo.

`Uso desconocido` significa que no existe evidencia suficiente para determinar su propósito.

No deben confundirse.

## Regla 6 — Identificar vacíos

La IA debe identificar información importante que no pudo determinar.

Un vacío no significa necesariamente un error del BI.

Significa que existe una pieza de conocimiento pendiente.

## Regla 7 — Propuestas basadas en evidencia

La IA debe proponer nuevos puntos de revisión cuando encuentre señales relevantes.

Toda propuesta debe responder:

> ¿Por qué se propone revisar esto?

## Regla 8 — No generar propuestas genéricas

No llenar la sección de propuestas con recomendaciones estándar sin relación con la evidencia del BI.

## Regla 9 — Mantener separación técnico/funcional

Cuando sea posible, documentar:

- Qué hace técnicamente.
- Qué significa funcionalmente.

## Regla 10 — No confundir inferencia con regla de negocio

Una regla de negocio debe estar respaldada por la lógica encontrada o por información funcional disponible.

Si solo puede inferirse, indicarlo.

## Regla 11 — Documentar limitaciones

Si no fue posible acceder a una fuente, archivo, configuración o información funcional, documentarlo.

## Regla 12 — Cierre obligatorio

Un censo no se considera completo hasta revisar:

- Checklist.
- Elementos no utilizados.
- Vacíos.
- Propuestas de revisión.
- Limitaciones.
