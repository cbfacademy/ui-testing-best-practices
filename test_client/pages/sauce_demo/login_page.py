from playwright.sync_api import expect
from test_client.pages.base_page import BasePage
from test_client.util.util import get_locator


class LoginPage(BasePage):
    # keys only
    USERNAME = 'username'
    PASSWORD = 'password'
    LOGIN_BUTTON = 'login_button'
    ERROR_MESSAGE = 'error_message'
    INVENTORY_CONTAINER = 'inventory_container'
    MENU_BUTTON = 'menu_button'
    LOGOUT_LINK = 'logout_link'

    def _loc(self, key: str) -> str:
        return get_locator('login_page', key)

    def navigate(self, path: str = ''):
        # navigate to the project base_url (pytest.ini) root or a given path
        super().navigate(path)

    def login(self, username: str, password: str):
        # fill credentials and submit
        self.fill_input(self._loc(self.USERNAME), username)
        self.fill_input(self._loc(self.PASSWORD), password)
        self.click_element(self._loc(self.LOGIN_BUTTON))

    def login_and_verify(self, username: str, password: str, timeout: int = 5000):
        # perform login and verify inventory page is visible
        self.login(username, password)
        expect(self.page.locator(self._loc(self.INVENTORY_CONTAINER))).to_be_visible(timeout=timeout)

    def get_error_text(self) -> str:
        # return visible error message text after failed login
        return self.get_element(self._loc(self.ERROR_MESSAGE)).inner_text()

    def is_logged_in(self, timeout: int = 2000) -> bool:
        # quick check if login succeeded by checking inventory container visibility
        try:
            expect(self.page.locator(self._loc(self.INVENTORY_CONTAINER))).to_be_visible(timeout=timeout)
            return True
        except Exception:
            return False

    def logout(self):
        self.click_element(self._loc(self.MENU_BUTTON))
        self.click_element(self._loc(self.LOGOUT_LINK))

    def logout_and_verify(self, timeout: int = 5000):
        self.logout()
        expect(self.page.locator(self._loc(self.USERNAME))).to_be_visible(timeout=timeout)
