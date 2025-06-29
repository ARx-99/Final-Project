import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime
from PIL import Image, ImageTk
import database
import os
from scrolled_frame import ScrolledFrame # Import the custom ScrolledFrame

class CalorieTrackerFrame(tk.Frame):
    """Calorie and Exercise Tracker page frame."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Set solid grey background as per request
        self.config(bg="grey")


        # Content frame, now a ScrolledFrame
        self.scrolled_content_frame = ScrolledFrame(self, bg=self.controller.config['content_bg_color'])
        self.scrolled_content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.8)

        # All existing widgets will be placed inside self.scrolled_content_frame.interior
        content_interior = self.scrolled_content_frame.interior

        tk.Label(content_interior, text="Log Exercise", font=("Inter", 20, "bold"), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(pady=10)

        # Input fields
        tk.Label(content_interior, text="Exercise Name:", font=("Inter", 12), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(pady=2)
        self.exercise_name_entry = tk.Entry(content_interior, font=("Inter", 12), bd=2, relief="groove")
        self.exercise_name_entry.pack(pady=2)

        tk.Label(content_interior, text="Sets:", font=("Inter", 12), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(pady=2)
        self.sets_entry = tk.Entry(content_interior, font=("Inter", 12), bd=2, relief="groove")
        self.sets_entry.pack(pady=2)

        tk.Label(content_interior, text="Repetitions:", font=("Inter", 12), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(pady=2)
        self.reps_entry = tk.Entry(content_interior, font=("Inter", 12), bd=2, relief="groove")
        self.reps_entry.pack(pady=2)
        
        # New: Weight input field
        tk.Label(content_interior, text="Weight (kg) (optional):", font=("Inter", 12), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(pady=2)
        self.weight_entry = tk.Entry(content_interior, font=("Inter", 12), bd=2, relief="groove")
        self.weight_entry.pack(pady=2)

        tk.Label(content_interior, text="Estimated Calories Burned:", font=("Inter", 12), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(pady=2)
        self.calories_entry = tk.Entry(content_interior, font=("Inter", 12), bd=2, relief="groove")
        self.calories_entry.pack(pady=2)

        tk.Button(content_interior, text="Log Exercise", font=("Inter", 12, "bold"), bg=self.controller.config['button_color'], fg="white",
                  command=self._log_exercise, relief="raised", bd=3, cursor="hand2", padx=10, pady=5).pack(pady=10)

        # Exercise Log Display
        tk.Label(content_interior, text="My Exercise Log:", font=("Inter", 16, "bold"), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(pady=10)
        self.log_display = scrolledtext.ScrolledText(content_interior, width=50, height=10, font=("Inter", 10), bd=2, relief="groove", bg="#e0e0e0") # Increased width
        self.log_display.pack(pady=5)
        self.log_display.config(state=tk.DISABLED) # Make it read-only

        # Back to Dashboard button added
        tk.Button(content_interior, text="Back to Dashboard", font=("Inter", 12), bg=self.controller.config['button_color'], fg="white",
                  command=lambda: self.controller.show_frame("DashboardFrame"), relief="raised", bd=3, cursor="hand2", padx=10, pady=5).pack(pady=10)


    def _log_exercise(self):
        if not self.controller.current_user_id:
            messagebox.showerror("Error", "Please log in to log exercises.")
            self.controller.show_frame("LoginFrame")
            return

        exercise_name = self.exercise_name_entry.get().strip()
        sets_str = self.sets_entry.get().strip()
        reps_str = self.reps_entry.get().strip()
        weight_str = self.weight_entry.get().strip() # Get weight string
        calories_str = self.calories_entry.get().strip()
        log_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not exercise_name:
            messagebox.showerror("Input Error", "Please enter an exercise name.")
            return

        try:
            sets = int(sets_str)
            reps = int(reps_str)
            calories = int(calories_str)
            weight_kg = float(weight_str) if weight_str else None # Convert to float, or None if empty

            if sets <= 0 or reps <= 0 or calories <= 0:
                messagebox.showerror("Input Error", "Sets, Repetitions, and Calories must be positive integers.")
                return
            if weight_kg is not None and weight_kg <= 0:
                messagebox.showerror("Input Error", "Weight must be a positive number or left empty.")
                return

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for Sets, Repetitions, Weight, and Calories.")
            return

        # Pass weight_kg to database function
        if database.log_exercise(self.controller.current_user_id, exercise_name, sets, reps, weight_kg, calories, log_date):
            messagebox.showinfo("Success", "Exercise logged successfully!")
            self._clear_entries()
            self._load_exercise_logs() # Refresh the log display
        else:
            messagebox.showerror("Error", "Failed to log exercise. Please try again.")

    def _clear_entries(self):
        self.exercise_name_entry.delete(0, tk.END)
        self.sets_entry.delete(0, tk.END)
        self.reps_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END) # Clear weight entry
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
            self.log_display.insert(tk.END, "Date/Time             Exercise          Sets Reps Weight Calories\n") # Updated header
            self.log_display.insert(tk.END, "------------------------------------------------------------------\n") # Adjusted underline
            for log in logs:
                exercise_name, sets, reps, weight_kg, calories, log_date = log # Unpack weight_kg
                weight_display = f"{weight_kg:.1f}" if weight_kg is not None else "N/A" # Format weight or show N/A
                self.log_display.insert(tk.END, f"{log_date:20s} {exercise_name:15s} {sets:^4d} {reps:^4d} {weight_display:^6s} {calories:^8d}\n") # Updated format
        else:
            self.log_display.insert(tk.END, "No exercise logs found yet.")

        self.log_display.config(state=tk.DISABLED) # Disable after editing

    def on_show(self):
        """Method called when this frame is shown."""
        self._load_exercise_logs()
