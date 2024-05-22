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
    usr_eml = request.form.get('email')
    if not usr_eml:
        return jsonify({"error": "email missing"}), 400
    usr_pwd = request.form.get('password')
    if not usr_pwd:
        return jsonify({ "error": "password missing" }), 400
    usr = User.search({'email': usr_eml})
    if not usr:
        return jsonify({"error": "no user found for this email"}), 404

    for us in usr:
        if us.is_valid_password(usr_pwd):
            from api.v1.app import auth
            ses_id = auth.create_session(us.id)
            user_json = jsonify(us.to_json())
            user_json.set_cookie(os.getenv('SESSION_NAME'), ses_id)
            return user_json
        else:
            return jsonify({"error": "wrong password"}), 401

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
