"""
Interactive web-based visualizations using Plotly.
"""

import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


def create_interactive_orbital_scatter(
    df: pd.DataFrame,
    output_html: str = "output/interactive/interactive_orbital_scatter.html",
) -> go.Figure:
    """
    Interactive scatter plot of Altitude (km) vs. Inclination (deg).
    Clusters clearly highlight orbital regimes:
    - Starlink shell (~550 km, 53°)
    - OneWeb shell (~1200 km, 88°)
    - Sun-synchronous Earth Observation (~500-800 km, ~98°)
    - Navigation constellations (MEO, ~20,000 km, ~55°)
    - Geostationary Telecom (GEO, ~35,786 km, ~0°)
    """
    os.makedirs(os.path.dirname(output_html), exist_ok=True)
    
    active = df[df["OBJECT_TYPE"] != "DEB"].copy()
    # Limit to reasonable display sample if large
    if len(active) > 4000:
        sample = active.sample(4000, random_state=42).copy()
    else:
        sample = active.copy()
        
    fig = px.scatter(
        sample,
        x="INCLINATION",
        y="ALTITUDE_KM",
        color="GEOPOLITICAL_BLOC",
        hover_name="OBJECT_NAME",
        hover_data=["NORAD_CAT_ID", "OWNER", "MISSION_COHORT", "ALTITUDE_KM"],
        title="Orbital Architecture: Altitude vs. Inclination by Geopolitical Bloc",
        labels={"INCLINATION": "Orbital Inclination (Degrees)", "ALTITUDE_KM": "Altitude (km)"},
        template="plotly_dark",
        opacity=0.75,
    )
    
    # Annotations for major orbital regimes
    fig.add_hline(y=550, line_dash="dash", line_color="lime", annotation_text="Starlink Shell (550 km)", annotation_position="top left")
    fig.add_hline(y=1200, line_dash="dash", line_color="cyan", annotation_text="OneWeb Shell (1200 km)", annotation_position="top left")
    fig.add_hline(y=35786, line_dash="dash", line_color="magenta", annotation_text="Geostationary Orbit (35,786 km)", annotation_position="top left")
    
    fig.update_layout(
        yaxis_type="log",
        height=650,
        legend_title_text="Geopolitical Bloc",
    )
    
    fig.write_html(output_html)
    print(f"Saved interactive plot: {output_html}")
    return fig


def create_interactive_trajectory_map(
    sample_trajectories_df: pd.DataFrame,
    output_html: str = "output/interactive/interactive_trajectory_map.html",
) -> go.Figure:
    """
    2D Plate Carrée interactive map of sample satellite trajectories.
    """
    os.makedirs(os.path.dirname(output_html), exist_ok=True)
    
    fig = px.scatter_geo(
        sample_trajectories_df,
        lat="LATITUDE",
        lon="LONGITUDE",
        color="GEOPOLITICAL_BLOC",
        hover_name="OBJECT_NAME",
        hover_data=["MISSION_COHORT", "ALTITUDE_KM"],
        title="Global Satellite Ground Track Trajectories (30-Day Sample)",
        template="plotly_dark",
        opacity=0.6,
    )
    
    fig.update_geos(
        showcoastlines=True, coastlinecolor="gray",
        showland=True, landcolor="#111111",
        showocean=True, oceancolor="#050510",
        showlakes=True, lakecolor="#050510",
        showcountries=True, countrycolor="#333333",
    )
    
    fig.update_layout(height=650)
    fig.write_html(output_html)
    print(f"Saved interactive plot: {output_html}")
    return fig


def create_interactive_regional_revisit_dashboard(
    df_revisit: pd.DataFrame,
    output_html: str = "output/interactive/interactive_revisit_dashboard.html",
) -> go.Figure:
    """
    Interactive horizontal bar chart of Earth Observation revisit density across regions.
    """
    os.makedirs(os.path.dirname(output_html), exist_ok=True)
    
    fig = px.bar(
        df_revisit,
        x="Pass Density (Passes / M km²)",
        y="Region",
        color="Category",
        orientation="h",
        hover_data=["Area (M km²)", "Total EO Passes", "Estimated Revisit (Hours / M km²)"],
        title="Earth Observation & Reconnaissance Pass Density Across World Regions",
        template="plotly_white",
        color_discrete_map={
            "Global North": "#1f77b4",
            "Global South": "#e377c2",
            "Asia-Pacific": "#2ca02c",
            "Eurasia": "#ff7f0e",
            "Global South / Allied": "#bcbd22",
            "Commons / Strategic": "#7f7f7f",
        }
    )
    
    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        height=550,
        xaxis_title="Pass Density (Passes per Million km²)",
    )
    
    fig.write_html(output_html)
    print(f"Saved interactive plot: {output_html}")
    return fig
