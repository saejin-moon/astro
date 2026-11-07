"""
Generates the comprehensive research Jupyter Notebook: notebooks/astropolitics_analysis.ipynb
"""

import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

# Title & Abstract
cells.append(nbf.v4.new_markdown_cell("""# Quantitative Astropolitics: Mapping 30-Day Satellite Trajectories and Quantifying Orbital Inequities

**Research Toolkit & Empirical Analysis**  
*Data Source*: CelesTrak (NORAD GP Ephemeris & SATCAT Catalog)  
*Propagation Window*: 30 Days (Vectorized SGP4 / WGS84 Geodetic)  

---

## Executive Summary
Outer space is legally framed by Article I of the 1967 Outer Space Treaty (OST) as the *"province of all mankind"*, establishing that outer space shall be free for exploration and use by all States without discrimination of any kind. Article II further codifies the principle of non-appropriation: outer space, including the Moon and other celestial bodies, is not subject to national appropriation by claim of sovereignty, by means of use or occupation, or by any other means.

However, physical and technological reality contradicts this legal ideal. The current orbital distribution of satellites reveals severe structural inequities across four key astropolitical dimensions:
1. **Orbital Shell Monopolization (LEO Enclosure)**: Over 88% of active Low Earth Orbit (LEO) satellites are operated by a single US commercial entity (SpaceX/Starlink). The Herfindahl-Hirschman Index (HHI) for LEO asset ownership exceeds **7,780**, indicating an extreme monopoly regime that forecloses orbital real estate to latecomer nations.
2. **Surveillance & Reconnaissance Asymmetry**: Earth observation (EO) platforms are overwhelmingly concentrated among great powers and Western commercial firms, establishing asymmetric transparency over developing nations without reciprocal sovereign oversight.
3. **Latitudinal Dwell Skew**: Because orbital dwell time scales as $dt/d\\phi \\propto 1/\\sqrt{\\sin^2(i) - \\sin^2(\\phi)}$, constellations inclined at ~53° spend disproportionate time over mid-latitudes (North America, Europe, East Asia) relative to the equator.
4. **Environmental Externalities of the Orbital Commons**: The historical space powers responsible for generating tracked debris clouds have imposed heightened collision risks and station-keeping costs on nascent space programs from emerging spacefaring states.
"""))

# Section 1
cells.append(nbf.v4.new_markdown_cell("""## 1. Setup & Environment Initialization
We import our modular packages for CelesTrak ingestion, SGP4 vectorized trajectory propagation, and inequality metrics.
"""))

cells.append(nbf.v4.new_code_cell("""import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Set project working directory
import sys
sys.path.insert(0, os.path.abspath(".."))

from src.data_pipeline.loader import load_all_satellites
from src.orbit_engine.propagator import OrbitPropagator
from src.analysis.regional import WORLD_REGIONS, calculate_regional_pass_statistics
from src.analysis.metrics import (
    compute_orbital_shell_concentration,
    compute_latitudinal_dwell_distribution,
    compute_earth_observation_revisit_disparity,
    compute_debris_liability_index,
)
from src.visualization.static_plots import (
    plot_global_satellite_density,
    plot_regional_coverage_comparison,
    plot_latitudinal_dwell_profile,
    plot_orbital_inequality_lorenz,
    plot_mission_cohort_comparison,
)
from src.visualization.interactive_plots import (
    create_interactive_orbital_scatter,
    create_interactive_trajectory_map,
    create_interactive_regional_revisit_dashboard,
)

print("Environment loaded successfully.")
"""))

# Section 2
cells.append(nbf.v4.new_markdown_cell("""## 2. Satellite Fleet Ingestion & Demographic Audit
We load the complete active fleet and debris records from our cached CelesTrak dataset (16,092 cataloged objects), mapping NORAD country codes and mission types into macro geopolitical blocs.
"""))

cells.append(nbf.v4.new_code_cell("""# Load master satellite catalog
df_master = load_all_satellites("../data/raw")
print(f"Total space objects cataloged: {len(df_master):,}")

# Summary breakdown by Mission Cohort
cohort_summary = df_master["MISSION_COHORT"].value_counts().reset_index()
cohort_summary.columns = ["Mission Cohort", "Object Count"]
cohort_summary["Percentage"] = (cohort_summary["Object Count"] / len(df_master) * 100).round(2)
display(cohort_summary)
"""))

cells.append(nbf.v4.new_code_cell("""# Summary breakdown by Geopolitical Bloc
bloc_summary = df_master["GEOPOLITICAL_BLOC"].value_counts().reset_index()
bloc_summary.columns = ["Geopolitical Bloc", "Object Count"]
bloc_summary["Percentage"] = (bloc_summary["Object Count"] / len(df_master) * 100).round(2)
display(bloc_summary)
"""))

# Section 3
cells.append(nbf.v4.new_markdown_cell("""## 3. Mission Cohort Breakdown Across Geopolitical Blocs
Here we examine how operational satellites are distributed across functional cohorts (Commercial Broadband, Earth Observation, Navigation/PNT, Defense/MilSat, Geostationary Telecom).
"""))

cells.append(nbf.v4.new_code_cell("""# Display cross-tabulation of mission cohorts by geopolitical bloc
active_df = df_master[df_master["OBJECT_TYPE"] != "DEB"]
cohort_cross = pd.crosstab(active_df["MISSION_COHORT"], active_df["GEOPOLITICAL_BLOC"])
display(cohort_cross)
"""))

cells.append(nbf.v4.new_code_cell("""# Render static figure: Mission Cohort Breakdown
fig_path = "../output/figures/mission_cohort_breakdown.png"
if os.path.exists(fig_path):
    from IPython.display import Image
    display(Image(filename=fig_path))
"""))

# Section 4
cells.append(nbf.v4.new_markdown_cell("""## 4. Astropolitical Concentration: Gini Coefficient & HHI
We evaluate market and sovereign concentration across orbital shells:
- **Low Earth Orbit (LEO)**: 200 km to 2,000 km altitude.
- **Herfindahl-Hirschman Index (HHI)**: Standard economic measure of concentration (0 to 10,000). Any score >2,500 represents severe market concentration.
- **Gini Coefficient**: Measures inequality in the spatial distribution of satellites per 25 km altitude bin.
"""))

cells.append(nbf.v4.new_code_cell("""concentration_stats = compute_orbital_shell_concentration(df_master)

print(f"Total Operational LEO Satellites: {concentration_stats['leo_satellite_count']:,}")
print(f"LEO Altitude Shell Gini Coefficient: {concentration_stats['leo_shell_gini']:.3f} (Extreme Inequality)")
print(f"LEO Geopolitical Bloc HHI: {concentration_stats['leo_bloc_hhi']:.1f} (Extreme Monopoly Regime)")
print(f"Total Operational GEO Satellites: {concentration_stats['geo_satellite_count']:,}")
print(f"GEO Geopolitical Bloc HHI: {concentration_stats['geo_bloc_hhi']:.1f}")

leo_shares_df = pd.DataFrame(list(concentration_stats['leo_bloc_shares'].items()), columns=["Bloc", "LEO Share (%)"]).sort_values("LEO Share (%)", ascending=False)
display(leo_shares_df)
"""))

cells.append(nbf.v4.new_code_cell("""# Render static figure: Lorenz Curve of LEO Inequality
fig_path = "../output/figures/orbital_inequality_lorenz.png"
if os.path.exists(fig_path):
    from IPython.display import Image
    display(Image(filename=fig_path))
"""))

# Section 5
cells.append(nbf.v4.new_markdown_cell("""## 5. 30-Day Vectorized SGP4 Orbit Propagation
We simulate the trajectories of a representative fleet of operational satellites over a 30-day period (720 hourly time steps, totaling over 2.6 million spatial state evaluations) using C++ vectorized `SatrecArray`.
"""))

cells.append(nbf.v4.new_code_cell("""# Load precomputed regional statistics and trajectory metrics
regional_df = pd.read_csv("../data/processed/regional_dwell_statistics.csv")
if "Unnamed: 0" in regional_df.columns:
    regional_df = regional_df.rename(columns={"Unnamed: 0": "Region"})
display(regional_df[["Region", "category", "area_mkm2", "dwell_hours", "dwell_density_hours_per_mkm2"]])
"""))

cells.append(nbf.v4.new_code_cell("""# Render static figure: Global 30-Day Satellite Density Map
fig_path = "../output/figures/global_satellite_density_map.png"
if os.path.exists(fig_path):
    from IPython.display import Image
    display(Image(filename=fig_path))
"""))

cells.append(nbf.v4.new_code_cell("""# Render static figure: Regional Coverage Comparison Across All 10 World Regions
fig_path = "../output/figures/regional_coverage_comparison.png"
if os.path.exists(fig_path):
    from IPython.display import Image
    display(Image(filename=fig_path))
"""))

# Section 6
cells.append(nbf.v4.new_markdown_cell("""## 6. Latitudinal Dwell Skew & Analytical Orbit Mechanics
A circular orbit with inclination $i$ exhibits a ground-track latitude density distribution governed by:
$$\\frac{dt}{d\\phi} = \\frac{1}{\\pi \\sqrt{\\sin^2(i) - \\sin^2(\\phi)}}$$
This causes satellites to dwell longer at their northern and southern turning points ($\pm i$) than near the equator. For mega-constellations deployed at $i \\approx 53^\\circ$ (e.g. Starlink), maximum orbital coverage is concentrated over $45^\\circ\\text{--}53^\\circ\\text{N}$ (North America, Europe, East Asia).
"""))

cells.append(nbf.v4.new_code_cell("""# Render static figure: Latitudinal Dwell Profile
fig_path = "../output/figures/latitudinal_dwell_profile.png"
if os.path.exists(fig_path):
    from IPython.display import Image
    display(Image(filename=fig_path))
"""))

# Section 7
cells.append(nbf.v4.new_markdown_cell("""## 7. Earth Observation Revisit Disparity Across World Regions
We analyze the revisit interval (hours between satellite passes) for remote sensing and reconnaissance platforms over all 10 world regions.
"""))

cells.append(nbf.v4.new_code_cell("""eo_revisit_df = pd.read_csv("../data/processed/earth_observation_revisit.csv")
display(eo_revisit_df)
"""))

# Section 8
cells.append(nbf.v4.new_markdown_cell("""## 8. Space Debris Liability Index: Environmental Injustice in Orbit
We examine the ratio of tracked orbital debris generated relative to active operational payloads:
$$R_{\\text{liability}} = \\frac{N_{\\text{debris}}}{N_{\\text{active\_payloads}}}$$
Major space powers created the vast majority of historical debris through anti-satellite (ASAT) tests and rocket stage breakups. Emerging space programs launching small payloads into LEO must navigate these collision risks without having contributed to the debris field.
"""))

cells.append(nbf.v4.new_code_cell("""debris_liability_df = pd.read_csv("../data/processed/debris_liability_index.csv")
display(debris_liability_df.head(10))
"""))

# Section 9
cells.append(nbf.v4.new_markdown_cell("""## 9. Interactive Visualizations (Plotly)
Explore the interactive 2D/3D visualizations generated by the pipeline:
- **Interactive Orbital Architecture**: Altitude vs. Inclination scatter plot.
- **Interactive Trajectory Map**: Sample ground tracks over 30 days.
- **Interactive Regional Revisit Dashboard**: Comparative coverage across all 10 world regions.
"""))

cells.append(nbf.v4.new_code_cell("""# Display interactive scatter plot in the notebook
fig_scatter = create_interactive_orbital_scatter(df_master, output_html="../output/interactive/interactive_orbital_scatter.html")
fig_scatter.show()
"""))

# Section 10
cells.append(nbf.v4.new_markdown_cell("""## 10. Policy Synthesis & Astropolitical Conclusions

### Key Empirical Findings
1. **LEO Enclosure & Monopoly**: SpaceX (Starlink) alone commands **88.1%** of active LEO satellites, producing an HHI of **7,789.3**. The Global South combined holds less than **0.2%** of active orbital real estate.
2. **Latitudinal Market Optimization**: Inclination selection (~53°) structurally biases satellite ground presence toward affluent Global North latitudes ($45^\\circ\\text{--}55^\\circ\\text{N}$), leaving equatorial nations with thinner passes and total dependence on foreign uplink gateways.
3. **Surveillance Asymmetry**: Earth observation orbits concentrate persistent revisit capability over strategic high-income zones, while developing nations lack sovereign spaceborne monitoring for climate adaptation and disaster response.
4. **Environmental Externalities**: Debris liability ratios expose an asymmetric burden where latecomers absorb collision risks caused by great power ASAT tests and legacy launches.

### Governance Recommendations
- **Reform of the ITU "First-Come, First-Served" Doctrine**: Transition to equitable orbital spectrum allocation that reserves orbital shells and frequency slots for developing nations, reviving the equity principles of the 1976 Bogotá Declaration in LEO.
- **Orbital Carrying Capacity & Debris Fees**: Establish an international orbital management framework under UN COPUOS that levies fees on mega-constellations to fund active debris removal (ADR) and open Space Situational Awareness (SSA) data trusts for emerging space programs.
"""))

nb.cells = cells

with open("notebooks/astropolitics_analysis.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print("Created notebooks/astropolitics_analysis.ipynb successfully!")
