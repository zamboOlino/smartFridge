import tkinter as tk
import tkinter.font as tkfont
import cv2
import os
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
from config import *
from smartFridge.vkeyboard import VKeyboard

if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


class EanScanner:
    def __init__(self, root, window_title="EAN Scanner", video_source=0):

        self.root = root
        self.root.title(window_title)
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
        self.btn_home.place(x=10, y=540, width=100, height=btn_height)

        self.btn_enter = tk.Button(self.root, text="Eingabe", font=ft_times_14, bg=btn_bg_color, fg=btn_fg_color,
                                   anchor=tk.E, command=self.on_click_enter)
        self.btn_enter.place(x=120, y=540, width=100, height=btn_height)

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
        print("Enter")

    def update(self):
        if self.is_active:
            succes, frame = self.video.get_frame()

            if succes:
                for barcode in decode(frame):
                    barcode_data = barcode.data.decode('utf-8')
                    print(barcode_data)
                    self.txt_ean.delete(0, tk.END)
                    self.txt_ean.insert(0, barcode_data)
                    # pts = np.array([barcode.polygon], np.int32)
                    # pts = pts.reshape((-1, 1, 2))
                    # cv2.polylines(frame, [pts], True, (255, 0, 255), 5)
                    pts2 = barcode.rect
                    cv2.putText(frame, barcode_data,
                                (pts2[0], pts2[1]),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (255, 0, 255), 2)

                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            self.root.after(self.delay, self.update)


class VideoCapture:
    def __init__(self, video_source=0):
        self.video = cv2.VideoCapture(video_source)
        if not self.video.isOpened():
            raise ValueError("Unable to open video source", video_source)

        self.width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.video.isOpened():
            success, frame = self.video.read()

            if success:
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
