#!/usr/bin/env python3
"""
handles routes for task 7
"""
from flask import request, jsonify, abort
from typing import Tuple
from models.user import User
import os
from api.v1.views import app_views


@app_views.route('/auth_session/login/', methods=['POST'],
                 strict_slashes=False)
def session_login() -> Tuple[str, int]:
    """
    logging in for defs
    """
    from api.v1.app import auth
    user_email = request.form.get('email')
    password = request.form.get('password')

    if user_email is None:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': user_email})

    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    session_id = auth.create_session(user.id)
    usa = user.to_json()
    resp = jsonify(usa)
    resp.set_cookie(os.getenv('SESSION_NAME'), session_id)

    return resp, 200


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout() -> str:
    """
    logging out def
    """
    from api.v1.app import auth
    destruct = auth.destroy_session(request)
    if destruct is False:
        abort(404)
    else:
        return jsonify({}), 200
