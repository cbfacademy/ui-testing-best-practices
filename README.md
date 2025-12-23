# UI Testing Best Practices

Short overview: A Python-based Playwright + pytest example repository illustrating recommended patterns for reliable UI tests: page object; centralized locators, environment overlays, fixtures for per-test browser contexts, artifact collection, and CI-ready reporting.

## Quick links
- [`docs/environment_setup.md`](./docs/environment_setup.md) — environment, `uv` setup, creating virtualenv, running tests, and generating Allure reports.
- [`docs/ui-testing-best-practices.md`](./docs/ui-testing-best-practices.md) — design decisions, locator strategy, fixtures, artifacts.

## Repository layout
- `tests/` — test suites and parametrized cases.  
  - [Login Overview](docs/tests/test_login.md)
  - [Checkout Overview](docs/tests/test_checkout.md)
  - [Accessibility Overview](docs/tests/test_accessibility.md)
  - [API Overview](docs/tests/test_api.md)
  - [Visual Overview](docs/tests/test_visual.md)
  - **Parallel Execution**: Tests run with 5-way concurrency by default (configured in `pytest.ini`). Use `pytest -n <num>` to override.
  - **Data Driven**: Parameterized tests using CSV and external data.
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

1. **Sync dependencies**:
   ```bash
   uv sync
   ```

2. **Run all tests**:

   **Windows (PowerShell):**
   ```powershell
   $env:APP_USER="standard_user"; $env:APP_PASSWORD="secret_sauce"; uv run pytest
   ```

   **macOS / Linux:**
   ```bash
   APP_USER="standard_user" APP_PASSWORD="secret_sauce" uv run pytest
   ```

Generate Allure HTML:
```bash
uv run task generate-report
# or
uv run allure generate reports/json -o test-results/html --clean
```

## Notes
- Sensitive credentials are supplied via `APP_USER` and `APP_PASSWORD` and referenced in `pytest.ini` via placeholders.
- Use `pytest --env=qa` to pick environment overlays defined in `pytest.ini`.
- Artifacts (videos/screenshots) are written to predictable folders for CI collection: `test-results/videos`, `reports/json`.
