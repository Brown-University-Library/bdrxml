from setuptools import setup, find_packages

setup(name='bdrxml',
    version='1.0b1',
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

