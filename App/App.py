#!/usr/bin/env python3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Label, Menu, Tk, PanedWindow
import argparse

class TextScrollCombo(ttk.Frame):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
    # ensure a consistent GUI size
        self.grid_propagate(False)
    # implement stretchability
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    # create a Text widget
        self.txt = tk.Text(self)
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

    # create a Scrollbar and associate it with txt
        scrollb = ttk.Scrollbar(self, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set

class interface:
    def __init__(self, master, appWidth, appHeight):
        self.master = master
        geo = "%dx%d" % (appWidth, appHeight)
        master.geometry(geo)
        master.title("Smacket")
        self.videoPath = ""

        bcg = "#0A8049"
        topLeft = PanedWindow(master, orient=tk.VERTICAL)
        topLeft.config(bg = bcg)
        topLeft.grid(row = 0, column = 0)
        topLeftTitle = tk.Message(master, text = "Timestamps")
        topLeftTitle.config(anchor = "center", aspect = 500, font = ("consolas", 20, "bold"), bg = bcg, relief = "sunken")
        timeStamps = TextScrollCombo(master)
        timeStamps.config(width=appWidth // 10, height= appHeight // 2)
        timeStamps.txt.config(font=("consolas", 12), undo=True, wrap='word', borderwidth=3, relief="sunken")
        topLeft.add(topLeftTitle)
        topLeft.add(timeStamps)

        bottomLeft = PanedWindow(master, orient=tk.VERTICAL)
        bottomLeft.config(bg = bcg)
        bottomLeft.grid(row = 1, column = 0)
        bottomLeftTitle = tk.Message(master, text = "Matches")
        bottomLeftTitle.config(anchor = "center", aspect = 500, font = ("consolas", 20, "bold"), bg = bcg, relief = "sunken")
        matches = TextScrollCombo(master)
        matches.config(width= appWidth// 10 , height=appHeight // 2)
        matches.txt.config(font=("consolas", 12), undo=True, wrap='word', borderwidth=3, relief="sunken")
        bottomLeft.add(bottomLeftTitle)
        bottomLeft.add(matches)

        videoPlayer = Label(master, 
                            height = 20,
                            width = appWidth - (appWidth // 10),
                            bg = 'red',
                            text = "VideoPlayer",)
        videoPlayer.grid(row=0, column=1)

        videoSkimmer = Label(master, 
                            height = 20,
                            width = appWidth - (appWidth // 10),
                            bg = 'yellow',
                            text = "VideoSkimmer",)
        videoSkimmer.grid(row=1, column=1)


def createMenu(root):
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Import Video", command=root.quit)
    filemenu.add_command(label="Import Timeline", command=importTimeline)
    filemenu.add_command(label="Export", command=root.quit)
    filemenu.add_command(label="Save", command=root.quit)
    filemenu.add_command(label="Close", command=root.quit)

    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    root.config(menu=menubar)

def importTimeline():
    fileName = "timeline.txt"
    f = open(fileName, "r")
    f1 = f.readlines()
    for x in f1:
        print(x)

def cli_args():
    parser = argparse.ArgumentParser(description='Simple GUI to utilize the video trimmer')
    parser.add_argument("--height", help="Desired height for application window")
    parser.add_argument("--width", help="Desired width for application window")
    parser.add_argument("--video", help="Optional preload video input")
    parser.add_argument("--timeline", help="Optional preload timeline input")
    args = parser.parse_args()
    return args


def main():
    root = Tk()
    args = cli_args()
    interface(root, int(args.width), int(args.height))
    createMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
