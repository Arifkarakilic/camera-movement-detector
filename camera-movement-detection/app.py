import streamlit as st
from config import setup_page
from ui.sidebar import select_mode
from ui.realtime_view import run_realtime_view
from ui.video_analysis_view import run_video_analysis_view

setup_page()
mode = select_mode()

if mode == " Gerçek Zamanlı Takip":
    run_realtime_view()
else:
    run_video_analysis_view()
