# Welcome to pyNodeBB

[![Build Status](https://travis-ci.org/davidvuong/pynodebb.svg?branch=master)](https://travis-ci.org/davidvuong/pynodebb)
[![Coverage Status](https://coveralls.io/repos/davidvuong/pynodebb/badge.svg?branch=master&service=github)](https://coveralls.io/github/davidvuong/pynodebb?branch=master)
[![Code Climate](https://codeclimate.com/github/davidvuong/pynodebb/badges/gpa.svg)](https://codeclimate.com/github/davidvuong/pynodebb)

pyNodeBB is a Python client for the NodeBB API (still under development).

## Install and setup

1. Install NodeBB. Currently this wrapper only supports 0.7.3 so you'll need to clone from the `0.7.x` branch. Follow the install guide [here](https://docs.nodebb.org/en/latest/installing/os.html).
1. Install the `nodebb-plugin-write-api`. Unfortunately NodeBB only has a read-api and a write-api needs to be installed separately:

  ```
  cd /path/to/nodebb/node_modules/
  git clone git@github.com:davidvuong/nodebb-plugin-write-api.git
  ```

  The plugin exposes NodeBB functionality via a REST API. You can read more about it [here](https://github.com/davidvuong/nodebb-plugin-write-api/blob/master/routes/v1/README.md).

1. After you've correctly installed and activated the `nodebb-plugin-write-api` plugin, create a master token under `/admin/plugins/write-api/`.
1. Turn off the "make user info private" option in your ACP (this is required for `GET /users/uid/:id` requests to work).
1. The last step is to install `pynodebb` from the CheeseShop:

  ```bash
  pip install pynodebb
  ```

## Example usage

```python
from __future__ import print_function
from pynodebb import Client

client = Client('http://localhost:4567', 'master_token')
status_code, user = client.users.get(uid)

print(user['username'])

client.users.update(user['uid'], **{'fullname': 'David Vuong'})
```

You can find out more information about the write-api endpoints [here](https://github.com/davidvuong/nodebb-plugin-write-api/blob/master/routes/v1/README.md).

## Contribution

Please read the [contribution guide](https://github.com/davidvuong/pynodebb/blob/master/CONTRIBUTING.md) before contributing.

1. Clone and install dependencies:

  ```bash
  git clone git@github.com:davidvuong/pynodebb.git

  mkvirtualenv pynodebb
  cd pynodebb

  python setup.py develop
  pip install -r requirements.txt
  ```

## License

[MIT](https://github.com/davidvuong/pynodebb/blob/master/LICENSE.md)
