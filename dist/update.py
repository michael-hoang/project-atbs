"""This module contains a class called Updater which checks on Github for the
latest release on a repository and downloads it to the user's root directory."""


import requests
import sys
import os
import tkinter as tk
from tkinter import END
import json


FONT = ('Helvetica', 12, 'normal')
STATUS_FONT = ('Helvetica', 12, 'bold')


class Updater:
    """This class creates a GUI which checks for latest repo updates and prompts
    the user to download and install."""

    def __init__(self):
        """Initialize version number, Github URL, and GUI."""

        self.updater_current_version = 'v1.0.0'
        self.latest_version_url = 'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/dist/latest_version/latest_version.json'
        self.latest_app_dl_url = 'https://github.com/michael-hoang/project-atbs-work/raw/main/dist/latest_version/main.exe'
        self.main_app_current_version = ''
        self.app_latest_version = ''
        self.current_working_directory = ''
        self.main_app_path = ''
        self.updater_path = ''
        self.current_version_path = ''

        self.get_paths()
        self.get_current_app_version()

        # GUI
        self.root = tk.Tk()
        self.root.title('App Update Manager')
        self.root.resizable(width=False, height=False)

        self.lf_current_version = tk.LabelFrame(self.root, text='Current Version', font=FONT)
        self.lf_current_version.grid(column=0, row=0, columnspan=2, padx=20, pady=(20, 0))

        self.l_updater_current_version = tk.Label(
            self.lf_current_version, text='App Update Manager:', font=FONT)
        self.l_updater_current_version.grid(column=0, row=0, sticky='e', padx=(15, 0), pady=(15, 0))
        self.e_updater_current_version = tk.Entry(self.lf_current_version, width=8, font=FONT)
        self.e_updater_current_version.grid(column=1, row=0, padx=(0, 15), pady=(15, 0))
        self.e_updater_current_version.insert(
            0, f'{self.updater_current_version}')
        self.e_updater_current_version.config(state='disabled')

        self.l_main_app_current_version = tk.Label(
            self.lf_current_version, text='Main App:', font=FONT)
        self.l_main_app_current_version.grid(column=0, row=1, sticky='e', padx=(15, 0), pady=(0, 15))
        self.e_main_app_current_version = tk.Entry(self.lf_current_version, width=8, font=FONT)
        self.e_main_app_current_version.grid(column=1, row=1, padx=(0, 15), pady=(0, 15))
        self.e_main_app_current_version.insert(0, f'{self.main_app_current_version}')
        self.e_main_app_current_version.config(state='disabled')

        self.l_status = tk.Label(self.root, text='Status:', font=STATUS_FONT)
        self.l_status.grid(column=0, row=1, padx=(15, 0), pady=(20), sticky='w')
        self.l_status_message = tk.Label(self.root, text='', font=STATUS_FONT)
        self.l_status_message.grid(column=1, row=1, padx=(0, 15), pady=(20), sticky='w')

        self.b_check_update = tk.Button(
            self.root, text='Check for updates', font=FONT, command=self.check_for_latest_app_version, width=17
        )
        self.b_check_update.grid(columnspan=2, pady=(0, 20))

        # Center root window
        self.root.update_idletasks()
        win_width = self.root.winfo_reqwidth()
        win_height = self.root.winfo_reqheight()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int(screen_width/2 - win_width/2)
        y = int(screen_height/2 - win_width/2)
        self.root.geometry(f"{win_width}x{win_height}+{x}+{y}")
        self.root.deiconify()

        self.root.mainloop()

    def get_latest_app_version(self):
        """Retrieve the latest version number for the app."""

        latest_version_response = requests.get(self.latest_version_url)
        if latest_version_response.status_code == 200:
            data = json.loads(latest_version_response.content)
            self.app_latest_version = data['main']

    def get_current_app_version(self):
        """Retrieve the current version number for the app"""

        current_version_path = f'{self.updater_path}\current_version\current_version.json'
        with open(current_version_path) as f:
            data = json.load(f)
            self.main_app_current_version = data['main']

    def check_for_latest_app_version(self):
        """ Compare app's current version with the latest version on Github repo."""

        self.get_latest_app_version()
        if self.main_app_current_version != self.app_latest_version:
            self.l_status_message.config(
                text=f'{self.app_latest_version} available', fg='green'
            )
            self.b_check_update.config(
                text='Update', command=self.download_files
            )
        else:
            self.l_status_message.config(
                text='No update available', fg='black'
            )

    def download_files(self):
        """Download the latest file(s) from Github repo to root directory."""

        if getattr(sys, 'frozen', False):
            updater_path = os.path.dirname(sys.executable)
        else:
            updater_path = os.path.dirname(os.path.abspath(__file__))
        # Download main.exe
        root_path = f'{updater_path[:-5]}\main.exe'
        response = requests.get(self.latest_app_dl_url, stream=True)
        block_size = 1024
        with open(root_path, 'wb') as f:
            for data in response.iter_content(block_size):
                f.write(data)
        # Download current_version.json
        current_version_path = f'{updater_path}\current_version\current_version.json'
        response = requests.get(self.latest_version_url, stream=True)
        block_size = 4
        with open(current_version_path, 'wb') as f:
            for data in response.iter_content(block_size):
                f.write(data)
        # Update status message and reset button
        self.l_status_message.config(
            text=f'App has been updated', fg='green'
        )
        self.b_check_update.config(
            text='Check for updates', command=self.check_for_latest_app_version, fg='black'
        )
        self.main_app_current_version = self.app_latest_version
        self.e_main_app_current_version.config(state='normal')
        self.e_main_app_current_version.delete(0, END)
        self.e_main_app_current_version.insert(0, f'{self.main_app_current_version}')
        self.e_main_app_current_version.config(state='disabled')
    
    def get_paths(self):
        """Get paths for current working directory, main app, and updater."""

        if getattr(sys, 'frozen', False):
            self.updater_path = os.path.dirname(sys.executable)
        else:
            self.updater_path = os.path.dirname(os.path.abspath(__file__))

        self.current_working_directory = self.updater_path[:-5]
        self.main_app_path = f'{self.current_working_directory}\main.exe'

    def open_main_app(self):
        """Run the main app"""

        os.startfile(self.main_app_path, cwd=self.current_working_directory)
            

if __name__ == '__main__':
    Updater()
