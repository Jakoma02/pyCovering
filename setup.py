#!/usr/bin/env python3

"""
Setuptools install script
"""

from setuptools import setup, find_packages

setup(
    name="pyCovering",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "jupyter",
        "vpython",
        "PySide2",
        "wheel",
    ],

    author="Jakub Komárek",
    author_email="komaja@email.cz",
    description="Pyramid puzzle tile generator",

    entry_points="""
        [console_scripts]
        pycovering-cli=pycovering.main:main

        [gui_scripts]
        pycovering=pycovering.qt_gui.gui:main
    """
)
