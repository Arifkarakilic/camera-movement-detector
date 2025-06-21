import cv2
import numpy as np
import os
from PIL import Image
import streamlit as st
import tempfile

from movement_detector import detect_camera_movement
from movement_detector_optical import detect_camera_movement_optical
from movement_detector_affine import detect_camera_movement_affine

st.set_page_config(layout="wide")
st.title("📸 Camera Movement Detection")

method = st.radio("🔧 Algoritma Seç", [
    "ORB (Homografi)",
    "Optical Flow",
    "Affine (GoodFeatures + RANSAC)"
])

if method == "ORB (Homografi)":
    threshold = st.slider("🎚️ Translationsal Shift Eşiği (px)", 1, 100, 50, 1)
    min_matches = st.slider("🔹 Minimum Eşleşme Sayısı", 5, 100, 10, 1)
    st.info("Eşik değer (threshold), iki ardışık karedeki kameranın x/y yönünde yer değiştirmesini (shift) ifade eder. Eğer bu değer yüksekse, sadece büyük kamera hareketleri algılanır. Minimum eşleşme (min_matches) değeri düşükse, küçük benzerlikler bile dikkate alınır.")
elif method == "Optical Flow":
    threshold = st.slider("🎚️ Ortalama Flow Büyüklüğü (px)", 0.1, 5.0, 1.2, 0.1)
    variance_limit = st.slider("📉 Varyans Limiti", 0.1, 3.0, 0.8, 0.1)
    st.info("Ortalama hareket büyüklüğü (threshold), sahnedeki tüm piksel hareketlerinin ortalamasıdır. Varyans limiti, bu hareketlerin sahneye yayılmış olup olmadığını kontrol eder. Yüksek varyans, sadece nesne hareketi olduğunu gösterir.")
else:
    threshold = st.slider("🎚️ Affine Model Kayma Eşiği (px)", 0.5, 10.0, 2.0, 0.5)
    min_features = st.slider("🔹 Minimum Feature Sayısı", 10, 500, 100, 10)
    st.info("Affine model eşik değeri (threshold), sahnedeki global hareketin büyüklüğünü ölçer. Minimum feature sayısı, takip edilmesi gereken köşe sayısını belirtir. Bu yöntem sadece sahne genelinde tekdüze hareket varsa hareketi algılar.")

uploaded_file = st.file_uploader("📂 Video veya GIF Yükle (.mp4 / .gif)", type=["mp4", "gif"])
available_dirs = [d for d in os.listdir() if d.startswith("frames_video_")]
selected_dir = st.radio("🗂️ Hazır Frame Klasörü Seç", available_dirs, index=0)

def extract_frames_from_video(video_path, output_dir, progress_placeholder):
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

def run_detection(frame_dir):
    if method == "ORB (Homografi)":
        return detect_camera_movement(frame_dir, threshold=threshold, min_matches=min_matches)
    elif method == "Optical Flow":
        return detect_camera_movement_optical(frame_dir, threshold=threshold, variance_limit=variance_limit)
    else:
        return detect_camera_movement_affine(frame_dir, threshold=threshold, min_features=min_features)

temp_dir = None
if uploaded_file is not None:
    with st.spinner("🎞 Video karelere ayrılıyor..."):
        temp_dir = tempfile.mkdtemp()
        video_path = os.path.join(temp_dir, uploaded_file.name)
        with open(video_path, "wb") as f:
            f.write(uploaded_file.read())

        frame_dir = os.path.join(temp_dir, "frames")
        if 'video_processed' not in st.session_state or not os.path.exists(frame_dir):
            progress_placeholder = st.empty()
            total = extract_frames_from_video(video_path, frame_dir, progress_placeholder)
            progress_placeholder.empty()
            st.session_state.video_processed = True
        else:
            total = len([f for f in os.listdir(frame_dir) if f.endswith('.jpg')])
        st.success(f"Toplam {total} kare çıkarıldı.")

        if st.button("📊 Yüklenen Videoyu Analiz Et"):
            with st.spinner("Analiz ediliyor..."):
                movement_frames = run_detection(frame_dir)
            st.success(f"{len(movement_frames)} hareketli kare tespit edildi.")
            for idx in movement_frames:
                img_path = os.path.join(frame_dir, f"frame_{idx:03d}.jpg")
                if os.path.exists(img_path):
                    st.image(Image.open(img_path), caption=f"Kare {idx}", use_column_width=True)

if selected_dir and st.button("📊 Seçili Klasörü Analiz Et"):
    with st.spinner("Analiz ediliyor..."):
        movement_frames = run_detection(selected_dir)
    st.success(f"{len(movement_frames)} hareketli kare bulundu.")
    for idx in movement_frames:
        img_path = os.path.join(selected_dir, f"frame_{idx:03d}.jpg")
        if os.path.exists(img_path):
            st.image(Image.open(img_path), caption=f"Kare {idx}", use_column_width=True)
