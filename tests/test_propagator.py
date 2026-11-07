"""
Unit tests for SGP4 orbit propagation and coordinate transformations.
"""

import numpy as np
from src.orbit_engine.coordinates import gmst_from_jd, teme_to_ecef, ecef_to_geodetic
from src.orbit_engine.propagator import OrbitPropagator


def test_coordinate_transformation_bounds():
    # Synthetic TEME coordinates around LEO (~6800 km radius)
    r_teme = np.array([[[6800.0, 0.0, 0.0], [0.0, 6800.0, 0.0], [0.0, 0.0, 6800.0]]])
    jd = np.array([2461351.5, 2461351.5, 2461351.5])
    fr = np.array([0.0, 0.25, 0.5])
    
    gmst = gmst_from_jd(jd, fr)
    assert len(gmst) == 3
    assert np.all(gmst >= 0.0) and np.all(gmst <= 2 * np.pi)
    
    r_ecef = teme_to_ecef(r_teme, gmst[np.newaxis, :])
    assert r_ecef.shape == (1, 3, 3)
    
    lat, lon, alt = ecef_to_geodetic(r_ecef)
    assert np.all(lat >= -90.0) and np.all(lat <= 90.0)
    assert np.all(lon >= -180.0) and np.all(lon <= 180.0)
    assert np.all(alt > 300.0) and np.all(alt < 500.0)  # ~421 km altitude above WGS84


def test_propagator_execution():
    prop = OrbitPropagator()
    assert len(prop.satrec_objects) > 0
    
    # Propagate ISS (NORAD 25544) or first available satellite for 1 day
    first_id = list(prop.satrec_objects.keys())[0]
    res = prop.propagate(target_norad_ids=[first_id], duration_days=1.0, step_hours=1.0)
    
    assert res.n_satellites == 1
    assert res.n_timesteps == 24
    assert res.latitudes.shape == (1, 24)
    assert not np.all(np.isnan(res.latitudes))
