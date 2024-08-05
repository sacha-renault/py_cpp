#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "%module_name%.h"

namespace py = pybind11;

// Bind the cpp module here

PYBIND11_MODULE(%module_name%, m) {
    /* Add bindings here ... */
}

/*
More infos on : 
- https://pybind11.readthedocs.io/en/stable/basics.html
- https://pybind11.readthedocs.io/en/stable/classes.html
*/