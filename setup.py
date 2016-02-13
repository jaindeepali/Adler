import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

with open('requirements.txt') as f:
    requirements = [l.strip() for l in f.readlines()]

setup(
    name = "Adler",
    version = "0.0.1",
    author = "Deepali Jain",
    author_email = "djdeepalijain811@gmail.com",
    description = ("Ready-to-use text classification corpus generation from [TechTC-300 Test Collection](http://techtc.cs.technion.ac.il/techtc300/techtc100.html)."),
    license = "MIT",
    url = "https://github.com/jaindeepali/Adler",
    install_requires=requirements,
    packages=['Adler'],
    package_data={
        'Adler': ['config/config.json']
    },
    long_description=read('README.md'),
)