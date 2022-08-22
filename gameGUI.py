from tkinter import *

from bottlesgui import BottlesGui
from PathGUI import PathGui
from scroll import scroll_frame_in, clear_widget
from game import Game
from utils import *

WIDTH = 800
HEIGHT = 400

"""
Display game using tkinter
"""


class GUI(Frame):
    start_x = 100
    start_y = 200

    bottles = [[0, 2, 6, 1], [5, 3, 2, 4], [1, 6, 2, 4], [2, 1, 3, 4], [5, 4, 0, 5], [3, 0, 0, 5], [1, 6, 3, 6], [], []]
    bottles_gui: BottlesGui

    # entry_s: Entry
    # entry_d: Entry

    def __init__(self):
        super().__init__()
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT, bg="white")
        self.bottles_gui = BottlesGui(self.canvas)
        self.master.title("Bubble Sort Game")
        self.pack(fill=BOTH, expand=1)
        self.canvas.pack(fill=BOTH, expand=1)  # side=LEFT,
        self.initUI()

        # sf = Frame(self,width=WIDTH, highlightbackground="navy", highlightthickness=1)
        # sf.pack()
        # self.sf = scroll_frame_in(self)
        # for i in range(10):
        #     NextStateGui(self.sf, self.bottles).grid(row=1, column=i, padx=10)

    """UI"""

    def initUI(self):
        # scroll_bar = Scrollbar(orient=VERTICAL, command=self.canvas.yview)
        # scroll_bar.pack(side=RIGHT, fill=Y)

        # self.canvas.configure(yscrollcommand=scroll_bar.set)
        # self.canvas.bind('<Configure>', lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        #
        # frame = Frame(self.canvas)
        #
        # self.canvas.create_window((0, 0), window=frame, anchor="nw")

        text_x, text_y, button_x, button_y, = self.initial_values()
        self.make_text("Welcome to bubble sort game, choose difficulty level:", text_x, text_y, 20)
        self.make_button("Easy", lambda: self.game_level(1), button_x, button_y)
        self.make_button("Medium", lambda: self.game_level(2), button_x + 150, button_y)
        self.make_button("Hard", lambda: self.game_level(3), button_x + 300, button_y)

        self.draw_bottles()

    def game_level(self, level):
        max_color, max_bottle, max_length = set_initial_values(level)
        self.initial_x(level)
        self.start_game(max_color, max_bottle, max_length)

    def start_game(self, max_color, max_bottle, max_length):
        self.game = Game(max_color, max_bottle, max_length)
        self.bottles = self.game.generate_bottles()
        self.sf = scroll_frame_in(self)
        # next_states = self.game.next_states()
        # for i,state in enumerate(next_states):
        #     NextStateGui(self.sf, state.bottles).grid(row=1, column=i, padx=10)
        self.canvas.delete("all")
        self.make_buttons()
        self.input_field()
        self.draw_numbers()
        self.draw_bottles()

    def make_buttons(self):
        self.make_button('Restart', self.restart, WIDTH - 50, 30)
        self.make_button('Show Next States', self.show_next_states, WIDTH - 170, 30)
        self.make_button('Move', self.move, WIDTH - 285, 30)
        self.make_button('BFS', self.BFS, WIDTH - 50, 70)
        self.make_button('DFS', self.DFS, WIDTH - 50, 110)
        self.make_button('UCS', self.UCS, WIDTH - 50, 150)
        self.make_button(' H C ', self.hill_climbing, WIDTH - 50, 190)
        self.make_button('  A*  ', self.A_star, WIDTH - 50, 230)
        # self.make_button('Move', self.move, WIDTH - 120, 30)

    def input_field(self):
        self.make_text("Enter source stack number:", 40, 60, 12)
        self.entry_s = Entry()
        self.canvas.create_window(350, 60, window=self.entry_s)
        self.make_text("Enter destination stack number:", 40, 100, 12)
        self.entry_d = Entry()
        self.canvas.create_window(350, 100, window=self.entry_d)

    """Commands"""

    def move(self):
        self.canvas.delete("restart_move")
        source = self.entry_s.get()
        destination = self.entry_d.get()

        if source == "" or destination == "":
            self.message_error(MESSAGE[8])
        elif not source.isdecimal() or not destination.isdecimal():
            self.message_error(MESSAGE[9])
        else:
            s = int(source)
            d = int(destination)
            l = len(self.bottles)
            if s > l or d > l:
                self.message_error(MESSAGE[7].format(l))
            else:

                move = self.game.move(s - 1, d - 1)
                if move == 4:
                    self.update_ui()

                    if self.game.check_win():
                        self.win_lose(MESSAGE[5])
                    elif self.game.check_lose():
                        self.win_lose(MESSAGE[6])

                else:
                    self.message_error("Illegal Move, " + MESSAGE[move])

    def win_lose(self, text):
        self.clear_entries()
        self.make_text(text, 180, 150, 30, font="Purisa", tag="restart")

    def update_ui(self):
        self.canvas.delete("del")
        self.draw_bottles()
        clear_widget(
            self.sf)  # _________________________________________________________________________________________
        # next_states = self.game.next_states()
        # for i,state in enumerate(next_states):
        #     NextStateGui(self.sf, state.bottles).grid(row=1, column=i, padx=10)
        self.clear_entries()

    def restart(self):
        self.bottles = self.game.generate_bottles()
        # self.game.bottles = self.bottles ####################################

        self.update_ui()
        self.canvas.delete("restart")
        self.canvas.delete("restart_move")
        self.clear_entries()

    def BFS(self):
        node = self.game.bfs()
        self.show_path(node)
        # self.sf = scroll_frame_in(self)

    def DFS(self):
        node = self.game.dfs()
        self.show_path(node)

    def UCS(self):
        node = self.game.ucs()
        self.show_path(node)

    def hill_climbing(self):
        node = self.game.hill()
        self.show_path(node)

    def A_star(self):
        node = self.game.A_star()
        self.show_path(node)

    def show_path(self, node):
        clear_widget(self.sf)
        i = 0
        nodes = []

        while node is not None:
            nodes.append(node.bottles)
            node = node.parent

        for bottle in nodes[::-1]:
            PathGui(self.sf, bottle).grid(row=1, column=i, padx=10)
            i += 1

    def show_next_states(self):
        states = self.game.next_states()
        clear_widget(self.sf)
        for i,state in enumerate(states):
            PathGui(self.sf, state.bottles).grid(row=1, column=i, padx=10)
        # self.canvas.delete("del")
        # self.make_buttons()

    def clear_entries(self):
        self.entry_s.delete(0, 'end')
        self.entry_d.delete(0, 'end')

    """Objects"""

    def make_button(self, text, command, x, y):
        color_bg, color_fg, size, font = '#fe3e77', 'white', 12, 'helvetica'
        button = Button(text=text, command=command, bg=color_bg, fg=color_fg,
                        font=(font, size, 'bold'))
        self.canvas.create_window(x, y, window=button)

    def make_text(self, text, x, y, size, color='black', font='Times 20', tag=''):
        self.canvas.create_text(x, y, anchor=W, fill=color, font=(font, size),
                                text=text, tag=tag)

    def message_error(self, text):
        msg = self.canvas.create_text(50, 130, anchor=W, fill='red', font=("Purisa", 10),
                                      text=text, tag='restart_move')
        self.after(3000, self.canvas.delete, msg)
        self.clear_entries()

    """Bottles"""

    def draw_bottles(self):
        # x = self.start_x
        # y = self.start_y
        #
        # for bottle in self.bottles:
        #     self.draw_stack(x, y)
        #     ball_x, ball_y, diameter = self.ball_pos(x, y)
        #     for b in bottle:
        #         self.canvas.create_oval(ball_x, ball_y, ball_x + diameter, ball_y + diameter, fill=COLORS[b],
        #                                 outline="pink", tag='del')
        #         ball_y -= 40
        #     x += 70
        self.bottles_gui.draw_bottles(self.bottles, x=self.start_x, y=self.start_y, x_add=70, ball_y_minus=40,
                                      diameter=30, ball_x=5,
                                      ball_y=125, stack_width=40, stack_length=160)

    def draw_numbers(self):
        x = self.start_x + 15
        y = self.start_y + 180
        for i in range(len(self.bottles)):
            self.make_text(NUMBERS[i], x, y, 12)
            x += 70

    # def draw_stack(self, x, y):
    #     end_x, end_y = x + 40, y + 160
    #     self.canvas.create_line(x, y, x, end_y, dash=(4, 2), tag='del')
    #     self.canvas.create_line(end_x, y, end_x, end_y, dash=(4, 2), tag='del')
    #     self.canvas.create_line(x, end_y, end_x, end_y, dash=(4, 2), tag='del')

    """Initial"""

    # def ball_pos(self, x, y):
    #     diameter = 30
    #     start_x = x + 5
    #     start_y = y + 125
    #     # end_x = start_x + diameter
    #     # end_y = start_y + diameter
    #     return start_x, start_y, diameter

    def initial_values(self):
        text_x = 40
        text_y = 40
        button_x = 200
        button_y = text_y + 50
        return text_x, text_y, button_x, button_y

    def initial_x(self, level):
        if level == 1:
            self.start_x = 250
        elif level == 2:
            self.start_x = 180
        else:
            self.start_x = 120


def main():
    try:
        root = Tk()
        GUI()
        root.mainloop()
    except:
        # print("quit")
        root.quit()


if __name__ == '__main__':
    main()
