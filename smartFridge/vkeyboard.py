import os
from tkinter import *
import tkinter.font as tkfont


class VKeyboardView(Toplevel):

    def __init__(self, root, entry, x, y, key_color="#e3e3e3", key_size=3):
        Toplevel.__init__(self, takefocus=0)

        self.overrideredirect(True)
        self.attributes('-alpha', 0.85)

        self.root = root
        self.entry = entry
        self.x = x
        self.y = y
        self.key_size = key_size
        self.key_color = key_color
        self.shift = False

        self.rows = []
        for i in [0, 1, 2, 3, 4]:
            frame = Frame(self)
            frame.grid(row=i)
            self.rows.append(frame)

        self._init_keys()
        self.update_idletasks()
        self.geometry(f'{self.winfo_width()}x{self.winfo_height()}+{self.x}+{self.y}')

        self.bind('<Key>', lambda e: self.on_destroy())

    def _init_keys(self):
        self.alpha = {
            'row1': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '<x'],
            'row2': ['q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p', '/'],
            'row3': ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ',', '[ ENTER ]'],
            'row4': ['shift', 'y', 'x', 'c', 'v', 'b', 'n', 'm', '.', '?'],
            'row5': ['@', '#', '%', '*', '[ SPACE ]', '+', '-', '=']
        }

        for y, row in enumerate(self.alpha):
            for x, k in enumerate(self.alpha[row]):
                if k == '[ SPACE ]':
                    Button(self.rows[y], text=k, width=self.key_size * 3, bg=self.key_color,
                           command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=x + y)
                else:
                    Button(self.rows[y], text=k, width=self.key_size, bg=self.key_color,
                           command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=x + y)

    def _attach_key_press(self, k):
        if k == '[ ENTER ]':
            self.destroy()
        elif k == '[ SPACE ]':
            self.entry.insert(END, ' ')
        elif k == '<x':
            self.entry.delete(len(self.entry.get()) - 1, END)
        elif k == 'shift':
            self.shift = True
            return
        else:
            if self.shift and k in 'abcdefghijklmnopqrstuvwxyz':
                self.entry.insert(END, k.upper())
            else:
                self.entry.insert(END, k)
        self.shift = False

    def on_destroy(self):
        self.destroy()


class VKeyboard:
    def __init__(self, root, entry):
        self.root = root
        self.entry = entry
        self.state = 'idle'
        self.vkeyboard_view = None

        self.entry.bind('<FocusIn>', lambda e: self.check_state('focusin', self.root, self.entry))
        self.entry.bind('<FocusOut>', lambda e: self.check_state('focusout', self.root, self.entry))
        self.entry.bind('<Key>', lambda e: self.check_state('keypress', self.root, self.entry))

    def check_state(self, event, root, entry):
        if self.state == 'idle':
            if event == 'focusin':
                self.show_vkeyboard(root, entry)
                self.state = 'virtualkeyboard'
        elif self.state == 'virtualkeyboard':
            if event == 'focusin':
                self.hide_vkeyboard()
                self.state = 'typing'
            elif event == 'keypress':
                self.hide_vkeyboard()
                self.state = 'typing'
        elif self.state == 'typing':
            if event == 'focusout':
                self.state = 'idle'

    def hide_vkeyboard(self):
        if self.vkeyboard_view:
            self.vkeyboard_view.on_destroy()

    def show_vkeyboard(self, parent, entry):
        self.vkeyboard_view = VKeyboardView(entry=entry, root=parent, x=entry.winfo_rootx(),
                                            y=entry.winfo_rooty() + entry.winfo_reqheight(),
                                            key_size=3, key_color="#e3e3e3")


if __name__ == '__main__':

    if os.environ.get('DISPLAY', '') == '':
        print('no display found. Using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')

    root = Tk()
    root.geometry(f'{220}x{200}+{400}+{200}')

    ft_times_12 = tkfont.Font(family='Times', size=12)

    lab_ean_title = Label(root, text="EAN", font=ft_times_12, fg='black', anchor=W)
    lab_ean_title.place(x=10, y=10, width=200, height=30)
    txt_ean = Entry(root)
    txt_ean.place(x=10, y=40, width=200, height=30)

    lab_article_title = Label(root, text="Artikel", font=ft_times_12, fg='black', anchor=W)
    lab_article_title.place(x=10, y=80, width=200, height=30)
    txt_article = Entry(root)
    txt_article.place(x=10, y=120, width=200, height=30)

    VKeyboard(root, txt_ean)
    VKeyboard(root, txt_article)

    root.mainloop()
