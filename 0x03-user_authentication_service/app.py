#!/usr/bin/env python3
"""
flask app for auth
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome():
    """
    returns json payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def registered_users():
    """
    register a user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        res = {"email": email, "message": "user created"}
        return jsonify(res), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    login with user
    """
    user_email = request.form.get('email')
    user_pwd = request.form.get('password')
    if not AUTH.valid_login(user_email, user_pwd):
        abort(401)
    session_id = AUTH.create_session(user_email)
    result = jsonify({"email": user_email, "message": "logged in"})
    result.set_cookie('session_id', session_id)
    return result


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    logs a user out
    """
    ses_id = request.cookies.get('session_id')
    if ses_id is None:
        abort(403)
    exis_user = AUTH.get_user_from_session_id(ses_id)
    if exis_user is None:
        abort(403)
    AUTH.destroy_session(exis_user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
    returns a email
    """
    ses_id = request.cookies.get('session_id')
    if ses_id is None:
        abort(403)
    usr = AUTH.get_user_from_session_id(ses_id)
    if usr is None:
        abort(403)
    return jsonify({"email": usr.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    resets the password
    """
    try:
        usr_email = request.form.get('email')
        t = AUTH.get_reset_password_token(usr_email)
        return jsonify({"email": usr_email, "reset_token": t}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
