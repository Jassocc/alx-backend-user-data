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
