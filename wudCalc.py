import datetime as dt
import tkinter as tk
import pyperclip
from tkinter import END


FONT = ('Serif', 14, 'normal')
BG_COLOR = '#30323D'
FG_COLOR = 'white'
FG_COLOR2 = '#E8C547'
BG_COLOR3 = '#5C80BC'
BUTTON_BG_COLOR = '#4D5061'

class WrapUpDateCalculator():
    """Models a wrap up date calculator. Calculates next wrap up date."""

    def __init__(self):
        """Initializes WrapUpDateCalculator graphical user interface."""

        self.top = tk.Toplevel()
        self.top.withdraw()
        self.top.attributes('-topmost', 0)
        self.top.title('Wrap Up Date Calculator')
        self.top.config(bg=BG_COLOR,
                        padx=15,
                        pady=5)
        self.top.resizable(width=False, height=False)

        self.cal_calc_icon = tk.PhotoImage(file="img/cal_calc.png")
        self.top.iconphoto(False, self.cal_calc_icon)

        # Checkbutton
        self.alwaysTopVar = tk.IntVar()
        self.always_top_check_button = tk.Checkbutton(self.top, text='Always on top',
                                        variable=self.alwaysTopVar, onvalue=1, offvalue=0,
                                        bg=BG_COLOR, fg=FG_COLOR, font=('Serif', 10, 'normal'),
                                        activebackground=BG_COLOR, activeforeground=FG_COLOR,
                                        selectcolor=BG_COLOR, command=self.always_top)
        self.always_top_check_button.grid(column=0, row=0, sticky='NW', pady=(0, 5))
        
        # Dispense Date Label & Entry
        self.dispense_date_label = tk.Label(self.top, text='Dispense Date:',
                                            bg=BG_COLOR,
                                            fg=FG_COLOR,
                                            font=FONT)
        self.dispense_date_label.grid(column=0, row=1, sticky='E')
        self.dispense_date_entry = tk.Entry(self.top, bg=FG_COLOR,
                                            fg=BG_COLOR,
                                            font=FONT,
                                            width=12)
        self.dispense_date_entry.focus()
        self.dispense_date_entry.grid(column=1, row=1,
                                    padx=10)

        # Day Supply Label & Entry
        self.day_supply_label = tk.Label(self.top, text='Day Supply:',
                                        bg=BG_COLOR,
                                        fg=FG_COLOR,
                                        font=FONT)
        self.day_supply_label.grid(column=0, row=2, sticky='E')
        self.day_supply_entry = tk.Entry(self.top, bg=FG_COLOR,
                                        fg=BG_COLOR,
                                        font=FONT,
                                        width=12)
        self.day_supply_entry.grid(column=1, row=2, pady=5)

        # Radiobuttons
        self.v = tk.IntVar()
        self.v.set(1)
        self.seven_days = tk.Radiobutton(self.top, text='7 days before', variable=self.v, value=1,
                                        bg=BG_COLOR, fg=FG_COLOR, font=('Serif', 10, 'normal'),
                                        activebackground=BG_COLOR, activeforeground=FG_COLOR,
                                        selectcolor=BG_COLOR)
        self.seven_days.grid(column=0, row=3)
        self.nine_days = tk.Radiobutton(self.top, text='9 days before', variable=self.v, value=2,
                                        bg=BG_COLOR, fg=FG_COLOR, font=('Serif', 10, 'normal'),
                                        activebackground=BG_COLOR, activeforeground=FG_COLOR,
                                        selectcolor=BG_COLOR)
        self.nine_days.grid(column=1, row=3)
        
        # Calculate Button
        self.calculate_button = tk.Button(self.top, text='Calculate',
                                        bg=BUTTON_BG_COLOR,
                                        fg=FG_COLOR,
                                        font=FONT,
                                        activebackground=FG_COLOR2,
                                        borderwidth=0, command=self.calculate_wrap_up_date)
        self.calculate_button.grid(column=0, row=4,
                                    sticky='EW',
                                    columnspan=2,
                                    padx=5,
                                    pady=(10, 5))

        # Wrap Up Date Label
        self.wrap_up_date_text = tk.Label(self.top, text='Wrap Up Date:', 
                                            font=FONT,
                                            bg=BG_COLOR,
                                            fg=FG_COLOR2)
        self.wrap_up_date_text.grid(column=0, row=6, pady=(2, 7))
        self.wrap_up_date = tk.Label(self.top, text='',
                                        font=FONT,
                                        bg=BG_COLOR,
                                        fg=FG_COLOR2)
        self.wrap_up_date.grid(column=1, row=6, pady=(2, 7))

        # Clear button
        self.clear_button = tk.Button(self.top, text='Clear',
                                    bg=BUTTON_BG_COLOR,
                                    fg=FG_COLOR,
                                    font=FONT,
                                    activebackground=FG_COLOR2,
                                    borderwidth=0, command=self.clear)
        self.clear_button.grid(column=1, row=5, sticky='EW', padx=(5, 5), pady=(0, 10))

        # Exit button
        self.exit_button = tk.Button(self.top, text='Exit',
                                    bg=BUTTON_BG_COLOR,
                                    fg=FG_COLOR,
                                    font=FONT,
                                    activebackground=FG_COLOR2,
                                    borderwidth=0, command=self.top.destroy)
        self.exit_button.grid(column=0, row=5, sticky='EW', padx=(5, 0), pady=(0, 10))

        # Center window to screen
        self.top.update_idletasks()
        win_width = self.top.winfo_reqwidth()
        win_height = self.top.winfo_reqheight()
        screen_width = self.top.winfo_screenwidth()
        screen_height = self.top.winfo_screenheight()
        x = int(screen_width/2 - win_width/2)
        y = int(screen_height/2 - win_height/2)
        self.top.geometry(f"{win_width}x{win_height}+{x}+{y}")
        self.top.deiconify()

        self.top.bind('<Return>', self.calculate_wrap_up_date)
        self.top.bind('<Delete>', self.clear)

        # self.top.update()
        # # self.top.overrideredirect(True)
        # self._offsetx = 0
        # self._offsety = 0
        # self._window_x = int(screen_width/2 - win_width/2)
        # self._window_y = int(screen_height/2 - win_height/2)
        # self._window_w = self.top.winfo_width()
        # self._window_h = self.top.winfo_height()
        # # self.top.geometry('{w}x{h}+{x}+{y}'.format(w=self._window_w,h=self._window_h,x=self._window_x,y=self._window_y))
        # self.top.bind('<Button-1>',self.clickwin)
        # self.top.bind('<B1-Motion>',self.dragwin)

    # def dragwin(self,event):
    #     delta_x = self.top.winfo_pointerx() - self._offsetx
    #     delta_y = self.top.winfo_pointery() - self._offsety
    #     x = self._window_x + delta_x
    #     y = self._window_y + delta_y
    #     self.top.geometry("+{x}+{y}".format(x=x, y=y))
    #     self._offsetx = self.top.winfo_pointerx()
    #     self._offsety = self.top.winfo_pointery()
    #     self._window_x = x
    #     self._window_y = y

    # def clickwin(self,event):
    #     self._offsetx = self.top.winfo_pointerx()
    #     self._offsety = self.top.winfo_pointery()

    def press_enter_calculate_wrap_up_date(self, event):
        self.calculate_wrap_up_date()

    def press_enter_clear(self, event):
        self.clear()

    def clear(self, event=None):
        """Clear all entries."""
        self.dispense_date_entry.delete(0, END)
        self.day_supply_entry.delete(0, END)
        self.wrap_up_date.config(text='')
        self.dispense_date_entry.focus()

    def always_top(self):
        """Window always display on top."""
        if self.alwaysTopVar.get() == 1:
            self.top.attributes('-topmost', 1)
        elif self.alwaysTopVar.get() == 0:
            self.top.attributes('-topmost', 0)

    def calculate_wrap_up_date(self, event=None):
        """Calculate the next wrap up date."""
        # Separate month, day, and year into a list.
        try:
            entered_dispense_date = self.dispense_date_entry.get()
            if '/' in entered_dispense_date:
                dispense_date_split = entered_dispense_date.split('/')
            elif '-' in entered_dispense_date:
                dispense_date_split = entered_dispense_date.split('-')
            
            # Check if user entered 4 digits year. If not, format it to YYYY.
            if len(entered_dispense_date) <= 5:
                if len(dispense_date_split) == 3:
                    if len(dispense_date_split[2]) == 1: # if only 1 digit in the year
                        self.wrap_up_date.config(text='INVALID')
                        return
                else:
                    dispense_year = dt.datetime.now().year
            else:
                dispense_year = dispense_date_split[2]
                if len(dispense_year) == 2:
                    dispense_year = '20' + dispense_year

            dispense_month = int(dispense_date_split[0])
            dispense_day = int(dispense_date_split[1])
            dispense_year = int(dispense_year)

            day_supply = int(self.day_supply_entry.get())
            dispense_date = dt.datetime(month=dispense_month, day=dispense_day, year=dispense_year)

            v_state = self.v.get()
            if v_state == 1:
                days_before = 7
            elif v_state == 2:
                days_before = 9

            wrap_up_date = dispense_date + dt.timedelta(days=day_supply-days_before)
            # Avoid weekends
            if dt.datetime(wrap_up_date.year, wrap_up_date.month, wrap_up_date.day).weekday() == 5:
                wrap_up_date = dispense_date + dt.timedelta(days=day_supply-days_before-1)
            if dt.datetime(wrap_up_date.year, wrap_up_date.month, wrap_up_date.day).weekday() == 6:
                wrap_up_date = dispense_date + dt.timedelta(days=day_supply-days_before-2)

            # Make sure wrap up date is not in the past.

            if wrap_up_date < dt.datetime.today() and len(entered_dispense_date) < 10:
                self.wrap_up_date.config(text='INVALID')
                return

            formatted_wrap_up_date = wrap_up_date.strftime('%m/%d/%Y')
            self.wrap_up_date.config(text=f'{formatted_wrap_up_date}')
            pyperclip.copy(formatted_wrap_up_date)
        except:
            self.wrap_up_date.config(text='INVALID')
