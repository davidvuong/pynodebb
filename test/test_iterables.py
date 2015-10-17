#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import unittest
import httpretty
import mock

from pynodebb import Client
from pynodebb.iterables import ResourceIterable


class TestPyNodeBBResourceIterable(unittest.TestCase):
    def test_next_when_one_page(self):
        resources = ResourceIterable(None, {
            'resource': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        })
        resources.get_resource_id = mock.MagicMock(return_value='resource')
        self.assertEquals(len([r for r in resources]), 10)

    @httpretty.activate
    def test_next_when_multi_page(self):
        client = Client('http://localhost:4567', 'master_token123')
        resources = ResourceIterable(client.http_client, {
            'resource': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'pagination': {
                'next': {
                    'active': True,
                    'qs': 'page=2',
                },
            },
        })
        resources.get_resource_id = mock.MagicMock(return_value='resource')
        resources.get_url_path = mock.MagicMock(
            return_value='/api/resource/1/resource-slug'
        )

        # 2nd page of resource items (NodeBB pagination).
        endpoint = 'http://localhost:4567/api/resource/1/resource-slug?page=2'
        response_body = {
            'resource': [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            'pagination': {
                'next': {'active': False},
            },
        }

        httpretty.register_uri(
            httpretty.GET, endpoint,
            body=json.dumps(response_body),
            status=200, content_type='application/json'
        )
        self.assertEquals(len([r for r in resources]), 20)

    @httpretty.activate
    def test_next_http_error(self):
        client = Client('http://localhost:4567', 'master_token123')
        resources = ResourceIterable(client.http_client, {
            'resource': [1, 2, 3, 4, 5],
            'pagination': {
                'next': {
                    'active': True,
                    'qs': 'page=2',
                },
            },
        })
        resources.get_resource_id = mock.MagicMock(return_value='resource')
        resources.get_url_path = mock.MagicMock(
            return_value='/api/resource/1/resource-slug'
        )

        # 2nd page of resource items (NodeBB pagination) - timeout.
        endpoint = 'http://localhost:4567/api/resource/1/resource-slug?page=2'
        httpretty.register_uri(
            httpretty.GET, endpoint,
            body='{"code":"bad-request","message":"..."}',
            status=408, content_type='application/json'
        )
        self.assertEquals(len([r for r in resources]), 5)

    def test_when_when_one_page_no_items(self):
        resources = ResourceIterable(None, {
            'resource': [],
        })
        resources.get_resource_id = mock.MagicMock(return_value='resource')
        self.assertEquals(len([r for r in resources]), 0)
