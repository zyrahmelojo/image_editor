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
        # Image Display
        self.image_label = tk.Label(self.root, bg="#e6f7ff")
        self.image_label.pack(pady=8)

        # Filters Section
        self.filters_frame = tk.Frame(self.root, bg="#e6f7ff")
        self.filters_frame.pack(pady=18)

        filters = [
            ("Blur", ImageFilter.BLUR),
            ("Contour", ImageFilter.CONTOUR),
            ("Edge Enhance", ImageFilter.EDGE_ENHANCE),
            ("Emboss", ImageFilter.EMBOSS),
            ("Sharpen", ImageFilter.SHARPEN),
            ("Smooth", ImageFilter.SMOOTH),
        ]
        for filter_name, filter_type in filters:
            tk.Button(
                self.filters_frame, text=filter_name, command=lambda ft=filter_type: self.apply_filter(
                ft), bg="#007bff", fg="white", font=("Arial", 8), padx=8, pady=3
            ).pack(side="left", padx=8, pady=3)

        # Extra Filters
        tk.Button(self.filters_frame, text="Grayscale",
                  command=self.apply_grayscale,
                  bg="#6c757d", fg="white", font=("Arial", 8), padx=8
                  ).pack(side="left", padx=8)

        # Buttons Frame
        self.buttons_frame = tk.Frame(self.root, bg="#e6f7ff")
        self.buttons_frame.pack(pady=18)

        # Reset Button
        self.reset_button = tk.Button(
            self.buttons_frame, text="Reset Image", command=self.reset_image,
            bg="#28a745", fg="white", font=("Arial", 10), padx=8, pady=3
        )
        self.reset_button.pack(side="left", padx=8)

        # Save Image Button
        self.save_button = tk.Button(
            self.buttons_frame, text="Save Image", command=self.save_image, bg="#17a2b8", fg="white", font=("Arial", 10), padx=8, pady=3
        )
        self.save_button.pack(side="left", padx=10)

        # Rotate & Flip Buttons
        tk.Button(self.buttons_frame, text="Rotate 90°",
                  command=lambda: self.rotate_image(90),
                  bg="#ffc107", fg="black", font=("Arial", 10), padx=8, pady=3
                  ).pack(side="left", padx=8)

        tk.Button(self.buttons_frame, text="Flip Horizontal",
                  command=self.flip_horizontal,
                  bg="#ffc107", fg="black", font=("Arial", 10), padx=8, pady=3
                  ).pack(side="left", padx=8)

        # Undo/Redo Buttons
        tk.Button(self.buttons_frame, text="Undo",
                  command=self.undo,
                  bg="#dc3545", fg="white", font=("Arial", 10), padx=8, pady=3
                  ).pack(side="left", padx=8)

        tk.Button(self.buttons_frame, text="Redo",
                  command=self.redo,
                  bg="#dc3545", fg="white", font=("Arial", 10), padx=8, pady=3
                  ).pack(side="left", padx=8)

        # Brightness & Contrast Sliders
        self.brightness_slider = tk.Scale(self.root, from_=-50, to=50,
                                          orient="horizontal", label="Brightness",
                                          command=self.adjust_brightness)
        self.brightness_slider.pack(fill="x", padx=18)

        self.contrast_slider = tk.Scale(self.root, from_=-50, to=50,
                                        orient="horizontal", label="Contrast",
                                        command=self.adjust_contrast)
        self.contrast_slider.pack(fill="x", padx=18)
    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpg *.png *.bmp *.gif")]
        )
        if file_path:
            self.original_image = Image.open(file_path)
            self.image = self.original_image.copy()
            self.history = [self.image.copy()] #reset history
            self.display_image()

    def display_image(self):
        if self.image:
            max_width, max_height = 400, 300
            aspect_ratio = self.image.width / self.image.height

            if self.image.width > self.image.height:
                new_width = min(max_width, self.image.width)
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = min(max_height, self.image.height)
                new_width = int(new_height * aspect_ratio)

            self.image_tk = ImageTk.PhotoImage(
                self.image.resize((new_width, new_height), Image.LANCZOS)
            )
            self.image_label.configure(image=self.image_tk)

    def apply_filter(self, filter_type):
        if self.image:
            self.image = self.image.filter(filter_type)
            self.history.append(self.image.copy())
            self.redo_stack.clear()  # clear redo when new action
            self.display_image()

    def reset_image(self):
        if self.original_image:
            self.image = self.original_image.copy()
            self.display_image()

    def apply_grayscale(self):
        if self.image:
            self.image = self.image.convert("L").convert("RGB")
            self.history.append(self.image.copy())
            self.display_image()

    def save_image(self):
        if self.image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"),
                           ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            if file_path:
                self.image.save(file_path)
                messagebox.showinfo("Success", "Image saved successfully!")

    def rotate_image(self, angle):
        if self.image:
            self.image = self.image.rotate(angle, expand=True)
            self.history.append(self.image.copy())
            self.display_image()

    def flip_horizontal(self):
        if self.image:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            self.history.append(self.image.copy())
            self.display_image()

    def adjust_brightness(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Brightness(self.original_image)
            self.image = enhancer.enhance(1 + int(value) / 100)
            self.history.append(self.image.copy())
            self.display_image()

    def adjust_contrast(self, value):
        if self.original_image:
            enhancer = ImageEnhance.Contrast(self.original_image)
            self.image = enhancer.enhance(1 + int(value) / 100)
            self.display_image()







