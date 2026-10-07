# 2. FLUJO OPERATIVO

## 2.1 Creación

Solicitud
↓
Identificar responsable y solicitante
↓
Crear carpeta del tablero en `NIGGA\01_bi\01_versiones\00_original\[Nombre exacto BI]`
↓
Crear/actualizar `README.md` del tablero
↓
Registrar trabajo en `REGISTRO_CONTROL_TABLEROS.md`
↓
Contexto y finalidad
↓
Qué se requiere medir
↓
Público
↓
Fuentes/servidores
↓
KPIs y medidas
↓
¿Usuario define o desea propuestas IA?
↓
Visuales
↓
¿Usuario define o desea propuestas IA?
↓
Modelo semántico
↓
Relaciones / granularidad / calendario / DAX / transformaciones
↓
Páginas / layout / filtros / navegación
↓
Seguridad / actualización / interacciones cuando apliquen
↓
Confirmación
↓
Implementación
↓
Validación técnica + visual + integridad
↓
Pruebas antes/después cuando aplique
↓
Documentación
↓
Listo para entrega

## 2.2 Modificación

Solicitud
↓
Nombre exacto
↓
Identificar responsable y solicitante
↓
Abrir `README.md` del tablero
↓
Registrar nueva intervención en el histórico
↓
Buscar CENSO en NIGGA\02_censo
↓
¿Existe?
├─ Sí → cargar CENSO
└─ No → bloquear modificación → realizar CENSO
↓
Preservar original como PBIP
↓
Analizar solicitud
↓
Matriz de dependencias
↓
Nivel de riesgo
↓
Plan de cambio
↓
Aprobación de propuestas
↓
Modificar
↓
Validar cambio
↓
Pruebas antes/después
↓
Revisión integral
↓
Alertas
↓
Documentar
↓
Listo para entrega

## 2.3 Depuración y Mejora

Solicitud/objetivo
↓
Identificar responsable y solicitante
↓
Abrir `README.md` del tablero
↓
Registrar nueva intervención en el histórico
↓
CENSO/estado actual
↓
Detectar oportunidades
↓
Fuente / SQL / Power Query / flujos / archivos
↓
Modelo / columnas / medidas / relaciones
↓
DAX / procesos
↓
Rendimiento
↓
Dependencias e impacto
↓
Proponer solución
↓
Analista aprueba/rechaza
↓
Ejecutar solo lo aprobado
↓
Comparar antes/después
↓
Validar integridad
↓
Documentar beneficio y pendientes
↓
Listo para entrega


## 2.4 Regla transversal de trazabilidad

En los tres procesos, la identificación y registro del responsable ocurre al
inicio.

El tablero debe tener:

1. registro central actualizado;
2. README individual;
3. responsable actual;
4. fecha de inicio;
5. tipo de trabajo;
6. estado;
7. histórico acumulativo.

Al finalizar, ambos registros deben actualizarse.


## Regla transversal de identificación

En Creación, Modificación y Depuración/Mejora, al inicio del trabajo se deben
registrar únicamente:

1. Correo de quien trabaja/modifica el tablero.
2. Correo de quien solicita/es dueño del requerimiento.

Estos correos deben quedar en el README del tablero. El histórico conserva las
intervenciones anteriores.


## Flujo obligatorio cuando una modificación no tiene CENSO

```text
Modificar BI existente
        ↓
Solicitar nombre exacto
        ↓
Buscar CENSO en NIGGA\02_censo
        ↓
¿Existe?
   ├── NO
   │    ↓
   │  BLOQUEAR MODIFICACIÓN
   │    ↓
   │  Conservar PBIP original
   │  NIGGA\01_bi\01_versiones\00_original\[Nombre exacto BI]\
   │    ↓
   │  Ejecutar ritual
   │  NIGGA\00_dlc\01_ai-dlc-censo
   │    ↓
   │  Guardar CENSO
   │  NIGGA\02_censo
   │    ↓
   │  Verificar CENSO
   │    ↓
   │  Continuar modificación
   │
   └── SÍ
        ↓
      Cargar CENSO
        ↓
      Continuar modificación
```


## Flujo obligatorio cuando una depuración/mejora no tiene CENSO

```text
Depuración / Mejora de BI existente
        ↓
Solicitar nombre exacto
        ↓
Registrar correo quien trabaja/modifica
        +
Registrar correo quien solicita/es dueño
        ↓
Buscar CENSO en NIGGA\02_censo
        ↓
¿Existe?
   ├── NO
   │    ↓
   │  BLOQUEAR DEPURACIÓN/MEJORA
   │    ↓
   │  Conservar PBIP original
   │  NIGGA\01_bi\01_versiones\00_original\[Nombre exacto BI]\
   │    ↓
   │  Ejecutar ritual
   │  NIGGA\00_dlc\01_ai-dlc-censo
   │    ↓
   │  Guardar CENSO
   │  NIGGA\02_censo
   │    ↓
   │  Verificar CENSO
   │    ↓
   │  Continuar depuración/mejora
   │
   └── SÍ
        ↓
      Cargar CENSO como contexto
        ↓
      Analizar oportunidades
        ↓
      Continuar depuración/mejora
```


## Regla transversal de copia de trabajo Kiro

En Creación, Modificación y Depuración/Mejora, antes de trabajar sobre el BI,
el agente debe disponer de una copia de trabajo en:

```text
NIGGA\01_bi\01_versiones\01_kiro\[Nombre exacto BI]\
```

El agente trabaja sobre esta copia y mantiene protegido el original ubicado
en `00_original`.
