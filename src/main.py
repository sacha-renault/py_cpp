from .utils import clean, build, create_module, add_component
from .openmp import has_openmp, get_openmp_flags

def main(args, call_dir, package_dir):
    if args.clean or args.build:
        if args.clean:
            print("Cleaning the build environment")
            clean()

        if args.build:
            print("Building the project")
            build()

    elif args.module or args.component or args.header:
        if args.module != "":
            print("Creating new artifacts")
            create_module(call_dir, package_dir, args.module)


        elif args.component != "":
            print("Creating new artifacts")
            add_component(call_dir, package_dir, args.component)

        elif args.header != "":
            print("Creating new artifacts")
            add_component(call_dir, package_dir, args.header, True)
    
    else:
        if args.openmp:
            if not has_openmp():
                print("OPEN MP NOT AVAILABLE")
            else:
                kwargs = {}
                comp, link = get_openmp_flags()
                kwargs["extra_compile_args"] = comp
                kwargs["extra_link_args"] = link
                print("ADD THIS TO YOUR SETUP.PY IN Pybind11Extension")
                print(f"**{kwargs}")