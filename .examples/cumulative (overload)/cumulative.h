#pragma once
#include <pybind11/eigen.h>
#include <Eigen/Dense>

// Define types explicitly
template <typename T>
using VectorXx = Eigen::Matrix<T, Eigen::Dynamic, 1>;

template <typename T>
using VectorRef = Eigen::Ref<VectorXx<T>>;

template<typename T>
VectorXx<T> cumsum(VectorRef<T> matrix);