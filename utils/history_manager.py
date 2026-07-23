import datetime
import pandas as pd
import streamlit as st

def init_session_history():
    """
    Initializes session state prediction history if not already present.
    """
    if "prediction_history" not in st.session_state:
        st.session_state["prediction_history"] = []
    if "total_images_processed" not in st.session_state:
        st.session_state["total_images_processed"] = 0
    if "defects_detected_count" not in st.session_state:
        st.session_state["defects_detected_count"] = 0

def add_prediction_record(filename, prediction_label, confidence, inference_time_sec, defect_info):
    """
    Adds a new prediction entry to the session state log.
    """
    init_session_history()
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = {
        "ID": len(st.session_state["prediction_history"]) + 1,
        "Timestamp": timestamp,
        "Filename": filename,
        "Prediction": prediction_label.capitalize(),
        "Confidence (%)": round(confidence * 100.0, 2),
        "Inference Time (s)": round(inference_time_sec, 4),
        "Defect Status": "Defect Detected" if defect_info.get("defect_detected", False) else "Normal",
        "Coverage (%)": defect_info.get("defect_coverage_pct", 0.0),
        "Contours Found": defect_info.get("contour_count", 0)
    }
    
    st.session_state["prediction_history"].append(record)
    st.session_state["total_images_processed"] += 1
    if defect_info.get("defect_detected", False):
        st.session_state["defects_detected_count"] += 1

def get_history_dataframe():
    """
    Returns pandas DataFrame of current prediction history.
    """
    init_session_history()
    if not st.session_state["prediction_history"]:
        return pd.DataFrame(columns=[
            "ID", "Timestamp", "Filename", "Prediction", "Confidence (%)", 
            "Inference Time (s)", "Defect Status", "Coverage (%)", "Contours Found"
        ])
    return pd.DataFrame(st.session_state["prediction_history"])

def export_history_csv():
    """
    Exports history DataFrame as CSV string.
    """
    df = get_history_dataframe()
    return df.to_csv(index=False).encode('utf-8')

def clear_history():
    """
    Clears prediction history from session state.
    """
    st.session_state["prediction_history"] = []
    st.session_state["total_images_processed"] = 0
    st.session_state["defects_detected_count"] = 0
