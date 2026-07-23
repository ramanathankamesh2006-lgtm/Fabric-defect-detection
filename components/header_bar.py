import datetime
import streamlit as st

def render_header_bar(operator_id="Op-4092", camera_id="CAM-01 (Line 4)", model_ver="v1.4.2-CNN"):
    """
    Renders Vercel / Linear-grade Header Navigation Bar.
    """
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    st.markdown(f"""
    <div class="saas-header">
        <div class="saas-brand">
            <span>🧵 FabricAI</span>
            <span class="saas-badge-online">● ACTIVE</span>
        </div>
        <div style="display: flex; gap: 2rem; align-items: center;">
            <div style="display: flex; flex-direction: column;">
                <span style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; color: #64748B;">Camera Source</span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 600; color: #0F172A;">{camera_id}</span>
            </div>
            <div style="display: flex; flex-direction: column;">
                <span style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; color: #64748B;">Operator ID</span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 600; color: #0F172A;">{operator_id}</span>
            </div>
            <div style="display: flex; flex-direction: column;">
                <span style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; color: #64748B;">Model Engine</span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 600; color: #0F172A;">{model_ver}</span>
            </div>
            <div style="display: flex; flex-direction: column;">
                <span style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; color: #64748B;">Timestamp</span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 600; color: #0F172A;">{now_str}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
