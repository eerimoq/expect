import re
import logging
import sys

logger = logging.getLogger(__name__)

class Handler(object):
    '''
    '''
    
    def __init__(self,
                 iostream,
                 eol='\n',
                 break_conditions=['', None],
                 print_input=True,
                 print_output=False):
        '''
        Initialize object with given parameters.

        :param iostream:         Io stream to read data from and write data
                                 data to. The class of this object must
                                 implement two functions, read(count) and
                                 write(string). read() must return a string.
        :param eol:              'end of line' string to send after the
                                 'send string'.
        :param break_conditions: expect() throws an exception if the returned
                                 value from `iostream`.read() is in this
                                 iterable.
        :param print_input:      Print input on stdout.
        :param print_output:     Print output on stdout.
        '''

        self.iostream = iostream
        self.input_buffer = ''
        self.eol = eol
        self.break_conditions = break_conditions
        self.print_input = print_input
        self.print_output = print_output

    def expect(self, pattern):
        '''
        Returns when regular expression `pattern` matches the data
        read from the output stream.

        :param pattern: Regular expression to match.
        :returns:       The matched string.
        '''

        re_expect = re.compile('(' + pattern + ')')

        while True:
            mo = re_expect.search(self.input_buffer)

            if mo:
                logger.info("Found expected pattern '{}'.", pattern)
                self.input_buffer = self.input_buffer[mo.end():]
                return mo.group(1)
            else:
                char = self.iostream.read(1)
                if char in self.break_conditions:
                    fmt = "break condition met: '{}' in '{}'."
                    raise RuntimeError(fmt.format(char, self.break_conditions))
                if self.print_input:
                    sys.stdout.write(char)
                self.input_buffer += char

    def send(self, string, send_eol=True):
        '''
        Writes a string to the iostream.

        :param string:   String to send.
        :param send_eol: Send 'end of line' after ``string``.
        :returns:        Return value of iostream.write().
        '''

        if send_eol:
            string += self.eol
        if self.print_output:
            sys.stdout.write(string)
        return self.iostream.write(string)
