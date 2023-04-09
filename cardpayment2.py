"""This module contains a class that represents a card payment form GUI."""

import ttkbootstrap as tkb
from ttkbootstrap.constants import *


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

        # Form entries
        self.create_card_info_entries().pack(side=BOTTOM, fill=X, expand=YES, pady=5, padx=(18,0))
        self.create_entries_column().pack(side=TOP, fill=X, expand=YES, pady=5)

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


if __name__ == '__main__':
    app = tkb.Window(
        'Card Payment Form', 'superhero', resizable=(False, False)
    )
    CardPayment(app)
    app.mainloop()
