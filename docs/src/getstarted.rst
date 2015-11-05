Getting started with PyNodeBB
=============================

.. note::

    Before you continue, please read the install guide `here <install.html>`_.

To re-cap, make sure that you've:

1. Installed NodeBB and all dependencies (including Redis or MongoDB)
2. Installed and enabled the ``nodebb-plugin-write-api``
3. Created a write-api master token

The next step is to start using the PyNodeBB client.

.. code:: python

    from __future__ import print_function
    from pynodebb import Client

    client = Client('http://localhost:4567', 'master_token')
    client.configure(**{
      'page_size': 20
    })

    # Retrieves a NodeBB user given their `uid`.
    status_code, user = client.users.get(uid)
    print(user['username'])

    # Updates the retrieved user's `fullname`.
    client.users.update(user['uid'], **{'fullname': 'David Vuong'})

    # Iterate over all topics in category given the `cid`.
    status_code, topics = client.topics.list(1):
    for topic in topics:
        print(topic['title'])

For more information please checkout the `API Reference <pynodebb.html>`_.
