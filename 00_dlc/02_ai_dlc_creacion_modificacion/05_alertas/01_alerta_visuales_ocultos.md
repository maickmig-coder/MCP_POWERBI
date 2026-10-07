# 15. EJEMPLO — ALERTA DE VISUALES OCULTOS

## Hallazgo

Se detectan visuales con campos o medidas inexistentes que no aparecen en la
navegación normal.

## Posible causa

El BI fue creado a partir de una copia y algunos visuales heredados quedaron
asociados a marcadores o botones.

## Alerta

> ⚠️ Novedad detectada
>
> Se detectaron varios gráficos ocultos mediante marcadores que contienen
> campos o medidas que ya no existen en el modelo.
>
> Estos elementos pueden no ser visibles durante la navegación normal.
>
> Para revisarlos en Power BI Desktop:
> **Vista → Selección** para localizar objetos ocultos y
> **Vista → Marcadores** para identificar estados.
>
> No se eliminaron ni modificaron automáticamente.

## Regla

Los hallazgos ocultos deben informarse de forma comprensible y no deben
eliminarse automáticamente salvo autorización o alcance explícito.
