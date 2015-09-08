"""expect module
"""

import re
import logging
import sys
import time

LOGGER = logging.getLogger(__name__)


class ExpectTimeoutError(Exception):
    """Exception raised when expect times out.
    """
    pass


class Handler(object):
    """Class wrapping an io object.
    """

    def __init__(self,
                 iostream,
                 eol='\n',
                 break_conditions=None,
                 print_input=True,
                 print_output=False,
                 output=sys.stdout,
                 split_pattern=r'\n'):
        """Initialize object with given parameters.

        :param iostream:         Io stream to read data from and write data
                                 data to. The class of this object must
                                 implement two functions, read(count) and
                                 write(string). read() must return a string.
        :param eol:              'end of line' string to send after the
                                 'send string'.
        :param break_conditions: expect() throws an exception if the returned
                                 value from `iostream`.read() is in this
                                 iterable.
        :param print_input:      Print input on `output` object.
        :param print_output:     Print output on `output` object.
        :param output:           Write input and output data to this object.
        :param split_pattern:    Split read data using this regexp before sreaching
                                 for a match.
        """

        self.iostream = iostream
        self.input_buffer = ''
        self.eol = eol
        if break_conditions is None:
            break_conditions = ['', None]
        self.break_conditions = break_conditions
        self.print_input = print_input
        self.print_output = print_output
        self.output = output
        if split_pattern:
            self.re_split = re.compile(split_pattern)
        else:
            self.re_split = None

    def expect(self, pattern, timeout=None, print_input=True):
        """Returns when regular expression `pattern` matches the data
        read from the output stream.

        :param pattern: Regular expression to match.
        :returns:       The matched string.
        """

        start_time = time.time()

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
                    raise RuntimeError(fmt.format(char, self.break_conditions))
                if self.print_input and print_input == True:
                    self.output.write(char)
                self.input_buffer += char
                if self.re_split:
                    self.input_buffer = self.re_split.split(self.input_buffer)[-1]

                # timeout handling
                if timeout:
                    if (time.time() - start_time) > timeout:
                        raise ExpectTimeoutError("Timed out waiting for '%s'", pattern)

    def send(self, string, send_eol=True):
        """Writes a string to the iostream.

        :param string:   String to send.
        :param send_eol: Send 'end of line' after ``string``.
        :returns:        Return value of iostream.write().
        """

        if send_eol:
            string += self.eol
        if self.print_output:
            self.output.write(string)
        return self.iostream.write(string)
