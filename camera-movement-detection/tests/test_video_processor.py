import os
import shutil
import pytest
from logic.video_processor import extract_frames

def setup_function():
    os.makedirs("tests/videos", exist_ok=True)
    # örnek bir video varsa test için buraya koyabilirsin

def teardown_function():
    if os.path.exists("tests/output"):
        shutil.rmtree("tests/output")

def test_extract_frames_on_dummy_video():
    dummy_video = "tests/frames/frames_video_0/video_0.mp4"
    output_dir = "tests/output"

    if not os.path.exists(dummy_video):
        pytest.skip("🎥 Dummy video bulunamadı. Test atlandı.")

    class DummyProgress:
        def progress(self, val): pass

    total = extract_frames(dummy_video, output_dir, DummyProgress())
    assert total > 0
    assert os.path.exists(os.path.join(output_dir, "frame_000.jpg"))
