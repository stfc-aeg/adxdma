"""Setup script for Baby D Python package"""

import sys
from setuptools import setup, find_packages
import versioneer

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='adxdma',
    #   version=versioneer.get_versions(),
    #   cmdclass=versioneer.get_cmdclass(),
      description='ODIN Adxdma Adapter',
      url='https://github.com/stfc-aeg/adxdma',
      author='Ashley Neaves',
      author_email='ashley.neaves@stfc.ac.uk',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      setup_requires=["cffi>=1.0.0"],
      cffi_modules=["../lib/pyxdma_builder.py:ffibuilder"],
      install_requires=required,
      zip_safe=False
)
