"""This module contains a class that represents a card payment form GUI."""

from tkinter import *
from tkinter import messagebox
from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime
from PIL import Image, ImageTk
import os
import subprocess
import sys


class CardPayment:
    """
    Models card payment interface to enter information and then outputs payment 
    form in PDF.
    """

    def __init__(self):
        self.fields = {
            'Date': datetime.today().strftime('%m-%d-%Y'),
            # 'Visa': '/On',
            # 'MasterCard': '/Off',
            # 'Discover': '/Off',
            # 'AMEX': '/Off',
            'Credit Card No': '',
            'Exp': '',
            'Security No': '',
            'Cardholder Name': '',
            'MRN': '',
            'Medication Names 1': '',
            'Medication Names 2': '',
            'Medication Names 3': '',
            'Medication Names 4': '',
            'Medication Names 5': '',
            'Cost': '',
            'Cost 2': '',
            'Cost 3': '',
            'Cost 4': '',
            'Cost 5': '',
            'Total': '',
        }

        self.top = Toplevel()
        self.top.withdraw()
        self.top.attributes('-topmost', 0)
        self.top.config(padx=8, pady=8)
        self.top.resizable(width=False, height=False)
        self.top.title("Card Payment Form")
        self.top.after(ms=50, func=self.update_fields)

        self.cc_icon = PhotoImage(file="img/cc_icon.png")
        self.top.iconphoto(False, self.cc_icon)

        # Checkbutton
        self.alwaysTopVar = IntVar()
        self.always_top_check_button = Checkbutton(self.top, text='Always on top',
                                                   variable=self.alwaysTopVar, onvalue=1, offvalue=0,
                                                   command=self.always_top)
        self.always_top_check_button.grid(
            column=1, row=0, columnspan=2, sticky='NW')

        self.image_paths = [
            "img/generic_card.png",
            "img/amex.png",
            "img/discover.png",
            "img/mastercard.png",
            "img/visa.png"
        ]

        self.tk_images = {}

        for image_path in self.image_paths:
            with Image.open(fp=f"{image_path}") as i:
                img = i.resize(size=(75, 45))
                img_value = ImageTk.PhotoImage(img)
            key = image_path.split("/")[-1]
            image_key = key.split(".")[0]
            self.tk_images[image_key] = img_value

        self.card_button = Button(
            self.top, image=self.tk_images["generic_card"], borderwidth=0, command=self.open_directory)
        self.card_button.grid(
            column=1, row=1, columnspan=2, rowspan=3, sticky="w")

        self.date_text_label = Label(self.top, text="Date:")
        self.date_text_label.grid(column=2, row=1, columnspan=2, sticky="E")
        self.date_num_label = Label(
            self.top, text=datetime.today().strftime('%m-%d-%Y'))
        self.date_num_label.grid(column=4, row=1, sticky="W")

        self.cc_label = Label(self.top, text="Credit Card No.")
        self.cc_label.grid(column=2, row=2, columnspan=2, sticky="E")
        self.cc_entry = Entry(self.top)
        self.cc_entry.grid(column=4, row=2)

        self.exp_label = Label(self.top, text="Exp:")
        self.exp_label.grid(column=2, row=3, columnspan=2, sticky="E")
        self.exp_entry = Entry(self.top)
        self.exp_entry.grid(column=4, row=3)

        self.cvv_label = Label(self.top, text="Security No.")
        self.cvv_label.grid(column=2, row=4, columnspan=2, sticky="E")
        self.cvv_entry = Entry(self.top)
        self.cvv_entry.grid(column=4, row=4)

        self.cardholder_label = Label(self.top, text="Cardholder Name:")
        self.cardholder_label.grid(column=2, row=5, columnspan=2, sticky="E")
        self.cardholder_entry = Entry(self.top)
        self.cardholder_entry.grid(column=4, row=5)

        self.mrn_label = Label(self.top, text="MRN:")
        self.mrn_label.grid(column=2, row=6, columnspan=2, sticky="E")
        self.mrn_entry = Entry(self.top)
        self.mrn_entry.grid(column=4, row=6)

        self.index_label1 = Label(self.top, text="1.")
        self.index_label1.grid(column=1, row=8, sticky="E")
        self.index_label2 = Label(self.top, text="2.")
        self.index_label2.grid(column=1, row=9, sticky="E")
        self.index_label3 = Label(self.top, text="3.")
        self.index_label3.grid(column=1, row=10, sticky="E")
        self.index_label4 = Label(self.top, text="4.")
        self.index_label4.grid(column=1, row=11, sticky="E")
        self.index_label5 = Label(self.top, text="5.")
        self.index_label5.grid(column=1, row=12, sticky="E")

        self.medication_label = Label(self.top, text="Medication Name(s)")
        self.medication_label.grid(column=2, row=7)

        self.amount_label = Label(self.top, text="Amount")
        self.amount_label.grid(column=4, row=7, sticky="W")

        self.med_entry1 = Entry(self.top)
        self.med_entry1.grid(column=2, row=8)
        self.dollar_label1 = Label(self.top, text="$")
        self.dollar_label1.grid(column=3, row=8, padx=5, sticky="E")
        self.dollar_entry1 = Entry(self.top)
        self.dollar_entry1.grid(column=4, row=8)

        self.med_entry2 = Entry(self.top)
        self.med_entry2.grid(column=2, row=9)
        self.dollar_label2 = Label(self.top, text="$")
        self.dollar_label2.grid(column=3, row=9, padx=5, sticky="E")
        self.dollar_entry2 = Entry(self.top)
        self.dollar_entry2.grid(column=4, row=9)

        self.med_entry3 = Entry(self.top)
        self.med_entry3.grid(column=2, row=10)
        self.dollar_label3 = Label(self.top, text="$")
        self.dollar_label3.grid(column=3, row=10, padx=5, sticky="E")
        self.dollar_entry3 = Entry(self.top)
        self.dollar_entry3.grid(column=4, row=10)

        self.med_entry4 = Entry(self.top)
        self.med_entry4.grid(column=2, row=11)
        self.dollar_label4 = Label(self.top, text="$")
        self.dollar_label4.grid(column=3, row=11, padx=5, sticky="E")
        self.dollar_entry4 = Entry(self.top)
        self.dollar_entry4.grid(column=4, row=11)

        self.med_entry5 = Entry(self.top)
        self.med_entry5.grid(column=2, row=12)
        self.dollar_label5 = Label(self.top, text="$")
        self.dollar_label5.grid(column=3, row=12, padx=5, sticky="E")
        self.dollar_entry5 = Entry(self.top)
        self.dollar_entry5.grid(column=4, row=12)

        self.total_text_label = Label(self.top, text="Total")
        self.total_text_label.grid(column=3, row=13, sticky="E")
        self.total_num_label = Label(self.top, text="")
        self.total_num_label.grid(column=4, row=13, sticky="W")

        self.done_button = Button(
            self.top, text="Done", command=self.message_box)
        self.done_button.grid(
            column=1, row=14, columnspan=4, sticky="EW", pady=5)

        # Center window to screen
        self.top.update_idletasks()
        win_width = self.top.winfo_reqwidth()
        win_height = self.top.winfo_reqheight()
        screen_width = self.top.winfo_screenwidth()
        screen_height = self.top.winfo_screenheight()
        x = int(screen_width/2 - win_width/2)
        y = int(screen_height/2 - win_width/2)
        self.top.geometry(f"{win_width}x{win_height}+{x}+{y}")
        self.top.deiconify()
        self.cc_entry.focus_set()

    def always_top(self):
        """Window always display on top."""
        if self.alwaysTopVar.get() == 1:
            self.top.attributes('-topmost', 1)
        elif self.alwaysTopVar.get() == 0:
            self.top.attributes('-topmost', 0)

    def update_fields(self):
        """ 
        Update self.fields attribute with information entered by user in the
        payment form entry.
        """

        self.top.after(ms=50, func=self.update_fields)

        self.fields |= {
            'Date': datetime.today().strftime('%m-%d-%Y'),
            'Credit Card No': self.cc_entry.get(),
            'Exp': self.exp_entry.get(),
            'Security No': self.cvv_entry.get(),
            'Cardholder Name': self.cardholder_entry.get(),
            'MRN': self.mrn_entry.get(),
            'Medication Names 1': self.med_entry1.get(),
            'Medication Names 2': self.med_entry2.get(),
            'Medication Names 3': self.med_entry3.get(),
            'Medication Names 4': self.med_entry4.get(),
            'Medication Names 5': self.med_entry5.get(),
        }

        self.date_num_label.config(text=datetime.today().strftime('%m-%d-%Y'))

        if self.fields['Medication Names 1'] == "":
            cost_1 = 0
            self.fields['Cost'] = ""
        else:
            try:
                cost_1 = float(self.dollar_entry1.get())
            except ValueError:
                cost_1 = 0
                self.fields['Cost'] = ""
            else:
                self.fields['Cost'] = "${:,.2f}".format(cost_1)

        if self.fields['Medication Names 2'] == "":
            cost_2 = 0
            self.fields['Cost 2'] = ""
        else:
            try:
                cost_2 = float(self.dollar_entry2.get())
            except ValueError:
                cost_2 = 0
                self.fields['Cost 2'] = ""
            else:
                self.fields['Cost 2'] = "${:,.2f}".format(cost_2)

        if self.fields['Medication Names 3'] == "":
            cost_3 = 0
            self.fields['Cost 3'] = ""
        else:
            try:
                cost_3 = float(self.dollar_entry3.get())
            except ValueError:
                cost_3 = 0
                self.fields['Cost 3'] = ""
            else:
                self.fields['Cost 3'] = "${:,.2f}".format(cost_3)

        if self.fields['Medication Names 4'] == "":
            cost_4 = 0
            self.fields['Cost 4'] = ""
        else:
            try:
                cost_4 = float(self.dollar_entry4.get())
            except ValueError:
                cost_4 = 0
                self.fields['Cost 4'] = ""
            else:
                self.fields['Cost 4'] = "${:,.2f}".format(cost_4)

        if self.fields['Medication Names 5'] == "":
            cost_5 = 0
            self.fields['Cost 5'] = ""
        else:
            try:
                cost_5 = float(self.dollar_entry5.get())
            except ValueError:
                cost_5 = 0
                self.fields['Cost 5'] = ""
            else:
                self.fields['Cost 5'] = "${:,.2f}".format(cost_5)

        total = cost_1 + cost_2 + cost_3 + cost_4 + cost_5
        self.total_num_label.config(text="${:,.2f}".format(total))
        self.fields['Total'] = "${:,.2f}".format(total)

        try:
            if self.fields['Credit Card No'][0] == '3':
                amex_img = self.tk_images["amex"]
                self.card_button.config(image=amex_img)
            elif self.fields['Credit Card No'][0] == '4':
                visa_img = self.tk_images["visa"]
                self.card_button.config(image=visa_img)
            elif self.fields['Credit Card No'][0] == '5':
                mastercard_img = self.tk_images["mastercard"]
                self.card_button.config(image=mastercard_img)
            elif self.fields['Credit Card No'][0] == '6':
                discover_img = self.tk_images["discover"]
                self.card_button.config(image=discover_img)
        except IndexError:
            generic_card_img = self.tk_images["generic_card"]
            self.card_button.config(image=generic_card_img)

    def export_pdf(self):
        """Outputs payment information into a PDF form."""

        name_list = self.fields['Cardholder Name'].split()
        formatted_name = ""
        for name in name_list:
            formatted_name += name.lower()
            formatted_name += "_"
        formatted_name += self.fields['MRN']
        formatted_file_name = f"{formatted_name}.pdf"

        if getattr(sys, 'frozen', False):
            app_path = os.path.dirname(sys.executable)
        else:
            app_path = os.path.dirname(os.path.abspath(__file__))

        abs_path = f"{app_path}\PaymentForms"
        check_folder = os.path.isdir(abs_path)
        if not check_folder:
            os.makedirs(abs_path)

        reader = PdfReader("templates\card_payment_form.pdf")
        writer = PdfWriter()
        page = reader.pages[0]
        writer.add_page(page)
        writer.update_page_form_field_values(writer.pages[0], self.fields)
        with open(f"PaymentForms\{formatted_file_name}", "wb") as output_stream:
            writer.write(output_stream)

        os.startfile(f"{app_path}\PaymentForms\{formatted_file_name}", "print")

    def clear_entries(self):
        """Clear all entries."""

        self.cc_entry.delete(0, END)
        self.exp_entry.delete(0, END)
        self.cvv_entry.delete(0, END)
        self.cardholder_entry.delete(0, END)
        self.mrn_entry.delete(0, END)
        self.med_entry1.delete(0, END)
        self.med_entry2.delete(0, END)
        self.med_entry3.delete(0, END)
        self.med_entry4.delete(0, END)
        self.med_entry5.delete(0, END)
        self.dollar_entry1.delete(0, END)
        self.dollar_entry2.delete(0, END)
        self.dollar_entry3.delete(0, END)
        self.dollar_entry4.delete(0, END)
        self.dollar_entry5.delete(0, END)

    def message_box(self):
        """Prompt user for confirmation when 'Done' button is clicked."""

        answer = messagebox.askyesno(
            title="Confirm", message="Are you sure?", parent=self.top)

        if answer:
            self.export_pdf()
            self.clear_entries()
            self.cc_entry.focus_set()

    def open_directory(self):
        """Opens directory containing exported credit card forms."""

        if getattr(sys, 'frozen', False):
            app_path = os.path.dirname(sys.executable)
        else:
            app_path = os.path.dirname(os.path.abspath(__file__))

        abs_path = f"{app_path}\PaymentForms"
        check_folder = os.path.isdir(abs_path)
        if not check_folder:
            os.makedirs(abs_path)

        subprocess.Popen(f'explorer "{abs_path}"')


if __name__ == '__main__':
    root = Tk()
    cp = CardPayment()

    root.mainloop()
