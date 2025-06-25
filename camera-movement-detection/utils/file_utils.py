import os
import shutil

def clean_folder(folder_path):
    """
    
    Args:
        folder_path (str): Silinecek klasörün yolu
    """
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
