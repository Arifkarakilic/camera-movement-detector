import streamlit as st

def notify_email_sent():
    st.success(" E-posta başarıyla gönderildi.")

def notify_camera_movement():
    st.warning(" Kamera hareketi tespit edildi!")

def notify_processing():
    return st.spinner(" Analiz ediliyor...")

def notify_done(message="İşlem tamamlandı."):
    st.success(f" {message}")