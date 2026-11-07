"""
Unit tests for data ingestion, caching, and classification.
"""

import os
import pandas as pd
from src.data_pipeline.loader import load_all_satellites
from src.data_pipeline.geopolitics import get_geopolitical_bloc, classify_mission_cohort


def test_geopolitical_classification():
    assert get_geopolitical_bloc("US", "STARLINK-1008") == "US Commercial (SpaceX)"
    assert get_geopolitical_bloc("GBR", "ONEWEB-0100") == "Europe / UK Commercial (OneWeb)"
    assert get_geopolitical_bloc("PRC", "QIANFAN-1") == "China Commercial (Qianfan)"
    assert get_geopolitical_bloc("PRC", "YAOGAN-30") == "China (PRC)"
    assert get_geopolitical_bloc("CIS", "COSMOS 2550") == "Russia"
    assert get_geopolitical_bloc("BRA", "AMAZONIA-1") == "Global South"
    assert get_geopolitical_bloc("ZAF", "ZA-CUBE") == "Global South"


def test_mission_cohort_classification():
    assert classify_mission_cohort("STARLINK-1008") == "Commercial Broadband"
    assert classify_mission_cohort("NAVSTAR 75 (USA 242)") == "Positioning, Navigation & Timing (PNT)"
    assert classify_mission_cohort("SENTINEL-2A") == "Earth Observation & Surveillance"
    assert classify_mission_cohort("ISS (ZARYA)") == "Space Stations & Crewed"


def test_data_loader_caching():
    df = load_all_satellites()
    assert not df.empty
    assert "NORAD_CAT_ID" in df.columns
    assert "GEOPOLITICAL_BLOC" in df.columns
    assert "MISSION_COHORT" in df.columns
    assert len(df) > 1000
