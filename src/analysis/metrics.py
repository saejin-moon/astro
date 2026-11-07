"""
Quantitative Astropolitical Metrics: Gini, HHI, Dwell Skew, Revisit Rates, and Debris Liability.
"""

from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from src.analysis.regional import WORLD_REGIONS, mask_region


def compute_gini(values: np.ndarray) -> float:
    """
    Compute Gini coefficient of an array of values.
    0 = perfect equality, 1 = absolute concentration.
    """
    vals = np.asarray(values, dtype=np.float64)
    vals = vals[~np.isnan(vals)]
    if len(vals) == 0 or np.all(vals == 0):
        return 0.0
    if np.any(vals < 0):
        vals = vals - np.min(vals)
        
    vals = np.sort(vals)
    n = len(vals)
    cum_vals = np.cumsum(vals)
    sum_vals = cum_vals[-1]
    if sum_vals == 0:
        return 0.0
    index = np.arange(1, n + 1)
    gini = (2.0 * np.sum(index * vals) - (n + 1) * sum_vals) / (n * sum_vals)
    return float(np.clip(gini, 0.0, 1.0))


def compute_hhi(shares: np.ndarray) -> float:
    """
    Compute Herfindahl-Hirschman Index (HHI) given percentage market shares (0-100%).
    HHI ranges from ~0 to 10,000.
    > 2,500 indicates a highly concentrated market/regime.
    """
    s = np.asarray(shares, dtype=np.float64)
    total = np.sum(s)
    if total == 0:
        return 0.0
    pct = (s / total) * 100.0
    hhi = float(np.sum(pct**2))
    return hhi


def compute_orbital_shell_concentration(df: pd.DataFrame, altitude_bin_size_km: float = 25.0) -> Dict[str, Any]:
    """
    Analyze satellite concentration across orbital altitude shells (LEO, MEO, GEO).
    Computes Gini and HHI per shell and by geopolitical bloc.
    """
    # Filter active payloads
    active = df[df["OBJECT_TYPE"] != "DEB"].copy()
    
    # Altitude bins from 200 km to 2000 km for LEO
    leo_df = active[(active["ALTITUDE_KM"] >= 200) & (active["ALTITUDE_KM"] <= 2000)].copy()
    bins = np.arange(200, 2000 + altitude_bin_size_km, altitude_bin_size_km)
    leo_df["ALTITUDE_BIN"] = pd.cut(leo_df["ALTITUDE_KM"], bins=bins)
    
    shell_counts = leo_df["ALTITUDE_BIN"].value_counts().sort_index()
    gini_shells = compute_gini(shell_counts.values)
    
    # Geopolitical bloc shares in LEO
    bloc_counts = leo_df["GEOPOLITICAL_BLOC"].value_counts()
    hhi_leo = compute_hhi(bloc_counts.values)
    
    # Geostationary orbit (GEO: ~35,786 km +/- 500 km)
    geo_df = active[(active["ALTITUDE_KM"] >= 35000) & (active["ALTITUDE_KM"] <= 36500)].copy()
    geo_bloc_counts = geo_df["GEOPOLITICAL_BLOC"].value_counts()
    hhi_geo = compute_hhi(geo_bloc_counts.values)
    
    return {
        "leo_satellite_count": len(leo_df),
        "geo_satellite_count": len(geo_df),
        "leo_shell_gini": gini_shells,
        "leo_bloc_hhi": hhi_leo,
        "geo_bloc_hhi": hhi_geo,
        "leo_bloc_shares": (bloc_counts / len(leo_df) * 100.0).to_dict() if len(leo_df) > 0 else {},
        "geo_bloc_shares": (geo_bloc_counts / len(geo_df) * 100.0).to_dict() if len(geo_df) > 0 else {},
    }


def compute_latitudinal_dwell_distribution(latitudes: np.ndarray, num_bins: int = 180) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute empirical ground-track dwell density across latitude bands (-90 to +90 deg).
    latitudes: array of shape (N_sats, N_timesteps)
    Returns:
    - bin_centers: array of latitudes
    - density: normalized dwell probability density per degree
    """
    flat_lats = latitudes.flatten()
    valid_lats = flat_lats[~np.isnan(flat_lats)]
    
    counts, bin_edges = np.histogram(valid_lats, bins=num_bins, range=(-90.0, 90.0), density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0
    return bin_centers, counts


def compute_earth_observation_revisit_disparity(
    eo_latitudes: np.ndarray,
    eo_longitudes: np.ndarray,
    step_hours: float = 1.0,
    swath_radius_deg: float = 5.0,  # ~500 km swath footprint
) -> pd.DataFrame:
    """
    Calculate pass frequency and mean revisit interval (hours) across all 10 world regions
    for Earth Observation and Reconnaissance satellites over the 30-day epoch.
    """
    records = []
    duration_hours = eo_latitudes.shape[1] * step_hours
    
    for rname, rinfo in WORLD_REGIONS.items():
        mask = mask_region(eo_latitudes, eo_longitudes, rname)
        # Total sensor pass instances
        total_passes = int(np.sum(mask))
        
        # Approximate revisit interval: duration / passes
        # If total_passes > 0, mean revisit is duration_hours / total_passes
        # Normalized by regional area
        area_mkm2 = rinfo["area_km2"] / 1e6
        pass_density = total_passes / area_mkm2 if area_mkm2 > 0 else 0.0
        
        # Effective revisit interval in hours over any given 1M km^2 patch
        effective_revisit_hr = (duration_hours / (pass_density + 1e-6)) if pass_density > 0 else np.nan
        
        records.append({
            "Region": rname,
            "Category": rinfo["category"],
            "Area (M km²)": round(area_mkm2, 2),
            "Total EO Passes": total_passes,
            "Pass Density (Passes / M km²)": round(pass_density, 2),
            "Estimated Revisit (Hours / M km²)": round(effective_revisit_hr, 1),
        })
        
    df_revisit = pd.DataFrame(records).sort_values("Pass Density (Passes / M km²)", ascending=False)
    return df_revisit


def compute_debris_liability_index(df_master: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the ratio of debris and dead rocket bodies generated vs active payloads
    for sovereign states and blocs.
    """
    records = []
    owners = df_master["OWNER"].value_counts()
    
    for owner, total_count in owners.items():
        if total_count < 10:
            continue
        sub = df_master[df_master["OWNER"] == owner]
        n_deb = int(np.sum(sub["OBJECT_TYPE"] == "DEB"))
        n_pay = int(np.sum(sub["OBJECT_TYPE"] == "PAY"))
        
        liability_ratio = n_deb / n_pay if n_pay > 0 else float(n_deb)
        
        records.append({
            "Owner": owner,
            "Active Payloads": n_pay,
            "Tracked Debris": n_deb,
            "Total Objects": total_count,
            "Debris Liability Ratio": round(liability_ratio, 2),
        })
        
    df_liability = pd.DataFrame(records).sort_values("Debris Liability Ratio", ascending=False)
    return df_liability
