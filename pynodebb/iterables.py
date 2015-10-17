#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pynodebb/iterables.py

Copyright (c) 2015 David Vuong <david.vuong256@gmail.com>
Licensed MIT
"""
from __future__ import unicode_literals


class ResourceIterable(object):
    def __init__(self, client, resource_list):
        self.client = client
        self.resource_list = resource_list

    def __iter__(self):
        return self

    def __len__(self):
        raise NotImplementedError

    def get_url_path(self):
        raise NotImplementedError

    def get_resource_id(self):
        raise NotImplementedError

    def next(self):
        """Retrieves the `next` resource in the provided `resource_list`.

        `ResourceIterable` and all subclasses has support for pagination. That is,
        when `next` reaches the end of the resource list, a synchronous request
        is made to your NodeBB instance, asking for the next page.

        When there are no more remaining pages, the iterator stops and raises
        a `StopIteration` exception. Otherwise, the next page is fetched.

        """
        resource_id = self.get_resource_id()
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
            url_path = self.get_url_path() + '?' + next_qs

            status_code, response = self.client.get(url_path)
            if status_code != 200:
                raise StopIteration

            self.resource_list = response
            resources = self.resource_list.get(resource_id, [])

        # Double check for emptiness (in case we get 0 items in the next page).
        if not resources:
            raise StopIteration
        return resources.pop(0)


class TopicIterable(ResourceIterable):
    def __len__(self):
        return self.resource_list.get('topic_count', 0)

    def get_url_path(self):
        return '/api/category/%s' % self.resource_list['slug']

    def get_resource_id(self):
        return 'topics'
