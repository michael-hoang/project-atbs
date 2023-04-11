"""This module contains a class that represents a card payment form GUI."""

import os
import subprocess
import sys
import datetime as dt
import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from calendar import monthrange
from PyPDF2 import PdfReader, PdfWriter
from settings import Settings


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
        self.address = tkb.StringVar(value='')
        self.zip = tkb.StringVar(value='')
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
        
        # Trace
        self.price_1.trace('w', self.update_total)
        self.price_2.trace('w', self.update_total)
        self.price_3.trace('w', self.update_total)
        self.price_4.trace('w', self.update_total)
        self.price_5.trace('w', self.update_total)
        self.card_no.trace('w', self.limit_card_number_size)

        # Images
        image_files = {
            'AMEX': './assets/img/ae.png',
            'Discover': './assets/img/di.png',
            'MasterCard': './assets/img/mc.png',
            'Visa': './assets/img/vi.png',
        }

        self.photoimages = []
        for key, val in image_files.items():
            self.photoimages.append(tkb.PhotoImage(name=key, file=val))

        # Form entries
        self.create_entries_column().pack(side=TOP, fill=X, expand=YES, pady=5)
        self.create_card_info_entries().pack(side=LEFT, fill=X, expand=YES, pady=5, padx=(18,0))

        # Buttons
        self.create_buttonbox().pack(side=LEFT, fill=Y)

        # Event bindings
        self.cardnumber.winfo_children()[1].bind('<BackSpace>', self._do_backspace)
        self.cardnumber.winfo_children()[1].bind('<Key>', self._check_card_number_format)
        self.cardnumber.winfo_children()[1].bind('<KeyRelease>', self._delete_non_numeric_char)
   
        # Register validation callbacks
        self.valid_card_func = master.register(self._validate_card_number)

        # Validate numeric entries
        self.cardnumber.winfo_children()[1].configure(validate='focus', validatecommand=(self.valid_card_func, '%P'))

        # Settings window
        self.create_settings_window()

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
        self.cardnumber = self.create_long_form_entry(container, 'Card Number', self.card_no)
        self.cardnumber.grid(column=0, row=0, columnspan=2, sticky='w')
        card_img = self.create_card_image(container)
        card_img.grid(column=1, row=0, sticky='e', padx=2, pady=(20,0))
        exp = self.create_short_form_entry(container, 'Exp', self.exp)
        exp.grid(column=0, row=1, **grid_para)
        security = self.create_short_form_entry(container, 'Security Code', self.security_no)
        security.grid(column=1, row=1, **grid_para)
        cardholder = self.create_long_form_entry(container, 'Cardholder Name', self.cardholder)
        cardholder.grid(column=0, row=2, columnspan=2, **grid_para)
        address = self.create_long_form_entry(container, 'Billing Address', self.address)
        address.grid(column=0, row=3, columnspan=2, **grid_para)
        zip = self.create_short_form_entry(container, 'Zip Code', self.zip)
        zip.grid(column=0, row=4, columnspan=2, **grid_para)
        mrn = self.create_short_form_entry(container, 'MRN', self.mrn)
        mrn.grid(column=1, row=4, columnspan=2, **grid_para)
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
        self.image_lbl = tkb.Label(container, image='', border=0)
        self.image_lbl.pack()
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
            bootstyle='DEFAULT',
            width=9,
        )
        sub_btn.pack(side=BOTTOM, pady=(0,4))
        
        set_btn = tkb.Button(
            master=container,
            text="Settings",
            command=lambda: self.toggle_settings_window(e=None),
            bootstyle=DARK,
            width=9,
        )
        set_btn.pack(side=BOTTOM, pady=(0,12))

        self.files_btn = tkb.Button(
            master=container,
            text="Files",
            command=self.open_file_folder,
            bootstyle=DARK,
            width=9,
        )
        self.files_btn.pack(side=BOTTOM, pady=(0,12))

        notes_btn = tkb.Button(
            master=container,
            text="Notes",
            command=None,
            bootstyle=DARK,
            width=9,
        )
        notes_btn.pack(side=BOTTOM, pady=(0,12))

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
            'Credit Card No': self.card_no.get(),
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
        try:
            cardnumber = dict_fields['Credit Card No'].replace(' ', '')
            dict_fields[self.get_credit_card_network(cardnumber)] = 'X'
        except:
            pass

        return dict_fields
    
    def export_pdf(self):
        """Export payment information into a PDF form."""
        cardholder = self.cardholder.get().split()
        try:
            file_name = f'{cardholder[0]}_{self.mrn.get()}.pdf'
        except IndexError:
            file_name = f'{self.mrn.get()}.pdf'
            
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

        self.clear_all_entries()
        os.startfile(f"{app_path}\.tmp\{file_name}", "print")

    def get_credit_card_network(self, numbers: str) -> str or bool:
        """Return AMEX, Discover, MasterCard, Visa, or False."""
        prefix = int(numbers[:2])
        length = len(numbers)
        if prefix > 50 and prefix < 56 and length == 16:
            return 'MasterCard'
        elif (prefix == 34 or prefix == 37) and length == 15:
            return 'AMEX'
        elif numbers[0] == '4' and (length == 13 or length == 16):
            return 'Visa'
        elif numbers[:4] == '6011':
            return 'Discover'
        else:
            return False

    def luhns_algo(self, numbers: str) -> bool:
        """Return True if credit card numbers pass Luhn's Algorithm."""
        sum1 = 0
        sum2 = 0
        for i in range(len(numbers)):
            index = -(i + 1)
            if (index % 2) == 0:
                digit_x2_int = int(numbers[index]) * 2
                digit_x2_str = str(digit_x2_int)
                if len(digit_x2_str) > 1:
                    sum2 += int(digit_x2_str[0]) + int(digit_x2_str[1])
                else:
                    sum2 += digit_x2_int
            else:
                sum1 += int(numbers[index])
        # if the total modulo 10 is congruent to 0
        if (sum1 + sum2) % 10 == 0:
            return True

        return False
    
    def _do_backspace(self, e):
        """Force backspace key to do backspace."""
        cardnumber = self.card_no.get()
        length = len(cardnumber)
        try:
            if cardnumber[-1] != ' ':
                self.cardnumber.winfo_children()[1].delete(length, 'end')
        except:
            pass
    
    def _delete_non_numeric_char(self, e):
        """Delete inputted characters that are non-numeric."""
        cardnumber = self.card_no.get()
        try:
            if not cardnumber[-1].isdigit():
                self.cardnumber.winfo_children()[1].delete(0, 'end')
                self.cardnumber.winfo_children()[1].insert('end', cardnumber[:-1])
        except:
            pass
    
    def _check_card_number_format(self, e):
        """Format card numbers with spaces. (Ex. #### #### #### ####)"""
        cardnumber = self.card_no.get()
        length = len(cardnumber)
        try:
            if cardnumber[0] in ('4', '5', '6'):
                if length in (4, 9, 14):
                    self.cardnumber.winfo_children()[1].insert('end', ' ')
                if length > 19:
                    self.cardnumber.winfo_children()[1].set(cardnumber[:19])
            elif cardnumber[0] == '3':
                if length in (4, 11):
                    self.cardnumber.winfo_children()[1].insert('end', ' ')
                if length > 17:
                    self.cardnumber.winfo_children()[1].set(cardnumber[:17])
        except:
            pass
        
    def _validate_card_number(self, card_numbers: str) -> bool:
        """Validate that the input is a number and passes Luhn's algorithm."""
        raw_num = card_numbers.replace(' ', '')
        if raw_num.isdigit() and self.luhns_algo(raw_num):
            try:
                self.image_lbl.configure(image = self.get_credit_card_network(raw_num))
            except:
                pass
            return True
        elif card_numbers == '':
            self.image_lbl.configure(image = '')
            return True
        else:
            self.image_lbl.configure(image = '')
            return False
        
    def limit_card_number_size(self, *args):
        """Limit the number of characters depending on card network type"""
        cardnumber = self.card_no.get()
        length = len(cardnumber)
        try:
            if cardnumber[0] in ('4', '5', '6'):
                if length > 19:
                    self.cardnumber.winfo_children()[1].delete(0, 'end')
                    self.cardnumber.winfo_children()[1].insert('end', cardnumber[:19])
            elif cardnumber[0] == '3':
                if length > 17:
                    self.cardnumber.winfo_children()[1].delete(0, 'end')
                    self.cardnumber.winfo_children()[1].insert('end', cardnumber[:17])
            else:
                self.cardnumber.winfo_children()[1].delete(0, 'end')
        except:
            pass

    def open_file_folder(self):
        """Opens directory containing the exported card payment forms."""
        self.files_btn.config(text='Opening...')
        self.files_btn.after(2000, lambda: self.files_btn.config(text='Files'))
        if getattr(sys, 'frozen', False):
            app_path = os.path.dirname(sys.executable)
        else:
            app_path = os.path.dirname(os.path.abspath(__file__))

        abs_path = f"{app_path}\.tmp"
        check_folder = os.path.isdir(abs_path)
        if not check_folder:
            os.makedirs(abs_path)
            subprocess.call(["attrib", "+h", abs_path]) # hidden directory

        subprocess.Popen(f'explorer "{abs_path}"')

    def clear_all_entries(self):
        """Clear all entries on the form."""
        outer_containers = self.winfo_children()
        for outer_container in outer_containers:
            inner_containers = outer_container.winfo_children()
            for inner_container in inner_containers:
                if inner_container.winfo_class() == 'TFrame':
                    entry_widgets = inner_container.winfo_children()
                    for entry_widget in entry_widgets:
                        if entry_widget.winfo_class() == 'TEntry':
                            entry_widget.delete(0, 'end')

    def create_settings_window(self):
        """"Create the settings window."""
        self.settings_window = tkb.Toplevel(self)
        self.settings_window.title('Settings')
        self.settings_frame = Settings(self.settings_window)
        self.settings_isHidden = True
        self.toggle_settings_window(e=None)
        self.settings_window.protocol('WM_DELETE_WINDOW', func=lambda: self.toggle_settings_window(e=None))
    
    def toggle_settings_window(self, e):
        """Toggles Settings window."""
        if self.settings_isHidden:
            self.settings_window.withdraw()
            self.settings_isHidden = False
            self.lift()
            self.master.attributes('-disabled', 0)
            self.focus_force()
        else:
            self.settings_window.place_window_center()
            self.settings_isHidden = True
            self.master.attributes('-disabled', 1)
            self.settings_window.attributes('-topmost', 1)
            self.settings_window.deiconify()
            self.settings_window.focus()


if __name__ == '__main__':
    app = tkb.Window(
        'Card Payment Form', 'superhero', resizable=(False, False)
    )
    CardPayment(app)
    app.place_window_center()
    app.mainloop()
