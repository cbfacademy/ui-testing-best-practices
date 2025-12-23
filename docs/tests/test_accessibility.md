# Test Accessibility Overview

**File:** `tests/test_accessibility.py`

## Purpose
This module performs automated accessibility audits using `axe-core`. It ensures that the application meets WCAG standards and is usable by people with disabilities.

## Key Features
- **Axe-Core Integration:** Uses `axe-playwright-python` to run comprehensive scans.
- **Detailed Logging:** Reports specific violations, their impact level, and help descriptions directly to the test logs.
- **Fail/Warn Policy:** Can be configured to either fail the test on critical violations or simply log warnings for further review.

## Scenarios Covered
1. **Login Page Audit:** Scans the initial login screen for accessibility issues.
2. **Inventory Page Audit:** Scans the main product listing page after a successful login.
