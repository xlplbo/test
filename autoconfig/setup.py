#!/usr/bin/python
# coding:utf-8
# Contributor:
# liubo5 <lboxlp@163.com>

from distutils.core import setup
import py2exe

includes = ["encodings", "encodings.*"]
options = {"py2exe":
                    {"compressed": 1,
                     "optimize": 2,
                     "ascii": 1,
                     "includes":includes,
                     "bundle_files": 1}
           }
setup(
    options = options,
    zipfile=None,
    console=["autoconfig.py"],
    data_files=[(".",["config.ini", "ReadMe.txt", "windll.zip"])]
    )