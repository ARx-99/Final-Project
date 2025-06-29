import tkinter as tk
from tkinter import messagebox, scrolledtext # Import scrolledtext
from PIL import Image, ImageTk, ImageSequence # Import ImageSequence for GIF frames
import os

class ExerciseSelectionFrame(tk.Frame):
    """Frame for selecting exercises from a tile-based layout."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Removed: Load and set background image
        # try:
        #     self.bg_image_raw = Image.open(controller.config['exercise_selection_bg_image'])
        #     self.bg_image_tk = None # Will be set on resize
        #     self.bg_label = tk.Label(self, image=None)
        #     self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        #     self.bind("<Configure>", self._resize_background)
        # except FileNotFoundError:
        #     messagebox.showerror("Image Error", f"Background image not found: {controller.config['exercise_selection_bg_image']}")
        #     self.config(bg="#f0f0f0") # Fallback background color
        #     self.bg_image_raw = None
        # except Exception as e:
        #     messagebox.showerror("Image Error", f"Error loading background image: {e}")
        #     self.config(bg="#f0f0f0")
        #     self.bg_image_raw = None

        # Set solid grey background
        self.config(bg="grey")

        # Content frame for tiles - Adjusted relwidth to be larger
        content_frame = tk.Frame(self, bg=self.controller.config['content_bg_color'], bd=5, relief="groove")
        content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8) # Larger content frame for tiles

        tk.Label(content_frame, text="Select an Exercise for Demo", font=("Inter", 20, "bold"), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(pady=10)

        self.tiles_frame = tk.Frame(content_frame, bg=self.controller.config['content_bg_color'])
        self.tiles_frame.pack(pady=10, expand=True, fill='both')

        # Configure rows and columns for equal distribution within tiles_frame
        self.tiles_frame.grid_rowconfigure(0, weight=1)
        self.tiles_frame.grid_rowconfigure(1, weight=1)
        self.tiles_frame.grid_columnconfigure(0, weight=1)
        self.tiles_frame.grid_columnconfigure(1, weight=1)
        self.tiles_frame.grid_columnconfigure(2, weight=1)


        self.exercise_tiles = {} # Store PhotoImage references for static icons

        # Define exercises and their image paths (using config for paths)
        # Removed 'details' field for each exercise
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

    # Removed: _resize_background method
    # def _resize_background(self, event):
    #     if self.bg_image_raw:
    #         width, height = event.width, event.height
    #         if width > 0 and height > 0:
    #             resized_image = self.bg_image_raw.resize((width, height), Image.Resampling.LANCZOS)
    #             self.bg_image_tk = ImageTk.PhotoImage(resized_image)
    #             self.bg_label.config(image=self.bg_image_tk)
    #             self.bg_label.image = self.bg_image_tk


    def _load_exercise_tiles(self):
        # Clear existing tiles
        for widget in self.tiles_frame.winfo_children():
            widget.destroy()

        row_idx, col_idx = 0, 0
        tile_size = (150, 150) # Desired size for the tile images

        for exercise in self.exercises:
            try:
                # Load icon image (these are typically static, e.g., JPG/PNG)
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

    def _show_exercise_demo(self, exercise):
        """Switches to the ExerciseDemoFrame for the selected exercise, passing exercise data."""
        self.controller.show_frame("ExerciseDemoFrame", exercise_data=exercise)


class ExerciseDemoFrame(tk.Frame):
    """Frame for displaying a single exercise demo."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.current_exercise = None
        self.gif_frames = []        # To store PhotoImage objects for GIF frames
        self.current_gif_frame = 0  # Current frame index for GIF animation
        self.gif_animation_id = None # Stores the after() ID for GIF animation

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Removed: Load and set background image
        # try:
        #     self.bg_image_raw = Image.open(controller.config['exercise_demo_bg_image'])
        #     self.bg_image_tk = None # Will be set on resize
        #     self.bg_label = tk.Label(self, image=None)
        #     self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        #     self.bind("<Configure>", self._resize_background)
        # except FileNotFoundError:
        #     messagebox.showerror("Image Error", f"Background image not found: {controller.config['exercise_demo_bg_image']}")
        #     self.config(bg="#f0f0f0") # Fallback background color
        #     self.bg_image_raw = None
        # except Exception as e:
        #     messagebox.showerror("Image Error", f"Error loading background image: {e}")
        #     self.config(bg="#f0f0f0")
        #     self.bg_image_raw = None

        # Set solid grey background
        self.config(bg="grey")

        # Content frame for demo - Adjusted relwidth to be larger
        content_frame = tk.Frame(self, bg=self.controller.config['content_bg_color'], bd=5, relief="groove")
        content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        self.exercise_name_label = tk.Label(content_frame, text="", font=("Inter", 24, "bold"), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color'])
        self.exercise_name_label.pack(pady=20)

        # Adjusted demo_image_label to have a fixed size for the GIF
        self.demo_image_label = tk.Label(content_frame, image=None, bg=self.controller.config['content_bg_color'], bd=2, relief="groove")
        self.demo_image_label.pack(pady=10, expand=False) # Changed to False so text can pack below

        # Removed: Exercise Details section
        # tk.Label(content_frame, text="Details:", font=("Inter", 16, "bold"), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(pady=(10, 5))
        # self.details_text = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD, height=5, font=("Inter", 12), bd=2, relief="groove", bg="#e0e0e0")
        # self.details_text.pack(pady=5, padx=10, fill='x', expand=True) # Make it expand
        # self.details_text.config(state=tk.DISABLED) # Make it read-only

        tk.Button(content_frame, text="Back to Exercises", font=("Inter", 12), bg=self.controller.config['button_color'], fg="white",
                  command=lambda: self.controller.show_frame("ExerciseSelectionFrame"), relief="raised", bd=3, cursor="hand2", padx=10, pady=5).pack(pady=10)

    # Removed: _resize_background method
    # def _resize_background(self, event):
    #     if self.bg_image_raw:
    #         width, height = event.width, event.height
    #         if width > 0 and height > 0:
    #             resized_image = self.bg_image_raw.resize((width, height), Image.Resampling.LANCZOS)
    #             self.bg_image_tk = ImageTk.PhotoImage(resized_image)
    #             self.bg_label.config(image=self.bg_image_tk)
    #             self.bg_label.image = self.bg_image_tk

    def set_exercise(self, exercise_data):
        """Sets the exercise data for display in this frame."""
        self.current_exercise = exercise_data
        self.exercise_name_label.config(text=self.current_exercise["name"])
        
        # Removed: Update details text
        # self.details_text.config(state=tk.NORMAL)
        # self.details_text.delete(1.0, tk.END)
        # self.details_text.insert(tk.END, self.current_exercise.get("details", "No details available."))
        # self.details_text.config(state=tk.DISABLED)

        self._stop_gif_animation() # Stop any ongoing animation
        self._load_demo_image()

    def _load_demo_image(self):
        """Loads and displays the demo image for the current exercise.
        Handles both static images (JPG/PNG) and animated GIFs.
        """
        if self.current_exercise and self.current_exercise["demo"]:
            img_path = self.current_exercise["demo"]
            file_extension = os.path.splitext(img_path)[1].lower()

            try:
                if file_extension == '.gif':
                    self._start_gif_animation(img_path)
                else:
                    # Handle static image (JPG/PNG)
                    img_raw = Image.open(img_path)
                    self._display_static_image(img_raw)

            except FileNotFoundError:
                messagebox.showerror("Image Error", f"Demo image not found: {img_path}")
                self.demo_image_label.config(image=None, text="Image Not Found")
                self.demo_image_tk = None
                self.gif_display_image = None
            except Exception as e:
                messagebox.showerror("Image Error", f"Error loading demo image {img_path}: {e}")
                self.demo_image_label.config(image=None, text="Error Loading Image")
                self.demo_image_tk = None
                self.gif_display_image = None
        else:
            self.demo_image_label.config(image=None, text="No Exercise Selected")
            self.demo_image_tk = None
            self.gif_display_image = None

    def _display_static_image(self, img_raw):
        """Helper to display a single static image."""
        # Decreased max_width and max_height for the exercise demo image
        max_width = 350
        max_height = 350

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
        self.demo_image_label.config(image=self.demo_image_tk, text="") # Clear text if image is loaded
        self.demo_image_label.image = self.demo_image_tk # Keep a reference!
        self.gif_display_image = None # Ensure GIF reference is cleared

    def _start_gif_animation(self, gif_path):
        """Loads GIF frames and starts the animation."""
        self.gif_frames = []
        self.current_gif_frame = 0
        try:
            img = Image.open(gif_path)
            # Decreased max_width and max_height for the exercise demo GIF frames
            max_width = 350
            max_height = 350

            for frame in ImageSequence.Iterator(img):
                # Ensure each frame is converted to RGBA to avoid issues with paletted images
                frame = frame.convert("RGBA")
                original_width, original_height = frame.size
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

                resized_frame = frame.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.gif_frames.append(ImageTk.PhotoImage(resized_frame))

            self.demo_image_label.config(text="") # Clear text before animation
            self._animate_gif() # Start the animation loop

        except Exception as e:
            messagebox.showerror("GIF Error", f"Could not load or animate GIF: {e}")
            self.demo_image_label.config(image=None, text="GIF Error")
            self.gif_frames = []
            self.demo_image_tk = None
            self.gif_display_image = None


    def _animate_gif(self):
        """Updates the GIF frame displayed."""
        if not self.gif_frames:
            self._stop_gif_animation()
            return

        # Use a new variable for the current frame to ensure reference
        self.gif_display_image = self.gif_frames[self.current_gif_frame]
        self.demo_image_label.config(image=self.gif_display_image)
        self.demo_image_label.image = self.gif_display_image # Explicitly keep reference here

        self.current_gif_frame = (self.current_gif_frame + 1) % len(self.gif_frames)

        # Set delay to 0.5 seconds (500 milliseconds)
        delay = 500

        # Check if the label is still visible on the screen to avoid errors
        # This is a robust way to ensure we don't try to animate a destroyed widget
        if self.demo_image_label.winfo_exists():
            self.gif_animation_id = self.after(delay, self._animate_gif)
        else:
            self._stop_gif_animation() # Stop if label no longer exists

    def _stop_gif_animation(self):
        """Stops any ongoing GIF animation."""
        if self.gif_animation_id:
            self.after_cancel(self.gif_animation_id)
            self.gif_animation_id = None
        self.gif_frames = [] # Clear frames to free memory
        self.current_gif_frame = 0
        self.gif_display_image = None # Clear the current PhotoImage reference

    def on_show(self, exercise_data=None):
        """Method called when this frame is shown."""
        if exercise_data:
            self.set_exercise(exercise_data)
        else:
            # Clear previous content if no exercise data is passed (e.g., direct navigation)
            self.exercise_name_label.config(text="")
            self.demo_image_label.config(image=None, text="Select an exercise to see the demo.")
            # Removed: details_text related clearing
            # self.details_text.config(state=tk.NORMAL)
            # self.details_text.delete(1.0, tk.END)
            # self.details_text.insert(tk.END, "Details about the exercise will appear here.")
            # self.details_text.config(state=tk.DISABLED)
            self._stop_gif_animation() # Ensure animation is stopped if no data
