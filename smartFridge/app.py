import os
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
from config import *
from eanscanner import EanScanner


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

        lst_mhd_criticle = ttk.Treeview(window, columns=("ean", "article", "mhd"), show="headings", height=5)
        lst_mhd_criticle.place(x=270, y=50, width=506, height=153)
        lst_mhd_criticle.column("ean", minwidth=0, width=120, stretch=False, anchor="w")
        lst_mhd_criticle.heading("ean", text="EAN")
        lst_mhd_criticle.column("article", minwidth=0, width=300, stretch=False, anchor="w")
        lst_mhd_criticle.heading("article", text="Artikel")
        lst_mhd_criticle.column("mhd", minwidth=0, width=100, stretch=False, anchor="e")
        lst_mhd_criticle.heading("mhd", text="MHD")

        lab_fridge_title = tk.Label(window, text="Kühlschrank", font=ft_times_20, fg=lab_fg_color, anchor="w")
        lab_fridge_title.place(x=270, y=220, width=250, height=30)
        lst_fridge = ttk.Treeview(window, columns=("ean", "article", "mhd"), show="headings", height=5)
        lst_fridge.place(x=270, y=250, width=511, height=330)
        lst_fridge.column("ean", minwidth=0, width=120, stretch=False, anchor="w")
        lst_fridge.heading("ean", text="EAN")
        lst_fridge.column("article", minwidth=0, width=300, stretch=False, anchor="w")
        lst_fridge.heading("article", text="Artikel")
        lst_fridge.column("mhd", minwidth=0, width=100, stretch=False, anchor="e")
        lst_fridge.heading("mhd", text="MHD")

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

    def on_click_home(self):
        print("home")

    def on_click_add_article(self):
        print("add article")

    def on_click_scan_article(self):
        ean_scanner = EanScanner(tk.Toplevel(self.window))
        print("scan article")

    def on_click_statistic(self):
        print("statistic")


if __name__ == "__main__":
    # On Raspberry TKINTER will not start if the DISPLAY environment variable is not set
    if os.environ.get('DISPLAY', '') == '':
        print('no display found. Using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')

    root = tk.Tk()
    app = App(root)
    root.mainloop()
