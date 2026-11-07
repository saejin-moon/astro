"""
Vectorized SGP4 Orbit Propagation Engine using SatrecArray.
"""

import os
import glob
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict
import numpy as np
import pandas as pd
from sgp4 import omm
from sgp4.api import Satrec, SatrecArray, jday

from src.orbit_engine.coordinates import gmst_from_jd, teme_to_ecef, ecef_to_geodetic


class TrajectoryResult:
    """Stores propagated orbital state history for a collection of satellites."""
    
    def __init__(
        self,
        norad_ids: np.ndarray,
        names: List[str],
        geopolitical_blocs: List[str],
        mission_cohorts: List[str],
        timestamps: List[datetime],
        latitudes: np.ndarray,
        longitudes: np.ndarray,
        altitudes: np.ndarray,
    ):
        self.norad_ids = norad_ids
        self.names = names
        self.geopolitical_blocs = geopolitical_blocs
        self.mission_cohorts = mission_cohorts
        self.timestamps = timestamps
        # Shape: (N_satellites, N_timesteps)
        self.latitudes = latitudes
        self.longitudes = longitudes
        self.altitudes = altitudes
        self.n_satellites = len(names)
        self.n_timesteps = len(timestamps)

    def to_dataframe_sample(self, max_points: int = 50000) -> pd.DataFrame:
        """Flatten a random or uniform sample of trajectory points to a DataFrame."""
        total_points = self.n_satellites * self.n_timesteps
        stride = max(1, total_points // max_points)
        
        records = []
        for sat_idx in range(self.n_satellites):
            nid = int(self.norad_ids[sat_idx])
            name = self.names[sat_idx]
            bloc = self.geopolitical_blocs[sat_idx]
            cohort = self.mission_cohorts[sat_idx]
            
            for t_idx in range(0, self.n_timesteps, stride):
                lat = self.latitudes[sat_idx, t_idx]
                lon = self.longitudes[sat_idx, t_idx]
                alt = self.altitudes[sat_idx, t_idx]
                
                # Filter unphysical points
                if np.isnan(lat) or np.isnan(lon) or alt < 80.0 or alt > 50000.0:
                    continue
                    
                records.append({
                    "NORAD_CAT_ID": nid,
                    "OBJECT_NAME": name,
                    "GEOPOLITICAL_BLOC": bloc,
                    "MISSION_COHORT": cohort,
                    "TIMESTAMP": self.timestamps[t_idx],
                    "LATITUDE": lat,
                    "LONGITUDE": lon,
                    "ALTITUDE_KM": alt,
                })
        return pd.DataFrame(records)


class OrbitPropagator:
    """Manages satellite fleet ingestion and vectorized 30-day propagation."""
    
    def __init__(self, data_dir: str = "data/raw"):
        self.data_dir = data_dir
        self.satrec_objects: Dict[int, Satrec] = {}
        self.satellite_meta: Dict[int, dict] = {}
        self._load_all_records()

    def _load_all_records(self):
        """Parse all GP files and build Satrec instances."""
        gp_files = sorted(glob.glob(os.path.join(self.data_dir, "gp_*.csv")))
        for f in gp_files:
            try:
                with open(f, "r", encoding="utf-8") as fp:
                    for row in omm.parse_csv(fp):
                        try:
                            norad_id = int(row.get("NORAD_CAT_ID", 0))
                            if norad_id == 0 or norad_id in self.satrec_objects:
                                continue
                            sat = Satrec()
                            omm.initialize(sat, row)
                            self.satrec_objects[norad_id] = sat
                            self.satellite_meta[norad_id] = {
                                "OBJECT_NAME": str(row.get("OBJECT_NAME", "")).strip(),
                                "OBJECT_ID": str(row.get("OBJECT_ID", "")).strip(),
                                "EPOCH": str(row.get("EPOCH", "")).strip(),
                                "INCLINATION": float(row.get("INCLINATION", 0.0)),
                                "MEAN_MOTION": float(row.get("MEAN_MOTION", 15.0)),
                            }
                        except Exception:
                            continue
            except Exception as e:
                print(f"Warning reading {f}: {e}")

    def propagate(
        self,
        target_norad_ids: Optional[List[int]] = None,
        master_df: Optional[pd.DataFrame] = None,
        duration_days: float = 30.0,
        step_hours: float = 1.0,
        start_time: Optional[datetime] = None,
    ) -> TrajectoryResult:
        """
        Propagate selected satellites over a duration using vectorized SGP4.
        """
        if start_time is None:
            # Past 30 days up to current epoch
            start_time = datetime.now(timezone.utc) - timedelta(days=duration_days)
            
        # Select target NORAD IDs
        if target_norad_ids is None:
            active_ids = [nid for nid in self.satrec_objects.keys() if nid in self.satellite_meta]
        else:
            active_ids = [nid for nid in target_norad_ids if nid in self.satrec_objects]

        sats_to_propagate = [self.satrec_objects[nid] for nid in active_ids]
        sat_array = SatrecArray(sats_to_propagate)
        
        # Build time steps
        n_steps = int(np.ceil((duration_days * 24.0) / step_hours))
        time_offsets_hours = np.arange(n_steps) * step_hours
        timestamps = [start_time + timedelta(hours=float(h)) for h in time_offsets_hours]
        
        # Julian dates for SGP4
        jds = np.empty(n_steps, dtype=np.float64)
        frs = np.empty(n_steps, dtype=np.float64)
        for i, ts in enumerate(timestamps):
            jd, fr = jday(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second + ts.microsecond * 1e-6)
            jds[i] = jd
            frs[i] = fr
            
        # Run vectorized SGP4: returns shape (N_sats, N_steps, 3)
        errs, r_teme, v_teme = sat_array.sgp4(jds, frs)
        
        # Calculate GMST and transform coordinates
        gmst = gmst_from_jd(jds, frs)
        # Broadcast across satellites: shape (1, N_steps)
        r_ecef = teme_to_ecef(r_teme, gmst[np.newaxis, :])
        lat_deg, lon_deg, alt_km = ecef_to_geodetic(r_ecef)
        
        # Clean up errors/decayed values
        valid_mask = (errs == 0)
        lat_deg = np.where(valid_mask, lat_deg, np.nan)
        lon_deg = np.where(valid_mask, lon_deg, np.nan)
        alt_km = np.where(valid_mask, alt_km, np.nan)
        
        # Extract metadata
        names = []
        blocs = []
        cohorts = []
        
        # Map metadata from master_df if provided
        lookup_map = {}
        if master_df is not None:
            for _, row in master_df.iterrows():
                lookup_map[int(row["NORAD_CAT_ID"])] = (
                    row.get("GEOPOLITICAL_BLOC", "Other / International"),
                    row.get("MISSION_COHORT", "Science & Other Payloads"),
                )
                
        for nid in active_ids:
            meta = self.satellite_meta.get(nid, {})
            name = meta.get("OBJECT_NAME", f"SAT-{nid}")
            names.append(name)
            
            if nid in lookup_map:
                bloc, cohort = lookup_map[nid]
            else:
                bloc = "Other / International"
                cohort = "Science & Other Payloads"
            blocs.append(bloc)
            cohorts.append(cohort)
            
        return TrajectoryResult(
            norad_ids=np.array(active_ids),
            names=names,
            geopolitical_blocs=blocs,
            mission_cohorts=cohorts,
            timestamps=timestamps,
            latitudes=lat_deg,
            longitudes=lon_deg,
            altitudes=alt_km,
        )
