import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserInterface:
    def display_menu(self):
        logger.info("Select files to merge:")
        logger.info("1. Merge files")
        logger.info("2. Exit")

    def get_file_paths(self):
        input_files = input("Enter file paths (comma separated): ").strip()
        file_paths = [path.strip() for path in input_files.split(',')]
        output_file = input("Enter the output file path: ").strip()
        return file_paths, output_file