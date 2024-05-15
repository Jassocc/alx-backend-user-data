#!/usr/bin/env python3
"""
script for task5-6
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    returns hashed passwd
    """
    crypted = password.encode()
    hash_pwd = bcrypt.hashpw(crypted, bcrypt.gensalt())
    return hash_pwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    check if pwd matches
    """
    status = False
    encription = password.encode()
    if bcrypt.checkpw(encription, hashed_password):
        status = True
    return status
