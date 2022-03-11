#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import shutil
import binascii
from PIL import Image
from colorama import init
from colorama import Fore, Style
init()


class colors_decode:

    """Lib colors decode
    - init list: version_code, rgb_frame, directory_output, format_output, password_stk
                 colorfile, extension, password, verbose

    - def list: params_print, hex_to_string, rgb_to_hex, password_to_intlist, data_encode
                file_clean, decoder
    """

    def __init__(self):

        self.version_code = 0
        self.rgb_frame = ''
        self.directory_output = ''
        self.format_output = ''
        self.password_stk = False
        self.colorfile = ''
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


    def decoder(self):
        '''
        File decoder
        '''
        if self.extension != self.format_output:
            print(self.params_print('FAIL'))
            print('incorrect file format' + self.params_print('END'))
            sys.exit(0)

        color_image = Image.open(self.colorfile)
        color_w, color_h = color_image.size
        color_image_rgb = color_image.convert("RGB")

        print('SIZE: ' + str(color_w) + 'w | ' + str(color_h) + 'h')
        print('-' * 46)

        color_arr = []
        cnt_w, cnt_h = (1, 1)

        if not self.verbose:
            print('[Decrypt] Please wait...')

        while cnt_w < (color_w + 1):
            while cnt_h < (color_h + 1):
                px_color = color_image_rgb.getpixel((cnt_h-1, cnt_w-1))
                if color_h == 1 and self.verbose:
                    sys.stdout.write('[Decrypt] ' + str(
                        px_color) + ' | current line: ' + str(
                        cnt_w) + '\r')
                    sys.stdout.flush()

                hex_color = self.rgb_to_hex(px_color)
                for u_hex in hex_color.split(' '):
                    color_arr.append(u_hex)
                cnt_h += 1

            cnt_w += 1
            cnt_h = 1

        print('GET DATA OK')
        print('-' * 46)

        # D Frame init RGB
        iframe_hex = color_arr[:9]
        color_arr = color_arr[9:]
        iframe = ''.join(iframe_hex)

        if iframe != self.rgb_frame:
            print(self.params_print('WARNING'))
            print('The RGB validation is not correct,')
            print('there may be decoding problems. ' + self.params_print('END'))

        # Password bloc
        psw_hex = color_arr[:3]
        color_arr = color_arr[3:]
        psw_i = ''.join(psw_hex)

        if psw_i == 'FFFFFF' and not self.password:
            print(self.params_print('FAIL'))
            print('Please set password' + self.params_print('END'))
            sys.exit(1)

        # Type bloc (file or directory)
        type_hex = color_arr[:3]
        color_arr = color_arr[3:]
        type_i = ''.join(type_hex)

        # File + extension bloc
        extension_hex = color_arr[:8]
        color_arr = color_arr[8:]
        extension = self.hex_to_string(''.join(extension_hex))

        file_size_hex = color_arr[:16]
        color_arr = color_arr[16:]
        file_size = int(self.hex_to_string(''.join(file_size_hex)))

        color_arr_len = len(color_arr)

        if file_size != color_arr_len:
            print(self.params_print('INFO'))
            print('[SIZE] Change ' + str(color_arr_len) + ' to ' + str(
                file_size) + self.params_print('END'))
            color_arr = color_arr[:file_size]

        if self.password:
            cnt, data_arr, n = (13, [], 3)
            for index in range(0, len(color_arr), n):
                f_data_i = "".join(color_arr[index : index + n])
                data_arr.append(self.data_encode(self.password, f_data_i, cnt))
                cnt += 1
            color_arr = data_arr

        if not os.path.isdir(self.directory_output):
            os.mkdir(self.directory_output)

        bitout = open(self.directory_output + self.colorfile.replace(
            self.format_output, '') + extension, 'wb')
        bitout.write(binascii.a2b_hex(''.join(color_arr)))
        bitout.close()

        if type_i == 'FFFFFF':
            try:
                print(self.params_print('INFO'))
                print('Automatic decompression...' + self.params_print('END'))
                shutil.unpack_archive(self.directory_output + self.colorfile.replace(
                    self.format_output, '') + extension, self.directory_output)
            except Exception as err:
                print(self.params_print('WARNING'))
                print('Decompress_return: ' + err + self.params_print('END'))
            finally:
                self.file_clean(self.directory_output + self.colorfile.replace(
                    self.format_output, '') + extension)

        print(self.params_print('OK'))
        print('[Decrypt] Finish')
        print('the data has been moved into the output folder: ' + str(
            self.directory_output) + self.params_print(
            'END'))
