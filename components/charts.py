import streamlit as st
import plotly.graph_objects as go

def render_confidence_gauge(confidence_pct):
    """
    Renders a modern Plotly Gauge Chart for model prediction confidence.
    """
    gauge_color = "#10b981" if confidence_pct >= 85 else "#f59e0b" if confidence_pct >= 65 else "#ef4444"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence_pct,
        number={'suffix': "%", 'font': {'color': '#ffffff', 'size': 36}},
        title={'text': "Prediction Confidence", 'font': {'color': '#94a3b8', 'size': 16}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
            'bar': {'color': gauge_color, 'thickness': 0.75},
            'bgcolor': "rgba(15, 23, 42, 0.5)",
            'bordercolor': "rgba(255, 255, 255, 0.1)",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.15)'},
                {'range': [50, 80], 'color': 'rgba(245, 158, 11, 0.15)'},
                {'range': [80, 100], 'color': 'rgba(16, 185, 129, 0.15)'}
            ]
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20),
        height=220
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_probability_chart(probabilities_dict):
    """
    Renders Plotly Bar Chart showing probability breakdown across all fabric defect classes.
    """
    classes = [k.capitalize() for k in probabilities_dict.keys()]
    scores = [round(v * 100.0, 2) for v in probabilities_dict.values()]
    
    colors = ['#ef4444' if c == 'Hole' else '#f59e0b' if c == 'Horizontal' else '#a855f7' if c == 'Vertical' else '#10b981' for c in classes]
    
    fig = go.Figure(data=[
        go.Bar(
            x=classes,
            y=scores,
            text=[f"{s}%" for s in scores],
            textposition='auto',
            marker=dict(color=colors, line=dict(color='rgba(255,255,255,0.2)', width=1))
        )
    ])
    
    fig.update_layout(
        title=dict(text="Class Probability Distribution", font=dict(color="#f8fafc", size=16)),
        xaxis=dict(title="", tickfont=dict(color="#cbd5e1")),
        yaxis=dict(title="Probability (%)", range=[0, 105], tickfont=dict(color="#cbd5e1"), gridcolor="rgba(255,255,255,0.05)"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20),
        height=240
    )
    
    st.plotly_chart(fig, use_container_width=True)
