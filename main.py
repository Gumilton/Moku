from tkinter import Frame, Canvas, Label, Button, LEFT, RIGHT, ALL, Tk
from random import randint
import numpy as np
from game import check, colorpitch, colormap
from player import RandomPlay, MinimaxPlayer

class main:

    def __init__(self, master):
        self.size = 30
        self.width = 720
        self.height = 720
        self.offset = self.width / (float(self.size)) / 2
        self.pitchsize = self.width / (float(self.size)) / 2.5

        self.frame = Frame(master)
        self.frame.pack(fill="both", expand=True)
        self.canvas = Canvas(self.frame, width=self.width, height=self.height)
        self.canvas.pack(fill="both", expand=True)
        self.frameb = Frame(self.frame)
        self.frameb.pack(fill="both", expand=True)
        self.dp = Button(self.frameb, text='Double Players', height=4, command=self.humanplay,
                             bg='white', fg='purple')
        self.dp.pack(fill="both", expand=True, side=RIGHT)
        self.ai1 = Button(self.frameb, text='Against AI (First)', height=4, command=self.playai1,
                             bg='purple', fg='white')
        self.ai1.pack(fill="both", expand=True, side=LEFT)
        self.ai2 = Button(self.frameb, text='Against AI (Second)', height=4, command=self.playai2,
                             bg='purple', fg='white')
        self.ai2.pack(fill="both", expand=True, side=LEFT)
        self.colormap = colormap
        self.colorpitch = colorpitch
        self.black = True
        self.board = np.asarray([[0] * self.size] * self.size)
        self.gameOver = False

    def drawBoard(self):
        for i in range(self.size):
            # draw horizontal
            self.canvas.create_line(0, i * self.canvas.winfo_height() / (float(self.size)) + self.offset,
                                    self.canvas.winfo_width(), i * self.canvas.winfo_height() / (float(self.size)) + self.offset)
            # draw vertical
            self.canvas.create_line(i * self.canvas.winfo_width() / (float(self.size)) + self.offset, 0,
                                    i * self.canvas.winfo_width() / (float(self.size)) + self.offset, self.canvas.winfo_height())

        # print boarder
        self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(), outline="black", width = 10)


    def playai1(self):
        self.canvas.delete(ALL)
        # self.canvas.bind("<ButtonPress-1>", self.human_move_against_AI)
        self.drawBoard()
        self.count = 0
        self.play_AI()

    def playai2(self):
        self.canvas.delete(ALL)
        self.drawBoard()
        count = 0
        self.canvas.bind("<ButtonPress-1>", self.hplayer)

    def humanplay(self):
        self.canvas.delete(ALL)
        self.drawBoard()
        self.canvas.bind("<ButtonPress-1>", self.hplayer)

    def end(self):
        self.canvas.unbind("<ButtonPress-1>")
        self.gameOver = True

    def hplayer(self, event):
        self.move(event.x, event.y)

    def moveByPixel(self, posX, posY):
        ind_input_X = posX // (self.width / self.size)
        ind_input_Y = posY // (self.width / self.size)
        return self.moveByIndex(ind_input_X, ind_input_Y)

    def moveByIndex(self, indX, indY):
        if self.board[indX,indY] == 0:
            drawX = indX * self.width / float(self.size) + self.offset * 1.1
            drawY = indY * self.width / float(self.size) + self.offset * 1.1
            self.board[indX, indY] = self.colormap[self.black]
            self.canvas.create_oval(drawX - self.pitchsize, drawY - self.pitchsize,
                                    drawX + self.pitchsize, drawY + self.pitchsize, width=2,
                                    outline="black", fill=self.colorpitch[self.black])
            endPoint = check(indX, indY, self.board)
            if endPoint is not None:
                print endPoint
                drawX = endPoint[0] * self.width / float(self.size) + self.offset * 1.1
                drawY = endPoint[1] * self.width / float(self.size) + self.offset * 1.1
                self.canvas.create_oval(drawX - self.pitchsize/2.0, drawY - self.pitchsize/2.0,
                                        drawX + self.pitchsize/2.0, drawY + self.pitchsize/2.0, width=2,
                                        fill="red", outline=self.colorpitch[self.black])
                self.end()
            self.black = not self.black
            return True
        else:
            return False

    def play_AI(self):
        self.ai = MinimaxPlayer()
        self.canvas.bind("<ButtonPress-1>", self.human_move_against_AI)
        # # while not self.gameOver:
        # if self.count % 2 != 0:
        #     print self.count
        #     x, y = self.ai.move(self.board, self.black)
        #     print x, y
        #     self.moveByIndex(x, y)
        #     print np.where(self.board != 0)
        #     self.count += 1


    def human_move_against_AI(self, event):
        # while not self.gameOver:
        if self.count % 2 == 0:
            if self.moveByPixel(event.x, event.y):
                self.count += 1
                if self.count % 2 != 0:
                    # print self.count
                    x, y = self.ai.move(self.board, self.black)
                    # print x, y
                    self.moveByIndex(x, y)
                    # print np.where(self.board != 0)
                    self.count += 1




root = Tk()
app = main(root)
root.mainloop()
