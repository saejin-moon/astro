"""
Geographic definitions and spatial masking for all 10 world regions.
"""

from typing import Dict, Any
import numpy as np


WORLD_REGIONS: Dict[str, Dict[str, Any]] = {
    "North America": {
        "lat_range": (25.0, 72.0),
        "lon_range": (-168.0, -50.0),
        "area_km2": 24709000,
        "description": "United States and Canada",
        "category": "Global North",
    },
    "Western Europe": {
        "lat_range": (36.0, 71.0),
        "lon_range": (-11.0, 32.0),
        "area_km2": 5400000,
        "description": "EU members, UK, Norway, Switzerland",
        "category": "Global North",
    },
    "Eastern Europe & Russia": {
        "lat_range": (45.0, 75.0),
        "lon_range": (32.0, 180.0),
        "area_km2": 18000000,
        "description": "Russia, Ukraine, Belarus, Caucasus",
        "category": "Eurasia",
    },
    "East Asia": {
        "lat_range": (18.0, 54.0),
        "lon_range": (73.0, 145.0),
        "area_km2": 11800000,
        "description": "China, Japan, South Korea, Taiwan, Mongolia",
        "category": "Asia-Pacific",
    },
    "South Asia": {
        "lat_range": (6.0, 37.0),
        "lon_range": (60.0, 98.0),
        "area_km2": 5100000,
        "description": "India, Pakistan, Bangladesh, Sri Lanka, Nepal",
        "category": "Global South",
    },
    "Middle East & North Africa (MENA)": {
        "lat_range": (12.0, 42.0),
        "lon_range": (-17.0, 63.0),
        "area_km2": 11100000,
        "description": "Arabian Peninsula, Levant, North Africa",
        "category": "Global South",
    },
    "Sub-Saharan Africa": {
        "lat_range": (-35.0, 18.0),
        "lon_range": (-18.0, 52.0),
        "area_km2": 24300000,
        "description": "West, Central, East, and Southern Africa",
        "category": "Global South",
    },
    "Latin America & Caribbean": {
        "lat_range": (-56.0, 33.0),
        "lon_range": (-118.0, -34.0),
        "area_km2": 20100000,
        "description": "South America, Central America, Mexico, Caribbean",
        "category": "Global South",
    },
    "Oceania & Pacific Islands": {
        "lat_range": (-48.0, 0.0),
        "lon_range": (110.0, 180.0),
        "area_km2": 8500000,
        "description": "Australia, New Zealand, Melanesia, Polynesia",
        "category": "Global South / Allied",
    },
    "Polar Regimes": {
        "lat_range": (66.5, 90.0),  # Arctic combined with Antarctic (<-66.5)
        "lon_range": (-180.0, 180.0),
        "area_km2": 28000000,
        "description": "Arctic (>66.5°N) and Antarctic (<-66.5°S)",
        "category": "Commons / Strategic",
    },
}


def mask_region(latitudes: np.ndarray, longitudes: np.ndarray, region_name: str) -> np.ndarray:
    """
    Generate boolean mask for points falling within the specified region.
    Supports 1D, 2D, or higher-dimensional arrays of coordinates.
    """
    if region_name not in WORLD_REGIONS:
        raise ValueError(f"Unknown region: {region_name}. Choose from {list(WORLD_REGIONS.keys())}")
        
    cfg = WORLD_REGIONS[region_name]
    lat_min, lat_max = cfg["lat_range"]
    lon_min, lon_max = cfg["lon_range"]
    
    if region_name == "Polar Regimes":
        # Arctic or Antarctic
        mask = (latitudes >= 66.5) | (latitudes <= -66.5)
    else:
        mask = (
            (latitudes >= lat_min)
            & (latitudes <= lat_max)
            & (longitudes >= lon_min)
            & (longitudes <= lon_max)
        )
    return mask


def calculate_regional_pass_statistics(
    latitudes: np.ndarray,
    longitudes: np.ndarray,
    step_hours: float = 1.0,
) -> Dict[str, Dict[str, float]]:
    """
    Compute pass counts, dwell hours, and normalized pass density across all 10 regions.
    latitudes, longitudes: arrays of shape (N_sats, N_timesteps)
    """
    results = {}
    total_evaluations = latitudes.size
    
    for rname, rinfo in WORLD_REGIONS.items():
        mask = mask_region(latitudes, longitudes, rname)
        pass_count = int(np.sum(mask))
        dwell_hours = pass_count * step_hours
        area_mkm2 = rinfo["area_km2"] / 1e6  # Millions of km^2
        density_hours_per_mkm2 = dwell_hours / area_mkm2 if area_mkm2 > 0 else 0.0
        
        results[rname] = {
            "pass_count": pass_count,
            "dwell_hours": dwell_hours,
            "area_mkm2": area_mkm2,
            "dwell_density_hours_per_mkm2": density_hours_per_mkm2,
            "percentage_of_global_dwell": (pass_count / total_evaluations * 100.0) if total_evaluations > 0 else 0.0,
            "category": rinfo["category"],
        }
    return results
