from PIL import Image
import streamlit as st
import os

def show_detected_frames(frame_dir, indexes):
    """
    Detected kareleri belirtilen dizinden alır ve Streamlit arayüzünde gösterir.
    
    Args:
        frame_dir (str): Frame dizini
        indexes (List[int]): Gösterilecek frame indexleri
    """
    for idx in indexes:
        img_path = os.path.join(frame_dir, f"frame_{idx:03d}.jpg")
        if os.path.exists(img_path):
            st.image(Image.open(img_path), caption=f"Kare {idx}", use_column_width=True)