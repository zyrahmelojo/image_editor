import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageEnhance


class ImageEditorApp:
    def __init__(self, master):
        self.root = master
        self.root.title("Image Editing App")
        self.root.geometry("1000x700")
        self.root.configure(bg="#e6f7ff")
        self.contrast_slider = None
        self.brightness_slider = None
        self.save_button = None
        self.reset_button = None
        self.buttons_frame = None
        self.filters_frame = None
        self.image_label = None
        self.load_button = None
        self.original_image = None
        self.image = None
        self.image_tk = None

        # History for undo/redo
        self.history = []
        self.redo_stack = []

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Load Image Button
        self.load_button = tk.Button(
            self.root, text="Load Image", command=self.load_image,
            bg="#007bff", fg="white", font=("Arial", 10), padx=8, pady=3
        )
        self.load_button.pack(pady=8)
