from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name = 'plot-pytest-benchmark',
    version='0.0.1',
    description="Plot histograms from 'pytest-benchmark'",
    keywords=['pytest', 
              'benchmark', 
              'pytest-benchmark',
              ]
    author = 'Maurício Bonatte',
    author_email='mbonatte@ymail.com',
    url = 'https://github.com/mbonatte/plot-pytest-benchmark',
    license='MIT',
    long_description=long_description,
    
    # Dependencies
    install_requires=['matplotlib'],
    
    # Packaging
    packages =['plot-pytest-benchmark'],
    
)