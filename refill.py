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
        
        # === RF template GUI === #
        self.medication_label = tk.Label(self.top, text='Medication:')
        self.medication_label.grid(column=0, row=0)
        self.medication_entry = tk.Entry(self.top)
        self.medication_entry.grid(column=1, row=0)

        self.hipaa_verification_label = tk.Label(self.top, text='Methods of HIPAA Verification:')
        self.hipaa_verification_label.grid(column=0, row=1)
        # === Check button canvas === #
        self.hipaa_checkbtn_canvas = tk.Canvas(self.top)
        self.hipaa_checkbtn_canvas.grid(column=1, row=1)
        # Name
        self.hipaa_name_checkbtn = tk.Checkbutton(self.hipaa_checkbtn_canvas)
        self.hipaa_name_checkbtn.grid(column=0, row=0)
        self.hippa_name_label = tk.Label(self.hipaa_checkbtn_canvas, text='Name')
        self.hippa_name_label.grid(column=1, row=0)
        # DOB
        self.hipaa_dob_checkbtn = tk.Checkbutton(self.hipaa_checkbtn_canvas)
        self.hipaa_dob_checkbtn.grid(column=2, row=0)
        self.hippa_dob_label = tk.Label(self.hipaa_checkbtn_canvas, text='DOB')
        self.hippa_dob_label.grid(column=3, row=0)
        # Address
        self.hipaa_address_checkbtn = tk.Checkbutton(self.hipaa_checkbtn_canvas)
        self.hipaa_address_checkbtn.grid(column=4, row=0)
        self.hippa_address_label = tk.Label(self.hipaa_checkbtn_canvas, text='Address')
        self.hippa_address_label.grid(column=5, row=0)
        # Drug prescribed
        self.hipaa_drug_checkbtn = tk.Checkbutton(self.hipaa_checkbtn_canvas)
        self.hipaa_drug_checkbtn.grid(column=6, row=0)
        self.hippa_drug_label = tk.Label(self.hipaa_checkbtn_canvas, text='Drug Prescribed')
        self.hippa_drug_label.grid(column=7, row=0)
        
        self.changes = tk.Label(self.top, text='Changes Since Last Visit:')
        self.changes.grid(column=0, row=2)

        



        


if __name__ == '__main__':
    root = tk.Tk()
    rt = RefillTemplate()

    root.mainloop()


# CF_RTF = win32clipboard.RegisterClipboardFormat("Rich Text Format")
# rtf = bytearray(fr'{{\rtf1\ansi\deff0 {{\fonttbl {{\f0 Times New Roman;}}}}{{\colortbl;\red0\green0\blue0;\red255\green0\blue0;\red255\green255\blue0;}} {text}}}', 'utf8')
