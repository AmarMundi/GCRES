# smart_meeting_room_selector.py

import streamlit as st
import pandas as pd
from PIL import Image


pg = st.navigation([st.Page("🧠overview.py"), st.Page("🏢Smart_meeting_room_selector.py"), st.Page("📍Smart Meeting Room Location Map.py"), 
    st.Page("🔍Room Comparison Table.py"), st.Page("📡 Live IoT Sensor Data.py"), st.Page("📈 IoT Metrics Visualization.py"),
    st.Page("🤖 AI-Agent.py"), st.Page("🤖 AI Multi-Agent.py"), st.Page("🤖 AI Autonomus Multi-Agent System.py")])
pg.run()


st.sidebar.header("Global commercial real estate services")
image = Image.open("logo.png")
st.sidebar.image(image)