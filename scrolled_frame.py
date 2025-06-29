import tkinter as tk
from tkinter import ttk # For themed widgets (optional but good practice for scrollbar)

class ScrolledFrame(tk.Frame):
    """
    A custom Tkinter frame with a vertical scrollbar.
    It allows content to be placed inside a scrollable area.
    """
    def __init__(self, parent, *args, **kw):
        super().__init__(parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for that canvas
        self.canvas = tk.Canvas(self, borderwidth=0, background=self["bg"])
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create a frame inside the canvas to contain the actual content
        self.interior = tk.Frame(self.canvas, background=self["bg"])
        self.canvas.create_window((0, 0), window=self.interior, anchor="nw")

        # Bind the canvas to the scrollbar and the content frame to update scrollregion
        self.interior.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.bind("<Configure>", self._on_resize) # Bind parent frame resize

        # Bind mouse wheel for scrolling (Windows/Linux)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        # Bind mouse wheel for scrolling (macOS)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_mac)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_mac)

    def _on_frame_configure(self, event=None):
        """Update the scrollregion when the interior frame's size changes."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event=None):
        """Update interior frame's width to match canvas width when canvas resizes."""
        # This ensures that horizontal scrolling is not needed for the content
        # unless content specifically overflows horizontally.
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas.create_window((0,0), window=self.interior, anchor="nw", width=canvas_width), width=canvas_width)

    def _on_resize(self, event):
        """Resize the canvas to match the parent frame's size."""
        self.canvas.config(width=event.width, height=event.height)

    def _on_mousewheel(self, event):
        """Handles mouse wheel scrolling for Windows/Linux."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_mousewheel_mac(self, event):
        """Handles mouse wheel scrolling for macOS."""
        if event.num == 4: # Scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5: # Scroll down
            self.canvas.yview_scroll(1, "units")
