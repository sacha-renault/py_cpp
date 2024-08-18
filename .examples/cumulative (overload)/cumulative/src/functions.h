#pragma once
#include <pybind11/eigen.h>
#include <Eigen/Dense>

// Define types explicitly
template <typename T>
using VectorXx = Eigen::Matrix<T, Eigen::Dynamic, 1>;

template <typename T>
using VectorRef = Eigen::Ref<VectorXx<T>>;

template<typename T>
VectorXx<T> _cumsum(VectorRef<T> matrix);

// Wrapper functions
VectorXx<int> cumsum(VectorRef<int> matrix);
VectorXx<double> cumsum(VectorRef<double> matrix);
VectorXx<float> cumsum(VectorRef<float> matrix);
VectorXx<long> cumsum(VectorRef<long> matrix);
