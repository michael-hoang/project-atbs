"""This module contains a class that represents a card payment form GUI."""

import os
import subprocess
import sys
import time
import datetime as dt
import tkinter as tk
import ttkbootstrap as tkb

from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from tkinter.ttk import Style
from PyPDF2 import PdfReader, PdfWriter
from settings import Settings
from dateutil.relativedelta import relativedelta

from refill import Refill

class CardPayment(tkb.Frame):
    """
    Card Payment Form interface to automate printing of filled credit card forms.
    """

    def __init__(self,root, master):
        super().__init__(master, padding=(12, 10))
        self.pack(side=LEFT, fill=X, expand=YES, padx=(0, 5))
        style = Style()
        style.configure('TButton', font=('', 10, ''))
        self.root = root
        
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
        self.security_no.trace('w', self.limit_sec_code_len)

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
        self.create_buttonbox().pack(side=LEFT, fill=Y, padx=(18, 0), pady=(0, 1))

        # Event bindings
        self.cardnumber.winfo_children()[1].bind('<BackSpace>', self._do_backspace)
        self.cardnumber.winfo_children()[1].bind('<Key>', self._check_card_number_format)
        self.cardnumber.winfo_children()[1].bind('<KeyRelease>', self._delete_non_numeric_char)
        self.security_ent.winfo_children()[1].bind('<KeyRelease>', self._delete_non_numeric_char_for_sec_code)
        root.bind('<Control-Return>', self.submit_message_box)
        # root.bind('<Control-s>', self.toggle_settings_window)
        root.bind('<Control-n>', self.toggle_notes_window)
   
        # Register validation callbacks
        self.valid_card_func = root.register(self._validate_card_number)
        self.valid_digit_func = root.register(self._validate_only_digits)
        self.valid_exp_func = root.register(self._validate_exp_date)
        self.valid_sec_code_func = root.register(self._validate_security_code)

        # Validate numeric entries
        self.cardnumber.winfo_children()[1].configure(validate='focus', validatecommand=(self.valid_card_func, '%P'))
        self.exp_ent.winfo_children()[1].configure(validate='focus', validatecommand=(self.valid_exp_func, '%P'))
        self.zipcode.winfo_children()[1].configure(validate='key', validatecommand=(self.valid_digit_func, '%P'))
        self.mrn_ent.winfo_children()[1].configure(validate='key', validatecommand=(self.valid_digit_func, '%P'))
        self.security_ent.winfo_children()[1].configure(validate='focus', validatecommand=(self.valid_sec_code_func, '%P'))

        # Settings window
        # self.create_settings_window()
        # Notes window
        self.create_notes_window()

        # After method
        self.remove_files()
        self.after(ms=3_600_000, func=self.remove_files) # after 1 hour

    def create_long_form_entry(self, master, label, variable):
        """Create a single long form entry."""
        container = tkb.Frame(master)
        lbl = tkb.Label(container, text=label, width=25, font=('', 10, ''))
        lbl.pack(side=TOP, anchor='w')
        ent = tkb.Entry(container, textvariable=variable, width=25, font=('', 10, ''))
        ent.pack(side=LEFT, fill=X, expand=YES)
        return container

    def create_short_form_entry(self, master, label, variable):
        """Create a single short form entry."""
        container = tkb.Frame(master)
        lbl = tkb.Label(container, text=label, width=13, font=('', 10, ''))
        lbl.pack(side=TOP, anchor='w')
        ent = tkb.Entry(container, textvariable=variable, width=8, font=('', 10, ''))
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
        self.exp_ent = self.create_short_form_entry(container, 'Exp', self.exp)
        self.exp_ent.grid(column=0, row=1, **grid_para)
        self.security_ent = self.create_short_form_entry(container, 'Security Code', self.security_no)
        self.security_ent.grid(column=1, row=1, **grid_para)
        cardholder = self.create_long_form_entry(container, 'Cardholder Name', self.cardholder)
        cardholder.grid(column=0, row=2, columnspan=2, **grid_para)
        address = self.create_long_form_entry(container, 'Billing Address', self.address)
        address.grid(column=0, row=3, columnspan=2, **grid_para)
        self.zipcode = self.create_short_form_entry(container, 'Zip Code', self.zip)
        self.zipcode.grid(column=0, row=4, columnspan=2, **grid_para)
        self.mrn_ent = self.create_short_form_entry(container, 'MRN', self.mrn)
        self.mrn_ent.grid(column=1, row=4, columnspan=2, **grid_para)
        return container

    def create_list_entry(self, master, item_label, item_var, price_var):
        """Create a single item form entry."""
        container = tkb.Frame(master)
        container.pack(fill=X, expand=YES)
        item_lbl = tkb.Label(container, text=item_label, width=2, anchor='e', font=('', 10, ''))
        item_lbl.pack(side=LEFT, padx=(0,3))
        item_ent = tkb.Entry(container, textvariable=item_var, width=25)
        item_ent.pack(side=LEFT, fill=X, expand=YES)
        price_lbl = tkb.Label(container, text='$', width=2, anchor='e', font=('', 10, ''))
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
        item_col_lbl = tkb.Label(container, text='Medication', font=('', 10, ''))
        item_col_lbl.pack(side=LEFT, padx=(70,0))
        price_col_lbl = tkb.Label(container, text='Price', font=('', 10, ''))
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
        self.total_lbl = tkb.Label(container, text='$0.00', width=12, anchor='center', font=('', 10, ''))
        self.total_lbl.pack(side=TOP)

        self.sub_btn = tkb.Button(
            master=container,
            text="Submit",
            command=lambda: self.submit_message_box(e=None),
            bootstyle='DEFAULT',
            width=9,
            style='TButton',
        )
        self.sub_btn.pack(side=BOTTOM, pady=(0,4))
        
        set_btn = tkb.Button(
            master=container,
            text="Settings",
            command=lambda: self.toggle_settings_window(e=None),
            bootstyle=DARK,
            width=9,
            style='TButton.dark'
        )
        set_btn.pack(side=BOTTOM, pady=(0,12))

        self.files_btn = tkb.Button(
            master=container,
            text="Files",
            command=self.open_file_folder,
            bootstyle=DARK,
            width=9,
            style='TButton.dark'
        )
        self.files_btn.pack(side=BOTTOM, pady=(0,12))

        notes_btn = tkb.Button(
            master=container,
            text="Notes",
            command=lambda: self.toggle_notes_window(e=None),
            bootstyle=DARK,
            width=9,
            style='TButton.dark'
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
            'Billing Address': self.address.get(),
            'Zip Code': self.zip.get(),
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
            'Notes': self.notes_text_box.get(1.0, 'end-1c'), # -1c removes the added newline
        }
        try:
            cardnumber = dict_fields['Credit Card No'].replace(' ', '')
            if self.luhns_algo(cardnumber):
                dict_fields[self.get_credit_card_network(cardnumber)] = 'X'
        except:
            pass

        return dict_fields
    
    def submit_message_box(self, e):
        """Prompt user for confirmation when 'Submit' button is pressed."""
        answer = Messagebox.yesno(
            parent=self,
            title='Confirm Submit',
            message='Are you sure you want to submit?'
        )
        if answer == 'Yes':
            self.export_pdf()
            self.clear_all_entries()
            self.sub_btn.config(text='Printing...')
            self.sub_btn.after(5000, lambda: self.sub_btn.config(text='Submit'))
            self.focus_force()
    
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

        abs_path = f"{app_path}\.files"
        check_folder = os.path.isdir(abs_path)
        if not check_folder:
            os.makedirs(abs_path)
            subprocess.call(["attrib", "+h", abs_path]) # hidden directory

        reader = PdfReader("assets/form/cardpayment-form.pdf")
        writer = PdfWriter()
        page = reader.pages[0]
        writer.add_page(page)
        writer.update_page_form_field_values(writer.pages[0], fields)
        with open(f".files\{file_name}", "wb") as output_stream:
            writer.write(output_stream)

        os.startfile(f"{app_path}\.files\{file_name}", "print")

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
    
    def _delete_non_numeric_char_for_sec_code(self, e):
        """Delete inputted characters that are non-numeric."""
        sec_code = self.security_no.get()
        try:
            if not sec_code[-1].isdigit():
                self.security_ent.winfo_children()[1].delete(0, 'end')
                self.security_ent.winfo_children()[1].insert('end', sec_code[:-1])
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
        
    def _validate_only_digits(self, P: str) -> bool:
        """Validate that the input is strictly a digit."""
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
        
    def _validate_exp_date(self, P: str) -> bool:
        """Validate that the inputted date is not expired."""
        exp_str = P
        date_fmt = ('%m/%y', '%m-%y', '%m/%Y', '%m-%Y')
        for fmt in date_fmt:
            try:
                exp_date = dt.datetime.strptime(exp_str, fmt) + relativedelta(months=1) - relativedelta(days=1)
                if exp_date > dt.datetime.today():
                    return True
            except ValueError:
                pass

        if exp_str == '':
            return True
        else:
            return False
        
    def _validate_security_code(self, P: str) -> bool:
        """Validate that the data is strictly a digit, and is only 3 or 4 chars long."""
        sec_code = P
        try:
            first_digit = self.card_no.get()[0]
            sec_code_len = len(sec_code)
            for c in sec_code:
                if not c.isdigit():
                    return False
                
            if first_digit != '3':
                if sec_code_len == 3 or sec_code == '':
                    return True
                return False
            elif first_digit == '3':
                if sec_code_len == 4 or sec_code == '':
                    return True
                return False
        except:
            pass
        if sec_code == '':
            return True
        else:
            return False
        
    def limit_sec_code_len(self, *args):
        """Limit the number of characters depending on card network type"""
        try:
            first_digit = self.card_no.get()[0]
            sec_code = self.security_no.get()
            sec_code_len = len(sec_code)
            if first_digit != '3' and sec_code_len > 3:
                self.security_ent.winfo_children()[1].delete(0, 'end')
                self.security_ent.winfo_children()[1].insert('end', sec_code[:3])
            elif first_digit == '3' and sec_code_len > 4:
                self.security_ent.winfo_children()[1].delete(0, 'end')
                self.security_ent.winfo_children()[1].insert('end', sec_code[:4])
        except IndexError:
            pass
            
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

        abs_path = f"{app_path}\.files"
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
        self.notes_text_box.delete(1.0, END)
        self.cardnumber.winfo_children()[1].focus_force()
        self.exp_ent.winfo_children()[1].focus_force()
        self.security_ent.winfo_children()[1].focus_force()              

    def center_child_to_parent(self, child, parent, window_name):
        """Center child window to parent window."""
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_reqwidth()
        parent_height = parent.winfo_reqheight()
        if window_name == 'notes':
            dx = int((parent_width / 2)) - 120
            dy = int((parent_height / 2)) - 75
        elif window_name == 'settings':
            dx = int((parent_width / 2)) - 600
            dy = int((parent_height / 2)) - 300
        child.geometry('+%d+%d' % (parent_x + dx, parent_y + dy))

    def create_notes_window(self):
        """Create Notes window."""
        self.notes_window = tkb.Toplevel(self)
        self.notes_window.title('Notes')
        self.notes_window.geometry('240x150')
        self.notes_window.resizable(False, False)
        # self.notes_window.overrideredirect(True)
        self.notes_text_box = tk.Text(self.notes_window, font=('Sergoe UI', 14, 'normal'), wrap=WORD)
        self.notes_text_box.pack(expand=YES)
        self.notes_isHidden = True
        self.toggle_notes_window(e=None)
        self.notes_window.protocol('WM_DELETE_WINDOW', func=lambda: self.toggle_notes_window(e=None))
        self.notes_window.bind('<Escape>', self.toggle_notes_window)
        

    def toggle_notes_window(self, e):
        """Toggle Notes window."""
        if self.notes_isHidden:
            self.notes_isHidden = False
            self.lift()
            self.root.attributes('-disabled', 0)
            self.focus()
            self.notes_window.withdraw()
        else:
            self.center_child_to_parent(self.notes_window, self.master, 'notes')
            self.notes_isHidden = True
            self.root.attributes('-disabled', 1)
            self.notes_window.attributes('-topmost', 1)
            self.notes_window.deiconify()
            self.notes_text_box.focus()
            

    def create_settings_window(self):
        """"Create the settings window."""
        self.settings_window = tkb.Toplevel(self)
        self.settings_window.title('Settings')
        self.settings_window.resizable(False, False)
        # self.notes_window.overrideredirect(True)
        self.settings_frame = Settings(self.settings_window)
        self.settings_isHidden = True
        self.toggle_settings_window(e=None)
        self.settings_window.protocol('WM_DELETE_WINDOW', func=lambda: self.toggle_settings_window(e=None))
        self.settings_window.bind('<Escape>', self.toggle_settings_window)
    
    def toggle_settings_window(self, e):
        """Toggle Settings window."""
        if self.settings_isHidden:
            self.settings_isHidden = False
            self.lift()
            self.root.attributes('-disabled', 0)
            self.focus()
            self.settings_window.withdraw()
        else:
            self.center_child_to_parent(self.settings_window, self.master, 'settings')
            self.settings_isHidden = True
            self.root.attributes('-disabled', 1)
            self.settings_window.attributes('-topmost', 1)
            self.settings_window.deiconify()
            self.settings_window.focus()

    def remove_files(self):
        """Remove files in .files older than 7 days."""
        
        current_time = time.time()

        if getattr(sys, 'frozen', False):
            app_path = os.path.dirname(sys.executable)
        else:
            app_path = os.path.dirname(os.path.abspath(__file__))

        abs_path = f"{app_path}\.files"
        check_folder = os.path.isdir(abs_path)
        if not check_folder:
            os.makedirs(abs_path)
            subprocess.call(["attrib", "+h", abs_path]) # hidden directory

        for f in os.listdir(path=abs_path):
            file_path = os.path.join(abs_path, f)
            creation_time = os.path.getctime(file_path)
            if (current_time - creation_time) // (24 * 3600) >= 7:
                os.unlink(file_path)

        self.after(ms=3_600_000, func=self.remove_files) # after 1 hour


if __name__ == '__main__':
    app = tkb.Window(
        'Card Payment Form', 'superhero', resizable=(False, False)
    )
    app.config(padx=25, pady=25)
    app.place_window_center()

    refill_frame = tkb.Labelframe(app, text='Refill Coordination')
    refill_frame.pack(side=LEFT)
    refill = Refill(app, refill_frame)

    cardpayment_frame = tkb.Labelframe(app, text='Card Payment')
    cardpayment_frame.pack(side=LEFT, padx=(25, 0))
    cardpayment = CardPayment(app, cardpayment_frame)

    app.mainloop()
