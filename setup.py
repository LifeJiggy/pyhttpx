#!/usr/bin/env python3
"""
Setup script for pyhttpx-pro - A fast and multi-purpose HTTP toolkit
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open('requirements.txt', 'r') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="pyhttpx-pro",
    version="6.0.0",
    author="ArkhAngelLifeJiggy",
    author_email="Bloomtonjovish@gmail.com",
    description="A fast and multi-purpose HTTP toolkit inspired by httpx and httprobe",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LifeJiggy/pyhttpx-pro",
    packages=find_packages(),
    py_modules=['pyhttpx'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "Topic :: Utilities",
    ],
    keywords="http https probing security reconnaissance web-scanning",
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'pyhttpxpro=pyhttpx:main',
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/LifeJiggy/pyhttpx-pro/issues",
        "Source": "https://github.com/LifeJiggy/pyhttpx-pro",
        "Documentation": "https://github.com/LifeJiggy/pyhttpx-pro#readme",
    },
    include_package_data=True,
    zip_safe=False,
)