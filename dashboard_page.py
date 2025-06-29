import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk
import os
from scrolled_frame import ScrolledFrame # Import the custom ScrolledFrame

class DashboardFrame(tk.Frame):
    """Dashboard page frame."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Assuming this page should retain its background image if configured.
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


        # Content frame, now a ScrolledFrame
        # The content_frame itself will be placed using place, and its interior will be scrollable
        self.scrolled_content_frame = ScrolledFrame(self, bg=self.controller.config['content_bg_color'])
        self.scrolled_content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.7)

        # All existing widgets will be placed inside self.scrolled_content_frame.interior
        content_interior = self.scrolled_content_frame.interior

        self.welcome_label = tk.Label(content_interior, text="", font=("Inter", 18, "bold"), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color'])
        self.welcome_label.pack(pady=20)

        self.datetime_label = tk.Label(content_interior, text="", font=("Inter", 14), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color'])
        self.datetime_label.pack(pady=10)

        # Navigation Buttons
        button_font = ("Inter", 14, "bold")
        button_style = {"bg": controller.config['button_color'], "fg": "white", "relief": "raised", "bd": 3, "cursor": "hand2", "padx": 10, "pady": 5}

        tk.Button(content_interior, text="BMI Calculator", font=button_font, command=lambda: self.controller.show_frame("BMICalculatorFrame"), **button_style).pack(pady=10, fill='x')
        tk.Button(content_interior, text="Calorie & Exercise Tracker", font=button_font, command=lambda: self.controller.show_frame("CalorieTrackerFrame"), **button_style).pack(pady=10, fill='x')
        tk.Button(content_interior, text="Exercise Demos", font=button_font, command=lambda: self.controller.show_frame("ExerciseSelectionFrame"), **button_style).pack(pady=10, fill='x')
        
        # New Feature Buttons
        tk.Button(content_interior, text="Set & Track Goals", font=button_font, command=lambda: self.controller.show_frame("GoalSettingFrame"), **button_style).pack(pady=10, fill='x')
        tk.Button(content_interior, text="Progress Tracking", font=button_font, command=lambda: self.controller.show_frame("ProgressTrackingFrame"), **button_style).pack(pady=10, fill='x')
        tk.Button(content_interior, text="Data Analysis", font=button_font, command=lambda: self.controller.show_frame("DataAnalysisFrame"), **button_style).pack(pady=10, fill='x')

        tk.Button(content_interior, text="Logout", font=button_font, command=self._logout, **button_style).pack(pady=10, fill='x')

        self.update_datetime() # Start updating date and time

    def _resize_background(self, event):
        if self.bg_image_raw:
            width, height = event.width, event.height
            if width > 0 and height > 0:
                resized_image = self.bg_image_raw.resize((width, height), Image.Resampling.LANCZOS)
                self.bg_image_tk = ImageTk.PhotoImage(resized_image)
                self.bg_label.config(image=self.bg_image_tk)
                self.bg_label.image = self.bg_image_tk


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
