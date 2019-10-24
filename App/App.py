import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Label, Menu, Tk, PanedWindow

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
    def __init__(self, master):
        self.master = master
        master.geometry("1000x614")
        master.title("Smacket")
        self.videoPath = ""

        bcg = "#0A8049"
        topLeft = PanedWindow(master, orient=tk.VERTICAL)
        topLeft.config(bg = bcg)
        topLeft.grid(row = 0, column = 0)
        topLeftTitle = tk.Message(master, text = "Timestamps")
        topLeftTitle.config(anchor = "center", aspect = 500, font = ("consolas", 20, "bold"), bg = bcg, relief = "sunken")
        timeStamps = TextScrollCombo(master)
        timeStamps.config(width=200, height=260)
        timeStamps.txt.config(font=("consolas", 12), undo=True, wrap='word', borderwidth=3, relief="sunken")
        topLeft.add(topLeftTitle)
        topLeft.add(timeStamps)

        bottomLeft = PanedWindow(master, orient=tk.VERTICAL)
        bottomLeft.config(bg = bcg)
        bottomLeft.grid(row = 1, column = 0)
        bottomLeftTitle = tk.Message(master, text = "Matches")
        bottomLeftTitle.config(anchor = "center", aspect = 500, font = ("consolas", 20, "bold"), bg = bcg, relief = "sunken")
        matches = TextScrollCombo(master)
        matches.config(width=200, height=260)
        matches.txt.config(font=("consolas", 12), undo=True, wrap='word', borderwidth=3, relief="sunken")
        bottomLeft.add(bottomLeftTitle)
        bottomLeft.add(matches)

        videoPlayer = Label(master, 
                            height = 20, 
                            width = 120,
                            bg = 'red',
                            text = "VideoPlayer",)
        videoPlayer.grid(row=0, column=1)

        videoSkimmer = Label(master, 
                            height = 20, 
                            width = 120,
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

def main():
    root = Tk()
    interface(root)
    createMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
