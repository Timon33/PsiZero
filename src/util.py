import surge
import chess
import torch
import logging
import numpy as np


def pprint_bitboard(bitboard):
    files = (" " * 3).join([c for c in "ABCDEFGH"])
    line = "---".join("+" * 9)
    print(" " * 5 + files)

    for y in range(8):
        print(" " * 3 + line)

        print(" " * 3 + "|   " * 8 + "|")
        print(f" {8 - y} ", end="")
        for x in range(8):
            print(f"| {'+' if (bitboard >> (7 - y) * 8 + x) & 1 else ' '} ", end="")
        print("|")
        print(" " * 3 + "|   " * 8 + "|")
    print(" " * 3 + line)


def pprint_pos(position: surge.Position, level):
    logging.log(level, chess.Board(position.fen()))


def perf(pos, depth):
    if depth <= 1:
        return len(pos.legals())

    n = 0
    for m in pos.legals():
        pos.play(m)
        n += perf(pos, depth - 1)
        pos.undo(m)

    return n

# convert a position to the tensor representation used by the nn
def board_2_tensor(board: chess.Board) -> torch.tensor:
    nums = np.empty(13, dtype=np.uint64)
    for i in range(6):
        nums[i] = int(board.pieces(i + 1, chess.WHITE))
        nums[i + 6] = int(board.pieces(i + 1, chess.BLACK))

    nums[12] = 1 << board.ep_square if board.has_legal_en_passant() else 0

    bits = np.unpackbits(nums.view(np.uint8))
    return torch.tensor(bits).float()

def moves_2_str(moves):
    s = ""
    for m in moves:
        s += str(m) + " "
    return s + "\n"


