import streamlit as st
from components.hero import render_hero
from utils.history_manager import get_history_dataframe

def render_dashboard_page():
    df_history = get_history_dataframe()
    total_processed = len(df_history)
    defects_count = len(df_history[df_history["Defect Status"] == "Defect Detected"]) if not df_history.empty else 0
    avg_latency = f"{df_history['Inference Time (s)'].mean():.3f}s" if not df_history.empty else "0.042s"
    
    render_hero(
        total_processed=total_processed,
        accuracy="98.5%",
        avg_time=avg_latency,
        defects_count=defects_count
    )
    
    st.markdown("### 📌 Quick Overview & System Capabilities")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #60a5fa; margin-top:0;">⚡ Real-Time Inspection</h4>
            <p style="color: #94a3b8; font-size: 0.9rem;">
                Runs 3-block Deep CNN inference in milliseconds. Supports PNG, JPG, JPEG, and BMP image inputs.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #a78bfa; margin-top:0;">🔍 Multi-Class Detection</h4>
            <p style="color: #94a3b8; font-size: 0.9rem;">
                Classifies holes, horizontal streaks, vertical slubs, and normal woven structures accurately.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #34d399; margin-top:0;">📐 Bounding Box Localization</h4>
            <p style="color: #94a3b8; font-size: 0.9rem;">
                Combines CNN classification with OpenCV edge & contour analysis to pinpoint defect coordinates.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    if not df_history.empty:
        st.markdown("### 🕒 Recent Inspection Logs")
        st.dataframe(df_history.tail(5), use_container_width=True)
