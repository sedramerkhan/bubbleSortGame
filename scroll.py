from tkinter import *

"""
  this function make scollbar in the screen for showing all available moves
"""


def scroll_frame_in(root) -> Frame:
    canvas = Canvas(root, height=130)
    canvas.pack(side=TOP, fill=X)
    scroll = Scrollbar(root, orient=HORIZONTAL, command=canvas.xview)
    scroll.pack(side=BOTTOM, fill=X)
    canvas.configure(xscrollcommand=scroll.set, scrollregion=canvas.bbox("all"))
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<MouseWheel>", lambda e: canvas.xview_scroll(e.delta // 100, "units"))

    inner_frame = Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")
    return inner_frame


def clear_widget(widget: BaseWidget):
    for w in widget.winfo_children():
        w.destroy()

# def main():
#     root = Tk()
#     sf = Frame(root, highlightbackground="blue", highlightthickness=1)
#     sf.pack()
#     sf = scroll_frame_in(sf)
#     for i in range(10):
#         Frame(sf, width=100, height=100, background="blue").grid(row=1, column=i, padx=10)
#     root.geometry("500x300")
#
#     root.mainloop()
#
# if __name__ == '__main__':
#     main()
