import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk # Used for image handling
import os
import matplotlib.pyplot as plt # Import matplotlib.pyplot as plt

# Import all custom modules
import database
import utils
from auth_page import LoginFrame, SignupFrame
from dashboard_page import DashboardFrame
from bmi_page import BMICalculatorFrame
from calorie_tracker_page import CalorieTrackerFrame
from exercise_page import ExerciseSelectionFrame, ExerciseDemoFrame
from goal_setting_page import GoalSettingFrame # New import
from progress_tracking_page import ProgressTrackingFrame # New import
from data_analysis_page import DataAnalysisFrame # New import

class FitnessApp(tk.Tk):
    """Main application class for the Fitness Tracker."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Fitness Tracker")
        self.geometry("1024x768") # Default window size
        self.minsize(800, 600) # Minimum window size

        # Configuration for colors and image paths
        # >>> IMPORTANT: PLEASE REPLACE THESE PLACEHOLDER PATHS WITH YOUR ACTUAL IMAGE FILE PATHS! <<<
        # >>> Create an 'images' folder in the same directory as your script and place your images there. <<<
        # >>> Ensure the file names and extensions (e.g., .jpg, .png, .gif) match exactly. <<<
        self.config = {
            # Colors
            "primary_color": "#4CAF50",  # Green
            "secondary_color": "#8BC34A", # Light Green
            "button_color": "#FF5722",   # Orange
            "text_color": "#333333",     # Dark Gray
            "content_bg_color": "#FFFFFF", # White background for content frames
            "tile_bg_color": "#E0F2F7",  # Light blue for exercise tiles

            # Image Paths (Replace with your actual paths relative to the script)
            # Default images (ensure these exist if used as fallbacks or for general styling)
            "default_bg_image": "images/fitness_bg.jpg", # Placeholder, ensure this file exists

            # Login/Signup Page Images - Still using specific backgrounds
            "login_bg_image": "images/login_bg.jpg",
            "signup_bg_image": "images/signup_bg.jpg",

            # Dashboard Page Image - Still using specific background
            "dashboard_bg_image": "images/dashboard_bg.jpg",

            # BMI Page Image - Still using specific background
            "bmi_bg_image": "images/bmi_bg.jpg",

            # Calorie Tracker Page Image - Now using grey background, so removed from config
            # "calorie_bg_image": "images/calorie_bg.jpg",


            # Exercise Icons (for tiles)
            # These should be smaller, square images for best results.
            "pushup_icon": "images/pushup_icon.jpg",
            "squat_icon": "images/squat_icon.jpg",
            "plank_icon": "images/plank_icon.jpg",
            "lunges_icon": "images/lunges_icon.jpg",
            "burpees_icon": "images/burpees_icon.jpg",

            # Exercise Demo Images (larger images or GIFs for the demo page)
            # Make sure these are .gif if you want animation, otherwise .jpg or .png
            "pushup_demo": "images/pushup_demo.gif", # Ensure this is a .gif for animation
            "squat_demo": "images/squat_demo.gif",   # Ensure this is a .gif for animation
            "plank_demo": "images/plank_demo.gif",   # Ensure this is a .gif for animation
            "lunges_demo": "images/lunges_demo.gif", # Ensure this is a .gif for animation
            "burpees_demo": "images/burpees_demo.gif", # Ensure this is a .gif for animation
        }

        # Ensure the 'images' directory exists
        if not os.path.exists("images"):
            os.makedirs("images")
            messagebox.showinfo("Image Directory Created", "The 'images' directory has been created. Please place your image files inside it and update the 'config' in main.py with the correct names.")

        # Initialize database
        database.create_tables()

        self.current_user_id = None
        self.current_username = None

        # Container for all frames
        self.container = tk.Frame(self, bg=self.config['primary_color'])
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # List of all frame classes
        self.frame_classes = {
            "LoginFrame": LoginFrame,
            "SignupFrame": SignupFrame,
            "DashboardFrame": DashboardFrame,
            "BMICalculatorFrame": BMICalculatorFrame,
            "CalorieTrackerFrame": CalorieTrackerFrame,
            "ExerciseSelectionFrame": ExerciseSelectionFrame,
            "ExerciseDemoFrame": ExerciseDemoFrame,
            "GoalSettingFrame": GoalSettingFrame, # New frame class
            "ProgressTrackingFrame": ProgressTrackingFrame, # New frame class
            "DataAnalysisFrame": DataAnalysisFrame # New frame class
        }

        # Create the initial LoginFrame immediately
        self.create_frame("LoginFrame")


    def create_frame(self, page_name):
        """Creates a frame if it doesn't already exist and stores it."""
        if page_name not in self.frames:
            FrameClass = self.frame_classes.get(page_name)
            if FrameClass:
                # No side image path needed for any frame now
                frame = FrameClass(parent=self.container, controller=self)
                self.frames[page_name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            else:
                messagebox.showerror("Error", f"Unknown page: {page_name}")
                return None
        return self.frames[page_name]

    def show_frame(self, page_name, **kwargs): # Added **kwargs
        """Shows a frame for the given page name, creating it if necessary.
           Passes additional kwargs to the frame's on_show method.
        """
        frame = self.create_frame(page_name)
        if frame:
            frame.tkraise()
            # If the frame has an 'on_show' method, call it with kwargs
            if hasattr(frame, 'on_show'):
                frame.on_show(**kwargs) # Pass kwargs here

    def start(self):
        """Starts the application by showing the initial frame."""
        self.show_frame("LoginFrame")

if __name__ == "__main__":
    # Ensure matplotlib is not in interactive mode to prevent extra windows
    plt.ioff()
    app = FitnessApp()
    app.start() # Call the new start method to display the initial frame
    app.mainloop()
