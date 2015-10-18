#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest
import httpretty

from pynodebb import Client
from pynodebb.settings import settings


class TestPyNodeBBHttpClient(unittest.TestCase):
    def test_should_set_default_admin_uid(self):
        client = Client('http://localhost:4567', 'master_tokenxxx')
        self.assertEquals(client.http_client.admin_uid, settings['admin_uid'])

    def test_should_set_bearer_headers(self):
        client = Client('http://localhost:4567', 'master_tokenxxx')
        self.assertEquals(client.http_client.headers, {
            'Authorization': 'Bearer %s' % 'master_tokenxxx'
        })

    @httpretty.activate
    def test_get_user_with_username(self):
        client = Client('http://localhost:4567', 'master_tokenxxx')

        invalid_json = '{...}'
        httpretty.register_uri(
            httpretty.GET, 'http://localhost:4567/test-empty',
            body=invalid_json, status=200,
            content_type='application/json'
        )

        status_code, response = client.http_client.get('/test-empty')
        self.assertEquals(status_code, 200)
        self.assertDictEqual(response, {})
