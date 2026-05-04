# Claude Code: Agentes y Skills

Material del curso **Claude Code: Agentes y Skills** de LinkedIn Learning.

---

## Agentes y Skills

### ¿Qué es un Agente?

Un **agente** es una instancia de Claude que puede ejecutar tareas de forma autónoma o semi-autónoma. A diferencia de una conversación simple, un agente puede:

- Usar herramientas (leer archivos, ejecutar comandos, buscar en la web)
- Tomar decisiones en múltiples pasos para completar una tarea
- Delegar subtareas a otros agentes especializados
- Mantener contexto a lo largo de una sesión de trabajo

Claude Code permite lanzar agentes mediante el `Agent` tool, pudiendo correrlos en paralelo o de forma secuencial según las dependencias entre tareas.

### ¿Qué es un Skill?

Un **skill** es un conjunto de instrucciones predefinidas que extienden el comportamiento de Claude Code para un dominio específico. Se invocan con `/nombre-skill` y permiten estandarizar flujos de trabajo repetitivos, como revisar un PR, inicializar un proyecto, o configurar el entorno.

Los skills están definidos como archivos de instrucciones y son ejecutados por el propio harness de Claude Code, no por el modelo directamente.

---

## Proyecto de ejemplo: Grades API

El proyecto incluido en este repositorio es una API REST construida con **FastAPI** y **SQLite** para gestionar calificaciones de estudiantes. Se usa como ejemplo práctico a lo largo del curso para demostrar el uso de agentes y skills en un flujo de desarrollo real.

### ¿Qué hace?

Permite crear estudiantes, asignarles calificaciones por materia (matemáticas o español) y consultar un resumen de su desempeño.

### Stack

- **FastAPI** — framework de API
- **SQLModel** — ORM y validación de esquemas
- **SQLite** — base de datos local
- **uv** — gestión de entorno y dependencias

### Estructura

```
grades-api/
├── main.py
├── database.py
├── models/        # Modelos de base de datos (Student, Grade)
├── schemas/       # Schemas de entrada/salida (Subject, GradeCreate…)
└── routes/        # Endpoints organizados por recurso
```

### Ejecutar el proyecto

```bash
cd grades-api
uv sync
uv run uvicorn main:app --reload
```

Documentación interactiva en `http://localhost:8000/docs`.
