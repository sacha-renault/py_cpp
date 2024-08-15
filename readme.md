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
py_cpp --module my_module_name # create a new module
cd my_module_name # Need to be inside of the folder to add new component.
py_cpp --component my_component # add a new component
```

- Run the script to build

```sh
py_cpp --clean --build # Need to be inside of the folder to build the package.
```

- You can also add only a header file :

```sh
py_cpp --header my_header # add a new header
```

## Arguments

| Argument       | Action             | Default | Description                                                                      |
| -------------- | ------------------ | ------- | -------------------------------------------------------------------------------- |
| `--clean`      | set flag to `True` | `False` | Clean the build environment                                                      |
| `--build`      | set flag to `True` | `False` | Build the project                                                                |
| `--module`     | N/A                | `""`    | Create a new module with the specified name                                      |
| `--component`  | N/A                | `""`    | Create a new component within the module with the specified name                 |
| `--header`     | N/A                | `""`    | Create a new header within the module with the specified name                    |
| `--setopenmp`  | set flag to `True` | `False` | Set OpenMP to available if open mp isn't available, an exception will be raised. |
| `--setversion` | N/A                | `""`    | Change the version of the package                                                |
