|buildstatus|_

Installation
============

.. code-block:: python

    pip install xpect


Example usage
=============

See the test suite: https://github.com/eerimoq/expect/blob/master/tests/test_expect.py

A basic login example using pyserial:

.. code-block:: python

    >>> import serial
    >>> import expect
    >>> serial_linux = serial.Serial("/dev/ttyS0")
    >>> linux = expect.Handler(serial_linux)
    >>> linux.send("")
    >>> linux.expect(r"username: ")
    >>> linux.send("root")
    >>> linux.expect(r"password: ")
    >>> linux.send("root")
    >>> linux.expect(r"/home/root $ ")


.. |buildstatus| image:: https://travis-ci.org/eerimoq/expect.svg
.. _buildstatus: https://travis-ci.org/eerimoq/expect
