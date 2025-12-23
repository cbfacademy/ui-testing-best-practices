# Test API Overview

**File:** `tests/test_api.py`

## Purpose
This module demonstrates Playwright's ability to perform API-level testing. It validates the health and status of application endpoints and assets without requiring a full UI interaction.

## Key Features
- **APIRequestContext:** Uses Playwright's built-in API context for fast, HEAD/GET/POST requests.
- **Direct Asset Validation:** Verifies that critical assets like the favicon are reachable.
- **Integration Testing:** Can be used to verify backend state before or after UI tests.

## Scenarios Covered
1. **Endpoint Health:** Checks if the base URL or specific endpoints return a 200 OK status.
2. **Asset Availability:** Verifies that logos and other static assets are correctly served by the web application.
