import sys
import os
from setuptools import setup, find_packages

setup(
    name='luxvector',
    version='0.1.0',
    author='',
    author_email='',
    packages=find_packages(exclude=['tests*']),
    url='',
    license='MIT',
    description='',
    long_description=open('README.md').read(),
    install_requires=[
        "pytest",
        "stable_baselines3==1.2.1a2",
        "numpy",
        "tensorboard",
        "gym==0.19.0"
    ],
    package_data={},
    test_suite='',
    tests_require=[],
)
