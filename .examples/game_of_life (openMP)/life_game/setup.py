import os
from setuptools import setup
import pybind11
from pybind11.setup_helpers import Pybind11Extension, build_ext

def get_cpp_files() -> list:
    component_pathes = []
    for dir,_, files in os.walk("."):
        for file in files:
            if file.endswith(".cpp"):
                component_pathes.append(os.path.join(dir, file))
    return component_pathes

ext_modules = [
    Pybind11Extension(
        "life_game",
        get_cpp_files(),
        include_dirs=[pybind11.get_include(), "/usr/include/eigen3"],
        extra_compile_args = ["-fopenmp", '-std=c++14'],
        extra_link_args = ["-fopenmp"]
    ),
]

setup(
    name="life_game",
    version="0.1",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)
