# smart_meeting_room_selector.py

import streamlit as st
import pandas as pd

st.title("📍 Smart Meeting Room Location Map")

# Sample lat/lon data for rooms (replace with your own coordinates)
room_locations = pd.DataFrame({
    "Room": ["Room A", "Room B", "Room C"],
    "lat": [28.5385, 28.5386, 28.5361],
    "lon": [77.3385, 77.3412, 77.3440],
})

selected_rooms = st.multiselect("Show rooms on map", room_locations["Room"].tolist(), default=room_locations["Room"].tolist())
filtered = room_locations[room_locations["Room"].isin(selected_rooms)]

st.map(filtered, zoom=15)

