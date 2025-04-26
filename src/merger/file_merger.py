import os
import platform
import subprocess

class FileMerger:
    def merge_files(self, file_paths, output_file):
        with open(output_file, 'w') as outfile:
            for file_path in file_paths:
                outfile.write(f"--- Start of {file_path} ---\n")
                try:
                    with open(file_path, 'r') as infile:
                        outfile.write(infile.read())
                except UnicodeDecodeError:
                    # Handle binary files
                    outfile.write("[Binary content not shown]")
                except FileNotFoundError:
                    outfile.write(f"[File not found: {file_path}]")
                outfile.write(f"\n--- End of {file_path} ---\n")

    def write_to_file(self, content, output_file):
        with open(output_file, 'w') as outfile:
            outfile.write(content)
            
    def open_file(self, file_path):
        """Open file with the default system application."""
        try:
            if platform.system() == 'Windows':
                os.startfile(file_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', file_path])
            else:  # Linux and other OS
                subprocess.call(['xdg-open', file_path])
            return True
        except Exception as e:
            print(f"Error opening file: {e}")
            return False