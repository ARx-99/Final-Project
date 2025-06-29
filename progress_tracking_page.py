import tkinter as tk
from tkinter import messagebox
import database
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from datetime import datetime # Import datetime
from scrolled_frame import ScrolledFrame # Import the custom ScrolledFrame

class ProgressTrackingFrame(tk.Frame):
    """Frame for tracking fitness progress with charts."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Set solid grey background
        self.config(bg="grey")

        # Content frame, now a ScrolledFrame
        self.scrolled_content_frame = ScrolledFrame(self, bg=self.controller.config['content_bg_color'])
        self.scrolled_content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.9)

        # All existing widgets will be placed inside self.scrolled_content_frame.interior
        content_interior = self.scrolled_content_frame.interior

        tk.Label(content_interior, text="Progress Tracking", font=("Inter", 20, "bold"), bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(pady=10)

        # Frame for chart options
        chart_options_frame = tk.Frame(content_interior, bg=self.controller.config['content_bg_color'])
        chart_options_frame.pack(pady=5, fill='x')

        tk.Label(chart_options_frame, text="Select Chart:", bg=self.controller.config['content_bg_color'], fg=self.controller.config['text_color']).pack(side=tk.LEFT, padx=5)
        self.chart_type_var = tk.StringVar(self)
        self.chart_type_var.set("Calories Burned") # Default value
        chart_choices = ["Calories Burned", "Sets Completed", "Reps Completed", "Weight Lifted"]
        chart_option_menu = tk.OptionMenu(chart_options_frame, self.chart_type_var, *chart_choices, command=self._update_chart)
        chart_option_menu.config(font=("Inter", 10), bg=self.controller.config['button_color'], fg="white")
        chart_option_menu.pack(side=tk.LEFT, padx=5)

        # Matplotlib figure and canvas
        self.figure = plt.Figure(figsize=(7, 5), dpi=100, facecolor=self.controller.config['content_bg_color'])
        self.ax = self.figure.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=content_interior) # Master is now content_interior
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

        # Toolbar for chart navigation (zoom, pan, etc.)
        self.toolbar = NavigationToolbar2Tk(self.canvas, content_interior) # Master is now content_interior
        self.toolbar.update()
        
        # Back to Dashboard button
        tk.Button(content_interior, text="Back to Dashboard", font=("Inter", 12), bg=self.controller.config['button_color'], fg="white",
                  command=lambda: self.controller.show_frame("DashboardFrame"), relief="raised", bd=3, cursor="hand2", padx=10, pady=5).pack(pady=10)

    def _update_chart(self, *args):
        """Updates the chart based on the selected type."""
        if not self.controller.current_user_id:
            self.ax.clear()
            self.ax.text(0.5, 0.5, "Please log in to view progress.", horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes)
            self.canvas.draw()
            return

        logs = database.get_exercise_logs(self.controller.current_user_id)
        
        # Clear existing plot
        self.ax.clear()

        chart_type = self.chart_type_var.get()

        if not logs:
            self.ax.text(0.5, 0.5, "No exercise data available.", horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes)
        else:
            # Ensure dates are parsed correctly
            dates = []
            # Make sure we handle potential parsing errors or missing data gracefully
            for log in logs:
                try:
                    dates.append(datetime.strptime(log[5], "%Y-%m-%d %H:%M:%S"))
                except (ValueError, IndexError):
                    # Handle cases where log[5] is missing or malformed
                    continue
            
            # If no valid dates, display message
            if not dates:
                self.ax.text(0.5, 0.5, "No valid date data in logs.", horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes)
                self.canvas.draw()
                return

            dates.sort() # Ensure dates are sorted for chronological display

            if chart_type == "Calories Burned":
                data = [log[4] for log in logs if len(log) > 4] # calories is at index 4
                # Align data with sorted dates for proper plotting
                data_dict = {datetime.strptime(log[5], "%Y-%m-%d %H:%M:%S"): log[4] for log in logs if len(log) > 5 and log[4] is not None}
                plot_data = [data_dict.get(d) for d in dates] # Get data points aligned with sorted dates
                
                self.ax.plot(dates, plot_data, marker='o', linestyle='-', color='red')
                self.ax.set_ylabel("Calories Burned")
                self.ax.set_title("Calories Burned Over Time")
            elif chart_type == "Sets Completed":
                data = [log[1] for log in logs if len(log) > 1] # sets is at index 1
                data_dict = {datetime.strptime(log[5], "%Y-%m-%d %H:%M:%S"): log[1] for log in logs if len(log) > 5 and log[1] is not None}
                plot_data = [data_dict.get(d) for d in dates]
                
                self.ax.plot(dates, plot_data, marker='o', linestyle='-', color='blue')
                self.ax.set_ylabel("Sets")
                self.ax.set_title("Sets Completed Over Time")
            elif chart_type == "Reps Completed":
                data = [log[2] for log in logs if len(log) > 2] # reps is at index 2
                data_dict = {datetime.strptime(log[5], "%Y-%m-%d %H:%M:%S"): log[2] for log in logs if len(log) > 5 and log[2] is not None}
                plot_data = [data_dict.get(d) for d in dates]
                
                self.ax.plot(dates, plot_data, marker='o', linestyle='-', color='green')
                self.ax.set_ylabel("Repetitions")
                self.ax.set_title("Repetitions Completed Over Time")
            elif chart_type == "Weight Lifted":
                # Filter logs to only include entries with weight
                weighted_logs = [(datetime.strptime(log[5], "%Y-%m-%d %H:%M:%S"), log[3]) for log in logs if len(log) > 3 and log[3] is not None]
                if weighted_logs:
                    weighted_logs.sort(key=lambda x: x[0]) # Sort by date
                    dates_weighted = [item[0] for item in weighted_logs]
                    weights = [item[1] for item in weighted_logs]
                    self.ax.plot(dates_weighted, weights, marker='o', linestyle='-', color='purple')
                    self.ax.set_ylabel("Weight (kg)")
                    self.ax.set_title("Weight Lifted Over Time")
                else:
                    self.ax.text(0.5, 0.5, "No weight data available.", horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes)

        self.figure.autofmt_xdate() # Rotate x-axis labels for better readability
        self.canvas.draw()

    def on_show(self):
        """Method called when this frame is shown."""
        # Ensure chart is updated when the frame becomes visible
        self._update_chart()
