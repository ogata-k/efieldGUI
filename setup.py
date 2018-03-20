# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 13:37:16 2017

@author: Owner
うまく使えない
"""

import sys
from cx_Freeze import setup, Executable

base = None
copyDependentFiles = True
silent = True
includefiles = ["tmp.jpg", "log.txt"]
includes = ["matplotlib.pyplot"]
packages = ["wx", "math", "seaborn", "os"]
excludes = []

if sys.platform == "win32":
    base = "Win32GUI"

setup(name="sample",
      version="1.0",
      description="simulator",
      options={"build_exe": {"include_files": includefiles,
                             "includes":includes,
                             "excludes":excludes,
                             "packages":packages}},
      executables=[Executable("efield.py", base=base)])
