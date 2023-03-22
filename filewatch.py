import shutil
import argparse
from typing import List


from datetime import date
from pathlib import Path
from time import sleep

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def add_date_to_path(dest_root: Path) -> Path:
    """
    Helper function that adds the current year and month to the destination path. If the path does not already exist,
    it is created.

    :param dest_root: root of the destination path to append subdirectories based on date
    :type dest_root: Path
    :return: updated path with year and month appended
    :rtype: Path
    """
    dated_path = dest_root / f"{date.today().year}" / f"{date.today().month:02d}"
    dated_path.mkdir(parents=True, exist_ok=True)
    return dated_path


def rename_file(source: Path, dest_path: Path) -> Path:
    """
    Helper function that renames a file to reflect the new path. If a file of the same name already exists in the destination
    folder, the file name is numbered and incremented until the filename is unique (prevents overwriting files).

    :param source: source path of file to be moved
    :type source: Path
    :param dest_path: destination path to move the file to
    :type dest_path: Path
    :return: path to the renamed file
    :rtype: Path
    """
    if Path(dest_path / source.name).exists():
        increment = 1

        while True:
            new_name = dest_path / f"{source.stem}_{increment}{source.suffix}"
            increment += 1

            if not new_name.exists():
                return new_name
    else:
        return dest_path / source.name

class FileMoverEventHandler(FileSystemEventHandler):
    """
    A class that handles events for a specified watched folder and moves files with specified extensions to a destination folder.

    Attributes:
    -----------
    watched_folder : Path
        A Path object representing the folder to be watched for changes.
    destination_folder : Path
        A Path object representing the destination folder where the files will be moved.
    extensions : dict
        A dictionary containing the file extensions and their corresponding subdirectory names.

    Methods:
    --------
    on_modified(event):
        A method that is called when a file or folder is modified within the watched folder.
        If the modified item is a file with a specified extension, it is moved to the destination folder.
    """
    def __init__(self, watched_folders: List[Path], destination_folder: Path, extensions: dict):
        self.watched_folders = [folder.resolve() for folder in watched_folders]
        self.destination_folder = destination_folder.resolve()
        self.extensions = extensions

        self.observers = []
        for folder in self.watched_folders:
            observer = Observer()
            observer.schedule(self, str(folder), recursive=True)
            self.observers.append(observer)

    def on_modified(self, event):
        """
        Move files with specified extensions from watched_folder to destination_folder.

        Parameters:
        -----------
        event : FileSystemEvent
            A FileSystemEvent object representing the event that triggered the method.

        Returns:
        --------
        None
        """
        for folder in self.watched_folders:
            for child in folder.iterdir():
                # Skip directories and non-specified extensions
                if child.is_file() and child.suffix.lower() in self.extensions.keys():
                    dest_path = self.destination_folder / self.extensions[child.suffix.lower()]
                    dest_path = add_date_to_path(dest_root=dest_path)
                    dest_path = rename_file(source=child, dest_path=dest_path)
                    shutil.move(src=child, dst=dest_path)
                    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Watch a folder for changes and move files with specified extensions to a destination folder.')
    parser.add_argument('watched_folder', type=str, help='Path of the folder to be watched')
    parser.add_argument('destination_folder', type=str, help='Path of the destination folder')
    parser.add_argument('--extensions', nargs='+', default=['.jpg', '.png', '.pdf', '.py'], help='List of file extensions to be moved (default: .jpg .png .pdf)')
    args = parser.parse_args()

    watched_folder = Path(args.watched_folder).resolve()
    destination_folder = Path(args.destination_folder).resolve()
    extensions = {ext.lower(): f"_{ext[1:]}" for ext in args.extensions}

    event_handler = FileMoverEventHandler(watched_folders=[watched_folder], destination_folder=destination_folder, extensions=extensions)

    observer = Observer()
    observer.schedule(event_handler, str(watched_folder), recursive=True)
    observer.start()

    try:
        while True:
            sleep(60)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


