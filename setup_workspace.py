import argparse
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("base_dir", help="Path to EHR_TUTORIAL_WORKSPACE")
args = parser.parse_args()
base_dir = args.base_dir

# Create data folders
for folder in ["raw_data/structured_data", "raw_data/note_data", "processed_data"]:
    os.makedirs(os.path.join(base_dir, folder), exist_ok=True)
print(f"Workspace created at: {os.path.abspath(base_dir)}")

# Clone tutorial notebooks into scripts/
scripts_dir = os.path.join(base_dir, "scripts")
subprocess.run(
    ["git", "clone", "https://github.com/vectorranger/TUTORIAL.git", scripts_dir],
    check=True,
)
print(f"Tutorial files ready at: {os.path.abspath(scripts_dir)}")

# Print directory structure (2 levels deep)
for dirpath, dirnames, _ in os.walk(base_dir):
    level = dirpath.replace(base_dir, "").count(os.sep)
    if level >= 2:
        dirnames.clear()
    print("  " * level + os.path.basename(dirpath) + "/")
