# NOTE: This Streamlit app must be run in a local environment where 'streamlit' and 'pandas' are installed.

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime, time

# --- Multi-Agent System Components ---
class KnowledgeBase:
    def __init__(self):
        self.data = {}

    def update(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key, None)

class BookingAgent:
    def __init__(self, kb):
        self.kb = kb

    def find_room(self, preferences):
        rooms = self.kb.get("available_rooms")
        sensor_data = self.kb.get("sensor_data")
        for room in rooms:
            if sensor_data[room]["temp"] < preferences.get("max_temp", 23):
                return room
        return None

class EnvironmentAgent:
    def __init__(self, kb):
        self.kb = kb

    def fetch_sensor_data(self):
        data = {
            "Room A": {"temp": round(random.uniform(21, 23.5), 1), "occupancy": random.randint(1, 6)},
            "Room B": {"temp": round(random.uniform(23, 25.5), 1), "occupancy": random.randint(2, 8)},
            "Room C": {"temp": round(random.uniform(20, 22.5), 1), "occupancy": random.randint(1, 5)}
        }
        self.kb.update("sensor_data", data)

class NLPChatAgent:
    def __init__(self, kb, booking_agent):
        self.kb = kb
        self.booking_agent = booking_agent

    def handle_query(self, preferences):
        room = self.booking_agent.find_room(preferences)
        if room:
            return f"✅ I have booked **{room}** for you."
        return "⚠️ No suitable room found."

# --- Streamlit UI Setup ---
st.set_page_config(page_title="AI-Powered Room Selector", layout="wide")
st.title("🤖 AI-Powered Conference Room Selector")

st.markdown("""
This tool uses a simple AI agent system to suggest the best room based on live IoT sensor data and user preferences.
""")

# Initialize agents and knowledge base
kb = KnowledgeBase()
k_env = EnvironmentAgent(kb)
k_book = BookingAgent(kb)
k_chat = NLPChatAgent(kb, k_book)

kb.update("available_rooms", ["Room A", "Room B", "Room C"])
k_env.fetch_sensor_data()

# Input preferences
temp_preference = st.slider("Max Room Temperature (°C)", 20, 26, 23)
if st.button("Ask AI Agent to Book Room"):
    preferences = {"max_temp": temp_preference}
    st.markdown(k_chat.handle_query(preferences))

# Show live sensor data
data = kb.get("sensor_data")
df = pd.DataFrame.from_dict(data, orient='index')
df.reset_index(inplace=True)
df.rename(columns={'index': 'Room'}, inplace=True)
st.subheader("📡 Live IoT Sensor Data")
st.dataframe(df)

# Charts
st.subheader("📈 Sensor Visualization")
col1, col2 = st.columns(2)
with col1:
    fig1, ax1 = plt.subplots(figsize=(4, 3))
    ax1.bar(df["Room"], df["temp"], color='skyblue')
    ax1.set_ylabel("Temperature (°C)")
    ax1.set_title("HVAC Temperature")
    st.pyplot(fig1)
with col2:
    fig2, ax2 = plt.subplots(figsize=(4, 3))
    ax2.bar(df["Room"], df["occupancy"], color='salmon')
    ax2.set_ylabel("Occupancy")
    ax2.set_title("Current Occupancy")
    st.pyplot(fig2)
