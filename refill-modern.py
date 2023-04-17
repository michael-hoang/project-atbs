import datetime as dt
import json
import os
import sys
import subprocess
import tkinter as tk
import ttkbootstrap as tkb

from win32 import win32clipboard
from tkinter import WORD
from ttkbootstrap.constants import *


class MainFrame(tkb.Frame):
    """MainFrame object that houses the side panel buttons and main display."""

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES)

        # Side panel frame
        side_panel_frame = tkb.Frame(self)
        side_panel_frame.grid(row=0, column=0, sticky=NSEW)

        # Side panel buttons
        refill_btn = self.create_side_panel_btn(side_panel_frame, 'Refill')

        # Main display frame
        main_display_frame = tkb.Frame(self)
        main_display_frame.grid(row=0, column=1, sticky=NSEW)

        # ========================== REFILL ===================================#

        # Refill display frame
        refill_display_frame = tkb.Frame(
            master=main_display_frame,
            padding=20,
        )
        refill_display_frame.pack()

        # ===== REFILL QUESTIONS =====#

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
            refill_questions_frame, 'Spoke with'
        )

        # Medication

        # Row 1
        medication_row_1 = self.create_inner_frame(medication_labelframe)

        medication_entry = tkb.Entry(medication_row_1)
        medication_entry.pack(fill=BOTH)

        # Medication on hand

        # Row 1
        medication_on_hand_row_1 = self.create_inner_frame(
            master=medication_on_hand_labelframe,
        )

        medication_on_hand_entry = tkb.Entry(
            master=medication_on_hand_row_1,
            width=15,
        )
        medication_on_hand_entry.pack(side=LEFT)

        medication_on_hand_days_label = tkb.Label(
            master=medication_on_hand_row_1,
            text='day(s)',
        )
        medication_on_hand_days_label.pack(side=LEFT, padx=(2, 0))

        # Row 2
        medication_on_hand_row_2 = self.create_inner_frame(
            master=medication_on_hand_labelframe,
        )

        medication_on_hand_injection_btn = self.create_tk_btn(
            master=medication_on_hand_row_2,
            text='Injection',
            padding=False
        )

        medication_on_hand_cycle_btn = self.create_tk_btn(
            master=medication_on_hand_row_2,
            text='Cycle',
        )

        medication_on_hand_due_start_label = tkb.Label(
            master=medication_on_hand_row_2,
            text='is due',
        )
        medication_on_hand_due_start_label.pack(side=LEFT, padx=(2, 0))

        medication_on_hand_due_start_entry = tkb.Entry(
            master=medication_on_hand_row_2,
            width=15,
        )
        medication_on_hand_due_start_entry.pack(side=LEFT, padx=(2, 0))

        # Dispense date

        # Row 1
        dispense_date_row_1 = self.create_inner_frame(dispense_date_labelframe)

        dispense_date_dcs_btn = self.create_tk_btn(
            master=dispense_date_row_1,
            text='DCS',
            padding=False
        )
        dispense_date_fedex_btn = self.create_tk_btn(
            master=dispense_date_row_1,
            text='FedEx'
        )
        dispense_date_pickup_btn = self.create_tk_btn(
            master=dispense_date_row_1,
            text='Pick Up'
        )
        dispense_date_walkover_btn = self.create_tk_btn(
            master=dispense_date_row_1,
            text='Walk Over'
        )

        # Row 2
        dispense_date_row_2 = self.create_inner_frame(dispense_date_labelframe)

        dispense_date_method_label = tkb.Label(
            master=dispense_date_row_2,
            text='Walking over on'
        )
        dispense_date_method_label.pack(side=LEFT)

        dispense_date_calendar = tkb.DateEntry(
            master=dispense_date_row_2,
        )
        dispense_date_calendar.entry.config(width=10)
        dispense_date_calendar.pack(side=LEFT)

        dispense_date_pickup_time_label = tkb.Label(
            master=dispense_date_row_2,
            text='Time:'
        )
        dispense_date_pickup_time_label.pack(side=LEFT)

        dispense_date_pickup_time_entry = tkb.Entry(
            master=dispense_date_row_2,
            width=15,
        )
        dispense_date_pickup_time_entry.pack(side=LEFT)

        # ===== INTERVENTION QUESTIONS =====#

        # Intervention questions frame
        intervention_questions_frame = tkb.Frame(refill_display_frame)
        intervention_questions_frame.pack(side=RIGHT)

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

    def create_labelframe(self, master, text):
        """Create a label frame."""
        labelframe = tkb.Labelframe(
            master=master,
            text=text,
            padding=10,
        )
        labelframe.pack(side=TOP, fill=BOTH, pady=(0, 10))
        return labelframe

    def create_inner_frame(self, master):
        """Create an inner frame."""
        frame = tkb.Frame(master)
        frame.pack(anchor='w', fill=BOTH, pady=(10, 0))
        return frame

    def create_tk_btn(self, master, text, padding=True):
        """Create a Tk button."""
        btn = tk.Button(
            master=master,
            text=text,
            activeforeground='white',
            padx=6,
            pady=3,
        )
        btn.pack(side=LEFT)
        if padding:
            btn.pack_configure(padx=(2, 0))

        return btn


if __name__ == '__main__':
    app = tkb.Window(
        'Refill Coordination', 'superhero', resizable=(False, False)
    )
    MainFrame(app)
    app.place_window_center()
    app.mainloop()
