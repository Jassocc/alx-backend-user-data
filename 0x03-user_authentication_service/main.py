#!/usr/bin/env python3
"""
trsting for flask
"""
import requests


URL = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """
    test reg user
    """
    response = {"email": email, "password": password}
    result = requests.post(f'{URL}/users', response)
    assert result.status_code == 201


def log_in_wrong_password(email: str, password: str) -> None:
    """
    login with wrong password
    """
    response = {"email": email, "password": password}
    result = requests.post(f'{URL}/sessions', response)
    assert result.status_code == 401

def log_in(email: str, password: str) -> str:
    """
    log in user
    """
    response = {"email": email, "password": password}
    result = requests.post(f'{URL}/sessions', response)
    assert result.status_code == 200

def profile_unlogged() -> None:
    """
    profile unlog
    """
    ses = {"session_id": ""}
    result = requests.get(f'{URL}/profile', ses)
    assert result.status_code == 403

def profile_logged(session_id: str) -> None:
    """
    profile in log
    """
    ses = {"session_id": session_id}
    result = requests.get(f'{URL}/profile', ses)
    assert result.status_code == 200

def log_out(session_id: str) -> None:
    """
    log user ouit
    """
    ses = {"session_id": session_id}
    result = requests.delete(f'{URL}/sessions', ses)
    assert result.status_code == 204

def reset_password_token(email: str) -> str:
    """
    pwd reset
    """
    eml = {"email": email}
    result = requests.post(f'{URL}/reset_password', eml)
    assert result.status_code == 200

def update_password(email: str, reset_token: str, new_password: str) -> None:
    eml = {"email": email, "reset_token": reset_token,
           "new_password": new_password}
    result = requests.put(f'{URL}/reset_password', eml)
    assert result.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
