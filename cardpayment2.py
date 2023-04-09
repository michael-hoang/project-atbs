"""This module contains a class that represents a card payment form GUI."""

import os
import subprocess
import sys
import re
import datetime as dt
import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from calendar import monthrange
from PyPDF2 import PdfReader, PdfWriter


class CardPayment(tkb.Frame):
    """
    Card Payment Form interface to automate printing of filled credit card forms.
    """

    def __init__(self, master):
        super().__init__(master, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)

        # Form variables
        self.card_no = tkb.StringVar(value='')
        self.exp = tkb.StringVar(value='')
        self.security_no = tkb.StringVar(value='')
        self.cardholder = tkb.StringVar(value='')
        self.mrn = tkb.StringVar(value='')
        self.med_1 = tkb.StringVar(value='')
        self.med_2 = tkb.StringVar(value='')
        self.med_3 = tkb.StringVar(value='')
        self.med_4 = tkb.StringVar(value='')
        self.med_5 = tkb.StringVar(value='')
        self.price_1 = tkb.StringVar(value='')
        self.price_2 = tkb.StringVar(value='')
        self.price_3 = tkb.StringVar(value='')
        self.price_4 = tkb.StringVar(value='')
        self.price_5 = tkb.StringVar(value='')
        
        self.price_1.trace('w', self.update_total)
        self.price_2.trace('w', self.update_total)
        self.price_3.trace('w', self.update_total)
        self.price_4.trace('w', self.update_total)
        self.price_5.trace('w', self.update_total)

        # Images
        image_files = {
            'amex': './assets/img/ae.png',
            'discover': './assets/img/di.png',
            'mastercard': './assets/img/mc.png',
            'visa': './assets/img/vi.png',
        }

        self.photoimages = []
        for key, val in image_files.items():
            self.photoimages.append(tkb.PhotoImage(name=key, file=val))

        # Form entries
        self.create_entries_column().pack(side=TOP, fill=X, expand=YES, pady=5)
        self.create_card_info_entries().pack(side=LEFT, fill=X, expand=YES, pady=5, padx=(18,0))

        # Buttons
        self.create_buttonbox().pack(side=LEFT, fill=Y)
   
    def create_long_form_entry(self, master, label, variable):
        """Create a single long form entry."""
        container = tkb.Frame(master)
        lbl = tkb.Label(container, text=label, width=25)
        lbl.pack(side=TOP, anchor='w')
        ent = tkb.Entry(container, textvariable=variable, width=25)
        ent.pack(side=LEFT, fill=X, expand=YES)
        return container

    def create_short_form_entry(self, master, label, variable):
        """Create a single short form entry."""
        container = tkb.Frame(master)
        lbl = tkb.Label(container, text=label, width=13)
        lbl.pack(side=TOP, anchor='w')
        ent = tkb.Entry(container, textvariable=variable, width=8)
        ent.pack(side=LEFT, fill=X, expand=YES)
        return container

    def create_card_info_entries(self):
        """Create card payment information entries."""
        container = tkb.Frame(self)
        grid_para = {'pady': (4,0), 'sticky': 'w'}
        cardnumber = self.create_long_form_entry(container, 'Card Number', self.card_no)
        cardnumber.grid(column=0, row=0, columnspan=2, sticky='w')
        card_img = self.create_card_image(container)
        card_img.grid(column=1, row=0, sticky='e', padx=2, pady=(20,0))
        exp = self.create_short_form_entry(container, 'Exp', self.exp)
        exp.grid(column=0, row=1, **grid_para)
        security = self.create_short_form_entry(container, 'Security Code', self.security_no)
        security.grid(column=1, row=1, **grid_para)
        cardholder = self.create_long_form_entry(container, 'Cardholder Name', self.cardholder)
        cardholder.grid(column=0, row=2, columnspan=2, **grid_para)
        mrn = self.create_long_form_entry(container, 'MRN', self.mrn)
        mrn.grid(column=0, row=3, columnspan=2, **grid_para)
        return container

    def create_list_entry(self, master, item_label, item_var, price_var):
        """Create a single item form entry."""
        container = tkb.Frame(master)
        container.pack(fill=X, expand=YES)
        item_lbl = tkb.Label(container, text=item_label, width=2, anchor='e')
        item_lbl.pack(side=LEFT, padx=(0,3))
        item_ent = tkb.Entry(container, textvariable=item_var, width=25)
        item_ent.pack(side=LEFT, fill=X, expand=YES)
        price_lbl = tkb.Label(container, text='$', width=2, anchor='e')
        price_lbl.pack(side=LEFT, padx=(0,3))
        price_ent = tkb.Entry(container, textvariable=price_var, width=10)
        price_ent.pack(side=LEFT, fill=X, expand=YES)

    def create_entries_column(self):
        """Create a list column of 5 entries."""
        container = tkb.Frame(self)
        self.create_list_header(container)
        self.create_list_entry(container, '1.', self.med_1, self.price_1)
        self.create_list_entry(container, '2.', self.med_2, self.price_2)
        self.create_list_entry(container, '3.', self.med_3, self.price_3)
        self.create_list_entry(container, '4.', self.med_4, self.price_4)
        self.create_list_entry(container, '5.', self.med_5, self.price_5)
        return container
    
    def create_list_header(self, master):
        """Create labels for the list header."""
        container = tkb.Frame(master)
        container.pack(fill=X, expand=YES)
        item_col_lbl = tkb.Label(container, text='Medication')
        item_col_lbl.pack(side=LEFT, padx=(70,0))
        price_col_lbl = tkb.Label(container, text='Price')
        price_col_lbl.pack(side=RIGHT, padx=(0,25))

    def create_card_image(self, master):
        """Create card network image."""
        container = tkb.Frame(master)
        image = tkb.Label(container, image='', border=0)
        image.pack()
        return container
    
    def create_buttonbox(self):
        """Create the application buttonbox."""
        container = tkb.Frame(self)
        self.total_lbl = tkb.Label(container, text='$0.00', width=12, anchor='center')
        self.total_lbl.pack(side=TOP)

        sub_btn = tkb.Button(
            master=container,
            text="Submit",
            command=self.export_pdf,
            bootstyle=DEFAULT,
            width=9,
        )
        sub_btn.pack(side=BOTTOM, pady=(0,4))

        return container
    
    def get_total(self) -> float:
        """Calculate the total cost of medications."""
        prices = (self.price_1, self.price_2, self.price_3, self.price_4, self.price_5)
        total = 0
        for price in prices:
            try:
                total += float(price.get().replace(',', ''))
            except ValueError:
                continue
        
        return total
    
    def update_total(self, *args):
        """Update the total string variable."""
        self.total_lbl['text'] = "${:,.2f}".format(self.get_total())
    
    def get_dict_fields(self) -> dict:
        """Get a Python dictionary of field names and text values for PdfWriter."""
        dict_fields = {
            'Date': dt.datetime.today().strftime('%m-%d-%Y'),
            'Visa': '',
            'MasterCard': '',
            'Discover': '',
            'AMEX': '',
            'Credit Card No': '',
            'Exp': self.exp.get(),
            'Security No': self.security_no.get(),
            'Cardholder Name': self.cardholder.get(),
            'MRN': self.mrn.get(),
            'Medication Names 1': self.med_1.get(),
            'Medication Names 2': self.med_2.get(),
            'Medication Names 3': self.med_3.get(),
            'Medication Names 4': self.med_4.get(),
            'Medication Names 5': self.med_5.get(),
            'Cost': self.price_1.get(),
            'Cost 2': self.price_2.get(),
            'Cost 3': self.price_3.get(),
            'Cost 4': self.price_4.get(),
            'Cost 5': self.price_5.get(),
            'Total': '${:.2f}'.format(self.get_total()),
            'Notes': '',
        }
        return dict_fields
    
    def export_pdf(self):
        """Export payment information into a PDF form."""
        cardholder = self.cardholder.get().split()
        file_name = f'{cardholder[0] + self.mrn.get()}.pdf'
        fields = self.get_dict_fields()
        if getattr(sys, 'frozen', False):
            app_path = os.path.dirname(sys.executable)
        else:
            app_path = os.path.dirname(os.path.abspath(__file__))

        abs_path = f"{app_path}\.tmp"
        check_folder = os.path.isdir(abs_path)
        if not check_folder:
            os.makedirs(abs_path)
            subprocess.call(["attrib", "+h", abs_path]) # hidden directory

        reader = PdfReader("assets/form/cardpayment.pdf")
        writer = PdfWriter()
        page = reader.pages[0]
        writer.add_page(page)
        writer.update_page_form_field_values(writer.pages[0], fields)
        with open(f".tmp\{file_name}", "wb") as output_stream:
            writer.write(output_stream)

        # self.clear_entries()
        os.startfile(f"{app_path}\.tmp\{file_name}", "print")


if __name__ == '__main__':
    app = tkb.Window(
        'Card Payment Form', 'superhero', resizable=(False, False)
    )
    CardPayment(app)
    app.mainloop()
