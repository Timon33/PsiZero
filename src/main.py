import surge
import pickle
import torch
import torch.nn as nn
import numpy as np
from enum import Flag
import logging

import neuralnet
import util


class Color(Flag):
    WHITE = True
    BLACK = False


LR = 0.001
TIME_TRSH = 1

training_data = {}


def pos_2_tensor(pos: surge.Position) -> torch.tensor:
    bit_state = pos.bit_state()
    bits = np.unpackbits(bit_state.view(np.uint8))
    return torch.tensor(bits).float()


# gives a position a score from -1 to 1 (Black - White)
def score(pos: surge.Position) -> float:
    # return model.forward(pos_2_tensor(pos)).float()
    type_value = [1, 3, 3, 5, 9, 50, 0, 0, -1, -3, -3, -5, -9, -50, 0]
    bit_state = pos.bit_state()
    score = 0
    for type, bits in enumerate(bit_state):
        score += bin(bits).count("1") * type_value[type]
    return score


def play(pos: surge.Position, model: neuralnet.NN, side: Color, time: float):
    logging.debug(f"exploring pos with time {time} for side {side}:")
    # util.pprint_pos(pos)

    # generate the moves
    moves = pos.legals()
    best_series = []

    if len(moves) <= 0:
        # no more moves for the side -> end of game
        if pos.in_check():
            # checkmate
            logging.debug(f"{side} checkmate")
            return (-100, None) if side else (100, None)
        else:
            # stalemate
            return 0, None

    scores = np.array([0.0] * len(moves))

    # eval all the possible moves
    for i, move in enumerate(moves):
        pos.play(move)
        # eval the new pos and store the result
        scores[i] = score(pos)
        pos.undo(move)

    if time > TIME_TRSH:
        # if there is time left split it proportional to the positions score and search deeper
        if scores.sum() != 0:
            norm = scores / scores.sum()
        else:
            norm = np.array([1 / len(moves)] * len(moves))

        best_move = moves[0]
        best_max = 0

        best = [[]] * len(moves)

        # recursively explore all subtrees and update the scores
        for i, move in enumerate(moves):
            pos.play(move)
            scores[i], best[i] = play(pos, model, Color.BLACK if side else Color.WHITE, time * norm[i])
            pos.undo(move)

        if side:
            best_series = best[np.argmax(scores)]
        else:
            best_series = best[np.argmin(scores)]

    # min max the results
    if side:
        # white will play the move that gives the max score
        logging.debug(f"best found. max: {np.max(scores)}, best: {moves[np.argmax(scores)]}")
        best_series.insert(0, moves[np.argmax(scores)])
        return np.max(scores), best_series
    else:
        # black will play the move that gives the min score
        logging.debug(f"best found. max: {np.min(scores)}, best: {moves[np.argmin(scores)]}")
        best_series.insert(0, moves[np.argmin(scores)])
        return np.min(scores), best_series


def train():
    pos = surge.Position()
    pos.reset()

    print(score(pos))

    model = neuralnet.NN()
    loss_function = nn.MSELoss()
    optim = torch.optim.SGD(model.parameters(), lr=0.001)

    print(play(pos, model, Color.BLACK, 1000))


def init():
    surge.init()
    logging.basicConfig(level=logging.DEBUG, format="")
    train()


if __name__ == "__main__":
    init()
