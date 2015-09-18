#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pynodebb/api/users.py

Copyright (c) 2015 David Vuong <david.vuong256@gmail.com>
Licensed MIT
"""

class User(object):
    def __init__(self, client):
        self.client = client

    def create(self, username, **kwargs):
        """Creates a new NodeBB user.

        Args:
            username (str): a unique string used to identify the new user.
                If the username already exists, NodeBB will automatically
                append random numbers after `username` to ensure uniqueness.
            **kwargs: All other accepted user properties. You can find out
                what they are by referring to `updateProfile`.

        Returns:
            tuple: Tuple in the form (response_code, json_response)

        """
        kwargs.update({'username': username})
        return self.client.post('/api/v1/users', **kwargs)

    def update(self, uid, **kwargs):
        """Updates the user's NodeBB user properties.

        Accepted user properties can be found by referring to `updateProfile`.
        For a quick reference these are the accepted fields:

        username, email, fullname, website, location, birthday, signature

        Args:
            uid (str): The NodeBB uid for the user we are updating.
            **kwargs: A dictionary of user properties we are updating.

        Returns:
            tuple: Tuple in the form (response_code, json_response)

        """
        kwargs.update({'_uid': uid})
        return self.client.put('/api/v1/users/%s' % uid, **kwargs)

    def delete(self, uid):
        """Removes the associated NodeBB user.

        Warning! This operation is irreversible.

        Args:
            uid (str): The NodeBB uid for the user we are deleting

        Returns:
            tuple: Tuple in the form (response_code, json_response)

        """
        return self.client.delete('/api/v1/users/%s' % uid, {'_uid': uid})

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

    def get(self, uid, is_username=False):
        """Retrieves the NodeBB user given the user's `uid`.

        Fetches for the entire NodeBB user object (only user properties) given the
        `uid`. The `uid` can be the user's `uid` or the username. If the `uid` is
        expected to be a username, `is_username` must be set to `True`.

        Args:
            uid (str): The NodeBB user's email or username.
            is_username (Optional[bool]): Whether or not the first argument
                is the user's username or not. Defaults to False.

        Returns:
            tuple: Tuple in the form (response_code, json_response)

        """
        if is_username:
            return self.client.get('/api/user/%s' % uid)
        return self.client.get('/api/user/uid/%s' % uid)
