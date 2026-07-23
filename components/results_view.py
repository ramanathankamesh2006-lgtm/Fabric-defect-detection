import streamlit as st
from components.charts import render_confidence_gauge, render_probability_chart

def render_results_view(original_pil, inference_result, annotated_rgb, heatmap_rgb, defect_info):
    """
    Renders prediction result badges, side-by-side comparison, bounding boxes, and charts.
    """
    label = inference_result["label"]
    confidence = inference_result["confidence"]
    inf_time = inference_result["inference_time"]
    probs = inference_result["probabilities"]
    
    st.markdown("### 🎯 Detection Results")
    
    # Prediction Header Card
    badge_class = f"badge-{label}"
    defect_status_str = "DEFECT DETECTED" if defect_info["defect_detected"] else "FABRIC NORMAL"
    status_color = "#f87171" if defect_info["defect_detected"] else "#34d399"
    
    st.markdown(f"""
    <div class="glass-card" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
        <div>
            <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">Classification</div>
            <div style="font-size: 1.8rem; font-weight: 800; font-family: 'Outfit', sans-serif;">
                <span class="{badge_class}">{label.upper()}</span>
            </div>
        </div>
        <div>
            <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">Status</div>
            <div style="font-size: 1.3rem; font-weight: 700; color: {status_color};">{defect_status_str}</div>
        </div>
        <div>
            <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">Confidence</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #60a5fa;">{confidence*100.0:.2f}%</div>
        </div>
        <div>
            <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">Inference Latency</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #a78bfa;">{inf_time*1000.0:.1f} ms</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Side-by-Side Comparison Section
    st.markdown("#### 🖼️ Side-by-Side Visual Inspection")
    col_orig, col_pred = st.columns(2)
    
    with col_orig:
        st.image(original_pil, caption="Original Fabric Image", use_container_width=True)
        
    with col_pred:
        tab_annotated, tab_heatmap = st.tabs(["🔴 Defect Highlights & Bboxes", "🔥 Defect Heatmap Overlay"])
        with tab_annotated:
            st.image(annotated_rgb, caption=f"Predicted Overlay ({label.upper()})", use_container_width=True)
        with tab_heatmap:
            st.image(heatmap_rgb, caption="Contour Heatmap View", use_container_width=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visual Analytics Grid (Gauge & Probability Bar Chart)
    col_gauge, col_bar = st.columns(2)
    
    with col_gauge:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        render_confidence_gauge(round(confidence * 100.0, 2))
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_bar:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        render_probability_chart(probs)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Bounding Box Breakdown Table if defect exists
    if defect_info["defect_detected"] and defect_info["bounding_boxes"]:
        st.markdown("#### 📐 Localized Defect Bounding Boxes")
        box_data = []
        for idx, b in enumerate(defect_info["bounding_boxes"]):
            box_data.append({
                "Defect #": idx + 1,
                "X Offset (px)": b["x"],
                "Y Offset (px)": b["y"],
                "Width (px)": b["w"],
                "Height (px)": b["h"],
                "Area (px²)": int(b["area"])
            })
        st.dataframe(box_data, use_container_width=True)
