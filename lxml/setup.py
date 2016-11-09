from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("lxml.etree.pyx")
#    ext_modules = cythonize("helloworld.pyx")
)
