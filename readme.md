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

| Argument       | Action             | Default | Description                                                                      | Callable From   |
| -------------- | ------------------ | ------- | -------------------------------------------------------------------------------- | --------------- |
| `--clean`      | set flag to `True` | `False` | Clean the build environment                                                      | Inside a module |
| `--build`      | set flag to `True` | `False` | Build the project                                                                | Inside a module |
| `--module`     | N/A                | `""`    | Create a new module with the specified name                                      | Anywhere        |
| `--component`  | N/A                | `""`    | Create a new component within the module with the specified name                 | Inside a module |
| `--header`     | N/A                | `""`    | Create a new header within the module with the specified name                    | Inside a module |
| `--setopenmp`  | set flag to `True` | `False` | Set OpenMP to available. If OpenMP isn't available, an exception will be raised. | Inside a module |
| `--setversion` | N/A                | `""`    | Change the version of the package                                                | Inside a module |
