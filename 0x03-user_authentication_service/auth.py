#!/usr/bin/env python3
"""
handling authentication
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid


def _hash_password(password: str) -> str:
    """
    hash password
    """
    passw_bytes = password.encode('utf-8')
    hash_passw = bcrypt.hashpw(passw_bytes, bcrypt.gensalt())
    return hash_passw


class Auth:
    """
    auth class for db
    """

    def __init__(self):
        """
        initialiser for class
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        registers a new user
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hash_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hash_pwd)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        checks if password is correct
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False
        else:
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
