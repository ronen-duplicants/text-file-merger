import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.merger.file_merger import FileMerger
from src.ui.interface import UserInterface

def main():
    ui = UserInterface()
    ui.display_menu()
    choice = input("Enter your choice: ")
    
    if choice == '1':
        file_paths, output_file = ui.get_file_paths()
        
        merger = FileMerger()
        merger.merge_files(file_paths, output_file)
        print(f"Merged files into {output_file}")
        
        # Ask if user wants to open the merged file
        open_file = input("Do you want to open the merged file? (y/n): ").strip().lower()
        if open_file == 'y':
            if merger.open_file(output_file):
                print(f"Opened {output_file} with default application.")
            else:
                print("Could not open the file. Please open it manually.")
                
    elif choice == '2':
        print("Exiting...")
        return
    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main()