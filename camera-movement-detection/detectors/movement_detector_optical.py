import cv2
import numpy as np
import os

def detect_camera_movement_optical(frame_dir, threshold=1.0, variance_limit=0.8):
    """
    Optical flow ile sadece kamera hareketini algılar.
    Nesne hareketlerini varyans analizi ile filtreler.
    
    Args:
        frame_dir (str): Frame dizini
        threshold (float): Ortalama hareket eşiği
        variance_limit (float): Hareket yayılımı varyans sınırı
    
    Returns:
        List[int]: Kamera hareketi algılanan kare indexleri
    """
    frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith(".jpg")])
    movement_frames = []

    for i in range(len(frame_files) - 1):
        f1 = cv2.imread(os.path.join(frame_dir, frame_files[i]))
        f2 = cv2.imread(os.path.join(frame_dir, frame_files[i + 1]))

        g1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
        g2 = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)

        flow = cv2.calcOpticalFlowFarneback(
            g1, g2, None,
            0.5, 3, 15, 3, 5, 1.2, 0
        )

        dx, dy = flow[..., 0], flow[..., 1]
        magnitude = np.sqrt(dx**2 + dy**2)

        mean_shift = np.mean(magnitude)
        variance = np.var(magnitude)

        # Kamera hareketi ise: hem ortalama büyük hem de varyans küçük olmalı
        if mean_shift > threshold and variance < variance_limit:
            movement_frames.append(i + 1)

    return movement_frames
