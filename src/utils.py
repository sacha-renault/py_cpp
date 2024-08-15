import os
import sys
import subprocess

BINDING_INCLUDES = "// %%SETINCLUDES%%"

def kwargs_to_cmd(**kwargs):
    extra_args = []
    for k, v in kwargs.items():
        extra_args.append(f"--{k}")
        extra_args.append(v)
    return extra_args

def build(**kwargs):
    run_args = [sys.executable, "setup.py", "build_ext", "--inplace"] + kwargs_to_cmd(**kwargs)
    result = subprocess.run(run_args, capture_output=True, text=True)
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)


def clean(**kwargs):
    run_args = [sys.executable, "setup.py", "clean", "--all"]  + kwargs_to_cmd(**kwargs)
    result = subprocess.run(run_args, capture_output=True, text=True)
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)



def copy_and_replace(src_folder: str, src_file: str, dest_folder: str, package_name: str) -> None:
    with open(os.path.join(src_folder, src_file), "r") as fp:
        file = fp.read()

    dest = os.path.join(dest_folder, src_file.replace("template", package_name))
    with open(dest, "w") as fp:
        print(f"New file added : {dest}")
        fp.write(file.replace("%module_name%", package_name))



def create_module(call_dir, package_dir, package_name) -> None:
    print(call_dir, package_dir)

    # First step is to create the directory
    package_path = os.path.join(call_dir, package_name)
    if os.path.isdir(package_path):
        raise ValueError("Dirname alreay exist")
    os.mkdir(package_path)


    # Then for other files
    src_folder = os.path.join(package_dir, "files/module")
    for file in os.listdir(src_folder):
        copy_and_replace(src_folder, file, package_path, package_name)


def add_component(call_dir, package_dir, component_name, header_only = False):
    if not "setup.py" in os.listdir(call_dir):
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
        new_content = content.replace(BINDING_INCLUDES, f"{include_statement}\n{BINDING_INCLUDES}")
        file.write(new_content)    

    # Then for other files
    src_folder = os.path.join(package_dir, "files/component")
    if not header_only:
        for file in os.listdir(src_folder):
            copy_and_replace(src_folder, file, component_path, component_name)
    else:
        copy_and_replace(src_folder, "template.h", component_path, component_name)