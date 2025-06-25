import os
import shutil
from utils.file_utils import clean_folder

def test_clean_folder_creates_and_deletes_temp():
    test_dir = "tests/temp_test_folder"

    os.makedirs(test_dir, exist_ok=True)

    test_file = os.path.join(test_dir, "dummy.txt")
    with open(test_file, "w") as f:
        f.write("test")

    assert os.path.exists(test_file), "Test dosyası oluşturulamadı"

    clean_folder(test_dir)

    assert not os.path.exists(test_dir), "Klasör silinmedi"
