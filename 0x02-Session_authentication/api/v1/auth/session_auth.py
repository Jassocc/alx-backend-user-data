#!/usr/bin/env python3
"""
script for task 2
"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """
    defines auth's for sessions
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a nid
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        ses_id = str(uuid.uuid4())
        self.user_id_by_session_id[ses_id] = user_id
        return ses_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a user based on a session
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        res = self.user_id_by_session_id.get(session_id)
        return res

    def current_user(self, request=None):
        """
        delete a user ses
        """
        cook = self.session_cookie(request)
        if cook is None:
            return None
        users = self.user_id_for_session_id(cook)
        res = User.get(users)
        return res

    def destroy_session(self, request=None):
        """
        destroys a ses
        """
        if request is None:
            return False
        ses_id = self.session_cookie(request)
        if not ses_id:
            return False
        usr = self.user_id_for_session_id(ses_id)
        if not usr:
            return False
        del self.user_id_by_session_id[ses_id]
        return True
