#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pynodebb/api/users.py

Copyright (c) 2015 David Vuong <david.vuong256@gmail.com>
Licensed MIT
"""
from __future__ import unicode_literals


class User(object):
    def __init__(self, client):
        self.client = client

    def create(self, username, **kwargs):
        """Creates a new NodeBB user.

        Args:
            username (str): A unique string used to identify the new user.
                If the username already exists, NodeBB will automatically
                append random numbers after `username` to ensure uniqueness.
            **kwargs: All other accepted user properties. You can find out
                what they are by referring to `updateProfile`.

        Returns:
            tuple: Tuple in the form (response_code, json_response)

        """
        kwargs.update({'username': username})
        status_code, response = self.client.post('/api/v1/users', **kwargs)
        if status_code == 200:
            return status_code, response['payload']
        return status_code, response

    def _update(self, uid, endpoint, **kwargs):
        kwargs.update({'_uid': uid})
        return self.client.put(endpoint, **kwargs)[0]

    def update(self, uid, **kwargs):
        """Updates the user's NodeBB user properties.

        Accepted user properties can be found by referring to `updateProfile`.
        For a quick reference these are the accepted fields:

        username, email, fullname, website, location, birthday, signature

        Args:
            uid (str): The NodeBB uid for the user we are updating.
            **kwargs: A dictionary of user properties we are updating.

        Returns:
            int: The response status code.

        """
        return self._update(uid, '/api/v1/users/%s' % uid, **kwargs)

    def update_settings(self, uid, **kwargs):
        """Updates the user's NodeBB settings.

        All settings can be updated. They can be found here:
        https://github.com/NodeBB/NodeBB/blob/master/src/user/settings.js#L102-L118

        Args:
            uid (str): The NodeBB uid for the user we are updating.
            **kwargs: A dictionary of settings we are updating.

        Returns:
            int: The response status code.

        """
        return self._update(uid, '/api/v1/users/%s/settings' % uid, **kwargs)

    def delete(self, uid):
        """Removes the associated NodeBB user.

        Warning! This operation is irreversible. Note that if `uid` is None
        then, no requests will be made and a 404 will be returned.

        Args:
            uid (str): The NodeBB uid for the user we are deleting

        Returns:
            int: The response status code.

        """
        if not uid:
            return 404
        return self.client.delete('/api/v1/users/%s' % uid, **{'_uid': uid})[0]

    def change_password(self, uid, new, current=None):
        """Changes the user's password from `current` to `new`.

        If a `master_token` was generated then `current=None` is accepted. However
        if not, the `current` password is required.

        Args:
            uid (str): The NodeBB uid for the user we are changing the pw for.
            new (str): The new password we want to change to.
            current (Optional[str]): The current password we're changing from.

        Returns:
            tuple: Tuple in the form (response_code, json_response)

        """
        payload = {'new': new, 'current': current, '_uid': uid}
        return self.client.put('/api/v1/users/%s/password' % uid, **payload)

    def get(self, id_, is_username=False):
        """Retrieves the NodeBB user given the user's `id_`.

        Fetches for the entire NodeBB user object (only user properties) given the
        `id_`. The `id_` can be the user's uid or username. If the `id_` is
        expected to be a username, `is_username` must be set to `True`.

        Args:
            id_ (str): The NodeBB user's email or username.
            is_username (Optional[bool]): Whether or not the first argument
                is the user's username or not. Defaults to False.

        Returns:
            tuple: Tuple in the form (response_code, json_response)

        """
        endpoint = '/api/user/%s' if is_username else '/api/user/uid/%s'

        status_code, payload = self.client.get(endpoint % id_)
        if status_code != 200:
            return status_code, payload
        return status_code, payload['payload']
