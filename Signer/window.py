from tkinter import *
import time


class TextWindow:

    def __init__(self, master):
        self.root = master
        frame = Frame(master)
        frame.pack()
        # master.title("Gesture Keyboard Output")

        self.label = Label(master, text="Connecting...", font=("Helvetica", 50))
        self.label.configure(width=500, height=500, wraplength=800)
        self.label.configure()
        self.label.pack()

        self.update_clock()

    def update_clock(self):
        input_file = open("output.txt")
        self.label.configure(text=input_file.read())
        input_file.close()
        self.root.after(100, self.update_clock)

try:
    root = Tk()
    app = TextWindow(root)
    root.wm_attributes('-fullscreen', 'true')
    root.mainloop()
    root.destroy()
except TclError:
    print(" ")
    print("CLOSED")






