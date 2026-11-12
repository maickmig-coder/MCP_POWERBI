# 9. RENDIMIENTO, DAX Y OPTIMIZACIÓN

## Cadena de optimización

Fuente
→ SQL/consulta
→ Power Query
→ Modelo
→ DAX
→ Visual

La revisión debe buscar la capa más eficiente para resolver el problema.

## Principios

1. Filtrar lo antes posible cuando sea funcionalmente correcto.
2. Seleccionar solo columnas necesarias.
3. Evitar cargar información que después se elimina.
4. Revisar joins.
5. Evitar transformaciones redundantes.
6. Reutilizar medidas.
7. Evitar cálculos duplicados.
8. Evaluar si una transformación pertenece a SQL, Power Query, modelo o DAX.
9. Medir antes/después cuando sea posible.
10. No sacrificar exactitud por rendimiento sin aprobación.

## Recomendaciones

Toda recomendación debe contener:
- hallazgo;
- causa;
- propuesta;
- beneficio esperado;
- impacto/riesgo;
- decisión del analista;
- validación posterior.


## Dependencias y registro de impacto

Para cambios con impacto técnico o funcional se debe registrar la relación
entre elemento modificado, dependencia, impacto y nivel de riesgo.

La matriz debe acompañar el Registro de Cambio cuando corresponda.
