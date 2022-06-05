import datetime
import tkinter as tk
import tkinter.font as tkfont
import cv2
import os
from tkinter import messagebox
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
from config import *
from smartFridge.database import Database
from smartFridge.vkeyboard import VKeyboard

if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


class EanScanner:

    def __init__(self, root, window_title="EAN Scanner", video_source=0):

        self.db = Database()

        self.root = root
        self.root.title(window_title)
        self.root.wm_attributes('-fullscreen', 'True')

        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = f'{wnd_width}x{wnd_height}+{(screenwidth - wnd_width) // 2}+{(screenheight - wnd_height) // 2}'

        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        ft_times_12 = tkfont.Font(family='Times', size=12)
        ft_times_14 = tkfont.Font(family='Times', size=14)

        self.video_source = video_source

        self.video = VideoCapture(self.video_source)
        self.canvas = tk.Canvas(root, width=self.video.width, height=self.video.height)
        self.canvas.place(x=390, y=10, width=400, height=300)

        self.lab_ean_title = tk.Label(self.root, text="EAN", font=ft_times_12, fg=lab_fg_color, anchor=tk.W)
        self.lab_ean_title.place(x=10, y=10, width=370, height=lab_height)
        self.txt_ean = tk.Entry(self.root)
        self.txt_ean.place(x=10, y=30, width=370, height=txt_height)
        self.vkeyboard_ean = VKeyboard(self.root, self.txt_ean)

        self.lab_article_title = tk.Label(self.root, text="Artikel", font=ft_times_12, fg=lab_fg_color, anchor=tk.W)
        self.lab_article_title.place(x=10, y=80, width=370, height=lab_height)
        self.txt_article = tk.Entry(self.root)
        self.txt_article.place(x=10, y=100, width=370, height=txt_height)
        self.vkeyboard_aricle = VKeyboard(self.root, self.txt_article)

        self.lab_mhd_title = tk.Label(self.root, text="MHD", font=ft_times_12, fg=lab_fg_color, anchor=tk.W)
        self.lab_mhd_title.place(x=10, y=150, width=200, height=lab_height)
        self.txt_mhd = tk.Entry(self.root)
        self.txt_mhd.place(x=10, y=170, width=200, height=txt_height)
        self.vkeyboard_mhd = VKeyboard(self.root, self.txt_mhd)

        self.btn_home = tk.Button(self.root, text="Home", font=ft_times_14, bg=btn_bg_color, fg=btn_fg_color,
                                  anchor=tk.W, command=self.on_click_home)
        self.btn_home.place(x=10, y=420, width=150, height=btn_height)

        self.btn_enter = tk.Button(self.root, text="Hinzufügen", font=ft_times_14, bg=btn_bg_color, fg=btn_fg_color,
                                   anchor=tk.W, command=self.on_click_enter)
        self.btn_enter.place(x=170, y=420, width=150, height=btn_height)

        self.is_active = True

        self.delay = 10
        self.update()

        self.root.mainloop()

    def on_closing(self):
        print("Close")
        self.is_active = False
        del self.video
        self.vkeyboard_ean.hide_vkeyboard()
        self.vkeyboard_aricle.hide_vkeyboard()
        self.vkeyboard_mhd.hide_vkeyboard()
        self.root.destroy()

    def on_click_home(self):
        print("Home")
        self.on_closing()

    def on_click_enter(self):
        ean = self.txt_ean.get()
        mhd = self.txt_mhd.get()
        if self.is_valid_ean(ean) and self.is_valid_mhd(mhd):
            db = Database()
            article = self.txt_article.get()
            note = ""
            mhd = self.txt_mhd.get()
            db.insert(ean, article, note, mhd)
            del db
        else:
            if not self.is_valid_ean(ean):
                messagebox.showinfo(parent=self.root, message="Ungültiger EAN-Code.")
            if not self.is_valid_mhd(mhd):
                messagebox.showinfo(parent=self.root, message="Ungültiges MHD. <TT.MM.JJJJ>")

    def update(self):
        if self.is_active:
            succes, frame = self.video.get_frame()
            if succes:
                for barcode in decode(frame):
                    barcode_data = barcode.data.decode('utf-8')
                    if self.is_valid_ean(barcode_data):
                        print(barcode_data)
                        self.txt_ean.delete(0, tk.END)
                        self.txt_ean.insert(0, barcode_data)
                        cv2.putText(frame, barcode_data,
                                    (70, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (55, 255, 55), 2)

                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            self.root.after(self.delay, self.update)

    def is_valid_ean(self, barcode_data):
        if len(barcode_data) == 13:
            sum = 0
            for i, chr in enumerate(barcode_data[:12]):
                digit = ord(chr) - 48
                sum += digit
                if i % 2:
                    sum += digit * 2
            checksum = (10 - sum % 10) % 10
            return checksum == ord(barcode_data[-1]) - 48
        return False

    def is_valid_mhd(self, mhd):
        day, month, year = 0, 0, 0
        if len(mhd) == 10:
            if mhd.count(".") == 2:
                day, month, year = mhd.split(".")
        try:
            datetime.date(int(year), int(month), int(day))
            return True;
        except ValueError:
            return False


class VideoCapture:
    def __init__(self, video_source=0):
        self.video = cv2.VideoCapture(video_source)

        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
        self.video.set(cv2.CAP_PROP_FOCUS, 10)
        if not self.video.isOpened():
            raise ValueError("Unable to open video source", video_source)

        self.width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.video.isOpened():
            success, frame = self.video.read()

            if success:
                # frame = cv2.resize(frame, (0, 0), fx=3.0, fy=3.0, interpolation=cv2.INTER_NEAREST)
                return (success, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (success, None)
        else:
            return (False, None)

    def __del__(self):
        print("video release")
        if self.video.isOpened():
            self.video.release()


# Create a root and pass it to the Application object
if __name__ == '__main__':
    EanScanner(tk.Tk(), "EAN Scanner")
