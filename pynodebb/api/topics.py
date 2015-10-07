#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pynodebb/api/topics.py

Copyright (c) 2015 David Vuong <david.vuong256@gmail.com>
Licensed MIT
"""
from __future__ import unicode_literals


class Topic(object):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    ALL_TIME = 'alltime'

    POPULAR_TIME_INTERVALS = (
        DAILY, WEEKLY, MONTHLY, ALL_TIME,
    )
    DEFAULT_POPULAR_INTERVAL = ALL_TIME

    def __init__(self, client):
        self.client = client

    def create(self, cid, title, content):
        pass

    def post(self, tid, content):
        pass

    def delete(self, tid):
        pass

    def tag(self, tid, tags):
        pass

    def untag(self, tid):
        pass

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
