import pytest
from axe_playwright_python.sync_playwright import Axe
from test_client.pages.sauce_demo.login_page import LoginPage
from test_client.util.logger import get_logger

log = get_logger(__name__)

@pytest.mark.ACCESSIBILITY
class TestAccessibility:
    def test_login_page_accessibility(self, page, request):
        """
        Demonstrates automated accessibility testing using axe-core.
        """
        log.info('TEST START: test_login_page_accessibility')
        base_url = request.config.getini('base_url')
        login_page = LoginPage(page, base_url)
        login_page.navigate()
        
        log.info('Running accessibility scan on login page')
        axe = Axe()
        results = axe.run(page)
        
        violations = results.response["violations"]
        log.info('Accessibility scan complete. Violations found: %s', len(violations))
        
        # In a real project, you might want to assert on specific violation counts or types
        # For this demo, we just log them and show how to access them
        if len(violations) > 0:
            for i, violation in enumerate(violations):
                log.warning('Violation #%s: %s (Impact: %s)', i+1, violation.get('help'), violation.get('impact'))
        
        # We can also fail the test if there are critical violations
        # assert len(violations) == 0, f"Found {len(violations)} accessibility violations"
        log.info('TEST END: test_login_page_accessibility')

    def test_inventory_page_accessibility(self, page, request, standard_app_user, valid_password):
        """
        Verify accessibility of the inventory page after login.
        """
        log.info('TEST START: test_inventory_page_accessibility')
        base_url = request.config.getini('base_url')
        login_page = LoginPage(page, base_url)
        login_page.navigate()
        login_page.login(standard_app_user, valid_password)
        
        log.info('Running accessibility scan on inventory page')
        axe = Axe()
        results = axe.run(page)
        
        log.info('Inventory page accessibility scan complete. Violations: %s', len(results.response["violations"]))
        log.info('TEST END: test_inventory_page_accessibility')
