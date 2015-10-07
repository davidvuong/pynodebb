#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import unittest
import httpretty

from pynodebb import Client


class TestPyNodeBBCategories(unittest.TestCase):
    def setUp(self):
        self.client = Client('http://localhost:4567', 'master_token123')

    @httpretty.activate
    def test_list_categories(self):
        get_recent_endpoint = 'http://localhost:4567/api/categories'
        response_body = {
            'categories': [{
                'title': 'Example title',
            }],
        }

        httpretty.register_uri(
            httpretty.GET, get_recent_endpoint,
            body=json.dumps(response_body),
            status=200, content_type='application/json'
        )

        code, response = self.client.categories.list()
        self.assertEquals(code, 200)
        self.assertEquals(response, response_body['categories'])

    @httpretty.activate
    def test_list_categories_bad_request(self):
        get_recent_endpoint = 'http://localhost:4567/api/categories'
        httpretty.register_uri(
            httpretty.GET, get_recent_endpoint,
            body='{"code":"bad-request","message":"..."}',
            status=400, content_type='application/json'
        )

        code, response = self.client.categories.list()
        self.assertEquals(code, 400)
        self.assertEquals(response, 'Bad Request')
