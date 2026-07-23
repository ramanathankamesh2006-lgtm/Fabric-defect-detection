import streamlit as st

def render_about_page():
    st.markdown("## ℹ️ About FabricAI")
    
    st.markdown("""
    <div class="glass-card">
        <h3 style="color: #60a5fa;">FabricAI – Intelligent Fabric Defect Detection System</h3>
        <p style="color: #cbd5e1; line-height: 1.6;">
            FabricAI automates textile quality control by detecting fabric defects (holes, horizontal streaks, vertical slubs, and weave inconsistencies) 
            using deep convolutional neural networks and computer vision image processing techniques.
        </p>
        <p style="color: #cbd5e1; line-height: 1.6;">
            Integrated model repository reference: 
            <a href="https://github.com/Ahmed-Khalil101/Fabric-Defect-Detection-System" target="_blank" style="color: #93c5fd;">
                GitHub: Fabric-Defect-Detection-System
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 👥 Original Model & Research Authors")
    st.markdown("""
    - **Ahmed Adel Ahmed Khalil** (202202565)
    - **Ahmed Hossam Eldin Nazmy** (202201490)
    - **Ahmed Magdy Mahmoud El Khatib** (202201913)
    - **Ibrahim Medhat Ibrahim Mady** (202204875)
    - **Khaled Walid Samir** (202200533)
    - **Khaled Mohammed Mahmoud** (202202643)
    """)
    
    st.markdown("### 🏆 Performance Benchmark")
    st.markdown("""
    - **Training Accuracy:** ~98–100%
    - **Validation Accuracy:** ~90–98%
    - **Supported Defect Classes:** `hole`, `horizontal`, `vertical`, `normal`
    """)
