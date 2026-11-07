"""
Publication-quality static visualizations using Matplotlib.
"""

import os
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# Global publication style settings
plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.titlesize": 14,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})


def plot_global_satellite_density(
    latitudes: np.ndarray,
    longitudes: np.ndarray,
    output_path: str = "output/figures/global_satellite_density_map.png",
    bins: Tuple[int, int] = (180, 360),
):
    """
    Generate 2D Equirectangular global heatmap of 30-day satellite passes.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    flat_lats = latitudes.flatten()
    flat_lons = longitudes.flatten()
    valid = ~np.isnan(flat_lats) & ~np.isnan(flat_lons)
    
    counts, xedges, yedges = np.histogram2d(
        flat_lats[valid],
        flat_lons[valid],
        bins=bins,
        range=[[-90, 90], [-180, 180]]
    )
    
    fig, ax = plt.subplots(figsize=(13, 6.5))
    # Log scale for high dynamic range
    log_counts = np.log10(counts + 1)
    
    im = ax.imshow(
        log_counts,
        extent=[-180, 180, -90, 90],
        origin="lower",
        cmap="magma",
        aspect="auto"
    )
    
    cbar = fig.colorbar(im, ax=ax, orientation="vertical", pad=0.02, shrink=0.85)
    cbar.set_label("$\log_{10}(\\text{Pass Count} + 1)$")
    
    ax.axhline(0, color="cyan", linestyle="--", linewidth=0.8, alpha=0.7, label="Equator ($0^\\circ$)")
    ax.axhline(53, color="lime", linestyle=":", linewidth=1.0, alpha=0.8, label="Starlink Turning Lat ($+53^\\circ$)")
    ax.axhline(-53, color="lime", linestyle=":", linewidth=1.0, alpha=0.8)
    
    ax.set_title("Empirical 30-Day Satellite Ground Track Pass Density (CelesTrak)", fontweight="bold")
    ax.set_xlabel("Longitude ($^\\circ$)")
    ax.set_ylabel("Latitude ($^\\circ$)")
    ax.grid(True, linestyle=":", alpha=0.3, color="white")
    ax.legend(loc="lower left", facecolor="#222222", edgecolor="none", labelcolor="white")
    
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")


def plot_regional_coverage_comparison(
    regional_stats: Dict[str, Dict[str, float]],
    output_path: str = "output/figures/regional_coverage_comparison.png",
):
    """
    Horizontal bar chart comparing pass dwell density across all 10 world regions.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df = pd.DataFrame(regional_stats).T
    df = df.sort_values("dwell_density_hours_per_mkm2", ascending=True)
    
    # Color by category
    palette = {
        "Global North": "#2b5c8f",
        "Eurasia": "#d95f02",
        "Asia-Pacific": "#7570b3",
        "Global South": "#e7298a",
        "Global South / Allied": "#66a61e",
        "Commons / Strategic": "#e6ab02",
    }
    colors = [palette.get(c, "#999999") for c in df["category"]]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(df.index, df["dwell_density_hours_per_mkm2"], color=colors, edgecolor="black", linewidth=0.5)
    
    ax.set_title("30-Day Satellite Dwell Density Across All 10 World Regions", fontweight="bold")
    ax.set_xlabel("Dwell Hours per Million km² (Area-Normalized)")
    ax.grid(True, axis="x", linestyle="--", alpha=0.5)
    
    # Legend for categories
    handles = [plt.Rectangle((0, 0), 1, 1, color=col) for cat, col in palette.items() if cat in df["category"].values]
    labels = [cat for cat in palette.keys() if cat in df["category"].values]
    ax.legend(handles, labels, title="Geopolitical Category", loc="lower right")
    
    for bar in bars:
        w = bar.get_width()
        ax.annotate(f"{w:.0f}", xy=(w, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords="offset points", va="center", fontsize=9)
        
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")


def plot_latitudinal_dwell_profile(
    bin_centers: np.ndarray,
    density: np.ndarray,
    output_path: str = "output/figures/latitudinal_dwell_profile.png",
):
    """
    Line plot of latitudinal dwell probability density showing the inclination turning peaks.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(bin_centers, density, color="#1f77b4", linewidth=2.0, label="Empirical Dwell Density")
    ax.fill_between(bin_centers, density, color="#1f77b4", alpha=0.25)
    
    # Annotate Starlink inclination turning points (+/- 53 deg)
    ax.axvline(53, color="red", linestyle="--", label="Mega-Constellation Turning Latitude (+53°)")
    ax.axvline(-53, color="red", linestyle="--")
    ax.axvline(0, color="gray", linestyle=":", label="Equator (0°)")
    
    ax.set_title("Latitudinal Dwell Skew: Empirical Ground Track Density vs. Latitude", fontweight="bold")
    ax.set_xlabel("Geographic Latitude ($^\\circ$)")
    ax.set_ylabel("Probability Density per Degree")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper left")
    
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")


def plot_orbital_inequality_lorenz(
    bloc_shares: Dict[str, float],
    gini_score: float,
    output_path: str = "output/figures/orbital_inequality_lorenz.png",
):
    """
    Lorenz curve representing inequality in Low Earth Orbit (LEO) satellite ownership.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    shares = np.array(list(bloc_shares.values()))
    shares = np.sort(shares)
    shares_norm = shares / np.sum(shares)
    
    cum_shares = np.insert(np.cumsum(shares_norm), 0, 0.0)
    cum_entities = np.linspace(0.0, 1.0, len(cum_shares))
    
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.plot(cum_entities, cum_shares, marker="o", color="#d62728", linewidth=2.5, label=f"Actual LEO Ownership (Gini = {gini_score:.3f})")
    ax.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Line of Perfect Equality")
    
    ax.fill_between(cum_entities, cum_shares, cum_entities, color="#d62728", alpha=0.15)
    
    ax.set_title("Lorenz Curve of Low Earth Orbit (LEO) Asset Ownership", fontweight="bold")
    ax.set_xlabel("Cumulative Share of Global Actors / Blocs")
    ax.set_ylabel("Cumulative Share of Operational Satellites")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper left")
    
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")


def plot_mission_cohort_comparison(
    df: pd.DataFrame,
    output_path: str = "output/figures/mission_cohort_breakdown.png",
):
    """
    Bar chart showing satellite counts across functional cohorts disaggregated by power bloc.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    active = df[df["OBJECT_TYPE"] != "DEB"]
    cross = pd.crosstab(active["MISSION_COHORT"], active["GEOPOLITICAL_BLOC"])
    
    # Consolidate smaller blocs for readability
    top_blocs = ["US Commercial (SpaceX)", "Europe / UK Commercial (OneWeb)", "China Commercial (Qianfan)",
                 "United States (Civil / Defense)", "China (PRC)", "Europe (ESA / EU)", "Global South"]
    
    consolidated = pd.DataFrame(index=cross.index)
    for b in top_blocs:
        if b in cross.columns:
            consolidated[b] = cross[b]
    consolidated["Other / Allied"] = cross[[c for c in cross.columns if c not in top_blocs]].sum(axis=1)
    
    fig, ax = plt.subplots(figsize=(11, 6))
    consolidated.plot(kind="bar", stacked=True, ax=ax, colormap="tab10", edgecolor="black", linewidth=0.3)
    
    ax.set_title("Active Satellite Distribution by Mission Cohort and Geopolitical Bloc", fontweight="bold")
    ax.set_xlabel("Mission Cohort")
    ax.set_ylabel("Number of Active Satellites (Log Scale)")
    ax.set_yscale("log")
    ax.grid(True, axis="y", linestyle="--", alpha=0.6)
    plt.xticks(rotation=25, ha="right")
    ax.legend(title="Geopolitical Bloc", bbox_to_anchor=(1.02, 1), loc="upper left")
    
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")
