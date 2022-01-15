#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import math
import argparse
import numpy as np
import scipy.misc as smp
from PIL import Image


def hex_to_rgb(hex):
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i + 2], 16)
        rgb.append(decimal)

    return tuple(rgb)

def rgb_to_hex(px_color):
    r, g, b = px_color
    return '{:X} {:X} {:X}'.format(r, g, b)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True)
    parser.add_argument('-i', '--colorin', action='store_true')
    parser.add_argument('-o', '--colorout', action='store_true')
    args = parser.parse_args()
    colorfile = args.file
    colorin = args.colorin
    colorout = args.colorout

    if not os.path.isfile(colorfile):
        print('file not found: ' + colorfile)
        sys.exit(0)

    if colorin:
        color_image = Image.open(colorfile)
        color_w, color_h = color_image.size
        color_image_rgb = color_image.convert("RGB")

        print('-'*40)
        print('File: ' + colorfile)
        print('SIZE: ' + str(color_w) + 'w | ' + str(color_h) + 'h')
        print('-'*40)

        color_arr = []
        cnt_w, cnt_h = (1, 1)

        while cnt_w < (color_w + 1):
            while cnt_h < (color_h + 1):
                px_color = color_image_rgb.getpixel((cnt_w-1, cnt_h-1))

                if color_h == 1:
                    sys.stdout.write('[encrypt] ' + str(
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

        with open(colorfile + '.output', 'wb') as f:
            for i in color_arr:

                c = int(('0x' + i).encode(), 16)
                h = hex(c)
                print(h)

                f.write(h.encode())

    if colorout:
        with open(colorfile, 'rb') as f:
            hexdata = f.read().hex()
            data_arr = []
            n = 6
            img_w = 1920
            for index in range(0, len(hexdata), n):
                data_arr.append(hexdata[index : index + n])

            len_arr = len(data_arr)
            img_h = int(math.ceil(len_arr/img_w))

            im = Image.new('RGB', (img_w, img_h))
            color_arr = []

            for data in data_arr:
                color_arr.append(hex_to_rgb(data.ljust(6, '0')))

            im.putdata(color_arr)
            im.save(colorfile + '.colordisk.jpg')
