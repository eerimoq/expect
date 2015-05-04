|buildstatus|_

Installation
============

.. code-block:: python

    pip install xpect


Example usage
=============

See the test suite: https://github.com/eerimoq/xpect/blob/master/tests/test_xpect.py

A basic login example using pyserial:

.. code-block:: python

    >>> import pyserial
    >>> import xpect
    >>> serial_linux = pyserial.Serial('/dev/ttyS0')
    >>> linux = xpect.Handler(serial_linux)
    >>> linux.send('')
    >>> linux.expect('username: ')
    >>> linux.send('root')
    >>> linux.expect('password: ')
    >>> linux.send('root')
    >>> linux.expect('/home/root $ ')


.. |buildstatus| image:: https://travis-ci.org/eerimoq/xpect.svg
.. _buildstatus: https://travis-ci.org/eerimoq/xpect
