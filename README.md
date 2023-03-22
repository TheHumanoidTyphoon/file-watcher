# FileWatcher
FileMover is a Python script that monitors a folder for changes and moves files with specific extensions to a destination folder.

## Preview
<img width=100% src="https://github.com/TheHumanoidTyphoon/file-watcher/blob/main/file-watcher-preview.gif">

## Prerequisites
- Python 3.6 or higher 
- watchdog library `(pip install watchdog)`
## Usage
- Clone or download the repository.

- Install the prerequisites.

- Open a command prompt or terminal window.

- Navigate to the folder containing the script.

- Type the following command: `python filewatch.py [watched_folder] [destination_folder] [--extensions]`

- Replace `[watched_folder]` with the path of the folder to be monitored and `[destination_folder]` with the path of the folder where the files will be moved.

`--extensions` is an optional parameter that accepts a list of file extensions to be moved. By default, the script moves `.jpg`, `.png`, `.pdf`, and `.py` files.

## How it works
The script uses the watchdog library to monitor the specified folder for changes. When a file is modified, the script checks if it has a specified extension. If it does, the script moves the file to the destination folder.
Also the script creates subdirectories within the destination folder based on the current year and month. If a file with the same name already exists in the destination folder, the script renames the file with a numerical suffix to avoid overwriting the existing file.

## Contributing
Contributions are welcome! If you have any ideas for enhancing the program or identifying bugs, kindly submit an [issue](https://github.com/TheHumanoidTyphoon/file-watcher/issues) or pull request on the [GitHub repository](https://github.com/TheHumanoidTyphoon/file-watcher).

## Customizing the script
You can customize the script by modifying the following variables:
- `watched_folder`: The folder to be monitored for changes.
- `destination_folder`: The folder where the files will be moved.
- `extensions`: A dictionary containing the file extensions and their corresponding subdirectory names.
## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/TheHumanoidTyphoon/file-watcher/blob/main/LICENSE) file for details.
