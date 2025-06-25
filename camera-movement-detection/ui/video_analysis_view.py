import os
import tempfile
import streamlit as st
from PIL import Image
from logic.video_processor import extract_frames, run_detection
from utils.visual_utils import show_detected_frames

def run_video_analysis_view():
    method = st.radio(" Algoritma Seç", [
        "ORB (Homografi)",
        "Optical Flow",
        "Affine (GoodFeatures + RANSAC)"
    ])

    if method == "ORB (Homografi)":
        threshold = st.slider(" Translationsal Shift Eşiği (px)", 1, 100, 50, 1)
        min_matches = st.slider("🔹 Minimum Eşleşme Sayısı", 5, 100, 10, 1)
        params = (threshold, min_matches)
    elif method == "Optical Flow":
        threshold = st.slider(" Ortalama Flow Büyüklüğü (px)", 0.1, 5.0, 1.2, 0.1)
        variance_limit = st.slider(" Varyans Limiti", 0.1, 3.0, 0.8, 0.1)
        params = (threshold, variance_limit)
    else:
        threshold = st.slider(" Affine Model Kayma Eşiği (px)", 0.5, 10.0, 2.0, 0.5)
        min_features = st.slider("🔹 Minimum Feature Sayısı", 10, 500, 100, 10)
        params = (threshold, min_features)

    uploaded_file = st.file_uploader(" Video veya GIF Yükle (.mp4 / .gif)", type=["mp4", "gif"])
    frame_root = "frames"
    os.makedirs(frame_root, exist_ok=True)
    available_dirs = [os.path.join(frame_root, d) for d in os.listdir(frame_root) if d.startswith("frames_video_")]
    selected_dir = st.radio(" Hazır Frame Klasörü Seç", available_dirs, index=0 if available_dirs else None)

    if uploaded_file is not None:
        with st.spinner("🎞 Video karelere ayrılıyor..."):
            temp_dir = tempfile.mkdtemp()
            video_path = os.path.join(temp_dir, uploaded_file.name)
            with open(video_path, "wb") as f:
                f.write(uploaded_file.read())

            frame_dir = os.path.join(temp_dir, "frames")
            progress = st.empty()
            total = extract_frames(video_path, frame_dir, progress)
            progress.empty()
            st.success(f"Toplam {total} kare çıkarıldı.")

            if st.button("📊 Yüklenen Videoyu Analiz Et"):
                with st.spinner("Analiz ediliyor..."):
                    movement_frames = run_detection(method, frame_dir, params)
                st.success(f"{len(movement_frames)} hareketli kare tespit edildi.")
                show_detected_frames(frame_dir, movement_frames)

    if selected_dir and st.button("📊 Seçili Klasörü Analiz Et"):
        with st.spinner("Analiz ediliyor..."):
            movement_frames = run_detection(method, selected_dir, params)
        st.success(f"{len(movement_frames)} hareketli kare bulundu.")
        show_detected_frames(selected_dir, movement_frames)