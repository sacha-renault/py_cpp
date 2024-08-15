import os
from typing import List, Optional
import shutil

from .configuration import Config
from .data import __BINDING_INCLUDES__, __CONFIG_FILE_NAME__

def try_remove_dir(dir_path: str) -> None:
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
        print(f"Clean fodler {dir_path}/")

def clean():
    """Clean the previous build.
    """
    # first, remove build
    for directory in ["build", "temp", "tmp", "__pycache__"]:
        try_remove_dir(directory)

    # find all .o and all .so
    to_delete = []
    for directory, _, files in os.walk("."):
        for file in files:
            if file.endswith(".o") or file.endswith(".so"):
                to_delete.append(os.path.join(directory, file))
    
    # iterate over the to delete file to end
    for file in to_delete:
        os.remove(file)
        print(f"Clean file: {file}")


def copy_and_replace(src_folder: str, src_file: str, dest_folder: str, package_name: str) -> None:
    """Copy a file and replace a pattern with package_name.

    Args:
        src_folder (str): source folder
        src_file (str): source file
        dest_folder (str): folder where the file will be copied
        package_name (str): name of the package that will replace the pattern.
    """
    with open(os.path.join(src_folder, src_file), "r") as fp:
        file = fp.read()

    dest = os.path.join(dest_folder, src_file.replace("template", package_name))
    with open(dest, "w") as fp:
        print(f"New file added : {dest}")
        fp.write(file.replace("%module_name%", package_name))


def create_module(call_dir, package_dir, package_name) -> None:
    """Create a new module by creating a directory and copying files inside.
    Also create a config.json

    Args:
        call_dir (str): where the cmd is called
        package_dir (str): location of this package (py_cpp)
        package_name (str): desired name for the package

    Raises:
        ValueError: a folder already exist with the name of the package
    """

    # First step is to create the directory
    package_path = os.path.join(call_dir, package_name)
    if os.path.isdir(package_path):
        raise ValueError("Dirname alreay exist")
    os.mkdir(package_path)


    # Then for other files
    src_folder = os.path.join(package_dir, "files/module")
    for file in os.listdir(src_folder):
        copy_and_replace(src_folder, file, package_path, package_name)

    # Create the config.json
    config = Config(package_name)
    config.save(os.path.join(call_dir, package_name, __CONFIG_FILE_NAME__))


def add_component(call_dir, package_dir, component_name, header_only = False):
    """Add a component into a module

    Args:
        call_dir (str): where the cmd is called
        package_dir (str): location of this package (py_cpp)
        component_name (str): name of the component
        header_only (bool, optional): if true only add the header. Defaults to False.

    Raises:
        Exception: The current folder doesn't contain a config.json
        ValueError: Component name already exist
    """
    if not __CONFIG_FILE_NAME__ in os.listdir(call_dir):
        raise Exception("This is probably not a cpp module, no setup.py was found")

    # component path & check if src folder already exist
    component_path = os.path.join(call_dir, "src")
    if not os.path.isdir(component_path):
        os.mkdir(component_path)

    # Check if path already exist
    dst = os.path.join(component_path, component_name)
    if os.path.isfile(dst + ".h") or os.path.isfile(dst + ".cpp"):
        raise ValueError("Component already exist")

    # Open binding to add a new dependency
    with open("binding.cpp", "r") as file:
        content = file.read()

    # add includes in in bindings
    with open("binding.cpp", "w") as file:
        include_statement = f"#include \"src/{component_name}.h\""
        new_content = content.replace(__BINDING_INCLUDES__, f"{include_statement}\n{__BINDING_INCLUDES__}")
        file.write(new_content)    

    # Then for other files
    src_folder = os.path.join(package_dir, "files/component")
    if not header_only:
        for file in os.listdir(src_folder):
            copy_and_replace(src_folder, file, component_path, component_name)
    else:
        copy_and_replace(src_folder, "template.h", component_path, component_name)


def safe_list_extend(base_list: Optional[List[str]], new_items: List[str]) -> List:
    if base_list is None:
        return new_items
    else:
        for item in new_items:
            if item not in base_list:
                base_list.append(item)
        return base_list