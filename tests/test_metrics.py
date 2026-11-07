"""
Unit tests for quantitative astropolitical inequality metrics.
"""

import numpy as np
import pandas as pd
from src.analysis.metrics import compute_gini, compute_hhi, compute_orbital_shell_concentration
from src.analysis.regional import mask_region, WORLD_REGIONS


def test_compute_gini():
    # Perfect equality: all values identical -> Gini = 0
    eq = np.array([10.0, 10.0, 10.0, 10.0])
    assert np.isclose(compute_gini(eq), 0.0, atol=1e-3)
    
    # Extreme inequality: one person owns everything
    monopoly = np.array([0.0, 0.0, 0.0, 1000.0])
    assert compute_gini(monopoly) > 0.70


def test_compute_hhi():
    # Equal 4 firms (25% each) -> 4 * 625 = 2500
    shares = np.array([25.0, 25.0, 25.0, 25.0])
    assert np.isclose(compute_hhi(shares), 2500.0)
    
    # Pure monopoly (100%) -> 10000
    monopoly = np.array([100.0])
    assert np.isclose(compute_hhi(monopoly), 10000.0)


def test_world_regions_definitions():
    assert len(WORLD_REGIONS) == 10
    assert "North America" in WORLD_REGIONS
    assert "Sub-Saharan Africa" in WORLD_REGIONS
    assert "Latin America & Caribbean" in WORLD_REGIONS
    
    # Test masking
    lats = np.array([40.0, -10.0, 80.0])
    lons = np.array([-100.0, 20.0, 0.0])
    
    mask_na = mask_region(lats, lons, "North America")
    assert mask_na[0] == True
    assert mask_na[1] == False
    
    mask_polar = mask_region(lats, lons, "Polar Regimes")
    assert mask_polar[2] == True
