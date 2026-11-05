# 8. VALIDACIÓN E INTEGRIDAD

## Objetivo

Validar el BI completo, no solamente el cambio solicitado.

## Revisar

### Visuales
- visibles;
- ocultos;
- campos;
- medidas;
- entidades;
- títulos;
- configuración.

### Estados
- bookmarks;
- botones;
- selección;
- visibilidad;
- estados alternativos.

### Modelo
- tablas;
- columnas;
- medidas;
- relaciones;
- dependencias;
- granularidad.

### Diseño
- layout;
- posiciones;
- tamaños;
- alineación;
- jerarquía;
- consistencia.

### Archivos
- estructura;
- PBIR/TMDL/JSON cuando correspondan;
- referencias;
- sintaxis;
- codificación;
- UTF-8 sin BOM cuando sea requerido;
- integridad.

## Visuales ocultos

Caso obligatorio a revisar:
analistas pueden copiar un BI y dejar visuales heredados ocultos mediante
marcadores/botones. Pueden contener campos o medidas que ya no existen.

Alerta ejemplo:

> ⚠️ Novedad detectada
>
> Se detectaron visuales ocultos mediante marcadores que contienen campos o
> medidas inexistentes.
>
> Para revisarlos en Power BI Desktop:
> Vista → Selección
> y
> Vista → Marcadores.
>
> No se eliminaron automáticamente.

La alerta debe explicar:
1. qué;
2. dónde;
3. por qué importa;
4. cómo localizar;
5. acción posible.

## Severidad

- Bloqueante: impide una entrega confiable.
- Advertencia: requiere revisión.
- Información: hallazgo sin impacto bloqueante.

## Regla de no intervención automática

No eliminar ni modificar hallazgos fuera del alcance aprobado.

## Validación antes/después

Para cambios de datos, modelo o DAX:
- comparar resultado previo;
- comparar resultado posterior;
- validar diferencias;
- documentar diferencias esperadas.

## Cierre

Registrar:
- cambios;
- validaciones;
- alertas;
- pendientes;
- decisiones.


## Validación antes/después del cambio

Cuando el cambio lo permita, la validación debe comparar el estado anterior
contra el posterior, considerando según aplique:

- KPIs.
- Totales.
- Conteos.
- Filtros.
- Medidas.
- Relaciones.
- Visuales afectados.
- Rendimiento.

Los resultados deben quedar en el Registro de Cambio.


## Controles reforzados para Depuración

- Capturar estado antes y después con evidencia.
- Verificar KPIs, totales, conteos, filtros y contexto de cálculo afectados.
- Revisar refresh, conexiones, relaciones, RLS y navegación cuando correspondan.
- Revisar visuales ocultos, marcadores, botones y objetos heredados.
- Investigar diferencias no esperadas y no cerrar con pruebas críticas fallidas.
- No declarar mejora de rendimiento sin métrica comparable o evidencia explícita; indicar limitaciones de medición.
- Verificar reversibilidad según el riesgo.


## Control V9.5 — Inventario y preservación de visuales

Antes de cualquier eliminación de visuales, aplicar el protocolo `16_protocolo_integridad_visuales_eliminacion_segura.md`.

- Inventariar por ID técnico y página; el título no es clave única.
- Tratar búsquedas de texto/regex como localizadores de candidatos, nunca como prueba única.
- Aprobar acciones sobre IDs exactos antes de ejecutar.
- Comparar inventario antes/después por página e ID.
- Bloquear cierre ante cualquier desaparición no autorizada o diferencia no conciliada.
- Informar integridad técnica y funcional por separado.
- Si Power BI Desktop, refresh o una prueba funcional no se ejecutó, dejar constancia de `No validado`.
