# CHECKLIST INTEGRAL — CREACIÓN DE BI

Marcar `No aplica` con motivo cuando un control no corresponda. No declarar el BI listo si existe un bloqueo de seguridad, exactitud, integridad o aceptación.

## A. Inicio y alcance
- [ ] Se confirmó que es un BI nuevo y no una modificación/depuración disfrazada.
- [ ] Nombre exacto del BI aprobado.
- [ ] Correo de quien trabaja/modifica registrado.
- [ ] Correo de quien solicita/es dueño registrado.
- [ ] README histórico creado en la carpeta de trazabilidad.
- [ ] Registro central actualizado.
- [ ] Objetivo, público, decisiones a soportar y alcance definidos.
- [ ] Requisitos obligatorios separados de propuestas de IA.
- [ ] Criterios de aceptación y exclusiones documentados.
- [ ] Decisiones y aprobaciones registradas.
- [ ] Nivel de riesgo inicial definido.
- [ ] Carpeta de trabajo Kiro creada y ruta verificada.
- [ ] CENSO marcado `No aplica` por ser creación nueva; si parte de un BI existente, se reclasificó la solicitud.

## B. Fuentes y acceso
- [ ] Sistemas, servidores, motores, bases, esquemas, tablas/vistas y archivos identificados.
- [ ] Método de conexión y entorno (desarrollo/pruebas/producción) documentados.
- [ ] Accesos autorizados verificados sin guardar contraseñas, tokens ni secretos en archivos.
- [ ] Dueño de la fuente y restricciones de uso identificados cuando estén disponibles.
- [ ] Frecuencia de actualización y ventana de disponibilidad acordadas.
- [ ] Gateway, credenciales administradas, permisos de servicio y dependencias de actualización revisados cuando aplique.
- [ ] Calidad de fuente: duplicados, nulos, claves, tipos, fechas, granularidad y cobertura evaluados.
- [ ] SQL, Power Query, Dataflows/Flows, Excel y archivos se documentan cuando aplican.
- [ ] Filtros de origen y selección de columnas se evalúan por necesidad funcional y volumen; no se eliminan campos unilateralmente.

## C. Reglas de negocio y KPIs
- [ ] Definiciones de negocio, fórmulas, excepciones y responsables de validación documentados.
- [ ] Cada KPI tiene nombre, propósito, fórmula/lógica, campos requeridos, granularidad y formato.
- [ ] Se preguntó si el usuario define los KPIs o desea propuestas de IA.
- [ ] Cada propuesta de IA quedó marcada como aprobada, rechazada o pendiente.
- [ ] Totales, periodos, monedas, zonas horarias y tratamiento de nulos definidos cuando aplican.
- [ ] Fuente de verdad y método de conciliación de cifras definidos.

## D. Modelo semántico y cálculos
- [ ] Granularidad de cada tabla definida.
- [ ] Tablas de hechos/dimensiones y claves identificadas.
- [ ] Relaciones, cardinalidad y dirección de filtro justificadas.
- [ ] Tabla calendario y relaciones de fecha definidas cuando aplican.
- [ ] Medidas reutilizables identificadas antes de crear lógica duplicada.
- [ ] Columnas calculadas, tablas calculadas, transformaciones y DAX tienen justificación.
- [ ] Tipos de datos, claves, valores nulos y calidad de relaciones validados.
- [ ] RLS y demás restricciones de seguridad diseñadas y probadas cuando aplican.
- [ ] No hay credenciales ni secretos incrustados en código, consultas o documentación.

## E. Páginas, visuales e interacción
- [ ] Cada página tiene propósito y público definidos.
- [ ] Se preguntó si el usuario define los gráficos o desea propuestas de IA.
- [ ] Cada visual tiene propósito, campos/medidas y página asignada.
- [ ] La ubicación responde a la mesa de trabajo; no se ubicaron visuales arbitrariamente.
- [ ] Jerarquía de filtros corporativos aplicada a los filtros que realmente existen.
- [ ] Títulos, nombres de campos y etiquetas corresponden al contenido real.
- [ ] Header, logo oficial, última actualización, separador, filtros, botones, KPIs, gráficos, tablas, leyendas y navegación validados.
- [ ] Contraste, legibilidad, consistencia y accesibilidad básica revisados.
- [ ] Marcadores, botones, navegación, tooltips, drill-through, drill-down, exportaciones e interacciones probados cuando aplican.
- [ ] Visuales ocultos y estados alternativos revisados; no hay objetos rotos heredados de plantillas/copias.

## F. Actualización, seguridad y operación
- [ ] Frecuencia de actualización acordada y documentada.
- [ ] Parámetros y rutas dependientes del entorno identificados.
- [ ] Prueba de actualización realizada o marcada pendiente con responsable.
- [ ] RLS probada con perfiles autorizados cuando aplica.
- [ ] Requisitos de exportación, retención y sensibilidad considerados.
- [ ] Dependencias de gateway, credenciales gestionadas y permisos de publicación documentados cuando aplican.

## G. Pruebas y rendimiento
- [ ] Cifras conciliadas con la fuente de verdad o evidencia de aceptación registrada.
- [ ] KPIs, totales, conteos, filtros y periodos probados.
- [ ] Relaciones, medidas, páginas e interacciones probadas.
- [ ] Volumen, cardinalidad, tamaño y tiempos de actualización/renderizado evaluados cuando es posible.
- [ ] Se midió antes/después si se hicieron optimizaciones.
- [ ] Diferencias no esperadas investigadas y explicadas.
- [ ] No se sacrificó exactitud por rendimiento sin aprobación.

## H. Artefactos, documentación y entrega
- [ ] Artefactos se encuentran en la copia Kiro.
- [ ] Formato PBIP y estructura de proyecto conservados cuando aplique.
- [ ] Tema JSON u otros activos corporativos documentados cuando se usaron.
- [ ] README histórico actualizado.
- [ ] Registro central actualizado.
- [ ] Registro de creación/decisiones completado; Registro de Cambio usado cuando corresponda.
- [ ] Documentación funcional y técnica guardada en `MCP_POWERBI\01_documentacion_tableros` cuando aplique.
- [ ] Archivos de texto comprobados para codificación y BOM conforme a requisitos.
- [ ] Alertas, riesgos, limitaciones y pendientes comunicados.
- [ ] Versión/referencia entregada identificada y mecanismo de reversibilidad verificado.
- [ ] Versión base aprobada protegida en `00_original` según el mecanismo autorizado.
- [ ] Registro central refleja estado final y correos obligatorios.
- [ ] Estado `Listo para entrega` sustentado por pruebas y aceptación.

## Bloqueos de Creación
No declarar `Listo para entrega` si falta la aprobación del alcance, hay discrepancias críticas sin resolver, la seguridad/RLS necesaria no está validada, la actualización no es operativa cuando es requisito, existen errores bloqueantes de integridad o no se puede identificar la versión entregada. Documentar la causa y el estado.
