#!/usr/bin/env python3
from tkinter import Tk, Label, Button, filedialog
from tkinter import *
class Interface:
    def __init__(self, master):
        self.master = master
        master.geometry("800x800")
        master.title("Video Splicing 4 Smush")
        self.videoPath = ""
        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.import_button = Button(master, text="Import Video", command=self.importVideo)
        self.import_button.pack()

    def greet(self):
        print("Greetings!")

    def importVideo(self):
        self.videoPath = filedialog.askopenfilename(initialdir = ".", title="s")
        print(self.videoPath)

def main():
    root = Tk()
    my_gui = Interface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
