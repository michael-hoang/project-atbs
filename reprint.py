import datetime as dt
import json
import os
import sys
import tkinter as tk
import ttkbootstrap as tkb
import time

from ttkbootstrap.constants import *


DAYS_UNTIL_EXPIRATION = 7
SECONDS_PER_DAY = 86400
SECONDS_PER_HOUR = 3600
SECONDS_PER_MINUTE = 60


class Reprint(tkb.Frame):
    """
    Interface to reprint filled card payment forms.
    """

    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.create_treeview(master)
        self.create_solid_button(master, 'Print', None)

    def create_treeview(self, master):
        """Create ttkbootstrap Treeview object."""

        # Tree container (Treeview + Scrollbar)
        tree_container = tkb.Frame(master)
        tree_container.pack(padx=20, pady=20)

        # Scrollbar
        tree_scroll = tkb.Scrollbar(
            master=tree_container,
            bootstyle=''
        )
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Define columns
        columns = ('#', 'reference', 'date_created', 'expiration')

        # Create Treeview
        self.my_tree = tkb.Treeview(
            master=tree_container,
            bootstyle='',
            columns=columns,
            show='headings',
            yscrollcommand=tree_scroll.set,
            selectmode='browse',
            height=10
        )
        self.my_tree.pack()

        # Configure scrollbar
        tree_scroll.config(command=self.my_tree.yview)

        # Format columns
        self.my_tree.column('#', anchor=CENTER, width=50)
        self.my_tree.column('reference', anchor=W, width=150)
        self.my_tree.column('date_created', anchor=W, width=150)
        self.my_tree.column('expiration', anchor=W, width=80)

        # Headings
        self.my_tree.heading('#', text='#', anchor=CENTER)
        self.my_tree.heading('reference', text='Reference', anchor=W)
        self.my_tree.heading('date_created', text='Date Created', anchor=W)
        self.my_tree.heading('expiration', text='Expiration', anchor=W)

        # Populate Data
        self._populate_data()

    def create_solid_button(self, master, text, command) -> tkb.Button:
        """Create ttkbootstrap Solid Button object."""
        button = tkb.Button(
            master=master,
            text=text,
            command=command,
            width=8
        )
        button.pack(pady=(0, 20))

        return button

    def _get_program_path(self) -> str:
        """Return the path to the running executable or script."""
        if getattr(sys, 'frozen', False):
            path = os.path.dirname(sys.executable)
        else:
            path = os.path.dirname(os.path.abspath(__file__))

        return path

    def _get_abs_path_to_data_directory(self) -> str:
        """Return the absolute path to the '.data' directory."""
        program_path = self._get_program_path()
        directory_path = '.data'
        directory_abs_path = os.path.join(program_path, directory_path)
        return directory_abs_path

    def _get_formatted_creation_time(self, epoch_ctime: str) -> str:
        """Return the creation time in 12H format."""
        dt_obj = dt.datetime.fromtimestamp(epoch_ctime)
        time_str = dt_obj.strftime('%m/%d/%Y %I:%M %p')
        return time_str

    def _get_epoch_exp_time(self, epoch_ctime: str, days_expiration=7) -> int:
        epoch_exp_time = int(epoch_ctime) + (days_expiration * SECONDS_PER_DAY)
        return epoch_exp_time

    def _get_formatted_exp_time(self, epoch_exp_time: int) -> str:
        epoch_current_time = time.time()
        remaining_epoch_time = epoch_exp_time - epoch_current_time
        days = int(remaining_epoch_time // SECONDS_PER_DAY)
        remaining_epoch_sec = remaining_epoch_time % SECONDS_PER_DAY
        hours = int(remaining_epoch_sec // SECONDS_PER_HOUR)
        remaining_epoch_sec %= SECONDS_PER_HOUR
        minutes = int(remaining_epoch_sec // SECONDS_PER_MINUTE)
        formatted_exp_time = f'{days}d {hours}h {minutes}m'
        return formatted_exp_time

    def _populate_data(self):
        """Populate data from data.json into Treeview."""
        data_dir_path = self._get_abs_path_to_data_directory()
        json_file_path = os.path.join(data_dir_path, 'data.json')
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        index = 1
        iid = 0
        for ref_id in data:
            epoch_ctime = data[ref_id]['epoch_ctime']
            fmt_ctime = self._get_formatted_creation_time(epoch_ctime)
            epoch_exp_time = self._get_epoch_exp_time(epoch_ctime)
            fmt_exp_time = self._get_formatted_exp_time(epoch_exp_time)
            self.my_tree.insert(
                parent='',
                index=END,
                iid=iid,
                text='Parent',
                values=(index, ref_id, fmt_ctime, fmt_exp_time)
            )
            index += 1
            iid += 1


if __name__ == '__main__':
    reprint_window = tkb.Window(
        title='Reprint',
        themename='superhero',
    )
    rp = Reprint(master=reprint_window)

    reprint_window.mainloop()
