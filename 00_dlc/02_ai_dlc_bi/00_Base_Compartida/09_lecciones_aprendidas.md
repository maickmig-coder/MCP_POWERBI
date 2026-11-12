# 17. REGISTRO DE ERRORES Y LECCIONES APRENDIDAS

Toda nueva incidencia relevante debe convertirse en conocimiento reutilizable.

Formato:

## Error
¿Qué ocurrió?

## Causa
¿Por qué ocurrió?

## Impacto
¿Qué afectó?

## Solución
¿Qué se hizo?

## Regla preventiva
¿Qué debe hacer el AI-DLC para evitar que vuelva a ocurrir?

## Validación automática
¿Cómo puede detectarse antes de entregar?

## Incorporación
- Versión:
- Fecha:
- Documento/regla actualizada:

---

# Lecciones registradas

## Lección: optimizar antes de cargar (Depuración)
- **Caso:** un BI cargaba aproximadamente 20 millones de filas y unas 60 columnas. La optimización SQL y la eliminación de columnas no utilizadas redujeron el volumen a aproximadamente 1,3 millones de filas.
- **Causa/oportunidad:** datos y columnas innecesarios llegaban al modelo antes de ser descartados.
- **Impacto observado en el caso:** menor volumen de datos procesados/cargados. No generalizar la cifra como garantía de rendimiento.
- **Regla preventiva:** revisar filtros, columnas seleccionadas, joins y transformaciones en origen/consulta antes de cargar; validar semántica, granularidad y resultados.
- **Validación:** comparar filas, columnas, resultados de negocio, tiempo de refresh y tamaño del modelo antes/después cuando se pueda medir.

## Lección: una coincidencia textual no demuestra que un visual esté roto (V9.5, Depuración)
- **Caso observado:** durante una depuración de `GC - Flotillas` desapareció el visual `Participación por convenio (unidades año)` de `Dashboard_Convenios`, aunque era un visual válido según la información funcional disponible.
- **Causa técnica más respaldada:** se utilizó una búsqueda textual amplia sobre el contenido completo de `visual.json` para seleccionar carpetas y después se eliminó recursivamente la carpeta del visual. Esa condición podía coincidir con referencias secundarias o residuales, no solo con campos activos inválidos.
- **Límite de evidencia:** no se confirma que el título duplicado fuera la causa; la causa exacta por visual requiere comparar el PBIP original, el JSON original y la lista exacta de rutas seleccionadas.
- **Impacto:** eliminación accidental de un visual válido y pérdida de integridad funcional aunque las validaciones estáticas pudieran pasar.
- **Solución preventiva:** inventario por ID, análisis semántico de la referencia, lista positiva de objetos aprobados y comparación antes/después por página e ID. Restaurar/revertir si desaparece un objeto no aprobado.
- **Validación automática:** detectar diferencias de inventario; bloquear cierre si un ID desaparece sin acción aprobada; comprobar que el número de objetos eliminados coincide con la lista aprobada; validar JSON/codificación y separar controles técnicos de funcionales.

## Lección: un censo de una versión anterior no describe el tablero final (2026-11-12)
- **Caso:** la copia de trabajo `01_kiro` se ordenaba después de `00_original` y el censo la tomaba como «versión más reciente sin censar»; por el contrario, un tablero cambiado y guardado sin censar podía seguir usándose con su censo viejo.
- **Regla preventiva:** `01_kiro` no es una versión; Modificación y Depuración solo parten de un censo que `censo.py vigencia` declare VIGENTE y APTO; cada versión entregada se guarda como versión nueva y se censa antes de cerrar. El diccionario marca los censos que no describen el tablero final.
- **Validación automática:** `censo.py vigencia` (versión y huella del PBIP); `censo.py borrador` bloquea censar `01_kiro`; `diccionario.py` avisa «NO describe el tablero final».
