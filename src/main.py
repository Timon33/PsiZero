import chess
import torch
import numpy as np
import logging
import pickle
import os

import neuralnet
import util


# return the score of the position - black, + white and if the game is over
def eval_position(board: chess.Board, model: neuralnet.NN) -> (float, bool):
    
    # doesn't use is_game_over to get more performance

    if board.is_checkmate():
        # if white is checkmate black gets an -infinit score and inf for black in checkmate
        return (float("-inf"), True) if board.turn else (float("inf"), True)

    if board.is_stalemate() or board.is_insufficient_material():
        # 0 score for a draw
        return 0, True

    # if the game is not over evaluate the board using the nn
    return model.forward(util.board_2_tensor(board)), False
    # return static_material_eval(board), False

# stop exploring if the time unit for this branch fall below this threshold
TIME_TRSH = 1

# a tree search like minmax, but no alpha beta pruning. instead we eval each possition and allocate units of time depending on the score
def dynamic_move_search(board, model, time, is_maximizing) -> (float, chess.Move):

    # first, eval all next moves. this is used to allocate the time proportional later
    moves = list(board.generate_legal_moves())
    scores = np.empty(len(moves))
    gameovers = np.empty(len(moves), dtype=bool)

    for i, move in enumerate(moves):
            board.push(move)
            scores[i], gameovers[i] = eval_position(board, model)

            # if there is a checkmate for the opposide side, it will choose it and stop exploring
            if board.is_checkmate() and board.turn is not is_maximizing:
                board.pop()
                return scores[i], move

            board.pop()

    # if ther is no more time for this branch...
    if time < TIME_TRSH:
        # ...find the best move for the plaing side
        if is_maximizing:
            return np.max(scores), moves[np.argmax(scores)]
        else:
            return np.min(scores), moves[np.argmin(scores)]

    # if there still is time, allocate it proportional to the score and keep exploring
    if is_maximizing:
        scaled_scores = np.nan_to_num(scores) - np.min(scores) + 0.1
    else:
        scaled_scores = np.nan_to_num(-scores) - np.min(-scores) + 0.1
    time_factors = scaled_scores / np.sum(scaled_scores)


    if is_maximizing:
        for move, is_gameover, time_factor in zip(moves, gameovers, time_factors):
            if is_gameover:
                continue
            board.push(move)
            scores[i], _ = dynamic_move_search(board, model, time * time_factor, False)
            board.pop()

        # print("\t" * calls, scores, gameovers)
        return np.max(scores), moves[np.argmax(scores)]

    else:
        for move, is_gameover, time_factor in zip(moves, gameovers, time_factors):
            if is_gameover:
                continue
            board.push(move)
            scores[i], _ = dynamic_move_search(board, model, time * time_factor, True)
            board.pop()

        # print("\t" * calls, scores, gameovers)
        return np.min(scores), moves[np.argmin(scores)]

# plays a game against itself, return all positions form the game and the final score
def play_game(time: float, model: neuralnet.NN):
    b = chess.Board()
    positions = np.empty([0, 832])
    predictions = np.empty(832)

    game_over = False
    i = 0
    while not game_over:
        if i > 100:
            return positions, 0

        s, move = dynamic_move_search(b, model, time, b.turn)

        positions = np.append(positions, util.board_2_tensor(b))
        predictions[i] = s

        b.push(move)
        game_over = b.is_game_over()
        i += 1

    res = 0
    if b.is_checkmate():
        res = 1 if b.turn else -1
    
    return positions, predictions, res


def train(model, iters, time):

    loss_f = torch.nn.MSELoss(reduction="none")
    optim = torch.optim.SGD(model.parameters(), lr=0.001)

    try:
        for _ in range(iters):
            X, P, Y = play_game(time, model)
            model.zero_grad()
            loss = loss_f(P, torch.tensor(Y))
            loss.backward()
            optim.step()

            print(loss)

    except KeyboardInterrupt:
        with open(model_path, "wb") as f:
            pickle.dump(model, f)

project_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(project_dir, "../models/model")

with open(model_path, "rb") as f:
    model = pickle.load(f)

train(model, 100, 3)