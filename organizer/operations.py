import os
import shutil
from .file_types import FILE_CATEGORIES 

def organize_folder(path):
    """
    Organizes files in a given directory by moving them into subdirectories
    based on their file type defined in file_types.py.

    Args:
        path (str): The absolute path of the folder to organize.
    """
    if not os.path.isdir(path):
        print(f"Error: The path '{path}' is not a valid directory.")
        return

    print(f"Scanning files in: {path}\n")

   
    extension_to_category = {ext: cat for cat, exts in FILE_CATEGORIES.items() for ext in exts}

   
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)

       
        if os.path.isdir(file_path) or filename.startswith('.'):
            continue

        file_ext = os.path.splitext(filename)[1].lower()

        target_folder_name = extension_to_category.get(file_ext, "Other")
        target_folder_path = os.path.join(path, target_folder_name)

        if not os.path.exists(target_folder_path):
            try:
                os.makedirs(target_folder_path)
                print(f"Created folder: {target_folder_name}")
            except OSError as e:
                print(f"Error creating directory {target_folder_path}: {e}")
                continue

        
        try:
            shutil.move(file_path, os.path.join(target_folder_path, filename))
            print(f"Moved: {filename} -> {target_folder_name}/")
        except Exception as e:
            print(f"Error moving {filename}: {e}")

    print("\nOrganization complete!")