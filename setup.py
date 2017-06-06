from setuptools import setup, find_packages

setup(name='bdrxml',
    version='1.0a1',
    packages=find_packages(),
    package_data={'bdrxml': ['test/data/*.*',
                             'templates/*.*']},
    install_requires=[
        'eulxml>=1.0.1',
    ]
)
