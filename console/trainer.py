from tkinter import Tk
import json
import os

from trainer.Visualizer import Visualizer

def main():
    root = Tk()
    app = Visualizer(root)

    if os.path.isfile(app.list[0]):
            app.show_image(app.list[0])
    else:
        app.show_text("Image: " + app.list[0].split('.')[0])

    root.mainloop()