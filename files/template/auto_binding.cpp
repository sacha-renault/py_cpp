#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
// %%SETINCLUDES%%

namespace py = pybind11;

// Bind the cpp module here

PYBIND11_MODULE(%module_name%, m) {
// %%SETBINDINGS%%
}