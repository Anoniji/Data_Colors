#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Created by Anoniji
Library made available under the terms of the license
Attribution-NonCommercial-NoDerivs 3.0 Unported (CC BY-NC-ND 3.0)
https://creativecommons.org/licenses/by-nc-nd/3.0/
'''

import sys
from cx_Freeze import setup, Executable

VERSION = '1.0.0.0'
cible = Executable(script='script.py', base='Console', targetName="data_colors.exe")

setup(
    name='Data Colors',
    version=VERSION,
    author='Anoniji',
    options={
        'build_exe': {
            'path': sys.path,
            'includes': [],
            'excludes': [],
            'packages': [],
            'optimize': 2,
            'silent': True,
            'zip_include_packages': '*',
            'zip_exclude_packages': '',
            'include_msvcr': True,
            'build_exe': './_build/',
        },
    },
    executables=[cible],
)
