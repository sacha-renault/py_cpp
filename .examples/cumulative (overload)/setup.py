import argparse
import json
from setuptools import setup
import pybind11
from pybind11.setup_helpers import Pybind11Extension, build_ext

parser = argparse.ArgumentParser()
args = parser.parse_args()
print(args)

ext_modules = [
    Pybind11Extension(
        "cumulative",
        ["cumulative.cpp", "binding.cpp"],
        include_dirs=[pybind11.get_include(), "/usr/include/eigen3"],
    ),
]

setup(
    name="cumulative",
    version="0.1",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    include_package_data=True,
)