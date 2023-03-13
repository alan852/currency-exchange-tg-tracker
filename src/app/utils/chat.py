from typing import TypedDict

from .env import get_env, ENV


class ChatIds(TypedDict):
    admins: set
    users: set


def get_chat_ids() -> ChatIds:
    admins = get_env(ENV.ADMIN_CHAT_ID)
    admins = {int(admins)} if admins is not None and admins != '' else set()
    users = get_env(ENV.ALLOWED_CHAT_IDS)
    users = {int(_) for _ in users.split(',') if _ != ''} \
        if users is not None and users != '' else set()
    return {'admins': admins, 'users': users}
