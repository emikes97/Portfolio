import logging
import os
import shutil
from pathlib import Path
from datetime import datetime

# All file types that the script will scan and move to respective folders.
file_types = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
    'Videos': ['.mp4', '.mkv', '.avi', '.mov'],
    'Audio': ['.mp3', '.wav', '.ogg'],
    'Archives': ['.zip', '.rar', '.7z', '.tar'],
    'Scripts': ['.py', '.js', '.sh', '.bat'],
    'Installers': ['.exe', '.msi', '.dmg'],
    'Others': []
}

download_path = Path.home() / "Downloads" # Initiate the download path

# Add logging for each moved file.
log_file = Path.home() / "Downloads" / "organizer_log.txt"

if not log_file.exists():
    """If file don't exist, create it and add a header also"""
    log_file.touch() # Create new file, if it doesn't exist.
    with open(log_file, 'w') as file:
        file.write("Download Organizer Log\n")
        file.write("=" * 40 + "\n")

logging.basicConfig(
    filename=log_file,
    filemode= 'a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

for file in download_path.iterdir():
    if file.is_file():
        moved = False
        if file.name == "organizer_log.txt":
            continue
        for category, extensions in file_types.items():
            if file.suffix.lower() in extensions:
                target_folder = download_path / category
                target_folder.mkdir(exist_ok=True)
                shutil.move(str(file), str(target_folder / file.name))
                logging.info(f"Moved '{file.name}' -> '{category}/'")
                moved = True
                break
        if not moved:
            other_folder = download_path / "Others"
            other_folder.mkdir(exist_ok=True)
            shutil.move(str(file), str(other_folder / file.name))
            logging.info(f"Moved '{file.name}' -> 'Others/")

print("Download folder organized successfully!")
