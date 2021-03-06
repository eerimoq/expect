"""expect module
"""

import re
import logging
import sys
import threading

__author__ = 'Erik Moqvist'
__version__ = '3.1.1'

LOGGER = logging.getLogger(__name__)


class TimeoutError(Exception):
    """Exception raised when expect times out.

    """

    pass


class BreakConditionError(Exception):
    """Exception raised when a break condition is met.

    """

    pass


class _Timer(object):

    def __init__(self, timeout):
        self.expired = False
        self.timer = threading.Timer(timeout, self.timer_expired)
        self.timer.start()

    def timer_expired(self):
        self.expired = True

    def cancel(self):
        self.timer.cancel()


class Handler(object):
    """Class wrapping an io object.
    """

    def __init__(self,
                 iostream,
                 eol='\n',
                 break_conditions=None,
                 print_input=True,
                 print_output=False,
                 output=None,
                 receive_buffer_max=256):
        """Initialize object with given parameters.

        :param iostream:           Io stream to read data from and write data
                                   data to. This object must implement two
                                   functions, read(count) and write(string).
                                   read() must return a string.
        :param eol:                'end of line' string to send after the
                                   'send string'.
        :param break_conditions:   expect() throws an exception if the returned
                                   value from `iostream`.read() is in this
                                   iterable.
        :param print_input:        Print input on `output` object.
        :param print_output:       Print output on `output` object.
        :param output:             Write input and output data to this object. Default is stdout.
        :param receive_buffer_max: The maximum number of bytes to save in the receive buffer.

        """

        self.iostream = iostream
        self.input_buffer = ''
        self.eol = eol

        if break_conditions is None:
            break_conditions = ['', None]

        self.break_conditions = break_conditions
        self.print_input = print_input
        self.print_output = print_output

        if output is None:
            self.output = sys.stdout

        self.receive_buffer_max = receive_buffer_max

    def expect(self, pattern, timeout=None, print_input=True):
        """Returns when regular expression `pattern` matches the data
        read from the output stream.

        :param pattern:     Regular expression to match.
        :param timeout:     Timeout value in seconds, or None to wait forever.
        :param print_input: Print input on the `output` object.
        :returns:           The matched string.

        """

        # Timeout handling.
        if timeout is not None:
            timer = _Timer(timeout)

        try:
            # Wait for pattern.
            re_expect = re.compile(r'(' + pattern + r')')

            while True:
                mo = re_expect.search(self.input_buffer)

                if mo:
                    LOGGER.debug("Found expected pattern '%s'.", pattern)
                    self.input_buffer = self.input_buffer[mo.end():]

                    return mo.group(1)
                else:
                    char = self.iostream.read(1)

                    if char in self.break_conditions:
                        fmt = "break condition met: '{}' in '{}'."
                        raise BreakConditionError(fmt.format(char, self.break_conditions))

                    if self.print_input and print_input == True:
                        self.output.write(char)

                    self.input_buffer += char

                    # Limit the input buffer size for faster pattern matching.
                    self.input_buffer = self.input_buffer[-self.receive_buffer_max:]

                    # Timeout handling.
                    if timeout is not None:
                        if timer.expired:
                            raise TimeoutError("Timed out waiting for '%s'", pattern)
        finally:
            if timeout is not None:
                timer.cancel()

    def send(self, string, send_eol=True):
        """Write given string to the iostream.

        :param string:   String to send.
        :param send_eol: Send 'end of line' after ``string``.
        :returns:        Return value of iostream.write().

        """

        if send_eol:
            string += self.eol

        if self.print_output:
            self.output.write(string)

        return self.iostream.write(string)

    def sendln(self, string):
        """Write given string and a new line to the iostream.

        :param string:   String to send.
        :returns:        Return value of iostream.write().

        """

        return self.send(string, send_eol=True)
