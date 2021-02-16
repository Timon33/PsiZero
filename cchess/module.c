#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "cchess/board.h"

static PyModuleDef cchessmodule = {
    PyModuleDef_HEAD_INIT,
    "cchess",
    "Bitboard Chess C module",
    -1,
};

PyMODINIT_FUNC PyInit_cchess(void)
{
    PyObject *module;
    if (PyType_Ready(&BoardType) < 0)
    {
        return NULL;
    }

    module = PyModule_Create(&cchessmodule);
    if (module == NULL)
    {
        return NULL;
    }

    Py_INCREF(&BoardType);
    if (PyModule_AddObject(module, "Board", (PyObject *) &BoardType) < 0)
    {
        Py_DECREF(&BoardType);
        Py_DECREF(module);
        return NULL;
    }

    return module;
}