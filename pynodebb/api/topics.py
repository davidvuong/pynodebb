#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pynodebb/api/topics.py

Copyright (c) 2015 David Vuong <david.vuong256@gmail.com>
Licensed MIT
"""
from __future__ import unicode_literals

from pynodebb.api import Resource
from pynodebb.api.categories import _get_category_slug
from pynodebb.iterables import TopicIterable


class Topic(Resource):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    ALL_TIME = 'alltime'

    POPULAR_TIME_INTERVALS = (
        DAILY, WEEKLY, MONTHLY, ALL_TIME,
    )
    DEFAULT_POPULAR_INTERVAL = ALL_TIME

    def create(self, cid, title, content):
        raise NotImplementedError

    def delete(self, tid):
        raise NotImplementedError

    def list(self, cid, slug=None, start_page=None):
        """Retrieves and paginates a list of topics given the category `cid`.

        Note that due to NodeBB's API, in order to retrieve topics for a given
        category, we *need* the category `slug` along with the `cid`.

        If the category `slug` isn't supplied, a separate request is made to
        `/api/category/:cid` to retrieve the slug.

        Note that the success return tuple will contain an iterable.

        >>> from pynodebb import Client
        >>> client = Client('http://localhost:4567', 'master_token')
        >>> status_code, topics = client.topics.list(5)
        >>> for topic in topics:
        ...     print(topic['title'])

        NodeBB provides a way to paginate resources. By default resources are
        paginated by 20 items per page. This can be changed in your NodeBB instance's
        ACP (Admin control panel).

        When `list` has reached the end of the page, it will fetch for the next
        page if one is present.

        Args:
            cid (int, str): The id of the category we want to list topics for
            slug (Optional[str]): The category slug (aka title of the category
                formatted in a URL-safe way). Defaults to None.
            start_page (Optional[int]): The page we want the iterable to start at.
                Defaults to the first page if nothing is provided.

        Returns:
            tuple: Tuple in the form (response_code, TopicIterable)

        """
        if slug is None:
            slug = _get_category_slug(self.client, cid)
        if slug is None:
            return 404, 'Not Found'

        # The slug returned by NodeBB contains the `cid` (:cid/:slug).
        url_path = '/api/category/%s' % slug

        # Start at `page` if one was provided.
        if start_page is not None:
            url_path += '?page=%s' % start_page

        status_code, topics = self.client.get(url_path)
        if status_code == 200:
            topics = TopicIterable(self.client, topics)
        return status_code, topics

    def post(self, tid, content):
        raise NotImplementedError

    def tag(self, tid, tags):
        raise NotImplementedError

    def untag(self, tid):
        raise NotImplementedError

    def _extract_topics(self, response):
        status_code, response_body = response
        if status_code != 200:
            return status_code, response_body
        return status_code, response_body.get('topics', [])

    def get_recent(self):
        """Fetches the first set of recent topics.

        Note that recent topics are sorted in descending order. The most recent
        topics will be at the beginning of the list.

        When there aren't any recent topics, an empty array list is returned
        in place of the `json_response`.

        Returns:
            tuple: Tuple in the form (response_code, json_response)

        """
        return self._extract_topics(self.client.get('/api/recent'))

    def get_popular(self, interval=DEFAULT_POPULAR_INTERVAL):
        """Fetches popular topics given the popularity time `interval`.

        Args:
            interval (Optional[str]): The popularity time interval. When no interval
                is provided, defaults to `self.DEFAULT_POPULAR_INTERVAL`. To find
                what other time intervals are available, see `self.POPULAR_TIME_INTERVALS`.

        Raises:
            ValueError: When the `interval` isn't a valid popular topic time interval.

        Returns:
            tuple: Tuple in the form (response_code, json_response)

        """
        if interval not in self.POPULAR_TIME_INTERVALS:
            raise ValueError('Invalid topic type: %s' % interval)
        return self._extract_topics(self.client.get('/api/popular/' + interval))
