#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pynodebb/api/users.py

Copyright (c) 2015 David Vuong <david.vuong256@gmail.com>
Licensed MIT
"""

class User(object):
    def __init__(self, client):
        self.client = client

    def create(self, uid, username, **kwargs):
        pass

    def update(self, uid, **kwargs):
        pass

    def delete(self, uid):
        pass

    def change_password(self, uid, new, current=None):
        pass
