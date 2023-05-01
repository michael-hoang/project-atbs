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
        self.excel_data_df = self.load_excel_data(EXCEL_PATH)

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

        self.ndc_entry = tkb.Entry(
            master=ndc_input_container,
            width=12,
            font=FONT,
        )
        self.ndc_entry.pack(side=LEFT, padx=(10, 0))

        check_btn = tkb.Button(
            master=ndc_input_container,
            text='Check',
            style='TButton',
            command=self.check_if_dropship,
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

        self.drug_name = tkb.Text(
            master=drug_name_container,
            font=FONT,
            height=3,
            width=30,
            state='disabled'
        )
        self.drug_name.pack(side=LEFT, padx=(10, 0))

        status_container = tkb.Frame(master=self)
        status_container.pack(side=TOP, fill=BOTH, pady=(15, 0))

        status_label = tkb.Label(
            master=status_container,
            text='Status:',
            font=FONT
        )
        status_label.pack(side=LEFT)

        self.status = tkb.Label(
            master=status_container,
            text='',
            font=FONT
        )
        self.status.pack(side=LEFT, padx=(10, 0))

        self.ndc_entry.bind('<FocusIn>', self.on_click_select)

    def on_click_select(self, event):
        event.widget.select_range(0, END)

    def load_excel_data(self, excel_path) -> pd:
        df = pd.read_excel(excel_path, dtype={'NDC': str})
        return df

    def iterate_excel_data(self, ndc) -> tuple:
        item = ''
        for index, row in self.excel_data_df.iterrows():
            for column_name, value in row.items():
                if column_name == 'NDC':
                    if value == ndc:
                        continue
                    else:
                        break
                elif column_name == 'Item':
                    item = value
                elif column_name == 'Drop Ship':
                    if value == True:
                        return (item, True)
                    else:
                        return (item, False)

        return (None, None)

    def check_if_dropship(self):
        ndc = self.ndc_entry.get().strip()
        item, dropship = self.iterate_excel_data(ndc)
        self.drug_name.config(state='normal')
        self.drug_name.delete(1.0, END)
        if dropship:
            self.drug_name.insert(1.0, item)
            self.status.config(text='DROP SHIP', foreground='magenta2')
        elif dropship == False:
            self.drug_name.insert(1.0, item)
            self.status.config(text='NOT DROP SHIP', foreground='green3')
        else:
            self.drug_name.insert(1.0, 'NDC not in database')
            self.status.config(text='N/A', foreground='')
        
        self.drug_name.config(state='disabled')


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
