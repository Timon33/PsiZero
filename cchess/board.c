#include <Python.h>
#include "structmember.h"

#include <stdbool.h>

#include "cchess/board.h"
#include "cchess/bitboard.h"

#define PIECE_COUNT 12 // there are 12 unique pieces in chess, 6 for each side

// defines the board as a python type
// the interface to python

typedef unsigned char square;

// the custom python object
struct Board {
    PyObject_HEAD // boilerplate for python objects
    Bitboard bitboard[PIECE_COUNT]; // one bitboard for each unique piece type

    bool to_move;
    bool wccl; // white can castle long
    bool wccs; // white can castle short
    bool bccl; // black can castle long
    bool bccs; // black can castle short

    square en_passant;

    int half_moves;
};

// __new__
static PyObject *Board_new(PyTypeObject *type, PyObject *args)
{
    Board *self;
    self = (Board *) type->tp_alloc(type, 0); // allocate the new object of type board

    return (PyObject *) self;
}

// __init__
static int Board_init(Board *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"to_move", "wccl", "wccs", "bccl", "bccs", NULL};

    if(!PyArg_ParseTupleAndKeywords(args, kwds, "|ppppp", kwlist, &self->to_move, &self->wccl, &self->wccs, &self->bccl, &self->bccs))
    {
        return -1;
    }

    return 0;
}

// members of custom Board type
static PyMemberDef Board_members[] = {
    {"to_move", T_BOOL, offsetof(Board, to_move), 0, "to move"},
    {"wccl", T_BOOL, offsetof(Board, wccl), 0, "white can castle long"},
    {"wccs", T_BOOL, offsetof(Board, wccs), 0, "white can castle short"},
    {"bccl", T_BOOL, offsetof(Board, bccl), 0, "black can castle long"},
    {"bccs", T_BOOL, offsetof(Board, bccs), 0, "black can castle short"},
    {NULL} // Sentinel
};

// methods of custom Board type
static PyMethodDef Board_methods[] = {
    {NULL} // Sentinel
};

// the Board type
PyTypeObject BoardType = {
    PyVarObject_HEAD_INIT(NULL, 0) // boilerplate
    .tp_name = "cchess.Board",
    .tp_doc = "cchess Board object",
    .tp_basicsize = sizeof(Board),
    .tp_itemsize = 0, // no dynamic size change
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = Board_new, // __new__
    .tp_init = (initproc) Board_init, // __init__
    .tp_members = Board_members,
    .tp_methods = Board_methods,
};
