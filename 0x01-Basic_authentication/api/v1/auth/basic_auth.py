#!/usr/bin/env python3
"""
script for task 7
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    basic auth class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        returns base 64
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        returns decoded base 64
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            benc = base64_authorization_header.encode('utf-8')
            bdec = b64decode(benc)
            dec_val = bdec.decode('utf-8')
            return dec_val
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        returns users and emails
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        cred, pwd = decoded_base64_authorization_header.split(':', 1)
        return cred, pwd
