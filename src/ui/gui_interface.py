import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.merger.file_merger import FileMerger

class SettingsManager:
    def __init__(self):
        self.settings_file = os.path.join(os.path.expanduser("~"), ".text_file_merger_settings.json")
        self.default_settings = {
            "ask_to_open_file": True,
            "last_input_directory": "",
            "last_output_directory": "",
            "saved_files": []  # Add this to store the file list
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return self.default_settings.copy()
        return self.default_settings.copy()
    
    def save_settings(self):
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key):
        return self.settings.get(key, self.default_settings.get(key))
    
    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()

class AboutDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("About Text File Merger")
        
        # Keep it simple
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Add content
        tk.Label(self, text="Text File Merger", font=("Arial", 16, "bold")).pack(pady=(20, 10))
        tk.Label(self, text="Version 1.0").pack(pady=5)
        
        # Description frame with text
        desc_frame = tk.Frame(self)
        desc_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        description = """This tool allows you to merge multiple text files into a single file.
        
Features:
• Merge multiple text files into one output file
• Clearly mark the start and end of each input file
• Support for various file types that contain text content
• User-friendly interface for file selection

Perfect for combining source code, shaders, configuration files, 
or any text-based content for review or analysis."""
        
        desc_text = tk.Text(desc_frame, wrap=tk.WORD, height=10, width=40)
        desc_text.pack(fill=tk.BOTH, expand=True)
        desc_text.insert(tk.END, description)
        desc_text.config(state=tk.DISABLED)
        
        # Button frame with padding
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=20, pady=(5, 15))
        
        # OK button with proper width
        tk.Button(btn_frame, text="OK", command=self.destroy, width=10).pack(pady=5)

class SettingsDialog(tk.Toplevel):
    def __init__(self, parent, settings_manager):
        super().__init__(parent)
        self.title("Settings")
        
        # Keep it simple
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.settings_manager = settings_manager
        
        # Create variables
        self.ask_to_open_var = tk.BooleanVar(value=settings_manager.get("ask_to_open_file"))
        
        # Create widgets
        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="File Merger Settings", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))
        
        # Settings options
        tk.Checkbutton(frame, text="Ask to open file after merging", variable=self.ask_to_open_var).pack(anchor="w", pady=5)
        
        # Clear history buttons - group in a frame
        history_frame = tk.Frame(frame)
        history_frame.pack(fill=tk.X, pady=10)
        
        # Clear directory history
        tk.Button(history_frame, text="Clear directory history", 
                 command=self.clear_directory_history, 
                 width=20).pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear file list history (new)
        tk.Button(history_frame, text="Clear saved file list", 
                 command=self.clear_file_history, 
                 width=20).pack(side=tk.LEFT)
        
        # Bottom buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=20, pady=(5, 15))
        
        # Button container to center them
        button_container = tk.Frame(btn_frame)
        button_container.pack(pady=5)
        
        tk.Button(button_container, text="Save", command=self.save_settings, width=10).pack(side=tk.LEFT, padx=10)
        tk.Button(button_container, text="Cancel", command=self.destroy, width=10).pack(side=tk.LEFT, padx=10)
        
    def save_settings(self):
        self.settings_manager.set("ask_to_open_file", self.ask_to_open_var.get())
        self.destroy()
    
    def clear_directory_history(self):
        self.settings_manager.set("last_input_directory", "")
        self.settings_manager.set("last_output_directory", "")
        messagebox.showinfo("Directory History", "Directory history has been cleared.")
        
    def clear_file_history(self):
        self.settings_manager.set("saved_files", [])
        messagebox.showinfo("File List", "Saved file list has been cleared.")

class FilemergerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Text File Merger")
        self.root.geometry("600x400")
        
        self.file_merger = FileMerger()
        self.files_to_merge = []
        self.settings_manager = SettingsManager()
        
        # Create menu bar
        self.create_menu_bar()
        
        self.create_widgets()
        
        # Load previously saved files
        self.load_saved_files()
    
    # Add this method to load saved files
    def load_saved_files(self):
        saved_files = self.settings_manager.get("saved_files")
        if saved_files:
            for file in saved_files:
                if os.path.exists(file) and file not in self.files_to_merge:
                    self.files_to_merge.append(file)
                    self.file_listbox.insert(tk.END, file)
    
    # Add this method to save current file list
    def save_file_list(self):
        self.settings_manager.set("saved_files", self.files_to_merge)
    
    # Update the create_menu_bar to add Clear Saved Files option
    def create_menu_bar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Settings", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)
        
        # Edit menu (new)
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear Saved Files", command=self.clear_saved_files)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.open_about)
    
    # Add method to clear saved files
    def clear_saved_files(self):
        self.settings_manager.set("saved_files", [])
        messagebox.showinfo("Files Cleared", "Saved file list has been cleared.\nRestart the application to see the change.")
    
    # Update add_files method to default to All Files and save the file list
    def add_files(self):
        # Get last used directory for input files
        initial_dir = self.settings_manager.get("last_input_directory")
        if not initial_dir or not os.path.exists(initial_dir):
            initial_dir = os.path.expanduser("~")
            
        files = filedialog.askopenfilenames(
            title="Select files to merge", 
            initialdir=initial_dir,
            filetypes=[("All files", "*.*"), ("Text files", "*.txt")]  # Changed order to make All Files default
        )
        
        if files:
            # Save the last used directory
            self.settings_manager.set("last_input_directory", os.path.dirname(files[0]))
            
            for file in files:
                if file not in self.files_to_merge:
                    self.files_to_merge.append(file)
                    self.file_listbox.insert(tk.END, file)
            
            # Save the updated file list
            self.save_file_list()
    
    # Update remove_selected to also save file list
    def remove_selected(self):
        try:
            selected_idx = self.file_listbox.curselection()[0]
            self.file_listbox.delete(selected_idx)
            self.files_to_merge.pop(selected_idx)
            
            # Save the updated file list
            self.save_file_list()
        except IndexError:
            messagebox.showinfo("Info", "Please select a file to remove")
    
    # Update clear_files to also save file list
    def clear_files(self):
        self.file_listbox.delete(0, tk.END)
        self.files_to_merge = []
        
        # Save the updated file list
        self.save_file_list()
    
    def merge_files(self):
        if not self.files_to_merge:
            messagebox.showinfo("Info", "Please add files to merge")
            return
        
        # Get last used directory for output file
        initial_dir = self.settings_manager.get("last_output_directory") 
        if not initial_dir or not os.path.exists(initial_dir):
            initial_dir = os.path.expanduser("~")
            
        output_file = filedialog.asksaveasfilename(
            title="Save merged file as",
            initialdir=initial_dir,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if output_file:
            # Save the last used output directory
            self.settings_manager.set("last_output_directory", os.path.dirname(output_file))
            
            try:
                self.file_merger.merge_files(self.files_to_merge, output_file)
                
                # Check if we should ask to open the file
                if self.settings_manager.get("ask_to_open_file"):
                    # Use messagebox instead of custom dialog
                    self.show_open_file_messagebox(output_file)
                else:
                    # Just show a confirmation message
                    messagebox.showinfo("Success", f"Files have been merged into {output_file}")
                    
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_open_file_messagebox(self, output_file):
        """Use built-in messagebox instead of custom dialog"""
        # Ask if user wants to open the file
        response = messagebox.askyesno(
            "Success",
            f"Files have been merged into:\n{output_file}\n\nDo you want to open the file?"
        )
        
        if response:
            self.file_merger.open_file(output_file)
        
        # Separately ask if they want to stop showing this message
        dont_ask = messagebox.askyesno(
            "Preferences",
            "Would you like to stop showing this dialog in the future?",
            default=messagebox.NO
        )
        
        if dont_ask:
            self.settings_manager.set("ask_to_open_file", False)

    def open_settings(self):
        """Opens the settings dialog"""
        SettingsDialog(self.root, self.settings_manager)
    
    def open_about(self):
        """Opens the about dialog"""
        AboutDialog(self.root)

    def create_widgets(self):
        """Create the main UI widgets"""
        # Title
        title_label = tk.Label(self.root, text="Text File Merger", font=("Arial", 16))
        title_label.pack(pady=10)
        
        # Frame for file list
        self.list_frame = tk.Frame(self.root)
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Listbox for selected files
        self.file_listbox = tk.Listbox(self.list_frame, width=70, height=10)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(self.list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure scrollbar
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.file_listbox.yview)
        
        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        # Buttons
        add_button = tk.Button(button_frame, text="Add Files", command=self.add_files, width=15)
        add_button.grid(row=0, column=0, padx=5)
        
        remove_button = tk.Button(button_frame, text="Remove Selected", command=self.remove_selected, width=15)
        remove_button.grid(row=0, column=1, padx=5)
        
        clear_button = tk.Button(button_frame, text="Clear All", command=self.clear_files, width=15)
        clear_button.grid(row=0, column=2, padx=5)
        
        # Merge button
        merge_button = tk.Button(self.root, text="Merge Files", command=self.merge_files, bg="#4CAF50", fg="white", width=20, height=2)
        merge_button.pack(pady=10)

def run_gui():
    root = tk.Tk()
    app = FilemergerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()