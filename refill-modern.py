"""This module contains a class that represents Refill Coordination form."""

import datetime as dt
import json
import os
import sys
import subprocess
import tkinter as tk
import ttkbootstrap as tkb

from win32 import win32clipboard
from tkinter import WORD


class RefillTemplate(tkb.Frame):
    """This class represents a GUI template that handles refill qeustions and formatting."""

    def __init__(self,master):
        super().__init__(master, padding=(20, 10))


if __name__ == '__main__':
    app = tkb.Window(
        'Refill Coordination', 'superhero', resizable=(False, False)
    )
    RefillTemplate(app)
    app.place_window_center()
    app.mainloop()
