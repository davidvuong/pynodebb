#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import unittest
import httpretty

from pynodebb import Client
from pynodebb.exceptions import InvalidPage
from pynodebb.iterables import ResourceIterable
from pynodebb.iterables import TopicIterable


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


class TestPyNodeBBResourceIterable(unittest.TestCase):
    def test_next_when_one_page(self):
        resources = GenericResourceIterable(None, {
            'resources': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        })
        self.assertEquals(len([r for r in resources]), 10)

    @httpretty.activate
    def test_next_when_multi_page(self):
        client = Client('http://localhost:4567', 'master_token123')
        resources = GenericResourceIterable(client.http_client, {
            'resources': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'pagination': {
                'next': {
                    'active': True,
                    'qs': 'page=2',
                },
            },
            'slug': '1/resource-slug',
        })

        # 2nd page of resource items (NodeBB pagination).
        endpoint = 'http://localhost:4567/api/resource/1/resource-slug?page=2'
        response_body = {
            'resources': [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
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
        resources = GenericResourceIterable(client.http_client, {
            'resources': [1, 2, 3, 4, 5],
            'pagination': {
                'next': {
                    'active': True,
                    'qs': 'page=2',
                },
            },
            'slug': '1/resource-slug',
        })

        # 2nd page of resource items (NodeBB pagination) - timeout.
        endpoint = 'http://localhost:4567/api/resource/1/resource-slug?page=2'
        httpretty.register_uri(
            httpretty.GET, endpoint,
            body='{"code":"bad-request","message":"..."}',
            status=408, content_type='application/json'
        )
        self.assertEquals(len([r for r in resources]), 5)

    def test_when_when_one_page_no_items(self):
        resources = GenericResourceIterable(None, {
            'resources': [],
        })
        self.assertEquals(len([r for r in resources]), 0)

    def test_get_resource_length(self):
        resources = GenericResourceIterable(None, {
            'resources': [1, 2, 3, 4, 5],
            'resource_count': 5,
        })
        self.assertEquals(len(resources), 5)

    def test_get_resource_repr(self):
        resources = GenericResourceIterable(None, {
            'resource_count': 21,
            'currentPage': 1,
        })
        Client.configure(page_size=20)
        self.assertEquals(str(resources), '<Page 1 of 2>')

        resources_2 = GenericResourceIterable(None, {})
        self.assertEquals(str(resources_2), '<Page 0 of 0>')

    @httpretty.activate
    def test_get_page(self):
        client = Client('http://localhost:4567', 'master_token123')
        resources = GenericResourceIterable(client.http_client, {
            'resource_count': 21,
            'currentPage': 1,
            'slug': '1/resource-slug',
        })

        page_number = 2
        endpoint = 'http://localhost:4567/api/resource/1/resource-slug?page=%d' % page_number
        response_body = {
            'resource_count': 21,
            'currentPage': 2,
            'slug': '1/resource-slug',
        }

        httpretty.register_uri(
            httpretty.GET, endpoint,
            body=json.dumps(response_body),
            status=200, content_type='application/json'
        )

        resources_2 = resources.page(2)
        self.assertEquals(resources.current_page, 1)
        self.assertEquals(resources_2.current_page, 2)

    def test_num_pages(self):
        resources = GenericResourceIterable(None, {
            'resource_count': 21,
        })
        Client.configure(page_size=20)
        self.assertEquals(resources.num_pages, 2)

        Client.configure(page_size=10)
        self.assertEquals(resources.num_pages, 3)

        Client.configure(page_size=30)
        self.assertEquals(resources.num_pages, 1)

    def test_get_current_page(self):
        resources = GenericResourceIterable(None, {
            'resource_count': 21,
            'currentPage': 1,
        })
        self.assertEquals(resources.page(1).current_page, 1)

    def test_get_resources(self):
        resources = [1, 2, 3]
        iterable = GenericResourceIterable(None, {
            'resources': resources,
            'resource_count': 21,
            'currentPage': 1,
        })
        self.assertEquals(iterable.resources, resources)

    @httpretty.activate
    def test_get_page_err(self):
        client = Client('http://localhost:4567', 'master_token123')
        resources = GenericResourceIterable(client.http_client, {
            'resource_count': 21,
            'currentPage': 1,
            'slug': '1/resource-slug',
        })

        page_number = 2
        endpoint = 'http://localhost:4567/api/resource/1/resource-slug?page=%d' % page_number
        httpretty.register_uri(
            httpretty.GET, endpoint,
            body='{"code":"bad-request","message":"..."}',
            status=408, content_type='application/json'
        )
        self.assertRaises(InvalidPage, resources.page, page_number)

    def test_get_non_exist_page(self):
        resources = GenericResourceIterable(None, {
            'resource_count': 21,
            'currentPage': 1,
            'slug': '1/resource-slug',
        })

        page_number = 999999
        self.assertRaises(InvalidPage, resources.page, page_number)

    def test_get_negative_page(self):
        resources = GenericResourceIterable(None, {
            'resource_count': 21,
            'currentPage': 1,
        })
        self.assertRaises(InvalidPage, resources.page, -1)


class TestTopicIterable(unittest.TestCase):
    def test_url_path_property(self):
        resources = TopicIterable(None, {
            'slug': '1/topic-slug-example'
        })
        self.assertEquals(resources.url_path, '/api/category/1/topic-slug-example')

    def test_resource_id_property(self):
        resources = TopicIterable(None, {})
        self.assertEquals(resources.resource_id, 'topics')

    def test_resource_count_id_property(self):
        resources = TopicIterable(None, {})
        self.assertEquals(resources.resource_count_id, 'topic_count')
