""" This module contains a class that represents Refill Coordination form."""

import tkinter as tk
from tkinter import messagebox, END
from PIL import Image, ImageTk
from win32 import win32clipboard


class RefillTemplate:
    """This class represents a GUI template that handles refill questions and formatting."""

    def __init__(self):
        """Initialize variables, template GUI and refill questions."""

        # Initialize settings
        self.background_color = 'white'
        self.btn_font = ('Comic Sans MS', 11, 'normal')
        self.btn_text_color = 'white'
        self.btn_active_fg_color = 'white'
        self.btn_bg_color = 'RoyalBlue1'
        self.btn_active_bg_color = 'RoyalBlue1'
        self.select_btn_bg_color = 'RoyalBlue4'
        self.btn_borderwidth = 0
        self.btn_relief = 'sunken' # sunken, raised, groove, ridge
        self.labelFrame_font = ('Comic Sans MS', 11, 'normal')
        self.label_font = ('Comic Sans MS', 11, 'normal')
        self.entry_font = ('Comic Sans MS', 11, 'normal')
        self.canvas_padx = 10
        self.canvas_pady = 10
        self.entry_bg_color = 'gray92'
        self.entry_relief = 'flat'
    

        # Initialize GUI window
        self.top = tk.Toplevel()
        self.top.title('Refill Coordination')
        self.top.config(bg=self.background_color, padx=20, pady=20)

        # Initialize variables
        self.user = ''
        self.medication_name = ''
        self.hipaa_verification = ''
        self.changes = 'None'
        self.ready_to_fill = 'Yes, refill initiated in WAM.'
        self.days_supply = ''
        self.injection_cycle = ''
        self.due_start = ''
        self.dispense_method = ''
        self.dispense_date = ''
        self.signature_required = ''
        self.dispense_comments = ''
        self.walkover_location = ''
        self.allergies_review = 'Yes'
        self.new_allergies = 'No'
        self.medication_review = 'Yes'
        self.spoke_with = ''
        self.new_medication = 'No'
        self.medical_condition_review = 'Yes'
        self.medical_conditions_changes = 'No'
        self.therapy_continuation = 'Yes'
        self.medication_working = ''
        self.symptoms_reported = 'No'
        self.symptoms_intervention = 'No'
        self.medication_adherence = 'Yes'
        self.goal_met = 'Yes'
        self.speak_rph = 'No'

        
        
        # === Medication label frame === #
        self.medication_labelFrame = tk.LabelFrame(
            self.top, text='Medication', bg=self.background_color, font=self.labelFrame_font
            )
        self.medication_labelFrame.grid(column=0, row=1, sticky='w')
        #   Medication canvas
        self.medication_canvas = tk.Canvas(
            self.medication_labelFrame, bg=self.background_color, highlightthickness=0
            )
        self.medication_canvas.grid(column=0, row=0, sticky='w', padx=self.canvas_padx, pady=self.canvas_pady)
        # Medication entry
        self.medication_entry = tk.Entry(self.medication_canvas, font=self.entry_font, bg=self.entry_bg_color, relief=self.entry_relief)
        self.medication_entry.grid(column=1, row=0, sticky='w')

        # # === HIPAA label frame === #
        # self.hipaa_labelFrame = tk.LabelFrame(self.top, text='Methods of HIPAA Verfication')
        # self.hipaa_labelFrame.grid(column=0, row=2, sticky='w')
        # #   Check button canvas
        # self.hipaa_checkbtn_canvas = tk.Canvas(self.hipaa_labelFrame)
        # self.hipaa_checkbtn_canvas.grid(column=1, row=0, sticky='w')
        # # Name
        # self.hipaa_name_checkbtn = tk.Checkbutton(self.hipaa_checkbtn_canvas)
        # self.hipaa_name_checkbtn.grid(column=0, row=0)
        # self.hipaa_name_label = tk.Label(self.hipaa_checkbtn_canvas, text='Name')
        # self.hipaa_name_label.grid(column=1, row=0)
        # # DOB
        # self.hipaa_dob_checkbtn = tk.Checkbutton(self.hipaa_checkbtn_canvas)
        # self.hipaa_dob_checkbtn.grid(column=2, row=0)
        # self.hipaa_dob_label = tk.Label(self.hipaa_checkbtn_canvas, text='DOB')
        # self.hipaa_dob_label.grid(column=3, row=0)
        # # Address
        # self.hipaa_address_checkbtn = tk.Checkbutton(self.hipaa_checkbtn_canvas)
        # self.hipaa_address_checkbtn.grid(column=4, row=0)
        # self.hipaa_address_label = tk.Label(self.hipaa_checkbtn_canvas, text='Address')
        # self.hipaa_address_label.grid(column=5, row=0)
        # # Drug prescribed
        # self.hipaa_drug_checkbtn = tk.Checkbutton(self.hipaa_checkbtn_canvas)
        # self.hipaa_drug_checkbtn.grid(column=6, row=0)
        # self.hipaa_drug_label = tk.Label(self.hipaa_checkbtn_canvas, text='Drug Prescribed')
        # self.hipaa_drug_label.grid(column=7, row=0)
        
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
        self.medication_on_hand_labelFrame = tk.LabelFrame(
            self.top, text='Medication On Hand', bg=self.background_color, font=self.labelFrame_font
            )
        self.medication_on_hand_labelFrame.grid(column=0, row=4, sticky='w')
        #   Day supply canvas
        self.day_supply_canvas = tk.Canvas(
            self.medication_on_hand_labelFrame, bg=self.background_color, highlightthickness=0
            )
        self.day_supply_canvas.grid(column=0, row=0, sticky='w', padx=self.canvas_padx, pady=self.canvas_pady)
        # Day supply entry
        self.day_supply_entry = tk.Entry(self.day_supply_canvas, font=self.entry_font, bg=self.entry_bg_color, relief=self.entry_relief)
        self.day_supply_entry.grid(column=0, row=0)
        # Day supply label
        self.day_supply_label = tk.Label(
            self.day_supply_canvas, text='day(s)', bg=self.background_color, font=self.label_font
            )
        self.day_supply_label.grid(column=1, row=0)
        #   Injection/cycle canvas
        self.injection_cycle_canvas = tk.Canvas(
            self.medication_on_hand_labelFrame, bg=self.background_color, highlightthickness=0
            )
        self.injection_cycle_canvas.grid(column=0, row=1, sticky='w', padx=self.canvas_padx, pady=self.canvas_pady)
        self.injection_btn = tk.Button(
            self.injection_cycle_canvas, text='Injection', command=self.select_injection,
            bg=self.btn_bg_color, borderwidth=self.btn_borderwidth,
            relief=self.btn_relief, fg=self.btn_text_color, font=self.btn_font,
            activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color
            )
        self.injection_btn.grid(column=0, row=0)
        self.cycle_btn = tk.Button(
            self.injection_cycle_canvas, text='Cycle', command=self.select_cycle,
            bg=self.btn_bg_color, borderwidth=self.btn_borderwidth,
            relief=self.btn_relief, fg=self.btn_text_color, font=self.btn_font,
            activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color
            )
        self.cycle_btn.grid(column=1, row=0)
        # Due/start label
        self.due_start_label = tk.Label(
            self.injection_cycle_canvas, text='due/starts', bg=self.background_color, font=self.label_font
            )
        self.due_start_label.grid(column=2, row=0)
        # Due/start entry
        self.due_start_entry = tk.Entry(self.injection_cycle_canvas, font=self.entry_font, bg=self.entry_bg_color, relief=self.entry_relief)
        self.due_start_entry.grid(column=3, row=0)

        # === Dispense date label frame === #
        self.dispense_date_labelFrame = tk.LabelFrame(
            self.top, text='Dispense Date', bg=self.background_color, font=self.labelFrame_font
            )
        self.dispense_date_labelFrame.grid(column=0, row=5, sticky='w')
        #   Dispense btn canvas
        self.dispense_btn_canvas = tk.Canvas(
            self.dispense_date_labelFrame, bg=self.background_color, highlightthickness=0
            )
        self.dispense_btn_canvas.grid(column=0, row=0, sticky='w', padx=self.canvas_padx, pady=self.canvas_pady)
        # DCS button
        self.dispense_dcs_btn = tk.Button(
            self.dispense_btn_canvas, text='DCS', command='',
            bg=self.btn_bg_color, borderwidth=self.btn_borderwidth,
            relief=self.btn_relief, fg=self.btn_text_color, font=self.btn_font,
            activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color
            )
        self.dispense_dcs_btn.grid(column=0, row=0)
        # FedEx button
        self.dispense_fedex_btn = tk.Button(
            self.dispense_btn_canvas, text='FedEx', command='',
            bg=self.btn_bg_color, borderwidth=self.btn_borderwidth,
            relief=self.btn_relief, fg=self.btn_text_color, font=self.btn_font,
            activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color
            )
        self.dispense_fedex_btn.grid(column=1, row=0)
        # Pickup button
        self.dispense_pickup_btn = tk.Button(
            self.dispense_btn_canvas, text='Pickup', command='',
            bg=self.btn_bg_color, borderwidth=self.btn_borderwidth,
            relief=self.btn_relief, fg=self.btn_text_color, font=self.btn_font,
            activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color
            )
        self.dispense_pickup_btn.grid(column=2, row=0)
        # Walkover button
        self.dispense_walkover_btn = tk.Button(
            self.dispense_btn_canvas, text='Walkover', command='',
            bg=self.btn_bg_color, borderwidth=self.btn_borderwidth,
            relief=self.btn_relief, fg=self.btn_text_color, font=self.btn_font,
            activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color
            )
        self.dispense_walkover_btn.grid(column=3, row=0)
        # Walkover location label
        self.dispense_walkover_label = tk.Label(
            self.dispense_btn_canvas, text='Inpatient', bg=self.background_color, font=self.label_font
            )
        self.dispense_walkover_label.grid(column=4, row=0) ### Create top level window to select walk over location
        #   Dispense date canvas
        self.dispense_date_canvas = tk.Canvas(
            self.dispense_date_labelFrame, bg=self.background_color, highlightthickness=0
            )
        self.dispense_date_canvas.grid(column=0, row=1, sticky='w', padx=self.canvas_padx, pady=self.canvas_pady)
        # Dispense date label
        self.dispense_date_label = tk.Label(
            self.dispense_date_canvas, text='Ready to dispense date:', bg=self.background_color, font=self.label_font
            )
        self.dispense_date_label.grid(column=0, row=1)
        # Dispense date entry
        self.dispense_date_entry = tk.Entry(self.dispense_date_canvas, font=self.entry_font, bg=self.entry_bg_color, relief=self.entry_relief)
        self.dispense_date_entry.grid(column=3, row=1)
        #   Signature canvas
        self.dispense_signature_canvas = tk.Canvas(
            self.dispense_date_labelFrame, bg=self.background_color, highlightthickness=0
            )
        self.dispense_signature_canvas.grid(column=0, row=2, sticky='w', padx=self.canvas_padx, pady=self.canvas_pady)
        # Signature label
        self.dispense_signature_label = tk.Label(
            self.dispense_signature_canvas, text='Signature required?', bg=self.background_color, font=self.label_font
            )
        self.dispense_signature_label.grid(column=0, row=0)
        # Yes button
        self.dispense_signature_yes_btn = tk.Button(
            self.dispense_signature_canvas, text='Yes', command='',
            bg=self.btn_bg_color, borderwidth=self.btn_borderwidth,
            relief=self.btn_relief, fg=self.btn_text_color, font=self.btn_font,
            activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color
            )
        self.dispense_signature_yes_btn.grid(column=1, row=0)
        # No button
        self.dispense_signature_no_btn = tk.Button(
            self.dispense_signature_canvas, text='No', command='',
            bg=self.btn_bg_color, borderwidth=self.btn_borderwidth,
            relief=self.btn_relief, fg=self.btn_text_color, font=self.btn_font,
            activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color
            )
        self.dispense_signature_no_btn.grid(column=2, row=0)
        #   Comments canvas
        self.dispense_comments_canvas = tk.Canvas(
            self.dispense_date_labelFrame, bg=self.background_color, highlightthickness=0
            )
        self.dispense_comments_canvas.grid(column=0, row=3, sticky='w', padx=self.canvas_padx, pady=self.canvas_pady)
        # Comments label
        self.dispense_comments_label = tk.Label(
            self.dispense_comments_canvas, text='Comments:', bg=self.background_color, font=self.label_font
            )
        self.dispense_comments_label.grid(column=0, row=0)
        # Comments entry
        self.dispense_comments_entry = tk.Entry(self.dispense_comments_canvas, font=self.entry_font, bg=self.entry_bg_color, relief=self.entry_relief)
        self.dispense_comments_entry.grid(column=1, row=0)

        # === Medication efficacy label frame === #
        self.medication_efficacy_labelFrame = tk.LabelFrame(
            self.top, text='Medication Efficacy', bg=self.background_color, font=self.labelFrame_font
            )
        self.medication_efficacy_labelFrame.grid(column=0, row=6, sticky='w')
        #   Medication efficacy canvas
        self.medication_efficacy_canvas = tk.Canvas(
            self.medication_efficacy_labelFrame, bg=self.background_color, highlightthickness=0
            )
        self.medication_efficacy_canvas.grid(column=0, row=0, sticky='w', padx=self.canvas_padx, pady=self.canvas_pady)
        # Medication efficacy label
        self.medication_efficacy_label = tk.Label(
            self.medication_efficacy_canvas, text='Is medication working?', bg=self.background_color, font=self.label_font
            )
        self.medication_efficacy_label.grid(column=0, row=0)
        # A little button
        self.medication_efficacy_alittle_btn = tk.Button(
            self.medication_efficacy_canvas, text='A little', command='',
            bg=self.btn_bg_color, borderwidth=self.btn_borderwidth,
            relief=self.btn_relief, fg=self.btn_text_color, font=self.btn_font,
            activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color
            )
        self.medication_efficacy_alittle_btn.grid(column=1, row=0)
        # A lot button
        self.medication_efficacy_alot_btn = tk.Button(
            self.medication_efficacy_canvas, text='A lot', command='',
            bg=self.btn_bg_color, borderwidth=self.btn_borderwidth,
            relief=self.btn_relief, fg=self.btn_text_color, font=self.btn_font,
            activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color
            )
        self.medication_efficacy_alot_btn.grid(column=2, row=0)
        # Can't tell button
        self.medication_efficacy_cantTell_btn = tk.Button(
            self.medication_efficacy_canvas, text='Can\'t tell', command='',
            bg=self.btn_bg_color, borderwidth=self.btn_borderwidth,
            relief=self.btn_relief, fg=self.btn_text_color, font=self.btn_font,
            activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color
            )
        self.medication_efficacy_cantTell_btn.grid(column=3, row=0)

        # === Spoke with label frame === #
        self.spoke_with_labelFrame = tk.LabelFrame(
            self.top, text='Spoke with:', bg=self.background_color, font=self.labelFrame_font
            )
        self.spoke_with_labelFrame.grid(column=0, row=7, sticky='w')
        #   Spoke with canvas
        self.spoke_with_canvas = tk.Canvas(
            self.spoke_with_labelFrame, bg=self.background_color, highlightthickness=0
            )
        self.spoke_with_canvas.grid(column=0, row=0, sticky='w', padx=self.canvas_padx, pady=self.canvas_pady)
        # Spoke with entry
        self.spoke_with_entry = tk.Entry(self.spoke_with_canvas, font=self.entry_font, bg=self.entry_bg_color, relief=self.entry_relief)
        self.spoke_with_entry.grid(column=0, row=0)
        

    def select_injection(self):
        """Select injection"""
        self.injection_btn.config(bg=self.select_btn_bg_color, command=self.unselect_injection)
        self.cycle_btn.config(bg=self.btn_bg_color, command=self.select_cycle)
        self.injection_cycle = 'Injection is due on'

    def unselect_injection(self):
        """Unselect injection"""
        self.injection_btn.config(bg=self.btn_bg_color, command=self.select_injection)
        self.cycle_btn.config(bg=self.btn_bg_color, command=self.select_cycle)
        self.injection_cycle = ''

    def select_cycle(self):
        """Select cycle"""
        self.injection_btn.config(bg=self.btn_bg_color, command=self.select_injection)
        self.cycle_btn.config(bg=self.select_btn_bg_color, command=self.unselect_cycle)
        self.injection_cycle = 'Next cycle starts on'
    
    def unselect_cycle(self):
        """Unselect cycle"""
        self.injection_btn.config(bg=self.btn_bg_color, command=self.select_injection)
        self.cycle_btn.config(bg=self.btn_bg_color, command=self.select_cycle)
        self.injection_cycle = ''

        



        


if __name__ == '__main__':
    root = tk.Tk()
    rt = RefillTemplate()

    root.mainloop()


# CF_RTF = win32clipboard.RegisterClipboardFormat("Rich Text Format")
# rtf = bytearray(fr'{{\rtf1\ansi\deff0 {{\fonttbl {{\f0 Times New Roman;}}}}{{\colortbl;\red0\green0\blue0;\red255\green0\blue0;\red255\green255\blue0;}} {text}}}', 'utf8')
