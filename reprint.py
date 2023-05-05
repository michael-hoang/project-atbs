import tkinter as tk
import ttkbootstrap as tkb

from ttkbootstrap.constants import *


class Reprint(tkb.Frame):
    """
    Interface to reprint filled card payment forms.
    """

    def __init__(self, master):
        super().__init__(master)


if __name__ == '__main__':
    reprint_window = tkb.Window(
        title='Reprint',
        themename='superhero'
    )
    rp = Reprint(master=reprint_window)

    reprint_window.mainloop()
