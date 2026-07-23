import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.history_manager import get_history_dataframe

def render_analytics_page():
    st.markdown("## 📊 Inspection Analytics & Insights")
    st.markdown("<p style='color: #94a3b8;'>Statistical analysis of inspection volume, defect occurrences, and latency trends.</p>", unsafe_allow_html=True)
    
    df = get_history_dataframe()
    
    if df.empty:
        st.info("ℹ️ Analytics will update automatically once fabric images are inspected.")
        return
        
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Inspections", len(df))
    with c2:
        defects = len(df[df["Defect Status"] == "Defect Detected"])
        st.metric("Defects Found", defects, delta=f"{round((defects/len(df))*100, 1)}% Rate")
    with c3:
        avg_conf = f"{df['Confidence (%)'].mean():.1f}%"
        st.metric("Average Confidence", avg_conf)
    with c4:
        avg_time = f"{df['Inference Time (s)'].mean()*1000:.1f} ms"
        st.metric("Avg Latency", avg_time)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_pie, col_scatter = st.columns(2)
    
    with col_pie:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        counts = df["Prediction"].value_counts().reset_index()
        counts.columns = ["Class", "Count"]
        
        colors = {'Hole': '#ef4444', 'Horizontal': '#f59e0b', 'Vertical': '#a855f7', 'Normal': '#10b981'}
        fig_pie = px.pie(
            counts, values="Count", names="Class", 
            title="Defect Class Distribution",
            color="Class",
            color_discrete_map=colors,
            hole=0.4
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc")
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_scatter:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        fig_scat = px.scatter(
            df, x="Inference Time (s)", y="Confidence (%)", 
            color="Prediction",
            title="Confidence vs. Inference Latency",
            hover_data=["Filename"]
        )
        fig_scat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)")
        )
        st.plotly_chart(fig_scat, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
