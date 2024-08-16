from .utils import clean, create_module, add_component, safe_list_extend
from .build import build
from .openmp import has_openmp, get_openmp_flags
from .configuration import Config
from .data import __CONFIG_FILE_NAME__
from .auto_binding.create_binding import auto_bindings

def main(args, call_dir: str, package_dir: str):
    # First check if build or clean 
    if args.clean or args.build or args.auto_build:
        if args.clean:
            print("Cleaning the build environment")
            clean()

        if args.build:
            print("Building the project")
            build(call_dir, "binding.cpp")
        
        elif args.auto_build:
            auto_bindings(call_dir, package_dir)

    # Else (because cant add a module after build)
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
    
    # Else (update the config)
    else:
        config = Config.load(__CONFIG_FILE_NAME__)

        # Set openmp
        if args.setopenmp:
            if not has_openmp():
                raise Exception("OPEN MP NOT AVAILABLE")
            else:
                comp, link = get_openmp_flags()
                config.extra_compile_args = safe_list_extend(config.extra_compile_args, comp)
                config.extra_link_args = safe_list_extend(config.extra_link_args, link)
                config.save(__CONFIG_FILE_NAME__)
        
        elif args.setversion:
            config.version = args.setversion
            config.save(__CONFIG_FILE_NAME__)
        
        else:
            raise ValueError("Unknown cmd name")