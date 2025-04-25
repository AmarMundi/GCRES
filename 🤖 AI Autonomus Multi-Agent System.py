import streamlit as st
import random
from datetime import time

st.set_page_config(page_title="AI Multi-Agent Room Recommender", layout="wide")
st.title("🤖 Optimal Meeting Room Selector - Multi-Agent System")

st.markdown("""
This demo simulates an intelligent system powered by 8 AI agents. The system considers user preferences, environmental data, analytics, and resource availability to recommend the **most optimal meeting room**.
""")

# Shared knowledge base
class KnowledgeBase:
    def __init__(self):
        self.data = {}

    def update(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

kb = KnowledgeBase()
k_rooms = ["Room A", "Room B", "Room C"]

# Dynamic user preference inputs
st.sidebar.header("🔧 Simulate User Preferences")
max_temp = st.sidebar.slider("Preferred Max Temperature (°C)", 20, 26, 23)
need_quiet = st.sidebar.checkbox("Require Quiet Room", value=True)
need_projector = st.sidebar.checkbox("Require Projector", value=True)
k_preferences = {"quiet": need_quiet, "max_temp": max_temp, "need_projector": need_projector}
kb.update("available_rooms", k_rooms)
k_preferences = {"quiet": need_quiet, "max_temp": max_temp, "need_projector": need_projector}
kb.update("preferences", k_preferences)

# Simulated outputs from each agent (with randomized values for variation)
kb.update("environment", {
    "Room A": round(random.uniform(21, 24), 1),
    "Room B": round(random.uniform(22, 26), 1),
    "Room C": round(random.uniform(20, 23), 1)
})
k_analytics = {
    "Room A": random.choice(["Low Demand", "Medium Demand", "High Demand"]),
    "Room B": random.choice(["Low Demand", "Medium Demand", "High Demand"]),
    "Room C": random.choice(["Low Demand", "Medium Demand", "High Demand"])
}
kb.update("analytics", k_analytics)
k_alerts = random.choice([{"Room B": "Over Occupied"}, {}])
k_learning = {
    "Room A": round(random.uniform(3.0, 5.0), 1),
    "Room B": round(random.uniform(3.0, 5.0), 1),
    "Room C": round(random.uniform(3.0, 5.0), 1)
}
kb.update("alerts", k_alerts)
kb.update("learning", k_learning)
k_assets = {
    "Room A": random.choice(["OK", "Needs Cleaning"]),
    "Room B": random.choice(["OK", "Needs Cleaning"]),
    "Room C": random.choice(["OK", "Needs Cleaning"])
}
kb.update("assets", k_assets)
k_calendar = {
    "Room A": random.choice(["Free", "Busy"]),
    "Room B": random.choice(["Free", "Busy"]),
    "Room C": random.choice(["Free", "Busy"])
}
kb.update("calendar", k_calendar)

# Decision logic
def determine_optimal_room():
    final_scores = {}
    for room in k_rooms:
        score = 0
        if kb.get("calendar")[room] == "Free":
            score += 2
        if kb.get("assets")[room] == "OK":
            score += 1
        if room not in kb.get("alerts"):
            score += 1
        if kb.get("environment")[room] <= kb.get("preferences")["max_temp"]:
            score += 2
        score += kb.get("learning")[room]
        if kb.get("analytics")[room] == "Low Demand":
            score += 1
        final_scores[room] = round(score, 2)
    return max(final_scores, key=final_scores.get), final_scores

# UI Summary
st.header("📋 Agent-Based System Output")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Environment Agent")
    st.json(kb.get("environment"))
    st.subheader("Analytics Agent")
    st.json(kb.get("analytics"))

with col2:
    st.subheader("Alert Agent")
    st.json(kb.get("alerts"))
    st.subheader("Learning Agent")
    st.json(kb.get("learning"))

with col3:
    st.subheader("Asset Agent")
    st.json(kb.get("assets"))
    st.subheader("Calendar Agent")
    st.json(kb.get("calendar"))

# Final Recommendation
best_room, scores = determine_optimal_room()
st.header("✅ Final Recommended Room")
st.success(f"The most optimal meeting room is **{best_room}** based on all agents' evaluations.")

st.subheader("🏅 Score Summary")
st.write(scores)

st.caption("This recommendation is dynamically calculated from simulated data coming from 8 agents working together.")
