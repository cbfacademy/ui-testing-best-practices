import pytest

from test_client.util.logger import get_logger

log = get_logger(__name__)

pytest_plugins = [
    'tests.fixtures.hooks',
    'tests.fixtures.browser',
]


@pytest.fixture(scope='session')
def valid_password(request):
    """Resolved valid password from environment (never defaults)."""
    return request.config._app_password


@pytest.fixture(scope='session')
def standard_app_user(request):
    """Resolved standard app user from environment (never defaults)."""
    return request.config._standard_app_user
