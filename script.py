#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import argparse
from pathlib import Path
from colorama import init
from colorama import Fore, Style
init()

from libs import decoder, encoder


VERSION_CODE = 18
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

    filename = Path(colorfile).stem
    extension = Path(colorfile).suffix
    _dirname = os.path.dirname(colorfile)
    if _dirname == '':
        _dirname = '.'

    print('File: ' + colorfile)

    if colorin:
        # Decoder init function
        color_decoder = decoder.colors_decode()

        # Decoder init vars
        color_decoder.version_code = VERSION_CODE
        color_decoder.directory_output = DIRECTORY_OUTPUT
        color_decoder.format_output = FORMAT_OUTPUT
        color_decoder.password_stk = PASSWORD_STK

        color_decoder.colorfile = colorfile
        color_decoder.extension = extension
        color_decoder.password = password
        color_decoder.verbose = verbose

        # Decoder exec
        color_decoder.decoder()


    if colorout:
        # Encoder init function
        color_encoder = encoder.colors_encode()

        # Encoder init vars
        color_encoder.version_code = VERSION_CODE
        color_encoder.directory_output = DIRECTORY_OUTPUT
        color_encoder.format_output = FORMAT_OUTPUT
        color_encoder.password_stk = PASSWORD_STK

        color_encoder.colorfile = colorfile
        color_encoder.colordir = colordir
        color_encoder._dirname = _dirname
        color_encoder.filename = filename
        color_encoder.extension = extension
        color_encoder.password = password
        color_encoder.verbose = verbose

        # Decoder exec
        color_encoder.encoder()
