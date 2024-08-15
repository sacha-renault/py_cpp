#pragma once
#include <pybind11/eigen.h>
#include <Eigen/Dense>

class GameOfLife {
private:
    Eigen::MatrixXi grid_;
    int step_;
public:
    GameOfLife(int x, int y) : grid_(Eigen::MatrixXi::Zero(x, y)), step_(0) { }
    GameOfLife(int size) : GameOfLife(size, size) { }

    // getter & setter
    const Eigen::MatrixXi& getGrid() const { return  grid_; }
    int getStep() const { return step_; }
    void setAtIndex(int x, int y, int value) { grid_(x, y) = value; }
    void setPattern(int xOffset, int yOffset, const Eigen::MatrixXi& pattern);

    // functional
    void next();
    void next(int numSteps);
};