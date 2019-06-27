%module libstockwell

%{
  #define SWIG_FILE_WITH_INIT
  #include "stockwell.h"
%}

%include "typemaps.i"
%include "carrays.i"
%include "numpy.i"

%init %{
  import_array();
%}

%array_class(double, doubleArray);

%include "stockwell.h"
