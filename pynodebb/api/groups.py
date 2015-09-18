#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pynodebb/api/groups.py

Copyright (c) 2015 David Vuong <david.vuong256@gmail.com>
Licensed MIT
"""

class Group(object):
    def __init__(self, client):
        self.client = client

    def create(self, slug, name, **kwargs):
        pass

    def delete(self, slug, **kwargs):
        pass

    def join(self, slug, uid):
        pass

    def leave(self, slug, uid):
        pass
