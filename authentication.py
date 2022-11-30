"""This module contains a class that represents an authenticator."""

import tkinter as tk
from tkinter import messagebox
import random

from myEncryption import EnDeCrypt


FONT = ('Bahnschrift Light', 12, 'normal')


class Authenticator:
    """This class provides verification for users to access various apps."""

    def __init__(self, function=''):
        """Initialize encryption, GUI, and check credentials."""
        self.endecrypt = EnDeCrypt()
        self.root = tk.Tk()
        self.root.title('Enter Pin')

        self.pin = ''
        self.shiftNum = ''
        self.token = ''
        self.cred = self._check_for_existing_credential()
        self._start()

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
        """Start authentication or prompt user to create secret key."""
        if self.cred:
            self._authenticate()
        else:
            self._generate_token()
            self.shiftNum = str(random.choice(range(85)))
            self._create_secretkey()

    def _export_token(self):
        """
        Encrypt secret key and shift number, and embed inside token. Export
        to file data.json and auth.key
        """
        if self.pin:
            encryptedPin = self.endecrypt.encrypt(self.pin)
            encryptedShiftNum = self.endecrypt.encrypt(self.shiftNum)
            embeddedToken = self.token[:24] + encryptedPin + self.token[24:49] + encryptedShiftNum + self.token[49:]

            print(encryptedPin)
            print(encryptedShiftNum)
            print(embeddedToken)
            print(self.token)


    def _authenticate(self):
        """If credential exists, prompt user to enter pin."""

    def _create_secretkey(self):
        """Prompt user to create a secret key."""

        def _verifySecretKey():
            """Verify if user re-enters secret key correctly."""
            pin1 = keyEntry.get()
            pin2 = verifyKeyEntry.get()
            if pin1 == pin2:
                self.pin = pin1
                messagebox.showinfo(title='Success', message='Your PIN has been'
                                    ' created. Don\'t lose it!')
                self._export_token()
                createKeyWin.destroy()
            else:
                messagebox.showerror(title='Error', message='Your PIN did not'
                                     ' match. Please try again.')

        warning_message = 'Create a secret PIN or phrase.\n\nWARNING: This will be'\
        ' your secret key.\nKeep it safe. You will not be able'\
        ' to recover\nyour saved accounts and passwords if you lose'\
        ' it.'
        createKeyWin = tk.Toplevel(self.root)
        createKeyWin.title('Create PIN/Phrase')
        warningLabel = tk.Label(
            createKeyWin, text=warning_message, justify='left', font=FONT)
        warningLabel.grid(column=0, row=0, columnspan=2, sticky='EW')
        enterKeyLabel = tk.Label(createKeyWin, text='Enter PIN/Phrase: ', font=FONT)
        enterKeyLabel.grid(column=0, row=1, sticky='E')
        keyEntry = tk.Entry(createKeyWin, font=FONT)
        keyEntry.grid(column=1, row=1)
        verifyKeyLabel = tk.Label(
            createKeyWin, text='Re-Enter PIN/Phrase: ', font=FONT)
        verifyKeyLabel.grid(column=0, row=2, sticky='E')
        verifyKeyEntry = tk.Entry(createKeyWin, font=FONT)
        verifyKeyEntry.grid(column=1, row=2)
        okButton = tk.Button(createKeyWin, text='OK', command=_verifySecretKey)
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
 