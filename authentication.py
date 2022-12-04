"""This module contains a class that represents an authenticator."""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import json
import os
from myEncryption import EnDeCrypt


FONT = ('Bahnschrift Light', 12, 'normal')
BG_COLOR = '#30323D'
GOLD_COLOR = '#E9D985'
BUTTON_COLOR = '#4D5061'
LIGHT_GRAY = '#999999'


class Authenticator:
    """This class provides verification for users to access various apps."""

    def __init__(self):
        """Initialize encryption, GUI, and check credentials."""
        self.endecrypt = EnDeCrypt()
        self.top = tk.Toplevel()
        self.top.title('Verification')
        self.top.withdraw()

        self.instructLabel = tk.Label(
            self.top, text='Enter your PIN or secret phrase.')
        self.instructLabel.grid(column=0, row=0)
        self.enterKeyLabel = tk.Label(self.top, text='PIN/Phrase: ')
        self.enterKeyLabel.grid(column=0, row=2)
        self.keyEntry = tk.Entry(self.top)
        self.keyEntry.grid(column=1, row=2)
        self.okButton = tk.Button(
            self.top, text='OK', command=self.confirmation)
        self.okButton.grid(column=1, row=3)

        self.secretKey = ''
        self.shiftNum = ''
        self.token = ''
        self.isVerified = False
        self.cred = ''
        self._authenticate()

    def _authenticate(self):
        """Start authentication or prompt user to create secret key."""
        self.cred = self._check_for_existing_credential()
        if self.cred:
            self.top.deiconify()
        else:
            self._generate_token()
            self.shiftNum = str(random.choice(range(85)))
            self._create_secretkey()

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

    def _generate_token(self, size=150):
        """Generate a random token of default size 100."""
        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&\'()*+,-./:;<=>?@"[]^_`{|}~'
        token = ''
        for _ in range(size):
            randChar = random.choice(characters)
            token += randChar

        self.token = token

    def _create_secretkey(self):
        """Prompt user to create a secret key."""

        def _verifySecretKey(event):
            """Verify if user re-enters secret key correctly."""
            key1 = keyEntry.get()
            key2 = verifyKeyEntry.get()
            if key1 == key2:
                self.secretKey = key1
                messagebox.showinfo(title='Success', message='Your secret key has been'
                                    ' created. Don\'t lose it!')
                encryptedToken = self._encrypt_token()
                self._export_token(token=encryptedToken)
                self._authenticate()
                createKeyWin.destroy()
            else:
                messagebox.showerror(title='Error', message='Your secret key did not'
                                     ' match. Please try again.')
                verifyKeyEntry.focus()

        def showSecretKey(event):
            """Reveal PIN/Phrase to user."""
            keyEntry.config(show='')
            verifyKeyEntry.config(show='')

        def hideSecretKey(event):
            """Hide PIN/Phrase from user."""
            keyEntry.config(show='*')
            verifyKeyEntry.config(show='*')

        warning_message = 'Create a PIN or phrase.\n\nWARNING: This will be'\
            ' your secret key. Keep it safe. You will not be able'\
            ' to recover your saved accounts and passwords if you lose'\
            ' it.'
        createKeyWin = tk.Toplevel(self.top, padx=20, pady=20, bg=BG_COLOR)
        createKeyWin.title('Create PIN/Phrase')
        createKeyWin.withdraw()
        # Pin/Phrase creation window jumps to the front.
        createKeyWin.lift()
        createKeyWin.attributes('-topmost', True)
        createKeyWin.attributes('-topmost', False)
        warningLabel = tk.Label(
            createKeyWin, text=warning_message, justify='left', font=FONT, wraplength=400, bg=BG_COLOR, fg='white')
        warningLabel.grid(column=0, row=0, columnspan=2,
                          sticky='EW', padx=10, pady=(0, 10))
        enterKeyLabel = tk.Label(
            createKeyWin, text='Enter PIN/Phrase: ', font=FONT, bg=BG_COLOR, fg='white')
        enterKeyLabel.grid(column=0, row=1, sticky='E', pady=(10))
        keyEntry = tk.Entry(createKeyWin, font=FONT, show='*')
        keyEntry.focus()
        keyEntry.grid(column=1, row=1, pady=(10, 5))
        verifyKeyLabel = tk.Label(
            createKeyWin, text='Re-Enter PIN/Phrase: ', font=FONT, bg=BG_COLOR, fg='white')
        verifyKeyLabel.grid(column=0, row=2, sticky='E')
        verifyKeyEntry = tk.Entry(createKeyWin, font=FONT, show='*')
        verifyKeyEntry.grid(column=1, row=2, pady=(0, 10))
        okButton = tk.Button(createKeyWin, text='OK',
                             font=FONT, width=10, bg=BUTTON_COLOR, fg='white', borderwidth=0, activebackground=GOLD_COLOR, command=lambda: _verifySecretKey('event'))
        okButton.grid(column=1, row=3, pady=(10, 0))
        # Eye button
        createKeyWin.eyeImage_open = Image.open('img/eye.png')
        createKeyWin.eyeImage_resized = createKeyWin.eyeImage_open.resize(
            (25, 25))
        createKeyWin.eyeImage = ImageTk.PhotoImage(
            createKeyWin.eyeImage_resized)
        eyeButton = tk.Button(createKeyWin, image=createKeyWin.eyeImage,
                               bg=BG_COLOR, activebackground=BG_COLOR, borderwidth=0)
        eyeButton.grid(column=2, row=1, rowspan=2)
        eyeButton.bind('<ButtonPress-1>', showSecretKey)
        eyeButton.bind('<ButtonRelease-1>', hideSecretKey)

        createKeyWin.bind('<Return>', _verifySecretKey)
        createKeyWin.protocol('WM_DELETE_WINDOW', self.top.destroy)
        # Center window to screen
        createKeyWin.update_idletasks()
        win_width = createKeyWin.winfo_reqwidth()
        win_height = createKeyWin.winfo_reqheight()
        screen_width = createKeyWin.winfo_screenwidth()
        screen_height = createKeyWin.winfo_screenheight()
        x = int(screen_width/2 - win_width/2)
        y = int(screen_height/2 - win_width/2)
        createKeyWin.geometry(f"{win_width}x{win_height}+{x}+{y}")
        createKeyWin.deiconify()

    def _encrypt_token(self) -> str:
        """Encrypt and embed secret key inside token. Attach unencrypted shift number at the end of encrypted token."""
        encryptedKey = self.endecrypt.encrypt(
            message=self.secretKey, shiftNum=self.shiftNum)
        embeddedToken = self.token[:75] + encryptedKey + self.token[75:]
        encryptedKeyLen = len(encryptedKey)
        encryptedToken = str(encryptedKeyLen) + "::" + self.endecrypt.encrypt(
            message=embeddedToken, shiftNum=self.shiftNum) + "::" + self.shiftNum
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

    def confirmation(self):
        """Confirm if user can access Password Manager through authentication."""
        decryptedKey = self._decrypt_token()
        self._verify_entered_key(stored_key=decryptedKey)

    def _decrypt_token(self) -> str:
        """Decrypt token to get secret key."""
        token = self._get_token()
        splitToken = token.split('::')
        shiftNum = splitToken[-1]
        encryptedKeyLength = int(splitToken[0])
        bareToken = splitToken[1]
        decryptedToken = self.endecrypt.decrypt(
            encryptedMessage=bareToken, shiftNum=shiftNum)
        encryptedKey = decryptedToken[75:76+encryptedKeyLength]
        decryptedKey = self.endecrypt.decrypt(
            encryptedMessage=encryptedKey, shiftNum=shiftNum)
        return decryptedKey

    def _get_token(self) -> str:
        """Get token from data.json and auth.key"""
        with open('data/data.json', 'r') as f:
            data = json.load(f)
            tokenPiece1 = data['key']

        with open('cred/auth.key', 'r') as f:
            tokenPiece2 = f.read()

        token = tokenPiece1 + tokenPiece2
        return token

    def _verify_entered_key(self, stored_key) -> bool:
        """If entered key matches the stored key inside the token, open Password Manager."""
        entered_key = self.keyEntry.get()
        if entered_key == stored_key:
            self.isVerified = True
            print(self.isVerified)

        else:
            messagebox.showerror(
                title='Error', message='Invalid PIN or phrase.')
            print(stored_key)


if __name__ == '__main__':
    root = tk.Tk()
    a = Authenticator()

    root.mainloop()
