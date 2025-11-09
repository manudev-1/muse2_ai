from tkinter import Tk
import os

from trainer.Visualizer import Visualizer
from trainer.model.Register import Register

def main():
    root = Tk()
    app = Visualizer(root, recorder=Register())

    root.mainloop()