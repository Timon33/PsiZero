from distutils.core import setup, Extension


def main():
    setup(name="cchess",
          version="1.0.0",
          description="Bitboard Chess C module",
          author="Timon",
          ext_modules=[
              Extension(
                  "cchess",
                  ["module.c", "board.c"],
                  include_dirs=["cchess"]
              )
          ])


if __name__ == "__main__":
    main()
