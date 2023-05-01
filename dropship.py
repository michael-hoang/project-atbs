import pandas as pd
import ttkbootstrap as tkb

from ttkbootstrap.constants import *
from tkinter.ttk import Style


FONT = ('', 10, '')
EXCEL_PATH = './assets/data/dropship.xlsx'


class DropShipLookUp(tkb.Frame):
    """GUI for searching if a drug is ordered through drop ship."""

    def __init__(self):
        super().__init__(padding=25)
        self.pack()
        style = Style()
        style.configure('TButton', font=FONT)

        # Load Excel
        self.excel_data = self.load_excel_data(EXCEL_PATH)

        # GUI
        ndc_format_label = tkb.Label(
            master=self,
            text='Enter 11-digit raw NDC',
            font=FONT
        )
        ndc_format_label.pack(side=TOP)

        ndc_input_container = tkb.Frame(master=self)
        ndc_input_container.pack(side=TOP, fill=BOTH, pady=(15, 0))

        ndc_label = tkb.Label(
            master=ndc_input_container,
            text='NDC:',

        )
        ndc_label.pack(side=LEFT)

        ndc_entry = tkb.Entry(
            master=ndc_input_container,
            width=12,
            font=FONT,
        )
        ndc_entry.pack(side=LEFT, padx=(10, 0))

        check_btn = tkb.Button(
            master=ndc_input_container,
            text='Check',
            style='TButton',
            command=None,
        )
        check_btn.pack(side=LEFT, padx=(15, 0))

        drug_name_container = tkb.Frame(master=self)
        drug_name_container.pack(side=TOP, fill=BOTH, pady=(15, 0))

        drug_name_label = tkb.Label(
            master=drug_name_container,
            text='Drug:',
            font=FONT
        )
        drug_name_label.pack(side=LEFT)

        drug_name = tkb.Label(
            master=drug_name_container,
            text='',
            font=FONT
        )
        drug_name.pack(side=LEFT, padx=(10, 0))

        status_container = tkb.Frame(master=self)
        status_container.pack(side=TOP, fill=BOTH, pady=(15, 0))

        status_label = tkb.Label(
            master=status_container,
            text='Status:',
            font=FONT
        )
        status_label.pack(side=LEFT)

        status = tkb.Label(
            master=status_container,
            text='',
            font=FONT
        )
        status.pack(side=LEFT, padx=(10, 0))

    def load_excel_data(self, excel_path) -> pd:
        df = pd.read_excel(excel_path)
        return df


if __name__ == '__main__':
    app = tkb.Window(
        title='Drop Ship Look Up',
        themename='superhero',
        resizable=(False, False)
    )
    app.withdraw()

    DropShipLookUp()
    app.place_window_center()
    app.deiconify()

    app.mainloop()
