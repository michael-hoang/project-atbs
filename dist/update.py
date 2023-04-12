"""This module contains a class called Updater which checks on Github for the
latest release on a repository and downloads it to the user's root directory."""


import json, requests, os, sys, urllib.request
import tkinter as tk
from tkinter import END


FONT = ('Helvetica', 12, 'normal')
STATUS_FONT = ('Helvetica', 12, 'bold')


class Updater:
    """This class creates a GUI which checks for latest repo updates and prompts
    the user to download and install."""

    def __init__(self):
        """Initialize version number, Github URL, paths, and GUI."""
        self.updater_current_version = 'v1.1.1'
        self.latest_main_version_url = 'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/dist/latest_version/latest_main_version.json'
        self.latest_updater_version_url = 'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/dist/latest_version/latest_updater_version.json'
        self.latest_app_dl_url = 'https://github.com/michael-hoang/project-atbs-work/raw/main/dist/latest_version/main.exe'
        self.updater_path = ''
        self.root_directory = ''
        self.main_app_path = ''
        self.current_main_version_path = ''
        self.current_updater_version_path = ''
        self.main_app_current_version = ''
        self.main_app_latest_version = ''
        # Check for current version json file
        self.check_download_updater_version_json()

        # GUI
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.title('App Update Manager')
        self.root.resizable(width=False, height=False)

        self.lf_current_version = tk.LabelFrame(
            self.root, text='Current Version', font=FONT)
        self.lf_current_version.grid(
            column=0, row=0, columnspan=2, padx=20, pady=(20, 0))

        self.l_updater_current_version = tk.Label(
            self.lf_current_version, text='App Update Manager:', font=FONT)
        self.l_updater_current_version.grid(
            column=0, row=0, sticky='e', padx=(15, 0), pady=(15, 0))
        self.e_updater_current_version = tk.Entry(
            self.lf_current_version, width=8, font=FONT)
        self.e_updater_current_version.insert(0, self.updater_current_version)
        self.e_updater_current_version.grid(
            column=1, row=0, padx=(0, 15), pady=(15, 0))
        self.e_updater_current_version.config(state='disabled')

        self.l_main_app_current_version = tk.Label(
            self.lf_current_version, text='Main App:', font=FONT)
        self.l_main_app_current_version.grid(
            column=0, row=1, sticky='e', padx=(15, 0), pady=(0, 15))
        self.e_main_app_current_version = tk.Entry(
            self.lf_current_version, width=8, font=FONT)
        self.e_main_app_current_version.grid(
            column=1, row=1, padx=(0, 15), pady=(0, 15))

        self.l_status = tk.Label(self.root, text='Status:', font=STATUS_FONT)
        self.l_status.grid(column=0, row=1, padx=(
            15, 0), pady=(20), sticky='w')
        self.l_status_message = tk.Label(self.root, text='', font=STATUS_FONT)
        self.l_status_message.grid(
            column=1, row=1, padx=(0, 15), pady=(20), sticky='w')

        self.b_check_update = tk.Button(
            self.root, text='Check for updates', font=FONT, command=self.check_for_latest_main_app_version, width=17)
        self.b_check_update.grid(columnspan=2, pady=(0, 20))

        self.center_root_window_to_screen()
        self.get_paths()
        self.get_current_main_app_version()
        # GUI icon
        icon_path = self.root_directory.replace('\\', '/')
        self.root.iconphoto(False, tk.PhotoImage(
            file=f'{icon_path}/assets/img/update.png'))

        # print(f'Updater Path: {self.updater_path}') # DEBUG
        # print(f'Root Directory: {self.root_directory}') # DEBUG
        # print(f'Main App Path: {self.main_app_path}') # DEBUG
        # print(f'Current Main Version Path: {self.current_main_version_path}') # DEBUG
        # print(f'Current Updater Version Path: {self.current_updater_version_path}') # DEBUG
        # print(f'Main App Current Version: {self.main_app_current_version}') # DEBUG
        # print(f'Main App Latest Version: {self.main_app_latest_version}') # DEBUG

        self.root.mainloop()

    def check_download_updater_version_json(self):
        """Check and download current Updater version .json file."""
        data = {
            'updater': self.updater_current_version
        }
        current_path = self.get_exe_script_path()
        if '\\' in current_path:
            current_version_dir = f'{current_path}\\current_version'
            filename = f'{current_version_dir}\\current_updater_version.json'
        else:
            current_version_dir = f'{current_path}/current_version'
            filename = f'{current_version_dir}/current_updater_version.json'
        
        if not os.path.exists(current_version_dir):
            os.mkdir(current_version_dir)

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def center_root_window_to_screen(self):
        """Center root window"""
        self.root.update_idletasks()
        win_width = self.root.winfo_reqwidth()
        win_height = self.root.winfo_reqheight()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int(screen_width/2 - win_width/2)
        y = int(screen_height/2 - win_width/2)
        self.root.geometry(f"{win_width}x{win_height}+{x}+{y}")
        self.root.deiconify()

    def get_exe_script_path(self) -> str:
        """Return the path to the current exe or script file."""
        if getattr(sys, 'frozen', False):
            path = os.path.dirname(sys.executable)
        else:
            path = os.path.dirname(os.path.abspath(__file__))
        return path
    
    def get_root_path(self) -> str:
        """Return the path to the root directory of the main application."""
        # Determine if the current application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            current_path = os.path.dirname(sys.executable)
        else:
            current_path = os.path.dirname(os.path.abspath(__file__))

        if '\\' in current_path:
            dir_len = len(current_path.split('\\')[-1]) + 1
        elif '/' in current_path:
            dir_len = len(current_path.split('/')[-1]) + 1
        
        root_path = current_path[:-dir_len]
        return root_path
        
    def get_paths(self):
        """Get paths for current working directory, main app, and updater."""
        if getattr(sys, 'frozen', False):
            self.updater_path = os.path.dirname(sys.executable)
        else:
            self.updater_path = os.path.dirname(os.path.abspath(__file__))

        self.root_directory = self.updater_path[:-5]
        self.main_app_path = f'{self.root_directory}\main.exe'
        self.current_main_version_path = f'{self.updater_path}\current_version\current_main_version.json'
        self.current_updater_version_path = f'{self.updater_path}\current_version\current_updater_version.json'

    def get_current_main_app_version(self):
        """Retrieve the current version number for the main app"""
        with open(self.current_main_version_path) as f:
            data = json.load(f)
            self.main_app_current_version = data['main']

        self.e_main_app_current_version.config(state='normal')
        self.e_main_app_current_version.delete(0, END)
        self.e_main_app_current_version.insert(
            0, f'{self.main_app_current_version}')
        self.e_main_app_current_version.config(state='disabled')

    def get_latest_main_app_version(self):
        """Retrieve the latest version number for the main app."""
        latest_main_version_response = requests.get(
            self.latest_main_version_url)
        if latest_main_version_response.status_code == 200:
            data = json.loads(latest_main_version_response.content)
            self.main_app_latest_version = data['main']
            # print(f'Main App Latest Version: {self.main_app_latest_version}') # DEBUG

    def update_status_message(self, message, font_color):
        """Update status Label with new text message, text color, and font."""
        self.l_status_message.config(text=message, fg=font_color)

    def check_for_latest_main_app_version(self):
        """Compare main app's current version with the latest version on Github repo."""
        self.get_latest_main_app_version()
        if self.main_app_current_version != self.main_app_latest_version:
            message = f'{self.main_app_latest_version} available'
            font_color = 'green'
            # Change button to Update if new main app version is available to download.
            self.b_check_update.config(
                text='Update', command=self.update_main_app)
        else:
            message = 'No update available'
            font_color = 'black'

        self.update_status_message(message, font_color)

    def download_latest_files(self):
        """Download the latest files from Github repo."""
        # Download main.exe
        response = requests.get(self.latest_app_dl_url, stream=True)
        block_size = 1024
        with open(self.main_app_path, 'wb') as f:
            for data in response.iter_content(block_size):
                f.write(data)
        # Download current_main_version.json
        response = requests.get(self.latest_main_version_url, stream=True)
        block_size = 4
        with open(self.current_main_version_path, 'wb') as f:
            for data in response.iter_content(block_size):
                f.write(data)

    def reset_button(self):
        """Reset button back to 'Check for updates'"""
        self.b_check_update.config(
            text='Check for updates', command=self.check_for_latest_main_app_version, fg='black')

    def open_main_app(self):
        """Run main.exe from root directory."""
        os.startfile(self.main_app_path, cwd=self.root_directory)

    def update_main_app(self):
        """Update the main app"""
        self.download_latest_files()
        self.get_current_main_app_version()
        self.update_status_message('App has been updated', 'green')
        self.reset_button()
        self.open_main_app()

    def check_create_assets_dir(self):
        """Check if assets directory exists and create it if it doesn't."""
        root_path = self.get_root_path()
        if '\\' in root_path:
            assets_dir = f'{root_path}\\assets'
            assets_img_dir = f'{assets_dir}\\img'
            assets_form_dir = f'{assets_dir}\\form'
        elif '/' in root_path:
            assets_dir = f'{root_path}/assets'
            assets_img_dir = f'{assets_dir}/img'
            assets_form_dir = f'{assets_dir}/form'

        if not os.path.exists(assets_dir):
            os.mkdir(assets_dir)
            os.mkdir(assets_img_dir)
            os.mkdir(assets_form_dir)

    def update_assets(self):
        """Update files in the assets directory."""
        assets_img = (
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/amex.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/atbs_icon.ico',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/atbs_icon.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/authentication_icon.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/cal_calc.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/cc_icon.ico',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/cc_icon.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/check_mark.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/dice.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/discover.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/edit-user.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/eye.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/generic_card.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/lock_button.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/lock_icon.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/map_icon.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/mastercard.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/note.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/note_pin.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/rx.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/rx_icon.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/search.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/setting.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/setting_icon.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/update.ico',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/update.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/visa.png',
            'https://raw.githubusercontent.com/michael-hoang/project-atbs-work/main/assets/img/x_mark.png',
        )

        assets_form = (
            'https://github.com/michael-hoang/project-atbs-work/raw/242498f7014bd06daf6e507e6e011bf4d3d4a56d/assets/form/cardpayment.pdf',
        )

        root_path = self.get_root_path()
        if '\\' in root_path:
            assets_img_path = f'{root_path}\\assets\\img'
            assets_form_path = f'{root_path}\\assets\\form'
        elif '/' in root_path:
            assets_img_path = f'{root_path}/assets/img'
            assets_form_path = f'{root_path}/assets/form'

        for img_url in assets_img:
            filename = os.path.basename(img_url)
            urllib.request.urlretrieve(img_url, os.path.join(assets_img_path, filename))
        
        for form_url in assets_form:
            filename = os.path.basename(form_url)
            urllib.request.urlretrieve(form_url, os.path.join(assets_form_path, filename))


if __name__ == '__main__':
    Updater()
