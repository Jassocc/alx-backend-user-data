#!/usr/bin/env python3
"""
script for task 9
"""
from datetime import datetime, timedelta
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    inherits from base auth
    """

    def __init__(self):
        """
        initializes attributes
        """
        drat = os.getenv('SESSION_DURATION')
        if drat is not None and drat.isnumeric():
            self.session_duration = int(drat)
        else:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        creates a session
        """
        ses_id = super().create_session(user_id)
        if ses_id is None:
            return None
        self.user_id_by_session_id[ses_id] = {
            'user_id': user_id,
            'created_at': datetime.now()}
        return ses_id

    def user_id_for_session_id(self, session_id=None):
        """
        returns id based of session
        """
        if session_id is None:
            return None
        usr_ses = self.user_id_by_session_id.get(session_id)
        if usr_ses is None:
            return None
        if self.session_duration <= 0:
            return usr_ses.get('user_id')
        extime = usr_ses.get('created_at')
        if extime is None:
            return None
        expir_time = usr_ses.get(
                'created_at') + timedelta(seconds=self.session_duration)
        if expir_time < datetime.now():
            return None
        return usr_ses.get('user_id')
