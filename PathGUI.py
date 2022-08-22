from tkinter import *

from utils import COLORS
from bottlesgui import BottlesGui

'''
 Shows all available moves in the game from current state
'''


class PathGui(Frame):

    def __init__(self, frame, bottles):
        super().__init__(frame)
        # self.bottles = bottles
        # self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.canvas.configure(bg="snow", width=len(bottles)*30 + 30, height=120)
        self.canvas.pack(fill=BOTH, expand=1)
        self.bottles_gui = BottlesGui(self.canvas)
        self.draw_bottles(bottles)

    def draw_bottles(self,bottles):
        self.bottles_gui.draw_bottles(bottles,x=20, y=20, x_add=30, ball_y_minus=15, diameter=10, ball_x=5, ball_y=55,
                                      stack_width=20, stack_length=70)
