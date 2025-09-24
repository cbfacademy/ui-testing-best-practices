# test_client/pages/inventory_page.py
from typing import List
from test_client.pages.base_page import BasePage
from test_client.util.util import get_locator


class InventoryPage(BasePage):
    # keys
    INVENTORY_CONTAINER = 'inventory_container'
    ITEM = 'item'
    ITEM_NAME = 'item_name'
    ADD_TO_CART_BTN = 'add_to_cart_btn'
    REMOVE_BTN = 'remove_btn'
    CART_LINK = 'cart_link'
    CART_BADGE = 'cart_badge'

    def _loc(self, key: str) -> str:
        return get_locator('inventory_page', key)

    def navigate(self, path: str = ''):
        super().navigate(path)

    def add_item_by_name(self, name: str):
        btn = self._loc(self.ADD_TO_CART_BTN)
        selector = f'.inventory_item:has-text("{name}") {btn}'
        self.click_element(selector)

    def remove_item_by_name(self, name: str):
        btn = self._loc(self.REMOVE_BTN)
        selector = f'.inventory_item:has-text("{name}") {btn}'
        self.click_element(selector)

    def add_all_items(self):
        buttons = self.page.locator(self._loc(self.ADD_TO_CART_BTN))
        for i in range(buttons.count()):
            buttons.nth(i).click()

    def open_cart(self):
        self.click_element(self._loc(self.CART_LINK))

    def get_cart_count(self) -> int:
        badge = self._loc(self.CART_BADGE)
        if self.page.locator(badge).count() == 0:
            return 0
        text = self.get_element(badge).inner_text()
        return int(text)

    def get_item_names(self) -> List[str]:
        return self.page.locator(self._loc(self.ITEM_NAME)).all_text_contents()
