import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk
import os

class DashboardFrame(tk.Frame):
    """Dashboard page frame."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Load and set background image
        try:
            self.bg_image_raw = Image.open(controller.config['dashboard_bg_image'])
            self.bg_image_tk = None # Will be set on resize
            self.bg_label = tk.Label(self, image=None)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bind("<Configure>", self._resize_background)
        except FileNotFoundError:
            messagebox.showerror("Image Error", f"Background image not found: {controller.config['dashboard_bg_image']}")
            self.config(bg="#f0f0f0") # Fallback background color
            self.bg_image_raw = None
        except Exception as e:
            messagebox.showerror("Image Error", f"Error loading background image: {e}")
            self.config(bg="#f0f0f0")
            self.bg_image_raw = None

        # Load and set side image
        try:
            self.side_image_raw = Image.open(controller.config['dashboard_side_image'])
            self.side_image_tk = None # Will be set on resize
            self.side_label = tk.Label(self, image=None, bg=self.controller.config['content_bg_color'])
            self.side_label.place(relx=0.02, rely=0.1, relwidth=0.2, relheight=0.8) # Position on left
            self.bind("<Configure>", self._resize_side_image)
        except FileNotFoundError:
            messagebox.showerror("Image Error", f"Side image not found: {controller.config['dashboard_side_image']}")
            self.side_image_raw = None
        except Exception as e:
            messagebox.showerror("Image Error", f"Error loading side image: {e}")
            self.side_image_raw = None

        # Content frame
        content_frame = tk.Frame(self, bg=self.controller.config['content_bg_color'], bd=5, relief="groove")
        content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.4, relheight=0.6)

        self.welcome_label = tk.Label(content_frame, text="", font=("Inter", 18, "bold"), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color'])
        self.welcome_label.pack(pady=20)

        self.datetime_label = tk.Label(content_frame, text="", font=("Inter", 14), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color'])
        self.datetime_label.pack(pady=10)

        # Navigation Buttons
        button_font = ("Inter", 14, "bold")
        button_style = {"bg": controller.config['button_color'], "fg": "white", "relief": "raised", "bd": 3, "cursor": "hand2", "padx": 10, "pady": 5}

        tk.Button(content_frame, text="BMI Calculator", font=button_font, command=lambda: self.controller.show_frame("BMICalculatorFrame"), **button_style).pack(pady=10, fill='x')
        tk.Button(content_frame, text="Calorie & Exercise Tracker", font=button_font, command=lambda: self.controller.show_frame("CalorieTrackerFrame"), **button_style).pack(pady=10, fill='x')
        tk.Button(content_frame, text="Exercise Demos", font=button_font, command=lambda: self.controller.show_frame("ExerciseSelectionFrame"), **button_style).pack(pady=10, fill='x')
        tk.Button(content_frame, text="Logout", font=button_font, command=self._logout, **button_style).pack(pady=10, fill='x')

        self.update_datetime() # Start updating date and time

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

    def update_datetime(self):
        """Updates the current date and time displayed on the dashboard."""
        now = datetime.now()
        formatted_datetime = now.strftime("%A, %B %d, %Y\n%H:%M:%S")
        self.datetime_label.config(text=formatted_datetime)
        self.after(1000, self.update_datetime) # Update every 1 second

    def _logout(self):
        """Logs out the current user and returns to the login page."""
        self.controller.current_user_id = None
        self.controller.current_username = None
        messagebox.showinfo("Logout", "You have been logged out.")
        self.controller.show_frame("LoginFrame")

    def on_show(self):
        """Method called when the dashboard frame is shown."""
        if self.controller.current_username:
            self.welcome_label.config(text=f"Welcome, {self.controller.current_username}!")
        else:
            self.welcome_label.config(text="Welcome!")
        self.update_datetime() # Ensure datetime is updating
