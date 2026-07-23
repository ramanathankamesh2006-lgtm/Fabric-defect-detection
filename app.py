import os
import streamlit as st

# 1. Streamlit Page Configuration
st.set_page_config(
    page_title="FabricAI – Intelligent Fabric Defect Detection",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Load Custom Dark Theme CSS
css_path = os.path.join(os.path.dirname(__file__), "styles", "custom.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 3. Import Page Modules
from utils.history_manager import init_session_history
from pages.dashboard import render_dashboard_page
from pages.detect import render_detect_page
from pages.history import render_history_page
from pages.analytics import render_analytics_page
from pages.model_info import render_model_info_page
from pages.settings import render_settings_page
from pages.about import render_about_page

# 4. Initialize History Session State
init_session_history()

# 5. Sidebar Navigation
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <h2 style="font-family: 'Outfit', sans-serif; background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 1.8rem; margin:0;">
        🧵 FabricAI
    </h2>
    <p style="color: #94a3b8; font-size: 0.8rem; margin-top: 4px;">v1.0 • Defect Inspector</p>
</div>
""", unsafe_allow_html=True)

nav_selection = st.sidebar.radio(
    "Navigation Menu",
    options=[
        "🏠 Dashboard",
        "📥 Upload Image",
        "🚀 Run Detection",
        "📜 Prediction History",
        "📊 Analytics",
        "⚙️ Model Information",
        "🛠️ Settings",
        "ℹ️ About"
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="padding: 0.5rem; background: rgba(30, 41, 59, 0.4); border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); text-align: center;">
    <p style="color: #34d399; font-size: 0.85rem; margin: 0; font-weight: 600;">🟢 Model Active & Ready</p>
    <p style="color: #64748b; font-size: 0.75rem; margin: 4px 0 0 0;">CNN Model Embedded</p>
</div>
""", unsafe_allow_html=True)

# 6. Page Router
if nav_selection == "🏠 Dashboard":
    render_dashboard_page()
elif nav_selection in ["📥 Upload Image", "🚀 Run Detection"]:
    render_detect_page()
elif nav_selection == "📜 Prediction History":
    render_history_page()
elif nav_selection == "📊 Analytics":
    render_analytics_page()
elif nav_selection == "⚙️ Model Information":
    render_model_info_page()
elif nav_selection == "🛠️ Settings":
    render_settings_page()
elif nav_selection == "ℹ️ About":
    render_about_page()
