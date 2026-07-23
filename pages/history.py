import streamlit as st
from components.header_bar import render_header_bar
from utils.history_manager import get_history_dataframe, export_history_csv, clear_history

def render_history_page():
    render_header_bar()
    
    st.markdown("""
    <div class="ind-panel">
        <div class="ind-panel-header">
            <span>📜 Industrial Inspection Audit Logs</span>
            <span>EXPORT & AUDIT</span>
        </div>
    """, unsafe_allow_html=True)
    
    df = get_history_dataframe()
    
    if df.empty:
        st.info("No inspection records logged in current session.")
        st.markdown("</div>", unsafe_allow_html=True)
        return
        
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    with c1:
        q = st.text_input("Search Filename", key="hist_page_search", placeholder="Filename...")
    with c2:
        f_stat = st.selectbox("Status Filter", ["All Statuses", "Defect Detected", "Normal"], key="hist_page_filt")
    with c3:
        st.download_button("📥 Export CSV", data=export_history_csv(), file_name="inspection_logs.csv", mime="text/csv", use_container_width=True)
    with c4:
        if st.button("🗑️ Clear Logs", key="hist_page_clear", use_container_width=True):
            clear_history()
            st.rerun()
            
    filtered = df.copy()
    if q:
        filtered = filtered[filtered["Filename"].str.contains(q, case=False, na=False)]
    if f_stat != "All Statuses":
        filtered = filtered[filtered["Defect Status"] == f_stat]
        
    st.dataframe(filtered, use_container_width=True, height=450)
    st.caption(f"Showing {len(filtered)} of {len(df)} total inspection logs.")
    st.markdown("</div>", unsafe_allow_html=True)
