from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RESOURCE_DIR = BASE_DIR / "resources"

def resource_path(*paths):
	return RESOURCE_DIR.joinpath(*paths)
