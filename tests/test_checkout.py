import pytest
from test_client.pages.sauce_demo.login_page import LoginPage
from test_client.pages.sauce_demo.checkout.inventory_page import InventoryPage
from test_client.pages.sauce_demo.checkout.cart_page import CartPage
from test_client.pages.sauce_demo.checkout.checkout_info_page import CheckoutInfoPage
from test_client.pages.sauce_demo.checkout.checkout_overview_page import CheckoutOverviewPage
from test_client.pages.sauce_demo.checkout.checkout_complete_page import CheckoutCompletePage
from test_client.util.logger import get_logger
from pathlib import Path
import csv

log = get_logger(__name__)

_DATA_DIR = Path(__file__).resolve().parent.parent / 'config' / 'data'


def _load_csv_dicts(name):
    path = _DATA_DIR / name
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


_checkout_missing_rows = _load_csv_dicts('test_checkout_missing_info_validation.csv')


@pytest.mark.CHECKOUT
class TestCheckout:
    ERROR_SELECTOR = "[data-test='error']"
    item = 'Sauce Labs Backpack'

    @staticmethod
    def login_and_add_items(page, request, items):
        log.info('Start helper login_and_add_items items=%s', items)
        base_url = request.config.getini('base_url')
        login = LoginPage(page, base_url)
        log.info('Navigating to login page: %s', base_url)
        login.navigate()
        standard_app_user = request.getfixturevalue('standard_app_user')
        valid_password = request.getfixturevalue('valid_password')
        log.info('Logging in user=%s', standard_app_user)
        login.login(standard_app_user, valid_password)
        assert login.is_logged_in(), f'Login failed for {standard_app_user}'
        log.info('Login successful user=%s', standard_app_user)

        inventory = InventoryPage(page, base_url)
        for name in items:
            log.info('Adding item to cart: %s', name)
            inventory.add_item_by_name(name)
        cart_count = inventory.get_cart_count()
        log.info('Cart count now=%s expected=%s', cart_count, len(items))
        assert cart_count == len(items)
        log.info('Opening cart page')
        inventory.open_cart()
        return {'cart': CartPage(page, base_url), 'inventory': inventory}

    @staticmethod
    def proceed_to_overview(page, request, first='John', last='Doe', postal='12345'):
        log.info('Proceed to overview first=%s last=%s postal=%s', first, last, postal)
        base_url = request.config.getini('base_url')
        info = CheckoutInfoPage(page, base_url)
        info.continue_to_overview(first, last, postal)
        log.info('Reached overview page')
        return CheckoutOverviewPage(page, base_url)

    def test_checkout_single_item_success(self, page, request):
        log.info('TEST START: test_checkout_single_item_success')
        ctx = self.login_and_add_items(page, request, [self.item])
        log.info('Proceed to checkout info from cart')
        ctx['cart'].proceed_to_checkout()

        overview = self.proceed_to_overview(page, request)
        log.info('Verifying item present in overview: %s', self.item)
        assert self.item in overview.get_item_names()
        log.info('Finishing checkout')
        overview.finish_checkout()

        complete = CheckoutCompletePage(page, request.config.getini('base_url'))
        assert complete.is_complete()
        txt = complete.get_complete_text().lower()
        log.info('Completion text lower=%s', txt)
        assert 'dispatch' in txt or 'thank' in txt
        log.info('TEST END: test_checkout_single_item_success')

    def test_checkout_multiple_items_success(self, page, request):
        log.info('TEST START: test_checkout_multiple_items_success')
        items = ['Sauce Labs Backpack', 'Sauce Labs Bike Light', 'Sauce Labs Bolt T-Shirt']
        ctx = self.login_and_add_items(page, request, items)
        log.info('Proceed to checkout info from cart')
        ctx['cart'].proceed_to_checkout()

        overview = self.proceed_to_overview(page, request)
        overview_items = overview.get_item_names()
        log.info('Overview items: %s', overview_items)
        for i in items:
            assert i in overview_items
            log.info('Verified item in overview: %s', i)
        log.info('Finishing checkout for multiple items')
        overview.finish_checkout()
        complete = CheckoutCompletePage(page, request.config.getini('base_url'))
        assert complete.is_complete()
        log.info('TEST END: test_checkout_multiple_items_success')

    @pytest.mark.parametrize(
        'missing_field, first, last, postal, expected_error',
        [(r['missing_field'], r['first'], r['last'], r['postal'], r['expected_error']) for r in _checkout_missing_rows],
    )
    @pytest.mark.PARAMETERIZED
    def test_checkout_missing_info_validation(self, page, request, missing_field, first, last, postal, expected_error):
        log.info('TEST START: test_checkout_missing_info_validation missing_field=%s', missing_field)
        ctx = self.login_and_add_items(page, request, [self.item])
        ctx['cart'].proceed_to_checkout()
        base_url = request.config.getini('base_url')
        info = CheckoutInfoPage(page, base_url)
        log.info('Submitting checkout info with potential missing field=%s', missing_field)
        info.continue_to_overview(first, last, postal)
        err_text = page.locator(self.ERROR_SELECTOR).inner_text()
        log.info('Received error text: %s', err_text)
        assert err_text.startswith(expected_error)
        log.info('Validation matched expected=%s', expected_error)
        log.info('TEST END: test_checkout_missing_info_validation')

    def test_cancel_in_overview_returns_inventory(self, page, request):
        log.info('TEST START: test_cancel_in_overview_returns_inventory')
        items = [self.item]
        ctx = self.login_and_add_items(page, request, items)
        ctx['cart'].proceed_to_checkout()
        overview = self.proceed_to_overview(page, request)
        log.info('Cancelling from overview')
        overview.cancel()
        inventory = InventoryPage(page, request.config.getini('base_url'))
        cart_count = inventory.get_cart_count()
        log.info('Back to inventory cart_count=%s expected=%s', cart_count, len(items))
        assert cart_count == len(items)
        log.info('TEST END: test_cancel_in_overview_returns_inventory')

    def test_checkout_then_logout(self, page, request):
        log.info('TEST START: test_checkout_then_logout')
        ctx = self.login_and_add_items(page, request, [self.item])
        ctx['cart'].proceed_to_checkout()
        overview = self.proceed_to_overview(page, request)
        log.info('Verifying item before finishing checkout')
        assert self.item in overview.get_item_names()
        overview.finish_checkout()
        log.info('Finished checkout; verifying completion page')
        complete = CheckoutCompletePage(page, request.config.getini('base_url'))
        assert complete.is_complete()

        log.info('Navigating back to products')
        complete.back_to_products()
        inventory = InventoryPage(page, request.config.getini('base_url'))
        log.info('Inventory cart count=%s (sanity)', inventory.get_cart_count())

        log.info('Logging out')
        login_page = LoginPage(page, request.config.getini('base_url'))
        login_page.logout_and_verify()
        assert not login_page.is_logged_in()
        log.info('Logout verified')
        log.info('TEST END: test_checkout_then_logout')
