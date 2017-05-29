from game import colormap, check
import random
import numpy as np


def evalFunc(boardarray, isBlack):
    pass

def isEnd(boardarray, preX, preY):
    return check(preX, preY, boardarray)

def getMoves(boardarray, isBlack):
    candidates = np.where(boardarray == 0)
    return zip(candidates[0], candidates[1])

class RandomPlay:

    def move(self, boardarray, isBlack):
        curVal = colormap[isBlack]
        candidates = np.where(boardarray == 0)
        nextMoves = zip(candidates[0], candidates[1])
        return random.choice(nextMoves)

class MinimaxPlayer:

    def __init__(self, eval = evalFunc):
        self.ef = eval

    def move(self, boardarray, isBlack, preX, preY, depth = 5):
        bestMove, score = self.minimax(boardarray, isBlack, preX, preY, depth)

    def minimax(self, boardarray, isBlack, preX, preY, depth = 5):
        return self.maximize(boardarray, isBlack, preX, preY, depth)

    def maximize(self, boardarray, isBlack, preX, preY, depth = 5):
        if isEnd(boardarray, preX, preY) or depth < 1:
            return None, self.ef(boardarray, isBlack)

        best_move, bestv = None, -float("inf")

        for move in getMoves(boardarray, isBlack):
            b = np.copy(boardarray)
            b[move[0], move[1]] = colormap[isBlack]
            _, val = self.minimize(b, not isBlack, move[0], move[1], depth - 1)
            if val > bestv:
                best_move = move
                bestv = val

        return best_move, bestv

    def minimize(self, boardarray, isBlack, preX, preY, depth = 5):
        if isEnd(boardarray, preX, preY) or depth < 1:
            return None, self.ef(boardarray, isBlack)

        best_move, bestv = None, float("inf")

        for move in getMoves(boardarray, isBlack):
            b = np.copy(boardarray)
            b[move[0], move[1]] = colormap[isBlack]
            _, val = self.maximize(b, not isBlack, move[0], move[1], depth - 1)
            if val < bestv:
                best_move = move
                bestv = val

        return best_move, bestv

