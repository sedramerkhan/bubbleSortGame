from tkinter import *

from utils import COLORS

"""
  it contain functions for drawing bottles with colored balls
"""


class BottlesGui:

    def __init__(self, canvas):
        self.canvas = canvas

    def draw_stack(self, x, y, width, length, tag="del"):
        end_x, end_y = x + width, y + length
        self.canvas.create_line(x, y, x, end_y, dash=(4, 2), tag=tag)
        self.canvas.create_line(end_x, y, end_x, end_y, dash=(4, 2), tag=tag)
        self.canvas.create_line(x, end_y, end_x, end_y, dash=(4, 2), tag=tag)

    def draw_bottles(self, bottles, x, y, x_add, ball_y_minus, diameter, ball_x, ball_y, stack_width, stack_length,
                     tag="del"):
        for bottle in bottles:
            self.draw_stack(x, y, stack_width, stack_length)
            b_x = x + ball_x
            b_y = y + ball_y
            for b in bottle:
                self.canvas.create_oval(b_x, b_y, b_x + diameter, b_y + diameter, fill=COLORS[b],
                                        outline=COLORS[b], tag=tag)
                b_y -= ball_y_minus
            x += x_add
