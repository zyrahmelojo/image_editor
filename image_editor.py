import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter


class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editing App")
        # Adjusted window size to accommodate image and buttons
        self.root.geometry("1000x600")
        self.root.configure(bg="#e6f7ff")

        self.original_image = None
        self.image = None
        self.image_tk = None

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Load Image Button
        self.load_button = tk.Button(
            self.root, text="Load Image", command=self.load_image, bg="#007bff", fg="white", font=("Arial", 12), padx=10, pady=5
        )
        self.load_button.pack(pady=10)
