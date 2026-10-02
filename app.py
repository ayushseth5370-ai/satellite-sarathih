import streamlit as st
import plotly.graph_objects as go
import numpy as np

# ==========================================
# PAGE CONFIGURATION (Professional Aerospace UI)
# ==========================================
st.set_page_config(page_title="Satellite Sārathiḥ", layout="wide")
st.markdown("<style>body, .stApp {background-color: #010101; color: #E0E0E0; font-family: 'Inter', sans-serif;}</style>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #FFFFFF; font-weight: 400; letter-spacing: 2px;'>NAKSHATRA: ACTIVE DEBRIS MITIGATION (ADR)</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #777777; font-size: 14px;'>EXECUTING IMPULSIVE DELTA-V BURN FOR ORBIT TRANSFER</p>", unsafe_allow_html=True)

# ==========================================
# 1. ORBITAL MECHANICS & MATH
# ==========================================
r_earth = 6371 
r_dead = r_earth + 400     # Decaying dangerous orbit
r_safe = r_earth + 1500    # Graveyard orbit

# Background Reference Orbits
theta_full = np.linspace(0, 2*np.pi, 120)
x_dead_full = r_dead * np.cos(theta_full)
y_dead_full = r_dead * np.sin(theta_full)
z_dead_full = np.zeros_like(theta_full)

x_safe_full = r_safe * np.cos(theta_full)
y_safe_full = r_safe * np.sin(theta_full)
z_safe_full = np.zeros_like(theta_full)

# The Transfer Trajectory (Drifting outward after the thrust)
num_frames = 90
transfer_angles = np.linspace(0, np.pi, num_frames)
r_transfer = np.linspace(r_dead, r_safe, num_frames)

x_transfer = r_transfer * np.cos(transfer_angles)
y_transfer = r_transfer * np.sin(transfer_angles)
z_transfer = r_transfer * np.sin(transfer_angles) * 0.05 # Slight inclination

# ==========================================
# 2. BUILD THE PHOTOREALISTIC SCENE
# ==========================================
fig = go.Figure()

# TRACE 0: Photorealistic Earth (High-Res)
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x_e = r_earth * np.outer(np.cos(u), np.sin(v))
y_e = r_earth * np.outer(np.sin(u), np.sin(v))
z_e = r_earth * np.outer(np.ones(np.size(u)), np.cos(v))

# Colors mimicking real satellite imagery (Deep space edge, dark oceans, muted land)
photoreal_colors = [
    [0.0, '#01091c'], [0.2, '#041738'], [0.4, '#122e15'], 
    [0.7, '#382f1f'], [0.9, '#63625e'], [1.0, '#ffffff']
]

fig.add_trace(go.Surface(
    x=x_e, y=y_e, z=z_e, colorscale=photoreal_colors, showscale=False,
    lighting=dict(ambient=0.05, diffuse=0.9, specular=0.8, roughness=0.3, fresnel=0.2),
    name='Earth Topography'
))

# TRACE 1 & 2: Orbit Lines (Thin, professional, non-distracting)
fig.add_trace(go.Scatter3d(
    x=x_dead_full, y=y_dead_full, z=z_dead_full, mode='lines',
    line=dict(color='rgba(255, 50, 50, 0.3)', width=2, dash='dash'), name='Critical Orbit'
))
fig.add_trace(go.Scatter3d(
    x=x_safe_full, y=y_safe_full, z=z_safe_full, mode='lines',
    line=dict(color='rgba(50, 255, 50, 0.3)', width=2, dash='dash'), name='Graveyard Orbit'
))

# TRACE 3: Transfer Path (Faded line showing where it will drift)
fig.add_trace(go.Scatter3d(
    x=x_transfer, y=y_transfer, z=z_transfer, mode='lines',
    line=dict(color='rgba(150, 150, 150, 0.2)', width=1), name='Predicted Coasting Path'
))

# TRACE 4: The Dead Satellite (Dark Grey, dead piece of junk)
fig.add_trace(go.Scatter3d(
    x=[x_transfer[0]], y=[y_transfer[0]], z=[z_transfer[0]], mode='markers',
    marker=dict(size=7, color='#666666', symbol='square'), name='Defunct Satellite'
))

# TRACE 5: Sārathiḥ (Active Tug - Cyan)
fig.add_trace(go.Scatter3d(
    x=[x_transfer[0] - 120], y=[y_transfer[0] - 120], z=[z_transfer[0]], mode='markers',
    marker=dict(size=5, color='#00FFFF', symbol='diamond'), name='Sārathiḥ Spacecraft'
))

# TRACE 6: Thruster Plume (Initially invisible)
fig.add_trace(go.Scatter3d(
    x=[x_transfer[0]-120, x_transfer[0]-120], y=[y_transfer[0]-120, y_transfer[0]-120], z=[0,0], 
    mode='lines', line=dict(color='rgba(0,0,0,0)', width=4), name='Thruster Plume'
))

# ==========================================
# 3. ANIMATION LOGIC (The "Little Thrust" & Drift)
# ==========================================
frames = []
for k in range(num_frames):
    x, y, z = x_transfer[k], y_transfer[k], z_transfer[k]
    tug_x, tug_y = x - 120, y - 120
    
    # THE SHORT THRUST LOGIC: 
    # Engine fires ONLY between frame 10 and 25 (Just a short push).
    if 10 <= k <= 25:
        flame_x = [tug_x, tug_x - 300]
        flame_y = [tug_y, tug_y - 300]
        flame_z = [z, z]
        flame_color = 'rgba(255, 120, 0, 1.0)' # Bright plasma orange
        flame_width = 5
    else:
        flame_x = [tug_x, tug_x]
        flame_y = [tug_y, tug_y]
        flame_z = [z, z]
        flame_color = 'rgba(0,0,0,0)' # Invisible (Engine off, just drifting)
        flame_width = 0

    frames.append(go.Frame(
        data=[
            go.Scatter3d(x=[x], y=[y], z=[z]),                   # Update Trace 4 (Dead Sat)
            go.Scatter3d(x=[tug_x], y=[tug_y], z=[z]),           # Update Trace 5 (Tug)
            go.Scatter3d(x=flame_x, y=flame_y, z=flame_z, 
                         line=dict(color=flame_color, width=flame_width)) # Update Trace 6 (Flame)
        ],
        traces=[4, 5, 6], # Tell Plotly exactly which traces to update
        name=f'frame{k}'
    ))

fig.frames = frames

# ==========================================
# 4. CINEMATIC SCENE & LOOPING ENGINE
# ==========================================
fig.update_layout(
    scene=dict(
        xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
        bgcolor='#000000', # True black
        camera=dict(eye=dict(x=1.3, y=-1.5, z=0.5)) # Perfect cinematic angle
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    height=600,
    legend=dict(x=0.01, y=0.95, font=dict(color="white"), bgcolor="rgba(0,0,0,0)"),
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        x=0.5, y=0.05, xanchor="center", yanchor="bottom",
        buttons=[dict(
            label="▶ EXECUTE ORBIT TRANSFER (LOOP)",
            method="animate",
            args=[None, {"frame": {"duration": 80, "redraw": True}, "fromcurrent": True, "mode": "immediate", "transition": {"duration": 0}, "direction": "forward", "repeat": True}]
        )]
    )]
)

st.plotly_chart(fig, use_container_width=True)

# Clean, professional HUD
st.markdown("<hr style='border: 1px solid #222;'>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Target", "NORAD-49021 (Dead)")
col2.metric("Burn Duration", "15 Frames (Impulsive)")
col3.metric("Delta-V Applied", "1.42 km/s")
col4.metric("Status", "Coasting to Graveyard")
