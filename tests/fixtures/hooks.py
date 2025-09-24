import re
from pathlib import Path
import configparser
import os
import pytest
import allure
from allure_commons.types import AttachmentType

from test_client.util.logger import get_logger

log = get_logger(__name__)


def pytest_addoption(parser):
    # New ini options (all overridable via pytest.ini)
    parser.addini('browser', 'Browser engine: chromium|firefox|webkit', default='chromium')
    parser.addini('channel', 'Chromium channel: chrome|msedge|', default='')
    parser.addini('headless', 'Run headless: true|false', default='true')
    parser.addini('viewport', 'Viewport size WxH', default='1280x720')
    parser.addini('record_video', 'Record video: true|false', default='true')
    parser.addini('slowmo', 'Slow motion (ms)', default='0')
    parser.addini('screenshot_on', 'Screenshot capture: always|teardown|failure', default='teardown')
    parser.addini('allure_dir', 'Allure results directory', default='reports/json')
    parser.addini('base_url', 'Base URL for app under test', default='https://www.saucedemo.com')
    parser.addini('app_password_env', 'Environment variable name or placeholder for valid app password', default='APP_PASSWORD')
    parser.addini('standard_app_user_env', 'Environment variable name or placeholder for standard app user', default='STANDARD_APP_USER')
    parser.addini('app_password_env', 'Environment variable name or placeholder for valid app password', default='APP_PASSWORD')
    parser.addoption(
        '--env', action='store', default=os.environ.get('TEST_ENV', 'local'), help='Environment to use (matches section [env.<name>] in pytest.ini)'
    )


def _load_env_overrides(config):
    """Load overrides from pytest.ini section [env.<name>] if present."""
    env_name = config.getoption('env')
    log.info(f'Using test environment: {env_name}')
    overrides = {}
    ini_file = config.inifile
    if ini_file and Path(ini_file).is_file():
        cp = configparser.ConfigParser()
        cp.read(ini_file, encoding='utf-8')
        section = f'env.{env_name}'
        if cp.has_section(section):
            for k, v in cp.items(section):
                overrides[k] = v
    config._active_env = env_name
    config._env_overrides = overrides


def _final(config, key):
    return config._env_overrides.get(key, config.getini(key))


# --- Allure results directory bootstrap (now uses allure_dir ini + env overrides) --------
def pytest_configure(config):
    _load_env_overrides(config)  # must happen first

    # --- Generic processing of ini keys ending with '_env' that use ${VAR} placeholders ---
    ini_file = config.inifile
    placeholder_re = re.compile(r'^\s*\$\{([A-Za-z_][A-Za-z0-9_]*)\}\s*$')
    try:
        if ini_file and Path(ini_file).is_file():
            cp = configparser.ConfigParser()
            cp.read(ini_file, encoding='utf-8')
            if cp.has_section('pytest'):
                for key, _ in cp.items('pytest'):
                    if not key.endswith('_env'):
                        continue
                    val = _final(config, key)
                    m = placeholder_re.match(str(val or ''))
                    if not m:
                        # If not a placeholder like ${VAR}, store raw value as the env-name and leave resolved as None
                        base = key[:-4]
                        config.__dict__[f'_{base}_env'] = val
                        config.__dict__[f'_{base}'] = None
                        continue
                    env_var_name = m.group(1)
                    resolved = os.environ.get(env_var_name)
                    if resolved is None:
                        raise pytest.UsageError(f'Environment variable {env_var_name} must be set (referenced by ini key `{key}`)')
                    base = key[:-4]
                    # store both the env var name and the resolved value for tests/fixtures
                    config.__dict__[f'_{base}_env'] = env_var_name
                    config.__dict__[f'_{base}'] = resolved
    except Exception:
        # keep best-effort behavior; let other code handle failures where appropriate
        raise

    # --- Allure/results bootstrap (use final values) ---
    allure_dir = getattr(config.option, 'allure_report_dir', None)
    if not allure_dir:
        allure_dir = _final(config, 'allure_dir')
        config.option.allure_report_dir = allure_dir
    results_dir = Path(allure_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    # Dynamic environment.properties (use final values)
    try:
        env_file = results_dir / 'environment.properties'
        keys = ['base_url', 'browser', 'channel', 'headless', 'viewport', 'record_video', 'slowmo', 'screenshot_on']
        env_lines = [
            f'EnvName={config._active_env}',
            *[f'{k}={_final(config, k)}' for k in keys],
            f'standard_app_user={getattr(config, "_standard_app_user_env", "")}',
            f'Python={os.sys.version.split()[0]}',
            f'OS={os.name}',
        ]
        env_file.write_text('\n'.join(env_lines) + '\n', encoding='utf-8')
    except Exception:
        pass


# Add failure-time screenshot (covers early failures before fixture teardown)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when != 'call' or rep.passed or rep.skipped:
        return
    policy = item.config.getini('screenshot_on').lower()
    if policy not in ('always', 'failure'):
        return
    page = item.funcargs.get('page')
    if not page:
        return
    try:
        allure.attach(page.screenshot(full_page=True), name=f'Failure Screenshot - {item.name}', attachment_type=AttachmentType.PNG)
    except Exception:
        pass
