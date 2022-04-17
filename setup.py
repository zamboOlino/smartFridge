from setuptools import setup
import os

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = lib_folder + '/requirements.txt'

install_requires = []

if os.path.isfile(requirement_path):
    with open(requirement_path) as fp:
        install_requires = fp.read().splitlines()

setup(
    name='smartFridge',
    version='0.0.1',
    install_requires=install_requires,
    url='https://github.com/zamboOlino/smartFridge',
    author='K0NRAD',
    author_email='konrad.hauke@mail.schwarz',
    description='smartFridge - Kreative Köpfe 2022'
)

