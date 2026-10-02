import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# ==========================================
# PAGE CONFIGURATION (Professional Aerospace HUD)
# ==========================================
st.set_page_config(page_title="Satellite Sārathiḥ: Ultimate Dashboard", layout="wide")
st.markdown("<style>body, .stApp {background-color: #010103; color: #FFFFFF; font-family: 'Segoe UI', sans-serif;}</style>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FFFFFF; font-weight: 400; letter-spacing: 3px;'>NAKSHATRA: SATELLITE SĀRATHIḤ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00FFFF; font-size: 14px; letter-spacing: 2px;'>ACTIVE DEBRIS REMOVAL, RADAR PROXIMITY & MITIGATION SYSTEM</p>", unsafe_allow_html=True)
st.divider()

# ==========================================
# 1. LIVE METRICS & STATUS PANEL (Top Display)
# ==========================================
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Scenario 1", "Atmospheric Re-entry", "Thermal Dissolution")
m2.metric("Scenario 2", "Heavy Sat Push", "Impulsive Burn Armed")
m3.metric("Safety Protocol", "Zero Orbital Litter", "Fully Compliant")
m4.metric("Risk Engine", "Active (0-100)", "Nominal")
m5.metric("System Status", "All Systems Online", "Loop Ready")

st.divider()

# ==========================================
# 2. ORBITAL MECHANICS & SIMULATION MATH
# ==========================================
r_earth = 6371 
num_frames = 60

# Scenario 1: Small Debris Atmospheric Re-entry (Falls and burns up)
t_burn = np.linspace(0, 1, num_frames)
r_reentry = np.linspace(r_earth + 300, r_earth + 20, num_frames)
x_burn = r_reentry * np.cos(t_burn * np.pi * 0.4)
y_burn = r_reentry * np.sin(t_burn * np.pi * 0.4)
z_burn = np.zeros_like(t_burn)

# Scenario 2: Large Satellite Orbit Transfer (Impulsive Push to Graveyard)
t_transfer = np.linspace(0, np.pi * 0.7, num_frames)
r_transfer = np.linspace(r_earth + 400, r_earth + 1600, num_frames)
x_trans = r_transfer * np.cos(t_transfer)
y_trans = r_transfer * np.sin(t_transfer)
z_trans = r_transfer * np.sin(t_transfer) * 0.1

# ==========================================
# 3. BUILD THE PHOTOREALISTIC 3D SCENE
# ==========================================
fig_3d = go.Figure()

# Photorealistic Earth Topography
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x_e = r_earth * np.outer(np.cos(u), np.sin(v))
y_e = r_earth * np.outer(np.sin(u), np.sin(v))
z_e = r_earth * np.outer(np.ones(np.size(u)), np.cos(v))

terrain = np.sin(5*u)*np.cos(5*v) + 0.3*np.sin(12*u)*np.cos(12*v)
z_topo = z_e + (terrain * 80)

earth_colors = [
    [0.0, '#020b24'], [0.3, '#0b2654'], [0.5, '#1e4d2b'], 
    [0.7, '#594429'], [0.9, '#a39685'], [1.0, '#ffffff']
]

fig_3d.add_trace(go.Surface(
    x=x_e, y=y_e, z=z_topo, surfacecolor=z_topo, colorscale=earth_colors, showscale=False,
    lighting=dict(ambient=0.1, diffuse=0.85, specular=1.2, roughness=0.25, fresnel=0.1), name='Earth'
))

# Trajectory Paths
fig_3d.add_trace(go.Scatter3d(x=x_burn, y=y_burn, z=z_burn, mode='lines', line=dict(color='rgba(255, 69, 0, 0.4)', width=2), name='Re-entry Path'))
fig_3d.add_trace(go.Scatter3d(x=x_trans, y=y_trans, z=z_trans, mode='lines', line=dict(color='rgba(0, 255, 255, 0.3)', width=2, dash='dash'), name='Graveyard Transfer Path'))

# Moving Objects (Initial State)
fig_3d.add_trace(go.Scatter3d(x=[x_burn[0]], y=[y_burn[0]], z=[z_burn[0]], mode='markers', marker=dict(size=8, color='#FF4500', symbol='circle'), name='Burning Debris'))
fig_3d.add_trace(go.Scatter3d(x=[x_trans[0]], y=[y_trans[0]], z=[z_trans[0]], mode='markers', marker=dict(size=8, color='#888888', symbol='square'), name='Defunct Heavy Sat'))
fig_3d.add_trace(go.Scatter3d(x=[x_trans[0] - 100], y=[y_trans[0] - 100], z=[z_trans[0]], mode='markers', marker=dict(size=7, color='#00FFFF', symbol='diamond'), name='Sārathiḥ Tug'))
fig_3d.add_trace(go.Scatter3d(x=[0, 0], y=[0, 0], z=[0, 0], mode='lines', line=dict(color='rgba(0,0,0,0)', width=5), name='Impulsive Flame'))

# Animation Frames
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
    margin=dict(l=0, r=0, t=0, b=0), height=520,
    legend=dict(x=0.01, y=0.95, font=dict(color="white"), bgcolor="rgba(0,0,0,0)"),
    updatemenus=[dict(
        type="buttons", showactive=False, x=0.5, y=0.02, xanchor="center", yanchor="bottom",
        buttons=[dict(
            label="▶ START DUAL-SCENARIO SIMULATION",
            method="animate",
            args=[None, {"frame": {"duration": 70, "redraw": True}, "fromcurrent": True, "mode": "immediate", "transition": {"duration": 0}, "direction": "forward", "repeat": True}]
        )]
    )]
)

# ==========================================
# 4. DASHBOARD LAYOUT (Split View: 3D + Radar & Ranked List)
# ==========================================
col_left, col_right = st.columns([1.3, 1])

with col_left:
    st.markdown("### 3D AEROSPACE SIMULATION VIEW")
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
            bgcolor='#0A0A12',
            angularaxis=dict(showticklabels=False, gridcolor='#222233'),
            radialaxis=dict(range=[0, 180], showticklabels=True, gridcolor='#333344')
        ),
        margin=dict(l=20, r=20, t=20, b=20), height=220, showlegend=False
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("### RANKED HIGH-RISK DEBRIS LIST")
    df_risk = pd.DataFrame({
        "Debris ID": ["DEB-8801", "DEB-4029", "COSMOS-14", "SL-12 R/B"],
        "Miss Dist (km)": [2.1, 4.5, 12.3, 24.0],
        "Risk Score": [98, 89, 74, 52],
        "Action Status": ["Tug Deployed", "Monitor", "Warning", "Safe"]
    })
    st.dataframe(df_risk, use_container_width=True)
