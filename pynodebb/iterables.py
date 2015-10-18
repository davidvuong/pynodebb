#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pynodebb/iterables.py

Copyright (c) 2015 David Vuong <david.vuong256@gmail.com>
Licensed MIT
"""
from __future__ import unicode_literals
from __future__ import division

from copy import deepcopy
from math import ceil
from pynodebb.settings import settings
from pynodebb.exceptions import InvalidPage


class ResourceIterable(object):
    def __init__(self, client, resource_list):
        self.client = client
        self.resource_list = resource_list

    def __iter__(self):
        return self

    def __len__(self):
        return self.resource_list.get(self.resource_count_id, 0)

    def __str__(self):
        if not len(self):
            return '<Page 0 of 0>'

        max_pages = ceil(len(self) / settings['page_size'])
        return '<Page %d of %d>' % (self.current_page, max_pages)

    @property
    def url_path(self):
        raise NotImplementedError

    @property
    def resource_id(self):
        raise NotImplementedError

    @property
    def resource_count_id(self):
        raise NotImplementedError

    @property
    def current_page(self):
        return self.resource_list['current_page']

    def _fetch_page(self, url):
        status_code, response = self.client.get(url)
        if status_code == 200:
            self.resource_list = response
        return status_code, response

    def next(self):
        """Retrieves the `next` resource in the provided `resource_list`.

        `ResourceIterable` and all subclasses has support for pagination. That is,
        when `next` reaches the end of the resource list, a synchronous request
        is made to your NodeBB instance, asking for the next page.

        When there are no more remaining pages, the iterator stops and raises
        a `StopIteration` exception. Otherwise, the next page is fetched.

        """
        resource_id = self.resource_id
        resources = self.resource_list.get(resource_id)

        # No more items left in the current page, try fetching more.
        if not resources:
            pagination = self.resource_list.get('pagination')

            # No pagination or we're at the end of the list.
            if pagination is None:
                raise StopIteration
            if not pagination['next']['active']:
                raise StopIteration

            # Build the next page url to make a request against.
            next_qs = pagination['next']['qs']
            url_path = self.url_path + '?' + next_qs

            status_code, response = self._fetch_page(url_path)
            if status_code != 200:
                raise StopIteration
            resources = self.resource_list.get(resource_id, [])

        # Double check for emptiness (in case we get 0 items in the next page).
        if not resources:
            raise StopIteration
        return resources.pop(0)

    def page(self, page_number):
        """
        Given a `page_number`, retrieve and create a new iterable, setting the
        start position to be `page_number`.

        Note that if the `page_number` is equal to the current page then nothing
        will be fetched. Also note that a copy (not a reference) of the iterable
        will be returned.

        Args:
            page_number (int): The page number we want to begin at

        Raises:
            InvalidPage: Raised when the specified `page_number` is invalid

        Returns:
            ResourceIterable: An instance (deepcopy) of ResourceIterable
                containing the associated `resource_list`.

        """
        if str(self.current_page) == str(page_number):
            return deepcopy(self)

        url_path = self.url_path + '?page=%s' % page_number
        status_code, response = self._fetch_page(url_path)
        if status_code != 200:
            raise InvalidPage()
        return deepcopy(self)


class TopicIterable(ResourceIterable):
    @property
    def url_path(self):
        return '/api/category/%s' % self.resource_list['slug']

    @property
    def resource_id(self):
        return 'topics'

    @property
    def resource_count_id(self):
        return 'topic_count'
