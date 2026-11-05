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


## Control reforzado de edición segura (V9.5)

Antes de modificar un archivo, conservar una copia recuperable y registrar su ruta; cuando sea posible, calcular hash antes/después. Tras escribirlo, volver a leerlo, revisar el diff, comprobar BOM y caracteres acentuados, y validar sintaxis/estructura. Para JSON, el parseo debe terminar sin errores. Para TMDL, validar con herramientas disponibles y declarar las limitaciones.

No hacer reemplazos masivos sobre texto serializado sin comprender el contexto estructural. Una coincidencia textual puede estar en metadatos o en una referencia secundaria. Si se detecta mojibake, truncamiento o estructura alterada, detenerse y restaurar desde una copia íntegra antes de re-aplicar el cambio aprobado.
