

colormap = {True:1, False:-1}
colorpitch = {True:"black", False:"white"}

getNext = {"top": lambda x, y: (x, y - 1) ,
           "bottom": lambda x, y: (x, y + 1),
           "left": lambda x, y: (x -1, y),
           "right": lambda x, y: (x + 1, y),
           "topright": lambda x, y: (x + 1, y - 1),
           "topleft": lambda x, y: (x - 1, y - 1),
           "bottomright": lambda x, y: (x + 1, y + 1),
           "bottomleft": lambda x, y: (x - 1, y + 1)
           }

def countDirect(x, y, dirc, curVal, boardarray):
    if x < 0 or x >= boardarray.shape[0] or y < 0 or y >= boardarray.shape[1]:
        return 0

    if boardarray[x,y] != curVal:
        return 0

    next = getNext[dirc](x, y)

    return 1 + countDirect(next[0], next[1], dirc, curVal, boardarray)


def check(x, y, boardarray):
    curVal = boardarray[x, y]

    if (countDirect(x,y,"top",curVal, boardarray) + countDirect(x,y,"bottom",curVal, boardarray) > 5) or \
       (countDirect(x,y,"left",curVal, boardarray) + countDirect(x,y,"right",curVal, boardarray) > 5) or \
       (countDirect(x,y,"topleft",curVal, boardarray) + countDirect(x,y,"bottomright",curVal, boardarray) > 5) or \
       (countDirect(x,y,"topright",curVal, boardarray) + countDirect(x,y,"bottomleft",curVal, boardarray) > 5):
        return x, y
    else:
        return None



