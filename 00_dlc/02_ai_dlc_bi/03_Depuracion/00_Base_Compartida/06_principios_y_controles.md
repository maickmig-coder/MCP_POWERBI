# 1. AI-DLC PRINCIPAL

## 1.1 Principios generales

1. No asumir información que pueda cambiar el resultado.
2. Preguntar cuando falte información relevante.
3. Diferenciar requisitos del usuario, necesidades técnicas y propuestas de IA.
4. La decisión final sobre propuestas funcionales pertenece al usuario/analista.
5. En BI existentes, conservar la estética actual salvo solicitud, regla
   corporativa o necesidad técnica justificada.
6. No modificar elementos fuera del alcance solicitado.
7. No ubicar visuales arbitrariamente.
8. Validar el BI completo después de crear, modificar o depurar.
9. Convertir errores y lecciones aprendidas en reglas preventivas.
10. Mantener trazabilidad del original, cambios y validaciones.
11. Antes de crear lógica nueva, revisar si existe lógica reutilizable.
12. No eliminar elementos automáticamente por considerarlos no utilizados.
13. Toda recomendación de depuración debe explicar impacto, beneficio y riesgo.
14. La optimización debe analizar la cadena completa:
    Fuente → SQL/consulta → Power Query → Modelo → DAX → Visual.

## 1.2 Clasificación

### A. Creación
BI que no existía previamente.

### B. Modificación
Cambio funcional o técnico sobre un BI existente.

### C. Depuración y Mejora
Revisión orientada a integridad, datos, modelo, fuentes, consultas, DAX,
procesos, rendimiento y elementos innecesarios.

La depuración/mejora no debe convertirse en una "mejora estética". El diseño
se rige por creación/modificación y por el estándar corporativo.

## 1.3 Control de versiones y reversibilidad

Flujo mínimo:

Original → Versión de trabajo → Cambio → Validación → Versión final

El original no debe ser destino de modificación.

Cada cambio relevante debe registrar:
- qué cambió;
- por qué;
- quién/qué lo aprobó;
- elementos afectados;
- riesgo;
- validación realizada;
- resultado.

## 1.4 Nivel de riesgo

Clasificar cambios:

- Bajo: títulos, textos, ajustes visuales menores sin impacto funcional.
- Medio: filtros, visuales, navegación, medidas no centrales, transformaciones.
- Alto: relaciones centrales, granularidad, fuentes, consultas estructurales,
  medidas críticas, seguridad/RLS o cambios que puedan alterar resultados.

El riesgo alto exige validación de impacto y pruebas antes/después.

## 1.5 Matriz de dependencias

Antes de cambiar un elemento relevante, identificar:

Elemento cambiado → dependencias → visuales afectados → medidas afectadas →
filtros/relaciones/páginas → validaciones requeridas.

La matriz debe utilizarse para evitar cambios aislados que rompan otras partes
del BI.

## 1.6 Pruebas antes/después

Cuando un cambio pueda alterar resultados:
- capturar resultado/estado previo;
- ejecutar cambio;
- comparar resultado posterior;
- explicar diferencias esperadas;
- investigar diferencias no esperadas.

## 1.7 Registro de decisiones

Toda propuesta importante debe poder quedar registrada como:

- propuesta de IA;
- impacto/beneficio;
- decisión del analista: aprobado / rechazado / pendiente;
- fecha o versión cuando sea necesario.

## 1.8 Cierre "Listo para entrega"

No declarar terminado solo porque el cambio solicitado funciona.

Debe comprobarse:
- requerimiento;
- modelo;
- fuentes/consultas;
- DAX;
- visuales;
- marcadores/botones/estados;
- integridad;
- rendimiento cuando aplique;
- archivos/codificación;
- alertas;
- pendientes;
- trazabilidad.


## Control transversal de responsables y trazabilidad

Todo tablero debe tener trazabilidad desde el inicio, independientemente de si
el trabajo corresponde a creación, modificación o depuración.

La carpeta del tablero debe contener un `README.md` que funcione como historia
acumulativa del tablero. El responsable actual debe estar siempre identificado,
pero los responsables anteriores nunca se eliminan del histórico.

El registro central de tableros permite conocer rápidamente quién trabaja cada
BI y su estado actual.
