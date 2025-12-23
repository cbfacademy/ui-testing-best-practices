# Test Login Overview

**File:** `tests/test_login.py`

## Purpose
This module handles all authentication-related test scenarios for the SauceDemo application. It ensures that users can log in with valid credentials and receive appropriate error feedback for invalid or restricted accounts.

## Key Features
- **Data-Driven Testing:** Uses `@pytest.mark.parametrize` to test multiple credential sets (valid, locked out, invalid, empty).
- **Page Object Model:** Utilizes the `LoginPage` class for all interactions.
- **Fixture Support:** Leverages the `login_page` fixture for clean setup and teardown.

## Scenarios Covered
1. **Valid Login:** Verifies successful redirection to the inventory page.
2. **Locked Out User:** Ensures a specific error message is displayed for locked accounts.
3. **Invalid Password:** Validates that incorrect credentials prevent access and show a generic error.
4. **Empty Credentials:** Checks for mandatory field validation messages.
