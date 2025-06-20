import streamlit as st
import os
import cv2
from movement_detector import detect_camera_movement
from PIL import Image
import tempfile

st.set_page_config(layout="wide")
st.title("📸 Camera Movement Detection")

# Kullanıcı threshold seçsin
threshold = st.slider("🎚️ Hareket Eşik Değeri (sensitivity)", min_value=1, max_value=100, value=50)
st.info("Bu eşik değeri, hareketin hassasiyetini belirler.\n\nDaha **küçük değerler** küçük kamera kaymalarını bile algılar (örneğin `10`), daha **yüksek değerler** (`70` gibi) ise yalnızca büyük kamera hareketlerini algılar.")


st.markdown("Yüklü videolardan seç veya yeni bir video/GIF yükle.")

available_dirs = [d for d in os.listdir() if d.startswith("frames_video_")]
selected_dir = st.selectbox("📁 Hazır frame klasörü seç:", available_dirs)

uploaded_file = st.file_uploader("🗂️ Video veya GIF yükle (.mp4 / .gif)", type=["mp4", "gif"])

def extract_frames_from_video(video_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    i = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imwrite(os.path.join(output_dir, f"frame_{i:03d}.jpg"), frame)
        i += 1
    cap.release()
    return i

temp_dir = None
if uploaded_file is not None:
    with st.spinner("Video yükleniyor..."):
        temp_dir = tempfile.mkdtemp()
        video_path = os.path.join(temp_dir, uploaded_file.name)
        with open(video_path, "wb") as f:
            f.write(uploaded_file.read())

        frame_dir = os.path.join(temp_dir, "extracted_frames")
        total = extract_frames_from_video(video_path, frame_dir)
        st.success(f"{total} kare çıkarıldı.")

        if st.button("▶️ Yüklenen Videoyu Analiz Et"):
            with st.spinner("Analiz ediliyor..."):
                movement_frames = detect_camera_movement(frame_dir, threshold=threshold)
            st.success(f"{len(movement_frames)} hareketli kare bulundu.")
            for idx in movement_frames:
                img_path = os.path.join(frame_dir, f"frame_{idx:03d}.jpg")
                if os.path.exists(img_path):
                    st.image(Image.open(img_path), caption=f"Kare {idx}", use_column_width=True)

if selected_dir and st.button("📂 Seçili Klasörü Analiz Et"):
    with st.spinner("Analiz ediliyor..."):
        movement_frames = detect_camera_movement(selected_dir, threshold=threshold)
    st.success(f"{len(movement_frames)} hareketli kare bulundu.")
    for idx in movement_frames:
        img_path = os.path.join(selected_dir, f"frame_{idx:03d}.jpg")
        if os.path.exists(img_path):
            st.image(Image.open(img_path), caption=f"Kare {idx}", use_column_width=True)
