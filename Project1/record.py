# Import the necessary modules.
import tkinter
from tkinter import *
import tkinter.messagebox
import pyaudio
import wave
import os


class Application:
    FILE_NAME = "X.wav"

    def __init__(self, chunk=3024, frmat=pyaudio.paInt16, channels=2, rate=44100, py=pyaudio.PyAudio()):
        # Start Tkinter and set Title
        self.main = tkinter.Tk()
        self.collections = []
        self.main.geometry('1000x600')
        self.main.title('Record')
        self.CHUNK = chunk
        self.FORMAT = frmat
        self.CHANNELS = channels
        self.RATE = rate
        self.p = py
        self.frames = []
        self.st = 1
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True,
                                  frames_per_buffer=self.CHUNK)

        # Set Frames
        self.buttons = tkinter.Frame(self.main, padx=120, pady=100)

        # Pack Frame
        self.buttons.pack(fill=BOTH)

        # Title button
        self.title = Menubutton(self.buttons, width=10, padx=10,
                                pady=5, text="Chọn chủ đề", relief=RAISED)
        self.title.grid(row=0, column=0, padx=20, pady=5)
        self.title.menu = Menu(self.title)
        self.title["menu"] = self.title.menu

        # Show record sentence
        self.record_text = Text(self.buttons, width=75, height=20)
        self.record_text.grid(row=0, column=1, padx=20, pady=5)

        # Show statement
        self.statement = Label(self.buttons, text="", padx=10, pady=5)
        self.statement.grid(row=1, column=1, padx=10, pady=5)

        # Create title list
        choices = []
        mypath = './Records/'
        choices = os.listdir(mypath)
        for c in choices:
            self.title.menu.add_command(label=c, command=lambda c=c: self.record_title(c))

        # Start and Stop buttons
        self.strt_rec = tkinter.Button(self.buttons, width=10, padx=10,
                                       pady=5, text='Bắt đầu ghi âm', command=lambda: self.start_record())
        self.strt_rec.grid(row=3, column=0, padx=20, pady=5)
        self.stop_rec = tkinter.Button(self.buttons, width=10, padx=10,
                                       pady=5, text='Dừng ghi âm', command=lambda: self.stop())
        self.stop_rec.grid(row=4, column=0, columnspan=1, padx=20, pady=5)
        self.sentence_len = 0
        self.num_sen = 0
        self.sentences = []

        tkinter.mainloop()

    def start_record(self):
        self.st = 1
        self.frames = []
        self.statement['text'] = 'Đang ghi âm'
        stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True,
                             frames_per_buffer=self.CHUNK)
        while self.st == 1:
            data = stream.read(self.CHUNK)
            self.frames.append(data)
            print("* recording")
            self.main.update()

        stream.close()

        wf = wave.open(self.FILE_NAME + str(self.sentence_len - 1) + '.wav', 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def stop(self):
        self.st = 0
        self.statement['text'] = 'Dừng ghi âm'
        print("* stop recording")
        f = open(self.FILE_NAME + "link.txt", "a", encoding="utf8")
        f.write(str(self.sentence_len) + '.wav' + '\n')
        f.write(self.sentences[self.sentence_len] + '\n')
        f.close()
        self.sentence_len = self.sentence_len + 1
        if self.sentence_len >= self.num_sen:
            self.record_text.delete("1.0", END)
            self.record_text.insert(END, "Đã ghi âm xong chủ đề này")
        else:
            self.record_text.delete("1.0", END)
            self.record_text.insert(END, self.sentences[self.sentence_len])

    def record_title(self, direct):
        self.title['text'] = direct
        file_doc = 'Records/' + direct + '/doc.txt'
        file = open(file_doc, "r", encoding="utf8")
        doc_list = [line for line in file]
        docstr = ''.join(doc_list)
        self.sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', docstr)
        ss = []
        for s in self.sentences:
            ss.append(s.strip().replace('\n', ''))
        self.sentences = ss
        self.sentence_len = 0
        self.num_sen = self.sentences.__len__()
        self.record_text.delete("1.0", END)
        self.record_text.insert(END, self.sentences[0])
        self.FILE_NAME = 'Records/' + direct + "/"
        f = open(self.FILE_NAME + "link.txt", "a", encoding="utf8")
        f.write('\n')
        f.close()


# Create an object of the ProgramGUI class to begin the program.
app = Application()
