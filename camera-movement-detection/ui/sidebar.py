import streamlit as st

def select_mode():
    return st.radio(" Mod Seç", [" Video / Frame Analizi", " Gerçek Zamanlı Takip"])
