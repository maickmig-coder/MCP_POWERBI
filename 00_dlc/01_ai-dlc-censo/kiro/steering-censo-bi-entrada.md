---
inclusion: always
---

# Entrada al CENSO BI (ritual AI-DLC v2.3.4)

Aplica cuando el pedido menciona un censo o un tablero censado (crear, actualizar, revisar, validar, vigencia, pendientes, respuestas del dueño).

1. **Lee primero la guía completa:** `.kiro/steering/censo-bi.md`. No leas `scripts/*.py`, `examples/` ni el censo completo.
2. **Pide el correo** de quien lo solicita y no ejecutes nada hasta tenerlo escrito (R57). Si responde «es mi correo» sin escribirlo, pídele que lo escriba.
3. **Interpreta el pedido así:**

| El usuario dice | Qué significa | Qué haces |
|---|---|---|
| «validar el censo», «validación», «revisar los pendientes», «confirmar los puntos», «responder lo del dueño» | **Validación con el dueño** de los puntos «Pendiente de validación» | `iniciar-validacion` y luego `guia-validacion`, un punto a la vez (R58, R59) |
| «revisar el censo», «¿está vigente?», «¿se puede modificar el tablero?» | Consulta | `vigencia` y resumen en 3–5 líneas |
| «hacer el censo», «censar», «actualizar el censo», «nueva versión» | Censo nuevo o actualización | Flujo de la guía desde el paso 1 |

El comando `censo.py validar` es un control interno del documento; **nunca** es la respuesta a «validar el censo».

4. **Si el correo es el del dueño** (sección 0 del censo): dile «Eres el dueño del tablero: empezamos la validación» y arranca sin más preguntas. **Si no lo es:** pregunta si conoce las respuestas y acepta validar sin ser el dueño (R58).
5. Ejecuta los comandos desde `00_dlc/01_ai-dlc-censo` con rutas `..\..\02_censo\…` y `..\..\01_bi\01_versiones\…`.
