from test_client.pages.base_page import BasePage
from test_client.util.util import get_locator


class CheckoutCompletePage(BasePage):
    COMPLETE_HEADER = 'complete_header'
    COMPLETE_TEXT = 'complete_text'
    BACK_HOME = 'back_home'

    def _loc(self, key: str) -> str:
        return get_locator('checkout_complete_page', key)

    def navigate(self, path: str = 'checkout-complete.html'):
        super().navigate(path)

    def is_complete(self) -> bool:
        try:
            return self.get_element(self._loc(self.COMPLETE_HEADER)).is_visible()
        except Exception:
            return False

    def get_complete_text(self) -> str:
        return self.get_element(self._loc(self.COMPLETE_TEXT)).inner_text()

    def back_to_products(self):
        self.click_element(self._loc(self.BACK_HOME))
