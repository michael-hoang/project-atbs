import tkinter as tk
from PIL import Image, ImageTk
from wrapup import WrapUpDateCalculator
from cardpayment import CardPayment
from map import Map
from pwmanager import PasswordManager
from authentication import Authenticator
from dist.update import Updater


FONT = ('Bahnschrift Light', 17, 'normal')
BG_COLOR = '#30323D'
FG_COLOR = 'white'
HOVER_BUTTON_COLOR = 'SlateGray4'
ACTIVE_BG_COLOR = 'SlateGray2'


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.title('Project AtBS')
        self.config(bg=BG_COLOR)
        self.resizable(width=False, height=False)
        self.iconphoto(False, tk.PhotoImage(file='assets/img/atbs_icon.png'))

        self.button_images = []
        # Create buttons
        self.cp_but = self.create_button(
            'Payment', 'cc_icon.png', self.open_CardPaymentForm)
        self.wud_but = self.create_button(
            'Wrap Up', 'cal_calc.png', self.open_WrapUpDateCalculator)
        self.m_but = self.create_button(
            'Map', 'map_icon.png', self.open_MapSearch)
        self.pm_but = self.create_button(
            'Password', 'lock_icon.png', self.open_PasswordManager)

        # Place buttons on grid
        self.cp_but.grid(column=0, row=0, sticky='EW')
        self.wud_but.grid(column=0, row=1, sticky='EW')
        self.m_but.grid(column=0, row=2, sticky='EW')
        self.pm_but.grid(column=0, row=3, sticky='EW')

        # Bind events
        self.bind('<Enter>', self.pointerEnter)
        self.bind('<Leave>', self.pointerLeave)

        # Center window to screen
        self.update_idletasks()
        win_width = self.winfo_reqwidth()
        win_height = self.winfo_reqheight()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int(screen_width/2 - win_width/2)
        y = int(screen_height/2 - win_width/2)
        self.geometry(f"{win_width}x{win_height}+{x}+{y}")
        self.deiconify()

    def create_button(self, text, image_path, command):
        img_open = Image.open(fp=f'assets/img/{image_path}')
        img_resized = img_open.resize(size=(50, 50))
        self.img = ImageTk.PhotoImage(img_resized)
        self.button_images.append(self.img)
        button = tk.Button(text=f'  {text}', image=self.img, compound='left', font=FONT, fg=FG_COLOR,
                           bg=BG_COLOR, activebackground=ACTIVE_BG_COLOR, command=command,
                           anchor='w', padx=10, pady=5, width=207)
        return button

    def open_WrapUpDateCalculator(self):
        """Instantiate WrapUpDateCalculator object in a new TopLevel window."""
        top = WrapUpDateCalculator()

    def open_CardPaymentForm(self):
        """Instantiate CardPayment object in a new TopLevel window."""
        top = CardPayment()

    def open_MapSearch(self):
        """Instantiate Map object in a new TopLevel window."""
        top = Map()

    def open_PasswordManager(self):
        """Instantiate Password Manager in a new TopLevel window."""
        a = Authenticator()
        self._check_isVerified_flag(a)

    def _check_isVerified_flag(self, authenticator):
        """Recursively checks isVerified flag to signal instantiation of Password Manager object."""
        if not authenticator.isVerified:
            self.after(50, self._check_isVerified_flag, authenticator)
        else:
            authenticator.top.destroy()
            pm = PasswordManager()

    def check_for_updates():
        """Check if new version of Main App or App Update Manager is available."""

        #

    def open_Updater():
        """Run App Update Manager"""

        #

    def pointerEnter(self, event):
        """Change button color on mouse hover."""
        event.widget['bg'] = HOVER_BUTTON_COLOR

    def pointerLeave(self, event):
        """Change button color back to normal when mouse leave button."""
        event.widget['bg'] = BG_COLOR


if __name__ == '__main__':
    MainApp().mainloop()
