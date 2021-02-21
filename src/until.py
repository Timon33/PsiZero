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
            print(f"| {'+' if (bitboard >> y * 8 + x) & 1 else ' '} ", end="")
        print("|")
        print(" " * 3 + "|   " * 8 + "|")
    print(" " * 3 + line)


def show_pos(position: surge.Position):
    print(chess.Board(position.fen()))


pos = surge.Position()
pos.reset()

while True:
    try:
        show_pos(pos)
        for m in pos.legals():
            print(m)
        move = surge.Move(input("move: "))
        pos.play(move)

    except KeyboardInterrupt:
        break
