from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

RESOURCE_DIR = BASE_DIR / "resources"

def resource_path(*paths):
    if getattr(sys, "frozen", False):
        resource_dir = Path(sys._MEIPASS) / "dino_escape_room" / "resources"
    else:
        resource_dir = RESOURCE_DIR
    return resource_dir.joinpath(*paths)
