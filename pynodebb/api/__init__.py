#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pynodebb/api/__init__.py

Copyright (c) 2015 David Vuong <david.vuong256@gmail.com>
Licensed MIT
"""
from __future__ import unicode_literals


class Resource(object):
    def __init__(self, client):
        self.client = client
