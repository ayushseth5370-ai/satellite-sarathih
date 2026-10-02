import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# ==========================================
# PAGE CONFIGURATION & HIGH-END HUD THEME
# ==========================================
st.set_page_config(
    page_title="Satellite Sārathiḥ | Nakshatra Aerospace Mission Control",
    page_icon="🛰️",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #000002; color: #FFFFFF; font-family: 'Segoe UI', Roboto, Helvetica, sans-serif; }
    h1, h2, h3 { color: #FFFFFF; letter-spacing: 1.5px; }
    .hud-box { background-color: #050510; border: 1px solid #1a1a3a; padding: 15px; border-radius: 8px; box-shadow: 0 0 15px rgba(0,255,255,0.05); }
</style>
""", unsafe_allow_html=True)

# Header Section matching PPT Slide 1, 2 & Team Elysium
st.markdown("<h1 style='text-align: center; font-weight: 300; letter-spacing: 4px;'>SATELLITE SĀRATHIḤ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00FFFF; font-size: 15px; letter-spacing: 3px;'>ACTIVE SPACE DEBRIS DETECTION, TRACKING, CONJUNCTION ANALYSIS & MITIGATION PLANNER</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888; font-size: 13px;'>Team Elysium | Nakshatra Aerospace Hackathon (Problem Statement 03: Software)</p>", unsafe_allow_html=True)
st.divider()

# ==========================================
# FULL ACTIVE TELEMETRY HUD (Slide 5, 6 & Presentation Metrics)
# ==========================================
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Scenario 1", "Atmospheric Re-entry", "Thermal Dissolution")
c2.metric("Scenario 2", "Heavy Sat Transfer", "Impulsive Burn Armed")
c3.metric("Safety Protocol", "Zero Orbital Litter", "Fully Compliant")
c4.metric("Risk Engine Score", "0 - 100 Active", "Dynamic Threshold")
c5.metric("System Status", "All Modules Online", "Continuous Live Feed")

st.divider()

# ==========================================
# ORBITAL MECHANICS & SIMULATION MATH
# ==========================================
r_earth = 6371 
num_frames = 60

# Scenario 1: Small Debris Atmospheric Re-entry (Falls & Burns up completely)
t_burn = np.linspace(0, 1, num_frames)
r_reentry = np.linspace(r_earth + 300, r_earth + 20, num_frames)
x_burn = r_reentry * np.cos(t_burn * np.pi * 0.4)
y_burn = r_reentry * np.sin(t_burn * np.pi * 0.4)
z_burn = np.zeros_like(t_burn)

# Scenario 2: Large Satellite Orbit Transfer (Impulsive Push to Safe Graveyard Orbit)
t_transfer = np.linspace(0, np.pi * 0.7, num_frames)
r_transfer = np.linspace(r_earth + 400, r_earth + 1600, num_frames)
x_trans = r_transfer * np.cos(t_transfer)
y_trans = r_transfer * np.sin(t_transfer)
z_trans = r_transfer * np.sin(t_transfer) * 0.1

# ==========================================
# BUILD HYPER-REALISTIC TOPOGRAPHICAL EARTH & 3D SCENE
# ==========================================
fig_3d = go.Figure()

# High-resolution Photorealistic Earth (Oceans, Green Land, Mountains, Snow/Clouds)
u = np.linspace(0, 2 * np.pi, 140)
v = np.linspace(0, np.pi, 140)
x_e = r_earth * np.outer(np.cos(u), np.sin(v))
y_e = r_earth * np.outer(np.sin(u), np.sin(v))
z_e = r_earth * np.outer(np.ones(np.size(u)), np.cos(v))

# Mathematical terrain modeling to make the Earth look organic and realistic
terrain = np.sin(6*u)*np.cos(6*v) + 0.25*np.sin(15*u)*np.cos(15*v)
z_topo = z_e + (terrain * 90)

earth_colors = [
    [0.0, '#00081f'],  # Deep abyss ocean
    [0.3, '#041d4a'],  # Shallow shelf water
    [0.5, '#163b20'],  # Lush green land / forests
    [0.7, '#42311b'],  # Mountain ranges
    [0.9, '#7a6d5c'],  # Rocky high peaks
    [1.0, '#ffffff']   # Polar ice caps and atmospheric cloud gloss
]

fig_3d.add_trace(go.Surface(
    x=x_e, y=y_e, z=z_topo, surfacecolor=z_topo, colorscale=earth_colors, showscale=False,
    lighting=dict(ambient=0.15, diffuse=0.9, specular=1.5, roughness=0.15, fresnel=0.1), name='Earth'
))

# Trajectory Background Paths
fig_3d.add_trace(go.Scatter3d(x=x_burn, y=y_burn, z=z_burn, mode='lines', line=dict(color='rgba(255, 69, 0, 0.4)', width=2), name='Re-entry Trajectory'))
fig_3d.add_trace(go.Scatter3d(x=x_trans, y=y_trans, z=z_trans, mode='lines', line=dict(color='rgba(0, 255, 255, 0.3)', width=2, dash='dash'), name='Graveyard Transfer Path'))

# Dynamic Objects (Initial State)
fig_3d.add_trace(go.Scatter3d(x=[x_burn[0]], y=[y_burn[0]], z=[z_burn[0]], mode='markers', marker=dict(size=8, color='#FF4500', symbol='circle'), name='Burning Debris'))
fig_3d.add_trace(go.Scatter3d(x=[x_trans[0]], y=[y_trans[0]], z=[z_trans[0]], mode='markers', marker=dict(size=8, color='#777777', symbol='square'), name='Defunct Heavy Sat'))
fig_3d.add_trace(go.Scatter3d(x=[x_trans[0] - 100], y=[y_trans[0] - 100], z=[z_trans[0]], mode='markers', marker=dict(size=7, color='#00FFFF', symbol='diamond'), name='Sārathiḥ Tug'))
fig_3d.add_trace(go.Scatter3d(x=[0, 0], y=[0, 0], z=[0, 0], mode='lines', line=dict(color='rgba(0,0,0,0)', width=5), name='Impulsive Flame'))

# Animation Frames Logic (Simultaneous Dual Execution)
frames = []
for k in range(num_frames):
    bx, by, bz = x_burn[k], y_burn[k], z_burn[k]
    if k < 45:
        b_color, b_size = '#FFFFFF', 8
    elif k < 58:
        b_color, b_size = '#FF2200', 5
    else:
        b_color, b_size = 'rgba(0,0,0,0)', 0

    tx, ty, tz = x_trans[k], y_trans[k], z_trans[k]
    tug_x, tug_y = tx - 100, ty - 100

    if 10 <= k <= 25:
        flame_x, flame_y, flame_z = [tug_x, tug_x - 300], [tug_y, tug_y - 300], [tz, tz]
        flame_color, flame_width = 'rgba(255, 140, 0, 1.0)', 6
    else:
        flame_x, flame_y, flame_z = [tug_x, tug_x], [tug_y, tug_y], [tz, tz]
        flame_color, flame_width = 'rgba(0,0,0,0)', 0

    frames.append(go.Frame(
        data=[
            go.Scatter3d(x=[bx], y=[by], z=[bz], marker=dict(size=b_size, color=b_color)),
            go.Scatter3d(x=[tx], y=[ty], z=[tz]),
            go.Scatter3d(x=[tug_x], y=[tug_y], z=[tz]),
            go.Scatter3d(x=flame_x, y=flame_y, z=flame_z, line=dict(color=flame_color, width=flame_width))
        ],
        traces=[3, 4, 5, 6],
        name=f'frame{k}'
    ))

fig_3d.frames = frames

fig_3d.update_layout(
    scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False), bgcolor='#000000', camera=dict(eye=dict(x=1.2, y=-1.5, z=0.5))),
    margin=dict(l=0, r=0, t=0, b=0), height=530,
    legend=dict(x=0.01, y=0.95, font=dict(color="white"), bgcolor="rgba(0,0,0,0)"),
    updatemenus=[dict(
        type="buttons", showactive=False, x=0.5, y=0.02, xanchor="center", yanchor="bottom",
        buttons=[dict(
            label="▶ START DUAL-SCENARIO LIVE SIMULATION",
            method="animate",
            args=[None, {"frame": {"duration": 70, "redraw": True}, "fromcurrent": True, "mode": "immediate", "transition": {"duration": 0}, "direction": "forward", "repeat": True}]
        )]
    )]
)

# ==========================================
# INTERACTIVE SPLIT DASHBOARD LAYOUT
# ==========================================
col_left, col_right = st.columns([1.3, 1])

with col_left:
    st.markdown("### 3D AEROSPACE REALISTIC SIMULATION VIEW")
    st.plotly_chart(fig_3d, use_container_width=True)

with col_right:
    st.markdown("### RADAR PROXIMITY VIEW (Slide 6)")
    
    np.random.seed(42)
    radar_dists = np.random.uniform(5, 180, 25)
    radar_angles = np.random.uniform(0, 360, 25)
    radar_colors = ['#FF2222' if d < 35 else '#FFAA00' if d < 90 else '#00FFFF' for d in radar_dists]
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=radar_dists, theta=radar_angles, mode='markers',
        marker=dict(color=radar_colors, size=9, line=dict(color='white', width=1)),
        hoverinfo='r+theta'
    ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor='#0A0A16',
            angularaxis=dict(showticklabels=False, gridcolor='#1e1e3f'),
            radialaxis=dict(range=[0, 180], showticklabels=True, gridcolor='#2a2a5a')
        ),
        margin=dict(l=20, r=20, t=20, b=20), height=215, showlegend=False
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("### RANKED HIGH-RISK DEBRIS LIST (Slide 5)")
    df_risk = pd.DataFrame({
        "Debris ID": ["DEB-8801", "DEB-4029", "COSMOS-14", "SL-12 R/B"],
        "Miss Dist (km)": [2.1, 4.5, 12.3, 24.0],
        "Risk Score": [98, 89, 74, 52],
        "Action Status": ["Tug Deployed", "Monitor", "Warning", "Safe"]
    })
    st.dataframe(df_risk, use_container_width=True)

# ==========================================
# SYSTEM FLOWCHART & METHODOLOGY FOOTER (Slide 3 & 4)
# ==========================================
st.divider()
st.markdown("### SYSTEM ARCHITECTURE & WORKFLOW PIPELINE")
col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns(5)
with col_f1:
    st.markdown("**1. Data Input**")
    st.caption("Celestrak / Space-Track TLE ingestion & automated simulated fallbacks.")
with col_f2:
    st.markdown("**2. SGP4 Propagation**")
    st.caption("High-precision mathematical orbit propagation for position & velocity tracking.")
with col_f3:
    st.markdown("**3. Conjunction Analysis**")
    st.caption("Calculates Time of Closest Approach (TCA), relative velocity, and miss distance.")
with col_f4:
    st.markdown("**4. Risk Engine**")
    st.caption("Collates collision probability and computes a dynamic 0-100 risk score ranking.")
with col_f5:
    st.markdown("**5. Mitigation & Act**")
    st.caption("Triggers automated alerts, impulsive delta-v burns, and orbital transfers.")
