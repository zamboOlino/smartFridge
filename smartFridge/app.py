import datetime
import os
import tkinter as tk
import tkinter.font as tkfont
from datetime import date
from tkinter import ttk
from tkinter import messagebox
from config import *
from eanscanner import EanScanner
from smartFridge.database import Database


class App:
    def __init__(self, window):
        self.window = window

        # setting title
        window.title("smart-fridge")

        ft_times_12 = tkfont.Font(family='Times', size=12)
        ft_times_14 = tkfont.Font(family='Times', size=14)
        ft_times_20 = tkfont.Font(family='Times', size=20)
        ft_times_48 = tkfont.Font(family='Times', size=48)

        # setting root size
        screenwidth = window.winfo_screenwidth()
        screenheight = window.winfo_screenheight()
        alignstr = f'{wnd_width}x{wnd_height}+{(screenwidth - wnd_width) // 2}+{(screenheight - wnd_height) // 2}'
        window.geometry(alignstr)
        window.resizable(width=False, height=False)

        # fridge temperature
        lab_fridge_temperature_title = tk.Label(window, text="Kühltemperatur", font=ft_times_20, fg=lab_fg_color,
                                                anchor=tk.CENTER)
        lab_fridge_temperature_title.place(x=20, y=20, width=200, height=lab_height)

        lab_fridge_temperature = tk.Label(window, text="+05.4°C", font=ft_times_48, fg="#01aaed", anchor=tk.W)
        lab_fridge_temperature.place(x=20, y=80, width=236, height=88)

        lab_mhd_criticle_title = tk.Label(window, text="MHD Kritisch", font=ft_times_20, fg=lab_fg_color, anchor=tk.W)
        lab_mhd_criticle_title.place(x=270, y=20, width=250, height=30)

        self.lst_mhd_criticle = ttk.Treeview(window, columns=("ean", "article", "mhd"), show="headings", height=5)
        self.lst_mhd_criticle.place(x=270, y=50, width=506, height=153)
        self.lst_mhd_criticle.column("ean", minwidth=0, width=120, stretch=False, anchor="w")
        self.lst_mhd_criticle.heading("ean", text="EAN")
        self.lst_mhd_criticle.column("article", minwidth=0, width=290, stretch=False, anchor="w")
        self.lst_mhd_criticle.heading("article", text="Artikel")
        self.lst_mhd_criticle.column("mhd", minwidth=0, width=100, stretch=False, anchor="e")
        self.lst_mhd_criticle.heading("mhd", text="MHD")
        self.lst_mhd_criticle.bind('<1>', self.on_lst_mhd_criticle_clicked)

        self.lab_fridge_title = tk.Label(window, text="Kühlschrank", font=ft_times_20, fg=lab_fg_color, anchor="w")
        self.lab_fridge_title.place(x=270, y=220, width=250, height=30)
        self.lst_fridge = ttk.Treeview(window, columns=("ean", "article", "mhd"), show="headings", height=5)
        self.lst_fridge.place(x=270, y=250, width=511, height=330)
        self.lst_fridge.column("ean", minwidth=0, width=120, stretch=False, anchor="w")
        self.lst_fridge.heading("ean", text="EAN")
        self.lst_fridge.column("article", minwidth=0, width=290, stretch=False, anchor="w")
        self.lst_fridge.heading("article", text="Artikel")
        self.lst_fridge.column("mhd", minwidth=0, width=100, stretch=False, anchor="e")
        self.lst_fridge.heading("mhd", text="MHD")
        self.lst_fridge.bind('<1>', self.on_lst_fridge_clicked)

        btn_home = tk.Button(window, text="Home", font=ft_times_14, bg=btn_bg_color, fg=btn_fg_color,
                             anchor=tk.W, command=self.on_click_home)
        btn_home.place(x=20, y=250, width=220, height=44)

        btn_add_article = tk.Button(window, text="Artikel hinzufügen", font=ft_times_14, bg=btn_bg_color,
                                    fg=btn_fg_color,
                                    anchor=tk.W, command=self.on_click_add_article)
        btn_add_article.place(x=20, y=300, width=220, height=44)

        btn_scan_article = tk.Button(window, text="Artikel scannen", font=ft_times_14, bg=btn_bg_color, fg=btn_fg_color,
                                     anchor=tk.W, command=self.on_click_scan_article)
        btn_scan_article.place(x=20, y=350, width=220, height=44)

        btn_statistics = tk.Button(window, text="Statistik", font=ft_times_14, bg=btn_bg_color, fg=btn_fg_color,
                                   anchor=tk.W, command=self.on_click_statistic)
        btn_statistics.place(x=20, y=400, width=220, height=44)

        self.window.bind('<FocusIn>', self.on_form_event)

    def on_lst_fridge_clicked(self, event):
        item = self.lst_fridge.identify('item', event.x, event.y)
        result = messagebox.askyesno(message="Artikel löschen")
        if result:
            db = Database()
            db.remove(item)
            del db
            self.fill_lst_fridge()

    def on_lst_mhd_criticle_clicked(self, event):
        item = self.lst_mhd_criticle.identify('item', event.x, event.y)
        result = messagebox.askyesno(message="Artikel löschen")
        if result:
            db = Database()
            db.remove(item)
            del db
            self.fill_lst_mhd_criticle()

    def on_form_event(self, event):
        self.fill_lst_fridge()
        self.fill_lst_mhd_criticle()

    def on_click_home(self):
        print("home")

    def on_click_add_article(self):
        print("add article")

    def on_click_scan_article(self):
        ean_scanner = EanScanner(tk.Toplevel(self.window))
        print("scan article")

    def on_click_statistic(self):
        print("statistic")

    def fill_lst_fridge(self):

        for item in self.lst_fridge.get_children():
            self.lst_fridge.delete(item)
        db = Database()
        articles = db.find_all()
        for article in articles:
            id = article[0]
            ean = article[1]
            article_name = article[2]
            mhd = article[4]
            self.lst_fridge.insert("", "end",
                                   iid=str(id),
                                   values=(ean, article_name, mhd))
        del db

    def fill_lst_mhd_criticle(self):
        for item in self.lst_mhd_criticle.get_children():
            print(item)
            self.lst_mhd_criticle.delete(item)
        db = Database()
        articles = db.find_all()
        self.lst_fridge.delete()
        for article in articles:
            id = article[0]
            ean = article[1]
            article_name = article[2]
            mhd = article[4]
            day, month, year = [int(token) for token in mhd.split(".")]
            mhd_date = datetime.date(year, month - 1, day) - datetime.timedelta(2)
            today = date.today()
            if today > mhd_date:
                self.lst_mhd_criticle.insert("", "end",
                                             iid=str(id),
                                             values=(ean, article_name, mhd))
        del db


if __name__ == "__main__":
    # On Raspberry TKINTER will not start if the DISPLAY environment variable is not set
    if os.environ.get('DISPLAY', '') == '':
        print('no display found. Using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')

    root = tk.Tk()
    app = App(root)
    root.wm_attributes('-fullscreen', 'True')
    root.mainloop()
