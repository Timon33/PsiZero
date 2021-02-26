import surge
import torch
import torch.nn as nn
import numpy as np
from enum import Flag, Enum
import logging

import neuralnet
import util


class Color(Flag):
    WHITE = False
    BLACK = True


class EndState:
    WHITE_MATE = float("-inf")  # white is checkmate
    BLACK_MATE = float("inf")  # black is checkmate
    DRAW = float(0)


LR = 0.001
TIME_TRSH = 1
TIME_PER_MOVE = 0
DEPTH = 1

training_data = {}


def side_from_pos(pos):
    return Color(pos.color_to_play() != 0)


def pos_2_tensor(pos: surge.Position) -> torch.tensor:
    bit_state = pos.bit_state()
    bits = np.unpackbits(bit_state.view(np.uint8))
    return torch.tensor(bits).float()


# gives a position a score from -1 to 1 (Black - White) and if the game is over
def score(pos: surge.Position, model) -> (float, bool):

    moves = pos.legals()
    side = side_from_pos(pos)
    if len(moves) == 0:
        # no more moves for the side -> end of game
        if pos.in_check():
            # checkmate
            return (EndState.WHITE_MATE, True) if side == Color.WHITE else (EndState.BLACK_MATE, True)
        else:
            # stalemate
            return EndState.DRAW, True

    # return model.forward(pos_2_tensor(pos)).float(), False
    type_value = [1, 3, 3, 5, 9, 50, 0, 0, -1, -3, -3, -5, -9, -50, 0]
    bit_state = pos.bit_state()
    score = 0
    for type, bits in enumerate(bit_state):
        score += bin(bits).count("1") * type_value[type]
    return score, False


def play(pos: surge.Position, model: neuralnet.NN, side: Color, time: float, depth):
    taps = "\t" * (DEPTH - depth)
    logging.debug(f"{taps}-------------------------------------------------")
    logging.debug(f"{taps}exploring pos with depth {depth} for side {side}:")
    util.pprint_pos(pos, logging.DEBUG)

    # generate the moves
    moves = pos.legals()
    # best_series = []

    scores = np.array([float(0)] * len(moves))
    is_game_over = [False] * len(moves)

    # eval all the possible moves
    for i, move in enumerate(moves):
        pos.play(move)
        # eval the new pos and store the result
        scores[i], is_game_over[i] = score(pos, model)
        pos.undo(move)

    if depth > 0:

        # if there is time left split it proportional to the positions score and search deeper
        '''if scores.sum() != 0:
            norm = (scores + np.min(scores)) / np.sum(np.abs(scores))
        else:
            norm = np.array([1 / len(moves)] * len(moves))'''

        best_move = None
        best_max = 0

        # best = [[]] * len(moves)

        # recursively explore all subtrees and update the scores
        for i, move in enumerate(moves):
            logging.debug(f"{taps}exploring move {move}")

            if is_game_over[i]:
                logging.debug("CHECKMATE --- SKIPING")
                continue

            pos.play(move)
            scores[i], is_game_over[i], _ = play(pos, model, Color(not side.value), time, depth - 1)
            pos.undo(move)

    logging.debug(f"{taps}scores: {scores}")

    # min max the results
    if side == Color.WHITE:
        # white will play the move that gives the max score
        logging.debug(f"{taps}best found. max: {np.max(scores)}, best: {moves[np.argmax(scores)]}")
        return np.max(scores), is_game_over[np.argmax(scores)], moves[np.argmax(scores)]
    else:
        # black will play the move that gives the min score
        logging.debug(f"{taps}best found. min: {np.min(scores)}, best: {moves[np.argmin(scores)]}")
        return np.min(scores), is_game_over[np.argmin(scores)], moves[np.argmax(scores)]


def train():
    pos = surge.Position()
    surge.Position.set("k7/2K5/8/8/8/8/8/1PR5 w - - 0 1", pos)

    model = neuralnet.NN()
    loss_function = nn.MSELoss()
    optim = torch.optim.SGD(model.parameters(), lr=0.001)

    # print(play(pos, model, Color(pos.color_to_play() != 0), 0, 2))
    # return
    game_over = False

    while True:
        pos_score, game_over, best_move = play(pos, model, side_from_pos(pos), 0, DEPTH)
        logging.warning(f"score {pos_score}, move: {best_move}")

        if game_over:
            break

        pos.play(best_move)
        util.pprint_pos(pos, logging.WARNING)

    logging.error(f"game over: {pos_score}")
    util.pprint_pos(pos, logging.ERROR)gftr 


def init():
    surge.init()
    logging.basicConfig(level=logging.INFO, format="")
    train()


if __name__ == "__main__":
    init()
