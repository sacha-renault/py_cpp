import sys
import os
from typing import List, Optional
from glob import glob

from setuptools import setup
import pybind11
from pybind11.setup_helpers import Pybind11Extension, build_ext

from .configuration import Config
from .data import __CONFIG_FILE_NAME__

def build(
        path_pacakge, 
        binding_src) -> None:
    # load the configuration
    config = Config.load(os.path.join(path_pacakge, __CONFIG_FILE_NAME__))
    
    # Change the argv to execute the setup.py
    sys.argv = [sys.executable, "build_ext", "--inplace"]

    # If include dir is None just set as empty list
    if config.include_dirs is None:
        include_dirs = []
    else:
        include_dirs = config.include_dirs

    # Make the module
    ext_modules = [
        Pybind11Extension(
            config.name,
            [os.path.join(path_pacakge, binding_src), *glob(os.path.join(path_pacakge, "src", "*.cpp"))],
            include_dirs=[pybind11.get_include(), *include_dirs],
            extra_compile_args = config.extra_compile_args,
            extra_link_args = config.extra_link_args)
    ]

    # Finally exectute the setup
    setup(
        name=config.name,
        version=config.version,
        ext_modules=ext_modules,
        cmdclass={"build_ext": build_ext},
    )