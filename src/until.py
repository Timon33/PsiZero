import surge
import chess

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


def show_pos(position: surge.Position):
    print(chess.Board(position.fen()))


surge.init()
pos = surge.Position()
pos.reset(pos)

print("len", len(pos.legals()))
for m in pos.legals():
    pos.play(m)
    
    print(pos.fen())
    # show_pos(pos)
    pos.undo(m)
