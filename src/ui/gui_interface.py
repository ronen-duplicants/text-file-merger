import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.merger.file_merger import FileMerger

class FilemergerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Text File Merger")
        self.root.geometry("600x400")
        
        self.file_merger = FileMerger()
        self.files_to_merge = []
        
        self.create_widgets()
        
    def create_widgets(self):
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
        
    def add_files(self):
        files = filedialog.askopenfilenames(title="Select files to merge", 
                                           filetypes=[("Text files", "*.txt"), 
                                                     ("All files", "*.*")])
        if files:
            for file in files:
                if file not in self.files_to_merge:
                    self.files_to_merge.append(file)
                    self.file_listbox.insert(tk.END, file)
    
    def remove_selected(self):
        try:
            selected_idx = self.file_listbox.curselection()[0]
            self.file_listbox.delete(selected_idx)
            self.files_to_merge.pop(selected_idx)
        except IndexError:
            messagebox.showinfo("Info", "Please select a file to remove")
    
    def clear_files(self):
        self.file_listbox.delete(0, tk.END)
        self.files_to_merge = []
    
    def merge_files(self):
        if not self.files_to_merge:
            messagebox.showinfo("Info", "Please add files to merge")
            return
            
        output_file = filedialog.asksaveasfilename(title="Save merged file as",
                                                 defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), 
                                                           ("All files", "*.*")])
        
        if output_file:
            try:
                self.file_merger.merge_files(self.files_to_merge, output_file)
                
                # Ask if user wants to open the merged file
                open_file = messagebox.askyesno("Success", 
                                               f"Files have been merged into {output_file}\n\nDo you want to open the merged file?")
                
                if open_file:
                    self.file_merger.open_file(output_file)
                    
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

def run_gui():
    root = tk.Tk()
    app = FilemergerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()