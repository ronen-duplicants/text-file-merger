import unittest
from src.ui.interface import UserInterface

class TestUserInterface(unittest.TestCase):

    def setUp(self):
        self.ui = UserInterface()

    def test_display_menu(self):
        # Capture the output of the display_menu method
        with self.assertLogs(level='INFO') as log:
            self.ui.display_menu()
        self.assertIn("Select files to merge:", log.output[0])
        self.assertIn("1. Merge files", log.output[1])
        self.assertIn("2. Exit", log.output[2])

    def test_get_file_paths(self):
        # Mocking input to test get_file_paths
        with unittest.mock.patch('builtins.input', side_effect=['file1.txt', 'file2.txt', 'output.txt']):
            file_paths = self.ui.get_file_paths()
            self.assertEqual(file_paths, (['file1.txt', 'file2.txt'], 'output.txt'))

if __name__ == '__main__':
    unittest.main()