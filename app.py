import streamlit as st
import plotly.graph_objects as go
import numpy as np
from skyfield.api import load, EarthSatellite

# ---------------------------------------------------------
# UI Setup & Headers
# ---------------------------------------------------------
st.set_page_config(page_title="Satellite Sārathiḥ: Cinematic Simulation", page_icon="🛰️", layout="wide")
st.title("🛰️ NAKSHATRA: Satellite Sārathiḥ")
st.markdown("### Real-time Space Debris Tracking & Conjunction Analysis")

# ---------------------------------------------------------
# 1. ORBITAL ENGINE (Simulating a Massive Debris Catalog)
# ---------------------------------------------------------
ts = load.timescale()
t = ts.now()

# Simulating our Target Spacecraft (ISS Orbit for realism)
iss_tle_line1 = '1 25544U 98067A   23277.48512345  .00016717  00000-0  30043-3 0  9997'
iss_tle_line2 = '2 25544  51.6415 152.0360 0005010 326.6575  70.6273 15.49842407418706'
iss_sat = EarthSatellite(iss_tle_line1, iss_tle_line2, 'Sārathiḥ Target', ts)

# Projecting the orbit path
minutes = np.arange(0, 180, 2)
times = ts.utc(2026, 10, 3, 0, minutes)
iss_positions = iss_sat.at(times).position.km
iss_x, iss_y, iss_z = iss_positions[0], iss_positions[1], iss_positions[2]

# Generating a Massive Debris Cloud (500 objects)
num_debris = 500
np.random.seed(42) 
debris_radii = np.random.uniform(6371 + 200, 6371 + 1000, num_debris)
debris_angles = np.random.uniform(0, 2 * np.pi, num_debris)
debris_inclinations = np.random.uniform(-np.pi / 2, np.pi / 2, num_debris)

debris_x, debris_y, debris_z, debris_colors = [], [], [], []

for i in range(num_debris):
    r = debris_radii[i]
    phi = debris_angles[i]
    theta = debris_inclinations[i]
    
    debris_x.append(r * np.cos(phi) * np.cos(theta))
    debris_y.append(r * np.sin(phi) * np.cos(theta))
    debris_z.append(r * np.sin(theta))
    
    # Risk Engine: Altitude proximity coloring
    alt = r - 6371
    if alt < 350:
        debris_colors.append('#FF0000') # Critical (Red)
    elif alt < 500:
        debris_colors.append('#FFA500') # Warning (Orange)
    else:
        debris_colors.append('#555555') # Safe (Dark Grey)

# ---------------------------------------------------------
# 2. CINEMATIC 3D RENDERING
# ---------------------------------------------------------
fig = go.Figure()

# A. The Realistic Earth (Custom palette + Specular Lighting)
u = np.linspace(0, 2 * np.pi, 80)
v = np.linspace(0, np.pi, 80)
r_earth = 6371 
x_earth = r_earth * np.outer(np.cos(u), np.sin(v))
y_earth = r_earth * np.outer(np.sin(u), np.sin(v))
z_earth = r_earth * np.outer(np.ones(np.size(u)), np.cos(v))

earth_colors = [
    [0.0, '#000033'], [0.2, '#003366'], [0.4, '#2e8b57'], 
    [0.6, '#556b2f'], [0.8, '#8b4513'], [1.0, '#ffffff']
]

fig.add_trace(go.Surface(
    x=x_earth, y=y_earth, z=z_earth, 
    colorscale=earth_colors, showscale=False, name='Earth', 
    lighting=dict(specular=0.5, diffuse=0.8, ambient=0.2, roughness=0.5)
))

# B. Target Spacecraft Orbit & Glowing Marker
fig.add_trace(go.Scatter3d(
    x=iss_x, y=iss_y, z=iss_z, mode='lines',
    line=dict(color='#00FF00', width=2), name='Projected Trajectory'
))
fig.add_trace(go.Scatter3d(
    x=[iss_x[-1]], y=[iss_y[-1]], z=[iss_z[-1]], mode='markers',
    marker=dict(size=8, color='#00FF00', symbol='diamond', line=dict(color='white', width=1)),
    name='Sārathiḥ Target'
))

# C. The Debris Swarm
fig.add_trace(go.Scatter3d(
    x=debris_x, y=debris_y, z=debris_z, mode='markers',
    marker=dict(size=2.5, color=debris_colors, opacity=0.7),
    name='Tracked Debris Catalog'
))

# ---------------------------------------------------------
# 3. DARK SPACE STYLING & CAMERA
# ---------------------------------------------------------
fig.update_layout(
    height=800,
    scene=dict(
        xaxis=dict(showbackground=False, visible=False),
        yaxis=dict(showbackground=False, visible=False),
        zaxis=dict(showbackground=False, visible=False),
        bgcolor='#050505' # Deep pitch black space
    ),
    paper_bgcolor='#050505',
    font=dict(color='white'),
    margin=dict(l=0, r=0, b=0, t=0),
    scene_camera=dict(
        eye=dict(x=1.5, y=1.5, z=0.8) # Cinematic angled view
    )
)

st.plotly_chart(fig, use_container_width=True)

st.caption("🟢 Target Spacecraft | 🔴 Critical Risk (<350km) | 🟠 Warning (350-500km) | ⚫ Safe (>500km)")
