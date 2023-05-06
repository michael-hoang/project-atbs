import tkinter as tk
import ttkbootstrap as tkb

from ttkbootstrap.constants import *


class Reprint(tkb.Frame):
    """
    Interface to reprint filled card payment forms.
    """

    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.create_treeview(master)
        self.create_solid_button(master, 'Print', None)

    def create_treeview(self, master):
        """Create ttkbootstrap Treeview object."""

        # Tree container (Treeview + Scrollbar)
        tree_container = tkb.Frame(master)
        tree_container.pack(padx=20, pady=20)

        # Scrollbar
        tree_scroll = tkb.Scrollbar(
            master=tree_container,
            bootstyle=''
        )
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Define columns
        columns = ('#', 'reference', 'date_created', 'expiration')

        # Create Treeview
        my_tree = tkb.Treeview(
            master=tree_container,
            bootstyle='',
            columns=columns,
            show='headings',
            yscrollcommand=tree_scroll.set,
            selectmode='browse',
            height=10
        )
        my_tree.pack()

        # Configure scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Format columns
        my_tree.column('#', anchor=CENTER, width=50)
        my_tree.column('reference', anchor=W, width=100)
        my_tree.column('date_created', anchor=W, width=120)
        my_tree.column('expiration', anchor=W, width=100)

        # Headings
        my_tree.heading('#', text='#', anchor=CENTER)
        my_tree.heading('reference', text='Reference', anchor=W)
        my_tree.heading('date_created', text='Date Created', anchor=W)
        my_tree.heading('expiration', text='Expiration', anchor=W)

        # Add Data
        index = 1
        iid = 0
        for _ in range(100):
            my_tree.insert(
                parent='',
                index=END,
                iid=iid,
                text='Parent',
                values=(f'{index}', 'Mike_123456', '5/4/2023 9:57 AM', '6d 22h 34m')
            )
            index += 1
            iid += 1

    def create_solid_button(self, master, text, command) -> tkb.Button:
        """Create ttkbootstrap Solid Button object."""
        button = tkb.Button(
            master=master,
            text=text,
            command=command,
            width=8
        )
        button.pack(pady=(0, 20))

        return button


if __name__ == '__main__':
    reprint_window = tkb.Window(
        title='Reprint',
        themename='superhero',
    )
    rp = Reprint(master=reprint_window)

    reprint_window.mainloop()
