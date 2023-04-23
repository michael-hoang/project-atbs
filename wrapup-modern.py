import datetime as dt
import tkinter as tk
import ttkbootstrap as tkb

from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from tkinter.ttk import Style


class WrapUp(tkb.Frame):
    """Wrap up date calculator."""

    def __init__(self, master):
        """Initialize."""
        super().__init__(master)
        self.pack(side=LEFT, fill=BOTH, expand=YES)
        style = Style()
        style.configure('TButton', font=('', 11, ''))


if __name__ == '__main__':
    app = tkb.Window(
        'Wrap Up', 'superhero', resizable=(False, False)
    )
    WrapUp(app, app)
    app.place_window_center()
    app.mainloop()
