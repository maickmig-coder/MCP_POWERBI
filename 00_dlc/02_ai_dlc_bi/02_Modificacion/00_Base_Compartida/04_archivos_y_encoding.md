# 10. ARCHIVOS Y CODIFICACIÓN

## UTF-8

Power BI puede requerir archivos de texto en UTF-8 sin BOM.

No asumir que:
`Set-Content -Encoding UTF8`
garantiza UTF-8 sin BOM en todos los entornos.

## Regla preventiva

Después de crear o modificar archivos:
1. identificar archivos afectados;
2. validar codificación;
3. comprobar BOM;
4. corregir si corresponde;
5. volver a validar.

## Lección aprendida

Error → causa → impacto → solución → regla preventiva → validación automática.

Esta estructura debe utilizarse para nuevos errores técnicos que aparezcan.
