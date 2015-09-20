#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
import httpretty

from pynodebb import Client


class TestPyNodeBBUsers(unittest.TestCase):
    def setUp(self):
        self.create_endpoint = 'http://localhost:4567/api/v1/users'
        self.client = Client('http://localhost:4567', 'master_token123')

    @httpretty.activate
    def test_create_user(self):
        httpretty.register_uri(
            httpretty.POST, self.create_endpoint,
            body='{"code": "ok", "payload": {"uid": 5}}',
            status=200,
            content_type='application/json'
        )

        code, response = self.client.users.create('bob the builder')
        self.assertEquals(code, 200)
        self.assertEquals(response, {'uid': 5})

    @httpretty.activate
    def test_fail_create_user(self):
        httpretty.register_uri(
            httpretty.POST, self.create_endpoint,
            body='{"code":"bad-request","message":"..."',
            status=400,
            content_type='application/json'
        )

        code, response = self.client.users.create('')  # Empty username.
        self.assertEquals(code, 400)
        self.assertEquals(response, 'Bad Request')
