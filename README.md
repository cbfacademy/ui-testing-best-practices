# UI Testing Best Practices

Short overview: A Python-based Playwright + pytest example repository illustrating recommended patterns for reliable UI tests: page object\; centralized locators, environment overlays, fixtures for per-test browser contexts, artifact collection, and CI-ready reporting.

## Quick links
- [`docs/environment_setup.md`](./docs/environment_setup.md) — environment, `uv` setup, creating virtualenv, running tests, and generating Allure reports.
- [`docs/ui-testing-best-practices.md`](./docs/ui-testing-best-practices.md) — design decisions, locator strategy, fixtures, artifacts.

## Repository layout
- `tests/` — test suites and parametrized cases.  
- `test_client/` — helpers, page objects, locator resolution (e.g. `test_client/util/util.py`).  
- `tests/fixtures/` — pytest fixtures (browser/page lifecycle).  
- `docs/` — Markdown guides (linked above).  
- `reports/` — Allure result json and generated HTML.  
- `pytest.ini`, `conftest.py`, `pyproject.toml` — config and dependency metadata.

## Requirements
- Python 3.12\+  
- `uv` (project package manager) on PATH  
- Playwright browsers installed when prompted (`uv run playwright install`)

## Quick start
Set required environment variables:
```bash
export APP_USER="standard_user"
export APP_PASSWORD="super_secret"
```

Create venv, sync deps and run tests:
```bash
uv venv --python 3.12 .venv
source .venv/bin/activate
uv sync --group dev
uv run pytest
```

Generate Allure HTML:
```bash
uv run task generate-report
# or
uv run allure generate reports/json -o test-results/html --clean
```

## Notes
- Sensitive credentials are supplied via `APP_USER` and `APP_PASSWORD` and referenced in `pytest.ini` via placeholders.
- Use `pytest --env qa` to pick environment overlays defined in `pytest.ini`.
- Artifacts (videos/screenshots) are written to predictable folders for CI collection: `test-results/videos`, `reports/json`.
