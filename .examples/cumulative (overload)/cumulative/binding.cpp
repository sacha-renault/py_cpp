#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "src/functions.h"
// %%SETINCLUDES%%

namespace py = pybind11;

// Bind the cpp module here

PYBIND11_MODULE(cumulative, m) {
	// FUNCTION DEFINITION 
	m.def("cumsum", py::overload_cast<VectorRef<int>>(&cumsum));
	m.def("cumsum", py::overload_cast<VectorRef<double>>(&cumsum));
	m.def("cumsum", py::overload_cast<VectorRef<float>>(&cumsum));
	m.def("cumsum", py::overload_cast<VectorRef<long>>(&cumsum));



	// CLASS DEFINITION 


}