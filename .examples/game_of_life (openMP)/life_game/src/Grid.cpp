#include "Grid.h"

// Define your functions / class here
void GameOfLife::next(){
    // set step
    step_ ++;

    // get size
    int cols = grid_.cols();
    int rows = grid_.rows();

    // Init a new matrix, not memory efficient but allows
    // To parallelize during loop calculation
    Eigen::MatrixXi new_grid(Eigen::MatrixXi::Zero(cols, rows));

    #pragma omp parallel for
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {

            int sum = 0;
            for (int k = std::max(0, i - 1); k <= std::min(rows - 1, i + 1); ++k) {
                for (int l = std::max(0, j - 1); l <= std::min(cols - 1, j + 1); ++l) {
                    sum += grid_(k, l);
                }
            }

            // apply rules
            if (grid_(i, j) == 1) {
                if (sum < 3 || sum > 4) {
                    new_grid(i, j) = 0;  // Underpopulation or Overpopulation
                } else {
                    new_grid(i, j) = 1;  // Lives on to the next generation
                }
            } else {
                if (sum == 3) {
                    new_grid(i, j) = 1;  // Reproduction
                }
            }
        }
    }

    // current grid is updated
    grid_ = std::move(new_grid);
}

void GameOfLife::next(int numSteps){
    for (int i = 0 ; i < numSteps ; ++i) {
        this->next();
    }
}

void GameOfLife::setPattern(int rOffset, int cOffset, const Eigen::MatrixXi& pattern) {
    // get dimension
    int cols = pattern.cols();
    int rows = pattern.rows();

    // assert no overflow
    if (cOffset + cols > grid_.cols()){

        throw std::runtime_error("Figure is overflowing");
    }
    if (rOffset + rows > grid_.rows()){
        throw std::runtime_error("Figure is overflowing");
    }

    // set the pattern
    for (int i = 0 ; i < rows ; ++i) {
        for (int j = 0 ; j < cols ; ++j) {
            grid_(i + rOffset, j + cOffset) = pattern(i, j);
        }
    }
}