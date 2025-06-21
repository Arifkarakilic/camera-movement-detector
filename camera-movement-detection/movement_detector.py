import cv2
import numpy as np
import os

def detect_camera_movement(frame_dir, threshold=50, min_matches=10):
    """
    Kameradaki kaymaları algılar ve hangi karelerde olduğunu döner.
    """
    frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith(".jpg")])
    orb = cv2.ORB_create(1000)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    movement_frames = []

    for i in range(len(frame_files) - 1):
        img1 = cv2.imread(os.path.join(frame_dir, frame_files[i]), cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(os.path.join(frame_dir, frame_files[i+1]), cv2.IMREAD_GRAYSCALE)

        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)

        if des1 is None or des2 is None:
            continue

        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)

        if len(matches) < min_matches:
            continue

        src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

        H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        if H is None:
            continue

        dx = H[0, 2]
        dy = H[1, 2]
        shift = np.sqrt(dx**2 + dy**2)

        if shift > threshold:
            movement_frames.append(i + 1)

    return movement_frames