import os
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont


class App:
    def __init__(self, root):
        # setting title
        root.title("smart-fridge")

        # setting window size
        width = 800
        height = 600
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        ft_times_14 = tkFont.Font(family='Times', size=14)
        ft_times_20 = tkFont.Font(family='Times', size=20)
        ft_times_48 = tkFont.Font(family='Times', size=48)

        # fridge temperature
        lab_fridge_temperature_title = tk.Label(root, font=ft_times_20, anchor="c")
        lab_fridge_temperature_title.place(x=20, y=20, width=200, height=30)
        lab_fridge_temperature_title["fg"] = "#333333"
        lab_fridge_temperature_title["text"] = "Kühltemperatur"

        lab_fridge_temperature = tk.Label(root, font=ft_times_48)
        lab_fridge_temperature.place(x=20, y=80, width=236, height=88)
        lab_fridge_temperature["fg"] = "#01aaed"
        lab_fridge_temperature["justify"] = "left"
        lab_fridge_temperature["text"] = "+05.4°C"

        lab_mhd_criticle_title = tk.Label(root, font=ft_times_20, anchor="w")
        lab_mhd_criticle_title.place(x=270, y=20, width=250, height=30)
        lab_mhd_criticle_title["fg"] = "#333333"
        lab_mhd_criticle_title["text"] = "MHD Kritisch"

        lst_mhd_criticle = ttk.Treeview(root, columns=("ean", "article", "mhd"), show="headings", height=5)
        lst_mhd_criticle.place(x=270, y=50, width=506, height=153)
        lst_mhd_criticle.column("ean", minwidth=0, width=120, stretch=False, anchor="w")
        lst_mhd_criticle.heading("ean", text="EAN")
        lst_mhd_criticle.column("article", minwidth=0, width=300, stretch=False, anchor="w")
        lst_mhd_criticle.heading("article", text="Artikel")
        lst_mhd_criticle.column("mhd", minwidth=0, width=100, stretch=False, anchor="e")
        lst_mhd_criticle.heading("mhd", text="MHD")

        lab_fridge_title = tk.Label(root, font=ft_times_20, anchor="w")
        lab_fridge_title.place(x=270, y=220, width=250, height=30)
        lab_fridge_title["fg"] = "#333333"
        lab_fridge_title["text"] = "Kühlschrank"
        lst_fridge = ttk.Treeview(root, columns=("ean", "article", "mhd"), show="headings", height=5)
        lst_fridge.place(x=270, y=250, width=511, height=330)
        lst_fridge.column("ean", minwidth=0, width=120, stretch=False, anchor="w")
        lst_fridge.heading("ean", text="EAN")
        lst_fridge.column("article", minwidth=0, width=300, stretch=False, anchor="w")
        lst_fridge.heading("article", text="Artikel")
        lst_fridge.column("mhd", minwidth=0, width=100, stretch=False, anchor="e")
        lst_fridge.heading("mhd", text="MHD")

        btn_home = tk.Button(root,
                             text="Home",
                             font=ft_times_14,
                             bg="#cc33cc",
                             fg="white",
                             anchor="w",
                             command=self.on_click_home)
        btn_home.place(x=20, y=250, width=220, height=44)

        btn_add_article = tk.Button(root,
                                    text="Artikel hinzufügen",
                                    font=ft_times_14,
                                    bg="#cc33cc",
                                    fg="white",
                                    anchor="w",
                                    command=self.on_click_add_article)
        btn_add_article.place(x=20, y=300, width=220, height=44)

        btn_scan_article = tk.Button(root,
                                     text="Artikel scannen",
                                     font=ft_times_14,
                                     bg="#cc33cc",
                                     fg="white",
                                     anchor="w",
                                     command=self.on_click_scan_article)
        btn_scan_article.place(x=20, y=350, width=220, height=44)

        btn_statistics = tk.Button(root,
                                   text="Statistik",
                                   font=ft_times_14,
                                   bg="#cc33cc",
                                   fg="white",
                                   anchor="w",
                                   command=self.on_click_statistic)
        btn_statistics.place(x=20, y=400, width=220, height=44)

    def on_click_home(self):
        print("home")

    def on_click_add_article(self):
        print("add article")

    def on_click_scan_article(self):
        print("scan article")

    def on_click_statistic(self):
        print("statistic")


if __name__ == "__main__":
    # On Rasperry TKINTER will not start if the DISPLAY environment variable is not set
    if os.environ.get('DISPLAY', '') == '':
        print('no display found. Using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')

    root = tk.Tk()
    app = App(root)
    root.mainloop()
