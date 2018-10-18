from setuptools import setup, find_packages

setup(name='bdrxml',
    version='0.9',
    packages=find_packages(),
    package_data={'bdrxml': ['test/data/*.*',
                             'schemas/*.*']},
    install_requires=[
        'eulxml==1.1.3',
        'ply==3.8',
    ]
)
