import tkinter as tk
from tkinter import messagebox, scrolledtext
import database

class DataAnalysisFrame(tk.Frame):
    """Frame for displaying insights from workout data."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Set solid grey background
        self.config(bg="grey")

        # Content frame
        content_frame = tk.Frame(self, bg=self.controller.config['content_bg_color'], bd=5, relief="groove")
        content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.8)

        tk.Label(content_frame, text="Workout Data Analysis", font=("Inter", 20, "bold"), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(pady=10)

        self.analysis_display = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD, height=20, font=("Inter", 12), bd=2, relief="groove", bg="#e0e0e0")
        self.analysis_display.pack(pady=10, padx=10, fill='both', expand=True)
        self.analysis_display.config(state=tk.DISABLED) # Make it read-only

        # Back to Dashboard button
        tk.Button(content_frame, text="Back to Dashboard", font=("Inter", 12), bg=self.controller.config['button_color'], fg="white",
                  command=lambda: self.controller.show_frame("DashboardFrame"), relief="raised", bd=3, cursor="hand2", padx=10, pady=5).pack(pady=10)

    def _perform_analysis(self):
        """Analyzes workout data and updates the display."""
        if not self.controller.current_user_id:
            self.analysis_display.config(state=tk.NORMAL)
            self.analysis_display.delete(1.0, tk.END)
            self.analysis_display.insert(tk.END, "Please log in to analyze your data.")
            self.analysis_display.config(state=tk.DISABLED)
            return

        logs = database.get_exercise_logs(self.controller.current_user_id)
        
        self.analysis_display.config(state=tk.NORMAL)
        self.analysis_display.delete(1.0, tk.END)
        self.analysis_display.insert(tk.END, "--- Workout Analysis ---\n\n")

        if not logs:
            self.analysis_display.insert(tk.END, "No workout data to analyze yet.\n")
            self.analysis_display.config(state=tk.DISABLED)
            return

        total_workouts = len(logs)
        total_calories_burned = sum(log[4] for log in logs) # calories is at index 4
        
        # Calculate average sets/reps and max weight lifted
        total_sets = sum(log[1] for log in logs)
        total_reps = sum(log[2] for log in logs)
        
        avg_sets = total_sets / total_workouts if total_workouts > 0 else 0
        avg_reps = total_reps / total_workouts if total_workouts > 0 else 0

        # Track max weight lifted per exercise
        max_weights = {}
        exercise_counts = {}
        for log in logs:
            exercise_name = log[0]
            weight_kg = log[3]
            exercise_counts[exercise_name] = exercise_counts.get(exercise_name, 0) + 1
            if weight_kg is not None:
                max_weights[exercise_name] = max(max_weights.get(exercise_name, 0), weight_kg)

        self.analysis_display.insert(tk.END, f"Total Workouts Logged: {total_workouts}\n")
        self.analysis_display.insert(tk.END, f"Total Estimated Calories Burned: {total_calories_burned} kcal\n")
        self.analysis_display.insert(tk.END, f"Average Sets per Workout: {avg_sets:.1f}\n")
        self.analysis_display.insert(tk.END, f"Average Reps per Workout: {avg_reps:.1f}\n\n")

        self.analysis_display.insert(tk.END, "Most Frequent Exercises:\n")
        sorted_exercises = sorted(exercise_counts.items(), key=lambda item: item[1], reverse=True)
        for name, count in sorted_exercises[:5]: # Show top 5
            self.analysis_display.insert(tk.END, f"- {name}: {count} workouts\n")
        self.analysis_display.insert(tk.END, "\n")
        
        self.analysis_display.insert(tk.END, "Max Weight Lifted (per exercise):\n")
        if max_weights:
            for name, max_w in max_weights.items():
                self.analysis_display.insert(tk.END, f"- {name}: {max_w:.1f} kg\n")
        else:
            self.analysis_display.insert(tk.END, "No weight data logged yet.\n")

        self.analysis_display.config(state=tk.DISABLED)

    def on_show(self):
        """Method called when this frame is shown."""
        self._perform_analysis()
