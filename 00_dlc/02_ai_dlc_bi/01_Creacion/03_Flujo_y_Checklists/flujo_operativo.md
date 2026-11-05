# FLUJO OPERATIVO — CREACIÓN

```text
Solicitud de BI nuevo
        ↓
Confirmar que es creación (no modificación ni depuración)
        ↓
Confirmar nombre exacto y los dos correos obligatorios
        ↓
Crear README histórico y actualizar registro central
        ↓
Crear carpeta de trabajo en 01_kiro
        ↓
Levantar contexto, finalidad, público, alcance y criterios de aceptación
        ↓
Definir fuentes, reglas de negocio y seguridad
        ↓
Preguntar: ¿usuario define KPIs o desea propuestas de IA?
        ↓
Aprobar definiciones de KPI y fórmulas
        ↓
Preguntar: ¿usuario define gráficos o desea propuestas de IA?
        ↓
Aprobar páginas, visuales, filtros, navegación e interacciones
        ↓
Diseñar modelo semántico, relaciones, calendario, transformaciones y DAX
        ↓
Confirmar diseño y alcance antes de construir
        ↓
Implementar exclusivamente en la copia Kiro
        ↓
Validar fuentes, modelo, cifras, seguridad, visuales y actualización
        ↓
Ejecutar pruebas de aceptación y revisar integridad/rendimiento
        ↓
¿Hay bloqueantes o diferencias críticas?
   ├── Sí → registrar alerta, bloquear entrega y corregir/aprobar plan
   └── No → documentar evidencia y decisiones
        ↓
Preparar versión/referencia candidata y obtener aceptación
        ↓
Proteger versión base aprobada en 00_original mediante mecanismo autorizado
        ↓
Actualizar README, registro central y documentación
        ↓
Confirmar cierre: Listo para entrega
```

## Secuencia obligatoria

1. **Clasificación:** si el BI ya existe y el trabajo lo altera o depura, no continuar como creación.
2. **Trazabilidad:** solicitar únicamente el correo de quien trabaja/modifica y el correo de quien solicita/es dueño para el control de personas.
3. **Rutas:** README y trazabilidad en `MCP_POWERBI\01_bi\01_versiones\00_original\[Nombre exacto BI]\`; desarrollo en `MCP_POWERBI\01_bi\01_versiones\01_kiro\[Nombre exacto BI]\`.
4. **CENSO:** marcar `No aplica` para un BI verdaderamente nuevo. Si se descubre que se parte de un BI existente, reclasificar la solicitud antes de intervenir.
5. **Aprobaciones:** no convertir propuestas de IA en requisitos ni construir KPIs/visuales de negocio pendientes de aprobación.
6. **Validación:** registrar pruebas realizadas y evidencia. No declarar que una prueba pasó si no fue ejecutada.
7. **Liberación:** no sobrescribir versiones aprobadas; registrar la versión liberada y conservar reversibilidad.

## Cierre

El estado `Listo para entrega` solo se permite cuando los criterios de aceptación están satisfechos, las validaciones aplicables se ejecutaron, los bloqueantes están cerrados, la versión entregada está identificada y la documentación quedó actualizada. Los controles no aplicables se justifican.
