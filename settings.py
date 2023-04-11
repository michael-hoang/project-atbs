from pathlib import Path
from tkinter import PhotoImage
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox


PATH = Path(__file__).parent / 'assets'


class Settings(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES)

        self.images = [
            PhotoImage(
                name='reset', 
                file=PATH / 'icons8_reset_24px.png'),
            PhotoImage(
                name='reset-small', 
                file=PATH / 'icons8_reset_16px.png'),
            PhotoImage(
                name='submit', 
                file=PATH / 'icons8_submit_progress_24px.png'),
            PhotoImage(
                name='question', 
                file=PATH / 'icons8_question_mark_16px.png'),
            PhotoImage(
                name='direction', 
                file=PATH / 'icons8_move_16px.png'),
            PhotoImage(
                name='bluetooth', 
                file=PATH / 'icons8_bluetooth_2_16px.png'),
            PhotoImage(
                name='buy', 
                file=PATH / 'icons8_buy_26px_2.png'),
            PhotoImage(
                name='mouse', 
                file=PATH / 'magic_mouse.png')
        ]

        for i in range(3):
            self.columnconfigure(i, weight=1)
        self.rowconfigure(0, weight=1)

        # column 1
        col1 = ttk.Frame(self, padding=10)
        col1.grid(row=0, column=0, sticky=NSEW)

        # device info
        dev_info = ttk.Labelframe(col1, text='Device Info', padding=10)
        dev_info.pack(side=TOP, fill=BOTH, expand=YES)

        # header
        dev_info_header = ttk.Frame(dev_info, padding=5)
        dev_info_header.pack(fill=X)

        btn = ttk.Button(
            master=dev_info_header,
            image='reset',
            bootstyle=LINK,
            command=self.callback
        )
        btn.pack(side=LEFT)

        lbl = ttk.Label(dev_info_header, text='Model 2009, 2xAA Batteries')
        lbl.pack(side=LEFT, fill=X, padx=15)

        btn = ttk.Button(
            master=dev_info_header,
            image='submit',
            bootstyle=LINK,
            command=self.callback
        )
        btn.pack(side=LEFT)

        # image
        ttk.Label(dev_info, image='mouse').pack(fill=X)

        # progress message
        self.setvar('progress', 'Battery is discharging.')
        lbl = ttk.Label(
            master=dev_info,
            textvariable='progress',
            font='Helvetica 8',
            anchor=CENTER
        )
        lbl.pack(fill=X)

        # licence info
        lic_info = ttk.Labelframe(col1, text='License Info', padding=20)
        lic_info.pack(side=TOP, fill=BOTH, expand=YES, pady=(10, 0))
        lic_info.rowconfigure(0, weight=1)
        lic_info.columnconfigure(0, weight=2)

        lic_title = ttk.Label(
            master=lic_info,
            text='Trial Version, 28 days left',
            anchor=CENTER
        )
        lic_title.pack(fill=X, pady=(0, 20))

        lbl = ttk.Label(
            master=lic_info,
            text='Mouse serial number:',
            anchor=CENTER,
            font='Helvetica 8'
        )
        lbl.pack(fill=X)
        self.setvar('license', 'dtMM2-XYZGHIJKLMN3')

        lic_num = ttk.Label(
            master=lic_info,
            textvariable='license',
            bootstyle=PRIMARY,
            anchor=CENTER
        )
        lic_num.pack(fill=X, pady=(0, 20))

        buy_now = ttk.Button(
            master=lic_info,
            image='buy',
            text='Buy now',
            compound=BOTTOM,
            command=self.callback
        )
        buy_now.pack(padx=10, fill=X)

        # Column 2
        col2 = ttk.Frame(self, padding=10)
        col2.grid(row=0, column=1, sticky=NSEW)

        # scrolling
        scrolling = ttk.Labelframe(col2, text='Scrolling', padding=(15, 10))
        scrolling.pack(side=TOP, fill=BOTH, expand=YES)

        op1 = ttk.Checkbutton(scrolling, text='Scrolling', variable='op1')
        op1.pack(fill=X, pady=5)

        # no horizontal scrolling
        op2 = ttk.Checkbutton(
            master=scrolling,
            text='No horizontal scrolling',
            variable='op2'
        )
        op2.pack(fill=X, padx=(20, 0), pady=5)

        btn = ttk.Button(
            master=op2,
            image='question',
            bootstyle=LINK,
            command=self.callback
        )
        btn.pack(side=RIGHT)

        # inverse
        op3 = ttk.Checkbutton(
            master=scrolling,
            text='Inverse scroll directcion vertically',
            variable='op3'
        )
        op3.pack(fill=X, padx=(20, 0), pady=5)

        btn = ttk.Button(
            master=op3,
            image='direction',
            bootstyle=LINK,
            command=self.callback
        )
        btn.pack(side=RIGHT)

        # Scroll only vertical or horizontal
        op4 = ttk.Checkbutton(
            master=scrolling,
            text='Scroll only vertical or horizontal',
            state=DISABLED
        )
        op4.configure(variable='op4')
        op4.pack(fill=X, padx=(20, 0), pady=5)

        # smooth scrolling
        op5 = ttk.Checkbutton(
            master=scrolling,
            text='Smooth scrolling',
            variable='op5'
        )
        op5.pack(fill=X, padx=(20, 0), pady=5)

        btn = ttk.Button(
            master=op5,
            image='bluetooth',
            bootstyle=LINK,
            command=self.callback
        )
        btn.pack(side=RIGHT)

        # scroll speed
        scroll_speed_frame = ttk.Frame(scrolling)
        scroll_speed_frame.pack(fill=X, padx=(20, 0), pady=5)

        lbl = ttk.Label(scroll_speed_frame, text='Speed:')
        lbl.pack(side=LEFT)

        scale = ttk.Scale(scroll_speed_frame, value=35, from_=1, to=100)
        scale.pack(side=LEFT, fill=X, expand=YES, padx=5)

        scroll_speed_btn = ttk.Button(
            master=scroll_speed_frame,
            image='reset-small',
            bootstyle=LINK,
            command=self.callback
        )
        scroll_speed_btn.pack(side=LEFT)

        # scroll sense
        scroll_sense_frame = ttk.Frame(scrolling)
        scroll_sense_frame.pack(fill=X, padx=(20, 0), pady=(5, 0))

        ttk.Label(scroll_sense_frame, text='Sense:').pack(side=LEFT)

        scale = ttk.Scale(scroll_sense_frame, value=50, from_=1, to=100)
        scale.pack(side=LEFT, fill=X, expand=YES, padx=5)

        scroll_sense_btn = ttk.Button(
            master=scroll_sense_frame,
            image='reset-small',
            bootstyle=LINK,
            command=self.callback
        )
        scroll_sense_btn.pack(side=LEFT)

        # 1 finger gestures
        finger_gest = ttk.Labelframe(
            master=col2,
            text='1 Finger Gestures',
            padding=(15, 10)
        )
        finger_gest.pack(
            side=TOP,
            fill=BOTH,
            expand=YES,
            pady=(10, 0)
        )
        op6 = ttk.Checkbutton(
            master=finger_gest,
            text='Fast swipe left/right',
            variable='op6'
        )
        op6.pack(fill=X, pady=5)

        cb = ttk.Checkbutton(
            master=finger_gest,
            text='Swap swipe direction',
            variable='op7'
        )
        cb.pack(fill=X, padx=(20, 0), pady=5)

        # gest sense
        gest_sense_frame = ttk.Frame(finger_gest)
        gest_sense_frame.pack(fill=X, padx=(20, 0), pady=(5, 0))

        ttk.Label(gest_sense_frame, text='Sense:').pack(side=LEFT)

        scale = ttk.Scale(gest_sense_frame, value=50, from_=1, to=100)
        scale.pack(side=LEFT, fill=X, expand=YES, padx=5)

        btn = ttk.Button(
            master=gest_sense_frame,
            image='reset-small',
            bootstyle=LINK,
            command=self.callback
        )
        btn.pack(side=LEFT)

        # middle click
        middle_click = ttk.Labelframe(
            master=col2,
            text='Middle Click',
            padding=(15, 10)
        )
        middle_click.pack(
            side=TOP,
            fill=BOTH,
            expand=YES,
            pady=(10, 0)
        )
        cbo = ttk.Combobox(
            master=middle_click,
            values=['Any 2 finger', 'Other 1', 'Other 2']
        )
        cbo.current(0)
        cbo.pack(fill=X)

    def callback(self):
        """Demo callback"""
        Messagebox.ok(
            title='Button callback', 
            message="You pressed a button."
        )


if __name__ == '__main__':

    app = ttk.Window("Magic Mouse", "yeti")
    Settings(app)
    app.mainloop()
