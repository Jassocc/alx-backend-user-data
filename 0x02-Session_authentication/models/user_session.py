#!/usr/bin/env python3
"""
handles ses
"""
from models.base import Base


class UserSession(Base):
    """
    class with base props
    """

    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
