"""This module contains a class called Updater which checks on Github for the
latest release on a repository and downloads it to the user's root directory."""


import requests
import subprocess
import sys
import os
import urllib.request
import tkinter as tk
import time
import json


class Updater:
    """This class creates a GUI which checks for latest repo updates and prompts
    the user to download and install."""

    def __init__(self):
        """Initialize version number, Github repo info, and GUI."""

        self.updater_current_version = 'v1.0.0'
        self.app_current_version = ''
        self.app_latest_version = ''
        self.latest_version_url = 'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/dist/latest_version/latest_version.json'
        self.latest_app_dl_url = 'https://github.com/michael-hoang/project-atbs-work/raw/main/dist/latest_version/main.exe'
        # GUI
        self.root = tk.Tk()
        self.root.title('App Update Manager')

        self.b_check_update = tk.Button(self.root, text='Check for updates')
        self.b_check_update.pack(padx=15, pady=15)

        self.get_current_app_version_number()
        self.get_latest_app_version_number()
        self.download_files()

        self.root.mainloop()

    def get_latest_app_version_number(self):
        """Retrieve the latest version number for the app."""

        latest_version_response = requests.get(self.latest_version_url)
        if latest_version_response.status_code == 200:
            data = json.loads(latest_version_response.content)
            self.app_latest_version = data['main']

    def get_current_app_version_number(self):
        """Retrieve the current version number for the app"""

        if getattr(sys, 'frozen', False):
            updater_path = os.path.dirname(sys.executable)
        else:
            updater_path = os.path.dirname(os.path.abspath(__file__))

        current_version_path = f'{updater_path}\current_version\current_version.json'
        with open(current_version_path) as f:
            data = json.load(f)
            self.app_current_version = data['main']

    def compare_version(self):
        """ Compare app's current version with the latest version on Github repo."""

        if self.app_current_version != self.app_latest_version:
            self.download_files()

    def download_files(self):
        """Download the latest file(s) from Github repo to root directory."""

        if getattr(sys, 'frozen', False):
            updater_path = os.path.dirname(sys.executable)
        else:
            updater_path = os.path.dirname(os.path.abspath(__file__))

        destination_path = f'{updater_path[:-5]}\main.exe'
        response = requests.get(self.latest_app_dl_url, stream=True)
        block_size = 1024

        with open(destination_path, 'wb') as f:
            for data in response.iter_content(block_size):
                f.write(data)


if __name__ == '__main__':
    Updater()
