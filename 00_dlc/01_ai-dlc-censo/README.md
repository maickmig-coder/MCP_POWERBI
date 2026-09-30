# AI-DLC-CENSO

Repositorio estándar para el **censo técnico y funcional de soluciones de Business Intelligence (BI)** mediante un enfoque AI-DLC.

## Objetivo

Este repositorio define un ritual repetible para que una IA analice cualquier BI sin modificarlo y produzca un censo estructurado.

El proceso busca:

- Identificar la estructura técnica.
- Comprender la finalidad funcional.
- Identificar elementos utilizados.
- Identificar elementos no utilizados.
- Reconstruir reglas de negocio.
- Mapear dependencias.
- Detectar vacíos de información.
- Generar propuestas de revisión basadas en evidencia.
- Consolidar y validar el censo.

> **Alcance:** este repositorio está orientado exclusivamente al censo y descubrimiento. No define procesos de modificación, desarrollo, despliegue ni optimización del BI.

## Estructura

```text
AI-DLC-CENSO/
│
├── README.md
│
├── ai-dlc/
│   ├── ritual-censo-bi.md
│   ├── reglas-censo.md
│   ├── checklist-censo.md
│   └── criterios-propuestas.md
│
├── templates/
│   ├── censo-bi.md
│   ├── matriz-elementos-no-utilizados.csv
│   ├── matriz-vacios-censo.csv
│   └── matriz-propuestas.csv
│
└── examples/
    └── gc-leads-mg/
        └── censo.md
```

## Flujo

```text
Ingreso del BI
      ↓
Censo técnico
      ↓
Censo funcional
      ↓
Elementos utilizados
      ↓
Elementos no utilizados
      ↓
Reglas de negocio
      ↓
Dependencias
      ↓
Vacíos del censo
      ↓
Propuestas de revisión IA
      ↓
Consolidación
      ↓
Validación
```

## Regla central

La IA no debe limitarse a completar un checklist. Debe analizar la evidencia disponible y detectar aspectos adicionales que deban revisarse.

Toda afirmación debe distinguir entre:

- **Encontrado:** existe evidencia directa.
- **Inferido:** existe una inferencia razonable, pero no evidencia directa.
- **Desconocido:** no existe información suficiente.

## Uso

1. Entregar al agente el proyecto BI que debe censar.
2. Cargar las instrucciones de `ai-dlc/`.
3. Ejecutar el ritual definido en `ritual-censo-bi.md`.
4. Utilizar `checklist-censo.md` para verificar cobertura.
5. Generar el resultado utilizando `templates/censo-bi.md`.
6. Registrar elementos no utilizados, vacíos y propuestas en sus respectivas matrices.
7. Validar el censo antes de considerarlo terminado.

## Ejemplo

`examples/gc-leads-mg/censo.md` contiene un ejemplo basado en el censo del BI **GC - Leads MG** utilizado como referencia para estructurar este estándar.
