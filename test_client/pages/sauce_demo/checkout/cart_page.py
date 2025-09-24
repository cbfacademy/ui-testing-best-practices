from typing import List
from test_client.pages.base_page import BasePage
from test_client.util.util import get_locator


class CartPage(BasePage):
    CART_ITEM = 'cart_item'
    ITEM_NAME = 'item_name'
    REMOVE_BTN = 'remove_btn'
    CHECKOUT_BUTTON = 'checkout_button'
    CONTINUE_SHOPPING = 'continue_shopping'
    CART_EMPTY = 'cart_list_container'

    def _loc(self, key: str) -> str:
        return get_locator('cart_page', key)

    def navigate(self, path: str = 'cart.html'):
        super().navigate(path)

    def get_item_names(self) -> List[str]:
        return self.page.locator(self._loc(self.ITEM_NAME)).all_text_contents()

    def remove_item_by_name(self, name: str):
        remove_btn = self._loc(self.REMOVE_BTN)
        selector = f'.cart_item:has-text("{name}") {remove_btn}'
        self.click_element(selector)

    def proceed_to_checkout(self):
        self.click_element(self._loc(self.CHECKOUT_BUTTON))

    def continue_shopping(self):
        self.click_element(self._loc(self.CONTINUE_SHOPPING))

    def is_empty(self) -> bool:
        return self.page.locator(self._loc(self.CART_ITEM)).count() == 0
