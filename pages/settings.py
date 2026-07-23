import streamlit as st

def render_settings_page():
    st.markdown("## ⚙️ Application Settings")
    st.markdown("<p style='color: #94a3b8;'>Configure detection thresholds, visualization overlays, and model caching behavior.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("#### 🎯 Defect Thresholds & Contour Analysis")
    
    st.slider("Confidence Warning Threshold (%)", min_value=50, max_value=95, value=75, key="conf_thresh")
    st.slider("Minimum Contour Defect Area (px²)", min_value=5, max_value=100, value=15, key="min_area_thresh")
    st.selectbox("Heatmap Color Palette", ["JET", "TURBO", "VIRIDIS", "MAGMA", "HOT"], index=0, key="heatmap_cmap")
    
    st.markdown("---")
    st.markdown("#### 🧹 Model Caching & Memory Management")
    if st.button("Clear Model Resource Cache"):
        st.cache_resource.clear()
        st.success("Model resource cache cleared successfully!")
        
    st.markdown("</div>", unsafe_allow_html=True)
