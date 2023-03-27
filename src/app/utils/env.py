import os
from enum import Enum


class ENV(Enum):
    TELEGRAM_BOT_TOKEN = {'name': 'TELEGRAM_BOT_TOKEN', 'default': ''}
    ADMIN_CHAT_ID = {'name': 'ADMIN_CHAT_ID', 'default': ''}
    ALLOWED_CHAT_IDS = {'name': 'ALLOWED_CHAT_IDS', 'default': ''}
    FIRST_MINUTE = {'name': 'FIRST_MINUTE', 'default': '0'}
    REPORT_FREQUENCY = {'name': 'REPORT_FREQUENCY', 'default': '60'}
    LOG_FORMAT = {'name': 'LOG_FORMAT', 'default': ''}
    LOG_LEVEL = {'name': 'LOG_LEVEL', 'default': 'INFO'}
    API_HOST = {'name': 'API_HOST', 'default': ''}
    SYMBOLS = {'name': 'SYMBOLS', 'default': ''}
    JSON_TIMESTAMP_FORMAT = {'name': 'JSON_TIMESTAMP_FORMAT', 'default': ''}
    DISPLAY_TZ = {'name': 'DISPLAY_TZ', 'default': ''}
    DISPLAY_TIMESTAMP_FORMAT = {'name': 'DISPLAY_TIMESTAMP_FORMAT', 'default': ''}
    AUTH0_HOST = {'name': 'AUTH0_HOST', 'default': ''}
    CLIENT_ID = {'name': 'CLIENT_ID', 'default': ''}
    CLIENT_SECRET = {'name': 'CLIENT_SECRET', 'default': ''}
    AUDIENCE = {'name': 'AUDIENCE', 'default': ''}
    GRANT_TYPE = {'name': 'GRANT_TYPE', 'default': ''}
    HEALTH_CHECK_PUSH_URL = {'name': 'HEALTH_CHECK_PUSH_URL', 'default': ''}
    API_TOKEN = {'name': 'API_TOKEN', 'default': ''}


def get_env(env: ENV) -> str | None:
    return os.environ.get(env.value['name'], env.value['default'])


def set_env(env: ENV, value: str) -> None:
    os.environ[env.value['name']] = value
