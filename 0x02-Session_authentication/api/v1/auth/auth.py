#!/usr/bin/env python3
"""
script for task 3
"""

from typing import List, TypeVar
from flask import Flask, request
import os


class Auth:
    """
    class for authentication management
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        def for auth requirement
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if not path.endswith('/'):
            path += '/'
        for pathing in excluded_paths:
            if pathing.endswith('*'):
                if path.startswith(pathing[:-1]):
                    return False
        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """
        def for header
        """
        if request is None:
            return None
        if not request.headers.get("Authorization"):
            return None
        else:
            return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        def for user
        """
        return None

    def session_cookie(self, request=None):
        """
        returns a cookie
        """
        if request is None:
            return None
        ses_name = os.getenv('SESSION_NAME')
        res = request.cookies.get(ses_name)
        return res
