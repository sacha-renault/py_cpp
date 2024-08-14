import argparse
import subprocess
import os
import sys

BINDING_INCLUDES = "// %%SETINCLUDES%%"

def build():
    result = subprocess.run([sys.executable, "setup.py", "build_ext", "--inplace"], capture_output=True, text=True)
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)


def clean():
    result = subprocess.run([sys.executable, "setup.py", "clean", "--all"], capture_output=True, text=True)
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


def main(args):
    # Get where it is called from
    call_dir = os.getcwd()

    # Where the package is located
    package_dir = os.path.dirname(__file__)

    if args.clean or args.build:
        if args.clean:
            print("Cleaning the build environment")
            clean()

        if args.build:
            print("Building the project")
            build()

    else:
        if args.module != "":
            print("Creating new artifacts")
            create_module(call_dir, package_dir, args.module)


        elif args.component != "":
            print("Creating new artifacts")
            add_component(call_dir, package_dir, args.component)

        elif args.header != "":
            print("Creating new artifacts")
            add_component(call_dir, package_dir, args.header, True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true", help="Clean the build environment")
    parser.add_argument("--build", action="store_true", help="Build the project")
    parser.add_argument("--module", default="", help="create new module with the specified name")
    parser.add_argument("--component", default="", help="create new compoenent within the module with the specified name")
    parser.add_argument("--header", default="", help="create new header within the module with the specified name")

    args = parser.parse_args()

    try:
        main(args)
    except Exception as e:
        print(f"Script terminated with error : {e}")