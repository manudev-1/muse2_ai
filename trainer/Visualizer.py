from tkinter import Label, ttk, Tk
import os
from random import shuffle
import json
from PIL import Image, ImageTk
import time
from threading import Thread
from typing import Literal

from .model.Register import Register

class Visualizer:
    def __init__(self, root: Tk, recorder: Register):
        self.root = root
        self.recorder = recorder
        
        self.root.title("Trainer")

        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.root.attributes('-fullscreen', False))

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=1)

        self.left_frame = ttk.Frame(self.root, padding=10, relief="ridge")
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.right_frame = ttk.Frame(self.root, padding=10, relief="ridge")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        self.image_label = Label(self.left_frame)
        self.image_label.pack(expand=True)

        self.text_label = Label(self.left_frame, font=("Arial", 24))
        self.text_label.pack(expand=True)
        
        self.debug_label = Label(self.right_frame, text="Debug Label", font=("Arial", 14))
        self.debug_label.pack(pady=10)

        self.__build_control_panel()
        self.list = self.__list_determination()

    # ! Public Methods !
    def set_ready(self):
        """Set the application to ready state
        """
        for i in range(3):
            self.debug_label.config(text=f"Starting in {3 - i}...")
            self.root.update()
            time.sleep(1)
        self.debug_label.config(text=f"Recording...")
        Thread(target=self.__main_loop, daemon=True).start()

    def exit(self):
        """Exit the application
        """
        self.__save_list(self.list)
        self.root.destroy()
        
    # ! Private Methods !
    def __build_control_panel(self):
        """Build control panel"""
        ttk.Label(self.right_frame, text="Contol Panel", font=("Arial", 20)).pack(pady=10)
        ttk.Button(self.right_frame, text="Ready", command=self.set_ready).pack(fill="x", pady=5)
        ttk.Button(self.right_frame, text="Exit", command=self.exit).pack(fill="x", pady=20)

    def __list_determination(self) -> list:
        """If list order doesnt exist create it, otherwise it is returned"""
        loaded_list = self.__load_list()
        if loaded_list is not None:
            return loaded_list

        based_path = os.path.join(".", "trainer", "images")
        dict_list = {}

        for cat in os.listdir(based_path):
            cat_path = os.path.join(based_path, cat)
            if os.path.isdir(cat_path):
                for img in os.listdir(cat_path):
                    img_path = os.path.join(cat_path, img)
                    if os.path.isfile(img_path):
                        dict_list[img] = img_path

        list_imgs = list(dict_list.keys()) * 120

        counts = {img: 0 for img in dict_list}

        for i, img_name in enumerate(list_imgs):
            counts[img_name] += 1
            if counts[img_name] > 60:
                list_imgs[i] = dict_list[img_name]

        shuffle(list_imgs)

        self.__save_list(list_imgs)

        return list_imgs

    def __save_list(self, list_to_save: list):
        """Save the list

        Args:
            list_to_save (list): List saved
        """
        with open('trainer/list.json', 'w') as f:
            json.dump(list_to_save, f, indent=4)

    def __load_list(self) -> list | None:
        """If exist, load the list"""
        if os.path.isfile('trainer/list.json'):
            with open('trainer/list.json', 'r') as f:
                return json.load(f)
        return None
    
    def __save_block(self, phase: Literal['imagination', 'perception'], image_name: str | None = None):
        """Save the recorded block

        Args:
            phase (Literal[&#39;imagination&#39;, &#39;perception&#39;]): imagination or perception
            image_name (str | None, optional): name of the image shown. Defaults to None.
        """
        block = self.recorder.record_block(phase=phase, image_name=image_name)
        self.recorder.save(block)
    
    def __show_next(self):
        """Show next image or text from the list
        """
        if not self.list:
            self.show_text("No more items to show.")
            return False
        phase = ''

        next_item = self.list.pop(0)
        if os.path.isfile(next_item):
            self.__show_image(next_item)
            phase = 'perception'
            name = next_item
        else:
            self.__show_text("Image: " + next_item.split('.')[0])
            phase = 'imagination'
            name = next_item.split('.')[0]
        
        self.root.update()
        
        thread = Thread(target=self.__save_block, kwargs={"phase":phase, "image_name":name})
        thread.start()
        thread.join()
        return True

    def __show_text(self, text: str):
        """Show text on left frame

        Args:
            text (str): Text to show
        """
        self.image_label.config(image=None)
        self.image_label.image = None
        self.text_label.config(text=text)
        
    def __show_image(self, path: str):
        """Show image on left frame

        Args:
            path (str): Path of the image to show
        """

        if not os.path.exists(path):
            self.dynamic_label.config(text="Image not found.")
            return

        img = Image.open(path)
        width = self.left_frame.winfo_width()
        height = self.left_frame.winfo_height()
        if width <= 1 or height <= 1:
            self.root.after(100, lambda: self.show_image(path))
            return

        img = Image.open(path)
        img_w, img_h = img.size
        img_ratio = img_w / img_h
        target_ratio = 16 / 9

        if img_ratio > target_ratio:
            new_width = int(img_h * target_ratio)
            offset = (img_w - new_width) // 2
            img = img.crop((offset, 0, offset + new_width, img_h))
        elif img_ratio < target_ratio:
            new_height = int(img_w / target_ratio)
            offset = (img_h - new_height) // 2
            img = img.crop((0, offset, img_w, offset + new_height))

        target_w = int(width * 0.9)
        target_h = int(target_w / target_ratio)
        if target_h > height * 0.9:
            target_h = int(height * 0.9)
            target_w = int(target_h * target_ratio)

        img = img.resize((target_w, target_h))
        photo = ImageTk.PhotoImage(img)
        
        self.text_label.config(text="")
        self.image_label.config(image=photo)
        self.image_label.image = photo
        
    def __clear(self):
        self.image_label.config(image=None)
        self.image_label.image = None
        self.text_label.config(text="")
           
    def __main_loop(self):
        for i in range(400):
            self.__show_next()

            self.debug_label.config(text=f"Recording...")
            self.root.update_idletasks()

            self.__clear()

        self.debug_label.config(text="Training session done!")
        self.root.update_idletasks()
        