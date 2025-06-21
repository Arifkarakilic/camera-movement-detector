import cv2
import numpy as np
import os

def detect_camera_movement_affine(frame_dir, threshold=2.0, min_features=100):
    """
    Affine model ile kamera hareketini tespit eder. 
    Sahnede hareket eden objeleri filtreler.
    
    Args:
        frame_dir (str): Kare klasörü
        threshold (float): Ortalama transform vektör şiddeti
        min_features (int): Minimum izlenecek nokta sayısı
        
    Returns:
        List[int]: Kamera hareketi algılanan frame indexleri
    """
    frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith(".jpg")])
    movement_frames = []

    prev_gray = None
    prev_pts = None

    for i in range(len(frame_files) - 1):
        frame1 = cv2.imread(os.path.join(frame_dir, frame_files[i]))
        frame2 = cv2.imread(os.path.join(frame_dir, frame_files[i + 1]))
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # İlk frame için feature seç
        if prev_pts is None or prev_gray is None:
            prev_pts = cv2.goodFeaturesToTrack(gray1, maxCorners=500, qualityLevel=0.01, minDistance=10)
            prev_gray = gray1
            continue

        # Optical flow ile noktaları takip et
        next_pts, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray2, prev_pts, None)
        if next_pts is None or len(next_pts) < min_features:
            prev_pts = None
            prev_gray = gray2
            continue

        # Geçerli eşleşmeleri al
        good_old = prev_pts[status.flatten() == 1]
        good_new = next_pts[status.flatten() == 1]

        if len(good_old) < min_features:
            prev_pts = None
            prev_gray = gray2
            continue

        # Affine dönüşümü tahmin et (kamera hareketi varsa tutarlı çıkar)
        M, inliers = cv2.estimateAffinePartial2D(good_old, good_new, method=cv2.RANSAC)

        if M is None:
            prev_pts = None
            prev_gray = gray2
            continue

        # Sadece çeviri (dx, dy) bile yeterli olabilir
        dx = M[0, 2]
        dy = M[1, 2]
        shift = np.sqrt(dx**2 + dy**2)

        # print(f"[{i}] shift={shift:.2f}")

        if shift > threshold:
            movement_frames.append(i + 1)

        # Hazırlık: bir sonraki kare için güncelle
        prev_pts = cv2.goodFeaturesToTrack(gray2, maxCorners=500, qualityLevel=0.01, minDistance=10)
        prev_gray = gray2

    return movement_frames

# Örnek test
if __name__ == "__main__":
    frames = detect_camera_movement_affine("frames_video_0", threshold=2.0)
    print("Kamera hareketi algılanan kareler:", frames)
