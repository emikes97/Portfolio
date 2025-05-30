import logging
import argparse
import shutil
from pathlib import Path

download_path = Path.home() / "Downloads" # Initiate the download path

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

# Command line arguments
parser = argparse.ArgumentParser(description="Organize files by type.")
parser.add_argument("--path", type=str, default=download_path, help="Path to folder to organize")
parser.add_argument("--dry-run", action="store_true", help="Simulate without moving the files")
args = parser.parse_args()

# Add logging for each moved file.
target_path = Path(args.path).expanduser().resolve()
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
                if args.dry_run:
                    print(f"[DRY RUN] Would move '{file.name}' -> '{category}/'")
                else:
                    shutil.move(str(file), str(target_folder / file.name))
                    logging.info(f"Moved '{file.name}' -> '{category}/'")
                moved = True
                break
        if not moved:
            other_folder = download_path / "Others"
            other_folder.mkdir(exist_ok=True)
            if args.dry_run:
                print(f"[DRY RUN] Would move '{file.name}' -> 'Others/'")
            else:
                shutil.move(str(file), str(other_folder / file.name))
                logging.info(f"Moved '{file.name}' -> 'Others/")

print("✅ Folder organized." if not args.dry_run else "🧪 Dry run complete. No files were moved.")