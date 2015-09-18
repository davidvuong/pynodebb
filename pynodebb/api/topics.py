#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pynodebb/api/topics.py

Copyright (c) 2015 David Vuong <david.vuong256@gmail.com>
Licensed MIT
"""

class Topic(object):
    def __init__(self, client):
        self.client = client

    def create(self, cid, title, content):
        pass

    def post(self, tid, content):
        pass

    def delete(self, tid):
        pass

    def tag(self, tid, tags):
        pass

    def untag(self, tid):
        pass
