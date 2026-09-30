# Criterios para propuestas de revisión IA

## Objetivo

Definir cuándo la IA debe proponer un nuevo punto de revisión durante el censo.

## 1. La propuesta debe nacer de una evidencia

Una propuesta es válida cuando el análisis encuentra algo que:

- No está contemplado en el checklist.
- Puede afectar la comprensión del BI.
- Presenta una dependencia desconocida.
- Presenta una regla no documentada.
- Presenta una inconsistencia.
- Presenta información incompleta.
- Presenta un comportamiento técnico relevante.

## 2. Categorías de propuestas

### A. Gobierno

Ejemplos:

- Propietario no identificado.
- Responsable funcional desconocido.
- Responsable técnico desconocido.

### B. Datos

Ejemplos:

- Fuente sin descripción.
- Granularidad no identificada.
- Origen de dato desconocido.
- Transformación compleja no documentada.

### C. Modelo

Ejemplos:

- Relación cuya lógica no está clara.
- Tabla con función desconocida.
- Clave sin documentación.
- Dependencia entre tablas no evidente.

### D. Negocio

Ejemplos:

- KPI sin definición funcional.
- Clasificación sin explicación.
- Regla de negocio inferida pero no confirmada.

### E. Reporte

Ejemplos:

- Visual cuyo propósito no es claro.
- Página oculta sin finalidad identificada.
- Filtro cuyo comportamiento no puede determinarse.

### F. Actualización

Ejemplos:

- Frecuencia desconocida.
- Proceso de actualización no identificado.
- Dependencia externa no documentada.

### G. Calidad

Ejemplos:

- Tratamiento inconsistente de nulos.
- Duplicidad potencial.
- Campos con valores inesperados.
- Reglas de limpieza relevantes.

## 3. Estructura obligatoria

Toda propuesta debe contener:

| Campo | Obligatorio |
|---|---|
| Propuesta | Sí |
| Categoría | Sí |
| Motivo | Sí |
| Evidencia | Sí |
| Impacto | Sí |
| Prioridad | Sí |
| Requiere validación | Sí |

## 4. Prioridad

### Alta

Puede afectar significativamente la comprensión del BI o un KPI.

### Media

Puede afectar una parte del análisis o existe una dependencia relevante.

### Baja

Mejora la documentación o comprensión, pero no parece afectar el análisis principal.

## 5. No proponer modificaciones

Las propuestas de este proceso deben ser propuestas de **revisión o levantamiento de información**, no instrucciones para modificar el BI.

Ejemplo correcto:

> Revisar la lógica de deduplicación porque se detectó una regla compleja cuyo propósito funcional no está documentado.

Ejemplo incorrecto:

> Cambiar la lógica de deduplicación.

## 6. Principio de evidencia

La IA debe poder responder:

> ¿Qué encontraste que te llevó a proponer esto?

Si no puede responderlo, la propuesta no debe incluirse.
