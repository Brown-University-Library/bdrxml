from setuptools import setup, find_packages

setup(name='bdrxml',
    version='1.2',
    url='https://github.com/Brown-University-Library/bdrxml',
    author='Brown University Library',
    author_email='bdr@brown.edu',
    packages=find_packages(),
    package_data={'bdrxml': ['schemas/*.*']},
    install_requires=[
        'eulxml==1.1.3',
        'ply==3.8',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

