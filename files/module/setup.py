from glob import glob
from setuptools import setup
import pybind11
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "%module_name%",
        ["binding.cpp", *glob("src/*.cpp")],
        include_dirs=[pybind11.get_include()],
    ),
]

setup(
    name="%module_name%",
    version="0.1",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    include_package_data=True,
)
