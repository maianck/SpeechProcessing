from tkinter import *
import os
from os import walk
from tkinter import filedialog

from speech_record import Recording

window = Tk()


def choose_tittle():
    def sel():
        choice['text'] = str(var.get())

    def add_title():
        title = input_text.get()
        choices.append(title)
        dirname = filedialog.askdirectory(parent=choice_window, initialdir="/",
                                          title='Records')
        if not dirname:
            quit()
        full_path = dirname + "/" + title
        os.mkdir(full_path)

    choice_window = Tk()
    choice_window.geometry("200x200")
    choice_window.title("Chọn chủ đề")
    add = Button(choice_window, text="Thêm chủ đề", command=add_title)
    add.place(x=10, y=10)
    input_text = Entry(choice_window, text="Nhập chủ đề", bd=5)
    choices = []
    mypath = './Records/'
    for (dirpath, dirnames, filenames) in walk(mypath):
        choices = dirnames
    var = IntVar()
    for c in choices:
        r = Radiobutton(choice_window, text=c, variable=var, value=1, command=sel)
        r.pack(anchor=W)
    choice_window.mainloop()


RC = Recording()


def start_recording():
    RC.start_record('record.wav')


def stop_recording():
    RC.stop()


choice = Button(window, text="Chọn chủ đề", command=choose_tittle)
choice.place(x=100, y=100)

start = Button(window, text="Bắt đầu ghi âm", command=start_recording)
start.place(x=100, y=200)

stop = Button(window, text="Dừng ghi âm", command=stop_recording)
stop.place(x=100, y=250)

window.title('Speech recording application')
window.geometry("1000x600")
window.mainloop()
