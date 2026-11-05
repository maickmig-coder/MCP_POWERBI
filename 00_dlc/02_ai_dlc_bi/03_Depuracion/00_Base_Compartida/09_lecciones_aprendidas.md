# Lecciones aprendidas — Depuración y Mejora

## Lección: optimizar antes de cargar
- **Caso:** un BI cargaba aproximadamente 20 millones de filas y unas 60 columnas. La optimización SQL y la eliminación de columnas no utilizadas redujeron el volumen a aproximadamente 1,3 millones de filas.
- **Causa/oportunidad:** datos y columnas innecesarios llegaban al modelo antes de ser descartados.
- **Impacto observado en el caso:** menor volumen de datos procesados/cargados. No generalizar la cifra como garantía de rendimiento.
- **Regla preventiva:** revisar filtros, columnas seleccionadas, joins y transformaciones en origen/consulta antes de cargar; validar semántica, granularidad y resultados.
- **Validación:** comparar filas, columnas, resultados de negocio, tiempo de refresh y tamaño del modelo antes/después cuando se pueda medir.

## Registro de futuras lecciones
Para cada nueva incidencia documentar: error, causa, impacto, solución, regla preventiva, validación automática, versión/fecha y archivo actualizado.


## Lección: una coincidencia textual no demuestra que un visual esté roto (V9.5)
- **Caso observado:** durante una depuración de `GC - Flotillas` desapareció el visual `Participación por convenio (unidades año)` de `Dashboard_Convenios`, aunque era un visual válido según la información funcional disponible.
- **Causa técnica más respaldada:** se utilizó una búsqueda textual amplia sobre el contenido completo de `visual.json` para seleccionar carpetas y después se eliminó recursivamente la carpeta del visual. Esa condición podía coincidir con referencias secundarias o residuales, no solo con campos activos inválidos.
- **Límite de evidencia:** no se confirma que el título duplicado fuera la causa; la causa exacta por visual requiere comparar el PBIP original, el JSON original y la lista exacta de rutas seleccionadas.
- **Impacto:** eliminación accidental de un visual válido y pérdida de integridad funcional aunque las validaciones estáticas pudieran pasar.
- **Solución preventiva:** inventario por ID, análisis semántico de la referencia, lista positiva de objetos aprobados y comparación antes/después por página e ID. Restaurar/revertir si desaparece un objeto no aprobado.
- **Validación automática:** detectar diferencias de inventario; bloquear cierre si un ID desaparece sin acción aprobada; comprobar que el número de objetos eliminados coincide con la lista aprobada; validar JSON/codificación y separar controles técnicos de funcionales.
