import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk # Used for image handling
import os

# Import all custom modules
import database
import utils
from auth_page import LoginFrame, SignupFrame
from dashboard_page import DashboardFrame
from bmi_page import BMICalculatorFrame
from calorie_tracker_page import CalorieTrackerFrame
from exercise_page import ExerciseSelectionFrame, ExerciseDemoFrame

class FitnessApp(tk.Tk):
    """Main application class for the Fitness Tracker."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Fitness Tracker")
        self.geometry("1024x768") # Default window size
        self.minsize(800, 600) # Minimum window size

        # Configuration for colors and image paths
        # IMPORTANT: Replace these placeholder paths with your actual image file paths!
        # Create an 'images' folder in the same directory as your script and place your images there.
        self.config = {
            # Colors
            "primary_color": "#4CAF50",  # Green
            "secondary_color": "#8BC34A", # Light Green
            "button_color": "#FF5722",   # Orange
            "text_color": "#333333",     # Dark Gray
            "content_bg_color": "#FFFFFF", # White background for content frames
            "tile_bg_color": "#E0F2F7",  # Light blue for exercise tiles

            # Image Paths (Replace with your actual paths relative to the script)
            # General placeholders - you MUST replace these!
            "default_bg_image": "images/fitness_bg.jpg", # Placeholder, ensure this file exists
            "default_side_image": "images/fitness_side.jpg", # Placeholder, ensure this file exists

            # Login/Signup Page Images
            "login_bg_image": "images/login_bg.jpg",
            "login_side_image": "images/login_side.jpg",
            "signup_bg_image": "images/signup_bg.jpg",
            "signup_side_image": "images/signup_side.jpg",

            # Dashboard Page Images
            "dashboard_bg_image": "images/dashboard_bg.jpg",
            "dashboard_side_image": "images/dashboard_side.jpg",

            # BMI Page Images
            "bmi_bg_image": "images/bmi_bg.jpg",
            "bmi_side_image": "images/bmi_side.jpg",

            # Calorie Tracker Page Images
            "calorie_bg_image": "images/calorie_bg.jpg",
            "calorie_side_image": "images/calorie_side.jpg",

            # Exercise Selection Page Images
            "exercise_selection_bg_image": "images/exercise_selection_bg.jpg",
            "exercise_selection_side_image": "images/exercise_selection_side.jpg",

            # Exercise Demo Page Images
            "exercise_demo_bg_image": "images/exercise_demo_bg.jpg",
            "exercise_demo_side_image": "images/exercise_demo_side.jpg",

            # Exercise Icons (for tiles)
            "pushup_icon": "images/pushup_icon.jpg",
            "squat_icon": "images/squat_icon.jpg",
            "plank_icon": "images/plank_icon.jpg",
            "lunges_icon": "images/lunges_icon.jpg",
            "burpees_icon": "images/burpees_icon.jpg",

            # Exercise Demo Images (larger images for demo page)
            "pushup_demo": "images/pushup_demo.jpg",
            "squat_demo": "images/squat_demo.jpg",
            "plank_demo": "images/plank_demo.jpg",
            "lunges_demo": "images/lunges_demo.jpg",
            "burpees_demo": "images/burpees_demo.jpg",
        }

        # Ensure the 'images' directory exists
        if not os.path.exists("images"):
            os.makedirs("images")
            messagebox.showinfo("Image Directory Created", "The 'images' directory has been created. Please place your image files inside it.")

        # Initialize database
        database.create_tables()

        self.current_user_id = None
        self.current_username = None

        # Container for all frames
        container = tk.Frame(self, bg=self.config['primary_color'])
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginFrame, SignupFrame, DashboardFrame, BMICalculatorFrame, CalorieTrackerFrame, ExerciseSelectionFrame, ExerciseDemoFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew") # Stack all frames on top of each other

        self.show_frame("LoginFrame") # Start with the login page

    def show_frame(self, page_name):
        """Show a frame for the given page name."""
        frame = self.frames[page_name]
        frame.tkraise()
        # If the frame has an 'on_show' method, call it
        if hasattr(frame, 'on_show'):
            frame.on_show()

if __name__ == "__main__":
    app = FitnessApp()
    app.mainloop()
