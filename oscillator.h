// File: oscillator.h
//
// Recursive Oscillator.
//
#include <stdio.h>
#include <math.h>

class Oscillate {
  public:
    void wavesine (double *arr1, std::size_t fs1, float f1);
    void wavesquare (double *arr2, std::size_t fs2, float f2, float duty);
};
