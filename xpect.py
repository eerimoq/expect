import re
import logging

logger = logging.getLogger(__name__)

class Handler(object):
    '''
    '''
    
    def __init__(self, in_stream, out_stream=None, eol='\n'):
        '''
        Initialize object with given parameters.

        :param in_stream:  Stream object to read data from.
        :param out_stream: Stream object to write data to. If None, set to `in_stream`.
        :param eol:        'end of line' string to send after the 'send string'.
        '''

        self.in_stream = in_stream
        if not out_stream:
            out_stream = in_stream
        self.out_stream = out_stream
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
            self.in_buffer += self.in_stream.read(1)

    def send(self, string, send_eol=True):
        '''
        Sends a string on the input stream.

        :param string: string to send
        :param send_eol: send 'end of line' after `string`
        '''

        if send_eol:
            string += self.eol
        logger.info("Sending '%s'.", string)
        self.out_stream.write(string)
