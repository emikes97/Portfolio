import os
import shutil
from pathlib import Path

download_path = Path.home() / "Downloads"

file_types = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
    'Videos': ['.mp4', '.mkv', '.avi', '.mov'],
    'Audio': ['.mp3', '.wav', '.ogg'],
    'Archives': ['.zip', '.rar', '.7z', '.tar'],
    'Scripts': ['.py', '.js', '.sh', '.bat'],
    'Installers': ['.exe', '.msi', '.dmg'],
    'Others': []  # fallback
}

for file in download_path.iterdir():
    if file.is_file():
        moved = False
        for category, extensions in file_types.items():
            if file.suffix.lower() in extensions:
                target_folder = download_path / category
                target_folder.mkdir(exist_ok=True)
                shutil.move(str(file), str(target_folder / file.name))
                moved = True
                break
        if not moved:
            other_folder = download_path / "Others"
            other_folder.mkdir(exist_ok=True)
            shutil.move(str(file), str(other_folder / file.name))

print("Download folder organized successfully!")
