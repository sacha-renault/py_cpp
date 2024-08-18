# First import os
import os

# Get where it is called from
call_dir = os.getcwd()

# Where the package is located
pycpp_location = os.path.dirname(__file__)

# Then import sys
import sys
sys.path.insert(0, pycpp_location)

# Other imports
import argparse
from src.main import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true", help="Clean the build environment")
    parser.add_argument("--build", action="store_true", help="Build the project")
    parser.add_argument("--module", default="", help="create new module with the specified name")
    parser.add_argument("--component", default="", help="create new compoenent within the module with the specified name")
    parser.add_argument("--header", default="", help="create new header within the module with the specified name")
    parser.add_argument("--setopenmp", action="store_true", help="Setopenmp to available")
    parser.add_argument("--setversion", default="", help="Change version of package")
    parser.add_argument("--auto_binding", action="store_true", help="Auto make bindings")
    parser.add_argument("--auto_hints", action="store_true", help="Auto make hints (pyi)")
    parser.add_argument("--auto", action="store_true", help="Enable both auto_binding and auto_hints")

    # Parse
    args = parser.parse_args()

    # Handle auto
    if args.auto:
        args.auto_binding = True
        args.auto_hints = True

    try:
        main(args, call_dir, pycpp_location)
    except Exception as e:
        print(f"Script terminated with error : {e}")