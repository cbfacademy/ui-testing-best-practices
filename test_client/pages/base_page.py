from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def navigate(self, path: str = ''):
        self.page.goto(f'{self.base_url}/{path}')

    def get_element(self, selector: str):
        return self.page.locator(selector)

    def click_element(self, selector: str):
        self.get_element(selector).click()

    def fill_input(self, selector: str, text: str):
        self.get_element(selector).fill(text)

    def expect_element_visible(self, selector: str):
        expect(self.get_element(selector)).to_be_visible()

    def expect_element_text(self, selector: str, text: str):
        expect(self.get_element(selector)).to_have_text(text)

    def verify_title(self, expected_title: str):
        expect(self.page).to_have_title(f'*{expected_title}.*', use_regex=True)
