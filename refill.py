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
        self.top.config(padx=20, pady=20)
        
        # === Medication label frame === #
        self.medication_labelFrame = tk.LabelFrame(self.top, text='Medication')
        self.medication_labelFrame.grid(column=0, row=0, sticky='w')
        self.medication_entry = tk.Entry(self.medication_labelFrame)
        self.medication_entry.grid(column=1, row=0, sticky='w')

        # === HIPPA label frame === #
        self.hipaa_labelFrame = tk.LabelFrame(self.top, text='Methods of HIPAA Verfication')
        self.hipaa_labelFrame.grid(column=0, row=1, sticky='w')
        #   Check button canvas
        self.hipaa_checkbtn_canvas = tk.Canvas(self.hipaa_labelFrame)
        self.hipaa_checkbtn_canvas.grid(column=1, row=0, sticky='w')
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
        
        # === Changes label frame === #
        self.changes_labelFrame = tk.LabelFrame(self.top, text='Changes Since Last Visit')
        self.changes_labelFrame.grid(column=0, row=2, sticky='w')
        #   Check button canvas
        self.changes_checkbtn_canvas = tk.Canvas(self.changes_labelFrame)
        self.changes_checkbtn_canvas.grid(column=1, row=2, sticky='w')
        # None
        self.changes_none_checkbtn = tk.Checkbutton(self.changes_checkbtn_canvas)
        self.changes_none_checkbtn.grid(column=0, row=0, sticky='w')
        self.changes_none_label = tk.Label(self.changes_checkbtn_canvas, text='None')
        self.changes_none_label.grid(column=1, row=0, sticky='w', columnspan=4)
        # Changes to dose/direction
        self.changes_dose_checkbtn = tk.Checkbutton(self.changes_checkbtn_canvas)
        self.changes_dose_checkbtn.grid(column=0, row=1, sticky='w')
        self.changes_dose_label = tk.Label(self.changes_checkbtn_canvas, text='Changes to dose/directions')
        self.changes_dose_label.grid(column=1, row=1, sticky='w', columnspan=4)
        # Changes to medication profile
        self.changes_medProfile_checkbtn = tk.Checkbutton(self.changes_checkbtn_canvas)
        self.changes_medProfile_checkbtn.grid(column=0, row=2, sticky='w')
        self.changes_medProfile_label = tk.Label(self.changes_checkbtn_canvas, text='Changes to medication profile')
        self.changes_medProfile_label.grid(column=1, row=2, sticky='w', columnspan=4)
        # Other
        self.changes_other_checkbtn = tk.Checkbutton(self.changes_checkbtn_canvas)
        self.changes_other_checkbtn.grid(column=0, row=3, sticky='w')
        self.changes_other_label = tk.Label(self.changes_checkbtn_canvas, text='Other:')
        self.changes_other_label.grid(column=1, row=3, sticky='w')
        self.changes_other_entry = tk.Entry(self.changes_checkbtn_canvas)
        self.changes_other_entry.grid(column=2, row=3, columnspan=4, sticky='w')

        # === Medication on hand label frame === #
        self.medication_on_hand_labelFrame = tk.LabelFrame(self.top, text='Medication On Hand')
        self.medication_on_hand_labelFrame.grid(column=0, row=3)
        


        



        


if __name__ == '__main__':
    root = tk.Tk()
    rt = RefillTemplate()

    root.mainloop()


# CF_RTF = win32clipboard.RegisterClipboardFormat("Rich Text Format")
# rtf = bytearray(fr'{{\rtf1\ansi\deff0 {{\fonttbl {{\f0 Times New Roman;}}}}{{\colortbl;\red0\green0\blue0;\red255\green0\blue0;\red255\green255\blue0;}} {text}}}', 'utf8')
