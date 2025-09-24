import re
import subprocess
import time
import shutil
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright
import allure
from allure_commons.types import AttachmentType

from test_client.util.logger import get_logger

log = get_logger(__name__)


@pytest.fixture(scope='session', autouse=True)
def install_playwright(request):
    config_value = get_config_values(request)
    browser_name = config_value('browser').lower()
    subprocess_command_parts = ['playwright', 'install', browser_name]
    if _bool(config_value('headless')):
        subprocess_command_parts.append('--only-shell')
    subprocess.run(subprocess_command_parts, check=False)


def _final(config, key):
    return config._env_overrides.get(key, config.getini(key))


def _bool(v: str) -> bool:
    return str(v).strip().lower() in ('1', 'true', 'yes', 'on')


def _parse_viewport(v: str):
    try:
        w, h = v.lower().split('x')
        return int(w), int(h)
    except Exception:
        return 1280, 720


def _sanitize_filename(name: str) -> str:
    """Sanitize test nodeid to a filesystem-safe filename."""
    name = re.sub(r'[^A-Za-z0-9._-]', '_', name)
    return name


@pytest.fixture(scope='function')
def page(request, tmp_path):
    """Create a Playwright page with per-test video recording.

    Video files are produced in a temporary directory and moved to
    `test-results/videos` with a sanitized test name and timestamp.
    """
    # --- read final (env-aware) config ---
    config_value = get_config_values(request)
    browser_name = config_value('browser').lower()
    channel = config_value('channel').strip()
    headless = _bool(config_value('headless'))
    viewport_w, viewport_h = _parse_viewport(config_value('viewport'))
    record_video = _bool(config_value('record_video'))
    slowmo = int(config_value('slowmo') or 0)
    screenshot_policy = config_value('screenshot_on').lower()  # always|teardown|failure
    base_url = config_value('base_url')
    # --------------------------------

    videos_dir = tmp_path / 'videos'
    if record_video:
        videos_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        # Select browser
        if browser_name == 'firefox':
            browser_type = p.firefox
        elif browser_name == 'webkit':
            browser_type = p.webkit
        else:
            browser_name = 'chromium'
            browser_type = p.chromium

        launch_kwargs = {'headless': headless}
        if browser_name == 'chromium' and channel:
            launch_kwargs['channel'] = channel
        if slowmo:
            launch_kwargs['slow_mo'] = slowmo

        browser = browser_type.launch(**launch_kwargs)

        context_kwargs = {
            'viewport': {'width': viewport_w, 'height': viewport_h},
        }
        if record_video:
            context_kwargs['record_video_dir'] = str(videos_dir)

        context = browser.new_context(**context_kwargs)
        page = context.new_page()

        # Navigate to base_url early (convenience)
        try:
            page.goto(base_url, wait_until='domcontentloaded')
        except Exception:
            pass

        yield page

        # Teardown screenshot (if policy allows)
        if screenshot_policy in ('always', 'teardown'):
            try:
                screenshot_path = tmp_path / 'screenshot.png'
                page.screenshot(path=str(screenshot_path), full_page=True)
                allure.attach.file(str(screenshot_path), name=f'Screenshot - {request.node.name}', attachment_type=AttachmentType.PNG)
            except Exception:
                pass

        context.close()
        browser.close()

    # Video handling
    if record_video:
        files = list(videos_dir.rglob('*.webm'))
        if files:
            latest = max(files, key=lambda p: p.stat().st_mtime)
            dest_dir = Path.cwd() / 'test-results' / 'videos'
            dest_dir.mkdir(parents=True, exist_ok=True)
            test_name = _sanitize_filename(request.node.nodeid)
            timestamp = int(time.time())
            dest = dest_dir / f'{test_name}_{timestamp}.webm'
            try:
                shutil.move(str(latest), str(dest))
            except Exception:
                pass
            if dest.exists():
                try:
                    allure.attach.file(str(dest), name=f'Video - {request.node.name}', attachment_type=AttachmentType.WEBM)
                except Exception:
                    pass


def get_config_values(request):
    cfg = request.config
    get = lambda k: _final(cfg, k)
    return get
