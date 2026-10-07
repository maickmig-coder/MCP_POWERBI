# AI-DLC — Ritual estándar para el censo de BI

## 1. Propósito

Aplicar un proceso estándar, repetible y trazable para conocer un BI desde sus dimensiones técnicas y funcionales.

El ritual debe poder aplicarse independientemente del área, tablero, tecnología o fuente de datos.

## 2. Alcance

El ritual contempla exclusivamente:

1. Ingreso del BI.
2. Censo técnico.
3. Censo funcional.
4. Identificación de elementos utilizados.
5. Identificación de elementos no utilizados.
6. Identificación de reglas de negocio.
7. Mapa de dependencias.
8. Detección de vacíos.
9. Propuestas de revisión de IA.
10. Consolidación.
11. Validación final.

No se deben realizar modificaciones al BI como parte de este ritual.

---

# 3. Ritual 1 — Ingreso del BI

### Objetivo

Registrar la información mínima necesaria para iniciar el censo.

### Responsables del censo

Antes de iniciar el censo, la IA debe solicitar obligatoriamente:

- Correo electrónico de la persona que realizará el censo.
- Correo electrónico del dueño/responsable del tablero.

Los correos deben registrarse como identificadores de referencia para la posterior homologación de nombres.

La IA no debe solicitar el nombre de las personas.

### Revisar

- Nombre del BI.
- Nombre del proyecto.
- Propósito conocido.
- Área de negocio.
- Responsable funcional, si está disponible.
- Responsable técnico, si está disponible.
- Tecnología.
- Ubicación del proyecto.
- Repositorio, si existe.
- Ambiente, si está disponible.
- Fuentes conocidas.
- Fecha del censo.
- Versión analizada.

### Regla

Si un dato no puede ser identificado, registrar `No identificado` o `Pendiente de confirmar`.

---

# 4. Ritual 2 — Censo técnico

### Objetivo

Inventariar los componentes técnicos que conforman el BI.

### Revisar

#### Fuentes

- Bases de datos.
- Archivos.
- APIs.
- Data Warehouse.
- Data Lake.
- Servicios cloud.
- Otras fuentes.

#### Transformaciones

- SQL.
- Power Query.
- DAX.
- Scripts.
- Procedimientos.
- Transformaciones intermedias.
- Consultas auxiliares.

#### Modelo

- Tablas.
- Columnas.
- Medidas.
- Relaciones.
- Cardinalidades.
- Dirección de filtro.
- Claves.
- Jerarquías.
- Granularidad.
- Hechos.
- Dimensiones.

#### Reporte

- Páginas.
- Visuales.
- Slicers.
- Filtros.
- Bookmarks.
- Botones.
- Navegación.
- Tooltips.
- KPIs.

### Identificación de visuales

Para cada visual, la IA debe identificar obligatoriamente:

- Página.
- Nombre o título visible del visual.
- Tipo de visual.
- Campos/Categorías.
- Medidas.
- Filtros.
- Propósito o notas relevantes.

Si el visual no tiene título visible, debe registrarse como:

`Sin título visible`

La IA no debe inventar un nombre para el visual.

#### Presentación

- Tema.
- Colores.
- Fuentes.
- Fondos.
- Formatos.

---

# 5. Ritual 3 — Censo funcional

### Objetivo

Comprender qué representa el BI y para qué se utiliza.

### Revisar

- Objetivo.
- Problema de negocio.
- Usuarios.
- Áreas consumidoras.
- Procesos representados.
- Indicadores.
- KPIs.
- Dimensiones.
- Filtros.
- Segmentaciones.
- Definiciones.
- Periodo de información.
- Frecuencia de actualización, si puede determinarse.

### Pregunta central

> ¿Qué información intenta entregar este BI y para qué se utiliza?

---

# 6. Ritual 4 — Elementos utilizados

### Objetivo

Determinar qué elementos tienen consumo real.

Establecer, cuando sea posible:

`Elemento → Tabla/objeto → Visual → Página → Función`

Registrar como mínimo:

- Campo.
- Tabla.
- Tipo.
- Uso.
- Visual.
- Página.
- Función.

---

# 7. Ritual 5 — Elementos NO utilizados

### Objetivo

Detectar elementos existentes que no presentan consumo identificado.

Revisar:

- Columnas.
- Medidas.
- Tablas.
- Relaciones.
- Consultas.
- Parámetros.
- Visuales.
- Páginas.
- Campos.
- Elementos técnicos.

### Clasificación

- `No utilizado`
- `Uso técnico`
- `Uso desconocido`
- `Posible obsoleto`
- `Requiere validación`

### Regla

No concluir que un elemento puede eliminarse. El censo solamente debe identificarlo y documentar la evidencia disponible.

---

# 8. Ritual 6 — Reglas de negocio

### Objetivo

Reconstruir las reglas que convierten datos en información de negocio.

Revisar:

- Fórmulas.
- Condiciones.
- Clasificaciones.
- Estados.
- Segmentaciones.
- Deduplicaciones.
- Homologaciones.
- Tratamiento de nulos.
- Tratamiento de errores.
- Reglas temporales.
- Inclusiones.
- Exclusiones.
- Cálculos derivados.

Documentar cada regla en:

1. Implementación técnica.
2. Interpretación funcional.
3. Evidencia.

---

# 9. Ritual 7 — Dependencias

### Objetivo

Comprender cómo se relacionan los componentes.

Construir, cuando sea posible:

`Fuente → Consulta → Transformación → Tabla → Campo → Medida → Visual → Página → KPI`

Identificar:

- Dependencias directas.
- Dependencias indirectas.
- Elementos centrales.
- Elementos aislados.
- Concentraciones de lógica.

---

# 10. Ritual 8 — Vacíos del censo

### Objetivo

Identificar información que sería necesaria para comprender completamente el BI pero que no pudo determinarse.

Preguntar:

> ¿Qué debería saber sobre este BI para poder afirmar que lo conozco y todavía no puedo determinar?

Ejemplos:

- Fuente sin propietario.
- KPI sin definición.
- Tabla sin granularidad conocida.
- Campo sin descripción.
- Relación sin lógica clara.
- Proceso de actualización desconocido.
- Dependencia externa desconocida.
- Regla de negocio implícita.
- Responsable no identificado.
- Origen de dato no identificado.

---

# 11. Ritual 9 — Propuestas de revisión IA

### Objetivo

Permitir que la IA identifique aspectos adicionales que no estén contemplados en el checklist.

Toda propuesta debe contener:

- Propuesta.
- Motivo.
- Evidencia.
- Impacto.
- Prioridad.
- Requiere validación.

### Regla

No generar propuestas genéricas. Cada propuesta debe estar sustentada en evidencia encontrada durante el censo.

---

# 12. Ritual 10 — Consolidación

Consolidar en un único censo:

1. Identificación.
2. Objetivo.
3. Alcance.
4. Fuentes.
5. Transformaciones.
6. Modelo.
7. Tablas.
8. Columnas.
9. Medidas.
10. Relaciones.
11. Páginas.
12. Visuales.
13. KPIs.
14. Filtros.
15. Elementos utilizados.
16. Elementos no utilizados.
17. Reglas de negocio.
18. Dependencias.
19. Vacíos.
20. Propuestas IA.
21. Hallazgos.
22. Limitaciones.

---

# 13. Ritual 11 — Validación final

Verificar:

### Cobertura
¿Se revisaron los componentes disponibles?

### Consistencia
¿El documento coincide con la evidencia del BI?

### Trazabilidad
¿Las afirmaciones importantes tienen evidencia?

### Completitud
¿Quedaron elementos sin clasificar?

### Vacíos
¿Quedaron preguntas relevantes sin respuesta?

### Propuestas
¿Se revisó si el BI requiere puntos adicionales de análisis?

---

# 14. Resultado

El producto final del ritual es un **censo técnico y funcional validado**, no una modificación del BI.

El flujo final es:

`Censar → Entender → Detectar → Proponer → Documentar → Validar`
