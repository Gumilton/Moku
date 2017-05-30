from game import colormap, check
import random
import numpy as np
import re

def array2str(nparray):
    return "".join(str(i) for i in nparray)


def evalFunc(boardarray, isBlack):
    curval = colormap[isBlack]
    b = np.copy(boardarray)

    result = {1:0, -1:0}

    coef5 = 100
    coef4 = 20
    coef3 = 4
    coef2 = 1

    p2 = "110{3}|0{1}110{2}|0{2}110{1}|0{3}11"
    p3 = "1110{2}|0{2}111"
    p4 = "0{1}1111|11110{1}|0{1}1110{1}"
    p5 = "11111|0{1}11110{1}"

    # count row
    for i in range(b.shape[0]):
        row = array2str(b[i])
        result[1] += coef5 * len(re.findall(p5, row)) + coef4 * len(re.findall(p4, row)) + \
                     coef3 * len(re.findall(p3, row)) + coef2 * len(re.findall(p2, row))

    # count column
    for i in range(b.shape[1]):
        row = array2str(b[:,i])
        result[1] += coef5 * len(re.findall(p5, row)) + coef4 * len(re.findall(p4, row)) + \
                     coef3 * len(re.findall(p3, row)) + coef2 * len(re.findall(p2, row))

    # count diagonal
    for i in range(b.shape[0]):
        row = array2str(b.diagonal(i)) + array2str(b.diagonal(i-b.shape[0]))
        result[1] += coef5 * len(re.findall(p5, row)) + coef4 * len(re.findall(p4, row)) + \
                         coef3 * len(re.findall(p3, row)) + coef2 * len(re.findall(p2, row))

    b = b.transpose()
    # count diagonal
    for i in range(b.shape[0]):
        row = array2str(b.diagonal(i)) + array2str(b.diagonal(i-b.shape[0]))
        result[1] += coef5 * len(re.findall(p5, row)) + coef4 * len(re.findall(p4, row)) + \
                         coef3 * len(re.findall(p3, row)) + coef2 * len(re.findall(p2, row))

    b = b * -1
    for i in range(b.shape[0]):
        row = array2str(b[i])
        result[-1] += coef5 * len(re.findall(p5, row)) + coef4 * len(re.findall(p4, row)) + \
                      coef3 * len(re.findall(p3, row)) + coef2 * len(re.findall(p2, row))

    for i in range(b.shape[1]):
        row = array2str(b[:,i])
        result[-1] += coef5 * len(re.findall(p5, row)) + coef4 * len(re.findall(p4, row)) + \
                      coef3 * len(re.findall(p3, row)) + coef2 * len(re.findall(p2, row))

    # count diagonal
    for i in range(b.shape[0]):
        row = array2str(b.diagonal(i)) + array2str(b.diagonal(i-b.shape[0]))
        result[-1] += coef5 * len(re.findall(p5, row)) + coef4 * len(re.findall(p4, row)) + \
                         coef3 * len(re.findall(p3, row)) + coef2 * len(re.findall(p2, row))
    b = b.transpose()
    # count diagonal
    for i in range(b.shape[0]):
        row = array2str(b.diagonal(i)) + array2str(b.diagonal(i-b.shape[0]))
        result[-1] += coef5 * len(re.findall(p5, row)) + coef4 * len(re.findall(p4, row)) + \
                         coef3 * len(re.findall(p3, row)) + coef2 * len(re.findall(p2, row))

    return result[curval] - result[-curval] * 2

def isEnd(boardarray, curX, curY):
    return check(curX, curY, boardarray)

def getMoves(boardarray, isBlack, depth):
    candidates = np.where(boardarray == 0)
    nextMoves = zip(candidates[0], candidates[1])
    d = max(0, depth-1)
    occupied = np.where(boardarray != 0)
    top = max(0, np.min(occupied[0]) - d)
    down = min(boardarray.shape[0], np.max(occupied[0]) + d)
    left = max(0, np.min(occupied[1]) - d)
    right = min(boardarray.shape[1], np.max(occupied[1]) + d)

    # print("search bound in: ", left, right, top, down)

    return [m for m in nextMoves if left <= m[0] <= right and top <= m[1] <= down]

class RandomPlay:

    def move(self, boardarray, isBlack):
        curVal = colormap[isBlack]
        candidates = np.where(boardarray == 0)
        nextMoves = zip(candidates[0], candidates[1])
        return random.choice(nextMoves)

    def randomStart(self, boardarray):
        size = boardarray.shape[0]//3
        x = random.randrange(size, size*2)
        return x,x

class MinimaxPlayer:

    def __init__(self, eval = evalFunc):
        self.ef = eval

    """
        take in opponent's move preX and preY, return best move strategy
    """
    def move(self, boardarray, isBlack, preX, preY, depth = 2):
        return self.minimax(boardarray, isBlack, preX, preY, depth)

    def minimax(self, boardarray, isBlack, preX, preY, depth = 2):
        print "begin minimax"
        return self.maximize(boardarray, isBlack, preX, preY, depth)

    def maximize(self, boardarray, isBlack, preX, preY, depth = 2):
        if isEnd(boardarray, preX, preY) or depth < 1:
            v = self.ef(boardarray, isBlack)
            # print("End max:", v)
            return None, v

        best_move, bestv = None, -float("inf")

        available_moves = getMoves(boardarray, isBlack, depth)
        print("max:", len(available_moves))
        for move in available_moves:
            b = np.copy(boardarray)
            b[move[0], move[1]] = colormap[isBlack]
            _, val = self.minimize(b, not isBlack, move[0], move[1], depth - 1)
            if val > bestv:
                best_move = move
                bestv = val

        # print("max:", best_move, bestv)
        return best_move, bestv

    def minimize(self, boardarray, isBlack, preX, preY, depth = 2):
        if isEnd(boardarray, preX, preY) or depth < 1:
            v = self.ef(boardarray, isBlack)
            # print("End min:", v)
            return None, v

        best_move, bestv = None, float("inf")

        available_moves = getMoves(boardarray, isBlack, depth)
        print("min:", len(available_moves))
        for move in available_moves:
            b = np.copy(boardarray)
            b[move[0], move[1]] = colormap[isBlack]
            _, val = self.maximize(b, not isBlack, move[0], move[1], depth - 1)
            if val < bestv:
                best_move = move
                bestv = val


        # print("min:", best_move, bestv)
        return best_move, bestv

