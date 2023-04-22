import datetime as dt
import json
import os
import sys
import subprocess
import tkinter as tk
import ttkbootstrap as tkb

from win32 import win32clipboard
from tkinter import WORD
from tkinter.ttk import Style
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip


class MainFrame(tkb.Frame):
    """MainFrame object that houses the side panel buttons and main display."""

    def __init__(self, master):
        """Initialize string variables, style, radio button states, and widgets."""
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES)
        style = Style()
        style.configure('TLabelframe.Label', font=('', 11, 'bold'))
        style.configure('TButton', font=('', 11, ''))
        style.configure('Roundtoggle.Toolbutton', font=('', 11, ''))  # broken
        style.configure('TNotebook.Tab', font=('', 9, ''))

        # Initialize string variables for solid toolbuttons (radiobuttons)
        refill_str_var_list = [
            'medication_name', 'days_on_hand', 'inj_cyc_btn',
            'inj_cyc_start_date', 'dispense_method_btn', 'dispense_date',
            'time_location', 'sig_required_btn', 'dispense_comments',
            'medication_efficacy_btn', 'spoke_with'
        ]

        self.refill_str_vars = {
            str_var: tkb.StringVar() for str_var in refill_str_var_list
        }

        # Initialize Radio Button states to manage selecting/unselecting of
        # solid toolbuttons (radiobuttons)
        self.solid_tool_btn_states = {
            'inj_cyc_btn': {
                'Injection': 0,
                'Cycle': 0,
            },
            'dispense_method_btn': {
                'DCS': 0,
                'FedEx': 0,
                'Pick Up': 0,
                'Walk Over': 0,
            },
            'sig_required_btn': {
                'Yes': 0,
                'No': 0,
            },
            'medication_efficacy_btn': {
                'A lot': 0,
                'A little': 0,
                'Can\'t tell': 0,
            }
        }

        # Initialize integer varaibles for toolbuttons (checkbuttons)
        intervention_int_var_list = [
            'dose_direction_btn', 'medication_profile_btn', 'new_allergies_btn',
            'medical_condition_btn', 'other_changes_btn', 'other_side_effects_btn',
            'injection_site_rxn_btn', 'hospitalized_er_btn'
        ]

        self.intervention_int_vars = {
            int_var: tkb.IntVar() for int_var in intervention_int_var_list
        }

        # Initialize lists to track any changes or symptoms reported
        self.changes = []
        self.symptoms = []

        # # Side panel frame
        # side_panel_frame = tkb.Frame(self)
        # side_panel_frame.grid(row=0, column=0, sticky=NSEW)

        # # Side panel buttons
        # refill_btn = self.create_side_panel_btn(side_panel_frame, 'Refill')

        # Main display frame
        main_display_frame = tkb.Frame(self)
        main_display_frame.grid(row=0, column=1, sticky=NSEW, pady=(15, 0))

        # ===== TOOL BUTTONS ===== #

        # Toggle intervention button
        self.intervention_toggle_state = tkb.IntVar()
        intervention_toggle_btn = tkb.Checkbutton(
            master=main_display_frame,
            bootstyle='round-toggle',
            text='Intervention',
            variable=self.intervention_toggle_state,
            onvalue=1,
            offvalue=0,
            command=None,
            style='Roundtoggle.Toolbutton'
        )
        intervention_toggle_btn.grid(
            row=0, column=0, padx=(15, 0), pady=(0, 15), sticky='w'
        )
        ToolTip(
            widget=intervention_toggle_btn,
            text='Toggle Intervention',
            delay=500
        )

        # Clear button
        clear_btn = tkb.Button(
            master=main_display_frame,
            text='Clear',
            command=self.clear_entries,
            style='TButton',
            width=6
        )
        clear_btn.grid(
            row=0, column=1, rowspan=2, padx=(235, 0), pady=(0, 655)
        )
        ToolTip(clear_btn, 'Clear entries and clipboard', delay=500)

        # ===== NOTEBOOK ===== #

        # Notebook
        notebook = tkb.Notebook(main_display_frame, style='TNotebook.Tab')
        notebook.grid(row=1, column=0, columnspan=3)
        clear_btn.lift()

        # ========================== REFILL ===================================#

        # Refill display frame (tab)
        refill_display_frame = tkb.Frame(
            master=notebook,
            padding=20,
        )
        refill_display_frame.pack()
        notebook.add(refill_display_frame, text='Refill')

        # ===== REFILL QUESTIONS ===== #

        # Labelframes
        refill_questions_frame = tkb.Frame(refill_display_frame)
        refill_questions_frame.pack(side=LEFT)

        medication_labelframe = self.create_labelframe(
            refill_questions_frame, 'Medication', 0
        )
        medication_on_hand_labelframe = self.create_labelframe(
            refill_questions_frame, 'Medication On Hand', 1
        )
        dispense_date_labelframe = self.create_labelframe(
            refill_questions_frame, 'Dispense Date', 2
        )
        medication_efficacy_labelframe = self.create_labelframe(
            refill_questions_frame, 'Medication Efficacy', 3
        )
        spoke_with_labelframe = self.create_labelframe(
            refill_questions_frame, 'Spoke with', 4, sticky='w', padding=False
        )

        self.copy_template_btn = tkb.Button(
            master=refill_questions_frame,
            text='Copy Template',
            state='disabled'
        )
        self.copy_template_btn.grid(
            row=4, column=0, padx=(251, 0), pady=(10, 0), ipady=5
        )
        ToolTip(
            widget=self.copy_template_btn,
            text='Copy Refill Coordination template to clipboard',
            delay=500
        )

        # Medication

        # Row 1
        medication_row_1 = self.create_inner_frame(medication_labelframe)

        medication_entry = tkb.Entry(
            master=medication_row_1,
            textvariable=self.refill_str_vars['medication_name']
        )
        medication_entry.pack(fill=BOTH)
        ToolTip(
            widget=medication_entry,
            text='Enter medication name',
            delay=500
        )

        # Medication on hand

        # Row 1
        medication_on_hand_row_1 = self.create_inner_frame(
            master=medication_on_hand_labelframe,
        )

        self.medication_on_hand_entry = self.create_short_entry(
            master=medication_on_hand_row_1,
            padding=False,
            text_var=self.refill_str_vars['days_on_hand'],
            tooltip='Enter day supply on hand'
        )

        medication_on_hand_days_label = self.create_label(
            master=medication_on_hand_row_1,
            text='day(s)'
        )

        # Row 2
        medication_on_hand_row_2 = self.create_inner_frame(
            master=medication_on_hand_labelframe,
        )

        self.medication_on_hand_injection_btn = self.create_solid_tool_btn(
            master=medication_on_hand_row_2,
            text='Injection',
            variable=self.refill_str_vars['inj_cyc_btn'],
            value='Injection',
            command=lambda: self.click_injection_cycle_btn(
                'inj_cyc_btn', 'Injection', 'is due'
            ),
            padding=False,
            tooltip='Enter when the next injection is due'
        )

        self.medication_on_hand_cycle_btn = self.create_solid_tool_btn(
            master=medication_on_hand_row_2,
            text='Cycle',
            variable=self.refill_str_vars['inj_cyc_btn'],
            value='Cycle',
            command=lambda: self.click_injection_cycle_btn(
                'inj_cyc_btn', 'Cycle', 'starts'
            ),
            tooltip='Enter when the next cycle starts'
        )

        self.medication_on_hand_due_start_label = self.create_label(
            master=medication_on_hand_row_2,
            text='',
            width=5
        )

        self.medication_on_hand_due_start_entry = self.create_short_entry(
            master=medication_on_hand_row_2,
            text_var=self.refill_str_vars['inj_cyc_start_date'],
            tooltip='Enter the next injection or cycle date'
        )
        self.medication_on_hand_due_start_entry.pack_forget()

        # Dispense date

        # Row 1
        dispense_date_row_1 = self.create_inner_frame(
            master=dispense_date_labelframe,
            grid=True
        )
        dispense_date_row_1.grid(row=0, column=0, sticky='w', pady=(10, 0))

        dispense_date_dcs_btn = self.create_solid_tool_btn(
            master=dispense_date_row_1,
            text='DCS',
            padding=False,
            variable=self.refill_str_vars['dispense_method_btn'],
            value='DCS',
            command=lambda: self.click_dispense_method_btn(
                'dispense_method_btn', 'DCS', 'Shipping out on'
            ),
            tooltip='DCS\nSame day delivery. Reserved strictly for Orange County.'
        )
        dispense_date_fedex_btn = self.create_solid_tool_btn(
            master=dispense_date_row_1,
            text='FedEx',
            variable=self.refill_str_vars['dispense_method_btn'],
            value='FedEx',
            command=lambda: self.click_dispense_method_btn(
                'dispense_method_btn', 'FedEx', 'Shipping out on', 'for 4/12 delivery'
            ),
            tooltip='FedEx\nNext day delivery. No fridge shipments on Thursdays.'
        )
        dispense_date_pickup_btn = self.create_solid_tool_btn(
            master=dispense_date_row_1,
            text='Pick Up',
            variable=self.refill_str_vars['dispense_method_btn'],
            value='Pick up',
            command=lambda: self.click_dispense_method_btn(
                'dispense_method_btn', 'Pick Up', 'Picking up on', 'Time:'
            ),
            tooltip='Pick Up'
        )
        dispense_date_walkover_btn = self.create_solid_tool_btn(
            master=dispense_date_row_1,
            text='Walk Over',
            variable=self.refill_str_vars['dispense_method_btn'],
            value='Walk over',
            command=lambda: self.click_dispense_method_btn(
                'dispense_method_btn', 'Walk Over', 'Walking over on', '  to'
            ),
            tooltip='Clinic delivery\n(i.e. PAV 1, PAV 3, Inpatient)'
        )

        # Row 2
        dispense_date_row_2 = self.create_inner_frame(
            master=dispense_date_labelframe,
            grid=True
        )
        dispense_date_row_2.grid(row=1, column=0, sticky='w', pady=(10, 0))

        self.dispense_date_method_label = self.create_label(
            master=dispense_date_row_2,
            text='Dispense Date:',
            width=15,
            grid=True
        )
        self.dispense_date_method_label.grid(row=0, column=0)

        self.dispense_date_calendar = tkb.DateEntry(
            master=dispense_date_row_2,
        )
        self.dispense_date_calendar.entry.config(
            textvariable=self.refill_str_vars['dispense_date'],
            width=10,
            state='disabled'
        )
        self.dispense_date_calendar.button.config(state='disabled')
        self.dispense_date_calendar.grid(row=0, column=1, padx=(3, 0))
        self.dispense_date_calendar.entry.delete(0, END)
        ToolTip(
            widget=self.dispense_date_calendar.button,
            text='Select dispense date',
            delay=500
        )

        self.dispense_date_time_to_label = self.create_label(
            master=dispense_date_row_2,
            text='',
            grid=True
        )
        self.dispense_date_time_to_label.grid(
            row=0, column=2, sticky='w', padx=(3, 0)
        )

        self.dispense_date_time_location_entry = self.create_short_entry(
            master=dispense_date_row_2,
            text_var=self.refill_str_vars['time_location'],
            grid=True,
            tooltip='Pick Up: Enter pick up time\nWalk Over: Enter walk over location'
        )
        self.dispense_date_time_location_entry.grid(
            row=0, column=3, padx=(3, 0)
        )
        dispense_date_row_2.columnconfigure(2, minsize=148)
        self.dispense_date_time_location_entry.grid_forget()

        # Row 3
        dispense_date_row_3 = self.create_inner_frame(
            master=dispense_date_labelframe,
            grid=True
        )
        dispense_date_row_3.grid(row=2, column=0, sticky='w', pady=(10, 0))

        dispense_date_signature_required_label = self.create_label(
            master=dispense_date_row_3,
            text='Signature required?',
            padding=False
        )

        self.dispense_date_yes_btn = self.create_solid_tool_btn(
            master=dispense_date_row_3,
            text='Yes',
            variable=self.refill_str_vars['sig_required_btn'],
            value='Yes',
            command=lambda: self.click_sig_required_btn(
                'sig_required_btn', 'Yes'
            ),
            state='disabled',
            tooltip='Signature required\n(Required for Medicare Part B and Humana Part D)'
        )

        self.dispense_date_no_btn = self.create_solid_tool_btn(
            master=dispense_date_row_3,
            text='No',
            variable=self.refill_str_vars['sig_required_btn'],
            value='No',
            command=lambda: self.click_sig_required_btn(
                'sig_required_btn', 'No'
            ),
            state='disabled',
            tooltip='No signature required'
        )

        self.copy_wam_notes_btn = tkb.Button(
            master=dispense_date_labelframe,
            text='Copy WAM\n    Notes',
            state='disabled'
        )
        self.copy_wam_notes_btn.grid(
            row=2, column=0, rowspan=2, padx=(278, 0), pady=(30, 0), ipady=1
        )
        ToolTip(
            widget=self.copy_wam_notes_btn,
            text='Copy WAM dispense notes to clipboard',
            delay=500
        )

        # Row 4
        dispense_date_row_4 = self.create_inner_frame(
            master=dispense_date_labelframe,
            grid=True
        )
        dispense_date_row_4.grid(row=3, column=0, sticky='w', pady=(10, 0))

        dispense_date_comments_label = self.create_label(
            master=dispense_date_row_4,
            text='Comments:',
            padding=False
        )

        self.dispense_date_comments_entry = self.create_short_entry(
            master=dispense_date_row_4,
            width=30,
            text_var=self.refill_str_vars['dispense_comments'],
            tooltip='Enter any dispense, pick up, or delivery comments',
            state='disabled'
        )

        # Medication Efficacy

        # Row 1
        medication_efficacy_row_1 = self.create_inner_frame(
            master=medication_efficacy_labelframe
        )

        medication_efficacy_is_working_label = self.create_label(
            master=medication_efficacy_row_1,
            text='Is medication working?',
            padding=False
        )

        medication_efficacy_a_lot_btn = self.create_solid_tool_btn(
            master=medication_efficacy_row_1,
            text='A lot',
            variable=self.refill_str_vars['medication_efficacy_btn'],
            value='A lot',
            command=lambda: self.click_medication_efficacy_btn(
                'medication_efficacy_btn', 'A lot'
            ),
            tooltip='Medication is working a lot'
        )

        medication_efficacy_a_little_btn = self.create_solid_tool_btn(
            master=medication_efficacy_row_1,
            text='A little',
            variable=self.refill_str_vars['medication_efficacy_btn'],
            value='A little',
            command=lambda: self.click_medication_efficacy_btn(
                'medication_efficacy_btn', 'A little'
            ),
            tooltip='Medication is working a little'
        )

        medication_efficacy_cant_tell_btn = self.create_solid_tool_btn(
            master=medication_efficacy_row_1,
            text='Can\'t tell',
            variable=self.refill_str_vars['medication_efficacy_btn'],
            value='Can\'t tell',
            command=lambda: self.click_medication_efficacy_btn(
                'medication_efficacy_btn', 'Can\'t tell'
            ),
            tooltip='Can\'t tell if medication is working'
        )

        # Spoke with

        # Row 1
        spoke_with_row_1 = self.create_inner_frame(
            master=spoke_with_labelframe
        )

        spoke_with_entry = self.create_short_entry(
            master=spoke_with_row_1,
            padding=False,
            width=35,
            text_var=self.refill_str_vars['spoke_with'],
            tooltip='Name of the person you spoke with'
        )

        # ========================= INTERVENTION ==============================#

        # Intervention display frame (tab)
        intervention_display_frame = tkb.Frame(
            master=notebook,
            padding=20,
        )
        intervention_display_frame.pack()
        notebook.add(intervention_display_frame, text='Intervention')

        # ===== INTERVENTION QUESTIONS ===== #

        # Labelframes
        intervention_questions_frame = tkb.Frame(intervention_display_frame)
        intervention_questions_frame.pack(side=LEFT)

        changes_labelframe = self.create_labelframe(
            intervention_questions_frame, 'Changes', 0
        )

        side_effects_labelframe = self.create_labelframe(
            intervention_questions_frame, 'Side Effects', 1
        )

        adherence_labelframe = self.create_labelframe(
            intervention_questions_frame, 'Adherence', 2
        )

        additional_notes_labelframe = self.create_labelframe(
            intervention_questions_frame, 'Additional Notes', 3, padding=False
        )

        # Changes

        # Row 1
        changes_row_1 = self.create_inner_frame(changes_labelframe)

        changes_dose_direction_btn = self.create_tool_btn(
            master=changes_row_1,
            text='Dose/Direction',
            variable=self.intervention_int_vars['dose_direction_btn'],
            command=lambda: self.click_intervention_tool_btns(
                btn_clicked='dose_direction_btn',
                list=self.changes,
                value='Change to dose/directions of current medication'
            ),
            padding=False,
            tooltip='Changes to dose or direction of current medication'
        )

        changes_medication_profile_btn = self.create_tool_btn(
            master=changes_row_1,
            text='Medication Profile',
            variable=self.intervention_int_vars['medication_profile_btn'],
            command=lambda: self.click_intervention_tool_btns(
                btn_clicked='medication_profile_btn',
                list=self.changes,
                value='Change to medication profile',
            ),
            tooltip='Change to medication profile'
        )

        changes_new_allergies_btn = self.create_tool_btn(
            master=changes_row_1,
            text='New Allergies',
            variable=self.intervention_int_vars['new_allergies_btn'],
            command=lambda: self.click_intervention_tool_btns(
                btn_clicked='new_allergies_btn',
                list=self.changes,
                value='Changes in allergies'
            ),
            tooltip='Changes in allergies'
        )

        # Row 2
        changes_row_2 = self.create_inner_frame(changes_labelframe)

        changes_medical_condition_btn = self.create_tool_btn(
            master=changes_row_2,
            text='Medical Conditions',
            variable=self.intervention_int_vars['medical_condition_btn'],
            command=lambda: self.click_intervention_tool_btns(
                btn_clicked='medical_condition_btn',
                list=self.changes,
                value='New Medication Condition(s)'
            ),
            padding=False,
            tooltip='Patient has new medical condition(s)'
        )

        changes_other_btn = self.create_tool_btn(
            master=changes_row_2,
            text='Other',
            variable=self.intervention_int_vars['other_changes_btn'],
            command=lambda: self.click_intervention_tool_btns(
                btn_clicked='other_changes_btn',
                list=self.changes,
                value='Other'
            ),
            tooltip='Patient has other changes.\nAdd details in the text box below.'
        )

        # Row 3
        changes_row_3 = self.create_inner_frame(changes_labelframe)

        changes_textbox = self.create_text_box(master=changes_row_3)

        # Side effects

        # Row 1
        side_effects_row_1 = self.create_inner_frame(side_effects_labelframe)

        side_effects_other_btn = self.create_tool_btn(
            master=side_effects_row_1,
            text='Other',
            variable=self.intervention_int_vars['other_side_effects_btn'],
            command=lambda: self.click_intervention_tool_btns(
                btn_clicked='other_side_effects_btn',
                list=self.symptoms,
                value='Other'
            ),
            padding=False,
            tooltip='Patient has other symptoms or side effects'
        )

        side_effects_injection_site_rxn_btn = self.create_tool_btn(
            master=side_effects_row_1,
            text='Injection site reaction',
            variable=self.intervention_int_vars['injection_site_rxn_btn'],
            command=lambda: self.click_intervention_tool_btns(
                btn_clicked='injection_site_rxn_btn',
                list=self.symptoms,
                value='Injection site reaction'
            ),
            tooltip='Patient has injection site reaction'
        )

        side_effects_hospitalized_er_btn = self.create_tool_btn(
            master=side_effects_row_1,
            text='Hospitalized/ER',
            variable=self.intervention_int_vars['hospitalized_er_btn'],
            command=lambda: self.click_intervention_tool_btns(
                btn_clicked='hospitalized_er_btn',
                list=self.symptoms,
                value='Hospitalized/ER visit'
            ),
            tooltip='Patient was hospitalized or had an ER visit'
        )

        # Row 2
        side_effects_row_2 = self.create_inner_frame(side_effects_labelframe)

        side_effects_textbox = self.create_text_box(side_effects_row_2)

        # Adherence

        # Row 1
        adherence_row_1 = self.create_inner_frame(adherence_labelframe)

        adherence_textbox = self.create_text_box(adherence_row_1)

        # Additional notes

        # Row 1
        additional_notes_row_1 = self.create_inner_frame(
            additional_notes_labelframe
        )

        additional_notes_textbox = self.create_text_box(additional_notes_row_1)

    # Events and binds
        self.dispense_date_calendar.bind(
            '<FocusIn>', self._check_if_fedex_selected
        )

    # Widget Creation Methods

    def create_side_panel_btn(self, master, text):
        """Create side panel buttons."""
        btn = tkb.Button(
            master=master,
            text=text,
            compound=TOP,
            bootstyle=INFO
        )
        btn.pack(side=TOP, fill=BOTH, ipadx=10, ipady=10)
        return btn

    def create_labelframe(self, master, text, row, col=0, sticky='we', padding=True):
        """Create a label frame."""
        labelframe = tkb.Labelframe(
            master=master,
            text=text,
            style='TLabelframe.Label',
            padding=10,
        )
        labelframe.grid(row=row, column=col, sticky=sticky, pady=(0, 10))
        if not padding:
            labelframe.grid_configure(pady=0)

        return labelframe

    def create_inner_frame(self, master, grid=False):
        """Create an inner frame."""
        frame = tkb.Frame(master)
        if not grid:
            frame.pack(anchor='w', fill=BOTH, pady=(10, 0))

        return frame

    def create_label(self, master, text, anchor='e',  width=DEFAULT, padding=True, grid=False):
        """Create a label."""
        label = tkb.Label(
            master=master,
            text=text,
            width=width,
            anchor=anchor,
            font=('', 10, '')
        )
        if not grid:
            label.pack(side=LEFT, padx=(3, 0))
            if not padding:
                label.pack_configure(padx=0)

        return label

    def create_short_entry(self, master, width=15, padding=True, text_var=None, state='normal', grid=False, tooltip=''):
        """Create an entry field."""
        entry = tkb.Entry(
            master=master,
            width=width,
            textvariable=text_var,
            state=state
        )
        if not grid:
            entry.pack(side=LEFT, padx=(3, 0))
            if not padding:
                entry.pack_configure(padx=0)

        ToolTip(widget=entry, text=tooltip, delay=500)
        return entry

    def create_tk_btn(self, master, text, padding=True):
        """Create a Tk button."""
        btn = tk.Button(
            master=master,
            text=text,
            activeforeground='white',
            padx=6,
            pady=3,
        )
        btn.pack(side=LEFT, padx=(2, 0))
        if not padding:
            btn.pack_configure(padx=0)

        return btn

    def create_solid_tool_btn(
            self, master, text, variable, value, command, padding=True, state='normal', tooltip=''
    ):
        """Create a rectangular solid toolbutton (Radiobutton)."""
        solid_tool_btn = tkb.Radiobutton(
            master=master,
            bootstyle='toolbutton',
            text=text,
            variable=variable,
            value=value,
            command=command,
            state=state
        )
        solid_tool_btn.pack(side=LEFT, padx=(2, 0))
        if not padding:
            solid_tool_btn.pack_configure(padx=0)

        ToolTip(solid_tool_btn, text=tooltip, delay=500)
        return solid_tool_btn

    def create_tool_btn(
            self, master, text, variable, command, padding=True, state='normal', tooltip=''
    ):
        """Create a rectangular toolbutton (Checkbutton)."""
        tool_btn = tkb.Checkbutton(
            master=master,
            bootstyle='toolbutton',
            text=text,
            variable=variable,
            command=command,
            state=state
        )
        tool_btn.pack(side=LEFT, padx=(2, 0))
        if not padding:
            tool_btn.pack_configure(padx=0)

        ToolTip(tool_btn, text=tooltip, delay=500)
        return tool_btn

    def create_text_box(self, master):
        """Create a Tk text box."""
        textbox = tk.Text(
            master=master,
            wrap=WORD,
            height=3,
            width=53,
        )
        textbox.pack(side=LEFT, fill=BOTH)
        return textbox

    # Various methods for button commands

    def clear_entries(self):
        """Clear all entries from Refill and Intervention forms."""
        self.medication_on_hand_due_start_label.config(text='')
        self.medication_on_hand_due_start_entry.pack_forget()
        self.dispense_date_method_label.config(text='Dispense Date:')
        self.dispense_date_time_to_label.config(text='')
        self.dispense_date_time_location_entry.grid_forget()
        self._enable_disable_dispense_widgets('disabled')
        for str_var in self.refill_str_vars:
            self.refill_str_vars[str_var].set('')

        for btn_group in self.solid_tool_btn_states.values():
            for btn_state in btn_group:
                btn_group[btn_state] = 0

    def _update_radio_btn_states(self, btn_group, btn_clicked):
        """
        (Helper method)
        Update the state of all radio buttons in a particular radio button group.
        """
        for btn in self.solid_tool_btn_states[btn_group]:
            if btn == btn_clicked:
                self.solid_tool_btn_states[btn_group][btn] = 1
            else:
                self.solid_tool_btn_states[btn_group][btn] = 0

    def _select_injection_cycle_btn(self, btn_group, btn_clicked, label):
        """
        (Helper method)
        Update label text and radio button states. Display entry field.
        """
        if self.medication_on_hand_entry.get() == '':
            self.medication_on_hand_entry.insert(0, '0')
        self.medication_on_hand_due_start_label.config(text=label)
        self._update_radio_btn_states(btn_group, btn_clicked)
        self.medication_on_hand_due_start_entry.pack(side=LEFT, padx=(3, 0))

    def _unselect_injection_cycle_btn(self, btn_group, btn_clicked):
        """
        (Helper method)
        Remove label text and entry. Set radio button state to off.
        """
        self.refill_str_vars[btn_group].set(None)
        self.medication_on_hand_due_start_label.config(text='')
        self.solid_tool_btn_states[btn_group][btn_clicked] = 0
        self.medication_on_hand_due_start_entry.pack_forget()

    def click_injection_cycle_btn(self, btn_group: str, btn_clicked: str, label: str):
        """Toggle label text and entry for the next injection/therapy cycle."""
        if self.solid_tool_btn_states[btn_group][btn_clicked] == 0:
            self._select_injection_cycle_btn(btn_group, btn_clicked, label)
        else:
            self._unselect_injection_cycle_btn(btn_group, btn_clicked)

    def _enable_disable_dispense_widgets(self, state: str):
        """
        Enable/disable dispense widgets once a dispense method button is selected/unselected.
        """
        widgets = [
            self.dispense_date_calendar.entry, self.dispense_date_calendar.button,
            self.dispense_date_yes_btn, self.dispense_date_no_btn,
            self.dispense_date_comments_entry
        ]
        for widget in widgets:
            widget.config(state=state)

    def _select_dispense_method_btn(self, btn_group, btn_clicked, label1, label2=None):
        """
        (Helper method)
        Update label text and radio button states. Display entry field.
        """
        self._update_radio_btn_states(btn_group, btn_clicked)
        self._enable_disable_dispense_widgets(state='normal')
        if btn_clicked == 'DCS':
            self.dispense_date_method_label.config(text=label1)
            self.dispense_date_time_to_label.config(text='')
            self.dispense_date_time_location_entry.grid_forget()
        elif btn_clicked == 'FedEx':
            self.dispense_date_method_label.config(text=label1)
            self._update_fedex_delivery_label()
            self.dispense_date_time_location_entry.grid_forget()
        elif btn_clicked == 'Pick Up' or btn_clicked == 'Walk Over':
            self.dispense_date_method_label.config(text=label1)
            self.dispense_date_time_to_label.config(text=label2)
            self.dispense_date_time_location_entry.delete(0, END)
            self.dispense_date_time_location_entry.grid(
                row=0, column=2, columnspan=2, padx=(35, 0)
            )
        else:
            self.dispense_date_time_to_label.config(text='')

    def _unselect_dispense_method_btn(self, btn_group, btn_clicked):
        """
        (Helper method)
        Update label text and radio button states. Display entry field.
        """
        self.refill_str_vars[btn_group].set(None)
        self.solid_tool_btn_states[btn_group][btn_clicked] = 0
        self.dispense_date_method_label.config(text='Dispense Date:')
        self.dispense_date_time_to_label.config(text='')
        self.dispense_date_calendar.entry.delete(0, END)
        self.dispense_date_time_location_entry.grid_forget()
        self._enable_disable_dispense_widgets(state='disabled')

    def click_dispense_method_btn(self, btn_group: str, btn_clicked: str, label1: str, label2: str = None):
        """Toggle label texts, date entry, and time/location entry for dispensing."""
        if self.solid_tool_btn_states[btn_group][btn_clicked] == 0:
            self._select_dispense_method_btn(
                btn_group, btn_clicked, label1, label2
            )
        else:
            self._unselect_dispense_method_btn(btn_group, btn_clicked)

    def get_fedex_delivery_date(self) -> str:
        """Calculate and return FedEx delivery date."""
        ship_date = self.dispense_date_calendar.entry.get().strip()
        if ship_date:
            try:
                ship_date_dt = dt.datetime.strptime(ship_date, '%m/%d/%Y')
                delivery_date = ship_date_dt + dt.timedelta(days=1)
                return f'{delivery_date.month}/{delivery_date.day}'
            except:
                return ''
        else:
            return ''

    def _update_fedex_delivery_label(self):
        delivery_date = self.get_fedex_delivery_date().strip()
        if delivery_date:
            self.dispense_date_time_to_label.config(
                text=f'for {delivery_date} delivery'
            )
        else:
            self.dispense_date_time_to_label.config(text='')

    def click_sig_required_btn(self, btn_group: str, btn_clicked: str):
        """Toggle the 'Yes' and 'No' buttons on or off if signature is required."""
        if self.solid_tool_btn_states[btn_group][btn_clicked] == 0:
            self._update_radio_btn_states(btn_group, btn_clicked)
        else:
            self.solid_tool_btn_states[btn_group][btn_clicked] = 0
            self.refill_str_vars[btn_group].set(None)

    def click_medication_efficacy_btn(self, btn_group: str, btn_clicked: str):
        """Toggle `A lot`, `A little` and `Can't tell` buttons on or off."""
        if self.solid_tool_btn_states[btn_group][btn_clicked] == 0:
            self._update_radio_btn_states(btn_group, btn_clicked)
        else:
            self.solid_tool_btn_states[btn_group][btn_clicked] = 0
            self.refill_str_vars[btn_group].set(None)

    def click_intervention_tool_btns(self, btn_clicked: str, list: list, value: str):
        """Append or remove values from changes or symptoms list."""
        if self.intervention_int_vars[btn_clicked].get() == 1:
            list.append(value)
        else:
            list.remove(value)

    # Event bind callbacks

    def _check_if_fedex_selected(self, e):
        """Update FedEx delivery date label."""
        if self.solid_tool_btn_states['dispense_method_btn']['FedEx'] == 1:
            self._update_fedex_delivery_label()


if __name__ == '__main__':
    app = tkb.Window(
        'Refill Coordination', 'litera', resizable=(False, False)
    )
    MainFrame(app)
    app.place_window_center()
    app.mainloop()
