import streamlit as st
import plotly.graph_objects as go
import numpy as np

# ==========================================
# PAGE CONFIGURATION (Professional Dark Mode)
# ==========================================
st.set_page_config(page_title="Satellite Sārathiḥ: Active Debris Removal", layout="wide")
st.markdown("<style>body, .stApp {background-color: #050505; color: white;}</style>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #CCCCCC; font-family: Arial;'>SATELLITE SĀRATHIḤ: ACTIVE ORBIT TRANSFER SIMULATION</h3>", unsafe_allow_html=True)

# ==========================================
# 1. ORBIT MATH & TRAJECTORY CALCULATIONS
# ==========================================
r_earth = 6371 
r_dead_orbit = r_earth + 400   # Lower Decaying Orbit
r_safe_orbit = r_earth + 1500  # Higher Graveyard Orbit

# Generate full orbits (for the background lines)
theta_full = np.linspace(0, 2*np.pi, 100)
x_dead_full = r_dead_orbit * np.cos(theta_full)
y_dead_full = r_dead_orbit * np.sin(theta_full)
z_dead_full = np.zeros_like(theta_full)

x_safe_full = r_safe_orbit * np.cos(theta_full)
y_safe_full = r_safe_orbit * np.sin(theta_full)
z_safe_full = np.zeros_like(theta_full)

# Generate the Transfer Path (Hohmann Transfer style)
# We will animate across 60 frames
num_frames = 60
transfer_angles = np.linspace(0, np.pi, num_frames)
r_transfer = np.linspace(r_dead_orbit, r_safe_orbit, num_frames)

x_transfer = r_transfer * np.cos(transfer_angles)
y_transfer = r_transfer * np.sin(transfer_angles)
# Add a slight 3D inclination to the transfer
z_transfer = r_transfer * np.sin(transfer_angles) * 0.1 

# ==========================================
# 2. CREATE BASE FIGURE (Earth and Orbit Lines)
# ==========================================
fig = go.Figure()

# A. Ultra-Realistic Earth (High-resolution topology simulation)
u = np.linspace(0, 2 * np.pi, 80)
v = np.linspace(0, np.pi, 80)
x_e = r_earth * np.outer(np.cos(u), np.sin(v))
y_e = r_earth * np.outer(np.sin(u), np.sin(v))
z_e = r_earth * np.outer(np.ones(np.size(u)), np.cos(v))

# Professional satellite-imagery color palette
real_earth = [[0.0, '#000a1f'], [0.3, '#001a33'], [0.6, '#1a331a'], [0.8, '#332b1a'], [1.0, '#e6e6e6']]

fig.add_trace(go.Surface(
    x=x_e, y=y_e, z=z_e, colorscale=real_earth, showscale=False,
    lighting=dict(ambient=0.1, diffuse=0.8, specular=0.4, roughness=0.6, fresnel=0.1),
    name='Earth'
))

# B. Orbit Paths (Thin, professional dashed lines)
fig.add_trace(go.Scatter3d(
    x=x_dead_full, y=y_dead_full, z=z_dead_full, mode='lines',
    line=dict(color='#880000', width=2, dash='dot'), name='Dead Orbit (400km)', hoverinfo='skip'
))
fig.add_trace(go.Scatter3d(
    x=x_safe_full, y=y_safe_full, z=z_safe_full, mode='lines',
    line=dict(color='#006600', width=2, dash='dot'), name='Graveyard Orbit (1500km)', hoverinfo='skip'
))
fig.add_trace(go.Scatter3d(
    x=x_transfer, y=y_transfer, z=z_transfer, mode='lines',
    line=dict(color='#aa6600', width=1, dash='solid'), name='Transfer Trajectory', hoverinfo='skip'
))

# C. Initial Positions for the Satellites (Frame 0)
# Dead Satellite (Grey Block)
fig.add_trace(go.Scatter3d(
    x=[x_transfer[0]], y=[y_transfer[0]], z=[z_transfer[0]], mode='markers',
    marker=dict(size=6, color='#888888', symbol='square'), name='Dead Satellite'
))
# Sārathiḥ Tug (Cyan Diamond)
fig.add_trace(go.Scatter3d(
    x=[x_transfer[0] - 150], y=[y_transfer[0] - 150], z=[z_transfer[0]], mode='markers',
    marker=dict(size=5, color='#00FFFF', symbol='diamond'), name='Sārathiḥ Tug'
))

# ==========================================
# 3. ANIMATION FRAMES (The Looping Logic)
# ==========================================
frames = []
for k in range(num_frames):
    frames.append(go.Frame(
        data=[
            # We skip the first 4 traces (Earth, 3 orbit lines) and only update the 2 satellites
            go.Scatter3d(x=[x_transfer[k]], y=[y_transfer[k]], z=[z_transfer[k]]),
            go.Scatter3d(x=[x_transfer[k] - 150], y=[y_transfer[k] - 150], z=[z_transfer[k]])
        ],
        name=f'frame{k}'
    ))
fig.frames = frames

# ==========================================
# 4. CINEMATIC LAYOUT & LOOPING BUTTONS
# ==========================================
fig.update_layout(
    scene=dict(
        xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
        bgcolor='#000000', # True black space
        camera=dict(eye=dict(x=1.2, y=-1.5, z=0.6)) # Optimal viewing angle
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    height=600,
    legend=dict(x=0.01, y=0.95, font=dict(color="white"), bgcolor="rgba(0,0,0,0)"),
    # Add the Play/Loop Button
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        x=0.5, y=0.05, xanchor="center", yanchor="bottom",
        buttons=[
            dict(
                label="▶ INITIATE ORBIT TRANSFER (LOOP)",
                method="animate",
                args=[None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True, "mode": "immediate", "transition": {"duration": 0}, "direction": "forward", "repeat": True}]
            )
        ]
    )]
)

st.plotly_chart(fig, use_container_width=True)

# Professional Telemetry Panel
st.markdown("<hr style='border: 1px solid #333;'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
col1.metric("Mission Status", "Active Docking & Push")
col2.metric("Telemetry", "Nominal Trajectory")
col3.metric("Thruster Delta-V", "1.24 km/s Firing")
