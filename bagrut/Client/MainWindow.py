import tkinter as tk
from tkinter import font as tkFont

import socket
import sys


def check_connection(master, *a, **kwa):
    try:
        sck = socket.socket()
        sck.connect(master.address)
        sck.settimeout(10)
        sck.send(b'connectst')

        data = sck.recv(6)

        if data != b'alive':
            raise Exception('NOT A GAME SERVER!')
        
        return True
    except Exception as e:
        print(e, file=sys.stderr)
        return False
        

def site_msg(title, msg):
    """Change to grid"""
    popup = tk.Tk()
    popup.wm_title(title)
    popup.configure(background="white")
    popup['bg'] = "#170B3B"
    label = tk.Label(popup, text=msg, font=tkFont.Font(family='Arial', size=40), foreground="#aaa", background='#000')
    label.pack(side="top", fill="x", pady=10, padx=20)

    b1 = tk.Button(popup, text="OK", command=popup.destroy)
    b1.pack(pady=5)


def alert(title, msg, action):
    popup = tk.Tk()
    popup.wm_title(title)
    popup.configure(background="white")
    popup['bg'] = "#170B3B"
    label = tk.Label(popup, text=msg, font=tkFont.Font(family='Arial', size=40), foreground="#aaa", background='#000')
    label.pack(side="top", fill="x", pady=10, padx=20)

    b1 = tk.Button(popup, text="OK", command=[action(), popup.destroy()])
    b1.pack(pady=5)

    popup.mainloop()


class SelectMode(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def command_sp():
            self.master.master.mode = 'SP'
            self.master.master.destroy()

        def command_mp():
            self.master.master.mode = 'MP'
            self.master.master.show_frame('ServerDetails')

        btn_sp = tk.Button(self)
        btn_sp["bg"] = "#efefef"
        btn_sp["font"] = tkFont.Font(family='Arial', size=14)
        btn_sp["fg"] = "#000000"
        btn_sp["justify"] = "center"
        btn_sp["text"] = "Play in single-player mode"
        btn_sp.place(x=50,y=170,width=240,height=90)
        btn_sp['command'] = command_sp

        btn_mp = tk.Button(self)
        btn_mp["bg"] = "#efefef"
        btn_mp["font"] = tkFont.Font(family='Arial', size=14)
        btn_mp["fg"] = "#000000"
        btn_mp["justify"] = "center"
        btn_mp["text"] = "Play in multi-player mode"
        btn_mp.place(x=310,y=170,width=240,height=90)
        btn_mp['command'] = command_mp


class ServerDetails(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def on_login(*args, **kwargs):
            self.master.master.address = (entry_host.get(), int(entry_port.get()))

            result = check_connection(self.master.master)
            if result:
                site_msg('Success', 'Successfully communicated with server!')
                self.master.master.destroy()
            else:
                site_msg('Error', 'Failed to communicate with server!')

        label_host = tk.Label(self)
        label_host["font"] = tkFont.Font(family='Arial',size=18)
        label_host["fg"] = "#333333"
        label_host["justify"] = "right"
        label_host["text"] = "HOST:"
        label_host.place(x=50,y=100,width=145,height=60)

        label_port = tk.Label(self)
        label_port["font"] = tkFont.Font(family='Arial',size=18)
        label_port["fg"] = "#333333"
        label_port["justify"] = "right"
        label_port["text"] = "PORT:"
        label_port.place(x=50,y=175,width=145,height=60)

        entry_host = tk.Entry(self)
        entry_host["borderwidth"] = "1px"
        entry_host["font"] = tkFont.Font(family='Arial',size=10)
        entry_host["fg"] = "#333333"
        entry_host["justify"] = "center"
        entry_host.place(x=200,y=100,width=305,height=60)

        entry_port = tk.Entry(self)
        entry_port["borderwidth"] = "1px"
        entry_port["font"] = tkFont.Font(family='Arial',size=10)
        entry_port["fg"] = "#333333"
        entry_port["justify"] = "center"
        entry_port.place(x=200,y=175,width=305,height=60)

        btn_login = tk.Button(self)
        btn_login["bg"] = "#efefef"
        btn_login["font"] = tkFont.Font(family='Arial',size=24)
        btn_login["fg"] = "#000000"
        btn_login["justify"] = "center"
        btn_login["text"] = "Login"
        btn_login.place(x=190,y=290,width=230,height=80)
        btn_login["command"] = on_login


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        width=600
        height=500
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)

        self.mode = None
        self.address = None

        self.geometry(alignstr)
        self.resizable(False, False)
        self.title('Pong™')

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (SelectMode, ServerDetails):
            frame = F(master=container)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame('SelectMode')

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()


if __name__ == '__main__':
    win = MainWindow()
    win.mainloop()


