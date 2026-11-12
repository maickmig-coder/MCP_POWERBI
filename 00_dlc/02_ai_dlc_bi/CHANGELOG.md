# CHANGELOG — AI-DLC de tableros (Creación, Modificación, Depuración)

Los cambios anteriores de cada proceso están en su `04_Control_de_Versiones/`.

## V11 — 2026-11-12 · Base única y censo del tablero final

**Una sola base compartida.** Las tres copias de `00_Base_Compartida` (que ya diferían en 9 de 15 documentos) se
reemplazaron por `00_dlc/02_ai_dlc_bi/00_Base_Compartida/`, tomada de Creación (diseño V10, diccionario de datos):
- `01_rutas_y_censo.md` reescrito como documento común: rutas, versiones, copia de trabajo, puerta del censo por
  proceso y trazabilidad.
- Los checklists integrales (antes `14_checklist_integral.md`) pasan a `03_Flujo_y_Checklists/checklist_integral.md`
  de cada proceso, porque son distintos por naturaleza.
- Lo propio de Depuración que estaba en la base (controles reforzados de integridad, edición segura y rendimiento;
  alcance visual) pasa a `03_Depuracion/01_Reglas_del_Proceso/controles_reforzados_depuracion.md`; el protocolo de
  eliminación segura, a `03_Depuracion/01_Reglas_del_Proceso/`.
- Las lecciones aprendidas de Depuración se suman a `09_lecciones_aprendidas.md` común.
- Modificación y Depuración pasan del diseño V9 al V10 (con su regla de aplicación por proceso) y a la ruta correcta
  del logo (`02_ai_dlc_bi\00_fuentes\Logo_Nebula.png`; antes apuntaban a `02_ai_dlc_creacion_modificacion`).

**Censo del tablero final (ritual del censo v2.3.6).** Modificación y Depuración solo parten de un censo que
`censo.py vigencia` declare VIGENTE y APTO; preparan la copia desde la última versión guardada; al cerrar guardan la
versión nueva `NN_<proceso>_<ID>` y la censan (`Actualización`). Creación guarda `00_original` y la censa (`Inicial`).

**Trazabilidad en la salida del censo.** El README de cada tablero y el registro central pasan de `01_versiones\00_original`
a `02_censo\[BI]\README.md` y `02_censo\REGISTRO_CONTROL_TABLEROS.md`: `01_versiones` queda solo para versiones.

**Diccionario por proceso.** Modificación aplica la regla 16 si agrega fuentes; Depuración solo depura y no agrega.

Respaldo de la estructura anterior: historial de git (commit previo a este cambio).
