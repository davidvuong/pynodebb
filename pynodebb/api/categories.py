#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pynodebb/api/categories.py

Copyright (c) 2015 David Vuong <david.vuong256@gmail.com>
Licensed MIT
"""
from __future__ import unicode_literals


class Category(object):
    def __init__(self, client):
        self.client = client

    def create(self, cid, name, **kwargs):
        pass

    def update(self, cid, **kwargs):
        pass

    def list(self):
        """Retrieves a list of categories.

        Returns:
            tuple: Tuple in the form (response_code, json_response)

        """
        return self.client.get('/api/categories')
