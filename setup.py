from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize("main.py"),
    include_dirs=[numpy.get_include()]  # Include only NumPy headers
)

# to build: python setup.py build_ext --inplace