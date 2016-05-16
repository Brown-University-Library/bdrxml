from setuptools import setup, find_packages

setup(name='bdrxml',
    version='0.8-dev',
    packages=find_packages(),
    package_data={'bdrxml': ['test/data/*.*',
                             'templates/*.*']},
)
