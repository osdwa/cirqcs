import tkinter as tk
import tkinter.ttk as ttk


class Button(tk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, font="{Arial} 12 bold", fg="white", bg="#444", bd=0)


class Listbox(tk.Listbox):
    def __init__(self, *args, font="Arial 11", fg="white", sfg="white", **kwargs):
        super().__init__(*args, **kwargs, font=font, fg=fg, bg="#2e2e2e", activestyle="none",
                         borderwidth=0, highlightcolor="#444", highlightbackground="#444",
                         selectforeground=sfg, selectbackground="#777")
