#!/usr/bin/env python3
"""
handles routes for task 7
"""
from flask import request, jsonify, abort
from models.user import User
import os
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    user_email = request.form.get('email')
    if not user_email:
        return jsonify({"error": "email missing"}), 400
    user_password = request.form.get('password')
    if not user_password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': user_email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    for us in user:
        if us.is_valid_password(user_password):
            from api.v1.app import auth
            session_id = auth.create_session(us.id)
            user_json = jsonify(us.to_json())
            user_json.set_cookie(os.getenv('SESSION_NAME'), session_id)
            return user_json

    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout() -> str:
    """
    logging out def
    """
    from api.v1.app import auth
    destroy_session = auth.destroy_session(request)
    if destroy_session is False:
        abort(404)
    else:
        return jsonify({}), 200
