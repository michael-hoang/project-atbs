""" This module contains a class that represents Refill Coordination form."""

import tkinter as tk
from tkinter import messagebox, END
from PIL import Image, ImageTk
from win32 import win32clipboard


class RefillTemplate:
    """This class represents a GUI template that handles refill questions and formatting."""

    def __init__(self):
        """Initialize template window and refill questions."""

        self.top = tk.Toplevel()
        self.top.title('Refill Coordination')
        
        # Template
        self.medication_label = tk.Label(self.top, text='Medication:')
        self.medication_label.grid(column=0, row=0)
        self.medication_entry = tk.Entry(self.top)
        self.medication_entry.grid(column=1, row=0)

        



        


if __name__ == '__main__':
    root = tk.Tk()
    rt = RefillTemplate()

    root.mainloop()


# CF_RTF = win32clipboard.RegisterClipboardFormat("Rich Text Format")
# rtf = bytearray(fr'{{\rtf1\ansi\deff0 {{\fonttbl {{\f0 Times New Roman;}}}}{{\colortbl;\red0\green0\blue0;\red255\green0\blue0;\red255\green255\blue0;}} {text}}}', 'utf8')
