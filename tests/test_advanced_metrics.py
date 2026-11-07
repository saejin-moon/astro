"""
Unit tests for advanced astropolitical metrics: temporal enclosure, volumetric density,
GEO longitudinal sovereignty, climate-surveillance paradox, and atmospheric deorbit deposition.
"""

import numpy as np
import pandas as pd
from src.analysis.advanced_metrics import (
    compute_volumetric_density,
    compute_temporal_enclosure,
    compute_geo_longitudinal_sovereignty,
    compute_climate_vulnerability_gap,
    compute_atmospheric_deorbit_deposition,
    compute_global_activity_grid,
)


def test_volumetric_density_calculation():
    # Synthetic DataFrame with 10 satellites at 550 km
    df = pd.DataFrame({
        "OBJECT_TYPE": ["PAY"] * 10,
        "ALTITUDE_KM": [550.0] * 10,
        "OBJECT_NAME": ["STARLINK-1"] * 10,
    })
    density_df = compute_volumetric_density(df, bin_km=25.0)
    assert not density_df.empty
    assert "Density_Total_per_Mkm3" in density_df.columns
    # Check that shell around 550 km has positive density
    shell_550 = density_df[(density_df["Altitude_Min_km"] <= 550) & (density_df["Altitude_Max_km"] > 550)]
    assert not shell_550.empty
    assert shell_550.iloc[0]["Density_Total_per_Mkm3"] > 0


def test_atmospheric_deorbit_deposition():
    df = pd.DataFrame({
        "OBJECT_TYPE": ["PAY"] * 100,
        "OBJECT_NAME": ["STARLINK-1"] * 80 + ["ONEWEB-1"] * 20,
        "ALTITUDE_KM": [550.0] * 80 + [1200.0] * 20,
    })
    deorbit_df = compute_atmospheric_deorbit_deposition(df)
    assert not deorbit_df.empty
    assert "Annual Mass Burn-up (Metric Tons)" in deorbit_df.columns
    starlink_row = deorbit_df[deorbit_df["Operator / Constellation"].str.contains("Starlink")]
    assert not starlink_row.empty
    assert starlink_row.iloc[0]["Annual Mass Burn-up (Metric Tons)"] > 0


def test_global_activity_grid():
    lats = np.array([[0.0, 50.0], [-30.0, 80.0]])
    lons = np.array([[0.0, 10.0], [-100.0, 150.0]])
    lat_edges, lon_edges, counts = compute_global_activity_grid(lats, lons, res_deg=10.0)
    assert counts.shape == (18, 36)
    assert np.sum(counts) == 4
