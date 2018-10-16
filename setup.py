from setuptools import setup, find_packages

setup(name='bdrxml',
    version='0.9a1',
    packages=find_packages(),
    package_data={'bdrxml': ['test/data/*.*',
                             'templates/*.*']},
    install_requires=[
        'eulxml==1.1.3',
        'ply==3.8',
    ]
)
