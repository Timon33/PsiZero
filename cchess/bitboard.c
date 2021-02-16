#include <Python.h>

#include <stdint.h>
#include <stdio.h>

#include "cchess/board.h"
#include "cchess/bitboard.h"

enum piece_type {
    pawn = 0x0 << 1,
    rook = 0x1 << 1,
    bishop = 0x2 << 1,
    knight = 0x3 << 1,
    queen = 0x4 << 1,
    king = 0x5 << 1
};

enum piece_color {
    black = 0x0,
    white = 0x1
};

// logical AND bitboards
Bitboard combine_bitboards(Bitboard *bitboards, int length)
{
    Bitboard combined;
    for(int i = 0; i < length; i++)
    {
        combined &= bitboards[i];
    }
    return combined;
}