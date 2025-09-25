# UI Testing Best Practices (Playwright + Pytest)

This condensed guide keeps the core operational practices for the project.

---

## 1. Project Structure \& Separation of Concerns
Layers:
- Tests: behavioral specs under [`tests/`](../tests/)
- Page objects: interaction logic under [`test_client/pages/sauce_demo/`](../test_client/pages/sauce_demo/)
- Utilities: shared helpers in [`test_client/util/`](../test_client/util/)
- Configuration: [`pytest.ini`](../pytest.ini), locator map [`config/locators.yml`](../config/locators.yml)
- Fixtures: reusable setup in [`tests/fixtures/`](../tests/fixtures/) (e.g. [`tests/fixtures/browser.py`](../tests/fixtures/browser.py))  
  Benefits: clarity, low coupling, easier refactors.

---

## 2. Page Object Model (POM)
Each page exposes intent methods (e.g. `login_and_verify`, `add_item_by_name`) without embedding test assertions.  
Example files:
- [`test_client/pages/sauce_demo/login_page.py`](../test_client/pages/sauce_demo/login_page.py)
- [`test_client/pages/sauce_demo/checkout/inventory_page.py`](../test_client/pages/sauce_demo/checkout/inventory_page.py)
- [`test_client/pages/sauce_demo/checkout/cart_page.py`](../test_client/pages/sauce_demo/checkout/cart_page.py)  
  Guidelines:
- Keep assertions in tests (allow lightweight visibility checks).
- Use semantic method names (domain verbs).

---

## 3. Centralized Locator Management (YAML)
All selectors defined in one map: [`config/locators.yml`](../config/locators.yml).  
Resolution helper (e.g. `get_locator`) lives in [`test_client/util/util.py`](../test_client/util/util.py).  
Advantages:
- Single edit propagates everywhere.
- Supports fallback strategies (id \> css \> xpath, etc.).
- Page objects reference symbolic keys only.

---

## 4. Environment \& Runtime Configuration
[`pytest.ini`](../pytest.ini) holds base defaults plus environment overlays (`[env.local]`, `[env.qa]`, etc.).  
Runtime selection: `pytest --env=qa`.  
Sensitive/runtime values injected via placeholder keys:
- `standard_app_user_env = ${APP_USER}`
- `app_password_env = ${APP_PASSWORD}`  
  Resolved in [`conftest.py`](../conftest.py) (environment parsing) and consumed by fixtures (e.g. [`tests/fixtures/browser.py`](../tests/fixtures/browser.py)).

---

## 5. Fixtures \& Test Isolation
Primary browser/page lifecycle in [`tests/fixtures/browser.py`](../tests/fixtures/browser.py) via the `page` fixture:
- Per-test fresh context
- Optional video + screenshots
  Environment-aware options pulled from [`pytest.ini`](../pytest.ini).  
  Keep fixtures function-scoped unless sharing is intentional.

---

## 6. Data-Driven \& Parameterized Tests
Use `@pytest.mark.parametrize` for credential scenarios and edge cases (e.g. in [`tests/test_login.py`](../tests/test_login.py)).  
Benefits:
- Broader coverage
- Minimal duplication
- Clear separation of data vs mechanics

---

## 7. Test Artifacts \& Reporting
Artifacts configured by [`pytest.ini`](../pytest.ini) flags:
- Video (`record_video`)
- Screenshots (`screenshot_on`)  
  Captured in [`tests/fixtures/browser.py`](../tests/fixtures/browser.py) and attached to Allure output directory defined by `allure_dir` (e.g. [`reports/json`](../reports/json)).  
  Environment metadata written for traceability.

---

## 8. Avoiding Hard-Coded Secrets
Secrets provided via environment variables referenced indirectly:
- Placeholders in [`pytest.ini`](../pytest.ini) (`${APP_USER}`, `${APP_PASSWORD}`)
- Resolved at startup; never committed in code  
  Accessed through session fixtures (e.g. `standard_app_user`, `valid_password`).

---

## 9. CI Readiness
Deterministic, environment-driven runs:
```
pytest --env=qa --alluredir reports/json
```
Then generate human-readable report:
```
allure generate reports/json -o reports/html --clean
```
Artifacts (videos/screenshots) land under predictable folders (`test-results/videos`, `reports/json`) for CI collection.

---