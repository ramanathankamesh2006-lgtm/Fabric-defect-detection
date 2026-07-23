import streamlit as st
import numpy as np
from components.upload_widget import render_upload_widget
from components.results_view import render_results_view
from model.model_pipeline import load_fabric_model, run_inference
from utils.defect_analyzer import analyze_and_draw_defects
from utils.history_manager import add_prediction_record

@st.cache_resource
def get_cached_model():
    """
    Streamlit resource caching to ensure model loads only once across turns.
    """
    return load_fabric_model()

def render_detect_page():
    st.markdown("## 🔍 Fabric Defect Detection Workbench")
    st.markdown("<p style='color: #94a3b8;'>Upload a fabric sample to perform real-time AI classification and defect localization.</p>", unsafe_allow_html=True)
    
    uploaded_file, pil_img, metadata, is_valid, error_msg = render_upload_widget()
    
    if is_valid and uploaded_file is not None and pil_img is not None:
        st.markdown("<br>", unsafe_allow_html=True)
        btn_col, _ = st.columns([1, 2])
        with btn_col:
            run_btn = st.button("🚀 Detect Defects", key="btn_run_detection", use_container_width=True)
            
        if run_btn or st.session_state.get("last_uploaded_file") == uploaded_file.name:
            st.session_state["last_uploaded_file"] = uploaded_file.name
            
            with st.spinner("🧠 Loading AI Model & Executing Preprocessing Pipeline..."):
                try:
                    # 1. Load cached model
                    model, device = get_cached_model()
                    
                    # 2. Run real model inference
                    inference_res = run_inference(pil_img, model=model, device=device)
                    
                    # 3. Post-process & localize defect using OpenCV contour analyzer
                    annotated_rgb, heatmap_rgb, defect_info = analyze_and_draw_defects(
                        inference_res["resized_rgb"], 
                        inference_res["label"]
                    )
                    
                    # 4. Record to session state prediction history (only once per run)
                    if "current_inference_id" not in st.session_state or st.session_state["current_inference_id"] != f"{uploaded_file.name}_{inference_res['inference_time']}":
                        st.session_state["current_inference_id"] = f"{uploaded_file.name}_{inference_res['inference_time']}"
                        add_prediction_record(
                            filename=metadata["filename"],
                            prediction_label=inference_res["label"],
                            confidence=inference_res["confidence"],
                            inference_time_sec=inference_res["inference_time"],
                            defect_info=defect_info
                        )
                        
                    # 5. Display complete results
                    render_results_view(
                        original_pil=pil_img,
                        inference_result=inference_res,
                        annotated_rgb=annotated_rgb,
                        heatmap_rgb=heatmap_rgb,
                        defect_info=defect_info
                    )
                    
                except Exception as e:
                    st.error(f"⚠️ Error during inference pipeline: {str(e)}")
                    st.exception(e)
