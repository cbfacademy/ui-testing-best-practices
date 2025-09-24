from typing import List
from test_client.pages.base_page import BasePage
from test_client.util.util import get_locator


class CheckoutOverviewPage(BasePage):
    ITEM_NAME = 'item_name'
    SUMMARY_SUBTOTAL = 'summary_subtotal'
    SUMMARY_TAX = 'summary_tax'
    SUMMARY_TOTAL = 'summary_total'
    FINISH_BUTTON = 'finish_button'
    CANCEL_BUTTON = 'cancel_button'

    def _loc(self, key: str) -> str:
        return get_locator('checkout_overview_page', key)

    def navigate(self, path: str = 'checkout-step-two.html'):
        super().navigate(path)

    def get_item_names(self) -> List[str]:
        return self.page.locator(self._loc(self.ITEM_NAME)).all_text_contents()

    def get_subtotal(self) -> str:
        return self.get_element(self._loc(self.SUMMARY_SUBTOTAL)).inner_text()

    def get_tax(self) -> str:
        return self.get_element(self._loc(self.SUMMARY_TAX)).inner_text()

    def get_total(self) -> str:
        return self.get_element(self._loc(self.SUMMARY_TOTAL)).inner_text()

    def finish_checkout(self):
        self.click_element(self._loc(self.FINISH_BUTTON))

    def cancel(self):
        self.click_element(self._loc(self.CANCEL_BUTTON))
