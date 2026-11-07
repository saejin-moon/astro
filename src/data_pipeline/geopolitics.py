"""
Geopolitical categorization and mission cohort mapping for space objects.
"""

# NORAD / SATCAT Country Code to Macro Geopolitical Bloc
COUNTRY_BLOC_MAP = {
    # United States
    "US": "United States",
    
    # China
    "PRC": "China",
    
    # Russia / Former Soviet Union
    "CIS": "Russia",
    "RUS": "Russia",
    
    # European Union / ESA & European Nations
    "ESA": "Europe (ESA/EU)",
    "FRA": "Europe (National)",
    "DEU": "Europe (National)",
    "ITA": "Europe (National)",
    "ESP": "Europe (National)",
    "NLD": "Europe (National)",
    "BEL": "Europe (National)",
    "SWE": "Europe (National)",
    "NOR": "Europe (National)",
    "DNK": "Europe (National)",
    "FIN": "Europe (National)",
    "AUT": "Europe (National)",
    "POL": "Europe (National)",
    "PRT": "Europe (National)",
    "GRC": "Europe (National)",
    "EUM": "Europe (EUMETSAT)",
    
    # US Treaty Allies / Five Eyes / Developed Partners
    "GBR": "United Kingdom",
    "CAN": "US Allied Partners",
    "AUS": "US Allied Partners",
    "NZL": "US Allied Partners",
    "JPN": "Japan",
    "KOR": "US Allied Partners",
    "ISR": "US Allied Partners",
    
    # India
    "IND": "India",
    
    # Global South & Emerging Space Nations
    # Latin America
    "BRA": "Global South",
    "ARG": "Global South",
    "MEX": "Global South",
    "CHL": "Global South",
    "COL": "Global South",
    "PER": "Global South",
    "VEN": "Global South",
    "BOL": "Global South",
    "ECU": "Global South",
    "URY": "Global South",
    
    # Africa
    "ZAF": "Global South",
    "NGA": "Global South",
    "EGY": "Global South",
    "KEN": "Global South",
    "DZA": "Global South",
    "MAR": "Global South",
    "AGO": "Global South",
    "ETH": "Global South",
    "RWA": "Global South",
    "GHA": "Global South",
    "TUN": "Global South",
    "SDN": "Global South",
    
    # Middle East & Central Asia
    "TUR": "Global South",
    "SAU": "Global South",
    "UAE": "Global South",
    "QAT": "Global South",
    "IRN": "Global South",
    "PAK": "Global South",
    "KAZ": "Global South",
    "AZE": "Global South",
    
    # Southeast & South Asia
    "IDN": "Global South",
    "MYS": "Global South",
    "THA": "Global South",
    "VNM": "Global South",
    "PHL": "Global South",
    "SGP": "Global South",
    "BGD": "Global South",
    "LKA": "Global South",
}

def get_geopolitical_bloc(owner_code: str, object_name: str = "") -> str:
    """
    Classify satellite into macro astropolitical power blocs:
    - US Commercial (e.g. Starlink, Planet)
    - US Government / Military
    - China
    - Russia
    - Europe (ESA/EU/National)
    - India
    - Japan & Allied Partners
    - Global South & Emerging Space Nations
    - Other / International
    """
    owner = str(owner_code).strip().upper()
    name = str(object_name).strip().upper()
    
    # Specific commercial mega-constellations under US jurisdiction
    if "STARLINK" in name:
        return "US Commercial (SpaceX)"
    if "FLOCK" in name or "SKYSAT" in name or "PELICAN" in name:
        return "US Commercial (Planet Labs)"
    if "LEMUR" in name:
        return "US Commercial (Spire)"
    if "KUIPER" in name:
        return "US Commercial (Amazon)"
    if "ONEWEB" in name:
        return "Europe / UK Commercial (OneWeb)"
    if "QIANFAN" in name or "G60" in name or "SPACESCALE" in name:
        return "China Commercial (Qianfan)"
    if "HULIANWANG" in name or "GUOWANG" in name:
        return "China State (Guowang)"
    
    if owner == "US":
        return "United States (Civil / Defense)"
    if owner in ("PRC", "CHN"):
        return "China (PRC)"
    if owner in ("CIS", "RUS"):
        return "Russia"
    if owner in ("ESA", "FRA", "DEU", "ITA", "ESP", "NLD", "BEL", "SWE", "NOR", "DNK", "FIN", "AUT", "POL", "PRT", "GRC", "EUM"):
        return "Europe (ESA / EU)"
    if owner == "GBR":
        return "United Kingdom"
    if owner == "IND":
        return "India (ISRO)"
    if owner == "JPN":
        return "Japan (JAXA)"
    
    mapped = COUNTRY_BLOC_MAP.get(owner)
    if mapped:
        return mapped
    return "Other / International"


def classify_mission_cohort(object_name: str, group_tag: str = "") -> str:
    """
    Classify satellite into primary functional mission cohort:
    - Commercial Broadband (Mega-constellations)
    - Earth Observation & Remote Sensing
    - Positioning, Navigation & Timing (PNT)
    - Sovereign Defense & Communications
    - Science & Space Stations
    """
    name = str(object_name).strip().upper()
    tag = str(group_tag).strip().lower()
    
    # 1. Commercial Broadband
    if any(k in name for k in ["STARLINK", "ONEWEB", "KUIPER", "QIANFAN", "HULIANWANG", "O3B"]) or tag in ["starlink", "oneweb", "qianfan", "kuiper"]:
        return "Commercial Broadband"
    
    # 2. PNT
    if any(k in name for k in ["NAVSTAR", "GPS", "GLONASS", "COSMOS 24", "COSMOS 25", "GALILEO", "BEIDOU", "NAVIC", "QZSS"]) or tag in ["gps", "glonass", "galileo", "beidou", "gps-ops", "glo-ops"]:
        return "Positioning, Navigation & Timing (PNT)"
    
    # 3. Earth Observation & Remote Sensing
    if any(k in name for k in ["FLOCK", "SKYSAT", "LEMUR", "SENTINEL", "LANDSAT", "SPOT", "RADARSAT", "GAOFEN", "YAOGAN", "METEOSAT", "NOAA", "GOES", "COSMO", "TERRASAR", "ICEYE", "CAPELLA"]) or tag in ["resource", "weather", "sar", "planet", "spire"]:
        return "Earth Observation & Surveillance"
    
    # 4. Space Stations & Human Spaceflight
    if any(k in name for k in ["ISS", "ZARYA", "TIANHE", "WENTIAN", "MENGTIAN", "DRAGON", "SOYUZ", "SHENZHOU"]) or tag in ["stations"]:
        return "Space Stations & Crewed"
    
    # 5. Sovereign Defense / Military
    if any(k in name for k in ["USA ", "NROL", "KH-", "LACROSSE", "AEHF", "WGS", "SYRACUSE", "SKCN", "TDRS"]) or tag in ["military"]:
        return "Sovereign Defense & MilSat"
    
    # 6. Geostationary Telecom & General
    if tag == "geo":
        return "Geostationary Telecom"
    
    return "Science & Other Payloads"
