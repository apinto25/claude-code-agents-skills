# tests/

Unit and integration tests for the grades-api. Run from the `grades-api/` directory:

```bash
uv run pytest tests/
uv run pytest tests/ -v       # verbose output
uv run pytest tests/routes/   # single subfolder
```

## Structure

Tests are separated by layer to match the source layout:

- `routes/` — HTTP handler tests using `TestClient`. These are the integration tests: they exercise the full request/response cycle including validation, 404 handling, and DB side effects.
- `models/` — SQLModel table tests. Exercise persistence, retrieval, update, and delete directly against the session without going through HTTP.
- `schemas/` — Pydantic validation tests. No DB or HTTP involved; instantiate schema classes directly and assert on `ValidationError`.

## Fixtures (`conftest.py`)

Two fixtures are defined at the top level and available to all subfolders:

- **`session`** — creates a fresh in-memory SQLite database (`sqlite://` + `StaticPool`) per test, runs `create_all`, yields the session, then runs `drop_all`. Each test gets an isolated, empty database.
- **`client`** — depends on `session`. Overrides the `get_session` FastAPI dependency so all route handlers use the same in-memory session, then yields a `TestClient`. Clears `dependency_overrides` after each test.

Route tests that need to pre-seed the DB should accept both `client` and `session` as parameters. Tests that only make HTTP calls need only `client`.

## Conventions

- Group tests for a single endpoint or class inside a `class Test<Name>:` block.
- Use a module-level `make_<model>` helper to insert fixtures into the DB rather than repeating setup inline.
- Schema tests never import `Session`, `TestClient`, or anything from `database`/`main`.
- Model tests never import `TestClient` or anything from `routes`.
