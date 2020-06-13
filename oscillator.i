/* File: oscillator.i */
/* Name our python module */
%module oscillator

%include <std_string.i>
%include <math.i>

%{
   #define SWIG_FILE_WITH_INIT
   #include "oscillator.h"
%}


%include <numpy.i>
%init %{
import_array();
%}

%apply (double* ARGOUT_ARRAY1,int DIM1) {(double *arr1, std::size_t fs1)};
%apply (double* ARGOUT_ARRAY1,int DIM1) {(double *arr2, std::size_t fs2)};

%include "oscillator.h"

