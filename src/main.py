from glob import glob
from .utils import clean, create_module, add_component, safe_list_extend, move_to_backup
from .build import build
from .openmp import has_openmp, get_openmp_flags
from .configuration import Config
from .data import __CONFIG_FILE_NAME__, __BINDING_PATH__

def main(args, call_dir: str, pycpp_location: str):
    # First check if build or clean 
    if args.clean or args.build or args.auto_binding:
        if args.clean:
            print("Cleaning the build environment")
            clean()

        if args.auto_binding:
            from .auto_binding.create_binding import auto_bindings
            
            # Make the content of the new binding file
            content = auto_bindings(call_dir, pycpp_location)

            # move the current into backup
            move_to_backup(__BINDING_PATH__)

            # write into a new binding file
            with open(__BINDING_PATH__, "w+") as file:
                file.write(content)

        if args.auto_hints:
            from .auto_binding.create_pyi import auto_hints

            # Make the content of the new binding file
            content = auto_hints(call_dir, pycpp_location)

            # find pyi file
            pyi_file = glob("*.pyi")[0]

            # move the current into backup
            move_to_backup(pyi_file)

            # write into a new binding file
            with open(pyi_file, "w+") as file:
                file.write(content)

        if args.build:
            print("Building the project")
            build(call_dir, __BINDING_PATH__)
        
        

    # Else (because cant add a module after build)
    else:
        if args.module != "":
            print("Creating new artifacts")
            create_module(call_dir, pycpp_location, args.module)

        elif args.component != "":
            print("Creating new artifacts")
            add_component(call_dir, pycpp_location, args.component)

        elif args.header != "":
            print("Creating new artifacts")
            add_component(call_dir, pycpp_location, args.header, True)
    
        # Else (update the config)
        elif args.setopenmp:
            config = Config.load(__CONFIG_FILE_NAME__)

            if not has_openmp():
                raise Exception("OPEN MP NOT AVAILABLE")
            else:
                comp, link = get_openmp_flags()
                config.extra_compile_args = safe_list_extend(config.extra_compile_args, comp)
                config.extra_link_args = safe_list_extend(config.extra_link_args, link)
                config.save(__CONFIG_FILE_NAME__)
        
        elif args.setversion:
            config = Config.load(__CONFIG_FILE_NAME__)
            config.version = args.setversion
            config.save(__CONFIG_FILE_NAME__)
        
        else:
            raise ValueError("Unknown cmd name")