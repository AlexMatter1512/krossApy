from setuptools import find_packages, setup

with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name='krossApy',
    version='0.2.0',
    description='Unofficial Python client for the Kross Booking v5 mobile API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(include=['krossApy', 'krossApy.*']),
    install_requires=[
        'requests',
    ],
    python_requires='>=3.9',
)
