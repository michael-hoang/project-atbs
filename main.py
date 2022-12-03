import tkinter as tk
from PIL import Image, ImageTk
from wudCalc import WrapUpDateCalculator
from cpForm import CardPayment
from mapSearch import Map
from pwManager import PasswordManager
from authentication import Authenticator


FONT = ('Serif', 14, 'normal')
BG_COLOR = '#30323D'
FG_COLOR = 'white'


def open_WrapUpDateCalculator():
    """Instantiate WrapUpDateCalculator object in a new TopLevel window."""
    top = WrapUpDateCalculator()


def open_CardPaymentForm():
    """Instantiate CardPayment object in a new TopLevel window."""
    top = CardPayment()


def open_MapSearch():
    """Instantiate Map object in a new TopLevel window."""
    top = Map()


def open_PasswordManager():
    """Instantiate Password Manager in a new TopLevel window."""
    a = Authenticator()
    while True:
        if a.isVerfied:
            a.root.destroy()
            a.root.protocol('WM_DELETE_WINDOW', PasswordManager())
            break
    


root = tk.Tk()
root.withdraw()
root.title('Project AtBS')
root.config(bg=BG_COLOR)
root.resizable(width=False, height=False)

atbs_icon = tk.PhotoImage(file="img/atbs_icon.png")
root.iconphoto(False, atbs_icon)

# Card payment form
cc_img_open = Image.open(fp='img/cc_icon.png')
cc_img_resized = cc_img_open.resize(size=(50, 50))
cc_img = ImageTk.PhotoImage(cc_img_resized)
cp_but = tk.Button(text='  Payment', image=cc_img, compound='left',
                   font=FONT, fg=FG_COLOR, bg=BG_COLOR, command=open_CardPaymentForm,
                   anchor='w', padx=10, pady=5, width=208)
cp_but.grid(column=0, row=0, sticky='EW')

# Wrap up date calculator
cal_calc_img_open = Image.open(fp='img/cal_calc.png')
cal_calc_img_resized = cal_calc_img_open.resize(size=(50, 50))
cal_calc_img = ImageTk.PhotoImage(cal_calc_img_resized)
wud_but = tk.Button(text='  Wrap Up', image=cal_calc_img, compound='left',
                    font=FONT, fg=FG_COLOR, bg=BG_COLOR, command=open_WrapUpDateCalculator,
                    anchor='w', padx=10, pady=5, width=207)
wud_but.grid(column=0, row=1, sticky='EW')

# Map search
map_img_open = Image.open(fp='img/map_icon.png')
map_img_resized = map_img_open.resize(size=(50, 50))
map_img = ImageTk.PhotoImage(map_img_resized)
m_but = tk.Button(text='  Map', image=map_img, compound='left', font=FONT,
                  fg=FG_COLOR, bg=BG_COLOR, command=open_MapSearch, anchor='w',
                  padx=10, pady=5, width=207)
m_but.grid(column=0, row=2, sticky='EW')

# Password Manager
lock_img_open = Image.open(fp='img/lock_icon.png')
lock_img_resized = lock_img_open.resize(size=(50, 50))
lock_img = ImageTk.PhotoImage(lock_img_resized)
pm_but = tk.Button(text='  Password', image=lock_img, compound='left', font=FONT,
                   fg=FG_COLOR, bg=BG_COLOR, command=open_PasswordManager, anchor='w',
                   padx=10, pady=5, width=207)
pm_but.grid(column=0, row=3, sticky='EW')

# Center window to screen
root.update_idletasks()
win_width = root.winfo_reqwidth()
win_height = root.winfo_reqheight()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int(screen_width/2 - win_width/2)
y = int(screen_height/2 - win_width/2)
root.geometry(f"{win_width}x{win_height}+{x}+{y}")
root.deiconify()
# root.attributes('-topmost', 1)

root.mainloop()
