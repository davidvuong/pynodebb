#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import mock
import unittest
import httpretty

from pynodebb.api import Resource
from pynodebb.api.mixins import ResourceListMixin
from pynodebb.iterables import ResourceIterable
from pynodebb import Client


class GenericResourceIterable(ResourceIterable):
    @property
    def url_path(self):
        return '/api/resource/%s' % self.resource_list['slug']

    @property
    def resource_id(self):
        return 'resources'

    @property
    def resource_count_id(self):
        return 'resource_count'


class GenericResource(Resource, ResourceListMixin):
    parent_resource = 'resource'
    parent_resource_path = 'resource/id'
    resource_iterable = GenericResourceIterable


class TestPyNodeBBListMixin(unittest.TestCase):
    def setUp(self):
        self.client = Client('http://localhost:4567', 'master_token123')
        self.resources = GenericResource(self.client.http_client)

    @httpretty.activate
    def test_should_list_resources(self):
        response_body_1 = {
            'id': '1',
            'slug': '1/resource-slug',
        }
        response_body_2 = {
            'id': '1',
            'slug': '1/resource-slug',
            'pagination': {
                'next': {
                    'page': 1,
                    'active': False,
                }
            },
            'currentPage': 1,
            'resource_count': 30,
        }

        httpretty.register_uri(
            httpretty.GET,
            'http://localhost:4567/api/resource/id/1',
            body=json.dumps(response_body_1),
            status=200, content_type='application/json'
        )
        httpretty.register_uri(
            httpretty.GET,
            'http://localhost:4567/api/resource/1/resource-slug',
            body=json.dumps(response_body_2),
            status=200, content_type='application/json'
        )

        Client.configure(page_size=20)
        status_code, resources = self.resources.list(1)
        self.assertEquals(status_code, 200)
        self.assertEquals(resources.current_page, 1)
        self.assertEquals(resources.num_pages, 2)

    @httpretty.activate
    def test_should_not_fetch_slug(self):
        http_client = mock.MagicMock()
        http_client.get.return_value = (200, {})

        resources = GenericResource(http_client)
        resources.list(1, slug='1/resource-slug')
        self.assertEquals(http_client.get.call_count, 1)

    @httpretty.activate
    def test_should_start_at_given_page(self):
        http_client = mock.MagicMock()
        http_client.get.return_value = (200, {})

        resources = GenericResource(http_client)
        resources.list(1, slug='1/resource-slug', start_page=3)
        http_client.get.assert_called_with('/api/resource/1/resource-slug?page=3')

    @httpretty.activate
    def test_should_fail_given_invalid_id(self):
        resource_id = 123456789
        httpretty.register_uri(
            httpretty.GET,
            'http://localhost:4567/api/resource/id/%d' % resource_id,
            body='{"code":"bad-request","message":"..."}',
            status=404, content_type='application/json'
        )

        status_code, err_msg = self.resources.list(resource_id)
        self.assertEquals(status_code, 404)
        self.assertEquals(err_msg, 'Not Found')
