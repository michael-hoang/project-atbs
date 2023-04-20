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


class MainFrame(tkb.Frame):
    """MainFrame object that houses the side panel buttons and main display."""

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES)
        style = Style()
        style.configure('TLabelframe.Label', font=('', 12, 'bold'))

        # Initialize string variables
        refill_str_var_list = [
            'medication_name', 'days_on_hand', 'inj_cyc_btn',
            'inj_cyc_start_date', 'dispense_method_btn', 'dispense_date',
            'pickup_time', 'walkover_location', 'sig_required_btn',
            'dispense_comments', 'medication_efficacy_btn', 'spoke_with'
        ]

        self.refill_str_vars = {
            str_var: tkb.StringVar() for str_var in refill_str_var_list
        }

        # Initialize state of radio buttons
        tool_btn_list = [
            'Injection', 'Cycle', 'DCS', 'FedEx', 'Pick Up', 'Walk Over', 'Yes',
            'No', 'A lot', 'A little', 'Can\'t tell'
        ]
        self.tool_btn_states = {
            btn_state: 0 for btn_state in tool_btn_list
        }

        # # Side panel frame
        # side_panel_frame = tkb.Frame(self)
        # side_panel_frame.grid(row=0, column=0, sticky=NSEW)

        # # Side panel buttons
        # refill_btn = self.create_side_panel_btn(side_panel_frame, 'Refill')

        # Main display frame
        main_display_frame = tkb.Frame(self)
        main_display_frame.grid(row=0, column=1, sticky=NSEW)

        # ===== TOOLBAR ===== #

        # Toolbar container
        toolbar_container = tkb.Frame(
            master=main_display_frame
        )
        toolbar_container.grid(row=0, column=0, pady=10)

        # Toggle intervention button
        intervention_toggle_btn = tkb.Checkbutton(
            master=toolbar_container,
            bootstyle='round-toggle',
            text='Intervention'
        )
        intervention_toggle_btn.grid(row=0, column=0, padx=(10, 0))

        # Clear button
        clear_btn = tkb.Button(
            master=toolbar_container,
            text='Clear',
        )
        clear_btn.grid(row=0, column=1, padx=(240, 0))

        # ===== NOTEBOOK ===== #

        # Notebook
        notebook = tkb.Notebook(main_display_frame)
        notebook.grid(row=1, column=0, columnspan=3)

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
            refill_questions_frame, 'Medication'
        )
        medication_on_hand_labelframe = self.create_labelframe(
            refill_questions_frame, 'Medication On Hand'
        )
        dispense_date_labelframe = self.create_labelframe(
            refill_questions_frame, 'Dispense Date'
        )
        medication_efficacy_labelframe = self.create_labelframe(
            refill_questions_frame, 'Medication Efficacy'
        )
        spoke_with_labelframe = self.create_labelframe(
            refill_questions_frame, 'Spoke with', False
        )

        # Medication

        # Row 1
        medication_row_1 = self.create_inner_frame(medication_labelframe)

        medication_entry = tkb.Entry(
            master=medication_row_1,
            textvariable=self.refill_str_vars['medication_name']
        )
        medication_entry.pack(fill=BOTH)

        # Medication on hand

        # Row 1
        medication_on_hand_row_1 = self.create_inner_frame(
            master=medication_on_hand_labelframe,
        )

        medication_on_hand_entry = self.create_short_entry(
            master=medication_on_hand_row_1,
            padding=False,
            text_var=self.refill_str_vars['days_on_hand']
        )

        medication_on_hand_days_label = self.create_label(
            master=medication_on_hand_row_1,
            text='day(s)'
        )

        # Row 2
        medication_on_hand_row_2 = self.create_inner_frame(
            master=medication_on_hand_labelframe,
        )

        self.medication_on_hand_injection_btn = self.create_tool_btn(
            master=medication_on_hand_row_2,
            text='Injection',
            variable=self.refill_str_vars['inj_cyc_btn'],
            value='Injection',
            command=lambda: self.click_injection_cycle_btn(
                'Injection', 'is due'),
            padding=False
        )

        self.medication_on_hand_cycle_btn = self.create_tool_btn(
            master=medication_on_hand_row_2,
            text='Cycle',
            variable=self.refill_str_vars['inj_cyc_btn'],
            value='Cycle',
            command=lambda: self.click_injection_cycle_btn('Cycle', 'starts')
        )

        self.medication_on_hand_due_start_label = self.create_label(
            master=medication_on_hand_row_2,
            text='',
            width=6
        )

        self.medication_on_hand_due_start_entry = self.create_short_entry(
            master=medication_on_hand_row_2,
            text_var=self.refill_str_vars['inj_cyc_start_date']
        )
        self.medication_on_hand_due_start_entry.pack_forget()

        # Dispense date

        # Row 1
        dispense_date_row_1 = self.create_inner_frame(dispense_date_labelframe)

        dispense_date_dcs_btn = self.create_tool_btn(
            master=dispense_date_row_1,
            text='DCS',
            padding=False,
            variable=self.refill_str_vars['dispense_method_btn'],
            value='DCS',
            command=lambda: self.click_dispense_method_btn(
                'DCS', 'Shipping out on'
            )
        )
        dispense_date_fedex_btn = self.create_tool_btn(
            master=dispense_date_row_1,
            text='FedEx',
            variable=self.refill_str_vars['dispense_method_btn'],
            value='FedEx',
            command=None
        )
        dispense_date_pickup_btn = self.create_tool_btn(
            master=dispense_date_row_1,
            text='Pick Up',
            variable=self.refill_str_vars['dispense_method_btn'],
            value='Pick up',
            command=None
        )
        dispense_date_walkover_btn = self.create_tool_btn(
            master=dispense_date_row_1,
            text='Walk Over',
            variable=self.refill_str_vars['dispense_method_btn'],
            value='Walk over',
            command=None
        )

        # Row 2
        dispense_date_row_2 = self.create_inner_frame(dispense_date_labelframe)

        dispense_date_method_label = self.create_label(
            master=dispense_date_row_2,
            text='Walking over on',
            padding=False
        )

        dispense_date_calendar = tkb.DateEntry(
            master=dispense_date_row_2,
        )
        dispense_date_calendar.entry.config(width=10)
        dispense_date_calendar.pack(side=LEFT, padx=(3, 0))

        dispense_date_time_to_label = self.create_label(
            master=dispense_date_row_2,
            text='Time:'
        )

        dispense_date_time_location_entry = self.create_short_entry(
            master=dispense_date_row_2
        )

        # Row 3
        dispense_date_row_3 = self.create_inner_frame(dispense_date_labelframe)

        dispense_date_signature_required_label = self.create_label(
            master=dispense_date_row_3,
            text='Signature required?',
            padding=False
        )

        dispense_date_yes_btn = self.create_tk_btn(
            master=dispense_date_row_3,
            text='Yes'
        )

        dispense_date_no_btn = self.create_tk_btn(
            master=dispense_date_row_3,
            text='No'
        )

        # Row 4
        dispense_date_row_4 = self.create_inner_frame(dispense_date_labelframe)

        dispense_date_comments_label = self.create_label(
            master=dispense_date_row_4,
            text='Comments:',
            padding=False
        )

        dispense_date_comments_entry = self.create_short_entry(
            master=dispense_date_row_4,
            width=30
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

        medication_efficacy_a_lot_btn = self.create_tk_btn(
            master=medication_efficacy_row_1,
            text='A lot'
        )

        medication_efficacy_a_little_btn = self.create_tk_btn(
            master=medication_efficacy_row_1,
            text='A little'
        )

        medication_efficacy_cant_tell_btn = self.create_tk_btn(
            master=medication_efficacy_row_1,
            text='Can\'t tell'
        )

        # Spoke with

        # Row 1
        spoke_with_row_1 = self.create_inner_frame(
            master=spoke_with_labelframe
        )

        spoke_with_entry = self.create_short_entry(
            master=spoke_with_row_1,
            padding=False,
            width=30
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
            intervention_questions_frame, 'Changes'
        )

        side_effects_labelframe = self.create_labelframe(
            intervention_questions_frame, 'Side Effects'
        )

        adherence_labelframe = self.create_labelframe(
            intervention_questions_frame, 'Adherence'
        )

        additional_notes_labelframe = self.create_labelframe(
            intervention_questions_frame, 'Additional Notes', False
        )

        # Changes

        # Row 1
        changes_row_1 = self.create_inner_frame(changes_labelframe)

        changes_dose_direction_btn = self.create_tk_btn(
            master=changes_row_1,
            text='Dose/Direction',
            padding=False
        )

        changes_medication_profile_btn = self.create_tk_btn(
            master=changes_row_1,
            text='Medication Profile'
        )

        changes_new_allergies_btn = self.create_tk_btn(
            master=changes_row_1,
            text='New Allergies'
        )

        # Row 2
        changes_row_2 = self.create_inner_frame(changes_labelframe)

        changes_medical_condition_btn = self.create_tk_btn(
            master=changes_row_2,
            text='Medical Conditions',
            padding=False
        )

        changes_other_btn = self.create_tk_btn(
            master=changes_row_2,
            text='Other'
        )

        # Row 3
        changes_row_3 = self.create_inner_frame(changes_labelframe)

        changes_textbox = self.create_text_box(master=changes_row_3)

        # Side effects

        # Row 1
        side_effects_row_1 = self.create_inner_frame(side_effects_labelframe)

        side_effects_other_btn = self.create_tk_btn(
            master=side_effects_row_1,
            text='Other',
            padding=False
        )

        side_effects_injection_site_rxn_btn = self.create_tk_btn(
            master=side_effects_row_1,
            text='Injection site reaction'
        )

        side_effects_hospitalized_er_btn = self.create_tk_btn(
            master=side_effects_row_1,
            text='Hospitalized/ER'
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

    def create_labelframe(self, master, text, padding=True):
        """Create a label frame."""
        labelframe = tkb.Labelframe(
            master=master,
            text=text,
            style='TLabelframe.Label',
            padding=10,
        )
        labelframe.pack(side=TOP, fill=BOTH, pady=(0, 10))
        if not padding:
            labelframe.pack_configure(pady=0)

        return labelframe

    def create_inner_frame(self, master):
        """Create an inner frame."""
        frame = tkb.Frame(master)
        frame.pack(anchor='w', fill=BOTH, pady=(10, 0))
        return frame

    def create_label(self, master, text, padding=True, width=DEFAULT):
        """Create a label."""
        label = tkb.Label(
            master=master,
            text=text,
            width=width,
            anchor='center'
        )
        label.pack(side=LEFT, padx=(3, 0))
        if not padding:
            label.pack_configure(padx=0)

        return label

    def create_short_entry(self, master, width=15, padding=True, text_var=None):
        """Create an entry field."""
        entry = tkb.Entry(
            master=master,
            width=width,
            textvariable=text_var
        )
        entry.pack(side=LEFT, padx=(3, 0))
        if not padding:
            entry.pack_configure(padx=0)

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

    def create_tool_btn(
            self, master, text, variable, value, command, padding=True
    ):
        """Create a rectangular toolbutton (radio button)."""
        tool_btn = tkb.Radiobutton(
            master=master,
            bootstyle='toolbutton',
            text=text,
            variable=variable,
            value=value,
            command=command
        )
        tool_btn.pack(side=LEFT, padx=(2, 0))
        if not padding:
            tool_btn.pack_configure(padx=0)

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

    def _update_radio_btn_states(self, btn_group: dict, btn_clicked: str):
        """
        (Helper method.)
        Update the state of all radio buttons in a particular radio button group.
        """
        for btn in btn_group:
            if btn == btn_clicked:
                btn_group[btn] = 1
            else:
                btn_group[btn] = 0

    def _select_injection_cycle_btn(self, btn_clicked: str, label: str):
        """
        (Helper method.)
        Update label text and radio button states. Display entry.
        """
        self.medication_on_hand_due_start_label.config(text=label)
        self._update_radio_btn_states(self.tool_btn_states, btn_clicked)
        self.medication_on_hand_due_start_entry.pack(side=LEFT, padx=(3, 0))

    def _unselect_injection_cycle_btn(self, btn_clicked: str):
        """
        (Helper method.)
        Remove label text and entry. Set radio button state to off.
        """
        self.refill_str_vars['inj_cyc_btn'].set(None)
        self.medication_on_hand_due_start_label.config(text='')
        self.tool_btn_states[btn_clicked] = 0
        self.medication_on_hand_due_start_entry.pack_forget()

    def click_injection_cycle_btn(self, btn_clicked: str, label: str):
        """Toggle label text and entry for the next injection/therapy cycle."""
        if self.tool_btn_states[btn_clicked] == 0:
            self._select_injection_cycle_btn(btn_clicked, label)
        else:
            self._unselect_injection_cycle_btn(btn_clicked)

    def click_dispense_method_btn(self, btn_clicked: str, label1: str, label2: str = None):
        """Toggle label texts, date entry, and time/location entry for dispensing."""
        if self.tool_btn_states[btn_clicked] == 0:
            pass


if __name__ == '__main__':
    app = tkb.Window(
        'Refill Coordination', 'litera', resizable=(False, False)
    )
    MainFrame(app)
    app.place_window_center()
    app.mainloop()
