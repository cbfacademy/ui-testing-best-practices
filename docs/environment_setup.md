# Environment Setup

## 1. Environment Variables
Required (used by pytest.ini mappings):
- APP_USER: Standard application username (mapped via standard_app_user_env = ${APP_USER})
- APP_PASSWORD: Password for APP_USER (app_password_env = ${APP_PASSWORD})

Optional runtime overrides (pass as pytest args when needed):
- --base-url (defaults to https://www.saucedemo.com)
- --browser (chromium | firefox | webkit | msedge)
- --headed / --headless
- --video on / off (record_video in pytest.ini)
- --env selection pattern if you implement custom switching logic (current profiles: env.local, env.local-edge, env.dev, env.qa, env.prod in pytest.ini)

Set required variables before running tests:

Bash / Zsh:
```bash
export APP_USER="standard_user"
export APP_PASSWORD="secret_sauce"
```

PowerShell:
```powershell
$Env:APP_USER="standard_user"
$Env:APP_PASSWORD="secret_sauce"
```

CMD:
```cmd
set APP_USER=standard_user
set APP_PASSWORD=secret_sauce
```

(Optionally add them to a local .env and load with your shell profile.)

Verify:
```bash
python -c "import os; print(os.getenv('APP_USER'), bool(os.getenv('APP_PASSWORD')))"
```

## 2. Setup uv
uv is the Python package manager used (see pyproject.toml tool.uv.index for internal index config).

Install (choose one):

macOS / Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

Ensure it’s on PATH:
```bash
uv --version
```

Create and activate virtual environment (Python 3.12+):
```bash
uv venv --python 3.12 .venv
# Activate:
# Linux/macOS:
source .venv/bin/activate
# PowerShell:
.\.venv\Scripts\Activate.ps1
# CMD:
.\.venv\Scripts\activate.bat
```

Sync dependencies (main + dev group):
```bash
uv sync --group dev
```

(If you only need runtime deps: uv sync)

To refresh after pyproject changes:
```bash
uv sync --frozen  # CI style
# or
uv sync --upgrade
```

Clean reinstall (optional troubleshooting):
```bash
rm -rf .venv
uv venv --python 3.12 .venv
uv sync --group dev
```

## 3. Run Tests & Generate Report
Run full test suite:
```bash
uv run pytest
# or with task:
uv run task tests
```

Select markers:
```bash
uv run pytest -m LOGIN
```

Parallel execution (xdist present in dev group):
```bash
uv run pytest -n auto
```

Reduce Playwright slow motion for speed:
```bash
uv run pytest --slowmo 0
```

Switch logical environment (leverage config sections via custom CLI/options if implemented) e.g.:
```bash
# Example: run in a headless style (like env.dev settings) plus marker
uv run pytest -m CHECKOUT --headless
```

Generate Allure results (already configured via addopts -> reports/json):
Each test run populates reports/json (cleaned automatically via --clean-alluredir).

Generate static HTML:
```bash
uv run task generate-report
# Output: test-results/html/index.html
```

Serve interactive report:
```bash
uv run task view-report
```

Direct allure commands (alternative):
```bash
uv run allure generate reports/json -o test-results/html --clean
uv run allure serve reports/json
```

Open report manually (without serve):
```bash
# macOS
open test-results/html/index.html
# Linux
xdg-open test-results/html/index.html
# Windows
start test-results/html/index.html
```

Typical workflow quick reference:
1. Set APP_USER / APP_PASSWORD
2. uv venv && source activate (first time only)
3. uv sync --group dev
4. uv run task tests
5. uv run task generate-report (or uv run task view-report)

Troubleshooting:
- Missing videos/screenshots: ensure record_video and screenshot_on in the active env section.
- Credentials failing: echo $APP_USER to confirm export.
- Stale dependencies: uv sync --upgrade
- Playwright browsers not installed (if prompted):
  uv run playwright install

CI hint: Use uv sync --frozen then uv run pytest
