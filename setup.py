from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='str-macros',
    version='0.1',
    description='Macros (variables) for str class attributes',
    long_description=long_description,
    url='https://github.com/abramovd/str-macros',
    author='Dmitry Abramov',
    author_email='diabramo@yandex.ru',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='python django str macros',
    packages=find_packages(),
)
