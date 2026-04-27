import shutil
import os

source_dir = r"c:\Users\PRASANNA\Desktop\tai\student-portal-templates\templates\static\images"
dest_dir = r"c:\Users\PRASANNA\Desktop\tai\project file\Youtube\django\studentstudyportal\static\images"

files_to_copy = ["notes.jpg", "homework.jpg", "youtube.jpg", "todo.jpg", "books.jpg", "dictionary.jpg", "wiki.jpg", "conversion.jpg"]

os.makedirs(dest_dir, exist_ok=True)

copied_files = []
failed_files = []

print("=" * 70)
print("Starting file copy operation...")
print("=" * 70)
print(f"Source: {source_dir}")
print(f"Destination: {dest_dir}")
print("-" * 70)

for filename in files_to_copy:
    source_file = os.path.join(source_dir, filename)
    dest_file = os.path.join(dest_dir, filename)
    try:
        if os.path.exists(source_file):
            shutil.copy2(source_file, dest_file)
            copied_files.append(filename)
            print(f"Copied: {filename}")
        else:
            failed_files.append(filename)
            print(f"Failed: {filename} (not found)")
    except Exception as e:
        failed_files.append(filename)
        print(f"Failed: {filename} - {e}")

print("-" * 70)
print(f"Successfully copied: {len(copied_files)}/{len(files_to_copy)} files")
print(f"Failed: {len(failed_files)}/{len(files_to_copy)} files")
if len(failed_files) == 0:
    print("ALL FILES COPIED SUCCESSFULLY!")
print("=" * 70)
