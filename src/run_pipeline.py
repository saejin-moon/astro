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
    
    # Propagate active satellites (sample of ~2,500 representative active operational payloads across all blocs)
    # Ensuring all non-Starlink payloads and representative Starlink shell satellites are included
    active_sats = df_master[df_master["OBJECT_TYPE"] != "DEB"].copy()
    
    # Stratified sample: all non-Starlink + 1,500 Starlink to represent the full constellation accurately
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
    print(df_regional[["category", "area_mkm2", "dwell_hours", "dwell_density_hours_per_mkm2"]])
    
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
        print(df_revisit)
    else:
        df_revisit = pd.DataFrame()
        
    # 7. Debris Liability Ratio
    print("\n[Step 7] Computing debris liability index by sovereign nation...")
    df_liability = compute_debris_liability_index(df_master)
    df_liability.to_csv("data/processed/debris_liability_index.csv", index=False)
    print(df_liability.head(10))
    
    # 8. Visualizations (Static & Interactive)
    print("\n[Step 8] Generating static publication-grade figures...")
    plot_global_satellite_density(traj_res.latitudes, traj_res.longitudes)
    plot_regional_coverage_comparison(regional_stats)
    plot_latitudinal_dwell_profile(bin_centers, dwell_density)
    plot_orbital_inequality_lorenz(concentration_stats["leo_bloc_shares"], concentration_stats["leo_shell_gini"])
    plot_mission_cohort_comparison(df_master)
    
    print("\n[Step 9] Generating interactive Plotly widgets...")
    create_interactive_orbital_scatter(df_master)
    sample_df = traj_res.to_dataframe_sample(max_points=10000)
    create_interactive_trajectory_map(sample_df)
    if not df_revisit.empty:
        create_interactive_regional_revisit_dashboard(df_revisit)
        
    print("\n" + "=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    return traj_res, regional_stats, concentration_stats, df_revisit, df_liability


if __name__ == "__main__":
    run_astropolitics_pipeline()
