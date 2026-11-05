# AI-DLC-CENSO (v2.3)

Ritual estándar para el **censo técnico y funcional de tableros Power BI guardados en PBIP**. El censo es la **base de conocimiento** sobre la que se planifica cualquier cambio. La modificación, creación y depuración son un **DLC aparte**; este ritual no las ejecuta ni las prescribe.

## Qué produce

En `MCP_POWERBI\02_censo\[Nombre exacto del BI]`:

| Archivo | Contenido |
|---|---|
| `[Nombre] - censo.md` | **Estado actual** del tablero: secciones 0–18 de la última versión censada, IDs nativos completos con su nombre, huella del PBIP en el encabezado. |
| `[Nombre] - cambios.md` | Registro de cambios entre versiones (append-only): qué se agregó, eliminó o modificó, por qué proceso (DLC de modificación o depuración) y qué respondió el dueño. |
| `versiones/` | Censos anteriores archivados, uno por ejecución. |
| `historial-censos.md` | Una fila por ejecución validada (append-only). |

**¿Este censo es el del tablero final?** Ejecute `censo.py vigencia`: responde VIGENTE o DESACTUALIZADO (comparando con la última versión guardada en `01_versiones` y con la huella del PBIP) y APTO o NO APTO para el DLC de modificación o depuración.

Cubre fuentes y conexiones, código M y sus pasos, tablas, columnas (uso por clase de dependencia), medidas, relaciones, seguridad, páginas, visuales (posición, tamaño y bindings), filtros, segmentaciones, interacciones, bookmarks, botones, **estética: banners, logos, imágenes, formas y textos con su ubicación en cada página, escala de cada imagen y ruta del archivo**, tema y metadatos.

## Cómo se reparte el trabajo

| Quién | Qué hace | Costo |
|---|---|---|
| `scripts/censo.py` | Lee el PBIP y escribe todo lo mecánico: inventarios, IDs, bindings, dependencias, clasificación de uso, conciliación, hallazgos detectables. Valida y registra. | Segundos, cero tokens |
| La IA (Kiro) | Completa unos 11 marcadores `[IA: …]`: área, objetivo, rol de tablas, interpretación de KPIs y reglas, mapa de arquitectura, revisión de hallazgos y estado final. | Una fracción de v2.0 |

## Estructura

```text
01_ai-dlc-censo/
├── README.md
├── CHANGELOG.md
├── ai-dlc/
│   ├── ritual-censo-bi.md            Fases, estructura del resultado y criterios de clasificación
│   ├── reglas-censo.md               Reglas R01–R51 (R03 retirada)
│   ├── catalogos.md                  Valores permitidos (CAT-01 a CAT-15) e IDs nativos
│   ├── checklist-censo.md            Qué genera el script, qué valida y qué revisa la IA
│   └── criterios-puntos-revision.md  Cómo registrar hallazgos sin prescribir cambios
├── kiro/
│   └── steering-censo-bi.md          Guía de ejecución para Kiro (copiar a .kiro/steering/)
├── scripts/
│   ├── censo.py                      Comandos: borrador, comparar, iniciar-validacion, pendientes, validar, registrar, vigencia, inventario
│   ├── censo_versiones.py            Huella del PBIP, comparación entre censos, traslado de validaciones y vigencia
│   ├── censo_lectura.py              Lectura de PBIR, TMDL, M y DAX (solo lectura)
│   └── censo_analisis.py             Dependencias y clasificación de uso
└── examples/
    ├── README.md                     Qué contiene el ejemplo y cómo usarlo
    └── GC - Flotillas - censo.md     Censo real de referencia (ritual v2.2.3; formato v2.3)
```

Requisitos: Python 3.9 o superior. No necesita paquetes externos.

## Uso

```bash
cd MCP_POWERBI/00_dlc/01_ai-dlc-censo
V="../../01_bi/01_versiones"; S="../../02_censo/Nombre BI"

# ¿Hay censo y está vigente? (punto de partida de cualquier persona o DLC)
python scripts/censo.py vigencia --markdown "$S/Nombre BI - censo.md" --versiones "$V"

# A. Censo inicial
python scripts/censo.py borrador --pbip "$V/00_original/Nombre BI" --salida "$S" --version 00_original --tipo Inicial \
  --correo-ejecutor ejecutor@empresa.com --correo-dueno-tablero dueno@empresa.com

# B. Versión nueva (después de guardar el PBIP en 01_versiones/<versión>/<BI> y confirmarlo, R54)
python scripts/censo.py borrador --pbip "$V/01_depuracion/Nombre BI" --salida "$S" --version 01_depuracion --tipo Actualización \
  --pbip-guardado-confirmado --correo-ejecutor ... --correo-dueno-tablero ...
python scripts/censo.py comparar --borrador "$S/Nombre BI - censo.borrador.md" --origen "DLC de depuración DEP-001"

# C. Registrar respuestas del dueño sobre el mismo PBIP
python scripts/censo.py iniciar-validacion --markdown "$S/Nombre BI - censo.md" --pbip "$V/<versión>/Nombre BI"
python scripts/censo.py comparar --borrador "$S/Nombre BI - censo.borrador.md" --origen "Validación con el dueño"

# En los tres casos: marcadores de la IA, validación y registro
python scripts/censo.py pendientes --markdown "<censo o borrador>"
python scripts/censo.py validar   --pbip "<PBIP>" --markdown "<censo o borrador>"
python scripts/censo.py registrar --pbip "<PBIP>" --markdown "<censo o borrador>" --alcance "Censo completo del PBIP"
```

`registrar` archiva el censo anterior en `versiones/`, deja el borrador como censo vigente y agrega el bloque de cambios y la fila del historial.

## Qué valida `censo.py validar`

**Errores** (impiden registrar la ejecución):

- Secciones 0–18 en orden, correos, census_id, fecha y hora, tipo y estado de catálogo.
- Marcadores `[IA: …]` o `[Completar]` pendientes, conteos aproximados e IDs truncados.
- Estados de uso y valores por clase según catálogo; regla R22 para «Sin uso interno identificado».
- Tipo, prioridad, certeza y estado de la sección 16, y ausencia de verbos de cambio (R47).
- Filas de la IA en la sección 16 que citan filas H-A/V-A (R50).
- Limitaciones agregadas por la IA en 17.1 que citan hallazgos o vacíos (R49).
- Con `--pbip`: conciliación por ID de visuales, páginas, tablas, columnas, medidas, relaciones, bookmarks y recursos, conteo de filtros e interacciones, y huella del PBIP igual a la del encabezado (R53).
- Validación con el dueño: «Validación del dueño» coherente con la certeza en la sección 14; respuesta obligatoria en puntos confirmados o descartados; si el ejecutor es el dueño, cada pendiente con respuesta o constancia (R55).
- «Completado y validado» sin puntos pendientes de validación en 14 y 16 (R56).
- `registrar` exige el bloque de `comparar` cuando cierra un borrador (R52).

**Advertencias** (no impiden registrar, pero deben revisarse):

- Limitación agregada en 17.1 que se parece a una de las 5 estándar (R49).
- Regla de la sección 14 sobre una columna «Sin uso interno identificado» que no lo dice, o con certeza «Encontrado» para el significado de negocio (R51).
- Censo sin huella del PBIP (anterior a v2.3) (R53).
- Validación sin `--pbip`: no se concilia contra la fuente y no se puede usar «Completado y validado».

## Relación con el DLC de modificación, creación y depuración

1. **Puerta de entrada (R56):** el DLC solo empieza si `censo.py vigencia` responde **APTO**: censo de la última versión guardada, huella coincidente, estado `Completado y validado` y ninguna regla (14) ni punto (16) pendiente de validación con el dueño. Si responde NO APTO, lista lo que falta cerrar.
2. Cita el `census_id` del censo con el que parte y usa de él: IDs completos, referencias de cada objeto (secciones 5, 7, 9, 11 y 12), candidatas (17.2), hallazgos y vacíos (16) y recursos y estética (13).
3. Arma su propio plan de cambio y su matriz de regresión.
4. Guarda el resultado como una **versión nueva** en `01_versiones/<versión>/<BI>` y no se cierra hasta ejecutar el censo de tipo `Actualización` con `--origen` igual a su identificador (R52, R54). Así `[BI] - cambios.md` muestra qué cambió y por qué proceso, y el censo vigente muestra el tablero final.
