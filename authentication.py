"""This module contains a class that represents an authenticator."""

import tkinter as tk
from tkinter import messagebox
import random
import json
import os

from myEncryption import EnDeCrypt


FONT = ('Bahnschrift Light', 12, 'normal')


class Authenticator:
    """This class provides verification for users to access various apps."""

    def __init__(self, function=''):
        """Initialize encryption, GUI, and check credentials."""
        self.endecrypt = EnDeCrypt()
        self.root = tk.Tk()
        self.root.title('Enter Pin')

        self.secretKey = ''
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
            # ask if user wants to overwrite existing file and create new credential.
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

    def _encrypt_token(self) -> str:
        """Encrypt and embed secret key inside token. Attach unencrypted shift number at the end of encrypted token."""
        encryptedKey = self.endecrypt.encrypt(message=self.secretKey, shiftNum=self.shiftNum)
        embeddedToken = self.token[:75] + encryptedKey + self.token[75:]
        encryptedKeyLen = len(encryptedKey)
        encryptedToken = str(encryptedKeyLen) + "::" + self.endecrypt.encrypt(message=embeddedToken, shiftNum=self.shiftNum) + "::" + self.shiftNum
        return encryptedToken

    def _export_token(self, token: str):
        """Separate encrypted token into two parts and write each part to data.json and auth.key."""
        tokenPiece1 = token[:int(len(token)/2)]
        tokenPiece2 = token[int(len(token)/2):]
        relPath1 = 'data'
        relPath2 = 'cred'
        mainPath = os.path.dirname(__file__)
        absolutePath1 = os.path.join(mainPath, relPath1)
        absolutePath2 = os.path.join(mainPath, relPath2)
        isExist1 = os.path.exists(absolutePath1)
        isExist2 = os.path.exists(absolutePath2)

        if not isExist1:
            os.mkdir(absolutePath1)

        if not isExist2:
            os.mkdir(absolutePath2)

        with open('data/data.json', 'w') as f:
            data = {'key': tokenPiece1}
            json.dump(data, f, indent=4)

        with open('cred/auth.key', 'w') as f:
            f.write(tokenPiece2)


    def _authenticate(self):
        """If credential exists, prompt user to enter secret key."""

        def _get_token():
            """Get token from data.json and auth.key"""
            with open('data/data.json', 'r') as f:
                data = json.load(f)
                tokenPiece1 = data['key']
            
            with open('cred/auth.key', 'r') as f:
                tokenPiece2 = f.read()
            
            token = tokenPiece1 + tokenPiece2
            return token

        def _decrypt_token():
            """Extract PIN and shfit number from encrypted token."""
            token = _get_token()
            splitToken = token.split('::')
            shiftNum = splitToken[-1]
            encryptedKeyLength = int(splitToken[0])
            decryptedToken = self.endecrypt.decrypt(encryptedMessage=token, shiftNum=shiftNum)
            encryptedPin = decryptedToken[75:76+encryptedKeyLength]
            decryptedPin = self.endecrypt.decrypt(encryptedMessage=encryptedPin, shiftNum=shiftNum)


        authWin = tk.Toplevel(self.root)
        authWin.title('Verification')
        instructLabel = tk.Label(authWin, text='Enter your PIN or secret phrase.')
        instructLabel.grid(column=0, row=0)
        enterKeyLabel = tk.Label(authWin, text='PIN/Phrase: ')
        enterKeyLabel.grid(column=0, row=2)
        keyEntry = tk.Entry(authWin)
        keyEntry.grid(column=1, row=2)
        okButton = tk.Button(authWin, text='OK')
        okButton.grid(column=1, row=3)
        _decrypt_token()


    def _create_secretkey(self):
        """Prompt user to create a secret key."""

        def _verifySecretKey():
            """Verify if user re-enters secret key correctly."""
            key1 = keyEntry.get()
            key2 = verifyKeyEntry.get()
            if key1 == key2:
                self.secretKey = key1
                messagebox.showinfo(title='Success', message='Your secret key has been'
                                    ' created. Don\'t lose it!')
                encryptedToken = self._encrypt_token()
                self._export_token(token=encryptedToken)
                createKeyWin.destroy()
            else:
                messagebox.showerror(title='Error', message='Your secret key did not'
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
        enterKeyLabel = tk.Label(
            createKeyWin, text='Enter PIN/Phrase: ', font=FONT)
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

    def _generate_token(self, size=150):
        """Generate a random token of default size 100."""
        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&\'()*+,-./:;<=>?@"[]^_`{|}~'
        token = ''
        for _ in range(size):
            randChar = random.choice(characters)
            token += randChar

        self.token = token


if __name__ == '__main__':
    a = Authenticator()