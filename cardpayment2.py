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
        self.create_form_entry('Credit Card No.', self.card_no)
        self.create_form_entry('Exp:', self.exp)
        self.create_form_entry('Security No.', self.security_no)

    def create_form_entry(self, label, variable):
        """Create a single form entry."""
        container = tkb.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = tkb.Label(container, text=label, width=14, anchor='e')
        lbl.pack(side=LEFT, padx=5)

        entry = tkb.Entry(container, textvariable=variable)
        entry.pack(side=LEFT, padx=5, fill=X, expand=YES)


if __name__ == '__main__':
    app = tkb.Window(
        'Card Payment Form', 'superhero', resizable=(False, False)
    )
    CardPayment(app)
    app.mainloop()
