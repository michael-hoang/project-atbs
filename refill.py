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
        self.medication_labelFrame.grid(column=0, row=1, sticky='w')
        self.medication_entry = tk.Entry(self.medication_labelFrame)
        self.medication_entry.grid(column=1, row=0, sticky='w')

        # # === HIPPA label frame === #
        # self.hipaa_labelFrame = tk.LabelFrame(self.top, text='Methods of HIPAA Verfication')
        # self.hipaa_labelFrame.grid(column=0, row=2, sticky='w')
        # #   Check button canvas
        # self.hipaa_checkbtn_canvas = tk.Canvas(self.hipaa_labelFrame)
        # self.hipaa_checkbtn_canvas.grid(column=1, row=0, sticky='w')
        # # Name
        # self.hipaa_name_checkbtn = tk.Checkbutton(self.hipaa_checkbtn_canvas)
        # self.hipaa_name_checkbtn.grid(column=0, row=0)
        # self.hippa_name_label = tk.Label(self.hipaa_checkbtn_canvas, text='Name')
        # self.hippa_name_label.grid(column=1, row=0)
        # # DOB
        # self.hipaa_dob_checkbtn = tk.Checkbutton(self.hipaa_checkbtn_canvas)
        # self.hipaa_dob_checkbtn.grid(column=2, row=0)
        # self.hippa_dob_label = tk.Label(self.hipaa_checkbtn_canvas, text='DOB')
        # self.hippa_dob_label.grid(column=3, row=0)
        # # Address
        # self.hipaa_address_checkbtn = tk.Checkbutton(self.hipaa_checkbtn_canvas)
        # self.hipaa_address_checkbtn.grid(column=4, row=0)
        # self.hippa_address_label = tk.Label(self.hipaa_checkbtn_canvas, text='Address')
        # self.hippa_address_label.grid(column=5, row=0)
        # # Drug prescribed
        # self.hipaa_drug_checkbtn = tk.Checkbutton(self.hipaa_checkbtn_canvas)
        # self.hipaa_drug_checkbtn.grid(column=6, row=0)
        # self.hippa_drug_label = tk.Label(self.hipaa_checkbtn_canvas, text='Drug Prescribed')
        # self.hippa_drug_label.grid(column=7, row=0)
        
        # # === Changes label frame === #
        # self.changes_labelFrame = tk.LabelFrame(self.top, text='Changes Since Last Visit')
        # self.changes_labelFrame.grid(column=0, row=3, sticky='w')
        # #   Check button canvas
        # self.changes_checkbtn_canvas = tk.Canvas(self.changes_labelFrame)
        # self.changes_checkbtn_canvas.grid(column=1, row=2, sticky='w')
        # # None
        # self.changes_none_checkbtn = tk.Checkbutton(self.changes_checkbtn_canvas)
        # self.changes_none_checkbtn.grid(column=0, row=0, sticky='w')
        # self.changes_none_label = tk.Label(self.changes_checkbtn_canvas, text='None')
        # self.changes_none_label.grid(column=1, row=0, sticky='w', columnspan=4)
        # # Changes to dose/direction
        # self.changes_dose_checkbtn = tk.Checkbutton(self.changes_checkbtn_canvas)
        # self.changes_dose_checkbtn.grid(column=0, row=1, sticky='w')
        # self.changes_dose_label = tk.Label(self.changes_checkbtn_canvas, text='Changes to dose/directions')
        # self.changes_dose_label.grid(column=1, row=1, sticky='w', columnspan=4)
        # # Changes to medication profile
        # self.changes_medProfile_checkbtn = tk.Checkbutton(self.changes_checkbtn_canvas)
        # self.changes_medProfile_checkbtn.grid(column=0, row=2, sticky='w')
        # self.changes_medProfile_label = tk.Label(self.changes_checkbtn_canvas, text='Changes to medication profile')
        # self.changes_medProfile_label.grid(column=1, row=2, sticky='w', columnspan=4)
        # # Other
        # self.changes_other_checkbtn = tk.Checkbutton(self.changes_checkbtn_canvas)
        # self.changes_other_checkbtn.grid(column=0, row=3, sticky='w')
        # self.changes_other_label = tk.Label(self.changes_checkbtn_canvas, text='Other:')
        # self.changes_other_label.grid(column=1, row=3, sticky='w')
        # self.changes_other_entry = tk.Entry(self.changes_checkbtn_canvas)
        # self.changes_other_entry.grid(column=2, row=3, columnspan=4, sticky='w')

        # === Medication on hand label frame === #
        self.medication_on_hand_labelFrame = tk.LabelFrame(self.top, text='Medication On Hand')
        self.medication_on_hand_labelFrame.grid(column=0, row=4, sticky='w')
        #   Day supply canvas
        self.day_supply_canvas = tk.Canvas(self.medication_on_hand_labelFrame)
        self.day_supply_canvas.grid(column=0, row=0, sticky='w')
        self.day_supply_entry = tk.Entry(self.day_supply_canvas)
        self.day_supply_entry.grid(column=0, row=0)
        self.day_supply_label = tk.Label(self.day_supply_canvas, text='day(s)')
        self.day_supply_label.grid(column=1, row=0)
        #   Injection/cycle canvas
        self.injection_cycle_canvas = tk.Canvas(self.medication_on_hand_labelFrame)
        self.injection_cycle_canvas.grid(column=0, row=1, sticky='w')
        self.injection_btn = tk.Button(self.injection_cycle_canvas, text='Injection')
        self.injection_btn.grid(column=0, row=0)
        self.cycle_btn = tk.Button(self.injection_cycle_canvas, text='Cycle')
        self.cycle_btn.grid(column=1, row=0)
        self.due_start_label = tk.Label(self.injection_cycle_canvas, text='due/starts')
        self.due_start_label.grid(column=2, row=0)
        self.due_start_entry = tk.Entry(self.injection_cycle_canvas)
        self.due_start_entry.grid(column=3, row=0)

        # === Dispense date label frame === #
        self.dispense_date_labelFrame = tk.LabelFrame(self.top, text='Dispense Date')
        self.dispense_date_labelFrame.grid(column=0, row=5, sticky='w')
        #   Dispense btn canvas
        self.dispense_btn_canvas = tk.Canvas(self.dispense_date_labelFrame)
        self.dispense_btn_canvas.grid(column=0, row=0, sticky='w')
        # DCS button
        self.dispense_dcs_btn = tk.Button(self.dispense_btn_canvas, text='DCS')
        self.dispense_dcs_btn.grid(column=0, row=0)
        # FedEx button
        self.dispense_fedex_btn = tk.Button(self.dispense_btn_canvas, text='FedEx')
        self.dispense_fedex_btn.grid(column=1, row=0)
        # Pickup button
        self.dispense_pickup_btn = tk.Button(self.dispense_btn_canvas, text='Pickup')
        self.dispense_pickup_btn.grid(column=2, row=0)
        # Walkover button
        self.dispense_walkover_btn = tk.Button(self.dispense_btn_canvas, text='Walkover')
        self.dispense_walkover_btn.grid(column=3, row=0)
        # Walkover location label
        self.dispense_walkover_label = tk.Label(self.dispense_btn_canvas, text='Inpatient')
        self.dispense_walkover_label.grid(column=4, row=0) ### Create top level window to select walk over location
        #   Dispense date canvas
        self.dispense_date_canvas = tk.Canvas(self.dispense_date_labelFrame)
        self.dispense_date_canvas.grid(column=0, row=1, sticky='w')
        self.dispense_date_label = tk.Label(self.dispense_date_canvas, text='Ready to dispense date:')
        self.dispense_date_label.grid(column=0, row=1)
        self.dispense_date_entry = tk.Entry(self.dispense_date_canvas)
        self.dispense_date_entry.grid(column=3, row=1)
        #   Signature canvas
        self.dispense_signature_canvas = tk.Canvas(self.dispense_date_labelFrame)
        self.dispense_signature_canvas.grid(column=0, row=2, sticky='w')
        # Signature label
        self.dispense_signature_label = tk.Label(self.dispense_signature_canvas, text='Signature required?')
        self.dispense_signature_label.grid(column=0, row=0)
        # Yes button
        self.dispense_signature_yes_btn = tk.Button(self.dispense_signature_canvas, text='Yes')
        self.dispense_signature_yes_btn.grid(column=1, row=0)
        # No button
        self.dispense_signature_no_btn = tk.Button(self.dispense_signature_canvas, text='No')
        self.dispense_signature_no_btn.grid(column=2, row=0)
        #   Comments canvas
        self.dispense_comments_canvas = tk.Canvas(self.dispense_date_labelFrame)
        self.dispense_comments_canvas.grid(column=0, row=3, sticky='w')
        # Comments label
        self.dispense_comments_label = tk.Label(self.dispense_comments_canvas, text='Comments:')
        self.dispense_comments_label.grid(column=0, row=0)
        # Comments entry
        self.dispense_comments_entry = tk.Entry(self.dispense_comments_canvas)
        self.dispense_comments_entry.grid(column=1, row=0)

        # === Medication efficacy label frame === #
        self.medication_efficacy_labelFrame = tk.LabelFrame(self.top, text='Medication Efficacy')
        self.medication_efficacy_labelFrame.grid(column=0, row=6, sticky='w')
        #   Medication efficacy canvas
        self.medication_efficacy_canvas = tk.Canvas(self.medication_efficacy_labelFrame)
        self.medication_efficacy_canvas.grid(column=0, row=0, sticky='w')
        # Medication efficacy label
        self.medication_efficacy_label = tk.Label(self.medication_efficacy_canvas, text='Is medication working?')
        self.medication_efficacy_label.grid(column=0, row=0)
        # A little button
        self.medication_efficacy_alittle_btn = tk.Button(self.medication_efficacy_canvas, text='A little')
        self.medication_efficacy_alittle_btn.grid(column=1, row=0)
        # A lot button
        self.medication_efficacy_alot_btn = tk.Button(self.medication_efficacy_canvas, text='A lot')
        self.medication_efficacy_alot_btn.grid(column=2, row=0)
        # Can't tell button
        self.medication_efficacy_cantTell_btn = tk.Button(self.medication_efficacy_canvas, text='Can\'t tell')
        self.medication_efficacy_cantTell_btn.grid(column=3, row=0)
        



        



        


if __name__ == '__main__':
    root = tk.Tk()
    rt = RefillTemplate()

    root.mainloop()


# CF_RTF = win32clipboard.RegisterClipboardFormat("Rich Text Format")
# rtf = bytearray(fr'{{\rtf1\ansi\deff0 {{\fonttbl {{\f0 Times New Roman;}}}}{{\colortbl;\red0\green0\blue0;\red255\green0\blue0;\red255\green255\blue0;}} {text}}}', 'utf8')
