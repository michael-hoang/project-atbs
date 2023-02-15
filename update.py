"""This module contains a class called Updater which checks on Github for the
latest release on a repository and downloads it to the user's root directory."""


import requests
import subprocess
import sys
import os
import urllib.request
import tkinter as tk
from tkinter import ttk
import time


class Updater:
    """This class creates a GUI which checks for latest repo updates and prompts
    the user to download and install."""

    def __init__(self, current_version):
        """Initialize version number, Github repo info, and GUI."""

        self.updater_version = ''
        self.github_user = 'michael-hoang'
        self.github_repo = 'project-atbs-work'
        self.current_version = current_version
        self.latest_version = ''
        self.api_url = f'https://api.github.com/repos/{self.github_user}/{self.github_repo}/releases/latest'
        self.dl_url = 'https://github.com/michael-hoang/project-atbs-work/raw/main/dist/main.exe'
        # GUI
        self.root = tk.Tk()
        self.root.title('Updater')
        self.progress_bar = ttk.Progressbar(
            self.root, orient='horizontal', length=300, mode='determinate'
        )
        self.progress_bar.pack(padx=15, pady=15, fill=tk.X)
        self.b_check_update = tk.Button(self.root, text='Check for updates')
        self.b_check_update.pack(pady=(0, 15))

        self.root.mainloop()

    def compare_version(self):
        """ Compare app's current version with the latest version on Github repo."""

        response = requests.get(self.api_url)
        data = response.json()
        self.latest_version = data['tag_name']
        if self.latest_version != self.current_version:
            print('An update is available!')
            print(f'Current version: {self.current_version}')
            print(f'Latest version: {self.latest_version}')
        else:
            print('You have the latest version.')

    def download_files(self):
        """Download the latest file(s) from Github repo to root directory."""

        if getattr(sys, 'frozen', False):
            updater_path = os.path.dirname(sys.executable)
        else:
            updater_path = os.path.dirname(os.path.abspath(__file__))

        exe_path = f'{updater_path}\main.exe'
        response = requests.get(self.dl_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        progress = 0
        with open(exe_path, 'wb') as f:
            for data in response.iter_content(block_size):
                progress += len(data)
                self.progress_bar['value'] = progress / total_size * 100
                self.root.update_idletasks()
                f.write(data)


if __name__ == '__main__':
    Updater('4.5')


# # Download latest files
# if getattr(sys, 'frozen', False):
#     update_path = os.path.dirname(sys.executable)
# else:
#     update_path = os.path.dirname(os.path.abspath(__file__))

# exe_path = f'{update_path}\main.exe'
# url = 'https://github.com/michael-hoang/project-atbs-work/raw/main/dist/main.exe'
# # urllib.request.urlretrieve(url, exe_path)

# # Download progress bar
# window = tk.Tk()
# window.title('Download Progress')
# progress_bar = ttk.Progressbar(
#     window, orient='horizontal', length=300, mode='determinate')
# progress_bar.pack(padx=5, pady=5, fill=tk.X)
# response = requests.get(url, stream=True)
# total_size = int(response.headers.get('content-length', 0))
# block_size = 1024
# progress = 0

# with open(exe_path, 'wb') as f:
#     for data in response.iter_content(block_size):
#         progress += len(data)
#         progress_bar['value'] = progress / total_size * 100
#         window.update_idletasks()
#         # time.sleep(0.1)
#         f.write(data)


# # progress_bar['value'] = 0


# # Run main.exe once update completes
# p = subprocess.Popen(exe_path)
# p.wait()
# print('The exe file has finished executing.')

# window.mainloop()
