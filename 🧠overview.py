import streamlit as st

IMAGE_URL = "https://media.githubusercontent.com/media/NVIDIA/AgentIQ/develop/docs/source/_static/agentiq_gitdiagram.png"


st.image(IMAGE_URL, caption="NVIDIA AgentIQ")



st.write(
    """

"""
)

st.markdown("### 🧠 Multi-Agent System Overview")
st.markdown("""
| Agent | Role |
|-------|------|
| 🔁 **Booking Agent** | Manages reservations, conflict resolution, learns user behavior |
| 🌡️ **Environment Agent** | Controls HVAC, lighting, and suggests rooms based on environmental conditions |
| 📊 **Analytics Agent** | Predicts usage trends, demand peaks, and detects anomalies |
| 📢 **Alert Agent** | Monitors sensors, flags irregularities, notifies stakeholders |
| 🧠 **Learning Agent** | Learns from usage patterns, adapts preferences, updates policies |
| 💬 **NLP Chat Agent** | Interfaces with users via text or voice for booking/info |
| 📦 **Asset Manager Agent** | Tracks consumables, assets, maintenance needs |
| 📅 **Calendar Agent** | Integrates with external calendars to manage schedules and rescheduling |
""")
