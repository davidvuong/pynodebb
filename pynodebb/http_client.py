#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pynodebb/http_client.py

Copyright (c) 2015 David Vuong <david.vuong256@gmail.com>
Licensed MIT
"""
import requests


class HttpClient(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint

