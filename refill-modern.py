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

        # Initialize string variables
        refill_str_var_list = [
            'medication_name', 'days_on_hand', 'inj_cyc_btn',
            'inj_cyc_start_date', 'dispense_method_btn', 'dispense_date',
            'time_location', 'sig_required_btn', 'dispense_comments',
            'medication_efficacy_btn', 'spoke_with'
        ]

        self.refill_str_vars = {
            str_var: tkb.StringVar() for str_var in refill_str_var_list
        }

        # Initialize Radio Button states
        self.tool_btn_states = {
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
        ToolTip(clear_btn, 'Clear entries', delay=500)

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

        self.medication_on_hand_entry = self.create_short_entry(
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
                'inj_cyc_btn', 'Injection', 'is due'
            ),
            padding=False
        )

        self.medication_on_hand_cycle_btn = self.create_tool_btn(
            master=medication_on_hand_row_2,
            text='Cycle',
            variable=self.refill_str_vars['inj_cyc_btn'],
            value='Cycle',
            command=lambda: self.click_injection_cycle_btn(
                'inj_cyc_btn', 'Cycle', 'starts'
            )
        )

        self.medication_on_hand_due_start_label = self.create_label(
            master=medication_on_hand_row_2,
            text='',
            width=5
        )

        self.medication_on_hand_due_start_entry = self.create_short_entry(
            master=medication_on_hand_row_2,
            text_var=self.refill_str_vars['inj_cyc_start_date']
        )
        self.medication_on_hand_due_start_entry.pack_forget()

        # Dispense date

        # Row 1
        dispense_date_row_1 = self.create_inner_frame(
            master=dispense_date_labelframe,
            grid=True
        )
        dispense_date_row_1.grid(row=0, column=0, sticky='w', pady=(10, 0))

        dispense_date_dcs_btn = self.create_tool_btn(
            master=dispense_date_row_1,
            text='DCS',
            padding=False,
            variable=self.refill_str_vars['dispense_method_btn'],
            value='DCS',
            command=lambda: self.click_dispense_method_btn(
                'dispense_method_btn', 'DCS', 'Shipping out on'
            )
        )
        dispense_date_fedex_btn = self.create_tool_btn(
            master=dispense_date_row_1,
            text='FedEx',
            variable=self.refill_str_vars['dispense_method_btn'],
            value='FedEx',
            command=lambda: self.click_dispense_method_btn(
                'dispense_method_btn', 'FedEx', 'Shipping out on', 'for 4/12 delivery'
            )
        )
        dispense_date_pickup_btn = self.create_tool_btn(
            master=dispense_date_row_1,
            text='Pick Up',
            variable=self.refill_str_vars['dispense_method_btn'],
            value='Pick up',
            command=lambda: self.click_dispense_method_btn(
                'dispense_method_btn', 'Pick Up', 'Picking up on', 'Time:'
            )
        )
        dispense_date_walkover_btn = self.create_tool_btn(
            master=dispense_date_row_1,
            text='Walk Over',
            variable=self.refill_str_vars['dispense_method_btn'],
            value='Walk over',
            command=lambda: self.click_dispense_method_btn(
                'dispense_method_btn', 'Walk Over', 'Walking over on', '  to'
            )
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
            width=10
        )
        self.dispense_date_calendar.grid(row=0, column=1, padx=(3, 0))
        self.dispense_date_calendar.entry.delete(0, END)

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
            grid=True
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

        dispense_date_yes_btn = self.create_tool_btn(
            master=dispense_date_row_3,
            text='Yes',
            variable=self.refill_str_vars['sig_required_btn'],
            value='Yes',
            command=lambda: self.click_sig_required_btn(
                'sig_required_btn', 'Yes'
            )
        )

        dispense_date_no_btn = self.create_tool_btn(
            master=dispense_date_row_3,
            text='No',
            variable=self.refill_str_vars['sig_required_btn'],
            value='No',
            command=lambda: self.click_sig_required_btn(
                'sig_required_btn', 'No'
            )
        )

        self.copy_wam_notes_btn = tkb.Button(
            master=dispense_date_labelframe,
            text='Copy WAM\n    Notes',
            state='disabled'
        )
        self.copy_wam_notes_btn.grid(
            row=2, column=0, rowspan=2, padx=(278, 0), pady=(30, 0), ipady=1
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

        dispense_date_comments_entry = self.create_short_entry(
            master=dispense_date_row_4,
            width=30,
            text_var=self.refill_str_vars['dispense_comments']
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

        medication_efficacy_a_lot_btn = self.create_tool_btn(
            master=medication_efficacy_row_1,
            text='A lot',
            variable=self.refill_str_vars['medication_efficacy_btn'],
            value='A lot',
            command=lambda: self.click_medication_efficacy_btn(
                'medication_efficacy_btn', 'A lot'
            )
        )

        medication_efficacy_a_little_btn = self.create_tool_btn(
            master=medication_efficacy_row_1,
            text='A little',
            variable=self.refill_str_vars['medication_efficacy_btn'],
            value='A little',
            command=lambda: self.click_medication_efficacy_btn(
                'medication_efficacy_btn', 'A little'
            )
        )

        medication_efficacy_cant_tell_btn = self.create_tool_btn(
            master=medication_efficacy_row_1,
            text='Can\'t tell',
            variable=self.refill_str_vars['medication_efficacy_btn'],
            value='Can\'t tell',
            command=lambda: self.click_medication_efficacy_btn(
                'medication_efficacy_btn', 'Can\'t tell'
            )
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
            text_var=self.refill_str_vars['spoke_with']
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

    def create_short_entry(self, master, width=15, padding=True, text_var=None, grid=False):
        """Create an entry field."""
        entry = tkb.Entry(
            master=master,
            width=width,
            textvariable=text_var
        )
        if not grid:
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

    def clear_entries(self):
        """Clear all entries from Refill and Intervention forms."""
        self.medication_on_hand_due_start_label.config(text='')
        self.medication_on_hand_due_start_entry.pack_forget()
        self.dispense_date_method_label.config(text='Dispense Date:')
        self.dispense_date_time_to_label.config(text='')
        self.dispense_date_time_location_entry.grid_forget()
        for str_var in self.refill_str_vars:
            self.refill_str_vars[str_var].set('')

        for btn_group in self.tool_btn_states.values():
            for btn_state in btn_group:
                btn_group[btn_state] = 0

    def _update_radio_btn_states(self, btn_group, btn_clicked):
        """
        (Helper method)
        Update the state of all radio buttons in a particular radio button group.
        """
        for btn in self.tool_btn_states[btn_group]:
            if btn == btn_clicked:
                self.tool_btn_states[btn_group][btn] = 1
            else:
                self.tool_btn_states[btn_group][btn] = 0

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
        self.tool_btn_states[btn_group][btn_clicked] = 0
        self.medication_on_hand_due_start_entry.pack_forget()

    def click_injection_cycle_btn(self, btn_group: str, btn_clicked: str, label: str):
        """Toggle label text and entry for the next injection/therapy cycle."""
        if self.tool_btn_states[btn_group][btn_clicked] == 0:
            self._select_injection_cycle_btn(btn_group, btn_clicked, label)
        else:
            self._unselect_injection_cycle_btn(btn_group, btn_clicked)

    def _select_dispense_method_btn(self, btn_group, btn_clicked, label1, label2=None):
        """
        (Helper method)
        Update label text and radio button states. Display entry field.
        """
        self._update_radio_btn_states(btn_group, btn_clicked)
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
        self.tool_btn_states[btn_group][btn_clicked] = 0
        self.dispense_date_method_label.config(text='Dispense Date:')
        self.dispense_date_time_to_label.config(text='')
        self.dispense_date_calendar.entry.delete(0, END)
        self.dispense_date_time_location_entry.grid_forget()

    def click_dispense_method_btn(self, btn_group: str, btn_clicked: str, label1: str, label2: str = None):
        """Toggle label texts, date entry, and time/location entry for dispensing."""
        if self.tool_btn_states[btn_group][btn_clicked] == 0:
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
        if self.tool_btn_states[btn_group][btn_clicked] == 0:
            self._update_radio_btn_states(btn_group, btn_clicked)
        else:
            self.tool_btn_states[btn_group][btn_clicked] = 0
            self.refill_str_vars[btn_group].set(None)

    def click_medication_efficacy_btn(self, btn_group: str, btn_clicked: str):
        """Toggle `A lot`, `A little` and `Can't tell` buttons on or off."""
        if self.tool_btn_states[btn_group][btn_clicked] == 0:
            self._update_radio_btn_states(btn_group, btn_clicked)
        else:
            self.tool_btn_states[btn_group][btn_clicked] = 0
            self.refill_str_vars[btn_group].set(None)

    # Event bind callbacks

    def _check_if_fedex_selected(self, e):
        """Update FedEx delivery date label."""
        if self.tool_btn_states['dispense_method_btn']['FedEx'] == 1:
            self._update_fedex_delivery_label()


if __name__ == '__main__':
    app = tkb.Window(
        'Refill Coordination', 'superhero', resizable=(False, False)
    )
    MainFrame(app)
    app.place_window_center()
    app.mainloop()
