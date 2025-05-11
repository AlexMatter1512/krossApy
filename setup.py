from setuptools import find_packages, setup

with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name='krossApy',
    version='0.1.2',
    description='Unofficial API for KrossBooking',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    package_dir={"krossApy": "krossApy"},
)
