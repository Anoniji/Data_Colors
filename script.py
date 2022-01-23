#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import math
import shutil
import argparse
from pathlib import Path
import binascii
from PIL import Image
from colorama import init
from colorama import Fore, Style
init()


VERSION_CODE = 17
DIRECTORY_OUTPUT = './decode/'
FORMAT_OUTPUT = '.datacolors'
PASSWORD_STK = False


def params_print(key):
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

def hex_to_rgb(hex_data):
    '''
    Convert hex to rgb
    '''
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex_data[i:i + 2], 16)
        rgb.append(decimal)

    return tuple(rgb)

def hex_to_string(hex_text):
    '''
    Convert hex to string
    '''
    return bytes.fromhex(hex_text).decode('ASCII').replace('\x00', '')

def rgb_to_hex(pxcolor):
    '''
    Convert rgb to hex
    '''
    r_color, g_color, b_color = pxcolor
    return '%02X %02X %02X' % (r_color, g_color, b_color)

def string_to_hex(text):
    '''
    Convert string to hex
    '''
    return text.encode('utf-8').hex()

def password_to_intlist(pswd_input):
    '''
    Convert Password to int list
    '''
    global VERSION_CODE
    incm, output = (0, [VERSION_CODE])
    for char in pswd_input:
        int_out = ord(char)
        incm += int_out
        output.append(incm)

    return output


def data_encode(pswd_input, hexcolor, pos):
    '''
    Data encoder
    '''
    global PASSWORD_STK

    if not PASSWORD_STK:
        PASSWORD_STK = password_to_intlist(pswd_input)

    for ipos in PASSWORD_STK:
        if pos % ipos == 1:
            hexcolor = hexcolor[::-1]

    return hexcolor


def file_clean(filename_c):
    '''
    File cleaner
    '''
    if os.path.isfile(filename_c):
        try:
            os.remove(filename_c)
        except Exception:
            print(params_print('FAIL'))
            print('Unable to delete temporary file,')
            print('try again in 5 seconds ' + params_print('END'))
            time.sleep(5)
            os.remove(filename_c)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str)
    parser.add_argument('-d', '--directory', type=str)
    parser.add_argument('-i', '--colorin', action='store_true')
    parser.add_argument('-o', '--colorout', action='store_true')
    parser.add_argument('-p', '--password', type=str)
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()
    colorfile = args.file
    colordir = args.directory
    colorin = args.colorin
    colorout = args.colorout
    password = args.password
    verbose = args.verbose

    if colorfile is None and colordir is None:
        print(params_print('FAIL'))
        print('please set -d or -f parameter' + params_print('END'))
        sys.exit(0)

    print(params_print('INFO'))
    print(r" ____      _          _____     _             ")
    print(r"|    \ ___| |_ ___   |     |___| |___ ___ ___ ")
    print(r"|  |  | .'|  _| .'|  |   --| . | | . |  _|_ -|")
    print(r"|____/|__,|_| |__,|  |_____|___|_|___|_| |___|" + params_print('END'))

    if colordir and colorin:
        print(params_print('INFO'))
        print('please use -f for decompress directory datacolors' + params_print('END'))
        sys.exit(0)

    if colorfile and not os.path.isfile(colorfile):
        print(params_print('FAIL'))
        print('file not found: ' + colorfile + params_print('END'))
        sys.exit(0)

    if colordir and not os.path.isdir(colordir):
        print(params_print('FAIL'))
        print('directory not found: ' + colordir + params_print('END'))
        sys.exit(0)

    print('-' * 46)

    if colorout and colordir:
        print(params_print('INFO'))
        print('Prepare directory' + params_print('END'))

        try:
            shutil.make_archive('compressed', 'zip', colordir)
        except Exception as err:
            print(params_print('WARNING'))
            print('Compress_return: ' + err + params_print('END'))
        finally:
            colorfile = 'compressed.zip'

    FILENAME = Path(colorfile).stem
    extension = Path(colorfile).suffix
    _DIRNAME = os.path.dirname(colorfile)
    if _DIRNAME == '':
        _DIRNAME = '.'

    print('File: ' + colorfile)

    if colorin:
        if extension != FORMAT_OUTPUT:
            print(params_print('FAIL'))
            print('incorrect file format' + params_print('END'))
            sys.exit(0)

        color_image = Image.open(colorfile)
        color_w, color_h = color_image.size
        color_image_rgb = color_image.convert("RGB")

        print('SIZE: ' + str(color_w) + 'w | ' + str(color_h) + 'h')
        print('-' * 46)

        COLOR_ARR = []
        CNT_W, CNT_H = (1, 1)

        if not verbose:
            print('[Decrypt] Please wait...')

        while CNT_W < (color_w + 1):
            while CNT_H < (color_h + 1):
                px_color = color_image_rgb.getpixel((CNT_H-1, CNT_W-1))
                if color_h == 1 and verbose:
                    sys.stdout.write('[Decrypt] ' + str(
                        px_color) + ' | current line: ' + str(
                        CNT_W) + '\r')
                    sys.stdout.flush()

                hex_color = rgb_to_hex(px_color)
                for u_hex in hex_color.split(' '):
                    COLOR_ARR.append(u_hex)
                CNT_H += 1

            CNT_W += 1
            CNT_H = 1

        print('GET DATA OK')
        print('-' * 46)

        extension_hex = COLOR_ARR[:8]
        COLOR_ARR = COLOR_ARR[8:]
        extension = hex_to_string(''.join(extension_hex))

        file_size_hex = COLOR_ARR[:16]
        COLOR_ARR = COLOR_ARR[16:]
        file_size = int(hex_to_string(''.join(file_size_hex)))

        type_hex = COLOR_ARR[:3]
        COLOR_ARR = COLOR_ARR[3:]
        TYPE_I = ''.join(type_hex)

        psw_hex = COLOR_ARR[:3]
        COLOR_ARR = COLOR_ARR[3:]
        PSW_I = ''.join(psw_hex)

        # Decode Directory
        if TYPE_I == 'FFFFFF':
            print(params_print('WARNING'))
            print('Automatic decompression is currently not available' + params_print('END'))

        if PSW_I == 'FFFFFF' and not password:
            print(params_print('FAIL'))
            print('Please set password' + params_print('END'))
            sys.exit(1)

        COLOR_ARR_LEN = len(COLOR_ARR)

        if file_size != COLOR_ARR_LEN:
            print(params_print('INFO'))
            print('[SIZE] Change ' + str(COLOR_ARR_LEN) + ' to ' + str(
                file_size) + params_print('END'))
            COLOR_ARR = COLOR_ARR[:file_size]

        if password:
            cnt, data_arr, n = (10, [], 3)
            for index in range(0, len(COLOR_ARR), n):
                F_DATA_I = "".join(COLOR_ARR[index : index + n])
                data_arr.append(data_encode(password, F_DATA_I, cnt))
                cnt += 1
            COLOR_ARR = data_arr

        if not os.path.isdir(DIRECTORY_OUTPUT):
            os.mkdir(DIRECTORY_OUTPUT)

        bitout = open(DIRECTORY_OUTPUT + colorfile.replace(FORMAT_OUTPUT, '') + extension, 'wb')
        bitout.write(binascii.a2b_hex(''.join(COLOR_ARR)))
        bitout.close()

        print(params_print('OK'))
        print('[Decrypt] Finish')
        print('the data has been moved into the output folder: ' + DIRECTORY_OUTPUT + params_print(
            'END'))

    if colorout:
        file_size = os.path.getsize(colorfile)

        print('SIZE: ' + str(file_size) + ' bytes')
        print('-' * 46)

        file_size_hex, extension_hex = (
            string_to_hex(str(file_size)),
            string_to_hex(extension))

        if len(file_size_hex) > 32:
            print(params_print('FAIL'))
            print('The file size is too large' + params_print('END'))

            if colordir:
                file_clean('./compressed.zip')

            sys.exit(1)

        file_size_hex, extension_hex = (
            file_size_hex.ljust(32, '0'),
            extension_hex.ljust(16, '0'))

        print('file_size:', file_size_hex, len(file_size_hex))
        print('extension:', extension_hex, len(extension_hex))

        D_FRAME = extension_hex + file_size_hex

        # Type bloc (file or directory)
        if colordir:
            print('type     : directory')
            D_FRAME = D_FRAME + 'FFFFFF'
        else:
            print('type     : file')
            D_FRAME = D_FRAME + '000000'

        # Password bloc
        if password:
            print('password : ***')
            D_FRAME = D_FRAME + 'FFFFFF'
        else:
            print('password : not set')
            D_FRAME = D_FRAME + '000000'

        CNT_O, CNT_START = (0, int(len(D_FRAME)/6))

        read_file = open(colorfile, 'rb')
        hexdata = D_FRAME + read_file.read().hex()
        data_arr, n = ([], 6)
        for index in range(0, len(hexdata), n):
            f_data_o = hexdata[index : index + n]
            if password and CNT_O > CNT_START:
                f_data_o = data_encode(password, f_data_o, CNT_O)

            data_arr.append(f_data_o)
            CNT_O += 1

        img_wh = math.ceil(math.sqrt(len(data_arr)))
        print('img_dim  :', str(img_wh) + 'px2')
        print('-' * 46)

        im = Image.new('RGB', (img_wh, img_wh), color=(255, 255, 255))
        COLOR_ARR = []

        if not verbose:
            print('[Encrypt] Please wait...')

        for data in data_arr:
            if verbose:
                sys.stdout.write('[Encrypt] ' + str(
                    data.ljust(6, '0')) + '\r')
                sys.stdout.flush()
            COLOR_ARR.append(hex_to_rgb(data.ljust(6, '0')))

        im.putdata(COLOR_ARR)
        im.save(_DIRNAME + '/' + FILENAME + '.png', quality=100, subsampling=0)
        read_file.close()

        # Check if exist
        if os.path.isfile(_DIRNAME + '/' + FILENAME + FORMAT_OUTPUT):
            print(params_print('WARNING'))
            print('Since the file is already present,')
            print('the old version has been overwritten' + params_print('END'))
            os.remove( _DIRNAME + '/' + FILENAME + FORMAT_OUTPUT)
            time.sleep(1)

        os.rename(
            _DIRNAME + '/' + FILENAME + '.png',
            _DIRNAME + '/' + FILENAME + FORMAT_OUTPUT)

        if colordir:
            file_clean('./compressed.zip')

        print(params_print('OK'))
        print('[Encrypt] Finish' + params_print('END'))
