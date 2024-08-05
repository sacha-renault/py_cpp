import argparse
import subprocess
import os
import sys

def build():
    result = subprocess.run([sys.executable, "setup.py", "build_ext", "--inplace"], capture_output=True, text=True)
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)


def clean():
    result = subprocess.run([sys.executable, "setup.py", "clean", "--all"], capture_output=True, text=True)
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)

    

def copy_and_replace(src_folder: str, src_file: str, dest_folder: str, package_name: str) -> None:
    print(os.path.join(src_folder, src_file))
    with open(os.path.join(src_folder, src_file), "r") as fp:
        file = fp.read()
    
    with open(os.path.join(dest_folder, src_file.replace("template", package_name)), "w") as fp:
        fp.write(file.replace("%module_name%", package_name))

    
    
def create(call_dir, package_dir, package_name) -> None:
    print(call_dir, package_dir)

    # First step is to create the directory
    package_path = os.path.join(call_dir, package_name) 
    if os.path.isdir(package_path):
        raise ValueError("Dirname alreay exist")
    os.mkdir(package_path)


    # Then for other files
    src_folder = os.path.join(package_dir, "files")
    for file in os.listdir(src_folder):
        copy_and_replace(src_folder, file, package_path, package_name)


def main(args):
    # Get where it is called from 
    call_dir = os.getcwd()

    # Where the package is located
    package_dir = os.path.dirname(__file__)

    if args.clean:
        print("Cleaning the build environment")
        clean()

    if args.build:
        print("Building the project")
        build()

    if args.create != "":
        print("Creating new artifacts")
        create(call_dir, package_dir, args.create)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true", help="Clean the build environment")
    parser.add_argument("--build", action="store_true", help="Build the project")
    parser.add_argument("--create", default="", help="Create new artifacts with the specified name")

    args = parser.parse_args()

    try:
        main(args)
    except Exception as e:
        print(f"Script terminated with error : {e}")