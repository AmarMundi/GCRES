# smart_meeting_room_selector.py

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Smart Meeting Room Selector", layout="wide")
st.title("🏢 Smart Meeting Room Selection Matrix")

st.markdown("Evaluate and select the best meeting room based on intelligent facility criteria.")

# ---------------------
# Define rating conversion
rating_map = {"High": 1, "Medium": 2, "Low": 3, "Yes": 3, "Partial": 2, "No": 1, "Quiet": 3, "Moderate": 2, "Noisy": 1, "Near": 3, "Far": 1}

# Define criteria, weights
criteria = {
    "Occupancy Level": 5,
    "Noise Level": 4,
    "Natural Light Availability": 2,
    "Shared HVAC Zone": 3,
    "Energy Efficiency Features": 3,
    "Proximity to Team": 3,
    "Availability at Required Time": 5,
    "Security Level": 4,
    "Crowd Level on Floor": 3,
}

rooms = st.multiselect("Select Rooms to Compare", ["Room A", "Room B", "Room C"], default=["Room A", "Room B", "Room C"])

# Store results
room_scores = {}

for room in rooms:
    st.subheader(f"🏷️ {room}")
    score = 0
    cols = st.columns(3)  # 3 columns for narrower dropdown layout
    for idx, (crit, weight) in enumerate(criteria.items()):
        options = list(rating_map.keys())
        default = "Medium" if "Level" in crit else "Yes"
        with cols[idx % 3]:
            selection = st.selectbox(f"{crit}", options, index=options.index(default), key=f"{room}_{crit}")
        rating = rating_map.get(selection, 2)
        score += rating * weight
    room_scores[room] = score

# Display results
st.markdown("---")
st.header("📊 Room Scores")
for room, score in room_scores.items():
    st.metric(label=room, value=f"{score} points")

# Best room highlight
best_room = max(room_scores, key=room_scores.get)
st.success(f"✅ Recommended Room: **{best_room}** with {room_scores[best_room]} points")
