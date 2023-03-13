from datetime import datetime
from unittest import TestCase

import jwt
from dotenv import load_dotenv, find_dotenv

from src.app.utils import is_token_expired

load_dotenv(dotenv_path=find_dotenv())


class JwtTest(TestCase):
    def test_none_jwt(self):
        token = None
        self.assertTrue(is_token_expired(token))

    def test_expired_jwt(self):
        now = int(datetime.now().timestamp())
        key = 'secret'
        payload = {"exp": now - 1}
        token = jwt.encode(payload, key)
        self.assertTrue(is_token_expired(token))

    def test_unexpired_jwt(self):
        now = int(datetime.now().timestamp())
        key = 'secret'
        payload = {"exp": now + 60}
        token = jwt.encode(payload, key)
        self.assertFalse(is_token_expired(token))
