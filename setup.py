#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script for Work Memory

For modern pip, use pyproject.toml
For older pip, this setup.py provides compatibility
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read version
version_file = Path(__file__).parent / "VERSION"
version = version_file.read_text().strip() if version_file.exists() else "2.0.0"

setup(
    name="work-memory",
    version=version,
    author="OpenClaw Community",
    author_email="support@openclaw.ai",
    description="工作记忆系统 - 专为工作场景设计的文件系统记忆架构",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/openclaw/work-memory",
    packages=find_packages(where="."),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
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
        "Topic :: Office/Business :: Groupware",
    ],
    python_requires=">=3.6",
    install_requires=[],
    extras_require={
        "dev": ["pytest>=7.0.0", "black>=23.0.0"],
        "docs": ["mkdocs>=1.4.0"],
    },
)
