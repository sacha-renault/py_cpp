#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "src/Grid.h"
// %%SETINCLUDES%%

namespace py = pybind11;

// Bind the cpp module here

PYBIND11_MODULE(life_game, m) {
    py::class_<GameOfLife>(m, "GameOfLife")
        .def(py::init<int, int>())
        .def(py::init<int>())
        .def_property_readonly("grid", &GameOfLife::getGrid)
        .def_property_readonly("step", &GameOfLife::getStep)
        .def("next", py::overload_cast<>(&GameOfLife::next))
        .def("next", py::overload_cast<int>(&GameOfLife::next))
        .def("set_at_index", &GameOfLife::setAtIndex)
        .def("set_pattern", &GameOfLife::setPattern);
}

/*
More infos on :
- https://pybind11.readthedocs.io/en/stable/basics.html
- https://pybind11.readthedocs.io/en/stable/classes.html
- https://gist.github.com/jiwaszki/adeb35a922b37224087c749eb17bceb2 (example overload with lambdas)
*/
