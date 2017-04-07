from setuptools import setup

__version__ = '0.0.1'
__author__ = 'Giacomo Manzoli'


requirements = [
    'selenium==2.53.6',
    'pyvirtualdisplay'
]

description = 'Instagram data miner for hastags, pages and posts Automation Script'

setup(
    name='instaminer_py',
    version=__version__,
    author=__author__,
    author_email='giacomo.manzoli@gmail.com',
    url='https://github.com/GiacomoManzoli/InstaPy',
    py_modules='instaminer',
    description=description,
    install_requires=requirements
)
