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

## Usage

- Run the script to create a new package

```sh
py_cpp --create my_package_name
```

- Run the script to build

```sh
py_cpp --clean --build
```
