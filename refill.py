""" This module contains a class that represents Refill Coordination form."""

import tkinter as tk
import datetime as dt
import os, sys, subprocess, json
from tkinter import messagebox
from PIL import Image, ImageTk
from win32 import win32clipboard


class RefillTemplate:
    """This class represents a GUI template that handles refill questions and formatting."""

    def __init__(self):
        """Initialize variables, template GUI and refill questions."""

        # Initialize settings
        self.background_color = 'white'
            # Select buttons
        self.btn_font = ('Comic Sans MS', 11, 'normal')
        self.btn_text_color = 'white'
        self.btn_active_fg_color = 'white'
        self.btn_bg_color = 'RoyalBlue1'
        self.btn_active_bg_color = 'RoyalBlue1'
        self.select_btn_bg_color = 'RoyalBlue4'
        self.btn_borderwidth = 0
        self.btn_relief = 'sunken' # sunken, raised, groove, ridge
        self.btn_space_btwn = 5
        self.btn_disabled_fg_color = 'snow3'
        self.btn_disabled_bg_color = 'ghost white'
            # Label frames
        self.labelFrame_font = ('Comic Sans MS', 11, 'normal')
        self.labelFrame_space_btwn = 5
        self.label_font = ('Comic Sans MS', 11, 'normal')
        self.disabled_text_color = 'snow3'
        self.text_color = 'black'
            # Entry
        self.entry_font = ('Comic Sans MS', 11, 'normal')
        self.entry_bg_color = 'gray92'
        self.entry_relief = 'flat'
            # Canvas
        self.canvas_padx = 10
        self.canvas_pady = 10
            # Other buttons
        self.copy_btn_bg_color = 'ghost white'
        self.copy_btn_fg_color = 'medium sea green'
        self.copy_btn_active_bg_color = 'ghost white' # #ebfff3
        self.copy_btn_active_fg_color = 'medium sea green'
        self.copy_btn_disabled_fg_color = 'snow3'
    
        # Initialize GUI window
        self.top = tk.Toplevel()
        self.top.withdraw()
        self.top.attributes('-topmost', 0)
        self.top.title('Refill Coordination')
        self.top.config(bg=self.background_color, padx=20, pady=20)
        self.top.resizable(False, False)

        # Initialize variables
        self.user = self.get_existing_user()
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
        self.fedex_delivery_date = ''
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

        # === Container for top buttons === #
        self.container_top_buttons = tk.Canvas(
            self.top, bg=self.background_color, highlightthickness=0
            )
        self.container_top_buttons.grid(column=0, row=0, sticky='e')

        # Refill coordination label
        self.refill_coordination_label = tk.Label(
            self.container_top_buttons, text='Refill Coordination',
            bg=self.background_color, font=('Comic Sans MS', 15, 'normal')
            )
        self.refill_coordination_label.grid(column=0, row=0, padx=(0, 90))

        # Edit user button
        img_path = './assets/img/edit-user.png'
        img = Image.open(img_path)
        self.edit_user_img = ImageTk.PhotoImage(img)
        self.edit_user_btn = tk.Button(
            self.container_top_buttons, image=self.edit_user_img, command=self.user_setup_window,
            bg=self.copy_btn_bg_color
            )
        self.edit_user_btn.grid(column=1, row=0, padx=(0, 15))

        # === Container for Medication label frame and Clear button === #
        self.container_med_clear = tk.Canvas(
            self.top, bg=self.background_color, highlightthickness=0
            )
        self.container_med_clear.grid(column=0, row=1, sticky='w')

        # === Medication label frame === #
        self.medication_labelFrame = tk.LabelFrame(
            self.container_med_clear, text='Medication', bg=self.background_color, font=self.labelFrame_font
            )
        self.medication_labelFrame.grid(column=0, row=0, sticky='w')
        #   Medication canvas
        self.medication_canvas = tk.Canvas(
            self.medication_labelFrame, bg=self.background_color, highlightthickness=0
            )
        self.medication_canvas.grid(column=0, row=0, sticky='w', padx=self.canvas_padx, pady=self.canvas_pady)
        # Medication entry
        self.medication_entry = tk.Entry(
            self.medication_canvas, font=self.entry_font, bg=self.entry_bg_color,
            relief=self.entry_relief, width=30
            )
        self.medication_entry.grid(column=1, row=0, sticky='w')
        
        # Clear button
        self.clear_btn = tk.Button(
            self.container_med_clear, text='Clear', command=self.clear, bg=self.copy_btn_bg_color, relief='raised',
            fg='firebrick1', font=self.btn_font, activebackground=self.copy_btn_bg_color,
            activeforeground='firebrick1', width=9
            )
        self.clear_btn.grid(column=1, row=0, padx=(20,0))

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
        self.medication_on_hand_labelFrame.grid(column=0, row=4, sticky='we', pady=(self.labelFrame_space_btwn, 0))
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
        self.cycle_btn.grid(column=1, row=0, padx=(self.btn_space_btwn, 0))
        # Due/start label
        self.due_start_label = tk.Label(
            self.injection_cycle_canvas, text='', bg=self.background_color,
            font=self.label_font, width=7
            )
        self.due_start_label.grid(column=2, row=0)
        # Due/start entry
        self.due_start_entry = tk.Entry(
            self.injection_cycle_canvas, font=self.entry_font, bg=self.entry_bg_color,
            relief=self.entry_relief, width=19, disabledbackground=self.background_color,
            state='disabled'
            )
        self.due_start_entry.grid(column=3, row=0)

        # === Dispense date label frame === #
        self.dispense_date_labelFrame = tk.LabelFrame(
            self.top, text='Dispense Date', bg=self.background_color, font=self.labelFrame_font
            )
        self.dispense_date_labelFrame.grid(column=0, row=5, sticky='w', pady=(self.labelFrame_space_btwn, 0))
        #   Dispense btn canvas
        self.dispense_btn_canvas = tk.Canvas(
            self.dispense_date_labelFrame, bg=self.background_color, highlightthickness=0
            )
        self.dispense_btn_canvas.grid(column=0, row=0, sticky='w', padx=self.canvas_padx, pady=self.canvas_pady)
        # DCS button
        self.dispense_dcs_btn = tk.Button(
            self.dispense_btn_canvas, text='DCS', command=self.select_dcs,
            bg=self.btn_bg_color, borderwidth=self.btn_borderwidth,
            relief=self.btn_relief, fg=self.btn_text_color, font=self.btn_font,
            activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color
            )
        self.dispense_dcs_btn.grid(column=0, row=0)
        # FedEx button
        self.dispense_fedex_btn = tk.Button(
            self.dispense_btn_canvas, text='FedEx', command=self.select_fedex,
            bg=self.btn_bg_color, borderwidth=self.btn_borderwidth,
            relief=self.btn_relief, fg=self.btn_text_color, font=self.btn_font,
            activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color
            )
        self.dispense_fedex_btn.grid(column=1, row=0, padx=(self.btn_space_btwn, 0))
        # Pick up button
        self.dispense_pickup_btn = tk.Button(
            self.dispense_btn_canvas, text='Pick Up', command=self.select_pickup,
            bg=self.btn_bg_color, borderwidth=self.btn_borderwidth,
            relief=self.btn_relief, fg=self.btn_text_color, font=self.btn_font,
            activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color
            )
        self.dispense_pickup_btn.grid(column=2, row=0, padx=(self.btn_space_btwn, 0))
        # Walk over button
        self.dispense_walkover_btn = tk.Button(
            self.dispense_btn_canvas, text='Walk Over', command=self.select_walkover,
            bg=self.btn_bg_color, borderwidth=self.btn_borderwidth,
            relief=self.btn_relief, fg=self.btn_text_color, font=self.btn_font,
            activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color
            )
        self.dispense_walkover_btn.grid(column=3, row=0, padx=(self.btn_space_btwn, 0))
        # Walkover location entry
        self.dispense_walkover_entry = tk.Entry(
            self.dispense_btn_canvas, font=self.entry_font, bg=self.entry_bg_color,
            relief=self.entry_relief, width=15, disabledbackground=self.background_color,
            state='disabled'
            )
        self.dispense_walkover_entry.grid(column=4, row=0, padx=(self.btn_space_btwn, 0))
        #   Dispense date canvas
        self.dispense_date_canvas = tk.Canvas(
            self.dispense_date_labelFrame, bg=self.background_color, highlightthickness=0
            )
        self.dispense_date_canvas.grid(column=0, row=1, sticky='w', padx=self.canvas_padx, pady=self.canvas_pady)
        # Dispense date label
        self.dispense_date_label = tk.Label(
            self.dispense_date_canvas, text='Dispense Date:',
            bg=self.background_color, font=self.label_font, width=13, fg=self.disabled_text_color
            )
        self.dispense_date_label.grid(column=0, row=1)
        # Dispense date entry
        self.dispense_date_entry = tk.Entry(
            self.dispense_date_canvas,font=self.entry_font, bg=self.entry_bg_color,
            relief=self.entry_relief, width=10, state='disabled'
            )
        self.dispense_date_entry.grid(column=3, row=1)
        # FedEx delivery label
        self.fedex_delivery_label = tk.Label(
            self.dispense_date_canvas, font=self.label_font, bg=self.background_color,
            text='for 3/31 delivery'
            )
        self.fedex_delivery_label.grid(column=4, row=1)

        # Copy WAM notes button (@ canvas widget level, master is top level window)
        self.copy_wam_notes_btn = tk.Button(
            self.dispense_date_labelFrame, text='Copy WAM Notes', command='',
            bg=self.copy_btn_bg_color, relief='raised', fg=self.copy_btn_fg_color,
            font=self.btn_font, activebackground=self.copy_btn_active_bg_color,
            activeforeground=self.copy_btn_active_fg_color, width=11,
            wraplength=80, disabledforeground=self.copy_btn_disabled_fg_color
            )
        self.copy_wam_notes_btn.grid(column=0, row=2, rowspan=3, padx=(275,0), pady=(20,0))

        #   Signature canvas
        self.dispense_signature_canvas = tk.Canvas(
            self.dispense_date_labelFrame, bg=self.background_color, highlightthickness=0
            )
        self.dispense_signature_canvas.grid(column=0, row=3, sticky='w', padx=self.canvas_padx, pady=self.canvas_pady)
        # Signature label
        self.dispense_signature_label = tk.Label(
            self.dispense_signature_canvas, text='Signature required?',
            bg=self.background_color, font=self.label_font, fg=self.disabled_text_color
            )
        self.dispense_signature_label.grid(column=0, row=0)
        # Yes button
        self.dispense_signature_yes_btn = tk.Button(
            self.dispense_signature_canvas, text='Yes', command=self.select_yes_sig,
            bg=self.btn_disabled_bg_color, borderwidth=self.btn_borderwidth,
            relief=self.btn_relief, fg=self.btn_text_color, font=self.btn_font,
            activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color,
            disabledforeground=self.copy_btn_disabled_fg_color, state='disabled'
            )
        self.dispense_signature_yes_btn.grid(column=1, row=0)
        # No button
        self.dispense_signature_no_btn = tk.Button(
            self.dispense_signature_canvas, text='No', command=self.select_no_sig,
            bg=self.btn_disabled_bg_color, borderwidth=self.btn_borderwidth,
            relief=self.btn_relief, fg=self.btn_text_color, font=self.btn_font,
            activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color,
            disabledforeground=self.copy_btn_disabled_fg_color, state='disabled'
            )
        self.dispense_signature_no_btn.grid(column=2, row=0, padx=(self.btn_space_btwn, 0))

        #   Comments canvas
        self.dispense_comments_canvas = tk.Canvas(
            self.dispense_date_labelFrame, bg=self.background_color, highlightthickness=0
            )
        self.dispense_comments_canvas.grid(column=0, row=4, sticky='w', padx=self.canvas_padx, pady=self.canvas_pady)
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
        self.medication_efficacy_labelFrame.grid(column=0, row=6, sticky='w', pady=(self.labelFrame_space_btwn, 0))
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
            self.medication_efficacy_canvas, text='A little', command=self.select_a_little,
            bg=self.btn_bg_color, borderwidth=self.btn_borderwidth,
            relief=self.btn_relief, fg=self.btn_text_color, font=self.btn_font,
            activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color
            )
        self.medication_efficacy_alittle_btn.grid(column=1, row=0)
        # A lot button
        self.medication_efficacy_alot_btn = tk.Button(
            self.medication_efficacy_canvas, text='A lot', command=self.select_a_lot,
            bg=self.btn_bg_color, borderwidth=self.btn_borderwidth,
            relief=self.btn_relief, fg=self.btn_text_color, font=self.btn_font,
            activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color
            )
        self.medication_efficacy_alot_btn.grid(column=2, row=0, padx=(self.btn_space_btwn, 0))
        # Can't tell button
        self.medication_efficacy_cantTell_btn = tk.Button(
            self.medication_efficacy_canvas, text='Can\'t tell', command=self.select_cant_tell,
            bg=self.btn_bg_color, borderwidth=self.btn_borderwidth,
            relief=self.btn_relief, fg=self.btn_text_color, font=self.btn_font,
            activebackground=self.btn_active_bg_color, activeforeground=self.btn_active_fg_color
            )
        self.medication_efficacy_cantTell_btn.grid(column=3, row=0, padx=(self.btn_space_btwn, 0))

        # === Spoke with label frame === #
        self.spoke_with_labelFrame = tk.LabelFrame(
            self.top, text='Spoke with:', bg=self.background_color, font=self.labelFrame_font
            )
        self.spoke_with_labelFrame.grid(column=0, row=7, sticky='w', pady=(self.labelFrame_space_btwn, 0))
        #   Spoke with canvas
        self.spoke_with_canvas = tk.Canvas(
            self.spoke_with_labelFrame, bg=self.background_color, highlightthickness=0
            )
        self.spoke_with_canvas.grid(column=0, row=0, sticky='w', padx=self.canvas_padx, pady=self.canvas_pady)
        # Spoke with entry
        self.spoke_with_entry = tk.Entry(
            self.spoke_with_canvas, font=self.entry_font, bg=self.entry_bg_color,
            relief=self.entry_relief, width=25
            )
        self.spoke_with_entry.grid(column=0, row=0)

        # Copy template button
        self.copy_template_btn = tk.Button(
            self.top, text='Copy Template', command='', bg=self.copy_btn_bg_color,
            relief='raised', fg=self.copy_btn_fg_color, font=self.btn_font,
            activebackground=self.copy_btn_active_bg_color,
            activeforeground=self.copy_btn_active_fg_color, width=14,
            disabledforeground=self.copy_btn_disabled_fg_color
            )
        self.copy_template_btn.grid(column=0, row=7, padx=(260,0), pady=(15,0))

        # ~ ~ ~ bind ~ ~ ~ #
        self.dispense_walkover_entry.bind('<FocusIn>', self.remove_temp_text)
        self.top.bind('<Delete>', self.clear)
        self.top.bind('<Control-u>', self.user_setup_window)
        
        # ~ ~ ~ after ~ ~ ~ #
        self.top.after(ms=50, func=self.run_validations)

        # ~ ~ ~ Center window ~ ~ ~ #
        self.top.update_idletasks()
        win_width = self.top.winfo_reqwidth()
        win_height = self.top.winfo_reqheight()
        screen_width = self.top.winfo_screenwidth()
        screen_height = self.top.winfo_screenheight()
        x = int(screen_width/2 - win_width/2)
        y = int(screen_height/2 - win_width/2)
        self.top.geometry(f"{win_width}x{win_height}+{x}+{y}")

        # ~ ~ ~ Check user ~ ~ ~ #
        if self.user:
            self.top.title(f'Refill Coordination - {self.user}')
            self.top.deiconify()
            self.medication_entry.focus()
        else:
            relative_path = '.data'
            if getattr(sys, 'frozen', False):
                application_path = os.path.dirname(sys.executable)
            elif __file__:
                application_path = os.path.dirname(__file__)

            absolute_path = os.path.join(application_path, relative_path)
            if not os.path.exists(absolute_path):
                self._create_data_dir(absolute_path)

            self.user_setup_window()


    def select_injection(self):
        """Select injection button."""
        self.injection_btn.config(bg=self.select_btn_bg_color, command=self._unselect_injection_cycle)
        self.cycle_btn.config(bg=self.btn_bg_color, command=self.select_cycle)
        self.injection_cycle = 'Injection is due'
        self.due_start_label.config(text='is due')
        self.due_start_entry.config(state='normal')
        self.top.focus()
        if not self.day_supply_entry.get().strip():
            self.day_supply_entry.insert(0, '0')

    def select_cycle(self):
        """Select cycle button."""
        self.injection_btn.config(bg=self.btn_bg_color, command=self.select_injection)
        self.cycle_btn.config(bg=self.select_btn_bg_color, command=self._unselect_injection_cycle)
        self.injection_cycle = 'Next cycle starts'
        self.due_start_label.config(text='starts')
        self.due_start_entry.config(state='normal')
        self.top.focus()
        if not self.day_supply_entry.get().strip():
            self.day_supply_entry.insert(0, '0')
    
    def _unselect_injection_cycle(self):
        """Unselect injection/cycle button."""
        self.injection_btn.config(bg=self.btn_bg_color, command=self.select_injection)
        self.cycle_btn.config(bg=self.btn_bg_color, command=self.select_cycle)
        self.injection_cycle = ''
        self.due_start_label.config(text='')
        self.due_start_entry.delete(0, 'end')
        self.due_start_entry.config(state='disabled')


    def select_dcs(self):
        """Select DCS button."""
        self.dispense_dcs_btn.config(bg=self.select_btn_bg_color, command=self._unselect_dcs_fedex)
        self.dispense_fedex_btn.config(bg=self.btn_bg_color, command=self.select_fedex)
        self.dispense_pickup_btn.config(bg=self.btn_bg_color, command=self.select_pickup)
        self.dispense_walkover_btn.config(bg=self.btn_bg_color, command=self.select_walkover)
        self.dispense_method = 'DCS'
        self.dispense_walkover_entry.delete(0, 'end')
        self.dispense_walkover_entry.config(state='disabled')
        self.dispense_date_label.config(text='Shiping out on', fg=self.text_color)
        self.dispense_date_entry.config(state='normal')
        self.dispense_signature_yes_btn.config(state='normal', bg=self.btn_bg_color)
        self.dispense_signature_no_btn.config(state='normal', bg=self.btn_bg_color)
        self.dispense_signature_label.config(fg=self.text_color)
        self.fedex_delivery_label.config(text='')

    def select_fedex(self):
        """Select FedEx button."""
        self.dispense_dcs_btn.config(bg=self.btn_bg_color, command=self.select_dcs)
        self.dispense_fedex_btn.config(bg=self.select_btn_bg_color, command=self._unselect_dcs_fedex)
        self.dispense_pickup_btn.config(bg=self.btn_bg_color, command=self.select_pickup)
        self.dispense_walkover_btn.config(bg=self.btn_bg_color, command=self.select_walkover)
        self.dispense_method = 'FedEx'
        self.dispense_walkover_entry.delete(0, 'end')
        self.dispense_walkover_entry.config(state='disabled')
        self.dispense_date_label.config(text='Shiping out on', fg=self.text_color)
        self.dispense_date_entry.config(state='normal')
        self.dispense_signature_yes_btn.config(state='normal', bg=self.btn_bg_color)
        self.dispense_signature_no_btn.config(state='normal', bg=self.btn_bg_color)
        self.dispense_signature_label.config(fg=self.text_color)


    def select_pickup(self):
        """Select Pick Up button."""
        self.dispense_dcs_btn.config(bg=self.btn_bg_color, command=lambda: [self.select_dcs(), self._enable_yes_no_btn()])
        self.dispense_fedex_btn.config(bg=self.btn_bg_color, command=lambda: [self.select_fedex(), self._enable_yes_no_btn()])
        self.dispense_pickup_btn.config(bg=self.select_btn_bg_color, command=self._unselect_pickup_walkover)
        self.dispense_walkover_btn.config(bg=self.btn_bg_color, command=self.select_walkover)
        self.dispense_method = 'Pick up'
        self.dispense_walkover_entry.delete(0, 'end')
        self.dispense_walkover_entry.config(state='disabled')
        self.dispense_signature_yes_btn.config(state='disabled', bg=self.btn_disabled_bg_color)
        self.dispense_signature_no_btn.config(state='disabled', bg=self.btn_disabled_bg_color)
        self.signature_required = ''
        self.dispense_signature_label.config(fg=self.disabled_text_color)
        self.dispense_date_label.config(text='Picking up on', fg=self.text_color)
        self.dispense_date_entry.config(state='normal')
        self.fedex_delivery_label.config(text='')

    def select_walkover(self):
        """Select Walkover button."""
        self.dispense_dcs_btn.config(bg=self.btn_bg_color, command=lambda: [self.select_dcs(), self._enable_yes_no_btn()])
        self.dispense_fedex_btn.config(bg=self.btn_bg_color, command=lambda: [self.select_fedex(), self._enable_yes_no_btn()])
        self.dispense_pickup_btn.config(bg=self.btn_bg_color, command=self.select_pickup)
        self.dispense_walkover_btn.config(bg=self.select_btn_bg_color, command=self._unselect_pickup_walkover)
        self.dispense_method = 'Walk over'
        self.dispense_walkover_entry.config(state='normal')
        self.dispense_walkover_entry.insert(0, '-> enter location <-')
        self.dispense_signature_yes_btn.config(state='disabled', bg=self.btn_disabled_bg_color)
        self.dispense_signature_no_btn.config(state='disabled', bg=self.btn_disabled_bg_color)
        self.signature_required = ''
        self.dispense_signature_label.config(fg=self.disabled_text_color)
        self.dispense_date_label.config(text='Walking over on', fg=self.text_color)
        self.dispense_date_entry.config(state='normal')
        self.fedex_delivery_label.config(text='')
        self.top.focus()
        
    def remove_temp_text(self, e):
        """Remove temporary text from walk over entry box."""
        self.dispense_walkover_entry.delete(0, 'end')

    def _unselect_dcs_fedex(self):
        """Unselect DCS/FedEx button."""
        self.dispense_dcs_btn.config(bg=self.btn_bg_color, command=self.select_dcs)
        self.dispense_fedex_btn.config(bg=self.btn_bg_color, command=self.select_fedex)
        self.dispense_pickup_btn.config(bg=self.btn_bg_color, command=self.select_pickup)
        self.dispense_walkover_btn.config(bg=self.btn_bg_color, command=self.select_walkover)
        self.dispense_method = ''
        self.dispense_walkover_entry.delete(0, 'end')
        self.dispense_walkover_entry.config(state='disabled')
        self.dispense_date_label.config(text='Dispense Date:', fg=self.btn_disabled_fg_color)
        self.dispense_date_entry.delete(0, 'end')
        self.dispense_date_entry.config(state='disabled')
        self.signature_required = ''
        self.dispense_signature_label.config(fg=self.disabled_text_color)
        self.dispense_signature_yes_btn.config(state='disabled', bg=self.btn_disabled_bg_color)
        self.dispense_signature_no_btn.config(state='disabled', bg=self.btn_disabled_bg_color)
        self.fedex_delivery_label.config(text='')
  
    def _unselect_pickup_walkover(self):
        """Unselect Pick Up/Walk Over button."""
        self.dispense_dcs_btn.config(bg=self.btn_bg_color, command=self.select_dcs)
        self.dispense_fedex_btn.config(bg=self.btn_bg_color, command=self.select_fedex)
        self.dispense_pickup_btn.config(bg=self.btn_bg_color, command=self.select_pickup)
        self.dispense_walkover_btn.config(bg=self.btn_bg_color, command=self.select_walkover)
        self.dispense_method = ''
        self.dispense_walkover_entry.delete(0, 'end')
        self.dispense_walkover_entry.config(state='disabled')
        self.dispense_signature_yes_btn.config(state='normal', bg=self.btn_bg_color)
        self.dispense_signature_no_btn.config(state='normal', bg=self.btn_bg_color)
        self.dispense_date_label.config(text='Dispense Date:', fg=self.btn_disabled_fg_color)
        self.dispense_date_entry.delete(0, 'end')
        self.dispense_date_entry.config(state='disabled')
        self.signature_required = ''
        self.dispense_signature_label.config(fg=self.disabled_text_color)
        self.dispense_signature_yes_btn.config(state='disabled', bg=self.btn_disabled_bg_color)
        self.dispense_signature_no_btn.config(state='disabled', bg=self.btn_disabled_bg_color)

    def _enable_yes_no_btn(self):
        """Enable Yes and No buttons when selecting away from Pick Up or Walk Over."""
        self.dispense_signature_yes_btn.config(
            state='normal', bg=self.btn_bg_color, command=self.select_yes_sig,
            fg=self.btn_text_color
            )
        self.dispense_signature_no_btn.config(
            state='normal', bg=self.btn_bg_color, command=self.select_no_sig,
            fg=self.btn_text_color
            )

    def select_yes_sig(self):
        """Select Yes signature button."""
        self.dispense_signature_yes_btn.config(bg=self.select_btn_bg_color, command=self._unselect_yes_no_sig) 
        self.dispense_signature_no_btn.config(bg=self.btn_bg_color, command=self.select_no_sig)
        self.signature_required = 'signature required'

    def select_no_sig(self):
        """Select No signature button."""
        self.dispense_signature_yes_btn.config(bg=self.btn_bg_color, command=self.select_yes_sig) 
        self.dispense_signature_no_btn.config(bg=self.select_btn_bg_color, command=self._unselect_yes_no_sig)
        self.signature_required = 'no signature'

    def _unselect_yes_no_sig(self):
        """Unselect Yes/No signature button."""
        self.dispense_signature_yes_btn.config(bg=self.btn_bg_color, command=self.select_yes_sig) 
        self.dispense_signature_no_btn.config(bg=self.btn_bg_color, command=self.select_no_sig)
        self.signature_required = ''

    def select_a_little(self):
        """Select working 'A little' button."""
        self.medication_efficacy_alittle_btn.config(bg=self.select_btn_bg_color, command=self._unselect_alittle_alot_cant_tell)
        self.medication_efficacy_alot_btn.config(bg=self.btn_bg_color, command=self.select_a_lot)
        self.medication_efficacy_cantTell_btn.config(bg=self.btn_bg_color, command=self.select_cant_tell)
        self.medication_working = 'Yes, it\'s working a little.'

    def select_a_lot(self):
        """Select working 'A lot' button."""
        self.medication_efficacy_alittle_btn.config(bg=self.btn_bg_color, command=self.select_a_little)
        self.medication_efficacy_alot_btn.config(bg=self.select_btn_bg_color, command=self._unselect_alittle_alot_cant_tell)
        self.medication_efficacy_cantTell_btn.config(bg=self.btn_bg_color, command=self.select_cant_tell)
        self.medication_working = 'Yes, it\'s working a lot.'

    def select_cant_tell(self):
        """Select "Can't tell" button."""
        self.medication_efficacy_alittle_btn.config(bg=self.btn_bg_color, command=self.select_a_little)
        self.medication_efficacy_alot_btn.config(bg=self.btn_bg_color, command=self.select_a_lot)
        self.medication_efficacy_cantTell_btn.config(bg=self.select_btn_bg_color, command=self._unselect_alittle_alot_cant_tell)
        self.medication_working = 'No, I don\'t feel a difference.'

    def _unselect_alittle_alot_cant_tell(self):
        """Unselect a little/a lot/can't tell button."""
        self.medication_efficacy_alittle_btn.config(bg=self.btn_bg_color, command=self.select_a_little)
        self.medication_efficacy_alot_btn.config(bg=self.btn_bg_color, command=self.select_a_lot)
        self.medication_efficacy_cantTell_btn.config(bg=self.btn_bg_color, command=self.select_cant_tell)
        self.medication_working = ''

    def clear(self, e=None):
        """Clear all inputs."""
        self.medication_entry.delete(0, 'end')
        self.day_supply_entry.delete(0, 'end')
        self.dispense_date_entry.delete(0, 'end')
        self.dispense_comments_entry.delete(0, 'end')
        self.spoke_with_entry.delete(0, 'end')
        
        self._unselect_injection_cycle()
        self._unselect_yes_no_sig()
        self._unselect_dcs_fedex()
        self._unselect_alittle_alot_cant_tell()
        self.medication_entry.focus()

    def run_validations(self):
        """Recursively execute various validation methods."""
        self._validate_copy_btns()
        self._validate_fedex_delivery_label()
        self._update_variables()

        self.top.after(ms=50, func=self.run_validations)
    
    def _validate_copy_btns(self):
        """Check and enable copy buttons if conditions are met."""
        copy_wam_notes_conditions_met = self._check_copy_wam_notes_conditions()
        copy_template_conditions_met = self._check_copy_template_conditions()
        if copy_wam_notes_conditions_met:
            self.copy_wam_notes_btn.config(state='normal')
            if copy_template_conditions_met:
                self.copy_template_btn.config(state='normal')
        else:
            self.copy_wam_notes_btn.config(state='disabled')
            self.copy_template_btn.config(state='disabled')

    def _check_copy_wam_notes_conditions(self) -> bool:
        """Check if Copy WAM Notes conditions are met."""
        dispense_date_entry_not_empty = self.dispense_date_entry.get().strip()
        walkover_location = self.dispense_walkover_entry.get().strip()
        if self.dispense_method in ('DCS', 'FedEx') and dispense_date_entry_not_empty and self.signature_required\
        or self.dispense_method == 'Pick up' and dispense_date_entry_not_empty\
        or self.dispense_method == 'Walk over' and dispense_date_entry_not_empty and walkover_location not in ('-> enter location <-', ''):
            return True
        else:
            return False
        

    def _check_copy_template_conditions(self) -> bool:
        """Check if Copy Template conditions are met."""
        medication_entry_not_empty = self.medication_entry.get().strip()
        day_supply_entry_not_empty = self.day_supply_entry.get().strip()
        if medication_entry_not_empty and day_supply_entry_not_empty and self.medication_working and self.spoke_with:
            return True
        else:
            return False

    def _validate_fedex_delivery_label(self):
        """Check and enable FedEx delivery date label."""
        if self.dispense_method == 'FedEx':
            valid_delivery_date = self._calculate_fedex_delivery_date()
            if valid_delivery_date:
                self.fedex_delivery_date = valid_delivery_date
                self.fedex_delivery_label.config(text=f'for {self.fedex_delivery_date} delivery')
            else:
                self.fedex_delivery_date = ''
                self.fedex_delivery_label.config(text='')
        else:
            self.fedex_delivery_date = ''
            self.fedex_delivery_label.config(text='')


    def _calculate_fedex_delivery_date(self) -> str:
        """Calculate FedEx delivery date."""
        current_date = dt.datetime.now()
        split_ship_date = []
        try:
            entered_ship_date = self.dispense_date_entry.get().strip()
            if '/' in entered_ship_date:
                split_ship_date = entered_ship_date.split('/')
            elif '-' in entered_ship_date:
                split_ship_date = entered_ship_date.split('-')

            if split_ship_date:
                ship_month = int(split_ship_date[0])
                ship_day = int(split_ship_date[1])
                if current_date.month == 12:
                    if ship_month != 12:
                        ship_year = current_date.year + 1 # next year
                    else:
                        ship_year = current_date.year
                else:
                    ship_year = current_date.year

            delivery_date = dt.date(ship_year, ship_month, ship_day) + dt.timedelta(days=1)
            return f'{delivery_date.month}/{delivery_date.day}'
        except:
            return ''
        
    def _update_variables(self):
        """Update variables from user entry."""
        self.spoke_with = self.spoke_with_entry.get().strip()

    def get_existing_user(self) -> str:
        """Get existing user from user.json file."""
        try:
            with open('.data/user.json', 'r') as f:
                data = json.load(f)
                first_name = data['first_name']
                last_name = data['last_name']
                if first_name and last_name:
                    return f'{first_name} {last_name}'
                else:
                    raise Exception()
        except:
            return ''

    def _create_user_json(self, first_name: str, last_name: str):
        """Create user.json file."""
        with open('.data/user.json', 'w') as f:
            data = {'first_name': first_name, 'last_name': last_name}
            json.dump(data, f, indent=4)
    
    def _create_data_dir(self, path: str):
        """Create .data directory."""
        os.mkdir(path)
        subprocess.call(["attrib", "+h", path]) # hidden directory

    def user_setup_window(self, e=None):
        """Graphic user interface for setting up a new user."""

        def flash(entry_box, counter=4, color='#ffd7d0'):
            """Flash the given entry box a certain number of times."""
            duration1 = 100
            duration2 = 200
            for _ in range(counter):
                setup_window.after(duration1, lambda: entry_box.config(bg=color))
                setup_window.after(duration2, lambda: entry_box.config(bg=self.entry_bg_color))
                duration1 += 200
                duration2 += 200

        def confirm_user(e=None):
            """Confirm user first and last name."""
            first_name = first_name_entry.get().strip()
            last_name = last_name_entry.get().strip()

            if first_name and last_name:
                first_name_title = first_name.title()
                last_name_title = last_name.title()
                self._create_user_json(first_name_title, last_name_title)
                self.user = f'{first_name_title} {last_name_title}'
                self.top.title(f'Refill Coordination - {self.user}')
                self.top.attributes('-disabled', 0)
                self.top.deiconify()
                self.medication_entry.focus()
                setup_window.destroy()
            else:
                if first_name == '':
                    flash(first_name_entry)
                if last_name == '':
                    flash(last_name_entry)

        setup_window = tk.Toplevel(self.top)
        setup_window.withdraw()
        setup_window.title('User Setup')
        setup_window.config(bg=self.background_color, padx=20, pady=20)
        setup_window.resizable(False, False)

        first_name_label = tk.Label(
            setup_window, text='First Name:', bg=self.background_color, font=self.label_font
            )
        first_name_label.grid(column=0, row=0, padx=5)
        first_name_entry = tk.Entry(
            setup_window, font=self.entry_font, bg=self.entry_bg_color, relief=self.entry_relief
            )
        first_name_entry.grid(column=1, row=0, pady=(0, 5))
        
        last_name_label = tk.Label(
            setup_window, text='Last Name:', bg=self.background_color, font=self.label_font
            )
        last_name_label.grid(column=0, row=1, padx=5)
        last_name_entry = tk.Entry(
            setup_window, font=self.entry_font, bg=self.entry_bg_color, relief=self.entry_relief
            )
        last_name_entry.grid(column=1, row=1)

        ok_btn = tk.Button(
            setup_window, text='OK', bg=self.copy_btn_bg_color, relief='raised',
            font=self.btn_font, activebackground=self.copy_btn_bg_color, width=9,
            command=confirm_user
            )
        ok_btn.grid(column=0, row=2, columnspan=2, pady=(5, 0))

        # Center setup window to screen
        if self.user == '':
            setup_window.update_idletasks()
            setup_window_width = setup_window.winfo_reqwidth()
            setup_window_height = setup_window.winfo_reqheight()
            screen_width = setup_window.winfo_screenwidth()
            screen_height = setup_window.winfo_screenheight()
            x = int(screen_width/2 - setup_window_width/2)
            y = int(screen_height/2 - setup_window_width/2)
            setup_window.geometry(f"{setup_window_width}x{setup_window_height}+{x}+{y}")
            
        else: # center setup window to top window
            setup_window.update_idletasks()
            top_x = self.top.winfo_x()
            top_y = self.top.winfo_y()
            top_width = self.top.winfo_reqwidth()
            top_height = self.top.winfo_reqheight()
            setup_window_width = setup_window.winfo_reqwidth()
            setup_window_height = setup_window.winfo_reqheight()
            dx = int((top_width / 2) - (setup_window_width / 2))
            dy = int((top_height / 2) - (setup_window_height / 2))
            setup_window.geometry('+%d+%d' % (top_x + dx, top_y + dy))

        self.top.attributes('-disabled', 1)
        setup_window.wm_transient(self.top)
        setup_window.attributes('-topmost', 1)
        setup_window.deiconify()
        first_name_entry.focus()
        
        setup_window.protocol('WM_DELETE_WINDOW', lambda: self.on_closing_user_setup_window(setup_window))

        setup_window.bind('<Return>', confirm_user)
        setup_window.bind('<Escape>', lambda e: self.on_closing_user_setup_window(setup_window, e))

    def on_closing_user_setup_window(self, setup_window, e=None):
        """Enable top window on closing user setup window."""
        if self.user == '':
            sys.exit()

        self.top.attributes('-disabled', 0)
        self.top.deiconify()
        self.medication_entry.focus()
        setup_window.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    rt = RefillTemplate()

    root.mainloop()


# CF_RTF = win32clipboard.RegisterClipboardFormat("Rich Text Format")
# rtf = bytearray(fr'{{\rtf1\ansi\deff0 {{\fonttbl {{\f0 Times New Roman;}}}}{{\colortbl;\red0\green0\blue0;\red255\green0\blue0;\red255\green255\blue0;}} {text}}}', 'utf8')
