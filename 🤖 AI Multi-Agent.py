import streamlit as st

# Shared state
class KnowledgeBase:
    def __init__(self):
        self.data = {}

    def update(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key, None)

# Initialize KB
kb = KnowledgeBase()
kb.update("available_rooms", ["Room A", "Room B", "Room C"])

# App UI setup
st.set_page_config(page_title="Multi-Agent Facility AI Demo", layout="wide")
st.title("🤖 Multi-Agent AI Demo for Smart Facilities")

st.markdown("""
This is a simulation of 8 AI agents managing a smart facility. Each tab represents an agent's functionality. Try interacting with each and watch how they collaborate!
""")

tabs = st.tabs([
    "🏠 Booking Agent", "🌡️ Environment Agent", "📊 Analytics Agent",
    "📢 Alert Agent", "🧠 Learning Agent", "💬 Chat Agent",
    "📦 Asset Agent", "📅 Calendar Agent", "📋 Summary"
])

# 1. Booking Agent
tabs[0].subheader("🏠 Booking Agent")
selected_date = tabs[0].date_input("Select a booking date")
time_slot = tabs[0].time_input("Select time slot")
if tabs[0].button("Book Room"):
    tabs[0].success("Room booked based on availability and preferences!")

# 2. Environment Agent
tabs[1].subheader("🌡️ Environment Agent")
tabs[1].markdown("Live Temperature: 22.4°C\n\nOccupancy: 4 people")
if tabs[1].button("Optimize HVAC"):
    tabs[1].info("HVAC settings adjusted for energy efficiency.")

# 3. Analytics Agent
tabs[2].subheader("📊 Analytics Agent")
tabs[2].markdown("Predicted peak demand: 2 PM - 4 PM\n\nEnergy usage high in Room B")

# 4. Alert Agent
tabs[3].subheader("📢 Alert Agent")
if tabs[3].button("Simulate Over-Occupancy Alert"):
    tabs[3].warning("Room A exceeded max capacity! Notified admin.")

# 5. Learning Agent
tabs[4].subheader("🧠 Learning Agent")
tabs[4].markdown("User Jane prefers Room A for afternoon meetings.\n\nUser Bob avoids Room C due to lighting.")

# 6. Chat Agent
tabs[5].subheader("💬 Chat Agent")
query = tabs[5].text_input("Ask the AI:", "Find me a room with low noise at 3 PM")
if tabs[5].button("Send"):
    tabs[5].markdown("🤖 Recommended: Room A — Quiet & available at 3 PM")

# 7. Asset Agent
tabs[6].subheader("📦 Asset Agent")
tabs[6].markdown("Projector stock: OK\n\nWhiteboard markers: Low\n\nLast maintenance: Room B — 3 days ago")

# 8. Calendar Agent
tabs[7].subheader("📅 Calendar Agent")
tabs[7].markdown("Meeting: Design Sprint — Room C at 2 PM\n\nAvailability clash resolved by shifting to Room A")

# 9. Summary Tab
tabs[8].subheader("📋 System Summary")
tabs[8].markdown("**Agents executed:** Booking ✅, Environment ✅, Alert ⚠️\n\n**Preferred Room:** Room A\n\n**Next Action:** Send maintenance to Room B")
