#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pynodebb/api/posts.py

Copyright (c) 2015 David Vuong <david.vuong256@gmail.com>
Licensed MIT
"""
from __future__ import unicode_literals

from pynodebb.api import Resource
from pynodebb.api.mixins import ResourceListMixin
from pynodebb.iterables import PostIterable


class Post(Resource, ResourceListMixin):
    parent_resource = 'topic'
    parent_resource_path = 'topic/tid'
    resource_iterable = PostIterable
