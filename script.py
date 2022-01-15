#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import math
import argparse
from pathlib import Path
import numpy as np
import scipy.misc as smp
from PIL import Image
from colorama import init
from colorama import Fore, Style
init()

def params_print(key):
    values = {
        'INFO': Style.BRIGHT + Fore.CYAN,
        'OK': Style.BRIGHT + Fore.GREEN,
        'WARNING': Style.BRIGHT + Fore.YELLOW,
        'FAIL': Style.BRIGHT + Fore.RED,
        'DEFAULT': Style.BRIGHT + Fore.WHITE,
        'END': Style.RESET_ALL,
    }
    return values.get(key, Style.RESET_ALL)

def hex_to_rgb(hex):
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i + 2], 16)
        rgb.append(decimal)

    return tuple(rgb)

def hex_to_string(hex_text):
    return bytes.fromhex(hex_text).decode('ASCII')

def rgb_to_hex(px_color):
    r, g, b = px_color
    return '%02X %02X %02X' % (r, g, b)

def string_to_hex(text):
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

    filename = Path(colorfile).stem
    extension = Path(colorfile).suffix
    dirname = os.path.dirname(colorfile)
    if dirname == '':
        dirname = '.'

    print('-' * 46)
    print('File: ' + colorfile)

    if colorin:
        color_image = Image.open(colorfile)
        color_w, color_h = color_image.size
        color_image_rgb = color_image.convert("RGB")

        print('SIZE: ' + str(color_w) + 'w | ' + str(color_h) + 'h')
        print('-' * 46)

        color_arr = []
        cnt_w, cnt_h = (1, 1)

        while cnt_w < (color_w + 1):
            while cnt_h < (color_h + 1):
                px_color = color_image_rgb.getpixel((cnt_h-1, cnt_w-1))
                if color_h == 1:
                    sys.stdout.write('[Decrypt] ' + str(
                        px_color) + ' | current line: ' + str(
                        cnt_w) + '\r')
                    sys.stdout.flush()

                hex_color = rgb_to_hex(px_color)
                for u_hex in hex_color.split(' '):
                    color_arr.append(u_hex)
                cnt_h += 1

            cnt_w += 1
            cnt_h = 1

        print('GET DATA OK')

        file_size_hex = color_arr[:8]
        color_arr = color_arr[8:]
        print(file_size_hex)

        print(hex_to_string(''.join(file_size_hex)))

        extension_hex = color_arr[:16]
        color_arr = color_arr[16:]
        print(extension_hex)

        print(hex_to_string(''.join(extension_hex)))

        sys.exit(0)

        print(color_arr)

        sys.exit(0)

        with open(colorfile + '.output', 'wb') as f:
            for i in color_arr:

                c = int(('0x' + i).encode(), 16)
                h = hex(c)
                print(h)

                f.write(h.encode())

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

            print(hexdata)

            data_arr, n = ([], 6)
            for index in range(0, len(hexdata), n):
                data_arr.append(hexdata[index : index + n])

            img_wh = math.ceil(math.sqrt(len(data_arr)))
            print('img_dim  :', str(img_wh) + 'px2')
            print('-' * 46)

            im = Image.new('RGB', (img_wh, img_wh))
            color_arr = []

            for data in data_arr:

                sys.stdout.write('[Encrypt] ' + str(
                    data.ljust(6, '0')) + '\r')
                sys.stdout.flush()

                color_arr.append(hex_to_rgb(data.ljust(6, '0')))

            print(params_print('OK'))
            print('[Encrypt] Finish' + params_print('END'))

            im.putdata(color_arr)
            im.save(dirname + '/' + filename + '.datacolors.jpg', quality=100, subsampling=0)
