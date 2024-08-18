# JUST NOTICED THERE IS A SIMILAR REPOSITORY (much better) that does same : https://pthom.github.io/litgen/litgen_book/00_00_intro.html

# PyCpp

## Purpose

Create functions in cpp for python in minutes.

## Install (Linux)

- install dependencies :

```sh
pip install -r requirements.txt
```

- (Optional / Linux) Add the script as a cmd in bashrc file

```sh
chmod +x setup_py_cpp.sh
./setup_py_cpp.sh
```

- You need to add Python dev headers (Note : you might need a specific version depending on your current python version):

```sh
apt-get install python3-dev
```

- You need to install cpp compiler as well, you can choose anything. (Example [g++ compiler | https://data-flair.training/blogs/install-cpp/])

- (Optional / Linux) Add extra library.
  - Eigen (For Vector & Matrices)

```sh
apt-get install libeigen3-dev
```

## Usage

- Run the script to create a new package

```sh
pycpp --module my_module_name # create a new module
cd my_module_name # Need to be inside of the folder to add new component.
pycpp --component my_component # add a new component
```

- Run the script to build

```sh
pycpp --clean --build # Need to be inside of the folder to build the package.
```

- You can also add only a header file :

```sh
pycpp --header my_header # add a new header
```

## Arguments

Except --module that can be called from anywhere to create a new module, all cmd must be called from inside of a module

### Module Arguments

| Argument       | Action              | Default | Description                                                     |
| -------------- | ------------------- | ------- | --------------------------------------------------------------- |
| `--module`     | N/A                 | `""`    | Creates a new module with the specified name                    |
| `--component`  | N/A                 | `""`    | Creates a new component within a module with the specified name |
| `--header`     | N/A                 | `""`    | Creates a new header within a module with the specified name    |
| `--setopenmp`  | Sets flag to `True` | `False` | Enables OpenMP. Raises an exception if OpenMP isn't available.  |
| `--setversion` | N/A                 | `""`    | Changes the version of the package                              |

**Note:** Module arguments **do not stack**. For instance, using `pycpp --module my_module --component my_component` will ignore the `--component` argument.

### Build Arguments

| Argument         | Action              | Default | Description                                    |
| ---------------- | ------------------- | ------- | ---------------------------------------------- |
| `--clean`        | Sets flag to `True` | `False` | Cleans the build environment                   |
| `--auto_binding` | Sets flag to `True` | `False` | Automatically generates the `binding.cpp` file |
| `--auto_hints`   | Sets flag to `True` | `False` | Automatically generates the `.pyi` file        |
| `--auto`         | Sets flag to `True` | `False` | Enables both `auto_binding` and `auto_hints`   |
| `--build`        | Sets flag to `True` | `False` | Builds the project                             |

- **Note:** Build arguments **do stack**. For example, running `pycpp --clean --auto_binding --auto_hints --build` will execute all these actions sequentially. However, actions are always executed in the following order: **clean > auto_binding > auto_hints > build**, regardless of the order in which they are specified.
- **Note:** To use any of `auto`, you need to install clang : [clang | https://pypi.org/project/clang/]. The version of clang you install must match the libclang library you installed previously. Then, you need to setup the path of the lib for clang.cindex :

```sh
python
>>> from clang.cindex import Config
>>> Config.set_library_file("path/to/the/library")
```

## Writing cpp code

- /!\ Template functions aren't supported as interface, you can use it iternally but you need to wrap it in normal function to expose in bindings (see .example/cumulative (overload)).
- functions and classes whose name starts with "\_" are considered as internal and will not be exposed in bindings or the interface pyi file.
- Operator not supported yet.
