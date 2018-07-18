"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
from setuptools import setup, find_packages


setup(
    name="gigabyte_k85",
    packages=find_packages(),
    version="0.0.1",
    description="Gigabyte K85 backend for rgbkeyboards",
    author="RedFantom",
    url="https://github.com/RedFantom/gigabyte_k85",
    keywords=["RGB", "HID Device", "rgbkeboards"],
    license="GNU GPLv3",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
    ],
    install_requires=["pyusb"]
)
