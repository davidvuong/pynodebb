Contributing to PyNodeBB
========================

    *All code in any code-base should look like a single person typed it, no matter how many people contributed.*

The following are a few rules you need to follow when contributing to ``pynodebb``.

* Please follow PEP8... or to the best of your ability... and when it makes sense.

    *All I want to say is, people lighten up. The style guide can't solve all your problems. You are never going to have all code compliant. Use the style guide when it helps, ignore it when it's in the way.* -- Guido van Rossum

* When documenting your code, please follow the Google Style Docstrings. Here's an `example <http://sphinxcontrib-napoleon.readthedocs.org/en/latest/example_google.html>`_.

1. Fork the PyNodeBB `repository <https://github.com/davidvuong/pynodebb>`_ on GitHub.

2. Clone your PyNodeBB fork:

.. code::

    git clone git@github.com:your-github-name/pynodebb.git
    cd pynodebb

3. Setup your development environment:

.. code::

    mkvirtualenv pynodebb

    pip install setuptools --upgrade
    pip install -r requirements.txt

4. Make your awesome changes.

5. Submit a pull request on `GitHub <https://github.com/davidvuong/pynodebb/pulls>`_.
