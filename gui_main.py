# file: gui_main.py
# This file creates the graphical user interface for the application.

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from organizer.operations import organize_folder
import threading

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("File Organizer")
        self.geometry("500x250")
        self.resizable(False, False)

        # --- Style Configuration ---
        style = ttk.Style(self)
        style.configure("TButton", font=("Helvetica", 10))
        style.configure("TLabel", font=("Helvetica", 10))

        # --- State Variables ---
        self.folder_path = tk.StringVar()

        # --- UI Layout ---
        self.create_widgets()

    def create_widgets(self):
        """Creates and places the widgets in the main window."""
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill="both")

        # --- Folder Selection ---
        select_frame = ttk.Frame(main_frame)
        select_frame.pack(fill="x", pady=10)

        path_label = ttk.Label(select_frame, text="Folder to Organize:")
        path_label.pack(side="left")

        self.select_button = ttk.Button(select_frame, text="Select Folder...", command=self.select_folder)
        self.select_button.pack(side="right")

        path_display = ttk.Entry(main_frame, textvariable=self.folder_path, state="readonly", width=60)
        path_display.pack(fill="x", pady=5)

        # --- Action Button ---
        self.organize_button = ttk.Button(main_frame, text="Organize Files", command=self.start_organization_thread)
        self.organize_button.pack(pady=20, ipady=5)
        
        # --- Status Label ---
        self.status_label = ttk.Label(main_frame, text="Please select a folder to begin.")
        self.status_label.pack(pady=10)


    def select_folder(self):
        """Opens a dialog to select a folder and updates the path variable."""
        path = filedialog.askdirectory(title="Select a Folder")
        if path:
            self.folder_path.set(path)
            self.status_label.config(text=f"Ready to organize.")

    def start_organization_thread(self):
        """
        Starts the file organization in a separate thread to keep the GUI responsive.
        """
        path = self.folder_path.get()
        if not path:
            messagebox.showwarning("Warning", "Please select a folder first.")
            return

        # Disable buttons to prevent multiple clicks
        self.organize_button.config(state="disabled")
        self.select_button.config(state="disabled")
        self.status_label.config(text="Organizing... Please wait.")

        # Run the potentially long-running task in a new thread
        organization_thread = threading.Thread(
            target=self.run_organization, 
            args=(path,)
        )
        organization_thread.start()

    def run_organization(self, path):
        """
        The actual function that calls the organizer logic.
        This runs in a separate thread.
        """
        try:
            # NOTE: The original organize_folder function prints to the console.
            # A more advanced GUI would capture this output. For now, the user
            # can see the progress in the console if the app is run from there.
            organize_folder(path)
            
            # When done, schedule a GUI update on the main thread
            self.after(0, self.on_organization_complete)
        except Exception as e:
            # Schedule an error message on the main thread
            self.after(0, self.on_organization_error, e)
            
    def on_organization_complete(self):
        """Updates the GUI after the organization is successfully finished."""
        messagebox.showinfo("Success", "Folder organization complete!")
        self.status_label.config(text="Organization complete! Select another folder.")
        self.organize_button.config(state="normal")
        self.select_button.config(state="normal")

    def on_organization_error(self, error):
        """Updates the GUI if an error occurs during organization."""
        messagebox.showerror("Error", f"An error occurred:\n{error}")
        self.status_label.config(text="An error occurred. Please try again.")
        self.organize_button.config(state="normal")
        self.select_button.config(state="normal")


if __name__ == "__main__":
    app = App()
    app.mainloop()

