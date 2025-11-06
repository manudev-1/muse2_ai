from tkinter import Label, ttk
from PIL import Image, ImageTk
import os
from random import shuffle
import json

class Visualizer:
    def __init__(self, root):
        self.root = root
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

        self.dynamic_label = Label(self.left_frame, text="Dynamic text", font=("Arial", 24))
        self.dynamic_label.pack(expand=True)

        self.__build_control_panel()
        self.list = self.__list_determination()

    # ! Public Methods !
    def clear_left_frame(self):
        """Clear the content of the left frame
        """
        for widget in self.left_frame.winfo_children():
            widget.destroy()

    def show_next(self):
        """Show next image or text from the list
        """
        if not self.list:
            self.show_text("No more items to show.")
            return

        next_item = self.list.pop(0)
        if os.path.isfile(next_item):
            self.show_image(next_item)
        else:
            self.show_text("Image: " + next_item.split('.')[0])

    def show_text(self, text: str):
        """Show text on left frame

        Args:
            text (str): Text to show
        """
        self.clear_left_frame()
        label_widget = Label(self.left_frame, font=("Arial", 24), text=text)
        label_widget.pack(expand=True)

    def show_image(self, path: str):
        """Show image on left frame

        Args:
            path (str): Path of the image to show
        """
        self.clear_left_frame()

        if not os.path.exists(path):
            lbl = Label(self.left_frame, text="⚠️ Immagine non trovata", font=("Arial", 20))
            lbl.pack(expand=True)
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

        lbl = Label(self.left_frame, image=photo)
        lbl.image = photo
        lbl.pack(expand=True)

    # ! Private Methods !
    def __build_control_panel(self):
        ttk.Label(self.right_frame, text="Contol Panel", font=("Arial", 20)).pack(pady=10)
        ttk.Button(self.right_frame, text="Show Next", command=self.show_next).pack(fill="x", pady=5)
        ttk.Button(self.right_frame, text="Exit", command=self.root.destroy).pack(fill="x", pady=20)

    def __list_determination(self) -> list:

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
        with open('trainer/list.json', 'w') as f:
            json.dump(list_to_save, f, indent=4)

    def __load_list(self) -> list | None:
        if os.path.isfile('trainer/list.json'):
            with open('trainer/list.json', 'r') as f:
                return json.load(f)
        return None