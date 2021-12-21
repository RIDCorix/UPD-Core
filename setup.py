import os
from setuptools import setup, find_packages

setup(
    name='UPD-Core',
    version='1.0.0',
    url='https://github.com/RIDCorix/UPD-Core.git',
    license='BSD',
    description='UPD-Core for extensions',
    author='RIDCorix',
    author_email='ridcorix@gmail.com',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    install_requires=['setuptools', 'Yapsy', 'PySide6'],

    classifiers=[
        'Development Status :: 1 - Developing',
        'Framework :: Pyside6',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
    ]
)