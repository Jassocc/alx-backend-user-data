#!/usr/bin/env python3
"""
script for task 3
"""

from typing import List, TypeVar
from flask import Flask, request


class Auth:
    """
    class for authentication management
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        def for auth requirement
        """
        return False


    def authorization_header(self, request=None) -> str:
        """
        def for header
        """
        if request is None:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        def for user
        """
        return None
