# 🧵 FabricAI – Intelligent Fabric Defect Detection Web Application

FabricAI is a production-ready Streamlit web application for real-time textile fabric defect inspection, classification, and visual defect localization using deep Convolutional Neural Networks (CNN) and OpenCV contour analysis.

The application fully integrates the inference pipeline and CNN model architecture from the [Fabric-Defect-Detection-System](https://github.com/Ahmed-Khalil101/Fabric-Defect-Detection-System) repository.

---

## 🌟 Key Features

* **Real Machine Learning Inference**: Uses embedded CNN model trained on 4 fabric classes (`hole`, `horizontal`, `vertical`, `normal`).
* **OpenCV Defect Localization**: Performs adaptive thresholding, edge detection, and contour extraction to draw bounding boxes and heatmaps.
* **Modern Dark Glassmorphism Design**: High-contrast dark theme, animated cards, glowing metric badges, and smooth hover effects.
* **Side-by-Side Visual Comparison**: View original fabric alongside annotated defect bounding boxes and contour heatmaps.
* **Plotly Visual Analytics**: Interactive Confidence Gauge, Class Probability Chart, and Latency Metrics.
* **Prediction History & CSV Export**: Session tracking for uploaded images, prediction labels, confidence scores, and one-click CSV export.
* **Automatic Weight Training & Caching**: Auto-generates weights if absent and leverages Streamlit `@st.cache_resource` for zero-lag performance.

---

## 📁 Project Structure

```
fabric_ai/
├── app.py                      # Main entrypoint & Streamlit layout router
├── requirements.txt            # Python package requirements
├── README.md                   # Application documentation
├── model/
│   ├── fabric_defect_model.pt  # PyTorch model weights
│   └── model_pipeline.py       # CNN architecture, training & inference code
├── utils/
│   ├── data_loader.py          # Image validation & metadata extraction
│   ├── defect_analyzer.py      # OpenCV edge detection, bounding boxes & heatmaps
│   └── history_manager.py      # Session state log & CSV export
├── components/
│   ├── hero.py                 # Hero section & stat cards
│   ├── upload_widget.py        # File drag-and-drop uploader
│   ├── results_view.py         # Prediction result badges & side-by-side view
│   └── charts.py               # Plotly Gauge & class probability distribution
├── pages/
│   ├── dashboard.py            # Overview dashboard
│   ├── detect.py               # Real-time inspection workbench
│   ├── history.py              # Prediction history logs & CSV exporter
│   ├── analytics.py            # Inspection metrics & defect distribution charts
│   ├── model_info.py           # Model architecture specs & runtime system details
│   ├── settings.py             # Defect threshold & palette settings
│   └── about.py                # Model credits & original repo references
└── styles/
    └── custom.css              # Custom CSS rules for glassmorphic styling
```

---

## 🚀 How to Run

1. Open your terminal and navigate to the project directory:
   ```bash
   cd "C:\Users\Subash R\.gemini\antigravity\scratch\fabric_ai"
   ```

2. Run the Streamlit web app:
   ```bash
   streamlit run app.py
   ```

3. Open your browser at `http://localhost:8501`.
