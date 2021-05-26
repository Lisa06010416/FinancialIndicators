import os
import platform
from setuptools import find_packages, setup
from setuptools.command.install import install


setup(
    name="financial_indicators",
    version="0.1.0",
    description="",
    long_description="",
    long_description_content_type='text',
    author="Lisa",
    author_email="lisalin0601@gmail.com",
    url="https://github.com/Lisa06010416/PythonPackaging",
    packages=find_packages("src", exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    package_dir={"":"src"},
    install_requires=["ta-lib", "requests", "pandas"],
    classifiers={
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Environment :: MacOS X",
        "Programming Language :: Python",
    }
)