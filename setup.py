# import
from setuptools import setup, find_packages

# setup
setup(
    name='techan',
    version='0.0.2',
    description='A Python package for technical analysis',
    url='https://github.com/XO30/techan',
    author='Stefan Siegler',
    author_email='dev@siegler.one',
    packages=find_packages(),
    classifiers=[
            'Intended Audience :: Data Scientists',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10'
        ],
    install_requires=[
            'numpy',
            'pandas',
            'datetime',
            'typing',
            'plotly',
            'tqdm',
        ],
    python_requires='>3.5, <4',
)
