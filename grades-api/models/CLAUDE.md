# models/

SQLModel table classes with `table=True`. These are the actual database tables; they are kept separate from the request/response schemas in `schemas/`.

## Conventions

- Import shared field definitions from `schemas/` rather than duplicating them (e.g., `Grade` imports `Subject` from `schemas.grade`).
- Both models **must be imported in `main.py`** before `SQLModel.metadata.create_all` is called, otherwise their tables are never registered and won't be created on startup.
- Do not add business logic here. Models are pure table definitions.

## Files

- `student.py` — `Student` table: `id` (PK, auto), `name` (indexed string).
- `grade.py` — `Grade` table: `id` (PK, auto), `student_id` (FK → `student.id`), `subject` (`Subject` enum), `grade` (float, `0 ≤ grade ≤ 10`).

## Adding a new model

1. Create `models/<name>.py` with a class inheriting `SQLModel` with `table=True`.
2. Import it in `main.py` so `SQLModel.metadata.create_all` picks it up.
3. Drop and recreate `grades.db` if the schema changed — no migrations tooling is configured.
