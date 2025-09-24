from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, Iterable, Sequence
import threading
import yaml

__LOCATORS_CACHE: Dict[str, Any] | None = None
__LOCK = threading.Lock()

_DEFAULT_PREFERENCE: Sequence[str] = ('id', 'css', 'xpath', 'role', 'text')


def _locators_path() -> Path:
    return Path(__file__).resolve().parents[2] / 'config' / 'locators.yml'


def load_locators(force: bool = False) -> Dict[str, Any]:
    global __LOCATORS_CACHE
    if __LOCATORS_CACHE is None or force:
        with __LOCK:
            if __LOCATORS_CACHE is None or force:
                with _locators_path().open('r', encoding='utf-8') as f:
                    __LOCATORS_CACHE = yaml.safe_load(f) or {}
    return __LOCATORS_CACHE


def get_page_section(page_name: str) -> Dict[str, Dict[str, str]]:
    data = load_locators()
    page = data.get(page_name)
    if page is None:
        raise KeyError(f"Page '{page_name}' not found in {_locators_path()}")
    return page


def get_locator(page_name: str, key: str, prefer: Iterable[str] = _DEFAULT_PREFERENCE) -> str:
    """
    Resolve a locator by key for a page.
    Preference order: css > id > xpath > role > text (configurable).
    If type == id and value not prefixed, convert to '#value'.
    """
    page = get_page_section(page_name)
    searched = set()
    for loc_type in prefer:
        section = page.get(loc_type)
        if section and key in section:
            value = section[key]
            if loc_type == 'id':
                # Normalize id to CSS id selector
                if not value.startswith('#'):
                    value = f'#{value}'
            return value
        if loc_type in page:
            searched.add(loc_type)
    # Fallback: search remaining types not in preference list
    for loc_type, section in page.items():
        if loc_type in searched:
            continue
        if key in section:
            value = section[key]
            if loc_type == 'id' and not value.startswith('#'):
                value = f'#{value}'
            return value
    raise KeyError(f"Locator key '{key}' not found for page '{page_name}'")


def list_keys(page_name: str) -> Dict[str, list[str]]:
    page = get_page_section(page_name)
    return {loc_type: list(keys.keys()) for loc_type, keys in page.items()}
