import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class ExerciseSelectionFrame(tk.Frame):
    """Frame for selecting exercises from a tile-based layout."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Load and set background image
        try:
            self.bg_image_raw = Image.open(controller.config['exercise_selection_bg_image'])
            self.bg_image_tk = None # Will be set on resize
            self.bg_label = tk.Label(self, image=None)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bind("<Configure>", self._resize_background)
        except FileNotFoundError:
            messagebox.showerror("Image Error", f"Background image not found: {controller.config['exercise_selection_bg_image']}")
            self.config(bg="#f0f0f0") # Fallback background color
            self.bg_image_raw = None
        except Exception as e:
            messagebox.showerror("Image Error", f"Error loading background image: {e}")
            self.config(bg="#f0f0f0")
            self.bg_image_raw = None

        # Load and set side image
        try:
            self.side_image_raw = Image.open(controller.config['exercise_selection_side_image'])
            self.side_image_tk = None # Will be set on resize
            self.side_label = tk.Label(self, image=None, bg=self.controller.config['content_bg_color'])
            self.side_label.place(relx=0.02, rely=0.1, relwidth=0.2, relheight=0.8) # Position on left
            self.bind("<Configure>", self._resize_side_image)
        except FileNotFoundError:
            messagebox.showerror("Image Error", f"Side image not found: {controller.config['exercise_selection_side_image']}")
            self.side_image_raw = None
        except Exception as e:
            messagebox.showerror("Image Error", f"Error loading side image: {e}")
            self.side_image_raw = None

        # Content frame for tiles
        content_frame = tk.Frame(self, bg=self.controller.config['content_bg_color'], bd=5, relief="groove")
        content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.8) # Larger content frame for tiles

        tk.Label(content_frame, text="Select an Exercise for Demo", font=("Inter", 20, "bold"), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(pady=10)

        self.tiles_frame = tk.Frame(content_frame, bg=self.controller.config['content_bg_color'])
        self.tiles_frame.pack(pady=10, expand=True, fill='both')

        # Configure rows and columns for equal distribution within tiles_frame
        self.tiles_frame.grid_rowconfigure(0, weight=1)
        self.tiles_frame.grid_rowconfigure(1, weight=1)
        self.tiles_frame.grid_columnconfigure(0, weight=1)
        self.tiles_frame.grid_columnconfigure(1, weight=1)
        self.tiles_frame.grid_columnconfigure(2, weight=1)


        self.exercise_tiles = {} # Store PhotoImage references

        # Define exercises and their image paths (using config for paths)
        self.exercises = [
            {"name": "Push-up", "icon": controller.config['pushup_icon'], "demo": controller.config['pushup_demo']},
            {"name": "Squat", "icon": controller.config['squat_icon'], "demo": controller.config['squat_demo']},
            {"name": "Plank", "icon": controller.config['plank_icon'], "demo": controller.config['plank_demo']},
            {"name": "Lunges", "icon": controller.config['lunges_icon'], "demo": controller.config['lunges_demo']},
            {"name": "Burpees", "icon": controller.config['burpees_icon'], "demo": controller.config['burpees_demo']},
        ]

        self._load_exercise_tiles()

        tk.Button(content_frame, text="Back to Dashboard", font=("Inter", 12), bg=self.controller.config['button_color'], fg="white",
                  command=lambda: self.controller.show_frame("DashboardFrame"), relief="raised", bd=3, cursor="hand2", padx=10, pady=5).pack(pady=10)

    def _resize_background(self, event):
        if self.bg_image_raw:
            width, height = event.width, event.height
            if width > 0 and height > 0:
                resized_image = self.bg_image_raw.resize((width, height), Image.Resampling.LANCZOS)
                self.bg_image_tk = ImageTk.PhotoImage(resized_image)
                self.bg_label.config(image=self.bg_image_tk)
                self.bg_label.image = self.bg_image_tk

    def _resize_side_image(self, event):
        if self.side_image_raw:
            frame_width = self.side_label.winfo_width()
            frame_height = self.side_label.winfo_height()
            if frame_width > 0 and frame_height > 0:
                resized_image = self.side_image_raw.resize((frame_width, frame_height), Image.Resampling.LANCZOS)
                self.side_image_tk = ImageTk.PhotoImage(resized_image)
                self.side_label.config(image=self.side_image_tk)
                self.side_label.image = self.side_image_tk

    def _load_exercise_tiles(self):
        # Clear existing tiles
        for widget in self.tiles_frame.winfo_children():
            widget.destroy()

        row_idx, col_idx = 0, 0
        tile_size = (150, 150) # Desired size for the tile images

        for exercise in self.exercises:
            try:
                # Load icon image
                img_raw = Image.open(exercise["icon"])
                img_resized = img_raw.resize(tile_size, Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img_resized)
                self.exercise_tiles[exercise["name"]] = img_tk # Keep reference

                tile_button = tk.Button(self.tiles_frame, image=img_tk, text=exercise["name"], compound="top",
                                       font=("Inter", 12, "bold"), fg=self.controller.config['text_color'],
                                       bg=self.controller.config['tile_bg_color'], relief="raised", bd=3,
                                       cursor="hand2", padx=10, pady=10,
                                       command=lambda e=exercise: self._show_exercise_demo(e))
                tile_button.grid(row=row_idx, column=col_idx, padx=10, pady=10, sticky="nsew")

            except FileNotFoundError:
                messagebox.showerror("Image Error", f"Exercise icon not found: {exercise['icon']}")
                # Create a fallback button if image is missing
                tile_button = tk.Button(self.tiles_frame, text=f"{exercise['name']}\n(Image Missing)", compound="top",
                                       font=("Inter", 12, "bold"), fg=self.controller.config['text_color'],
                                       bg=self.controller.config['tile_bg_color'], relief="raised", bd=3,
                                       cursor="hand2", padx=10, pady=10,
                                       command=lambda e=exercise: self._show_exercise_demo(e))
                tile_button.grid(row=row_idx, column=col_idx, padx=10, pady=10, sticky="nsew")
            except Exception as e:
                messagebox.showerror("Image Error", f"Error loading exercise icon {exercise['icon']}: {e}")
                tile_button = tk.Button(self.tiles_frame, text=f"{exercise['name']}\n(Error)", compound="top",
                                       font=("Inter", 12, "bold"), fg=self.controller.config['text_color'],
                                       bg=self.controller.config['tile_bg_color'], relief="raised", bd=3,
                                       cursor="hand2", padx=10, pady=10,
                                       command=lambda e=exercise: self._show_exercise_demo(e))
                tile_button.grid(row=row_idx, column=col_idx, padx=10, pady=10, sticky="nsew")

            col_idx += 1
            if col_idx > 2: # 3 columns per row
                col_idx = 0
                row_idx += 1


class ExerciseDemoFrame(tk.Frame):
    """Frame for displaying a single exercise demo."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.current_exercise = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Load and set background image
        try:
            self.bg_image_raw = Image.open(controller.config['exercise_demo_bg_image'])
            self.bg_image_tk = None # Will be set on resize
            self.bg_label = tk.Label(self, image=None)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bind("<Configure>", self._resize_background)
        except FileNotFoundError:
            messagebox.showerror("Image Error", f"Background image not found: {controller.config['exercise_demo_bg_image']}")
            self.config(bg="#f0f0f0") # Fallback background color
            self.bg_image_raw = None
        except Exception as e:
            messagebox.showerror("Image Error", f"Error loading background image: {e}")
            self.config(bg="#f0f0f0")
            self.bg_image_raw = None

        # Load and set side image
        try:
            self.side_image_raw = Image.open(controller.config['exercise_demo_side_image'])
            self.side_image_tk = None # Will be set on resize
            self.side_label = tk.Label(self, image=None, bg=self.controller.config['content_bg_color'])
            self.side_label.place(relx=0.02, rely=0.1, relwidth=0.2, relheight=0.8) # Position on left
            self.bind("<Configure>", self._resize_side_image)
        except FileNotFoundError:
            messagebox.showerror("Image Error", f"Side image not found: {controller.config['exercise_demo_side_image']}")
            self.side_image_raw = None
        except Exception as e:
            messagebox.showerror("Image Error", f"Error loading side image: {e}")
            self.side_image_raw = None

        # Content frame for demo
        content_frame = tk.Frame(self, bg=self.controller.config['content_bg_color'], bd=5, relief="groove")
        content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.8)

        self.exercise_name_label = tk.Label(content_frame, text="", font=("Inter", 24, "bold"), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color'])
        self.exercise_name_label.pack(pady=20)

        self.demo_image_label = tk.Label(content_frame, image=None, bg=self.controller.config['content_bg_color'], bd=2, relief="groove")
        self.demo_image_label.pack(pady=20, expand=True)
        self.demo_image_tk = None # Store reference

        tk.Button(content_frame, text="Back to Exercises", font=("Inter", 12), bg=self.controller.config['button_color'], fg="white",
                  command=lambda: self.controller.show_frame("ExerciseSelectionFrame"), relief="raised", bd=3, cursor="hand2", padx=10, pady=5).pack(pady=10)

    def _resize_background(self, event):
        if self.bg_image_raw:
            width, height = event.width, event.height
            if width > 0 and height > 0:
                resized_image = self.bg_image_raw.resize((width, height), Image.Resampling.LANCZOS)
                self.bg_image_tk = ImageTk.PhotoImage(resized_image)
                self.bg_label.config(image=self.bg_image_tk)
                self.bg_label.image = self.bg_image_tk

    def _resize_side_image(self, event):
        if self.side_image_raw:
            frame_width = self.side_label.winfo_width()
            frame_height = self.side_label.winfo_height()
            if frame_width > 0 and frame_height > 0:
                resized_image = self.side_image_raw.resize((frame_width, frame_height), Image.Resampling.LANCZOS)
                self.side_image_tk = ImageTk.PhotoImage(resized_image)
                self.side_label.config(image=self.side_image_tk)
                self.side_label.image = self.side_image_tk

    def set_exercise(self, exercise_data):
        """Sets the exercise data for display in this frame."""
        self.current_exercise = exercise_data
        self.exercise_name_label.config(text=self.current_exercise["name"])
        self._load_demo_image()

    def _load_demo_image(self):
        """Loads and displays the demo image for the current exercise."""
        if self.current_exercise and self.current_exercise["demo"]:
            try:
                img_path = self.current_exercise["demo"]
                img_raw = Image.open(img_path)

                # Resize image to fit a reasonable area within the frame, e.g., 80% of content frame width
                # This needs to be responsive to the content_frame's actual size
                # For initial load, use a fixed max size
                max_width = 400
                max_height = 400

                original_width, original_height = img_raw.size
                aspect_ratio = original_width / original_height

                if original_width > max_width or original_height > max_height:
                    if aspect_ratio > 1: # Wider than tall
                        new_width = max_width
                        new_height = int(max_width / aspect_ratio)
                    else: # Taller than wide or square
                        new_height = max_height
                        new_width = int(max_height * aspect_ratio)
                else:
                    new_width, new_height = original_width, original_height

                img_resized = img_raw.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.demo_image_tk = ImageTk.PhotoImage(img_resized)
                self.demo_image_label.config(image=self.demo_image_tk)
                self.demo_image_label.image = self.demo_image_tk # Keep a reference!

            except FileNotFoundError:
                messagebox.showerror("Image Error", f"Demo image not found: {self.current_exercise['demo']}")
                self.demo_image_label.config(image=None, text="Image Not Found")
                self.demo_image_tk = None
            except Exception as e:
                messagebox.showerror("Image Error", f"Error loading demo image {self.current_exercise['demo']}: {e}")
                self.demo_image_label.config(image=None, text="Error Loading Image")
                self.demo_image_tk = None
        else:
            self.demo_image_label.config(image=None, text="No Exercise Selected")
            self.demo_image_tk = None
