#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import math
from PIL import Image
from colorama import init
from colorama import Fore, Style
init()


class colors_encode:

    """Lib colors encode
    - init list: version_code, directory_output, format_output, password_stk, colorfile
                 colordir, _dirname, filename, extension, password, verbose

    - def list: params_print, hex_to_string, rgb_to_hex, password_to_intlist, data_encode
                file_clean, decoder
    """

    def __init__(self):

        self.version_code = 0
        self.directory_output = ''
        self.format_output = ''
        self.password_stk = False
        self.colorfile = ''
        self.colordir = ''
        self._dirname = ''
        self.filename = ''
        self.extension = ''
        self.password = False
        self.verbose = False


    def params_print(self, key):
        '''
        Color cmd
        '''
        values = {
            'INFO': Style.BRIGHT + Fore.CYAN,
            'OK': Style.BRIGHT + Fore.GREEN,
            'WARNING': Style.BRIGHT + Fore.YELLOW,
            'FAIL': Style.BRIGHT + Fore.RED,
            'DEFAULT': Style.BRIGHT + Fore.WHITE,
            'END': Style.RESET_ALL,
        }
        return values.get(key, Style.RESET_ALL)


    def hex_to_rgb(self, hex_data):
        '''
        Convert hex to rgb
        '''
        rgb = []
        for i in (0, 2, 4):
            decimal = int(hex_data[i:i + 2], 16)
            rgb.append(decimal)

        return tuple(rgb)


    def hex_to_string(self, hex_text):
        '''
        Convert hex to string
        '''
        return bytes.fromhex(hex_text).decode('ASCII').replace('\x00', '')


    def rgb_to_hex(self, pxcolor):
        '''
        Convert rgb to hex
        '''
        r_color, g_color, b_color = pxcolor
        return '%02X %02X %02X' % (r_color, g_color, b_color)


    def string_to_hex(self, text):
        '''
        Convert string to hex
        '''
        return text.encode('utf-8').hex()


    def password_to_intlist(self, pswd_input):
        '''
        Convert Password to int list
        '''
        incm, output = (0, [self.version_code])
        for char in pswd_input:
            int_out = ord(char)
            incm += int_out
            output.append(incm)

        return output


    def data_encode(self, pswd_input, hexcolor, pos):
        '''
        Data encoder
        '''
        if not self.password_stk:
            self.password_stk = self.password_to_intlist(pswd_input)

        for ipos in self.password_stk:
            if pos % ipos == 1:
                hexcolor = hexcolor[::-1]

        return hexcolor


    def file_clean(self, filename_c):
        '''
        File cleaner
        '''
        if os.path.isfile(filename_c):
            try:
                os.remove(filename_c)
            except Exception:
                print(self.params_print('FAIL'))
                print('Unable to delete temporary file,')
                print('try again in 5 seconds ' + self.params_print('END'))
                time.sleep(5)
                os.remove(filename_c)


    def encoder(self):
        '''
        File decoder
        '''
        file_size = os.path.getsize(self.colorfile)

        print('SIZE: ' + str(file_size) + ' bytes')
        print('-' * 46)

        file_size_hex, extension_hex = (
            self.string_to_hex(str(file_size)),
            self.string_to_hex(self.extension))

        if len(file_size_hex) > 32:
            print(self.params_print('FAIL'))
            print('The file size is too large' + self.params_print('END'))

            if self.colordir:
                self.file_clean('./compressed.zip')

            sys.exit(1)

        file_size_hex, extension_hex = (
            file_size_hex.ljust(32, '0'),
            extension_hex.ljust(16, '0'))

        print('file_size:', file_size_hex, len(file_size_hex))
        print('extension:', extension_hex, len(extension_hex))

        d_frame = extension_hex + file_size_hex

        # Type bloc (file or directory)
        if self.colordir:
            print('type     : directory')
            d_frame = d_frame + 'FFFFFF'
        else:
            print('type     : file')
            d_frame = d_frame + '000000'

        # Password bloc
        if self.password:
            print('password : ***')
            d_frame = d_frame + 'FFFFFF'
        else:
            print('password : not set')
            d_frame = d_frame + '000000'

        cnt_o, cnt_start = (0, int(len(d_frame)/6))

        read_file = open(self.colorfile, 'rb')
        hexdata = d_frame + read_file.read().hex()
        data_arr, n_pos = ([], 6)
        for index in range(0, len(hexdata), n_pos):
            f_data_o = hexdata[index : index + n_pos]
            if self.password and cnt_o > cnt_start:
                f_data_o = self.data_encode(self.password, f_data_o, cnt_o)

            data_arr.append(f_data_o)
            cnt_o += 1

        img_wh = math.ceil(math.sqrt(len(data_arr)))
        print('img_dim  :', str(img_wh) + 'px2')
        print('-' * 46)

        img_c = Image.new('RGB', (img_wh, img_wh), color=(255, 255, 255))
        colors_arr = []

        if not self.verbose:
            print('[Encrypt] Please wait...')

        for data in data_arr:
            if self.verbose:
                sys.stdout.write('[Encrypt] ' + str(
                    data.ljust(6, '0')) + '\r')
                sys.stdout.flush()
            colors_arr.append(self.hex_to_rgb(data.ljust(6, '0')))

        img_c.putdata(colors_arr)
        img_c.save(self._dirname + '/' + self.filename + '.png', quality=100, subsampling=0)
        read_file.close()

        # Check if exist
        if os.path.isfile(self._dirname + '/' + self.filename + self.format_output):
            print(self.params_print('WARNING'))
            print('Since the file is already present,')
            print('the old version has been overwritten' + self.params_print('END'))
            os.remove( self._dirname + '/' + self.filename + self.format_output)
            time.sleep(1)

        os.rename(
            self._dirname + '/' + self.filename + '.png',
            self._dirname + '/' + self.filename + self.format_output)

        if self.colordir:
            self.file_clean('./compressed.zip')

        print(self.params_print('OK'))
        print('[Encrypt] Finish' + self.params_print('END'))
