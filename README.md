# Text File Merger

This project provides a simple tool to merge multiple text files into a single file. Each file's content is prefixed with a header indicating the start and end of the file, making it easy to identify where each file's content begins and ends.

## Features

- Merge multiple text files into one.
- Clearly indicate the start and end of each file in the merged output.
- User-friendly interface for selecting files to merge.
- GUI interface for easier file selection.

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

1. Run the script using the following command:

```
python scripts/merge_files.py
```

2. Follow the prompts in the user interface to select the text files you want to merge and specify the output file name.

### Graphical User Interface

For a more user-friendly experience, use the GUI version:

```
python scripts/run_gui.py
```

The GUI allows you to:
- Add multiple files
- Remove selected files
- Clear all files
- Merge files and save to a location of your choice

## File Structure

```
text-file-merger
├── src
│   ├── merger
│   │   ├── __init__.py
│   │   └── file_merger.py
│   ├── ui
│   │   ├── __init__.py
│   │   └── interface.py
│   └── __init__.py
├── scripts
│   └── merge_files.py
├── tests
│   ├── __init__.py
│   ├── test_merger.py
│   └── test_ui.py
├── requirements.txt
├── setup.py
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.