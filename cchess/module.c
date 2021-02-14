#define PY_SSIZE_T_CLEAN
#include <Python.h>



static PyMethodDef ChessMethods[] = {
    {"fputs", method_fputs, METH_VARARGS, "Python interface for fputs C library function"}
};

static struct PyModuleDef cchessmodule = {
    PyModuleDef_HEAD_INIT,
    "cchess",
    "Bitboard Chess C module",
    -1,
    ChessMethods
};

PyMODINIT_FUNC PyInit_cchess(void) {
    return PyModule_Create(&cchessmodule);
}