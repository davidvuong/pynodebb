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
