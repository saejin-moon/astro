"""
Data loader for satellite orbital elements (GP) and catalog metadata (SATCAT).
"""

import os
import glob
import pandas as pd
from typing import Optional
from src.data_pipeline.geopolitics import get_geopolitical_bloc, classify_mission_cohort


def load_satcat_catalog(data_dir: str = "data/raw") -> pd.DataFrame:
    """
    Load and consolidate all cached SATCAT metadata records.
    Deduplicates by NORAD_CAT_ID.
    """
    satcat_files = glob.glob(os.path.join(data_dir, "satcat_*.csv"))
    dfs = []
    for f in satcat_files:
        try:
            df = pd.read_csv(f)
            dfs.append(df)
        except Exception as e:
            print(f"Warning loading {f}: {e}")
            
    if not dfs:
        return pd.DataFrame()
        
    merged = pd.concat(dfs, ignore_index=True)
    # Deduplicate by NORAD_CAT_ID
    if "NORAD_CAT_ID" in merged.columns:
        merged = merged.drop_duplicates(subset=["NORAD_CAT_ID"]).copy()
    return merged


def load_all_satellites(data_dir: str = "data/raw") -> pd.DataFrame:
    """
    Load all active operational satellites and debris from GP files.
    Merges with SATCAT metadata for owner, launch date, and apogee/perigee.
    Adds geopolitical bloc and mission cohort classifications.
    """
    gp_files = sorted(glob.glob(os.path.join(data_dir, "gp_*.csv")))
    satcat_df = load_satcat_catalog(data_dir)
    
    records = []
    seen_norad = set()
    
    for f in gp_files:
        tag = os.path.basename(f).replace("gp_", "").replace(".csv", "")
        is_debris = "debris" in tag
        
        try:
            df = pd.read_csv(f)
            df.columns = [c.strip() for c in df.columns]
            
            for _, row in df.iterrows():
                norad_id = int(row.get("NORAD_CAT_ID", 0))
                if norad_id in seen_norad or norad_id == 0:
                    continue
                seen_norad.add(norad_id)
                
                name = str(row.get("OBJECT_NAME", "")).strip()
                obj_id = str(row.get("OBJECT_ID", "")).strip()
                epoch = str(row.get("EPOCH", "")).strip()
                
                # Mean motion (rev/day) -> semi-major axis (km)
                # n (rev/day) -> n (rad/s) = n * 2*pi / 86400
                # mu = 398600.4418 km^3/s^2, a = (mu / n^2)^(1/3)
                mean_motion = float(row.get("MEAN_MOTION", 15.0))
                ecc = float(row.get("ECCENTRICITY", 0.0))
                inc = float(row.get("INCLINATION", 0.0))
                raan = float(row.get("RA_OF_ASC_NODE", 0.0))
                arg_per = float(row.get("ARG_OF_PERICENTER", 0.0))
                mean_anomaly = float(row.get("MEAN_ANOMALY", 0.0))
                bstar = float(row.get("BSTAR", 0.0))
                
                n_rad_s = mean_motion * (2.0 * 3.141592653589793 / 86400.0)
                if n_rad_s > 0:
                    a_km = (398600.4418 / (n_rad_s**2)) ** (1.0 / 3.0)
                    perigee_km = a_km * (1.0 - ecc) - 6378.137
                    apogee_km = a_km * (1.0 + ecc) - 6378.137
                    altitude_km = (perigee_km + apogee_km) / 2.0
                else:
                    altitude_km = 0.0
                    perigee_km = 0.0
                    apogee_km = 0.0
                
                # Default owner from satcat or heuristic
                owner = "US" if "STARLINK" in name else "UNK"
                launch_date = ""
                obj_type = "DEB" if is_debris else "PAY"
                
                # Check satcat match
                if not satcat_df.empty and "NORAD_CAT_ID" in satcat_df.columns:
                    match = satcat_df[satcat_df["NORAD_CAT_ID"] == norad_id]
                    if not match.empty:
                        m_row = match.iloc[0]
                        owner = str(m_row.get("OWNER", owner)).strip()
                        launch_date = str(m_row.get("LAUNCH_DATE", "")).strip()
                        obj_type = str(m_row.get("OBJECT_TYPE", obj_type)).strip()
                
                # Fallback owner heuristics for debris
                if is_debris:
                    if "COSMOS" in tag:
                        owner = "CIS"
                    elif "FENGYUN" in tag:
                        owner = "PRC"
                    elif "IRIDIUM" in tag:
                        owner = "US"
                        
                bloc = get_geopolitical_bloc(owner, name)
                cohort = "Orbital Debris" if is_debris or obj_type == "DEB" else classify_mission_cohort(name, tag)
                
                records.append({
                    "NORAD_CAT_ID": norad_id,
                    "OBJECT_NAME": name,
                    "OBJECT_ID": obj_id,
                    "EPOCH": epoch,
                    "MEAN_MOTION": mean_motion,
                    "ECCENTRICITY": ecc,
                    "INCLINATION": inc,
                    "RA_OF_ASC_NODE": raan,
                    "ARG_OF_PERICENTER": arg_per,
                    "MEAN_ANOMALY": mean_anomaly,
                    "BSTAR": bstar,
                    "ALTITUDE_KM": altitude_km,
                    "APOGEE_KM": apogee_km,
                    "PERIGEE_KM": perigee_km,
                    "OWNER": owner,
                    "LAUNCH_DATE": launch_date,
                    "OBJECT_TYPE": obj_type,
                    "GROUP_TAG": tag,
                    "GEOPOLITICAL_BLOC": bloc,
                    "MISSION_COHORT": cohort,
                })
        except Exception as e:
            print(f"Error processing {f}: {e}")
            
    df_all = pd.DataFrame(records)
    return df_all
