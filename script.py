#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import math
import argparse
from pathlib import Path
import binascii
from PIL import Image
from colorama import init
from colorama import Fore, Style
init()


FORMAT_OUTPUT = '.datacolors.png'


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True)
    parser.add_argument('-i', '--colorin', action='store_true')
    parser.add_argument('-o', '--colorout', action='store_true')
    args = parser.parse_args()
    colorfile = args.file
    colorin = args.colorin
    colorout = args.colorout

    print(params_print('INFO'))
    print(r" ____      _          _____     _             ")
    print(r"|    \ ___| |_ ___   |     |___| |___ ___ ___ ")
    print(r"|  |  | .'|  _| .'|  |   --| . | | . |  _|_ -|")
    print(r"|____/|__,|_| |__,|  |_____|___|_|___|_| |___|" + params_print('END'))

    if not os.path.isfile(colorfile):
        print('file not found: ' + colorfile)
        sys.exit(0)

    FILENAME = Path(colorfile).stem
    extension = Path(colorfile).suffix
    _DIRNAME = os.path.dirname(colorfile)
    if _DIRNAME == '':
        _DIRNAME = '.'

    print('-' * 46)
    print('File: ' + colorfile)

    if colorin:
        color_image = Image.open(colorfile)
        color_w, color_h = color_image.size
        color_image_rgb = color_image.convert("RGB")

        print('SIZE: ' + str(color_w) + 'w | ' + str(color_h) + 'h')
        print('-' * 46)

        COLOR_ARR = []
        CNT_W, CNT_H = (1, 1)

        while CNT_W < (color_w + 1):
            while CNT_H < (color_h + 1):
                px_color = color_image_rgb.getpixel((CNT_H-1, CNT_W-1))
                if color_h == 1:
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

        COLOR_ARR_LEN = len(COLOR_ARR)

        if file_size != COLOR_ARR_LEN:
            print(params_print('INFO'))
            print('[SIZE] Change ' + str(COLOR_ARR_LEN) + ' to ' + str(
                file_size) + params_print('END'))
            COLOR_ARR = COLOR_ARR[:file_size]

        bitout = open(colorfile + '.decode' + extension, 'wb')
        bitout.write(binascii.a2b_hex(''.join(COLOR_ARR)))
        bitout.close()

        print(params_print('OK'))
        print('[Decrypt] Finish' + params_print('END'))

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
            sys.exit(1)

        file_size_hex, extension_hex = (
            file_size_hex.ljust(32, '0'),
            extension_hex.ljust(16, '0'))

        print('file_size:', file_size_hex, len(file_size_hex))
        print('extension:', extension_hex, len(extension_hex))

        with open(colorfile, 'rb') as f:
            hexdata = extension_hex + file_size_hex + f.read().hex()
            data_arr, n = ([], 6)
            for index in range(0, len(hexdata), n):
                data_arr.append(hexdata[index : index + n])

            img_wh = math.ceil(math.sqrt(len(data_arr)))
            print('img_dim  :', str(img_wh) + 'px2')
            print('-' * 46)

            im = Image.new('RGB', (img_wh, img_wh), color=(255, 255, 255))
            COLOR_ARR = []

            for data in data_arr:
                sys.stdout.write('[Encrypt] ' + str(
                    data.ljust(6, '0')) + '\r')
                sys.stdout.flush()
                COLOR_ARR.append(hex_to_rgb(data.ljust(6, '0')))

            im.putdata(COLOR_ARR)
            im.save(_DIRNAME + '/' + FILENAME + FORMAT_OUTPUT, quality=100, subsampling=0)

            print(params_print('OK'))
            print('[Encrypt] Finish' + params_print('END'))
