# CONSOLIDACIÓN V6 — CENSO Y PBIP PARA MODIFICACIONES

## Regla incorporada

Cuando se solicite modificar un BI existente y no exista CENSO:

- la modificación queda bloqueada;
- se conserva el PBIP original;
- el PBIP se guarda en `NIGGA\01_bi\01_versiones\00_original\[Nombre exacto BI]\`;
- se ejecuta el ritual `NIGGA\00_dlc\01_ai-dlc-censo`;
- el resultado se guarda en `NIGGA\02_censo`;
- se verifica el CENSO;
- solo después se habilita la modificación.

## Integridad de versiones anteriores

Esta incorporación es aditiva. No elimina ni reemplaza las reglas existentes de:

- Creación.
- Modificación.
- Depuración y Mejora.
- Diseño corporativo.
- Integridad.
- Rendimiento.
- DAX.
- Fuentes y consultas.
- Visuales ocultos.
- Marcadores.
- Dependencias.
- Decisiones del analista.
- Validaciones antes/después.
- Registro de cambios.
- README histórico.
- Control por correo.
- Encoding.
- Control de versiones.
- Alertas y cierre.

## Estado

Esta regla se considera **BLOQUEANTE** para modificación de BI existente.
