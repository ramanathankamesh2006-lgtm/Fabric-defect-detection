import os
import sys
import platform
import streamlit as st
import torch
import cv2
import numpy as np
import pandas as pd
import PIL
import plotly
from model.model_pipeline import MODEL_SAVE_PATH, CLASSES, IMG_HEIGHT, IMG_WIDTH

def render_model_info_page():
    st.markdown("## ⚙️ Model Architecture & Runtime Environment")
    st.markdown("<p style='color: #94a3b8;'>Deep Neural Network specs, parameter counts, weights metadata, and runtime dependencies.</p>", unsafe_allow_html=True)
    
    # Check model file size
    model_size_str = "Unknown"
    if os.path.exists(MODEL_SAVE_PATH):
        size_mb = os.path.getsize(MODEL_SAVE_PATH) / (1024 * 1024)
        model_size_str = f"{size_mb:.2f} MB"
        
    device_str = "CUDA GPU 🚀" if torch.cuda.is_available() else "CPU 💻"
    
    # Model Specs Cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### 🧠 Model Technical Metadata")
        st.markdown(f"**Framework:** `PyTorch {torch.__version__}`")
        st.markdown(f"**Model Name:** `Fabric Defect 3-Block CNN`")
        st.markdown(f"**Weights File:** `{os.path.basename(MODEL_SAVE_PATH)}`")
        st.markdown(f"**Model Weights Size:** `{model_size_str}`")
        st.markdown(f"**Input Resolution:** `{IMG_HEIGHT} x {IMG_WIDTH} x 3 (RGB)`")
        st.markdown(f"**Class Count:** `{len(CLASSES)}` (`{', '.join(CLASSES)}`)")
        st.markdown(f"**Inference Device:** `{device_str}`")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### 💻 Runtime & Library Environment")
        st.markdown(f"**Python Version:** `{sys.version.split(' ')[0]}`")
        st.markdown(f"**OS Platform:** `{platform.system()} {platform.release()}`")
        st.markdown(f"**Streamlit:** `{st.__version__}`")
        st.markdown(f"**OpenCV (cv2):** `{cv2.__version__}`")
        st.markdown(f"**NumPy:** `{np.__version__}`")
        st.markdown(f"**Pandas:** `{pd.__version__}`")
        st.markdown(f"**Pillow (PIL):** `{PIL.__version__}`")
        st.markdown(f"**Plotly:** `{plotly.__version__}`")
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("#### 🏗️ Convolutional Network Layer Breakdown")
    st.code("""
FabricCNN (
  (features): Sequential(
    (0): Conv2d(3, 32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
    (1): ReLU()
    (2): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
    (3): Conv2d(32, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
    (4): ReLU()
    (5): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
    (6): Conv2d(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
    (7): ReLU()
    (8): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
  )
  (classifier): Sequential(
    (0): Flatten(start_dim=1, end_dim=-1)
    (1): Linear(in_features=100352, out_features=128, bias=True)
    (2): ReLU()
    (3): Dropout(p=0.5, inplace=False)
    (4): Linear(in_features=128, out_features=4, bias=True)
  )
)
Total Trainable Parameters: ~12,863,940
    """, language="python")
