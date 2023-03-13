from datetime import datetime

import jwt

from .env import get_env, ENV, set_env
from .api import get_token


def is_token_expired(token: str | None) -> bool:
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        now = int(datetime.now().timestamp())
    except:
        return True
    return now > decoded['exp'] - 60


def renew_api_token() -> str | None:
    payload = {
        'client_id': get_env(ENV.CLIENT_ID),
        'client_secret': get_env(ENV.CLIENT_SECRET),
        'audience': get_env(ENV.AUDIENCE),
        'grant_type': get_env(ENV.GRANT_TYPE)
    }
    api_token = get_token(get_env(ENV.AUTH0_HOST), payload)
    if api_token is not None:
        set_env(ENV.API_TOKEN, api_token)
    return api_token
