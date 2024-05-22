#!/usr/bin/env python3
"""
handles routes for task 7
"""
from flask import request, jsonify, abort
from typing import Tuple
from models.user import User
import os
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> Tuple[str, int]:
    nowt = {"error": "no user found for this email"}
    user_email = request.form.get('email')
    if user_email is None or len(user_email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    user_password = request.form.get('password')
    if user_password is None or len(user_password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        user = User.search({'email': user_email})
    except Exception:
        return jsonify(nowt), 404
    if len(user) <= 0:
        return jsonify(nowt), 404
    if user[0].is_valid_password(user_password):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(user[0], 'id'))
        us = jsonify(user[0].to_json())
        us.set_cookie(os.getenv('SESSION_NAME'), session_id)
        return us

    return jsonify({"error": "wrong password"}), 401


"""@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout() -> str:
    
    logging out def
    
    from api.v1.app import auth
    destroy_session = auth.destroy_session(request)
    if destroy_session is False:
        abort(404)
    else:
        return jsonify({}), 200"""
