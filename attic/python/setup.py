import codecs
import os
import re

from setuptools import find_packages, setup


def requirements():
    with open('.meta/packages_base') as f:
        reqs = f.readlines()

    return reqs


def get_version():
    with codecs.open(os.path.join(os.path.abspath(os.path.dirname(
            __file__)), 'pyarcan', 'version.py'), 'r', 'latin1') as fp:
        try:
            version = re.findall(r"^__version__ = '([^']+)'\r?$",
                                 fp.read(), re.M)[0]
            return version
        except IndexError:
            raise RuntimeError('Unable to determine version.')


setup(
    name='pyarcan',
    version=get_version(),
    description='Arcan bindings',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    keywords='arcan',
    author='Oleg Musaev',
    author_email='olegmusaev@gmail.com',
    packages=find_packages(),
    install_requires=requirements(),
    extras_require={},
    include_package_data=True,
    zip_safe=False,
)
