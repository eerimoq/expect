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

        :param iostream: Io stream to read data from and write data data to.
        :param eol:      'end of line' string to send after the 'send string'.
        :param break_conditions: expect() throws an exception if the returned
        value from `iostream`.read() is in this iterable.
        :param print_input: Print input on stdout.
        :param print_output: Print output on stdout.
        '''

        self.iostream = iostream
        self.in_buffer = ''
        self.eol = eol
        self.break_conditions = break_conditions
        self.print_input = print_input
        self.print_output = print_output

    def expect(self, pattern):
        '''
        Returns when regular expression `pattern` matches the data
        read from the output stream.

        :param pattern: regular expression to match
        :returns: the matched string
        '''

        while True:
            mo = re.search('(' + pattern + ')', self.in_buffer)
            if mo:
                logger.info("Found expected pattern '%s' in data '%s'.",
                            pattern,
                            self.in_buffer)
                self.in_buffer = self.in_buffer[mo.end():]
                return mo.group(1)
            char = self.iostream.read(1)
            if char in self.break_conditions:
                raise RuntimeError("break condition met: '{}' in '{}'.".format(
                    char,
                    self.break_conditions))
            if self.print_input:
                sys.stdout.write(char)
            self.in_buffer += char

    def send(self, string, send_eol=True):
        '''
        Sends a string on the input stream.

        :param string: string to send
        :param send_eol: send 'end of line' after `string`
        '''

        if send_eol:
            string += self.eol
        if self.print_output:
            sys.stdout.write(string)
        self.iostream.write(string)
