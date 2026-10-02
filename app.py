import streamlit as st
import plotly.graph_objects as go
import numpy as np

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Satellite Sārathiḥ: Mitigation", layout="wide")
st.markdown("<style>body, .stApp {background-color: #020202; color: white;}</style>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #FFFFFF; font-weight: 300; font-family: sans-serif;'>NAKSHATRA: MITIGATION PLANNER</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888;'>Active Debris Removal: Initiating Orbit Raising Maneuver</p>", unsafe_allow_html=True)

fig = go.Figure()

# ==========================================
# 1. ULTRA-REALISTIC SMOOTH EARTH
# ==========================================
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
r_earth = 6371 
x_earth = r_earth * np.outer(np.cos(u), np.sin(v))
y_earth = r_earth * np.outer(np.sin(u), np.sin(v))
z_earth = r_earth * np.outer(np.ones(np.size(u)), np.cos(v))

# Deep space photorealistic color palette (Oceans, subtle landmasses, clouds)
photoreal_colors = [
    [0.0, '#000514'],     # Deep space edge/abyss
    [0.2, '#001D3D'],     # Deep ocean
    [0.5, '#003566'],     # Shallow ocean
    [0.7, '#2F3E2B'],     # Dark landmass
    [1.0, '#D3D3D3']      # Clouds/Ice
]

fig.add_trace(go.Surface(
    x=x_earth, y=y_earth, z=z_earth,
    colorscale=photoreal_colors, showscale=False,
    # Professional lighting: Strong diffuse light, sharp specular reflection for oceans
    lighting=dict(ambient=0.1, diffuse=0.8, specular=0.6, roughness=0.4, fresnel=0.2),
    name='Earth'
))

# ==========================================
# 2. ORBITAL MECHANICS (The "Push" Maneuver)
# ==========================================
angles = np.linspace(0, 2*np.pi, 200)

# Orbit 1: Current Danger Orbit (Where the dead satellite is)
r_old = r_earth + 400
x_old = r_old * np.cos(angles)
y_old = r_old * np.sin(angles)
z_old = np.zeros_like(angles)

# Orbit 2: Target Safe Graveyard Orbit (Where we are pushing it)
r_new = r_earth + 1200
# Tilting the new orbit slightly for 3D depth
x_new = r_new * np.cos(angles)
y_new = r_new * np.sin(angles) * np.cos(0.2)
z_new = r_new * np.sin(angles) * np.sin(0.2)

# Transfer Trajectory: The path taken while pushing
transfer_angles = np.linspace(0, np.pi, 100)
r_transfer = np.linspace(r_old, r_new, 100)
x_transfer = r_transfer * np.cos(transfer_angles)
y_transfer = r_transfer * np.sin(transfer_angles) * np.cos(np.linspace(0, 0.2, 100))
z_transfer = r_transfer * np.sin(transfer_angles) * np.sin(np.linspace(0, 0.2, 100))

# ==========================================
# 3. PLOTTING THE PATHS & SPACECRAFT
# ==========================================
# Draw Orbits
fig.add_trace(go.Scatter3d(
    x=x_old, y=y_old, z=z_old, mode='lines', 
    line=dict(color='rgba(255, 0, 0, 0.4)', width=2, dash='dot'), name='Decaying Orbit (Critical)'
))
fig.add_trace(go.Scatter3d(
    x=x_new, y=y_new, z=z_new, mode='lines', 
    line=dict(color='rgba(0, 255, 0, 0.4)', width=2, dash='dot'), name='Target Graveyard Orbit'
))

# Draw the Push Trajectory (Delta-v burn path)
fig.add_trace(go.Scatter3d(
    x=x_transfer, y=y_transfer, z=z_transfer, mode='lines', 
    line=dict(color='#FFA500', width=5), name='Transfer Maneuver Path'
))

# Draw the Dead Satellite (Grey, broken look)
fig.add_trace(go.Scatter3d(
    x=[x_transfer[10]], y=[y_transfer[10]], z=[z_transfer[10]], mode='markers',
    marker=dict(size=12, color='#555555', symbol='square', line=dict(color='white', width=1)),
    name='Dead Target Satellite'
))

# Draw Sārathiḥ (The active pusher satellite attached to it)
fig.add_trace(go.Scatter3d(
    # Positioned right next to the dead satellite (Pushing it)
    x=[x_transfer[10] - 150], y=[y_transfer[10] - 150], z=[z_transfer[10] - 50], mode='markers',
    marker=dict(size=8, color='#00FFFF', symbol='diamond', line=dict(color='white', width=2)),
    name='Sārathiḥ (Active Tug)'
))

# Add Exhaust/Thrust visual (A small cone/line behind Sarathih)
fig.add_trace(go.Scatter3d(
    x=[x_transfer[10]-150, x_transfer[10]-400], 
    y=[y_transfer[10]-150, y_transfer[10]-400], 
    z=[z_transfer[10]-50, z_transfer[10]-50], 
    mode='lines', line=dict(color='#00FFFF', width=3), name='Thrust Vector'
))

# ==========================================
# 4. CINEMATIC SCENE SETUP
# ==========================================
fig.update_layout(
    scene=dict(
        xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
        bgcolor='#000000', # Pitch black deep space
        camera=dict(
            # Focused camera angle on the maneuver
            eye=dict(x=0.8, y=-1.5, z=0.5),
            center=dict(x=0.1, y=0, z=0)
        )
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    height=650,
    legend=dict(x=0.02, y=0.98, font=dict(color="white"), bgcolor="rgba(0,0,0,0.5)")
)

st.plotly_chart(fig, use_container_width=True)

# Dashboard Data Panel at the bottom
col1, col2, col3 = st.columns(3)
col1.metric("Target Debris ID", "NORAD-49021", "Critical Decay")
col2.metric("Required Delta-V", "1.24 km/s", "Thrusters Engaged")
col3.metric("Transfer Status", "In Progress", "ETA: 42 mins")
