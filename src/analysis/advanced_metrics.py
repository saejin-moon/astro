"""
Advanced astropolitical metrics: temporal enclosure velocity, volumetric spatial density,
GEO longitudinal sovereignty (Bogotá test), climate-surveillance paradox, and atmospheric deorbit deposition.
"""

import re
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from src.orbit_engine.coordinates import gmst_from_jd


def extract_launch_year(row: pd.Series) -> int:
    """Extract 4-digit launch year from LAUNCH_DATE or OBJECT_ID."""
    date_str = str(row.get("LAUNCH_DATE", "")).strip()
    match = re.search(r"^(19\d{2}|20\d{2})", date_str)
    if match:
        return int(match.group(1))
        
    obj_id = str(row.get("OBJECT_ID", "")).strip()
    match_id = re.search(r"^(19\d{2}|20\d{2})", obj_id)
    if match_id:
        return int(match_id.group(1))
        
    # Starlink default to post-2019
    name = str(row.get("OBJECT_NAME", "")).upper()
    if "STARLINK" in name:
        return 2021
    if "QIANFAN" in name:
        return 2024
    if "ONEWEB" in name:
        return 2021
    return 2020


def compute_temporal_enclosure(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate annual and cumulative satellite deployments from 1957 to 2026
    disaggregated by geopolitical bloc, isolating the 2019 inflection point.
    """
    active = df[df["OBJECT_TYPE"] != "DEB"].copy()
    active["LAUNCH_YEAR"] = active.apply(extract_launch_year, axis=1)
    
    # Filter valid years
    active = active[(active["LAUNCH_YEAR"] >= 1957) & (active["LAUNCH_YEAR"] <= 2026)]
    
    # Cross-tabulate by year and bloc
    cross = pd.crosstab(active["LAUNCH_YEAR"], active["GEOPOLITICAL_BLOC"])
    
    # Cumulative active sum over time
    cum_df = cross.cumsum()
    return cum_df


def compute_volumetric_density(df: pd.DataFrame, bin_km: float = 25.0) -> pd.DataFrame:
    """
    Calculate physical satellite density in Low Earth Orbit (200-2,000 km)
    as objects per million cubic kilometers (N / 10^6 km^3).
    Exposes the 550 km congestion wall.
    """
    active = df[df["OBJECT_TYPE"] != "DEB"].copy()
    leo = active[(active["ALTITUDE_KM"] >= 200.0) & (active["ALTITUDE_KM"] <= 2000.0)].copy()
    
    r_earth = 6378.137
    bins = np.arange(200.0, 2000.0 + bin_km, bin_km)
    
    records = []
    for i in range(len(bins) - 1):
        h_low = bins[i]
        h_high = bins[i + 1]
        h_mid = (h_low + h_high) / 2.0
        
        # Spherical shell volume in km^3: 4/3 * pi * (r2^3 - r1^3)
        r1 = r_earth + h_low
        r2 = r_earth + h_high
        vol_km3 = (4.0 / 3.0) * np.pi * (r2**3 - r1**3)
        vol_mkm3 = vol_km3 / 1e6  # Millions of km^3
        
        in_shell = leo[(leo["ALTITUDE_KM"] >= h_low) & (leo["ALTITUDE_KM"] < h_high)]
        n_total = len(in_shell)
        n_starlink = int(np.sum(in_shell["OBJECT_NAME"].str.contains("STARLINK", na=False)))
        n_other = n_total - n_starlink
        
        density_total = n_total / vol_mkm3 if vol_mkm3 > 0 else 0.0
        density_starlink = n_starlink / vol_mkm3 if vol_mkm3 > 0 else 0.0
        
        records.append({
            "Altitude_Min_km": h_low,
            "Altitude_Max_km": h_high,
            "Altitude_Mid_km": h_mid,
            "Shell_Volume_Mkm3": vol_mkm3,
            "Total_Objects": n_total,
            "Starlink_Objects": n_starlink,
            "Other_Objects": n_other,
            "Density_Total_per_Mkm3": density_total,
            "Density_Starlink_per_Mkm3": density_starlink,
        })
        
    return pd.DataFrame(records)


def compute_geo_longitudinal_sovereignty(df: pd.DataFrame) -> pd.DataFrame:
    """
    Empirical Test of the 1976 Bogotá Declaration:
    Analyzes geostationary satellite positions across 0-360 degrees longitude,
    comparing sub-satellite equatorial sovereign landmasses with satellite owner blocs.
    """
    active = df[df["OBJECT_TYPE"] != "DEB"].copy()
    # Filter GEO objects (~35,786 km +/- 700 km, low eccentricity, low inclination)
    geo = active[
        (active["ALTITUDE_KM"] >= 35000)
        & (active["ALTITUDE_KM"] <= 36500)
        & (active["ECCENTRICITY"] < 0.05)
        & (active["INCLINATION"] < 15.0)
    ].copy()
    
    # Calculate approximate sub-satellite longitude:
    # lambda_deg = (RAAN + ARG_PER + MEAN_ANOMALY - GMST_deg) % 360
    # For GEO, RAAN + ARG_PER + MEAN_ANOMALY is the mean right ascension
    # We normalize to [-180, +180] longitude
    geo_lons = (geo["RA_OF_ASC_NODE"] + geo["ARG_OF_PERICENTER"] + geo["MEAN_ANOMALY"]) % 360.0
    geo["SUB_SATELLITE_LON"] = np.where(geo_lons > 180.0, geo_lons - 360.0, geo_lons)
    
    # Define longitudinal terrestrial zones:
    # 1. Americas / Pacific (-180 to -35)
    # 2. Atlantic / Africa (-35 to +50)
    # 3. Middle East / Indian Ocean (+50 to +100)
    # 4. Asia-Pacific / Oceania (+100 to +180)
    def assign_geo_sector(lon: float) -> str:
        if -120.0 <= lon < -35.0:
            return "Americas & Caribbean"
        elif -35.0 <= lon < 50.0:
            return "Africa & Europe Corridor"
        elif 50.0 <= lon < 100.0:
            return "Middle East & South Asia"
        elif 100.0 <= lon < 160.0:
            return "East Asia & Southeast Asia"
        else:
            return "Pacific Ocean Commons"
            
    geo["GEO_SECTOR"] = geo["SUB_SATELLITE_LON"].apply(assign_geo_sector)
    
    # Cross-tabulation of sector by geopolitical bloc
    sector_bloc = pd.crosstab(geo["GEO_SECTOR"], geo["GEOPOLITICAL_BLOC"])
    return sector_bloc


def compute_climate_vulnerability_gap(
    regional_dwell_df: pd.DataFrame,
    eo_revisit_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Contrasts regional Earth observation revisit frequency against ND-GAIN climate vulnerability scores.
    Exposes the Climate Vulnerability vs. Sovereign Observation Paradox.
    """
    # ND-GAIN Climate Vulnerability Index (0 = resilient, 1 = severely vulnerable)
    nd_gain_vulnerability = {
        "Sub-Saharan Africa": 0.58,
        "South Asia": 0.52,
        "Oceania & Pacific Islands": 0.48,
        "Middle East & North Africa (MENA)": 0.46,
        "Latin America & Caribbean": 0.44,
        "East Asia": 0.35,
        "Eastern Europe & Russia": 0.32,
        "North America": 0.27,
        "Western Europe": 0.25,
        "Polar Regimes": 0.50,
    }
    
    records = []
    for region, vuln in nd_gain_vulnerability.items():
        # Match revisit data
        eo_match = eo_revisit_df[eo_revisit_df["Region"] == region] if not eo_revisit_df.empty else pd.DataFrame()
        if not eo_match.empty:
            revisit_density = float(eo_match.iloc[0]["Pass Density (Passes / M km²)"])
            effective_revisit = float(eo_match.iloc[0]["Estimated Revisit (Hours / M km²)"])
            category = str(eo_match.iloc[0]["Category"])
        else:
            revisit_density = 100.0
            effective_revisit = 0.5
            category = "Other"
            
        # Vulnerability-to-Monitoring Disparity Ratio:
        # High vulnerability + high revisit interval = highest neglected risk
        disparity_index = vuln * effective_revisit
        
        records.append({
            "Region": region,
            "Category": category,
            "Climate_Vulnerability_Score": vuln,
            "EO_Pass_Density": revisit_density,
            "Estimated_Revisit_Hours": effective_revisit,
            "Climate_Surveillance_Disparity_Index": round(disparity_index, 3),
        })
        
    return pd.DataFrame(records).sort_values("Climate_Surveillance_Disparity_Index", ascending=False)


def compute_atmospheric_deorbit_deposition(df: pd.DataFrame) -> pd.DataFrame:
    """
    Quantify annual aerosolized metal mass (metric tons) deposited into the upper atmosphere
    from continuous replenishment cycles of mega-constellations.
    """
    active = df[df["OBJECT_TYPE"] != "DEB"].copy()
    
    operators = [
        ("SpaceX (Starlink)", "STARLINK", 550.0, 5.0),    # ~550 kg dry mass, 5-year replacement cycle
        ("OneWeb", "ONEWEB", 150.0, 6.0),                 # ~150 kg dry mass, 6-year cycle
        ("China (Qianfan)", "QIANFAN", 300.0, 5.0),       # ~300 kg dry mass, 5-year cycle
        ("Planet Labs", "FLOCK", 5.0, 3.0),               # ~5 kg CubeSat, 3-year cycle
        ("Other Commercial LEO", "", 200.0, 7.0),
    ]
    
    records = []
    for label, pattern, dry_mass_kg, lifespan_years in operators:
        if pattern:
            sub = active[active["OBJECT_NAME"].str.contains(pattern, na=False)]
        else:
            sub = active[
                ~active["OBJECT_NAME"].str.contains("STARLINK|ONEWEB|QIANFAN|FLOCK", na=False)
                & (active["ALTITUDE_KM"] <= 1200.0)
            ]
        count = len(sub)
        annual_deorbits = count / lifespan_years
        annual_mass_tons = (annual_deorbits * dry_mass_kg) / 1000.0
        # Aluminum oxide fraction (~80% of satellite dry mass is aluminum alloys)
        annual_alumina_tons = annual_mass_tons * 0.80
        
        records.append({
            "Operator / Constellation": label,
            "Active Satellites": count,
            "Avg Dry Mass (kg)": dry_mass_kg,
            "Operational Lifespan (Yrs)": lifespan_years,
            "Annual Satellites Deorbiting": round(annual_deorbits, 1),
            "Annual Mass Burn-up (Metric Tons)": round(annual_mass_tons, 2),
            "Annual Alumina Injection (Tons)": round(annual_alumina_tons, 2),
        })
        
    return pd.DataFrame(records).sort_values("Annual Mass Burn-up (Metric Tons)", ascending=False)


def compute_global_activity_grid(
    latitudes: np.ndarray,
    longitudes: np.ndarray,
    res_deg: float = 1.0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate high-resolution 2D grid of global satellite pass counts and activity.
    Returns lat_edges, lon_edges, 2D count matrix.
    """
    flat_lats = latitudes.flatten()
    flat_lons = longitudes.flatten()
    valid = ~np.isnan(flat_lats) & ~np.isnan(flat_lons)
    
    lat_bins = int(180 / res_deg)
    lon_bins = int(360 / res_deg)
    
    counts, lat_edges, lon_edges = np.histogram2d(
        flat_lats[valid],
        flat_lons[valid],
        bins=[lat_bins, lon_bins],
        range=[[-90.0, 90.0], [-180.0, 180.0]],
    )
    return lat_edges, lon_edges, counts
