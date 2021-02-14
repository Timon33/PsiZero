#include <Python.h>

static PyObject *method_echo(PyObject *self, PyObject *args) {
    char *echo = NULL;

    /* Parse arguments */
    if(!PyArg_ParseTuple(args, "s", &echo)) {
        return NULL;
    }

    return ;
}