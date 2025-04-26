import unittest
from src.merger.file_merger import FileMerger

class TestFileMerger(unittest.TestCase):
    def setUp(self):
        self.merger = FileMerger()

    def test_merge_files(self):
        # Create temporary files for testing
        file1 = 'test_file1.txt'
        file2 = 'test_file2.txt'
        output_file = 'output.txt'
        
        with open(file1, 'w') as f:
            f.write('Content of file 1.')
        
        with open(file2, 'w') as f:
            f.write('Content of file 2.')

        # Merge files
        self.merger.merge_files([file1, file2], output_file)

        # Check if output file is created and contains the correct content
        with open(output_file, 'r') as f:
            content = f.read()
        
        expected_content = '--- Start of test_file1.txt ---\nContent of file 1.\n--- End of test_file1.txt ---\n--- Start of test_file2.txt ---\nContent of file 2.\n--- End of test_file2.txt ---\n'
        self.assertEqual(content, expected_content)

    def tearDown(self):
        import os
        try:
            os.remove('test_file1.txt')
            os.remove('test_file2.txt')
            os.remove('output.txt')
        except OSError:
            pass

if __name__ == '__main__':
    unittest.main()