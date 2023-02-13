""" This module contains a class that represents Refill Coordination form."""

import tkinter as tk
from tkinter import messagebox, END
from PIL import Image, ImageTk


class RefillTemplate:
    """This class represents a GUI template that handles refill questions and formatting."""

    def __init__(self):
        """Initialize template window and refill questions."""

        self.root = tk.Tk()
        self.root.title('Refill Coordination')
        self.root.config(height=500, width=400)

        self.root.mainloop()


if __name__ == '__main__':
    RefillTemplate()
