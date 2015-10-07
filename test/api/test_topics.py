#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import unittest
import httpretty

from pynodebb import Client


class TestPyNodeBBTopics(unittest.TestCase):
    def setUp(self):
        self.client = Client('http://localhost:4567', 'master_token123')

    @httpretty.activate
    def test_get_recent(self):
        get_recent_endpoint = 'http://localhost:4567/api/recent'
        response_body = {
            'topics': [{
                'title': 'Example title',
                'deleted': False,
                'pinned': True,
                'locked': True,
                'viewcount': '100',
                'postcount': '10',
            }],
        }

        httpretty.register_uri(
            httpretty.GET, get_recent_endpoint,
            body=json.dumps(response_body),
            status=200, content_type='application/json'
        )

        code, response = self.client.topics.get_recent()
        self.assertEquals(code, 200)
        self.assertEquals(response, response_body['topics'])

    @httpretty.activate
    def test_get_recent_empty(self):
        get_recent_endpoint = 'http://localhost:4567/api/recent'
        response_body = {'topics': []}

        httpretty.register_uri(
            httpretty.GET, get_recent_endpoint,
            body=json.dumps(response_body),
            status=200, content_type='application/json'
        )

        code, response = self.client.topics.get_recent()
        self.assertEquals(code, 200)
        self.assertEquals(response, response_body['topics'])

    @httpretty.activate
    def test_get_recent_bad_request(self):
        get_recent_endpoint = 'http://localhost:4567/api/recent'
        httpretty.register_uri(
            httpretty.GET, get_recent_endpoint,
            body='{"code":"bad-request","message":"..."}',
            status=400, content_type='application/json'
        )

        code, response = self.client.topics.get_recent()
        self.assertEquals(code, 400)
        self.assertEquals(response, 'Bad Request')

    @httpretty.activate
    def test_get_popular(self):
        get_popular_endpoint = 'http://localhost:4567/api/popular/alltime'
        response_body = {
            'topics': [{
                'title': 'Example title',
                'deleted': False,
                'pinned': True,
                'locked': True,
                'viewcount': '100',
                'postcount': '10',
            }],
        }

        httpretty.register_uri(
            httpretty.GET, get_popular_endpoint,
            body=json.dumps(response_body),
            status=200, content_type='application/json'
        )

        code, response = self.client.topics.get_popular()
        self.assertEquals(code, 200)
        self.assertEquals(response, response_body['topics'])

    @httpretty.activate
    def test_get_popular_empty(self):
        get_popular_endpoint = 'http://localhost:4567/api/popular/daily'
        httpretty.register_uri(
            httpretty.GET, get_popular_endpoint,
            body=json.dumps({}),
            status=200, content_type='application/json'
        )

        code, response = self.client.topics.get_popular('daily')
        self.assertEquals(code, 200)
        self.assertEquals(response, [])

    def test_get_popular_invalid_interval(self):
        self.assertRaises(ValueError, self.client.topics.get_popular, 'bad-interval')
