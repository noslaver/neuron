from setuptools import setup, find_packages

setup(
    nam = 'neuron',
    version = '0.1.0',
    author = 'Noam Koren',
    description = 'Brain-Computer interface',
    packages = find_packages(),
    install_require = [],
    tests_require = ['pytest', 'pytest-cov']
)
