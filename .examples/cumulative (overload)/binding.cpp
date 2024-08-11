#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "cumulative.h"

namespace py = pybind11;

// Bind the cpp module here

PYBIND11_MODULE(cumulative, m) {
    // def cumsum
    m.def("cumsum", py::overload_cast<VectorRef<int>>(&cumsum<int>));
    m.def("cumsum", py::overload_cast<VectorRef<double>>(&cumsum<double>));
    m.def("cumsum", py::overload_cast<VectorRef<float>>(&cumsum<float>));
    m.def("cumsum", py::overload_cast<VectorRef<long>>(&cumsum<long>));
}

/*
More infos on : 
- https://pybind11.readthedocs.io/en/stable/basics.html
- https://pybind11.readthedocs.io/en/stable/classes.html
*/