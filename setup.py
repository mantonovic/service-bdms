import setuptools
from distutils.core import setup

requirements = open('requirements.txt').read().split('\n')

setup(
    name='BMS-Server',
    description='BMS - Web server',
    url='https://gitlab.com/ist-supsi/swisstopo/bms',
    project_urls={
        'Documentation': 'hhttps://gitlab.com/ist-supsi/swisstopo/bms',
        'Source': 'https://gitlab.com/ist-supsi/swisstopo/bms/server.git',
        'Tracker': 'https://gitlab.com/ist-supsi/swisstopo/bms/server/issues',
    },
    author='IST-SUPSI',
    author_email='geoservice@supsi.ch',
    version='1.0.0b1',
    packages=setuptools.find_packages(),
    install_requires=[x for x in requirements if x],
    package_data={
        'assets': ['bms/assets'],
    },
    python_requires='>=3, <4',
    license='GNU General Public License v3 (GPLv3)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='Borehole Managment System - Server',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only'
    ]
)
