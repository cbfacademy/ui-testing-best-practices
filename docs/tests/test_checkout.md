# Test Checkout Overview

**File:** `tests/test_checkout.py`

## Purpose
This module validates the end-to-end shopping cart and checkout process. It ensures that items can be added, reviewed, and purchased correctly, and that the application handles mandatory data entry during the checkout steps.

## Key Features
- **Multi-Page Flows:** Interacts with `InventoryPage`, `CartPage`, `CheckoutStepOnePage`, `CheckoutStepTwoPage`, and `CheckoutCompletePage`.
- **Item Parameterization:** Tests checkout with varying numbers and types of products.
- **Error Validation:** Ensures the checkout cannot proceed without first name, last name, or postal code.

## Scenarios Covered
1. **Successful Single/Multi Item Checkout:** Verifies the complete flow from cart to "Thank You" screen.
2. **Mandatory Field checks:** Validates that user info is required to proceed.
3. **Checkout Cancellation:** Ensures users can back out of the checkout at various stages without state corruption.
