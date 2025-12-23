import pytest
from playwright.sync_api import APIRequestContext
from test_client.util.logger import get_logger

log = get_logger(__name__)

@pytest.fixture(scope="session")
def api_request_context(playwright, request):
    base_url = request.config.getini('base_url')
    request_context = playwright.request.new_context(base_url=base_url)
    yield request_context
    request_context.dispose()

@pytest.mark.API
class TestAPI:
    def test_verify_home_page_status(self, api_request_context: APIRequestContext):
        """
        Demonstrates using Playwright as an API client to verify endpoint health.
        """
        log.info('TEST START: test_verify_home_page_status')
        response = api_request_context.get("/")
        log.info('Received status code: %s', response.status)
        assert response.ok
        assert response.status == 200
        log.info('TEST END: test_verify_home_page_status')

    def test_verify_assets_load(self, api_request_context: APIRequestContext):
        """
        Verify that key assets (like the favicon) are reachable.
        """
        log.info('TEST START: test_verify_assets_load')
        response = api_request_context.get("/favicon.ico")
        log.info('Asset status: %s', response.status)
        assert response.status == 200
        log.info('TEST END: test_verify_assets_load')
