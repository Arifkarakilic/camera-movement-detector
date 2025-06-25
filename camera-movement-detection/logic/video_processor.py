import os
import cv2
from detectors.movement_detector import detect_camera_movement
from detectors.movement_detector_affine import detect_camera_movement_affine
from detectors.movement_detector_optical import detect_camera_movement_optical

def extract_frames(video_path, output_dir, progress_placeholder):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    i = 0
    progress = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imwrite(os.path.join(output_dir, f"frame_{i:03d}.jpg"), frame)
        i += 1
        new_progress = int((i / total) * 100)
        if new_progress > progress:
            progress = new_progress
            progress_placeholder.progress(min(progress, 100))
    cap.release()
    return i

def run_detection(method, frame_dir, params):
    if method == "ORB (Homografi)":
        return detect_camera_movement(frame_dir, *params)
    elif method == "Optical Flow":
        return detect_camera_movement_optical(frame_dir, *params)
    else:
        return detect_camera_movement_affine(frame_dir, *params)