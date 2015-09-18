#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pynodebb/http_client.py

Copyright (c) 2015 David Vuong <david.vuong256@gmail.com>
Licensed MIT
"""
from __future__ import unicode_literals

import requests
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class HttpClient(object):
    DEFAULT_ADMIN_UID = 1

    def __init__(self, endpoint, token, admin_uid=DEFAULT_ADMIN_UID):
        self.endpoint = endpoint
        self.admin_uid = admin_uid or self.DEFAULT_ADMIN_UID
        self.headers = {'Authorization': 'Bearer %s' % token}

    def _request(self, method, path, **kwargs):
        """Simple wrapper over `requests.request`.

        Formats the request headers, payload and endpoint and returns the
        response status_code and response.json in a tuple.

        Args:
            method (str): The HTTP method we want to make a request with.
            path (str): The "path" section of the URI e.g. `/api/users/5/`.
            **kwargs: The request payload (request body).

        Returns:
            tuple: A tuple in the form (response_code, response_json)

        """
        if '_uid' not in kwargs:
            kwargs.update({'_uid': self.admin_uid})
        response = requests.request(
            method, urlparse.urljoin(self.endpoint, path),
            headers=self.headers, data=kwargs
        )
        return response.status_code, response.json()

    def get(self, path, **kwargs):
        return self._request('GET', path, **kwargs)

    def post(self, path, **kwargs):
        return self._request('POST', path, **kwargs)

    def put(self, path, **kwargs):
        return self._request('PUT', path, **kwargs)

    def delete(self, path, **kwargs):
        return self._request('DELETE', path, **kwargs)
