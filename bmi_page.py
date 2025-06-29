import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class BMICalculatorFrame(tk.Frame):
    """BMI Calculator page frame."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Load and set background image
        try:
            self.bg_image_raw = Image.open(controller.config['bmi_bg_image'])
            self.bg_image_tk = None # Will be set on resize
            self.bg_label = tk.Label(self, image=None)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bind("<Configure>", self._resize_background)
        except FileNotFoundError:
            messagebox.showerror("Image Error", f"Background image not found: {controller.config['bmi_bg_image']}")
            self.config(bg="#f0f0f0") # Fallback background color
            self.bg_image_raw = None
        except Exception as e:
            messagebox.showerror("Image Error", f"Error loading background image: {e}")
            self.config(bg="#f0f0f0")
            self.bg_image_raw = None

        # Removed: Load and set side image
        # try:
        #     self.side_image_raw = Image.open(controller.config['bmi_side_image'])
        #     self.side_image_tk = None # Will be set on resize
        #     self.side_label = tk.Label(self, image=None, bg=self.controller.config['content_bg_color'])
        #     self.side_label.place(relx=0.02, rely=0.1, relwidth=0.2, relheight=0.8) # Position on left
        #     self.bind("<Configure>", self._resize_side_image)
        # except FileNotFoundError:
        #     messagebox.showerror("Image Error", f"Side image not found: {controller.config['bmi_side_image']}")
        #     self.side_image_raw = None
        # except Exception as e:
        #     messagebox.showerror("Image Error", f"Error loading side image: {e}")
        #     self.side_image_raw = None

        # Content frame - Adjusted relwidth to be larger
        content_frame = tk.Frame(self, bg=self.controller.config['content_bg_color'], bd=5, relief="groove")
        content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.6)


        tk.Label(content_frame, text="BMI Calculator", font=("Inter", 20, "bold"), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(pady=20)

        tk.Label(content_frame, text="Weight (kg):", font=("Inter", 12), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(pady=5)
        self.weight_entry = tk.Entry(content_frame, font=("Inter", 12), bd=2, relief="groove")
        self.weight_entry.pack(pady=5)

        tk.Label(content_frame, text="Height (cm):", font=("Inter", 12), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(pady=5)
        self.height_entry = tk.Entry(content_frame, font=("Inter", 12), bd=2, relief="groove")
        self.height_entry.pack(pady=5)

        tk.Button(content_frame, text="Calculate BMI", font=("Inter", 12, "bold"), bg=self.controller.config['button_color'], fg="white",
                  command=self._calculate_bmi, relief="raised", bd=3, cursor="hand2", padx=10, pady=5).pack(pady=15)

        self.result_label = tk.Label(content_frame, text="Your BMI: ", font=("Inter", 14), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color'])
        self.result_label.pack(pady=10)

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

    # Removed: def _resize_side_image(self, event):
    #     if self.side_image_raw:
    #         frame_width = self.side_label.winfo_width()
    #         frame_height = self.side_label.winfo_height()
    #         if frame_width > 0 and frame_height > 0:
    #             resized_image = self.side_image_raw.resize((frame_width, frame_height), Image.Resampling.LANCZOS)
    #             self.side_image_tk = ImageTk.PhotoImage(resized_image)
    #             self.side_label.config(image=self.side_image_tk)
    #             self.side_label.image = self.side_image_tk

    def _calculate_bmi(self):
        try:
            weight_kg = float(self.weight_entry.get())
            height_cm = float(self.height_entry.get())

            if weight_kg <= 0 or height_cm <= 0:
                messagebox.showerror("Input Error", "Weight and Height must be positive numbers.")
                return

            height_m = height_cm / 100
            bmi = weight_kg / (height_m ** 2)
            bmi_category = self._get_bmi_category(bmi)

            self.result_label.config(text=f"Your BMI: {bmi:.2f}\nCategory: {bmi_category}", fg=self._get_category_color(bmi_category))

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values for Weight and Height.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def _get_bmi_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    def _get_category_color(self, category):
        colors = {
            "Underweight": "orange",
            "Normal weight": "green",
            "Overweight": "red",
            "Obese": "darkred"
        }
        return colors.get(category, "black")
