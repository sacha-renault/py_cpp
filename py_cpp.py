# First import os
import os

# Get where it is called from
call_dir = os.getcwd()

# Where the package is located
package_dir = os.path.dirname(__file__)

# Then import sys
import sys
sys.path.insert(0, package_dir)

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
    parser.add_argument("--openmp", action="store_true", help="Show if openmp is available")

    args = parser.parse_args()

    try:
        main(args, call_dir, package_dir)
    except Exception as e:
        print(f"Script terminated with error : {e}")