import datetime as dt
import json
import os
import sys
import tkinter as tk
import ttkbootstrap as tkb
import time

from ttkbootstrap.constants import *


DAYS_EXPIRATION = 0.00069 * 1.2
SECONDS_PER_DAY = 86400
SECONDS_PER_HOUR = 3600
SECONDS_PER_MINUTE = 60


class Reprint(tkb.Frame):
    """
    Interface to reprint filled card payment forms.
    """

    def __init__(self, master, reprint_command):
        super().__init__(master)
        self.pack()
        self.reprint_command = reprint_command

        self.create_treeview(master)
        self.create_solid_button(master, 'Print', self.reprint_command)

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
        self.my_tree.column('expiration', anchor=W, width=100)

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
            command=self.reprint_command,
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

    def _get_epoch_exp_time(self, epoch_ctime: str) -> int:
        epoch_exp_time = int(epoch_ctime) + (DAYS_EXPIRATION * SECONDS_PER_DAY)
        return epoch_exp_time

    def _get_formatted_exp_time(self, epoch_exp_time: int) -> str:
        epoch_current_time = time.time()
        remaining_epoch_time = epoch_exp_time - epoch_current_time
        days = int(remaining_epoch_time // SECONDS_PER_DAY)
        remaining_epoch_sec = remaining_epoch_time % SECONDS_PER_DAY
        hours = int(remaining_epoch_sec // SECONDS_PER_HOUR)
        remaining_epoch_sec %= SECONDS_PER_HOUR
        minutes = int(remaining_epoch_sec // SECONDS_PER_MINUTE)
        remaining_epoch_sec %= SECONDS_PER_MINUTE
        formatted_exp_time = f'{days}d {hours}h {minutes}m {int(remaining_epoch_sec)}s'
        return formatted_exp_time

    def _populate_data(self):
        """Populate data from data.json into Treeview."""
        data_dir_path = self._get_abs_path_to_data_directory()
        json_file_path = os.path.join(data_dir_path, 'data.json')
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        iid = 1
        for ref_id in data:
            epoch_ctime = data[ref_id]['epoch_ctime']
            fmt_ctime = self._get_formatted_creation_time(epoch_ctime)
            epoch_exp_time = self._get_epoch_exp_time(epoch_ctime)
            fmt_exp_time = self._get_formatted_exp_time(epoch_exp_time)
            self.my_tree.insert(
                parent='',
                index=END,
                iid=iid,
                values=(iid, ref_id, fmt_ctime, fmt_exp_time),
                text=epoch_ctime
            )
            iid += 1

    def _refresh_treeview(self):
        """Refresh items in Treeview window."""
        try:
            current_selection = self.my_tree.focus()
        except:
            pass

        for child in self.my_tree.get_children():
            self.my_tree.delete(child)

        self._populate_data()

        try:
            self.my_tree.selection_set(current_selection)
            self.my_tree.focus(current_selection)
        except:
            pass

    def _get_reference_id(self) -> str:
        """
        Return the reference id of selected item from Treeview window.
        """
        iid = self.my_tree.focus()
        reference_id = self.my_tree.item(iid)['values'][1]
        return reference_id


if __name__ == '__main__':
    reprint_window = tkb.Window(
        title='Reprint',
        themename='litera',
    )
    Reprint(reprint_window, None)

    reprint_window.mainloop()
