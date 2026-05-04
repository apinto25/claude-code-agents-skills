# Grades API

API REST para gestionar calificaciones de estudiantes por materia, construida con FastAPI y SQLite.

## Stack

- **FastAPI** — framework de API
- **SQLModel** — ORM y validación de esquemas
- **SQLite** — base de datos (`grades.db`)
- **uv** — gestión de entorno y dependencias

## Estructura del proyecto

```
grades-api/
├── main.py           # Punto de entrada, lifespan, registro de routers
├── database.py       # Engine y dependencia de sesión
├── models/
│   ├── student.py    # Modelo de tabla Student
│   └── grade.py      # Modelo de tabla Grade (FK → student)
├── schemas/
│   ├── student.py    # StudentCreate, StudentUpdate
│   └── grade.py      # Enum Subject, GradeCreate, GradeUpdate
└── routes/
    ├── students.py   # CRUD + endpoint de resumen
    └── grades.py     # CRUD con filtros
```

## Instalación

```bash
uv sync
```

## Ejecutar

```bash
uv run uvicorn main:app --reload
```

Documentación interactiva disponible en `http://localhost:8000/docs`.

## Endpoints

### Estudiantes

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/students` | Crear un estudiante |
| `GET` | `/students` | Listar todos los estudiantes |
| `GET` | `/students/{id}` | Obtener un estudiante |
| `PATCH` | `/students/{id}` | Actualizar un estudiante |
| `DELETE` | `/students/{id}` | Eliminar un estudiante |
| `GET` | `/students/{id}/summary` | Calificaciones por materia y promedio |

### Calificaciones

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/grades` | Agregar una calificación |
| `GET` | `/grades` | Listar calificaciones (filtrar por `student_id`, `subject`) |
| `GET` | `/grades/{id}` | Obtener una calificación |
| `PATCH` | `/grades/{id}` | Actualizar una calificación |
| `DELETE` | `/grades/{id}` | Eliminar una calificación |

## Modelo de datos

- **Student** — `id`, `name`
- **Grade** — `id`, `student_id`, `subject` (`math` | `spanish`), `grade` (0–10)

## Ejemplo de uso

```bash
# Crear un estudiante
curl -X POST http://localhost:8000/students \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'

# Agregar una calificación
curl -X POST http://localhost:8000/grades \
  -H "Content-Type: application/json" \
  -d '{"student_id": 1, "subject": "math", "grade": 9.5}'

# Ver resumen del estudiante
curl http://localhost:8000/students/1/summary
```
