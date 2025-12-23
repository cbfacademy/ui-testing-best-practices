# Test Visual Overview

**File:** `tests/test_visual.py`

## Purpose
This module demonstrates visual regression testing. It captures screenshots of the application and compares them against "baseline" images to detect unexpected UI changes.

## Key Features
- **to_be_visible Baseline:** Uses functional visibility checks as a reliable starting point.
- **Screenshot Capture:** Demonstrates how to take debug screenshots of specific page states.
- **UI Consistency:** Designed to serve as a template for `expect(page).to_have_screenshot()` once baselines are established.

## Scenarios Covered
1. **Login Page Visuals:** Ensures the login form and landing elements are visible and correctly placed.
2. **Inventory Page Visuals:** Verifies the visual layout of the product list after login.
