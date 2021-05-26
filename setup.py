import os
import platform
from setuptools import find_packages, setup
from setuptools.command.install import install


class MyInstall(install):
    def run(self):
        if platform.system().lower() == 'windows': ##?
            os.system("wget https://download.lfd.uci.edu/pythonlibs/q4trcu4l/cp36/TA_Lib-0.4.19-cp36-cp36m-win_amd64.whl")
            os.system("pip install TA_Lib-0.4.19-cp36-cp36m-win_amd64.whl")
        elif platform.system().lower() == 'linux': ##?
            os.system("wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz")
            os.system("tar -xvf ta-lib-0.4.0-src.tar.gz")
            os.system("cd ta-lib")
            os.system("./configure --prefix=/usr")
            os.system("make")
            os.system("sudo make install")
        else:
            os.system("brew install ta-lib")
        install.run(self)


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
    },
    cmdclass={'install': MyInstall},
)