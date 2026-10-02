import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from skyfield.api import load, EarthSatellite

# ==========================================
# PAGE CONFIG & PPT THEME
# ==========================================
st.set_page_config(page_title="Satellite Sārathiḥ Dashboard", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4b0082;'>SATELLITE SĀRATHIḤ</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>SPACE DEBRIS DETECTION, TRACKING AND MITIGATION PLANNING</h4>", unsafe_allow_html=True)
st.divider()

# ==========================================
# STEP 1 & 2: INGEST & TRACK (PPT Slide 4 Logic)
# ==========================================
# Ingesting TLE Data & Propagating with SGP4 (Simulated for real-time app)
ts = load.timescale()
t = ts.now()

# Simulating 50 Debris objects around Target Spacecraft
np.random.seed(42)
num_debris = 50
debris_ids = [f"DEB-080-{1000+i}" for i in range(num_debris)]
distances_km = np.random.uniform(5, 150, num_debris)
relative_velocities = np.random.uniform(5, 15, num_debris) # km/s
angles = np.random.uniform(0, 360, num_debris)

# ==========================================
# STEP 3 & 4: SCREEN & SCORE (PPT Risk Engine - Slide 5)
# ==========================================
# Conjunction Analysis: Miss distance, relative velocity -> Risk Score (0-100)
risk_scores = []
risk_zones = []
colors = []

for dist in distances_km:
    if dist <= 10:
        score = np.random.randint(85, 100) # Critical (0-100 risk score)
        risk_zones.append("CRITICAL")
        colors.append("#FF0000") # Red
    elif dist <= 50:
        score = np.random.randint(40, 84) # Warning
        risk_zones.append("WARNING")
        colors.append("#FFA500") # Orange
    else:
        score = np.random.randint(0, 39) # Safe
        risk_zones.append("SAFE")
        colors.append("#00FF00") # Green
    risk_scores.append(score)

# ==========================================
# STEP 5: ACT - OUTPUT DASHBOARD (PPT Slide 5 & 6)
# ==========================================
col1, col2 = st.columns([1.5, 1])

# --- LEFT COLUMN: 3D REALISTIC EARTH ---
with col1:
    st.markdown("### 3D ORBIT VIEW (Realistic Terrain)")
    fig_3d = go.Figure()

    # Generating Highly Realistic Topographical Earth (Matching your photo)
    u = np.linspace(0, 2 * np.pi, 120)
    v = np.linspace(0, np.pi, 120)
    r_earth = 6371 
    x_earth = r_earth * np.outer(np.cos(u), np.sin(v))
    y_earth = r_earth * np.outer(np.sin(u), np.sin(v))
    z_earth = r_earth * np.outer(np.ones(np.size(u)), np.cos(v))
    
    # Adding noise to z to simulate mountains/terrain mathematically
    terrain = np.sin(5*u)*np.cos(5*v) + np.sin(10*u)*np.cos(10*v)
    z_earth_textured = z_earth + (terrain * 50) 

    # Colorscale matching your photo (Deep ocean, green land, brown mountains, white snow peaks)
    realistic_colors = [
        [0.0, '#000033'],     # Very deep ocean
        [0.2, '#0044cc'],     # Ocean
        [0.3, '#228b22'],     # Green land/forests
        [0.6, '#8b4513'],     # Brown mountains
        [0.8, '#d2b48c'],     # Dry high mountains
        [1.0, '#ffffff']      # Snow caps / clouds
    ]

    fig_3d.add_trace(go.Surface(
        x=x_earth, y=y_earth, z=z_earth_textured, 
        surfacecolor=z_earth_textured, # Map colors to heights
        colorscale=realistic_colors, showscale=False,
        # Lighting parameters for photorealism (Specular highlights like in photo)
        lighting=dict(ambient=0.3, diffuse=0.8, specular=0.6, roughness=0.7, fresnel=0.2)
    ))

    # Add Target Spacecraft
    fig_3d.add_trace(go.Scatter3d(
        x=[r_earth+400], y=[0], z=[0], mode='markers',
        marker=dict(size=8, color='#00FFFF', symbol='diamond', line=dict(color='white', width=1)),
        name="Target Spacecraft"
    ))

    # Add Debris Swarm using calculated coordinates
    deb_x = (r_earth + distances_km*10) * np.cos(np.radians(angles))
    deb_y = (r_earth + distances_km*10) * np.sin(np.radians(angles))
    deb_z = np.random.uniform(-2000, 2000, num_debris)

    fig_3d.add_trace(go.Scatter3d(
        x=deb_x, y=deb_y, z=deb_z, mode='markers',
        marker=dict(size=4, color=colors, opacity=0.9),
        name="Tracked Debris"
    ))

    fig_3d.update_layout(
        scene=dict(
            xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
            bgcolor='black' # Deep space background
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=550, showlegend=False,
        scene_camera=dict(eye=dict(x=1.2, y=1.2, z=0.8))
    )
    st.plotly_chart(fig_3d, use_container_width=True)


# --- RIGHT COLUMN: RADAR & RANKED LIST ---
with col2:
    st.markdown("### RADAR VIEW (Slide 6)")
    # Radar View logic from PPT Slide 6
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=distances_km, theta=angles, mode='markers',
        marker=dict(color=colors, size=8, line=dict(color='white', width=1)),
        hovertext=[f"Score: {s}/100<br>TCA: {d:.1f}km" for s, d in zip(risk_scores, distances_km)],
        hoverinfo='text', name="Debris"
    ))
    
    # Radar Danger Zones
    fig_radar.add_shape(type="circle", xref="x", yref="y", x0=-10, y0=-10, x1=10, y1=10, line_color="red", fillcolor="red", opacity=0.3)
    fig_radar.add_shape(type="circle", xref="x", yref="y", x0=-50, y0=-50, x1=50, y1=50, line_color="orange", fillcolor="orange", opacity=0.2)
    fig_radar.add_shape(type="circle", xref="x", yref="y", x0=-150, y0=-150, x1=150, y1=150, line_color="green", fillcolor="green", opacity=0.1)

    fig_radar.update_layout(
        polar=dict(
            bgcolor='#111111',
            angularaxis=dict(showticklabels=False, gridcolor='#333333'),
            radialaxis=dict(range=[0, 150], showticklabels=True, gridcolor='#555555')
        ),
        margin=dict(l=20, r=20, t=20, b=20),
        height=300, showlegend=False
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # Ranked High-Risk List (From Flowchart / Slide 5 output dashboard)
    st.markdown("### RANKED HIGH-RISK LIST")
    
    # Create DataFrame, sort by Risk Score (Descending) just like PPT logic
    df = pd.DataFrame({
        "Debris ID": debris_ids,
        "Miss Distance (km)": np.round(distances_km, 2),
        "Rel. Velocity (km/s)": np.round(relative_velocities, 2),
        "Risk Score (0-100)": risk_scores,
        "Zone": risk_zones
    })
    
    # Filter only Warning & Critical, sort by highest risk
    high_risk_df = df[df["Zone"].isin(["CRITICAL", "WARNING"])].sort_values(by="Risk Score (0-100)", ascending=False).reset_index(drop=True)
    
    st.dataframe(high_risk_df.head(10), use_container_width=True)

    # Optional Mitigation Plan Trigger (From Slide 4 & 5)
    if not high_risk_df.empty and high_risk_df.iloc[0]["Risk Score (0-100)"] >= 90:
        st.error(f"🚨 MITIGATION ALERT: Collision probability high for {high_risk_df.iloc[0]['Debris ID']}. Delta-v maneuver planner activated.")
