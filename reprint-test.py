import datetime
import os
import time
import win32api
import win32print

DAYS_UNTIL_EXPIRATION = 7
SECONDS_PER_DAY = 86400
SECONDS_PER_HOUR = 3600
SECONDS_PER_MINUTE = 60

FILES_PATH = '.files/'


def get_epoch_creation_time() -> int:
    epoch_current_time = int(time.time())
    return epoch_current_time


def get_epoch_exp_time(epoch_ctime: str, days_expiration=7) -> int:
    epoch_exp_time = int(epoch_ctime) + (days_expiration * SECONDS_PER_DAY)
    return epoch_exp_time


def get_formatted_exp_time(epoch_exp_time: int) -> str:
    epoch_current_time = time.time()
    remaining_epoch_time = epoch_exp_time - epoch_current_time
    days = int(remaining_epoch_time // SECONDS_PER_DAY)
    remaining_epoch_sec = remaining_epoch_time % SECONDS_PER_DAY
    hours = int(remaining_epoch_sec // SECONDS_PER_HOUR)
    remaining_epoch_sec %= SECONDS_PER_HOUR
    minutes = int(remaining_epoch_sec // SECONDS_PER_MINUTE)
    formatted_exp_time = f'{days}d {hours}h {minutes}m'
    return formatted_exp_time


def show_printers():
    pdf_path = '.\\assets\\form\cardpayment-form.pdf'

    all_printers = [printer[2] for printer in win32print.EnumPrinters(2)]
    all_network_printers = [printer[2] for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_CONNECTIONS, None, 1)]
    print(all_network_printers)

    original_default_printer = win32print.GetDefaultPrinter()
    microsoft_print_to_pdf = all_printers[3]

    print(f'Original: {original_default_printer}')
    print(f'Selected: {microsoft_print_to_pdf}')

    win32print.SetDefaultPrinter(microsoft_print_to_pdf)
    print(win32print.GetDefaultPrinter())
    # os.startfile(pdf_path, 'print')
    
    # win32print.SetDefaultPrinter(original_default_printer)



# # Iterate through .files directory and get metadata
# for file in os.listdir(FILES_PATH):
#     file_path = os.path.join(FILES_PATH, file)
#     epoch_creation_time = os.path.getctime(file_path)

#     epoch_exp_time = get_epoch_exp_time(epoch_creation_time)
#     exp_time = get_formatted_exp_time(epoch_exp_time)

#     print(exp_time)


data = {
    'Mike_123456': {
        'epoch_ctime': '1683185563',
        'fields': {
            'Date': '5/3/2023',
            'Visa': 'X',
            'MasterCard': '',
            'Discover': '',
            'AMEX': '',
            'Credit Card No': '',
            'Exp': '5/25',
            'Security No': '123',
            'Billing Address': '13651 Lorna St',
            'Zip Code': '92844',
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
            'Notes': '',
        }
    }
}

show_printers()
