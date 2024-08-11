#include "cumulative.h"

// Explicit instanciation
template VectorXx<int> cumsum(VectorRef<int> matrix);
template VectorXx<double> cumsum(VectorRef<double> matrix);
template VectorXx<float> cumsum(VectorRef<float> matrix);
template VectorXx<long> cumsum(VectorRef<long> matrix);

template<typename T>
Eigen::Matrix<T, Eigen::Dynamic, 1> cumsum(Eigen::Ref<Eigen::Matrix<T, Eigen::Dynamic, 1>> matrix) {
    // Get the size of the input vector
    int size = matrix.size();

    // Initialize the output vector with the same size as the input vector
    Eigen::Matrix<T, Eigen::Dynamic, 1> output(size);
    output(0) = matrix(0);

    for (int i = 1; i < size; ++i) {
        output(i) = matrix(i) + output(i - 1);
    }

    return output;
}