import streamlit as st

def render_hero(total_processed=0, accuracy="98.5%", avg_time="0.04s", defects_count=0):
    """
    Renders Hero section with gradient titles, system introduction, and stat cards.
    """
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">FabricAI</div>
        <div class="hero-subtitle">AI-Powered Textile Quality Inspection System</div>
        <p style="color: #cbd5e1; max-width: 750px; margin-bottom: 0;">
            Automated defect classification and localization powered by deep convolutional neural networks (CNN).
            Instantly detect <strong>holes, horizontal flaws, vertical tears</strong>, and structural weave anomalies.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Images Processed</div>
            <div class="stat-val">{total_processed}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Model Accuracy</div>
            <div class="stat-val" style="color: #34d399;">{accuracy}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Avg Inference Time</div>
            <div class="stat-val" style="color: #60a5fa;">{avg_time}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Defects Detected</div>
            <div class="stat-val" style="color: #f87171;">{defects_count}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
