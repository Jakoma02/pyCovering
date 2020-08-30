#!/usr/bin/env python3

"""
Setuptools install script
"""

from setuptools import setup

setup(
    name="Covering",
    version="0.1",
    packages=[
        "covering"
    ],
    install_requires=[
        "jupyter",
        "vpython"
    ],

    author="Jakub Komárek",
    author_email="komaja@email.cz",
    description="Pyramid puzzle tile generator",

    entry_points="""
        [console_scripts]
        covering=covering.main:main
    """
)
