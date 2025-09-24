from test_client.pages.base_page import BasePage
from test_client.util.util import get_locator


class CheckoutInfoPage(BasePage):
    FIRST_NAME = 'first_name'
    LAST_NAME = 'last_name'
    POSTAL_CODE = 'postal_code'
    CONTINUE_BUTTON = 'continue_button'
    CANCEL_BUTTON = 'cancel_button'

    def _loc(self, key: str) -> str:
        return get_locator('checkout_info_page', key)

    def navigate(self, path: str = 'checkout-step-one.html'):
        super().navigate(path)

    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str):
        self.fill_input(self._loc(self.FIRST_NAME), first_name)
        self.fill_input(self._loc(self.LAST_NAME), last_name)
        self.fill_input(self._loc(self.POSTAL_CODE), postal_code)

    def continue_to_overview(self, first_name: str = None, last_name: str = None, postal_code: str = None):
        if first_name is not None or last_name is not None or postal_code is not None:
            self.fill_checkout_info(first_name or '', last_name or '', postal_code or '')
        self.click_element(self._loc(self.CONTINUE_BUTTON))

    def cancel(self):
        self.click_element(self._loc(self.CANCEL_BUTTON))
