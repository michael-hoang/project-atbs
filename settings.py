import json
import os
import sys
import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from tkinter.ttk import Style


class Settings(tkb.Frame):

    def __init__(self, master, cardpayment):
        super().__init__(master, padding=12)
        self.pack(fill=BOTH, expand=YES)
        style = Style()
        style.configure('TRadiobutton', font=('', 10, ''))

        self.cardpayment = cardpayment

        # Settings
        self.current_settings = self._read_settings_json_file()

        self.settings_labelframe = self.create_labelframe(
            master=self,
            text='Settings',
            row=0,
        )

        self.always_top_int_var = tkb.IntVar()
        always_top_btn = self.create_toggle_btn(
            master=self.settings_labelframe,
            text='Always on top',
            command=self.set_always_on_top,
            variable=self.always_top_int_var,
        )
        always_top_btn.pack_configure(anchor='w')

        # Row 2

        settings_row_2 = self.create_inner_frame(
            master=self.settings_labelframe)

        print_blank_form_label = self.create_label(
            master=settings_row_2,
            text='Print blank card payment forms',
        )

        print_blank_form_btn = self.create_solid_btn(
            master=settings_row_2,
            text='Print',
            command=None,
            width=7
        )
        print_blank_form_btn.pack_configure(side=RIGHT, padx=(10, 0))

        # Row 3

        settings_row_3 = self.create_inner_frame(
            master=self.settings_labelframe)

        change_user_label = self.create_label(
            master=settings_row_3,
            text='Change user'
        )

        change_user_btn = self.create_solid_btn(
            master=settings_row_3,
            text='Edit',
            command=None,
            width=7,
            state='disabled'
        )
        change_user_btn.pack_configure(side=RIGHT, padx=(10, 0))

        # Mode

        self.mode_str_var = tkb.StringVar()

        mode_labelframe = self.create_labelframe(
            master=self,
            text='Mode',
            row=1,
        )

        payment_mode = self.create_radio_btn(
            master=mode_labelframe,
            text='Payment',
            command=None,
            variable=self.mode_str_var,
            value='Payment'
        )

        refill_mode = self.create_radio_btn(
            master=mode_labelframe,
            text='Refill',
            command=None,
            variable=self.mode_str_var,
            value='Refill'
        )

        refill_mode.pack_configure(padx=(20, 0))

        # Theme menu
        themes = ['superhero', 'solar', 'darkly', 'cyborg', 'vapor'
                  'cosmo', 'flatly', 'journal', 'litera', 'lumen',
                  'minty', 'pulse', 'sandstone', 'united', 'yeti',
                  'morph', 'simplex', 'cerculean']

        theme_labelframe = self.create_labelframe(
            master=self,
            text='Theme',
            row=2,
        )

        self.create_combobox(theme_labelframe, themes, 0)

        # Info

        info_labelframe = self.create_labelframe(
            master=self,
            text='Info',
            row=3,
        )

        # Row 1

        info_row_1 = self.create_inner_frame(info_labelframe)

        title_label = self.create_label(
            master=info_row_1,
            text='Card Payment App'
        )

        # Ok button
        ok_btn = tkb.Button(
            master=self,
            text='OK',
            command=self.save_settings,
            width=10,
        )

        ok_btn.grid(row=4, pady=(10, 0))

    def _check_always_on_top(self):
        """Check always on top setting from settings.json. (Used by CardPayment)"""
        if self.current_settings['always_on_top'] == 'yes':
            self.always_top_int_var.set(1)
        else:
            self.always_top_int_var.set(0)

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

    def _get_settings_json_path(self) -> str:
        """Return the absolute path to 'settings.json' file."""
        directory_abs_path = self._get_abs_path_to_data_directory()
        file_name = 'settings.json'
        file_path = os.path.join(directory_abs_path, file_name)
        return file_path

    def _read_settings_json_file(self) -> dict:
        """Read the 'settings.json' file."""
        settings_json_path = self._get_settings_json_path()
        with open(settings_json_path, 'r') as f:
            data = json.load(f)

        return data

    def _set_user_settings(self):
        """Set user settings from settings.json file."""
        self.cardpayment._set_always_on_top_setting(self.current_settings)

    def _user_setup_window(self):
        """Create user setup window."""
        self.setup_window = tkb.Toplevel(self)
        self.setup_window.title('User Setup')
        self.setup_window.config(padx=25, pady=15)
        self.setup_window.resizable(False, False)

        row_1 = self.create_inner_frame(self.setup_window)

        self.create_label(
            master=row_1,
            text='First Name:'
        )

        self.first_name_entry = self.create_short_entry(master=row_1, width=20)

        row_2 = self.create_inner_frame(self.setup_window)

        self.create_label(
            master=row_2,
            text='Last Name:'
        )

        self.last_name_entry = self.create_short_entry(master=row_2, width=20)

        ok_btn = self.create_solid_btn(
            master=self.setup_window,
            text='OK',
            command=self.user_setup_ok_btn_command,
            width=7
        )
        ok_btn.pack_configure(side=BOTTOM, pady=(15, 0))

        self.cardpayment.root.attributes('-disabled', 1)
        self.setup_window.wm_transient(self)
        self.setup_window.deiconify()
        self.first_name_entry.focus()

    # Button commands

    def user_setup_ok_btn_command(self):
        """Confirm user setup."""
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        if first_name and last_name:
            first_name_title = first_name.title()
            last_name_title = last_name.title()
            self.current_settings['users'] = {
                'first_name': first_name_title,
                'last_name': last_name_title,
            }
            self.save_settings()
            self.cardpayment.root.attributes('-disabled', 0)
            self.cardpayment.root.deiconify()
            self.setup_window.destroy()
        elif first_name and not last_name:
            self.first_name_entry.config(style='TEntry')
            self.last_name_entry.config(style='danger.TEntry')
        elif not first_name and last_name:
            self.first_name_entry.config(style='danger.TEntry')
            self.last_name_entry.config(style='TEntry')
        else:
            self.first_name_entry.config(style='danger.TEntry')
            self.last_name_entry.config(style='danger.TEntry')
            

    def save_settings(self):
        """Save current user settings to json file."""
        settings_json_path = self._get_settings_json_path()
        with open(settings_json_path, 'w') as f:
            data = json.dumps(self.current_settings, indent=4)
            f.write(data)

        self._set_user_settings()
        self.cardpayment.toggle_settings_window(e=None)

    def set_always_on_top(self):
        """Set always on top setting attribute"""
        if self.always_top_int_var.get() == 0:
            self.current_settings['always_on_top'] = 'no'
        else:
            self.current_settings['always_on_top'] = 'yes'

    def check_mode(self):
        """Check if changing mode conditions are satisfied."""
        selected_mode = self.mode_str_var.get()
        if selected_mode == 'Refill':
            if self.current_settings['user']:
                pass

            else:
                self._user_setup_window()
                #   if still no user
                #       select Payment mode

                # Widget creation methods

    def create_labelframe(self, master, text, row, col=0, sticky='we', padding=True):
        """Create a label frame grid."""
        labelframe = tkb.Labelframe(
            master=master,
            text=text,
            # style='TLabelframe.Label',
            padding=15,
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

    def create_label(self, master, text, anchor='e',  width=DEFAULT, grid=False):
        """Create a label."""
        label = tkb.Label(
            master=master,
            text=text,
            width=width,
            anchor=anchor,
            font=('', 10, '')
        )
        if not grid:
            label.pack(side=LEFT)

        return label

    def create_toggle_btn(self, master, text: str, command, variable: tkb.IntVar):
        """Create a toggle button ."""
        toggle_btn = tkb.Checkbutton(
            master=master,
            text=text,
            command=command,
            bootstyle='round-toggle',
            variable=variable,
        )

        toggle_btn.pack(side=TOP)
        return toggle_btn

    def create_solid_btn(self, master, text, command, width=DEFAULT, state='normal'):
        """Create a solid button."""
        solid_btn = tkb.Button(
            master=master,
            text=text,
            command=command,
            width=width,
            state=state
        )

        solid_btn.pack(side=LEFT)
        return solid_btn

    def create_radio_btn(self, master, text, command, variable, value):
        """Create a radiobutton."""
        radiobutton = tkb.Radiobutton(
            master=master,
            text=text,
            command=command,
            variable=variable,
            value=value,
            style='TRadiobutton'
        )

        radiobutton.pack(side=LEFT)
        return radiobutton

    def create_combobox(self, master, options: list, default_index: int):
        """Create a combobox drop down menu."""
        combobox = tkb.Combobox(
            master=master,
            values=options,
        )

        combobox.current(default_index)
        combobox.pack(fill=X)

    def create_short_entry(self, master, width=15, padding=True, text_var=None, state='normal'):
        """Create an entry field."""
        entry = tkb.Entry(
            master=master,
            width=width,
            textvariable=text_var,
            state=state
        )

        entry.pack(side=LEFT, padx=(3, 0))
        if not padding:
            entry.pack_configure(padx=0)

        return entry


if __name__ == '__main__':
    from cardpayment import CardPayment

    app = tkb.Window("Settings", "superhero")
    cardpayment = CardPayment(app, app)
    a = Settings(app, cardpayment)
    a._user_setup_window()
    app.mainloop()
