import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox


class Settings(tkb.Frame):

    def __init__(self, master):
        super().__init__(master, padding=10)
        self.pack(fill=BOTH, expand=YES)

        # Settings
        self.settings_labelframe = self.create_labelframe(
            master=self,
            text='Settings',
            row=0,
        )

        always_top_int_var = tkb.IntVar()
        always_top_btn = self.create_toggle_btn(
            master=self.settings_labelframe,
            text='Always on top',
            variable=always_top_int_var
        )
        always_top_btn.pack_configure(anchor='w')

        # Row 2

        row_2 = self.create_inner_frame(master=self.settings_labelframe)

        print_blank_form_label = self.create_label(
            master=row_2,
            text='Print blank card payment forms',
        )

        print_blank_form_btn = self.create_solid_btn(
            master=row_2,
            text='Print',
            command=None,
            width=7
        )
        print_blank_form_btn.pack_configure(side=RIGHT, padx=(10, 0))

        # Row 3

        row_3 = self.create_inner_frame(master=self.settings_labelframe)

        change_user_label = self.create_label(
            master=row_3,
            text='Change user'
        )

        change_user_btn = self.create_solid_btn(
            master=row_3,
            text='Edit',
            command=None,
             width=7,
             state='disabled'
        )
        change_user_btn.pack_configure(side=RIGHT, padx=(10, 0))

        # Mode

        mode_label_frame = self.create_labelframe(
            master=self,
            text='Mode',
            row=1,
            padding=False
        )

        # Theme menu
        themes = ['superhero', 'solar', 'darkly', 'cyborg', 'vapor'
                  'cosmo', 'flatly', 'journal', 'litera', 'lumen',
                  'minty', 'pulse', 'sandstone', 'united', 'yeti',
                  'morph', 'simplex', 'cerculean']

        theme_label_Frame = self.create_labelframe(
            master=self,
            text='Theme',
            row=2,
            padding=False
        )

        self.create_combobox(theme_label_Frame, themes, 0)

    def create_labelframe(self, master, text, row, col=0, sticky='we', padding=True):
        """Create a label frame."""
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

    def create_toggle_btn(self, master, text: str, variable: tkb.IntVar):
        """Create a toggle button ."""
        toggle_btn = tkb.Checkbutton(
            master=master,
            text=text,
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

    def create_combobox(self, master, options: list, default_index: int):
        """Create a combobox drop down menu."""
        combobox = tkb.Combobox(
            master=master,
            values=options,
        )

        combobox.current(default_index)
        combobox.pack(fill=X)


if __name__ == '__main__':

    app = tkb.Window("Settings", "superhero")
    Settings(app)
    app.mainloop()
