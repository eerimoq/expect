import re
import logging

logger = logging.getLogger(__name__)

class Handler(object):
    '''
    '''
    
    def __init__(self, iostream, eol='\n'):
        '''
        Initialize object with given parameters.

        :param iostream: Io stream to read data from and write data data to.
        :param eol:      'end of line' string to send after the 'send string'.
        '''

        self.iostream = iostream
        self.in_buffer = ''
        self.eol = eol

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
            self.in_buffer += self.iostream.read(1)

    def send(self, string, send_eol=True):
        '''
        Sends a string on the input stream.

        :param string: string to send
        :param send_eol: send 'end of line' after `string`
        '''

        if send_eol:
            string += self.eol
        logger.info("Sending '%s'.", string)
        self.iostream.write(string)
