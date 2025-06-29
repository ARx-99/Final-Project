import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import database
import utils
import os

class AuthFrame(tk.Frame):
    """Base class for authentication frames, handling common elements like background/side images."""
    def __init__(self, parent, controller, bg_image_path): # Removed side_image_path
        super().__init__(parent)
        self.controller = controller

        # Load and set background image
        try:
            self.bg_image_raw = Image.open(bg_image_path)
            self.bg_image_tk = None # Will be set on resize
            self.bg_label = tk.Label(self, image=None)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bind("<Configure>", self._resize_background)
        except FileNotFoundError:
            messagebox.showerror("Image Error", f"Background image not found: {bg_image_path}")
            self.config(bg="#f0f0f0") # Fallback background color
            self.bg_image_raw = None
        except Exception as e:
            messagebox.showerror("Image Error", f"Error loading background image: {e}")
            self.config(bg="#f0f0f0")
            self.bg_image_raw = None

        # Removed: Load and set side image
        # try:
        #     self.side_image_raw = Image.open(side_image_path)
        #     self.side_image_tk = None # Will be set on resize
        #     self.side_label = tk.Label(self, image=None, bg="#e0e0e0") # Set a temporary background for the label
        #     self.side_label.place(relx=0.02, rely=0.1, relwidth=0.2, relheight=0.8) # Position on left
        #     self.bind("<Configure>", self._resize_side_image)
        # except FileNotFoundError:
        #     messagebox.showerror("Image Error", f"Side image not found: {side_image_path}")
        #     self.side_image_raw = None
        # except Exception as e:
        #     messagebox.showerror("Image Error", f"Error loading side image: {e}")
        #     self.side_image_raw = None

        # Placeholder for content frame to ensure it's on top of images
        # Adjusted relwidth to be larger since side image is removed
        self.content_frame = tk.Frame(self, bg=self.controller.config['content_bg_color'], bd=5, relief="groove")
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.6) # Increased width


    def _resize_background(self, event):
        if self.bg_image_raw:
            # Resize image to fit window dimensions while maintaining aspect ratio
            width, height = event.width, event.height
            if width > 0 and height > 0:
                resized_image = self.bg_image_raw.resize((width, height), Image.Resampling.LANCZOS)
                self.bg_image_tk = ImageTk.PhotoImage(resized_image)
                self.bg_label.config(image=self.bg_image_tk)
                self.bg_label.image = self.bg_image_tk # Keep a reference!

    # Removed: def _resize_side_image(self, event):
    #     if self.side_image_raw:
    #         frame_width = self.side_label.winfo_width() # Get current width of the side_label
    #         frame_height = self.side_label.winfo_height() # Get current height of the side_label
    #
    #         if frame_width > 0 and frame_height > 0:
    #             resized_image = self.side_image_raw.resize((frame_width, frame_height), Image.Resampling.LANCZOS)
    #             self.side_image_tk = ImageTk.PhotoImage(resized_image)
    #             self.side_label.config(image=self.side_image_tk)
    #             self.side_label.image = self.side_image_tk # Keep a reference!


class LoginFrame(AuthFrame):
    """Login page frame."""
    def __init__(self, parent, controller):
        super().__init__(parent, controller, controller.config['login_bg_image']) # Removed side image path
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Content frame for login elements
        login_frame = self.content_frame

        tk.Label(login_frame, text="LOGIN", font=("Inter", 24, "bold"), bg=controller.config['content_bg_color'], fg=controller.config['text_color']).pack(pady=20)

        tk.Label(login_frame, text="Username:", font=("Inter", 12), bg=controller.config['content_bg_color'], fg=controller.config['text_color']).pack(pady=5)
        self.username_entry = tk.Entry(login_frame, font=("Inter", 12), bd=2, relief="groove")
        self.username_entry.pack(pady=5)

        tk.Label(login_frame, text="Password:", font=("Inter", 12), bg=controller.config['content_bg_color'], fg=controller.config['text_color']).pack(pady=5)
        self.password_entry = tk.Entry(login_frame, show="*", font=("Inter", 12), bd=2, relief="groove")
        self.password_entry.pack(pady=5)

        tk.Button(login_frame, text="Login", font=("Inter", 12, "bold"), bg=controller.config['button_color'], fg="white",
                  command=self._login, relief="raised", bd=3, cursor="hand2", padx=10, pady=5).pack(pady=10)

        tk.Button(login_frame, text="Don't have an account? Sign Up", font=("Inter", 10), bg=controller.config['content_bg_color'], fg=controller.config['text_color'],
                  command=lambda: self.controller.show_frame("SignupFrame"), relief="flat", cursor="hand2").pack(pady=5)

    def _login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Login Error", "Please enter both username and password.")
            return

        user_data = database.get_user(username)
        if user_data and utils.check_password(user_data[2], password): # user_data[2] is password_hash
            self.controller.current_user_id = user_data[0] # Store user ID
            self.controller.current_username = user_data[1] # Store username
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            self.controller.show_frame("DashboardFrame")
            # Clear fields after successful login
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")

class SignupFrame(AuthFrame):
    """Signup page frame."""
    def __init__(self, parent, controller):
        super().__init__(parent, controller, controller.config['signup_bg_image']) # Removed side image path
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Content frame for signup elements
        signup_frame = self.content_frame

        tk.Label(signup_frame, text="SIGN UP", font=("Inter", 24, "bold"), bg=controller.config['content_bg_color'], fg=controller.config['text_color']).pack(pady=20)

        tk.Label(signup_frame, text="Username:", font=("Inter", 12), bg=controller.config['content_bg_color'], fg=controller.config['text_color']).pack(pady=5)
        self.username_entry = tk.Entry(signup_frame, font=("Inter", 12), bd=2, relief="groove")
        self.username_entry.pack(pady=5)

        tk.Label(signup_frame, text="Password:", font=("Inter", 12), bg=controller.config['content_bg_color'], fg=controller.config['text_color']).pack(pady=5)
        self.password_entry = tk.Entry(signup_frame, show="*", font=("Inter", 12), bd=2, relief="groove")
        self.password_entry.pack(pady=5)

        tk.Button(signup_frame, text="Sign Up", font=("Inter", 12, "bold"), bg=controller.config['button_color'], fg="white",
                  command=self._signup, relief="raised", bd=3, cursor="hand2", padx=10, pady=5).pack(pady=10)

        tk.Button(signup_frame, text="Already have an account? Login", font=("Inter", 10), bg=controller.config['content_bg_color'], fg=controller.config['text_color'],
                  command=lambda: self.controller.show_frame("LoginFrame"), relief="flat", cursor="hand2").pack(pady=5)

        # --- Added Back Button ---
        tk.Button(signup_frame, text="Back", font=("Inter", 10), bg=controller.config['button_color'], fg="white",
                  command=lambda: self.controller.show_frame("LoginFrame"), relief="raised", bd=3, cursor="hand2", padx=10, pady=5).pack(pady=5)
        # --- End Back Button ---

    def _signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Signup Error", "Please enter both username and password.")
            return

        if database.add_user(username, utils.hash_password(password)):
            messagebox.showinfo("Signup Success", "Account created successfully! Please log in.")
            self.controller.show_frame("LoginFrame")
            # Clear fields after successful signup
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Signup Error", "Username already exists. Please choose a different one.")
