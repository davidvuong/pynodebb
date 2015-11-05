Installing PyNodeBB
===================

1. Download and install NodeBB. Follow NodeBB's OS specific install guide `here <https://docs.nodebb.org/en/latest/installing/os.html>`_, making sure to replace ``v0.x.x`` with ``v0.7.x``.

.. note::

    PyNodeBB has only been tested on NodeBB v0.7.x. Please download from the ``v0.7.x`` branch.

2. Install the ``nodebb-plugin-write-api`` plugin. Unfortunately NodeBB's API is read-only and does not natively support write requests hence a write-api plugin needs to be installed separately.

.. code::

    cd /path/to/nodebb/node_modules/
    git clone git@github.com:davidvuong/nodebb-plugin-write-api.git

Here we are installing my personal fork of the ``nodebb-plugin-write-api`` plugin.

The write-api plugin from NodeBB lacks necessary functionality e.g. allowing clients to update user settings. It also no longer supports NodeBB v0.7.x. For more information, checkout the README on `nodebb-plugin-write-api <https://github.com/davidvuong/nodebb-plugin-write-api>`_.

3. After you've cloned the repo, visit your NodeBB's ACP (Admin control panel) to enable the plugin and to create a master token. The master token can be created at ``/admin/plugins/write-api/``.

If you're not able to configure the write-api, restart your NodeBB instance and try again. The master token is used to authenticate requests to your NodeBB instance so keep it safe!

4. The final step is to install PyNodeBB itself. You can do that using pip:

.. code::

    pip install pynodebb --upgrade
