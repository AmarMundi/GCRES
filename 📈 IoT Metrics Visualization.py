# NOTE: This Streamlit app must be run in a local environment where 'streamlit' and 'pandas' are installed.
# This code will not work in restricted or sandboxed environments that block package imports.

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime, time

# Simulated real-time IoT data generator
def get_simulated_iot_data():
    return {
        "Room A": {"temp": round(random.uniform(21, 23.5), 1), "occupancy": random.randint(1, 6)},
        "Room B": {"temp": round(random.uniform(23, 25.5), 1), "occupancy": random.randint(2, 8)},
        "Room C": {"temp": round(random.uniform(20, 22.5), 1), "occupancy": random.randint(1, 5)},
    }

# Room attributes (example data)
def create_room_data(iot_data):
    return {
        "Room": ["Room A", "Room B", "Room C"],
        "Occupancy Suitability": [5, 3, 4],
        "Natural Lighting": [4, 2, 5],
        "Energy Efficiency": [3, 5, 4],
        "AV/Tech Availability": [5, 4, 3],
        "Noise Isolation": [4, 3, 4],
        "Proximity to Team Zone": [3, 4, 2],
        "Availability": [3, 5, 4],
        "HVAC Temp": [iot_data["Room A"]["temp"], iot_data["Room B"]["temp"], iot_data["Room C"]["temp"]],
        "Current Occupancy": [iot_data["Room A"]["occupancy"], iot_data["Room B"]["occupancy"], iot_data["Room C"]["occupancy"]],
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

# Scoring function
ideal_temp = 22.0
ideal_occupancy = 4

def calculate_score(row):
    base_score = sum(row[crit] * weights[crit] for crit in weights if crit not in ["HVAC Temp", "Current Occupancy"])
    temp_penalty = abs(row["HVAC Temp"] - ideal_temp) * 0.1
    occupancy_bonus = 5 - abs(row["Current Occupancy"] - ideal_occupancy)
    return base_score - temp_penalty + (occupancy_bonus * weights["Current Occupancy"])

# Streamlit UI
st.set_page_config(page_title="Conference Room Selector", layout="wide")
st.title("📊 Conference Room Selector - ODC")

st.markdown("""
This tool helps **Facility Admins** choose the best room based on:
- Room availability
- Occupancy needs
- Energy efficiency
- AV setup and more
""")

# Select desired meeting time
st.sidebar.subheader("📅 Choose Meeting Time")
selected_date = st.sidebar.date_input("Select a date")
start_time = st.sidebar.time_input("Start Time", value=time(9, 0))
end_time = st.sidebar.time_input("End Time", value=time(10, 0))

# Generate and display real-time data
iot_data = get_simulated_iot_data()
rooms_data = create_room_data(iot_data)
df = pd.DataFrame(rooms_data)

if start_time >= time(12, 0):
    df.loc[df['Room'] == "Room A", "Availability"] = 4
    df.loc[df['Room'] == "Room B", "Availability"] = 5
    df.loc[df['Room'] == "Room C", "Availability"] = 3
else:
    df.loc[df['Room'] == "Room A", "Availability"] = 3
    df.loc[df['Room'] == "Room B", "Availability"] = 4
    df.loc[df['Room'] == "Room C", "Availability"] = 5

df["Weighted Score"] = df.apply(calculate_score, axis=1)
df = df.sort_values("Weighted Score", ascending=False)

# Show live IoT data
st.subheader("📡 Live IoT Sensor Data")
for room in df["Room"]:
    st.markdown(f"**{room}** – Temp: {iot_data[room]['temp']} °C, Occupancy: {iot_data[room]['occupancy']} people")

# Visualize IoT metrics side-by-side
st.subheader("📈 IoT Metrics Visualization")
col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots(figsize=(4, 3))
    ax1.bar(df["Room"], df["HVAC Temp"], color='skyblue')
    ax1.set_ylabel("Temperature (°C)")
    ax1.set_title("HVAC Temperature")
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots(figsize=(4, 3))
    ax2.bar(df["Room"], df["Current Occupancy"], color='salmon')
    ax2.set_ylabel("Number of People")
    ax2.set_title("Current Occupancy")
    st.pyplot(fig2)

# Show the table
st.subheader("🔍 Room Comparison Table")
st.dataframe(df.reset_index(drop=True), use_container_width=True)

# Show recommended room
top_room = df.iloc[0]["Room"]
top_score = df.iloc[0]["Weighted Score"]
st.success(f"✅ Recommended Room: **{top_room}** with a score of **{top_score:.2f}**")
