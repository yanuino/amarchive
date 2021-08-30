import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

import os

from pystray import Icon as icon, MenuItem as item, Menu as menu
from PIL import Image

import pyperclip

import serial.tools.list_ports


class EnumCom_program():
    def __init__(self):
        #self.window = tk.Tk()
        #self.window = ThemedTk(theme="arc")
        self.window = ThemedTk(theme="black")
        self.window.resizable(False, False)
        #self.window = ThemedTk(theme="equilux")
        self.path = str(os.path.dirname(__file__))
        self.window.title("Com Ports")
        self.window.protocol('WM_DELETE_WINDOW', lambda: self.withdraw_window(self.window))
        self.listportsname = tk.StringVar()
        self.textportsdesc = tk.StringVar()
        self.textclipboard = tk.StringVar()
        self.hide = tk.IntVar(value=1)

        self.myimage = Image.open(os.path.join(self.path, 'EnumCom.png'))
        self.mymenu = menu(item('Quit', self.quit_window), item('Show', self.show_window, default=True))


        self.create_widgets()
        self.monitor(value=0)
        self.withdraw_window(self.window)

    def monitor(self, value):
        newvalue = len([port.device for port in serial.tools.list_ports.comports()])
        if newvalue != value:
            print(newvalue)
            self.comports(clear=False)
        self.window.after( 100, lambda value=newvalue: self.monitor(value))    

    def quit_window(self, icon, item):
        icon.stop()
        self.window.destroy()

    def show_window(self, icon, item):
        icon.stop()
        self.comports()
        self.window.after(0, self.window.deiconify)

    def withdraw_window(self, window):
        hide = self.hide.get()
        if hide:
            window.withdraw()
            self.myicon = icon('EnumCom', self.myimage, 'EnumCom', self.mymenu)
            self.myicon.run()
        else:
            window.destroy()

    def comports(self, clear = True):
        portsdevice = [port.device for port in serial.tools.list_ports.comports()]
        self.listportsname.set(portsdevice)
        if clear :
            self.my_listbox.selection_clear(0, tk.END)
            self.textportsdesc.set('')
    
    def my_listbox_copy(self, *args):
        idx = self.my_listbox.curselection()
        device = self.my_listbox.get(idx)
        pyperclip.copy(device)
        self.textclipboard.set(device)
        portsdesc = [port for port in serial.tools.list_ports.grep(device)]
        self.textportsdesc.set(portsdesc)

    def create_widgets(self):
        # Create some room around all the internal frames
        #self.window['padx'] = 5
        #self.window['pady'] = 5

        # - - - - - - - - - - - - - - - - - - - - -
        # The Choosing from lists frame
        main_frame = ttk.Frame(self.window, relief=tk.FLAT)
        main_frame.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S, padx=0)

        self.my_listbox = tk.Listbox(main_frame, height=8, width=15, activestyle='none', listvariable=self.listportsname, relief=tk.FLAT)
        self.my_listbox.bind('<<ListboxSelect>>', self.my_listbox_copy)
        self.my_listbox.grid(row=0, column=0, rowspan=3, padx=6, pady=6)

        info_frame = ttk.LabelFrame(main_frame, text="Info:", relief=tk.FLAT)
        info_frame.grid(row=0, column=1, padx=6, pady=6)

        info_text = ttk.Label(info_frame, width=50, textvariable=self.textportsdesc)
        info_text.grid(row=0, column=0)

        copy_frame = ttk.LabelFrame(main_frame, text="Clipboard:", relief=tk.FLAT)
        copy_frame.grid(row=1, column=1, padx=6, pady=6)

        copy_text = ttk.Label(copy_frame, width=50, textvariable=self.textclipboard)
        copy_text.grid(row=1, column=0)

        hide_check = ttk.Checkbutton(main_frame, text="Systray", variable=self.hide)
        hide_check.grid(row=2, column=1, sticky=tk.E, padx=6, pady=6)


        
# Create the entire GUI program
program = EnumCom_program()

# Start the GUI event loop
program.window.mainloop()
