"""
Logikit - Python package for automatically visualizing function execution
"""
from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="logikit",
    version="0.1.0",
    author="Rim Choi",
    author_email="hyerimc858@gmail.com",
    description="Automatically trace function execution and generate flowcharts with a Python decorator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rimi0108/logikit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
    },
)

