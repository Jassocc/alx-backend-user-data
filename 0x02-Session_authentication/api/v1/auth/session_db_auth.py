#!/usr/bin/env python3
"""
script for task 10
"""
from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    method for class
    """

    def create_session(self, user_id=None):
        """
        creates a session
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        usr_ses = UserSession(user_id=user_id, session_id=session_id)
        usr_ses.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        returns id for session
        """
        if session_id is None:
            return None
        UserSession.load_from_file()
        usr_ses = UserSession.search({'session_id': session_id})
        if len(usr_ses) == 0:
            return None
        if self.session_duration <= 0:
            return usr_ses[0].user_id
        creat = usr_ses[0].created_at
        if (creat +
                timedelta(seconds=self.session_duration)) < datetime.utcnow():
            return None
        return usr_ses[0].user_id

    def destroy_session(self, request=None):
        """
        destroys the session
        """
        if request is None:
            return False
        cook = self.session_cookie(request)
        if not cook:
            return False
        usr_ses = UserSession.search({'session_id': cook})
        if len(usr_ses) == 0:
            return False
        del self.user_id_by_session_id[cook]
        usr_ses[0].remove()
        return True
