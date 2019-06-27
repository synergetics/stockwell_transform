#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <fftw3.h>
#include <arrayobject.h>

static char *Wisfile = NULL;
static char *Wistemplate = "%s/.fftwis";
#define WISLEN 8

static void set_wisfile(void)
{
    char *home;

    if (Wisfile) return;
    home = getenv("HOME");
    Wisfile = (char *)malloc(strlen(home) + WISLEN + 1);
    sprintf(Wisfile, Wistemplate, home);
}

/* Convert frequencies in Hz into rows of the ST, given sampling rate and length. */

/* This isn't wrapped. Just do it in Python. */
#if 0
static int st_freq(double f, int len, double srate)
{
    return floor(f * len / srate + .5);
}
#endif

/* This is the Fourier Transform of a Gaussian. */

static double gauss(int n, int m)
{
    return exp(-2. * M_PI * M_PI * m * m / (n * n));
}

/* Stockwell transform of the real array data. The len argument is the
number of time points, and it need not be a power of two. The lo and hi
arguments specify the range of frequencies to return, in Hz. If they are
both zero, they default to lo = 0 and hi = len / 2. The result is
returned in the complex array result, which must be preallocated, with
n rows and len columns, where n is hi - lo + 1. For the default values of
lo and hi, n is len / 2 + 1. */

static void st(int len, int lo, int hi, double *data, double *result)
{
    int i, k, n, l2;
    double s, *p;
    FILE *wisdom;
    static int planlen = 0;
    static double *g;
    static fftw_plan p1, p2;
    static fftw_complex *h, *H, *G;

    /* Check for frequency defaults. */

    if (lo == 0 && hi == 0) {
        hi = len / 2;
    }

    /* Keep the arrays and plans around from last time, since this
    is a very common case. Reallocate them if they change. */

    if (len != planlen && planlen > 0) {
        fftw_destroy_plan(p1);
        fftw_destroy_plan(p2);
        fftw_free(h);
        fftw_free(H);
        fftw_free(G);
        free(g);
        planlen = 0;
    }

    if (planlen == 0) {
        planlen = len;
        h = fftw_malloc(sizeof(fftw_complex) * len);
        H = fftw_malloc(sizeof(fftw_complex) * len);
        G = fftw_malloc(sizeof(fftw_complex) * len);
        g = (double *)malloc(sizeof(double) * len);

        /* Get any accumulated wisdom. */

        set_wisfile();
        wisdom = fopen(Wisfile, "r");
        if (wisdom) {
            fftw_import_wisdom_from_file(wisdom);
            fclose(wisdom);
        }

        /* Set up the fftw plans. */

        p1 = fftw_plan_dft_1d(len, h, H, FFTW_FORWARD, FFTW_MEASURE);
        p2 = fftw_plan_dft_1d(len, G, h, FFTW_BACKWARD, FFTW_MEASURE);

        /* Save the wisdom. */

        wisdom = fopen(Wisfile, "w");
        if (wisdom) {
            fftw_export_wisdom_to_file(wisdom);
            fclose(wisdom);
        }
    }

    /* Convert the input to complex. Also compute the mean. */

    s = 0.;
    memset(h, 0, sizeof(fftw_complex) * len);
    for (i = 0; i < len; i++) {
        h[i][0] = data[i];
        s += data[i];
    }
    s /= len;

    /* FFT. */

    fftw_execute(p1); /* h -> H */

    /* Hilbert transform. The upper half-circle gets multiplied by
    two, and the lower half-circle gets set to zero.  The real axis
    is left alone. */

    l2 = (len + 1) / 2;
    for (i = 1; i < l2; i++) {
        H[i][0] *= 2.;
        H[i][1] *= 2.;
    }
    l2 = len / 2 + 1;
    for (i = l2; i < len; i++) {
        H[i][0] = 0.;
        H[i][1] = 0.;
    }

    /* Fill in rows of the result. */

    p = result;

    /* The row for lo == 0 contains the mean. */

    n = lo;
    if (n == 0) {
        for (i = 0; i < len; i++) {
            *p++ = s;
            *p++ = 0.;
        }
        n++;
    }

    /* Subsequent rows contain the inverse FFT of the spectrum
    multiplied with the FFT of scaled gaussians. */

    while (n <= hi) {

        /* Scale the FFT of the gaussian. Negative frequencies
        wrap around. */

        g[0] = gauss(n, 0);
        l2 = len / 2 + 1;
        for (i = 1; i < l2; i++) {
            g[i] = g[len - i] = gauss(n, i);
        }

        for (i = 0; i < len; i++) {
            s = g[i];
            k = n + i;
            if (k >= len) k -= len;
            G[i][0] = H[k][0] * s;
            G[i][1] = H[k][1] * s;
        }

        /* Inverse FFT the result to get the next row. */

        fftw_execute(p2); /* G -> h */
        for (i = 0; i < len; i++) {
            *p++ = h[i][0] / len;
            *p++ = h[i][1] / len;
        }

        /* Go to the next row. */

        n++;
    }
}

/* Inverse Stockwell transform. */

static void ist(int len, int lo, int hi, double *data, double *result)
{
    int i, n, l2;
    double *p;
    FILE *wisdom;
    static int planlen = 0;
    static fftw_plan p2;
    static fftw_complex *h, *H;

    /* Check for frequency defaults. */

    if (lo == 0 && hi == 0) {
        hi = len / 2;
    }

    /* Keep the arrays and plans around from last time, since this
    is a very common case. Reallocate them if they change. */

    if (len != planlen && planlen > 0) {
        fftw_destroy_plan(p2);
        fftw_free(h);
        fftw_free(H);
        planlen = 0;
    }

    if (planlen == 0) {
        planlen = len;
        h = fftw_malloc(sizeof(fftw_complex) * len);
        H = fftw_malloc(sizeof(fftw_complex) * len);

        /* Get any accumulated wisdom. */

        set_wisfile();
        wisdom = fopen(Wisfile, "r");
        if (wisdom) {
            fftw_import_wisdom_from_file(wisdom);
            fclose(wisdom);
        }

        /* Set up the fftw plans. */

        p2 = fftw_plan_dft_1d(len, H, h, FFTW_BACKWARD, FFTW_MEASURE);

        /* Save the wisdom. */

        wisdom = fopen(Wisfile, "w");
        if (wisdom) {
            fftw_export_wisdom_to_file(wisdom);
            fclose(wisdom);
        }
    }

    /* Sum the complex array across time. */

    memset(H, 0, sizeof(fftw_complex) * len);
    p = data;
    for (n = lo; n <= hi; n++) {
        for (i = 0; i < len; i++) {
            H[n][0] += *p++;
            H[n][1] += *p++;
        }
    }

    /* Invert the Hilbert transform. */

    l2 = (len + 1) / 2;
    for (i = 1; i < l2; i++) {
        H[i][0] /= 2.;
        H[i][1] /= 2.;
    }
    l2 = len / 2 + 1;
    for (i = l2; i < len; i++) {
        H[i][0] = H[len - i][0];
        H[i][1] = -H[len - i][1];
    }

    /* Inverse FFT. */

    fftw_execute(p2); /* H -> h */
    p = result;
    for (i = 0; i < len; i++) {
        *p++ = h[i][0] / len;
    }
}

/* This does just the Hilbert transform. */

static void hilbert(int len, double *data, double *result)
{
    int i, l2;
    double *p;
    FILE *wisdom;
    static int planlen = 0;
    static fftw_plan p1, p2;
    static fftw_complex *h, *H;

    /* Keep the arrays and plans around from last time, since this
    is a very common case. Reallocate them if they change. */

    if (len != planlen && planlen > 0) {
        fftw_destroy_plan(p1);
        fftw_destroy_plan(p2);
        fftw_free(h);
        fftw_free(H);
        planlen = 0;
    }

    if (planlen == 0) {
        planlen = len;
        h = fftw_malloc(sizeof(fftw_complex) * len);
        H = fftw_malloc(sizeof(fftw_complex) * len);

        /* Get any accumulated wisdom. */

        set_wisfile();
        wisdom = fopen(Wisfile, "r");
        if (wisdom) {
            fftw_import_wisdom_from_file(wisdom);
            fclose(wisdom);
        }

        /* Set up the fftw plans. */

        p1 = fftw_plan_dft_1d(len, h, H, FFTW_FORWARD, FFTW_MEASURE);
        p2 = fftw_plan_dft_1d(len, H, h, FFTW_BACKWARD, FFTW_MEASURE);

        /* Save the wisdom. */

        wisdom = fopen(Wisfile, "w");
        if (wisdom) {
            fftw_export_wisdom_to_file(wisdom);
            fclose(wisdom);
        }
    }

    /* Convert the input to complex. */

    memset(h, 0, sizeof(fftw_complex) * len);
    for (i = 0; i < len; i++) {
        h[i][0] = data[i];
    }

    /* FFT. */

    fftw_execute(p1); /* h -> H */

    /* Hilbert transform. The upper half-circle gets multiplied by
    two, and the lower half-circle gets set to zero.  The real axis
    is left alone. */

    l2 = (len + 1) / 2;
    for (i = 1; i < l2; i++) {
        H[i][0] *= 2.;
        H[i][1] *= 2.;
    }
    l2 = len / 2 + 1;
    for (i = l2; i < len; i++) {
        H[i][0] = 0.;
        H[i][1] = 0.;
    }

    /* Inverse FFT. */

    fftw_execute(p2); /* H -> h */

    /* Fill in the rows of the result. */

    p = result;
    for (i = 0; i < len; i++) {
        *p++ = h[i][0] / len;
        *p++ = h[i][1] / len;
    }
}

/* Plain old FFT. */

static void fft(int len, double *data, double *result)
{
    int i;
    double *d;
    FILE *wisdom;
    static int planlen = 0;
    static fftw_plan p;
    static fftw_complex *x, *X;

    /* Keep the arrays and plan around from last time, since this
    is a very common case. Reallocate them if they change. */

    if (len != planlen && planlen > 0) {
        fftw_destroy_plan(p);
        fftw_free(x);
        fftw_free(X);
        planlen = 0;
    }

    if (planlen == 0) {
        planlen = len;
        x = fftw_malloc(sizeof(fftw_complex) * len);
        X = fftw_malloc(sizeof(fftw_complex) * len);

        /* Get any accumulated wisdom. */

        set_wisfile();
        wisdom = fopen(Wisfile, "r");
        if (wisdom) {
            fftw_import_wisdom_from_file(wisdom);
            fclose(wisdom);
        }

        /* Set up the fftw plan. */

        p = fftw_plan_dft_1d(len, x, X, FFTW_FORWARD, FFTW_MEASURE);

        /* Save the wisdom. */

        wisdom = fopen(Wisfile, "w");
        if (wisdom) {
            fftw_export_wisdom_to_file(wisdom);
            fclose(wisdom);
        }
    }

    /* Convert the input to complex. */

    memset(x, 0, sizeof(fftw_complex) * len);
    for (i = 0; i < len; i++) {
        x[i][0] = data[i];
    }

    /* FFT. */

    fftw_execute(p); /* x -> X */

    /* Return the complex result. */

    d = result;
    for (i = 0; i < len; i++) {
        *d++ = X[i][0];
        *d++ = X[i][1];
    }
}

/* Plain old inverse FFT. */

static void ifft(int len, double *data, double *result)
{
    int i;
    double *d;
    FILE *wisdom;
    static int planlen = 0;
    static fftw_plan p;
    static fftw_complex *x, *X;

    /* Keep the arrays and plan around from last time, since this
    is a very common case. Reallocate them if they change. */

    if (len != planlen && planlen > 0) {
        fftw_destroy_plan(p);
        fftw_free(x);
        fftw_free(X);
        planlen = 0;
    }

    if (planlen == 0) {
        planlen = len;
        x = fftw_malloc(sizeof(fftw_complex) * len);
        X = fftw_malloc(sizeof(fftw_complex) * len);

        /* Get any accumulated wisdom. */

        set_wisfile();
        wisdom = fopen(Wisfile, "r");
        if (wisdom) {
            fftw_import_wisdom_from_file(wisdom);
            fclose(wisdom);
        }

        /* Set up the fftw plan. */

        p = fftw_plan_dft_1d(len, X, x, FFTW_BACKWARD, FFTW_MEASURE);

        /* Save the wisdom. */

        wisdom = fopen(Wisfile, "w");
        if (wisdom) {
            fftw_export_wisdom_to_file(wisdom);
            fclose(wisdom);
        }
    }

    /* Copy the input. */

    d = data;
    for (i = 0; i < len; i++) {
        X[i][0] = *d++;
        X[i][1] = *d++;
    }

    /* Inverse FFT. */

    fftw_execute(p); /* X -> x */

    /* Return the complex result. */

    d = result;
    for (i = 0; i < len; i++) {
        *d++ = x[i][0];
        *d++ = x[i][1];
    }
}

/* Python wrapper code. */

static char Doc_st[] =
"st(x[, lo, hi]) returns the 2d, complex Stockwell transform of the real\n\
array x. If lo and hi are specified, only those frequencies (rows) are\n\
returned; lo and hi default to 0 and n/2, resp., where n is the length of x.";

static PyObject *st_wrap(PyObject *self, PyObject *args)
{
    int n;
    int lo = 0;
    int hi = 0;
    npy_intp dim[2];
    PyObject *o;
    PyArrayObject *a, *r;

    if (!PyArg_ParseTuple(args, "O|ii", &o, &lo, &hi)) {
        return NULL;
    }

    a = (PyArrayObject *)PyArray_ContiguousFromAny(o, NPY_DOUBLE, 1, 1);
    if (a == NULL) {
        return NULL;
    }
    n = PyArray_DIM(a, 0);

    if (lo == 0 && hi == 0) {
        hi = n / 2;
    }

    dim[0] = hi - lo + 1;
    dim[1] = n;
    r = (PyArrayObject *)PyArray_SimpleNew(2, dim, NPY_CDOUBLE);
    if (r == NULL) {
        Py_DECREF(a);
        return NULL;
    }

    st(n, lo, hi, (double *)PyArray_DATA(a), (double *)PyArray_DATA(r));

    Py_DECREF(a);
    return PyArray_Return(r);
}

static char Doc_ist[] =
"ist(y[, lo, hi]) returns the inverse Stockwell transform of the 2d, complex\n\
array y.";

static PyObject *ist_wrap(PyObject *self, PyObject *args)
{
    int n, m;
    int lo = 0;
    int hi = 0;
    npy_intp dim[1];
    PyObject *o;
    PyArrayObject *a, *r;

    if (!PyArg_ParseTuple(args, "O|ii", &o, &lo, &hi)) {
        return NULL;
    }

    a = (PyArrayObject *)PyArray_ContiguousFromAny(o, NPY_CDOUBLE, 2, 2);
    if (a == NULL) {
        return NULL;
    }
    n = PyArray_DIM(a, 0);
    m = PyArray_DIM(a, 1);

    if (lo == 0 && hi == 0) {
        hi = m / 2;
    }
    if (hi - lo + 1 != n) {
        PyErr_SetString(PyExc_ValueError, "inconsistent dimensions in ist()");
        Py_DECREF(a);
        return NULL;
    }

    dim[0] = m;
    r = (PyArrayObject *)PyArray_SimpleNew(1, dim, NPY_DOUBLE);
    if (r == NULL) {
        Py_DECREF(a);
        return NULL;
    }

    ist(m, lo, hi, (double *)PyArray_DATA(a), (double *)PyArray_DATA(r));

    Py_DECREF(a);
    return PyArray_Return(r);
}

static char Doc_hilbert[] =
"hilbert(x) returns the complex Hilbert transform of the real array x.";

static PyObject *hilbert_wrap(PyObject *self, PyObject *args)
{
    int n;
    npy_intp dim[1];
    PyObject *o;
    PyArrayObject *a, *r;

    if (!PyArg_ParseTuple(args, "O", &o)) {
        return NULL;
    }

    a = (PyArrayObject *)PyArray_ContiguousFromAny(o, NPY_DOUBLE, 1, 1);
    if (a == NULL) {
        return NULL;
    }
    n = PyArray_DIM(a, 0);

    dim[0] = n;
    r = (PyArrayObject *)PyArray_SimpleNew(1, dim, NPY_CDOUBLE);
    if (r == NULL) {
        Py_DECREF(a);
        return NULL;
    }

    hilbert(n, (double *)PyArray_DATA(a), (double *)PyArray_DATA(r));

    Py_DECREF(a);
    return PyArray_Return(r);
}

static char Doc_fft[] =
"fft(x) returns the complex Fourier transform of the real array x.";

static PyObject *fft_wrap(PyObject *self, PyObject *args)
{
    int n;
    npy_intp dim[1];
    PyObject *o;
    PyArrayObject *a, *r;

    if (!PyArg_ParseTuple(args, "O", &o)) {
        return NULL;
    }

    a = (PyArrayObject *)PyArray_ContiguousFromAny(o, NPY_DOUBLE, 1, 1);
    if (a == NULL) {
        return NULL;
    }
    n = PyArray_DIM(a, 0);

    dim[0] = n;
    r = (PyArrayObject *)PyArray_SimpleNew(1, dim, NPY_CDOUBLE);
    if (r == NULL) {
        Py_DECREF(a);
        return NULL;
    }

    fft(n, (double *)PyArray_DATA(a), (double *)PyArray_DATA(r));

    Py_DECREF(a);
    return PyArray_Return(r);
}

static char Doc_ifft[] =
"ifft(x) returns the complex inverse Fourier transform of the real array x.";

static PyObject *ifft_wrap(PyObject *self, PyObject *args)
{
    int n;
    npy_intp dim[1];
    PyObject *o;
    PyArrayObject *a, *r;

    if (!PyArg_ParseTuple(args, "O", &o)) {
        return NULL;
    }

    a = (PyArrayObject *)PyArray_ContiguousFromAny(o, NPY_DOUBLE, 1, 1);
    if (a == NULL) {
        return NULL;
    }
    n = PyArray_DIM(a, 0);

    dim[0] = n;
    r = (PyArrayObject *)PyArray_SimpleNew(1, dim, NPY_CDOUBLE);
    if (r == NULL) {
        Py_DECREF(a);
        return NULL;
    }

    ifft(n, (double *)PyArray_DATA(a), (double *)PyArray_DATA(r));

    Py_DECREF(a);
    return PyArray_Return(r);
}

static char Doc_stmod[] =
"Stockwell and inverse Stockwell transforms of 1D time-series data.\n\
Regular FFT, inverse FFT, and Hilbert transforms are also included.";

static PyMethodDef Methods[] = {
    { "st", st_wrap, METH_VARARGS, Doc_st },
    { "ist", ist_wrap, METH_VARARGS, Doc_ist },
    { "hilbert", hilbert_wrap, METH_VARARGS, Doc_hilbert },
    { "fft", fft_wrap, METH_VARARGS, Doc_fft },
    { "ifft", ifft_wrap, METH_VARARGS, Doc_ifft },
    { NULL, NULL, 0, NULL }
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "st",
    Doc_stmod,
    -1,
    Methods,
    NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit_st(void)
{
    PyObject *m;

    m = PyModule_Create(&moduledef);
    if (m == NULL) {
        return NULL;
    }

    import_array();

    return m;
}

#else

PyMODINIT_FUNC initst()
{
    Py_InitModule3("st", Methods, Doc_stmod);
    import_array();
}

#endif
