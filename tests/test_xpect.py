import logging
import sys
import unittest
sys.path.insert(0, '..')
import xpect

# python 2 & 3 compatibility
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class XpectTest(unittest.TestCase):

    def test_uboot(self):
        '''U-boot communication example.
        '''
        outdata = '''
fatload mmc 0 0x3000000 uImage
fatload mmc 0 0x2A00000 devicetree.dtb
fatload mmc 0 0x2000000 uramdisk.image.gz
bootm 0x3000000 0x2000000 0x2A00000
'''

        indata = '''
Booting in 3 seconds...
Booting in 2 seconds...
u-boot> fatload mmc 0 0x3000000 uImage
u-boot> fatload mmc 0 0x2A00000 devicetree.dtb
u-boot> fatload mmc 0 0x2000000 uramdisk.image.gz
u-boot> bootm 0x3000000 0x2000000 0x2A00000
...
~ $
'''

        prompt = 'u-boot> '

        # setup input and output streams
        in_stream = StringIO(indata)
        out_stream = StringIO()

        # create the handler object and start to communicate with u-boot
        uboot = xpect.Handler(in_stream, out_stream)
        uboot.expect('Booting in \d+ seconds...')
        uboot.send('')
        uboot.expect(prompt)
        uboot.send('fatload mmc 0 0x3000000 uImage')
        uboot.expect(prompt)
        uboot.send('fatload mmc 0 0x2A00000 devicetree.dtb')
        uboot.expect(prompt)
        uboot.send('fatload mmc 0 0x2000000 uramdisk.image.gz')
        uboot.expect(prompt)
        uboot.send('bootm 0x3000000 0x2000000 0x2A00000')
        uboot.expect('~ \$')
        self.assertEqual(in_stream.getvalue(), indata)

    def test_expect_return_value(self):
        '''
        Verify the return value from the expect function.
        '''
        foobar = xpect.Handler(StringIO('barfoo'))
        match = foobar.expect('foo|bar')
        self.assertEqual(match, 'bar')
        match = foobar.expect('foo|bar')
        self.assertEqual(match, 'foo')

    def test_eol(self):
        '''
        End of line testing.
        '''
        out_stream = StringIO()
        handler = xpect.Handler(None, out_stream, eol='\r\n')
        handler.send('')
        self.assertEqual(out_stream.getvalue(), '\r\n')
        handler.send('', send_eol=False)
        self.assertEqual(out_stream.getvalue(), '\r\n')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
