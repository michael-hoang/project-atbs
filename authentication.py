"""This module contains a class that represents an authenticator."""

import tkinter as tk
import random

from myEncryption import EnDeCrypt


FONT = ('Bahnschrift Light', 14, 'normal')


class Authenticator:
    """This class provides verification for users to access various apps."""

    def __init__(self, function=''):
        """Initialize encryption, GUI, and check credentials."""
        self.endecrypt = EnDeCrypt()
        self.root = tk.Tk()
        self.root.title('Enter Pin')

        self.pin = ''
        self.token = ''
        self.cred = self._check_for_existing_credential()
        self._create_pin()

        self.root.mainloop()

    def _check_for_existing_credential(self) -> bool:
        """Check for existing crendential (data.json and auth.key)."""
        try:
            with open('cred/auth.key', 'r') as f:
                cred1 = f.read()
        except FileNotFoundError:
            cred1 = False

        try:
            with open('data/data.json', 'r') as f:
                cred2 = f.read()
        except FileNotFoundError:
            cred2 = False

        if cred1 and cred2:
            return True
        elif cred1 and not cred2:
            print("'cred/auth.key' verified.\n'data/data.json' missing.")
            return
        elif not cred1 and cred2:
            print("'cred/auth.key' missing.\n'data/data.json' verified.")
            return
        else:
            print("'cred/auth.key' missing.\n'data/data.json' missing.")
            return False

    def _start(self):
        """Start authentication or prompt user to create pin."""
        if self.cred:
            self._authenticate()
        else:
            self._create_pin()
            self._generate_token()

    def _authenticate(self):
        """If credential exists, prompt user to enter pin."""

    def _create_pin(self):
        """Prompt user to create pin."""
        warning_message = 'Create a 4-digit PIN.\n\nWARNING: Keep your PIN safe.\n'\
            'Your stored accounts and passwords\ncannot be recovered if PIN  is lost.'
        createPinWin = tk.Toplevel(self.root)
        createPinWin.title('Create PIN')
        warningLabel = tk.Label(
            createPinWin, text=warning_message, justify='left', font=FONT)
        warningLabel.grid(column=0, row=0, columnspan=2, sticky='EW')
        enterPinLabel = tk.Label(createPinWin, text='Enter PIN: ', font=FONT)
        enterPinLabel.grid(column=0, row=1, sticky='E')
        pinEntry = tk.Entry(createPinWin, font=FONT)
        pinEntry.grid(column=1, row=1)
        verifyPinLabel = tk.Label(createPinWin, text='Re-Enter PIN: ', font=FONT)
        verifyPinLabel.grid(column=0, row=2, sticky='E')
        verifyPinEntry = tk.Entry(createPinWin, font=FONT)
        verifyPinEntry.grid(column=1, row=2)
        okButton = tk.Button(createPinWin, text='OK')
        okButton.grid(column=1, row=3)

    def _generate_token(self, size=100):
        """Generate a random token of default size 100."""
        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&\'()*+,-./:;<=>?@"[]^_`{|}~'
        token = ''
        for _ in range(size):
            randChar = random.choice(characters)
            token += randChar

        self.token = token


if __name__ == '__main__':
    a = Authenticator()
    a._generate_token()
    # print(a.cred)
    # print(a.token)
