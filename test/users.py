#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import httpretty

from pynodebb import Client


class TestPyNodeBBUsers(unittest.TestCase):
    @httpretty.activate
    def test_create_user(self):
        create_endpoint = 'http://localhost:4567/api/v1/users'

        httpretty.register_uri(
            httpretty.POST, create_endpoint,
            body='{"code": "ok", "payload": {"uid": 5}}',
            status=200,
            content_type='application/json'
        )

        client = Client('http://localhost:4567', 'master_token123')
        code, response = client.users.create('bob the builder')

        self.assertEquals(code, 200)
        self.assertEquals(response, {
            'code': 'ok', 'payload': {'uid': 5}
        })
