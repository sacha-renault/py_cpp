import os
from setuptools import setup
import pybind11
from pybind11.setup_helpers import Pybind11Extension, build_ext

def get_component_path() -> list:
    component_pathes = []
    for path in os.listdir():
        if os.path.isdir(path) and path != "__pycache__":
            component_pathes.append(path)
    return [f"{component_path}/{component_path}.cpp" for component_path in component_pathes]

ext_modules = [
    Pybind11Extension(
        "%module_name%",
        ["binding.cpp"] + get_component_path(),
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
