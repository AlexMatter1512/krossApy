from setuptools import find_packages, setup

with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name='krossApy',
    version='0.0.4',
    description='Unofficial Python API for KrossBooking',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    # ext_package='krossApy',
    # packages=find_packages(where="krossApy"),
    package_dir={"krossApy": "krossApy"},
    # packages=find_packages(where="krossApy"),
)