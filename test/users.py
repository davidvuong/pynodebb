#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
import httpretty

from pynodebb import Client


class TestPyNodeBBUsers(unittest.TestCase):
    def setUp(self):
        self.client = Client('http://localhost:4567', 'master_token123')

    @httpretty.activate
    def test_create_user(self):
        create_endpoint = 'http://localhost:4567/api/v1/users'
        httpretty.register_uri(
            httpretty.POST, create_endpoint,
            body='{"code":"ok","payload":{"uid": 5, "username":"bob-the-builder"}}',
            status=200,
            content_type='application/json'
        )

        code, response = self.client.users.create('Bob the builder')
        self.assertEquals(code, 200)
        self.assertEquals(response, {'uid': 5, 'username': 'bob-the-builder'})

    @httpretty.activate
    def test_fail_create_user(self):
        create_endpoint = 'http://localhost:4567/api/v1/users'
        httpretty.register_uri(
            httpretty.POST, create_endpoint,
            body='{"code":"bad-request","message":"..."',
            status=400,
            content_type='application/json'
        )

        code, response = self.client.users.create('')  # Empty username.
        self.assertEquals(code, 400)
        self.assertEquals(response, 'Bad Request')

    @httpretty.activate
    def test_update_user(self):
        updated_endpoint = 'http://localhost:4567/api/v1/users/10'
        httpretty.register_uri(
            httpretty.PUT, updated_endpoint,
            body='{"code": "ok", "payload": {}}',
            status=200,
            content_type='application/json'
        )

        status_code = self.client.users.update(10, **{'fullname': 'David Vuong'})
        self.assertEquals(status_code, 200)

    @httpretty.activate
    def test_update_user_settings(self):
        updated_endpoint = 'http://localhost:4567/api/v1/users/10/settings'
        httpretty.register_uri(
            httpretty.PUT, updated_endpoint,
            body='{"code": "ok", "payload": {}}',
            status=200,
            content_type='application/json'
        )

        status_code = self.client.users.update_settings(10, **{'followTopicsOnReply': 1})
        self.assertEquals(status_code, 200)

    @httpretty.activate
    def test_delete_user(self):
        delete_endpoint = 'http://localhost:4567/api/v1/users/10'
        httpretty.register_uri(
            httpretty.DELETE, delete_endpoint,
            body='{"code": "ok", "payload": {}}',
            status=200,
            content_type='application/json'
        )

        status_code = self.client.users.delete(10)
        self.assertEquals(status_code, 200)
