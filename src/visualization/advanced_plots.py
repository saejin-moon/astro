"""
Advanced visualizations: temporal enclosure velocity, volumetric density (550 km wall),
GEO longitudinal sovereignty, climate-surveillance paradox, atmospheric deorbit mass,
and enhanced full-world satellite activity heatmaps.
"""

import os
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.express as px
import plotly.graph_objects as go


def plot_temporal_enclosure_velocity(
    cum_temporal_df: pd.DataFrame,
    output_path: str = "output/figures/temporal_enclosure_velocity.png",
):
    """
    Stacked area chart showing cumulative active satellite deployments from 1957 to 2026.
    Highlights the dramatic 2019 inflection point.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Consolidate top blocs for clean visual
    top_blocs = [
        "US Commercial (SpaceX)",
        "Europe / UK Commercial (OneWeb)",
        "China Commercial (Qianfan)",
        "United States (Civil / Defense)",
        "China (PRC)",
        "Europe (ESA / EU)",
        "Russia",
        "Global South",
    ]
    
    plot_df = pd.DataFrame(index=cum_temporal_df.index)
    for b in top_blocs:
        if b in cum_temporal_df.columns:
            plot_df[b] = cum_temporal_df[b]
    other_cols = [c for c in cum_temporal_df.columns if c not in top_blocs]
    if other_cols:
        plot_df["Other / International"] = cum_temporal_df[other_cols].sum(axis=1)
        
    fig, ax = plt.subplots(figsize=(11, 6))
    plot_df.plot(kind="area", stacked=True, ax=ax, colormap="tab10", alpha=0.85, linewidth=0)
    
    # Annotate 2019 inflection point
    ax.axvline(2019, color="black", linestyle="--", linewidth=1.5, alpha=0.8)
    ax.annotate(
        "2019: Mega-Constellation Launch Inflection\n(Commercial Enclosure Begins)",
        xy=(2019, plot_df.loc[2019].sum() if 2019 in plot_df.index else 2500),
        xytext=(1985, 8000),
        arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
        fontweight="bold",
        fontsize=9.5,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#fff9db", edgecolor="#e67700", alpha=0.9),
    )
    
    ax.set_title("The Velocity of Orbital Enclosure: Cumulative Active Satellites (1957–2026)", fontweight="bold")
    ax.set_xlabel("Launch Year")
    ax.set_ylabel("Cumulative Operational Satellites in Orbit")
    ax.set_xlim(1960, 2026)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(title="Geopolitical Bloc", loc="upper left", framealpha=0.9)
    
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")


def plot_volumetric_orbital_density(
    density_df: pd.DataFrame,
    output_path: str = "output/figures/volumetric_orbital_density.png",
):
    """
    Physical spatial density of Low Earth Orbit (N / 10^6 km^3) vs. altitude.
    Reveals the '550 km Wall'.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(10, 5.5))
    
    ax.plot(
        density_df["Altitude_Mid_km"],
        density_df["Density_Total_per_Mkm3"],
        color="#d62728",
        linewidth=2.2,
        label="Total Satellite Density (Objects / 10⁶ km³)",
    )
    ax.fill_between(
        density_df["Altitude_Mid_km"],
        density_df["Density_Total_per_Mkm3"],
        color="#d62728",
        alpha=0.2,
    )
    
    # Starlink contribution line
    ax.plot(
        density_df["Altitude_Mid_km"],
        density_df["Density_Starlink_per_Mkm3"],
        color="#1f77b4",
        linestyle="--",
        linewidth=1.8,
        label="SpaceX (Starlink) Contribution",
    )
    
    # Annotate the 550 km peak
    peak_row = density_df.loc[density_df["Density_Total_per_Mkm3"].idxmax()]
    peak_alt = peak_row["Altitude_Mid_km"]
    peak_val = peak_row["Density_Total_per_Mkm3"]
    
    ax.annotate(
        f"The 550 km Wall\nPeak Density: {peak_val:.1f} objects/M km³\n(Starlink Shell)",
        xy=(peak_alt, peak_val),
        xytext=(peak_alt + 200, peak_val * 0.8),
        arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.5),
        fontweight="bold",
        fontsize=9.5,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#ffe3e3", edgecolor="#c92a2a", alpha=0.9),
    )
    
    ax.set_title("Volumetric Spatial Density in Low Earth Orbit (LEO): The 550 km Congestion Wall", fontweight="bold")
    ax.set_xlabel("Orbital Altitude (km)")
    ax.set_ylabel("Spatial Density (Satellites per Million km³)")
    ax.set_xlim(200, 1600)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper right", framealpha=0.9)
    
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")


def plot_geo_longitudinal_sovereignty(
    sector_bloc_df: pd.DataFrame,
    output_path: str = "output/figures/geo_longitudinal_sovereignty.png",
):
    """
    Stacked bar chart testing the 1976 Bogotá Declaration:
    Examines ownership of GEO slots directly above terrestrial sectors.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Consolidate top blocs
    top_blocs = [
        "United States (Civil / Defense)",
        "China (PRC)",
        "Europe (ESA / EU)",
        "Russia",
        "Japan (JAXA)",
        "India (ISRO)",
        "Global South",
        "Other / International",
    ]
    
    consolidated = pd.DataFrame(index=sector_bloc_df.index)
    for b in top_blocs:
        if b in sector_bloc_df.columns:
            consolidated[b] = sector_bloc_df[b]
    other = sector_bloc_df[[c for c in sector_bloc_df.columns if c not in top_blocs]].sum(axis=1)
    if not other.empty and other.sum() > 0:
        consolidated["Commercial / Allied"] = other
        
    fig, ax = plt.subplots(figsize=(10, 6))
    consolidated.plot(kind="bar", stacked=True, ax=ax, colormap="tab20", edgecolor="black", linewidth=0.4)
    
    ax.set_title("Empirical Bogotá Test: Geostationary (GEO) Slot Ownership by Terrestrial Longitude", fontweight="bold")
    ax.set_xlabel("Terrestrial Longitudinal Sector (Directly Below Orbital Slot)")
    ax.set_ylabel("Operational GEO Satellites")
    ax.grid(True, axis="y", linestyle="--", alpha=0.5)
    plt.xticks(rotation=20, ha="right")
    ax.legend(title="Slot Owner Bloc", bbox_to_anchor=(1.02, 1), loc="upper left")
    
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")


def plot_climate_vulnerability_paradox(
    climate_gap_df: pd.DataFrame,
    output_path: str = "output/figures/climate_vulnerability_paradox.png",
):
    """
    Scatter plot contrasting climate vulnerability against Earth observation revisit density.
    Exposes the Climate Vulnerability vs. Sovereign Observation Paradox.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    palette = {
        "Global South": "#e7298a",
        "Global North": "#2b5c8f",
        "Asia-Pacific": "#7570b3",
        "Eurasia": "#d95f02",
        "Global South / Allied": "#66a61e",
        "Commons / Strategic": "#e6ab02",
        "Other": "#999999",
    }
    
    for _, row in climate_gap_df.iterrows():
        cat = row["Category"]
        color = palette.get(cat, "#333333")
        ax.scatter(
            row["Climate_Vulnerability_Score"],
            row["EO_Pass_Density"],
            s=row["Climate_Surveillance_Disparity_Index"] * 400 + 80,
            color=color,
            edgecolor="black",
            linewidth=0.8,
            alpha=0.85,
        )
        # Label offset
        ax.annotate(
            row["Region"],
            xy=(row["Climate_Vulnerability_Score"], row["EO_Pass_Density"]),
            xytext=(6, 4),
            textcoords="offset points",
            fontsize=8.5,
            fontweight="bold" if cat == "Global South" else "normal",
        )
        
    ax.set_title("The Climate-Surveillance Paradox: Regional Climate Risk vs. Earth Observation Density", fontweight="bold")
    ax.set_xlabel("ND-GAIN Climate Vulnerability Score (Higher = Greater Climate Risk)")
    ax.set_ylabel("Earth Observation Pass Density (Passes / Million km²)")
    ax.grid(True, linestyle=":", alpha=0.6)
    
    # Legend for categories
    handles = [plt.scatter([], [], color=col, s=80, edgecolor="black", label=cat) for cat, col in palette.items() if cat in climate_gap_df["Category"].values]
    ax.legend(handles=handles, title="Geopolitical Category", loc="upper left")
    
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")


def plot_atmospheric_deorbit_mass(
    deorbit_df: pd.DataFrame,
    output_path: str = "output/figures/atmospheric_deorbit_mass.png",
):
    """
    Horizontal bar chart of annual mass and aluminum oxide (alumina) deposited in the mesosphere.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    df = deorbit_df.sort_values("Annual Mass Burn-up (Metric Tons)", ascending=True)
    
    y = np.arange(len(df))
    height = 0.38
    
    bars1 = ax.barh(y + height / 2, df["Annual Mass Burn-up (Metric Tons)"], height=height, color="#c92a2a", label="Total Vaporized Mass (Tons/Yr)", edgecolor="black", linewidth=0.5)
    bars2 = ax.barh(y - height / 2, df["Annual Alumina Injection (Tons)"], height=height, color="#e8590c", label="Aluminum Oxide (Alumina) Injection (Tons/Yr)", edgecolor="black", linewidth=0.5)
    
    ax.set_yticks(y)
    ax.set_yticklabels(df["Operator / Constellation"])
    ax.set_title("Atmospheric Externalities: Annual Satellite Metal Mass Vaporized into Upper Atmosphere", fontweight="bold")
    ax.set_xlabel("Annual Aerosolized Mass (Metric Tons / Year)")
    ax.grid(True, axis="x", linestyle="--", alpha=0.5)
    ax.legend(loc="lower right")
    
    for bar in bars1:
        w = bar.get_width()
        if w > 10:
            ax.annotate(f"{w:.0f} t", xy=(w, bar.get_y() + bar.get_height() / 2),
                        xytext=(5, 0), textcoords="offset points", va="center", fontsize=8.5, fontweight="bold")
            
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")


def plot_enhanced_world_satellite_activity_heatmap(
    lat_edges: np.ndarray,
    lon_edges: np.ndarray,
    counts_2d: np.ndarray,
    output_path: str = "output/figures/world_satellite_activity_heatmap.png",
):
    """
    High-contrast, high-resolution full-world satellite activity heatmap.
    Overlays latitude turning points, equator, and geographic grids.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(14, 7), facecolor="#0a0e17")
    ax.set_facecolor("#0a0e17")
    
    # Log transformation for dynamic range
    log_counts = np.log10(counts_2d + 1)
    
    im = ax.imshow(
        log_counts,
        extent=[-180, 180, -90, 90],
        origin="lower",
        cmap="inferno",
        aspect="auto",
    )
    
    cbar = fig.colorbar(im, ax=ax, orientation="vertical", pad=0.02, shrink=0.85)
    cbar.set_label("$\log_{10}(\\text{30-Day Satellite Passes} + 1)$", color="white")
    cbar.ax.yaxis.set_tick_params(color="white")
    plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color="white")
    
    # Mark Equator and Mega-constellation Turning Latitudes
    ax.axhline(0, color="cyan", linestyle="-", linewidth=1.0, alpha=0.85, label="Equator (0°)")
    ax.axhline(53, color="#00ff66", linestyle="--", linewidth=1.2, alpha=0.9, label="Starlink Inclination Turning Latitude (+53°)")
    ax.axhline(-53, color="#00ff66", linestyle="--", linewidth=1.2, alpha=0.9)
    ax.axhline(88, color="#ffcc00", linestyle=":", linewidth=1.0, alpha=0.8, label="OneWeb Polar Shell (87.9°)")
    ax.axhline(-88, color="#ffcc00", linestyle=":", linewidth=1.0, alpha=0.8)
    
    ax.set_title("Global Satellite Activity Heatmap: Empirical 30-Day Trajectory Density (CelesTrak Fleet)",
                 fontweight="bold", color="white", fontsize=13, pad=12)
    ax.set_xlabel("Geographic Longitude (°)", color="white")
    ax.set_ylabel("Geographic Latitude (°)", color="white")
    ax.tick_params(colors="white")
    ax.grid(True, linestyle=":", alpha=0.25, color="gray")
    
    leg = ax.legend(loc="lower left", facecolor="#111827", edgecolor="#374151")
    for text in leg.get_texts():
        text.set_color("white")
        
    fig.savefig(output_path, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    print(f"Saved: {output_path}")


def create_interactive_world_activity_heatmap_html(
    lat_edges: np.ndarray,
    lon_edges: np.ndarray,
    counts_2d: np.ndarray,
    output_html: str = "output/interactive/interactive_world_activity_heatmap.html",
) -> go.Figure:
    """
    Interactive 2D full-world satellite activity heatmap using Plotly.
    Allows interactive zooming, pan, and hover over every geographic region.
    """
    os.makedirs(os.path.dirname(output_html), exist_ok=True)
    
    lat_centers = (lat_edges[:-1] + lat_edges[1:]) / 2.0
    lon_centers = (lon_edges[:-1] + lon_edges[1:]) / 2.0
    
    fig = go.Figure(
        data=go.Heatmap(
            z=np.log10(counts_2d + 1),
            x=lon_centers,
            y=lat_centers,
            colorscale="Inferno",
            colorbar=dict(title="log10(Passes + 1)"),
            hovertemplate="Lon: %{x:.1f}°<br>Lat: %{y:.1f}°<br>Activity Level: %{z:.2f}<extra></extra>",
        )
    )
    
    fig.update_layout(
        title="Interactive Global Satellite Activity Heatmap (30-Day Empirical Trajectories)",
        xaxis_title="Longitude (°)",
        yaxis_title="Latitude (°)",
        template="plotly_dark",
        height=650,
    )
    
    # Add turning latitude lines
    fig.add_hline(y=53, line_dash="dash", line_color="#00ff66", annotation_text="Starlink Shell (+53°)", annotation_position="top left")
    fig.add_hline(y=-53, line_dash="dash", line_color="#00ff66")
    fig.add_hline(y=0, line_dash="solid", line_color="cyan", annotation_text="Equator (0°)", annotation_position="bottom left")
    
    fig.write_html(output_html)
    print(f"Saved interactive plot: {output_html}")
    return fig
