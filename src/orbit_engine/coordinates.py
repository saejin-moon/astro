"""
Vectorized coordinate transformations: TEME -> ECEF -> Geodetic (WGS84).
"""

import numpy as np

# WGS84 Ellipsoid Constants
WGS84_A = 6378.137  # Semi-major axis in km
WGS84_F = 1.0 / 298.257223563  # Flattening
WGS84_B = WGS84_A * (1.0 - WGS84_F)  # Semi-minor axis in km
WGS84_E2 = 2.0 * WGS84_F - WGS84_F**2  # Eccentricity squared
WGS84_E_PRIME2 = (WGS84_A**2 - WGS84_B**2) / (WGS84_B**2)  # Second eccentricity squared


def gmst_from_jd(jd: np.ndarray, fr: np.ndarray) -> np.ndarray:
    """
    Calculate Greenwich Mean Sidereal Time (GMST) in radians for Julian Date (jd + fr).
    Uses IAU 1982 formulation matching SGP4 TEME coordinates.
    """
    # Julian centuries from J2000.0 (JD 2451545.0)
    d = (jd - 2451545.0) + fr
    t = d / 36525.0
    
    # GMST in seconds of time
    gmst_sec = (
        24110.54841
        + 8640184.812866 * t
        + 0.093104 * t**2
        - 6.2e-6 * t**3
    )
    
    # Add earth rotation for the fractional day (fr)
    # 86400 seconds per day, earth rotates 1.002737909350795 rev/day
    gmst_sec += fr * 86400.0 * 1.002737909350795
    
    # Convert to radians in [0, 2*pi)
    gmst_rad = (gmst_sec % 86400.0) * (2.0 * np.pi / 86400.0)
    return gmst_rad


def teme_to_ecef(r_teme: np.ndarray, gmst_rad: np.ndarray) -> np.ndarray:
    """
    Transform TEME position vectors to ECEF coordinates via GMST rotation about Z-axis.
    r_teme: shape (..., 3) in km
    gmst_rad: shape (...) in radians
    Returns r_ecef: shape (..., 3) in km
    """
    cos_theta = np.cos(gmst_rad)
    sin_theta = np.sin(gmst_rad)
    
    x = r_teme[..., 0]
    y = r_teme[..., 1]
    z = r_teme[..., 2]
    
    x_ecef = x * cos_theta + y * sin_theta
    y_ecef = -x * sin_theta + y * cos_theta
    z_ecef = z
    
    return np.stack([x_ecef, y_ecef, z_ecef], axis=-1)


def ecef_to_geodetic(r_ecef: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Convert ECEF Cartesian coordinates (km) to WGS84 Geodetic coordinates.
    Uses Bowring's closed-form algorithm (accurate to millimeters in single step).
    
    Returns:
    - lat_deg: Latitude in degrees [-90, +90]
    - lon_deg: Longitude in degrees [-180, +180]
    - alt_km: Altitude above WGS84 ellipsoid in km
    """
    x = r_ecef[..., 0]
    y = r_ecef[..., 1]
    z = r_ecef[..., 2]
    
    # Longitude in degrees
    lon_rad = np.arctan2(y, x)
    lon_deg = np.degrees(lon_rad)
    
    # Distance from Z-axis
    p = np.hypot(x, y)
    
    # Handle poles
    p_safe = np.where(p < 1e-6, 1e-6, p)
    
    # Bowring parametric angle
    theta = np.arctan2(z * WGS84_A, p_safe * WGS84_B)
    
    # Latitude
    sin_theta3 = np.sin(theta)**3
    cos_theta3 = np.cos(theta)**3
    lat_rad = np.arctan2(
        z + WGS84_E_PRIME2 * WGS84_B * sin_theta3,
        p_safe - WGS84_E2 * WGS84_A * cos_theta3
    )
    lat_deg = np.degrees(lat_rad)
    
    # Radius of curvature in the prime vertical
    sin_lat = np.sin(lat_rad)
    n = WGS84_A / np.sqrt(1.0 - WGS84_E2 * sin_lat**2)
    
    # Altitude
    cos_lat = np.cos(lat_rad)
    sin_lat_safe = np.where(np.abs(sin_lat) < 1e-6, 1e-6, np.abs(sin_lat))
    alt_km = np.where(
        np.abs(cos_lat) > 1e-4,
        (p_safe / cos_lat) - n,
        (np.abs(z) / sin_lat_safe) - (n * (1.0 - WGS84_E2))
    )
    
    return lat_deg, lon_deg, alt_km
