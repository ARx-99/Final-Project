import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime
from PIL import Image, ImageTk
import database
import os

class CalorieTrackerFrame(tk.Frame):
    """Calorie and Exercise Tracker page frame."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Load and set background image
        try:
            self.bg_image_raw = Image.open(controller.config['calorie_bg_image'])
            self.bg_image_tk = None # Will be set on resize
            self.bg_label = tk.Label(self, image=None)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bind("<Configure>", self._resize_background)
        except FileNotFoundError:
            messagebox.showerror("Image Error", f"Background image not found: {controller.config['calorie_bg_image']}")
            self.config(bg="#f0f0f0") # Fallback background color
            self.bg_image_raw = None
        except Exception as e:
            messagebox.showerror("Image Error", f"Error loading background image: {e}")
            self.config(bg="#f0f0f0")
            self.bg_image_raw = None

        # Load and set side image
        try:
            self.side_image_raw = Image.open(controller.config['calorie_side_image'])
            self.side_image_tk = None # Will be set on resize
            self.side_label = tk.Label(self, image=None, bg=self.controller.config['content_bg_color'])
            self.side_label.place(relx=0.02, rely=0.1, relwidth=0.2, relheight=0.8) # Position on left
            self.bind("<Configure>", self._resize_side_image)
        except FileNotFoundError:
            messagebox.showerror("Image Error", f"Side image not found: {controller.config['calorie_side_image']}")
            self.side_image_raw = None
        except Exception as e:
            messagebox.showerror("Image Error", f"Error loading side image: {e}")
            self.side_image_raw = None

        # Content frame
        content_frame = tk.Frame(self, bg=self.controller.config['content_bg_color'], bd=5, relief="groove")
        content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.4, relheight=0.8)

        tk.Label(content_frame, text="Log Exercise", font=("Inter", 20, "bold"), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(pady=10)

        # Input fields
        tk.Label(content_frame, text="Exercise Name:", font=("Inter", 12), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(pady=2)
        self.exercise_name_entry = tk.Entry(content_frame, font=("Inter", 12), bd=2, relief="groove")
        self.exercise_name_entry.pack(pady=2)

        tk.Label(content_frame, text="Sets:", font=("Inter", 12), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(pady=2)
        self.sets_entry = tk.Entry(content_frame, font=("Inter", 12), bd=2, relief="groove")
        self.sets_entry.pack(pady=2)

        tk.Label(content_frame, text="Repetitions:", font=("Inter", 12), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(pady=2)
        self.reps_entry = tk.Entry(content_frame, font=("Inter", 12), bd=2, relief="groove")
        self.reps_entry.pack(pady=2)

        tk.Label(content_frame, text="Estimated Calories Burned:", font=("Inter", 12), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(pady=2)
        self.calories_entry = tk.Entry(content_frame, font=("Inter", 12), bd=2, relief="groove")
        self.calories_entry.pack(pady=2)

        tk.Button(content_frame, text="Log Exercise", font=("Inter", 12, "bold"), bg=self.controller.config['button_color'], fg="white",
                  command=self._log_exercise, relief="raised", bd=3, cursor="hand2", padx=10, pady=5).pack(pady=10)

        # Exercise Log Display
        tk.Label(content_frame, text="My Exercise Log:", font=("Inter", 16, "bold"), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(pady=10)
        self.log_display = scrolledtext.ScrolledText(content_frame, width=40, height=5, font=("Inter", 10), bd=2, relief="groove", bg="#e0e0e0")
        self.log_display.pack(pady=5)
        self.log_display.config(state=tk.DISABLED) # Make it read-only

        # Back to Dashboard button added
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

    def _log_exercise(self):
        if not self.controller.current_user_id:
            messagebox.showerror("Error", "Please log in to log exercises.")
            self.controller.show_frame("LoginFrame")
            return

        exercise_name = self.exercise_name_entry.get().strip()
        sets_str = self.sets_entry.get().strip()
        reps_str = self.reps_entry.get().strip()
        calories_str = self.calories_entry.get().strip()
        log_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not exercise_name:
            messagebox.showerror("Input Error", "Please enter an exercise name.")
            return

        try:
            sets = int(sets_str)
            reps = int(reps_str)
            calories = int(calories_str)
            if sets <= 0 or reps <= 0 or calories <= 0:
                messagebox.showerror("Input Error", "Sets, Repetitions, and Calories must be positive integers.")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for Sets, Repetitions, and Calories.")
            return

        if database.log_exercise(self.controller.current_user_id, exercise_name, sets, reps, calories, log_date):
            messagebox.showinfo("Success", "Exercise logged successfully!")
            self._clear_entries()
            self._load_exercise_logs() # Refresh the log display
        else:
            messagebox.showerror("Error", "Failed to log exercise. Please try again.")

    def _clear_entries(self):
        self.exercise_name_entry.delete(0, tk.END)
        self.sets_entry.delete(0, tk.END)
        self.reps_entry.delete(0, tk.END)
        self.calories_entry.delete(0, tk.END)

    def _load_exercise_logs(self):
        """Loads and displays exercise logs for the current user."""
        if not self.controller.current_user_id:
            self.log_display.config(state=tk.NORMAL)
            self.log_display.delete(1.0, tk.END)
            self.log_display.insert(tk.END, "Please log in to view your exercise history.")
            self.log_display.config(state=tk.DISABLED)
            return

        logs = database.get_exercise_logs(self.controller.current_user_id)
        self.log_display.config(state=tk.NORMAL) # Enable for editing
        self.log_display.delete(1.0, tk.END) # Clear previous content

        if logs:
            self.log_display.insert(tk.END, "Date/Time             Exercise          Sets Reps Calories\n")
            self.log_display.insert(tk.END, "-------------------------------------------------------\n")
            for log in logs:
                exercise_name, sets, reps, calories, log_date = log
                self.log_display.insert(tk.END, f"{log_date:20s} {exercise_name:15s} {sets:^4d} {reps:^4d} {calories:^8d}\n")
        else:
            self.log_display.insert(tk.END, "No exercise logs found yet.")

        self.log_display.config(state=tk.DISABLED) # Disable after editing

    def on_show(self):
        """Method called when this frame is shown."""
        self._load_exercise_logs()
