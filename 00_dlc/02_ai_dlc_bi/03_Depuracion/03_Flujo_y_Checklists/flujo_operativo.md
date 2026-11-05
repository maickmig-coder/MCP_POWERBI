# Flujo operativo — Depuración y Mejora

```text
Solicitud
  ↓
Clasificar como Depuración/Mejora y fijar alcance/exclusiones
  ↓
Registrar los dos correos y abrir el histórico existente
  ↓
Buscar CENSO en MCP_POWERBI\02_censo
  ├─ Ausente / incorrecto / inaccesible → BLOQUEAR y ejecutar ritual CENSO
  └─ Válido → continuar
  ↓
Proteger PBIP original en 00_original
  ↓
Preparar copia de trabajo en 01_kiro
  ↓
Capturar línea base y evidencia
  ↓
Inventariar fuentes, consultas, modelo, DAX, visuales y dependencias
  ↓
Crear inventario de visuales por ID y línea base antes de cambios
  ↓
Clasificar referencias sospechosas semánticamente; regex solo localiza candidatos
  ↓
Presentar lista positiva de objetos exactos y obtener aprobación por objeto/grupo enumerado
  ↓
Clasificar hallazgos + causa + impacto + riesgo + beneficio esperado
  ↓
¿Se requiere revisión de consultas/fuentes? → preguntar si no está en alcance
  ↓
Proponer acciones y rollback; obtener decisión del analista
  ├─ Rechazado/Pendiente → documentar; no ejecutar
  └─ Aprobado → ejecutar solo la acción aprobada sobre 01_kiro
  ↓
Ejecutar por etapas en 01_kiro; validar tras cada grupo
  ↓
Comparar inventarios antes/después por ID y página; conciliar toda diferencia
  ↓
Pruebas técnicas y funcionales separadas: exactitud, visuales, navegación, refresh y rendimiento aplicable
  ↓
¿Pruebas pasan y diferencias explicadas?
  ├─ No → detener, corregir o revertir; registrar incidente
  └─ Sí → actualizar README, Registro de Cambio y registro central
  ↓
Comunicar beneficios medidos, alertas y riesgos residuales
  ↓
Listo para entrega si no quedan bloqueantes
```

## Reglas de ejecución
1. El original de `00_original` es de solo referencia; no editarlo.
2. La copia de trabajo se ubica en `MCP_POWERBI\01_bi\01_versiones\01_kiro\[Nombre exacto BI]`.
3. El CENSO es requisito bloqueante para cualquier depuración de BI existente.
4. El CENSO describe estado actual; no constituye aprobación de cambios.
5. No eliminar ni reemplazar campos, medidas, consultas o visuales sin aprobación explícita.
6. Mantener separados los cambios de integridad/rendimiento de los cambios funcionales o estéticos.
7. Si un hallazgo requiere cambiar alcance, pausar esa parte y registrar una solicitud separada de Modificación cuando corresponda.


## Bloqueo adicional V9.5

- Aplicar `00_Base_Compartida/16_protocolo_integridad_visuales_eliminacion_segura.md` y la matriz `02_Plantillas/04_inventario_visual_y_eliminacion_segura.md` antes de cambios destructivos en visuales, bookmarks, botones o estados.
- Una coincidencia textual no confirma un visual roto. No ejecutar borrados recursivos desde resultados de búsqueda sin verificación semántica y lista positiva aprobada.
- Si desaparece un visual/objeto sin aprobación exacta, detener la ejecución y restaurar/revertir antes de seguir.
- Si no se pudo probar el comportamiento en Power BI Desktop o no se ejecutó el refresh, registrar la prueba como `No validado`; no declarar integridad funcional completa.
