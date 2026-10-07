# 14. CHECKLIST GENERAL

## Antes
- [ ] Tipo de solicitud identificado.
- [ ] Correo de quien trabaja/modifica identificado.
- [ ] Correo de quien solicita/es dueño identificado.
- [ ] Carpeta del tablero creada/localizada.
- [ ] README.md del tablero creado/localizado.
- [ ] Trabajo registrado en el registro central.
- [ ] Fecha de inicio registrada.
- [ ] Contexto suficiente.
- [ ] Alcance definido.
- [ ] Requisitos obligatorios definidos.
- [ ] Propuestas separadas de requisitos.
- [ ] Decisiones registradas.
- [ ] CENSO disponible cuando corresponde.
- [ ] Original preservado.
- [ ] Nivel de riesgo definido.

## Fuentes
- [ ] Servidores/fuentes identificados.
- [ ] SQL revisado cuando aplique.
- [ ] Power Query revisado cuando aplique.
- [ ] Flows/Dataflows revisados cuando aplique.
- [ ] Excel/archivos revisados cuando aplique.
- [ ] Columnas innecesarias identificadas.
- [ ] Filtros de origen evaluados.

## Modelo
- [ ] Granularidad.
- [ ] Tablas.
- [ ] Relaciones.
- [ ] Claves.
- [ ] Calendario.
- [ ] Medidas.
- [ ] DAX.
- [ ] Dependencias.
- [ ] Redundancias.

## Visuales
- [ ] Visuales definidos.
- [ ] Propósito definido.
- [ ] Ubicación definida.
- [ ] Mesa de trabajo respetada.
- [ ] Filtros ordenados.
- [ ] Estándar corporativo aplicado.
- [ ] Marcadores revisados.
- [ ] Botones revisados.
- [ ] Visuales ocultos revisados.

## Diseño
- [ ] Header.
- [ ] Logo oficial y ruta.
- [ ] Título.
- [ ] Última actualización.
- [ ] Separador.
- [ ] Segmentaciones.
- [ ] Botones.
- [ ] KPIs.
- [ ] Gráficos.
- [ ] Tablas.
- [ ] Leyendas.
- [ ] Navegación.
- [ ] Consistencia entre páginas.

## Integridad
- [ ] Campos inexistentes detectados.
- [ ] Medidas inexistentes detectadas.
- [ ] Entidades inexistentes detectadas.
- [ ] Dependencias revisadas.
- [ ] Estados alternativos revisados.
- [ ] Objetos heredados revisados.
- [ ] Layout validado.
- [ ] Codificación validada.
- [ ] BOM validado.

## Rendimiento
- [ ] Volumen evaluado.
- [ ] Columnas evaluadas.
- [ ] Consultas costosas revisadas.
- [ ] DAX revisado cuando corresponda.
- [ ] Tamaño/cardinalidad evaluados.

## Antes/después
- [ ] Resultado previo capturado.
- [ ] Resultado posterior capturado.
- [ ] Diferencias explicadas.
- [ ] Diferencias no esperadas investigadas.

## Entrega
- [ ] Cambio solicitado validado.
- [ ] README.md actualizado con cambios y decisiones.
- [ ] Histórico del tablero actualizado.
- [ ] Correo de quien trabaja/modifica y fecha de cierre registrados.
- [ ] Registro central actualizado.
- [ ] No hubo cambios fuera de alcance sin autorización.
- [ ] Alertas comunicadas.
- [ ] Pendientes documentados.
- [ ] Decisiones registradas.
- [ ] Estado "Listo para entrega" confirmado.


## Registro específico de cambio

- [ ] Registro de Cambio creado cuando corresponde.
- [ ] Estado anterior documentado.
- [ ] Propuesta documentada.
- [ ] Dependencias identificadas.
- [ ] Decisión del analista registrada.
- [ ] Cambio realizado documentado.
- [ ] Estado posterior documentado.
- [ ] Validación antes/después documentada.
- [ ] Beneficio/impacto documentado.
- [ ] Alertas y pendientes documentados.


## Control bloqueante de CENSO para modificación

- [ ] Nombre exacto del BI confirmado.
- [ ] CENSO buscado en `NIGGA\02_censo`.
- [ ] Si no existe, modificación bloqueada.
- [ ] PBIP original conservado en `NIGGA\01_bi\01_versiones\00_original\[Nombre exacto BI]\`.
- [ ] Ritual de CENSO ejecutado desde `NIGGA\00_dlc\01_ai-dlc-censo`.
- [ ] Resultado del CENSO guardado en `NIGGA\02_censo`.
- [ ] CENSO verificado antes de habilitar la modificación.


## Control bloqueante de CENSO para depuración/mejora

- [ ] BI existente identificado por nombre exacto.
- [ ] CENSO buscado en `NIGGA\02_censo`.
- [ ] Si no existe, depuración/mejora bloqueada.
- [ ] PBIP original conservado en `NIGGA\01_bi\01_versiones\00_original\[Nombre exacto BI]\`.
- [ ] Ritual de CENSO ejecutado desde `NIGGA\00_dlc\01_ai-dlc-censo`.
- [ ] Resultado guardado en `NIGGA\02_censo`.
- [ ] CENSO verificado antes de iniciar la depuración/mejora.


## Control de copia de trabajo Kiro

- [ ] Copia de trabajo del BI generada/preparada.
- [ ] Copia guardada en `NIGGA\01_bi\01_versiones\01_kiro\[Nombre exacto BI]`.
- [ ] Original protegido en `NIGGA\01_bi\01_versiones\00_original\[Nombre exacto BI]`.
- [ ] El trabajo del agente se ejecuta sobre la copia de `01_kiro`.
- [ ] Ruta de la copia registrada en README/Registro de Cambio cuando corresponda.
