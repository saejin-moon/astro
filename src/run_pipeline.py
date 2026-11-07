"""
Master execution script for astropolitical data analysis and visualization.
"""

import os
import json
import numpy as np
import pandas as pd
from datetime import datetime, timezone, timedelta

from src.data_pipeline.loader import load_all_satellites
from src.orbit_engine.propagator import OrbitPropagator
from src.analysis.regional import calculate_regional_pass_statistics
from src.analysis.metrics import (
    compute_orbital_shell_concentration,
    compute_latitudinal_dwell_distribution,
    compute_earth_observation_revisit_disparity,
    compute_debris_liability_index,
)
from src.analysis.advanced_metrics import (
    compute_temporal_enclosure,
    compute_volumetric_density,
    compute_geo_longitudinal_sovereignty,
    compute_climate_vulnerability_gap,
    compute_atmospheric_deorbit_deposition,
    compute_global_activity_grid,
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
from src.visualization.advanced_plots import (
    plot_temporal_enclosure_velocity,
    plot_volumetric_orbital_density,
    plot_geo_longitudinal_sovereignty,
    plot_climate_vulnerability_paradox,
    plot_atmospheric_deorbit_mass,
    plot_enhanced_world_satellite_activity_heatmap,
    create_interactive_world_activity_heatmap_html,
)


def run_astropolitics_pipeline():
    print("=" * 70)
    print("ASTROPOLITICS SATELLITE TRAJECTORY RESEARCH PIPELINE")
    print("=" * 70)
    
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("output/figures", exist_ok=True)
    os.makedirs("output/interactive", exist_ok=True)
    
    # 1. Ingestion & Demographic Audit
    print("\n[Step 1] Loading and classifying CelesTrak satellite fleet...")
    df_master = load_all_satellites()
    print(f"Total space objects cataloged: {len(df_master)}")
    
    # Export demographic summary
    cohort_counts = df_master["MISSION_COHORT"].value_counts().to_dict()
    bloc_counts = df_master["GEOPOLITICAL_BLOC"].value_counts().to_dict()
    
    df_master.to_csv("data/processed/master_space_objects.csv", index=False)
    print("Saved: data/processed/master_space_objects.csv")
    
    # 2. Orbital Concentration Metrics
    print("\n[Step 2] Computing orbital shell concentration (Gini & HHI)...")
    concentration_stats = compute_orbital_shell_concentration(df_master)
    print(f"LEO Satellite Count: {concentration_stats['leo_satellite_count']}")
    print(f"LEO Shell Gini Coefficient: {concentration_stats['leo_shell_gini']:.3f}")
    print(f"LEO Geopolitical Bloc HHI: {concentration_stats['leo_bloc_hhi']:.1f}")
    
    with open("data/processed/concentration_stats.json", "w") as f:
        json.dump(concentration_stats, f, indent=2)
        
    # 3. 30-Day Trajectory Propagation
    print("\n[Step 3] Initializing SGP4 vectorized trajectory engine (30 days)...")
    propagator = OrbitPropagator()
    
    active_sats = df_master[df_master["OBJECT_TYPE"] != "DEB"].copy()
    non_starlink = active_sats[~active_sats["OBJECT_NAME"].str.contains("STARLINK", na=False)]
    starlink_sample = active_sats[active_sats["OBJECT_NAME"].str.contains("STARLINK", na=False)].sample(1500, random_state=42)
    selected_sats = pd.concat([non_starlink, starlink_sample])
    
    print(f"Selected representative active fleet: {len(selected_sats)} satellites for 30-day propagation.")
    norad_ids = selected_sats["NORAD_CAT_ID"].tolist()
    
    print("Running vectorized SGP4 propagation over 30 days (720 hourly steps)...")
    traj_res = propagator.propagate(
        target_norad_ids=norad_ids,
        master_df=df_master,
        duration_days=30.0,
        step_hours=1.0,
    )
    print(f"Trajectory propagation complete: {traj_res.n_satellites} satellites x {traj_res.n_timesteps} timesteps ({traj_res.n_satellites * traj_res.n_timesteps:,} evaluations).")
    
    # 4. Regional Pass Statistics Across All 10 Regions
    print("\n[Step 4] Computing dwell density and revisit rates across all 10 world regions...")
    regional_stats = calculate_regional_pass_statistics(
        traj_res.latitudes,
        traj_res.longitudes,
        step_hours=1.0,
    )
    df_regional = pd.DataFrame(regional_stats).T
    df_regional.to_csv("data/processed/regional_dwell_statistics.csv")
    
    # 5. Latitudinal Dwell Skew
    print("\n[Step 5] Computing latitudinal dwell profile...")
    bin_centers, dwell_density = compute_latitudinal_dwell_distribution(traj_res.latitudes)
    
    # 6. Earth Observation Revisit Disparity
    print("\n[Step 6] Analyzing Earth observation and reconnaissance revisit intervals...")
    eo_mask = np.array([c == "Earth Observation & Surveillance" for c in traj_res.mission_cohorts])
    eo_lats = traj_res.latitudes[eo_mask]
    eo_lons = traj_res.longitudes[eo_mask]
    
    if len(eo_lats) > 0:
        df_revisit = compute_earth_observation_revisit_disparity(eo_lats, eo_lons, step_hours=1.0)
        df_revisit.to_csv("data/processed/earth_observation_revisit.csv", index=False)
    else:
        df_revisit = pd.DataFrame()
        
    # 7. Debris Liability Ratio
    print("\n[Step 7] Computing debris liability index by sovereign nation...")
    df_liability = compute_debris_liability_index(df_master)
    df_liability.to_csv("data/processed/debris_liability_index.csv", index=False)
    
    # 8. Advanced Novel Metrics
    print("\n[Step 8] Computing advanced novel metrics...")
    
    # 8a. Temporal Enclosure Velocity (1957-2026)
    cum_temporal_df = compute_temporal_enclosure(df_master)
    cum_temporal_df.to_csv("data/processed/temporal_enclosure_cumulative.csv")
    print(f"  Calculated temporal enclosure over {len(cum_temporal_df)} years.")
    
    # 8b. Volumetric Density Profile (The 550 km Wall)
    density_df = compute_volumetric_density(df_master)
    density_df.to_csv("data/processed/volumetric_density_profile.csv", index=False)
    peak_density = density_df["Density_Total_per_Mkm3"].max()
    print(f"  Peak physical volumetric density in LEO: {peak_density:.2f} satellites / M km³")
    
    # 8c. Empirical Bogotá Test (GEO Longitudinal Sovereignty)
    geo_sectors_df = compute_geo_longitudinal_sovereignty(df_master)
    geo_sectors_df.to_csv("data/processed/geo_sovereignty_sectors.csv")
    print("  Calculated GEO longitudinal sovereignty sectors.")
    
    # 8d. Climate-Surveillance Paradox
    climate_gap_df = compute_climate_vulnerability_gap(df_regional, df_revisit)
    climate_gap_df.to_csv("data/processed/climate_vulnerability_gap.csv", index=False)
    print("  Calculated Climate Vulnerability vs. Sovereign Observation gap.")
    
    # 8e. Atmospheric Deorbit Deposition
    deorbit_df = compute_atmospheric_deorbit_deposition(df_master)
    deorbit_df.to_csv("data/processed/atmospheric_deorbit_deposition.csv", index=False)
    total_alumina = deorbit_df["Annual Alumina Injection (Tons)"].sum()
    print(f"  Total annual satellite alumina deposition in upper atmosphere: {total_alumina:.1f} metric tons/yr")
    
    # 8f. Enhanced World Activity Grid
    lat_edges, lon_edges, counts_2d = compute_global_activity_grid(traj_res.latitudes, traj_res.longitudes, res_deg=1.0)
    
    # 9. Visualizations (Static & Interactive)
    print("\n[Step 9] Generating primary static figures...")
    plot_global_satellite_density(traj_res.latitudes, traj_res.longitudes)
    plot_regional_coverage_comparison(regional_stats)
    plot_latitudinal_dwell_profile(bin_centers, dwell_density)
    plot_orbital_inequality_lorenz(concentration_stats["leo_bloc_shares"], concentration_stats["leo_shell_gini"])
    plot_mission_cohort_comparison(df_master)
    
    print("\n[Step 10] Generating advanced novel static figures...")
    plot_temporal_enclosure_velocity(cum_temporal_df)
    plot_volumetric_orbital_density(density_df)
    plot_geo_longitudinal_sovereignty(geo_sectors_df)
    plot_climate_vulnerability_paradox(climate_gap_df)
    plot_atmospheric_deorbit_mass(deorbit_df)
    plot_enhanced_world_satellite_activity_heatmap(lat_edges, lon_edges, counts_2d)
    
    print("\n[Step 11] Generating interactive Plotly widgets...")
    create_interactive_orbital_scatter(df_master)
    sample_df = traj_res.to_dataframe_sample(max_points=10000)
    create_interactive_trajectory_map(sample_df)
    if not df_revisit.empty:
        create_interactive_regional_revisit_dashboard(df_revisit)
    create_interactive_world_activity_heatmap_html(lat_edges, lon_edges, counts_2d)
        
    print("\n" + "=" * 70)
    print("ADVANCED ASTROPOLITICS PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    run_astropolitics_pipeline()
