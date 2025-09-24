import pytest
from test_client.pages.sauce_demo.login_page import LoginPage
from test_client.util.logger import get_logger
from pathlib import Path
import csv

log = get_logger(__name__)

_DATA_DIR = Path(__file__).resolve().parent.parent / 'config' / 'data'


def _load_csv_dicts(name):
    path = _DATA_DIR / name
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


_login_success_rows = _load_csv_dicts('test_login_success.csv')
_login_failure_rows = _load_csv_dicts('test_login_failure.csv')


@pytest.fixture
def login_page(page, request):
    base_url = request.config.getini('base_url')
    log.info('Fixture login_page navigate base_url=%s', base_url)
    lp = LoginPage(page, base_url.rstrip('/'))
    lp.navigate('')
    return lp


@pytest.mark.LOGIN
class TestLogin:
    # Positive (successful) login scenarios
    @pytest.mark.parametrize(
        'username',
        [(r['username']) for r in _login_success_rows],
    )
    @pytest.mark.PARAMETERIZED
    def test_login_success(self, login_page, username, valid_password):
        log.info('TEST START: test_login_success user=%s', username)
        login_page.login(username, valid_password)
        log.info('Login submitted for user=%s', username)
        assert login_page.is_logged_in(), f'Expected successful login for {username}'
        log.info('Login success verified user=%s', username)
        log.info('TEST END: test_login_success user=%s', username)

    # Negative (failed) login scenarios
    @pytest.mark.parametrize(
        'username,password,expected_error_start',
        [(r['username'], r['password'], r['expected_error_start']) for r in _login_failure_rows],
    )
    @pytest.mark.PARAMETERIZED
    def test_login_failure(self, login_page, valid_password, username, password, expected_error_start):
        log.info('TEST START: test_login_failure user=%s expected_error_prefix=%s', username, expected_error_start)
        use_pwd = valid_password if password == 'valid_password' else password
        login_page.login(username, use_pwd)
        log.info('Login attempt (expected fail) user=%s', username)
        assert not login_page.is_logged_in(), f'Login unexpectedly succeeded for {username}'
        error_text = login_page.get_error_text()
        log.info('Captured error text: %s', error_text)
        assert error_text.startswith(expected_error_start), f'Unexpected error text: {error_text}'
        log.info('Error assertion passed user=%s', username)
        log.info('TEST END: test_login_failure user=%s', username)
