# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About this repository

Course material for **Claude Code: Agentes y Skills** (LinkedIn Learning). The repository contains example projects built during the course. Skills and agents created as part of the course live in `.claude/skills/` and `.claude/agents/`.

## Grades API

The main example project is a FastAPI REST API under `grades-api/`. All commands below must be run from that directory.

### Setup and run

```bash
cd grades-api
uv sync
uv run uvicorn main:app --reload
```

### Add a dependency

```bash
uv add <package>
```

## Architecture: grades-api

The app uses **SQLModel**, which unifies SQLAlchemy table models and Pydantic schemas. The layers are intentionally separated:

- `schemas/` — input/output shapes (`GradeCreate`, `GradeUpdate`, `Subject` enum). No DB knowledge.
- `models/` — SQLModel table classes with `table=True`. Import from `schemas/` for shared field definitions. Both models **must be imported in `main.py`** so `SQLModel.metadata.create_all` registers both tables at startup.
- `routes/` — APIRouter instances, one file per resource. Imported and registered in `main.py`.
- `database.py` — single engine instance and `get_session` FastAPI dependency.

The DB is created automatically on startup via the `lifespan` handler in `main.py`. No migrations tooling is set up; schema changes require dropping and recreating `grades.db`.
