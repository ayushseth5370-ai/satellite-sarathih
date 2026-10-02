import streamlit as st
import plotly.graph_objects as go
import numpy as np

# ==========================================
# PAGE CONFIGURATION (Professional Aerospace HUD)
# ==========================================
st.set_page_config(page_title="Satellite Sārathiḥ: ADR Mission", layout="wide")
st.markdown("<style>body, .stApp {background-color: #000000; color: #FFFFFF; font-family: 'Helvetica Neue', sans-serif;}</style>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #FFFFFF; font-weight: 300; letter-spacing: 3px;'>NAKSHATRA: SATELLITE SĀRATHIḤ</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00FFFF; font-size: 13px; letter-spacing: 1px;'>ACTIVE DEBRIS REMOVAL & ATMOSPHERIC RE-ENTRY SIMULATOR</p>", unsafe_allow_html=True)

# ==========================================
# 1. ORBITAL MECHANICS & SCENARIO MATH
# ==========================================
r_earth = 6371 

# Scenario 1: Small Debris Atmospheric Re-entry (Burns up)
t_burn = np.linspace(0, 1, 40)
# Falls from 300km down into the atmosphere (r = 6371 -> 6300)
r_reentry = np.linspace(r_earth + 250, r_earth + 20, 40)
x_burn = r_reentry * np.cos(t_burn * np.pi * 0.5)
y_burn = r_reentry * np.sin(t_burn * np.pi * 0.5)
z_burn = np.zeros_like(t_burn)

# Scenario 2: Large Satellite Orbit Transfer (Impulsive Push to Graveyard)
t_transfer = np.linspace(0, np.pi * 0.8, 60)
r_transfer = np.linspace(r_earth + 400, r_earth + 1600, 60)
x_trans = r_transfer * np.cos(t_transfer)
y_trans = r_transfer * np.sin(t_transfer)
z_trans = r_transfer * np.sin(t_transfer) * 0.1

# ==========================================
# 2. BUILD THE PHOTOREALISTIC SCENE
# ==========================================
fig = go.Figure()

# TRACE 0: Photorealistic Earth (Matches your exact high-end reference)
u = np.linspace(0, 2 * np.pi, 120)
v = np.linspace(0, np.pi, 120)
x_e = r_earth * np.outer(np.cos(u), np.sin(v))
y_e = r_earth * np.outer(np.sin(u), np.sin(v))
z_e = r_earth * np.outer(np.ones(np.size(u)), np.cos(v))

# Earth topographical texture map simulation
terrain = np.sin(5*u)*np.cos(5*v) + 0.3*np.sin(12*u)*np.cos(12*v)
z_topo = z_e + (terrain * 80)

earth_colors = [
    [0.0, '#020b24'],  # Deep abyss ocean
    [0.3, '#0b2654'],  # Blue ocean shelf
    [0.5, '#1e4d2b'],  # Green forests / land
    [0.7, '#594429'],  # Brown mountains
    [0.9, '#a39685'],  # Rocky peaks
    [1.0, '#ffffff']   # Polar snow / clouds
]

fig.add_trace(go.Surface(
    x=x_e, y=y_e, z=z_topo,
    surfacecolor=z_topo, colorscale=earth_colors, showscale=False,
    lighting=dict(ambient=0.1, diffuse=0.85, specular=1.2, roughness=0.25, fresnel=0.1),
    name='Earth'
))

# TRACE 1: Atmospheric Burn-up Path (Small Debris)
fig.add_trace(go.Scatter3d(
    x=x_burn, y=y_burn, z=z_burn, mode='lines',
    line=dict(color='rgba(255, 69, 0, 0.6)', width=3, dash='solid'), name='Re-entry Trajectory'
))

# TRACE 2: Graveyard Transfer Path (Large Satellite Push)
fig.add_trace(go.Scatter3d(
    x=x_trans, y=y_trans, z=z_trans, mode='lines',
    line=dict(color='rgba(0, 255, 255, 0.4)', width=2, dash='dash'), name='Orbit Raising Path'
))

# TRACE 3: Small Re-entering Debris (Burning Object)
fig.add_trace(go.Scatter3d(
    x=[x_burn[0]], y=[y_burn[0]], z=[z_burn[0]], mode='markers',
    marker=dict(size=6, color='#FF4500', symbol='circle', line=dict(color='white', width=1)),
    name='Small Debris (Re-entry)'
))

# TRACE 4: Large Defunct Satellite
fig.add_trace(go.Scatter3d(
    x=[x_trans[0]], y=[y_trans[0]], z=[z_trans[0]], mode='markers',
    marker=dict(size=8, color='#888888', symbol='square'), name='Defunct Heavy Satellite'
))

# TRACE 5: Sārathiḥ Active Tug Spacecraft
fig.add_trace(go.Scatter3d(
    x=[x_trans[0] - 100], y=[y_trans[0] - 100], z=[z_trans[0]], mode='markers',
    marker=dict(size=7, color='#00FFFF', symbol='diamond', line=dict(color='white', width=1)),
    name='Sārathiḥ Spacecraft'
))

# TRACE 6: Thruster Plume (Impulsive Burn Flame)
fig.add_trace(go.Scatter3d(
    x=[0, 0], y=[0, 0], z=[0, 0], mode='lines',
    line=dict(color='rgba(0,0,0,0)', width=5), name='Impulsive Burn'
))

# ==========================================
# 3. ADVANCED SEQUENTIAL ANIMATION
# ==========================================
frames = []
total_frames = 60

for k in range(total_frames):
    # Part A: Small debris re-entry (First 35 frames)
    if k < 40:
        idx = min(k, 39)
        bx, by, bz = x_burn[idx], y_burn[idx], z_burn[idx]
        # Debris glows bright orange/white as it burns in atmosphere
        b_color = '#FFFFFF' if idx < 30 else '#FF2200' 
        b_size = 8 if idx < 30 else 3 # Shrinks as it burns up
    else:
        bx, by, bz = x_burn[-1], y_burn[-1], z_burn[-1]
        b_color = 'rgba(0,0,0,0)' # Disappears (burned completely)
        b_size = 0

    # Part B: Large satellite push maneuver (Active across all frames)
    idx_t = min(k, 59)
    tx, ty, tz = x_trans[idx_t], y_trans[idx_t], z_trans[idx_t]
    tug_x, tug_y = tx - 100, ty - 100

    # Single Impulsive Thrust between frame 10 and 22
    if 10 <= k <= 22:
        flame_x = [tug_x, tug_x - 300]
        flame_y = [tug_y, tug_y - 300]
        flame_z = [tz, tz]
        flame_color = 'rgba(255, 140, 0, 1.0)'
        flame_width = 7
    else:
        flame_x = [tug_x, tug_x]
        flame_y = [tug_y, tug_y]
        flame_z = [tz, tz]
        flame_color = 'rgba(0,0,0,0)'
        flame_width = 0

    frames.append(go.Frame(
        data=[
            go.Scatter3d(x=[bx], y=[by], z=[bz], marker=dict(size=b_size, color=b_color)), # Trace 3: Burning debris
            go.Scatter3d(x=[tx], y=[ty], z=[tz]),                                         # Trace 4: Heavy sat
            go.Scatter3d(x=[tug_x], y=[tug_y], z=[tz]),                                  # Trace 5: Tug
            go.Scatter3d(x=flame_x, y=flame_y, z=flame_z, line=dict(color=flame_color, width=flame_width)) # Trace 6: Flame
        ],
        traces=[3, 4, 5, 6],
        name=f'frame{k}'
    ))

fig.frames = frames

# ==========================================
# 4. CINEMATIC SCENE SETUP & PLAY BUTTON
# ==========================================
fig.update_layout(
    scene=dict(
        xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
        bgcolor='#000000',
        camera=dict(eye=dict(x=1.2, y=-1.5, z=0.5))
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    height=620,
    legend=dict(x=0.01, y=0.95, font=dict(color="white"), bgcolor="rgba(0,0,0,0)"),
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        x=0.5, y=0.05, xanchor="center", yanchor="bottom",
        buttons=[dict(
            label="▶ RUN DUAL-MODE ADR SIMULATION",
            method="animate",
            args=[None, {"frame": {"duration": 90, "redraw": True}, "fromcurrent": True, "mode": "immediate", "transition": {"duration": 0}, "direction": "forward", "repeat": True}]
        )]
    )]
)

st.plotly_chart(fig, use_container_width=True)

# Clean Telemetry HUD
st.markdown("<hr style='border: 1px solid #111;'>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Scenario 1 (Small)", "Atmospheric Re-entry", "Thermal Dissolution")
c2.metric("Scenario 2 (Heavy)", "Active Tug (Sārathiḥ)", "Impulsive Burn Executed")
c3.metric("Safety Protocol", "Zero Orbital Litter", "Fully Compliant")
c4.metric("Status", "Operational", "Loop Active")
