import io

from setuptools import find_packages, setup

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='gfndevice',
    version='1.0.0',
    license='BSD',
    maintainer='SOCC Unipi',
    description='Microservice for managing devices for the Gio system',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask_sqlalchemy'
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-cov'
        ],
    },
)
