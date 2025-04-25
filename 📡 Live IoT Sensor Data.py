# NOTE: This Streamlit app must be run in a local environment where 'streamlit' and 'pandas' are installed.
# This code will not work in restricted or sandboxed environments that block package imports.

import streamlit as st
import pandas as pd
from datetime import datetime, time

# Simulated IoT data generator
def get_simulated_iot_data():
    return {
        "Room A": {"temp": 22.5, "occupancy": 3},
        "Room B": {"temp": 24.1, "occupancy": 6},
        "Room C": {"temp": 21.0, "occupancy": 1},
    }

# Room attributes (example data)
rooms_data = {
    "Room": ["Room A", "Room B", "Room C"],
    "Occupancy Suitability": [5, 3, 4],
    "Natural Lighting": [4, 2, 5],
    "Energy Efficiency": [3, 5, 4],
    "AV/Tech Availability": [5, 4, 3],
    "Noise Isolation": [4, 3, 4],
    "Proximity to Team Zone": [3, 4, 2],
    "Availability": [3, 5, 4]  # Simulated availability score
}

weights = {
    "Occupancy Suitability": 0.20,
    "Natural Lighting": 0.10,
    "Energy Efficiency": 0.15,
    "AV/Tech Availability": 0.10,
    "Noise Isolation": 0.05,
    "Proximity to Team Zone": 0.05,
    "Availability": 0.25,
    "HVAC Temp": 0.05,
    "Current Occupancy": 0.05
}

# Convert to DataFrame
df = pd.DataFrame(rooms_data)

# Add columns for IoT metrics
iot_data = get_simulated_iot_data()
df["HVAC Temp"] = df["Room"].apply(lambda x: iot_data[x]["temp"])
df["Current Occupancy"] = df["Room"].apply(lambda x: iot_data[x]["occupancy"])

# Streamlit UI
st.set_page_config(page_title="Conference Room Selector", layout="centered")
st.title("📊 Conference Room Selector - ODC")

st.markdown("""
This tool helps **Facility Admins** choose the best room based on:
- Room availability
- Occupancy needs
- Energy efficiency
- AV setup and more
""")

# Select desired meeting time
st.subheader("📅 Choose Meeting Time")
selected_date = st.date_input("Select a date")
start_time = st.time_input("Start Time", value=time(9, 0))
end_time = st.time_input("End Time", value=time(10, 0))

# Simulate availability change based on time
if start_time >= time(12, 0):
    df.loc[df['Room'] == "Room A", "Availability"] = 4
    df.loc[df['Room'] == "Room B", "Availability"] = 5
    df.loc[df['Room'] == "Room C", "Availability"] = 3
else:
    df.loc[df['Room'] == "Room A", "Availability"] = 3
    df.loc[df['Room'] == "Room B", "Availability"] = 4
    df.loc[df['Room'] == "Room C", "Availability"] = 5

# Scoring function
ideal_temp = 22.0
ideal_occupancy = 4

def calculate_score(row):
    base_score = sum(row[crit] * weights[crit] for crit in weights if crit not in ["HVAC Temp", "Current Occupancy"])
    temp_penalty = abs(row["HVAC Temp"] - ideal_temp) * 0.1  # Adjust if far from 22°C
    occupancy_bonus = 5 - abs(row["Current Occupancy"] - ideal_occupancy)  # Closer to 4 is better
    return base_score - temp_penalty + (occupancy_bonus * weights["Current Occupancy"])

df["Weighted Score"] = df.apply(calculate_score, axis=1)
df = df.sort_values("Weighted Score", ascending=False)

# Show live IoT data
st.subheader("📡 Live IoT Sensor Data")
for room in df["Room"]:
    st.markdown(f"**{room}** – Temp: {iot_data[room]['temp']} °C, Occupancy: {iot_data[room]['occupancy']} people")

# Show the table
st.subheader("🔍 Room Comparison Table")
st.dataframe(df.reset_index(drop=True), use_container_width=True)

# Show recommended room
top_room = df.iloc[0]["Room"]
top_score = df.iloc[0]["Weighted Score"]
st.success(f"✅ Recommended Room: **{top_room}** with a score of **{top_score:.2f}**")
