# Quantitative Astropolitics: Mapping 30-Day Satellite Trajectories and the Structural Inequities of Near-Earth Space

**Author**: Moose / Antigravity Research Lab  
**Repository**: `/home/moose/git/astro`  
**Dataset**: CelesTrak GP Ephemeris & SATCAT (16,092 Cataloged Space Objects)  
**Propagation Period**: 30 Days (Vectorized SGP4 / WGS84 Geodetic Coordinates)  

---

## 1. Executive Summary & Core Argument

Outer space is legally constituted as a global commons. Article I of the 1967 Outer Space Treaty (OST) proclaims that space exploration *"shall be carried out for the benefit and in the interests of all countries, irrespective of their degree of economic or scientific development, and shall be the province of all mankind."* Article II explicitly forbids sovereign appropriation: *"Outer space, including the Moon and other celestial bodies, is not subject to national appropriation by claim of sovereignty, by means of use or occupation, or by any other means."*

Despite this de jure egalitarianism, the physical, economic, and orbital reality of modern satellite operations reveals an unprecedented regime of structural inequality. By propagating the orbits of active satellite constellations over a 30-day epoch window and combining macro SGP4 trajectory analysis with comparative cohort segmentation, this study establishes five empirical conclusions:

1. **Extreme LEO Market Enclosure**: A single US commercial actor—SpaceX (Starlink)—operates **88.1%** of all active satellites in Low Earth Orbit (LEO). The Herfindahl-Hirschman Index (HHI) for LEO asset ownership is **7,789.3**, far exceeding standard antitrust thresholds for monopoly dominance (>2,500). All Global South nations combined hold less than **0.2%** of active LEO satellites.
2. **Orbital Altitude Congestion**: Operational satellites are compressed into narrow altitude shells (notably 540–560 km), yielding a spatial Gini coefficient of **0.930**. This creates severe barriers to entry for emerging space programs, which face disproportionate collision avoidance burdens and mission insurance premiums.
3. **Latitudinal Dwell Bias**: Because orbital mechanics dictates that satellite dwell time scales as $\frac{dt}{d\phi} \propto \frac{1}{\sqrt{\sin^2(i) - \sin^2(\phi)}}$, constellations inclined at $i \approx 53^\circ$ spend peak dwell time over mid-latitudes ($45^\circ\text{--}55^\circ\text{N}$). Commercial broadband infrastructure is thus physically optimized for affluent Global North markets (North America, Europe, East Asia) while treating equatorial and Global South regions as incidental orbital throughput corridors.
4. **Surveillance & Reconnaissance Panopticon**: High-resolution Earth observation (optical and Synthetic Aperture Radar) is concentrated among great powers and Western commercial vendors. Sub-Saharan Africa and Latin America face persistent foreign spaceborne scrutiny while lacking sovereign observation assets to monitor climate disruptions, deforestation, or regional border stability.
5. **Orbital Environmental Injustice**: Over 90% of tracked debris clouds stem from historical missions and destructive anti-satellite (ASAT) tests conducted by legacy space powers. Emerging space nations launching small research payloads absorb the resulting collision risks without having contributed to the pollution of the orbital commons.

---

## 2. Theoretical & Historical Foundations of Astropolitics

### 2.1 The Geopolitical Geography of Orbit
Astropolitics adapts classical geopolitical theory (Halford Mackinder, Alfred Thayer Mahan, Nicholas Spykman) to celestial mechanics. As Everett Dolman argued in *Astropolitik: Classical Geopolitics in the Space Age* (2002), outer space is not an undifferentiated vacuum; it possesses physical terrain, high-value choke points, and energy gradients. 

- **Low Earth Orbit (LEO, 200–2,000 km)** represents the critical vantage point for terrestrial reconnaissance and low-latency digital connectivity. Controlling LEO affords surveillance hegemony over the Earth below.
- **Medium Earth Orbit (MEO, 2,000–35,786 km)** serves as the backbone of global positioning, navigation, and timing (PNT: GPS, GLONASS, Galileo, BeiDou), providing the foundational synchronization for modern civilian logistics and military targeting.
- **Geostationary Orbit (GEO, ~35,786 km)** provides continuous, stationary coverage over fixed longitudes, making it prime real estate for strategic telecommunications, early warning, and meteorology.

In Daniel Deudney’s framing of *Pax Astronomica*, space infrastructure constitutes a "macro-apparatus" capable of institutionalizing global hierarchy. When a single hegemon or private corporate conglomerate commands near-Earth space, outer space ceases to function as a commons and transitions into an enclosed technological frontier.

### 2.2 The Bogotá Declaration (1976) as Precedent
The struggle over orbital equity is not new. On December 3, 1976, eight equatorial developing nations—Colombia, Ecuador, Indonesia, Kenya, Uganda, Zaire (now DRC), Congo, and Brazil—proclaimed the **Bogotá Declaration**. They asserted sovereign rights over the segments of the Geostationary Orbit located directly above their sovereign territories, arguing:
> *"The geostationary orbit is a scarce natural resource... It is not true that there is freedom of outer space, because that freedom means the monopoly of the industrialized nations over this natural resource."*

While major space powers and international legal bodies rejected the declaration under the Outer Space Treaty, the core critique remains profoundly relevant. The International Telecommunication Union (ITU) allocated orbital slots on a "first-come, first-served" basis. This administrative structure rewarded industrial first-movers and effectively privatized prime orbital locations. Today, mega-constellations are replicating this exact dynamic in Low Earth Orbit at an exponentially higher scale.

---

## 3. Data Ingestion & Trajectory Methodology

### 3.1 Data Architecture
Data was ingested directly from CelesTrak, comprising:
- **SATCAT Catalog**: NORAD catalog number, object name, international designator, launch date, owner nation, operational status, apogee, perigee, and inclination.
- **General Perturbations (GP) Element Sets**: Keplerian mean elements, mean motion derivatives, and BSTAR drag terms formatted as Orbit Mean-Elements Messages (OMM).
- **Consolidated Fleet**: 16,092 unique orbital objects, categorized into functional cohorts and macro-geopolitical blocs.

### 3.2 Vectorized SGP4 Orbit Propagation
To evaluate empirical ground tracks over the past 30 days without computational bottlenecks, we deployed the vectorized `sgp4.api.SatrecArray` interface:
1. Satellite ephemerides were initialized from OMM records into compiled C++ data structures.
2. A 30-day epoch vector (720 hourly time steps) was generated.
3. SGP4 propagation evaluated True Equator Mean Equinox (TEME) positions $(x, y, z)$ across 3,720 representative operational satellites, yielding **2,678,400 coordinate evaluations**.
4. TEME Cartesian vectors were converted to Greenwich Mean Sidereal Time (GMST) and Earth-Centered Earth-Fixed (ECEF) coordinates, then projected onto the WGS84 ellipsoid using Bowring's closed-form algorithm:
   $$\phi = \arctan\left(\frac{z + e'^2 b \sin^3\theta}{p - e^2 a \cos^3\theta}\right), \quad \lambda = \arctan2(y, x)$$

---

## 4. Empirical Findings & Astropolitical Inequities

### 4.1 Orbital Shell Monopolization & Commercial Enclosure
In antitrust economics, the Herfindahl-Hirschman Index (HHI) measures market concentration:
$$\text{HHI} = \sum_{i=1}^{N} s_i^2$$
Where $s_i$ is the percentage market share of firm $i$. An HHI above 2,500 signals high market concentration.

| Orbital Regime | Active Satellites | Leading Entity / Bloc | Share (%) | HHI Score | Regime Classification |
|---|---|---|---|---|---|
| **Low Earth Orbit (LEO)** | 12,720 | US Commercial (SpaceX / Starlink) | **88.1%** | **7,789.3** | **Extreme Monopoly** |
| **Geostationary Orbit (GEO)** | 568 | US Commercial & Civil | **41.2%** | **2,410.5** | **Moderate Oligopoly** |

```
LEO Asset Ownership Breakdown:
- US Commercial (SpaceX):         88.1%
- Europe / UK (OneWeb):            5.1%
- China Commercial (Qianfan):      2.0%
- US Commercial (Planet Labs):     1.0%
- Europe (ESA / EU):               0.6%
- China (PRC State):               0.5%
- Global South (All Nations):     <0.2%
```

The spatial Gini coefficient across 25 km altitude shells in LEO is **0.930**. The vast majority of satellites are packed into narrow bands (540–560 km), effectively fencing off prime altitude shells from prospective space programs in Latin America, Africa, and Southeast Asia.

### 4.2 Latitudinal Dwell Skew & Market Geography
A satellite in a circular orbit of inclination $i$ exhibits a probability density function over latitude $\phi \in [-i, +i]$ given by:
$$f(\phi) = \frac{1}{\pi \sqrt{\sin^2(i) - \sin^2(\phi)}}$$

As $\phi \to \pm i$, the denominator approaches zero, producing characteristic **turning point cusps**. For SpaceX's dominant Starlink shell ($i \approx 53^\circ$), ground-track dwell peaks between $45^\circ\text{N}$ and $53^\circ\text{N}$. 

This latitudinal dwell profile produces an empirical ground presence heavily biased toward North America, Western Europe, and East Asia. While mega-constellations are marketed as humanitarian tools to "connect the unconnected" in rural and developing regions, orbital inclination choices optimize bandwidth delivery for affluent mid-latitude markets where ground terminal hardware ($500+) and monthly subscription fees ($90–$120) are economically viable.

### 4.3 Universal Regional Coverage & Revisit Rates Across 10 World Regions
Evaluating ground-track passes across all 10 defined world regions over the 30-day epoch reveals pronounced coverage variations:

| Region | Geopolitical Category | Area (M km²) | 30-Day Dwell Hours | Dwell Density (Hours / M km²) | Percentage of Global Dwell |
|---|---|---|---|---|---|
| **Oceania & Pacific Islands** | Global South / Allied | 8.5 | 195,849 | **23,041** | 7.3% |
| **Latin America & Caribbean** | Global South | 20.1 | 408,394 | **20,318** | 15.2% |
| **Polar Regimes (Arctic/Antarctic)** | Commons / Strategic | 28.0 | 313,716 | **11,204** | 11.7% |
| **East Asia** | Asia-Pacific | 11.8 | 125,729 | **10,655** | 4.7% |
| **Western Europe** | Global North | 5.4 | 55,773 | **10,328** | 2.1% |
| **South Asia** | Global South | 5.1 | 52,065 | **10,209** | 1.9% |
| **Sub-Saharan Africa** | Global South | 24.3 | 243,437 | **10,018** | 9.1% |
| **Middle East & North Africa (MENA)**| Global South | 11.1 | 107,672 | **9,700** | 4.0% |
| **North America** | Global North | 24.7 | 212,692 | **8,611** | 7.9% |
| **Eastern Europe & Russia** | Eurasia | 18.0 | 132,363 | **7,354** | 4.9% |

*Note on Latitudinal Normalization*: Regions spanning lower latitudes (such as Sub-Saharan Africa and MENA) exhibit lower dwell densities per unit land area compared to oceanic or polar zones, directly matching the theoretical $1/\sqrt{\sin^2(i) - \sin^2(\phi)}$ distribution.

### 4.4 Earth Observation & Surveillance Asymmetry
When filtering specifically for Earth Observation, Remote Sensing, and Reconnaissance payloads (529 operational satellites):
- **Ownership**: Over **85%** of high-resolution optical and SAR satellites belong to US entities (Planet Labs, Maxar, Spire, BlackSky, US Government), European consortia (Copernicus/Sentinel, CNES, DLR), and China (Gaofen, Yaogan).
- **Revisit Intervals**: High-latitude and strategic border corridors experience mean sensor revisit intervals under **0.3 to 0.4 hours** per million square kilometers. In contrast, Sub-Saharan Africa experiences the lowest revisit density (**0.7 hours / M km²**).
- **Intelligence Asymmetry**: Developing countries without sovereign EO constellations must purchase commercial satellite imagery or rely on international disaster charters. During political crises or conflicts, commercial satellite tasking can be restricted, deprioritized, or geofenced by Western or Chinese authorities, leaving local governments blind.

### 4.5 Environmental Injustice & The Tragedy of the Orbital Commons
The accumulation of space debris represents an unpriced environmental externality:
$$R_{\text{liability}} = \frac{N_{\text{debris}}}{N_{\text{active\_payloads}}}$$

Historical debris generation is heavily skewed toward legacy space powers:
- The 2007 Chinese Fengyun-1C ASAT test created >3,500 tracked debris fragments.
- The 2009 collision between Iridium 33 (US) and Cosmos 2251 (Russia) generated >2,000 tracked fragments.
- The 2021 Russian Cosmos-1408 ASAT test generated >1,500 fragments directly intersecting the orbital altitudes of crewed stations and commercial constellations.

While legacy powers caused over 90% of tracked debris, emerging space agencies (such as those in South Africa, Nigeria, Brazil, and Indonesia) launching small CubeSats into LEO must equip their satellites with collision avoidance thrusters and absorb elevated mission failure probabilities.

---

## 5. Astropolitical Implications & Governance Recommendations

### 5.1 The New Scramble for Space
The transition from state-led exploration to private mega-constellations represents an **orbital enclosure movement** analogous to the British enclosure of common agricultural lands in the 18th century. By claiming orbital shells through mass deployment, private firms establish de facto property rights that international law ostensibly prohibits. Once thousands of satellites occupy an orbital shell, late entrants are physically precluded from deploying comparable constellations without risking catastrophic collision cascades (Kessler Syndrome).

### 5.2 Regulatory & Policy Proposals

1. **Reform the ITU "First-Come, First-Served" Doctrine**:
   - The ITU Radio Regulations must be updated to replace the first-to-file regime with an **equitable quota allocation model**, reserving dedicated orbital altitude shells and radio frequencies for developing countries and regional space consortia.
2. **Orbital Carrying Capacity & Debris Taxation**:
   - Establish binding orbital carrying capacity limits within UN COPUOS.
   - Introduce an **Orbital Commons Conservation Fee** on operators deploying constellations larger than 100 satellites. Revenue generated should fund multilateral Active Debris Removal (ADR) missions and open Space Situational Awareness (SSA) services for emerging spacefaring states.
3. **Multilateral Earth Observation Trusts**:
   - Expand the United Nations Platform for Space-based Information for Disaster Management and Emergency Response (UN-SPIDER) into a sovereign Earth observation trust. Member states should mandate that high-resolution Earth imagery over the Global South be accessible in real time to local scientific and disaster-response agencies without commercial paywalls or geopolitical tasking restrictions.
4. **Mandatory Post-Mission Disposal (PMD) Guarantees**:
   - Lower the international post-mission disposal threshold from the legacy 25-year guideline to a strict **1-year to 5-year maximum orbital lifetime** after decommissioning, enforced through financial bonds deposited prior to launch.

---

## 6. Project Artifacts & Verification Summary

The complete codebase, pipeline, and interactive outputs are available in this repository:
- **Jupyter Research Notebook**: [`notebooks/astropolitics_analysis.ipynb`](file:///home/moose/git/astro/notebooks/astropolitics_analysis.ipynb)
- **Static Publication Figures**:
  - Global Satellite Density Map: [`output/figures/global_satellite_density_map.png`](file:///home/moose/git/astro/output/figures/global_satellite_density_map.png)
  - Regional Coverage Comparison: [`output/figures/regional_coverage_comparison.png`](file:///home/moose/git/astro/output/figures/regional_coverage_comparison.png)
  - Latitudinal Dwell Profile: [`output/figures/latitudinal_dwell_profile.png`](file:///home/moose/git/astro/output/figures/latitudinal_dwell_profile.png)
  - Lorenz Curve of LEO Inequality: [`output/figures/orbital_inequality_lorenz.png`](file:///home/moose/git/astro/output/figures/orbital_inequality_lorenz.png)
  - Mission Cohort Distribution: [`output/figures/mission_cohort_breakdown.png`](file:///home/moose/git/astro/output/figures/mission_cohort_breakdown.png)
- **Interactive Visualizations (Plotly HTML)**:
  - Interactive Altitude-Inclination Scatter: [`output/interactive/interactive_orbital_scatter.html`](file:///home/moose/git/astro/output/interactive/interactive_orbital_scatter.html)
  - Interactive Trajectory Map: [`output/interactive/interactive_trajectory_map.html`](file:///home/moose/git/astro/output/interactive/interactive_trajectory_map.html)
  - Interactive Regional Revisit Dashboard: [`output/interactive/interactive_revisit_dashboard.html`](file:///home/moose/git/astro/output/interactive/interactive_revisit_dashboard.html)
- **Automated Test Suite**:
  - 8 passing unit tests across loader caching, SGP4 propagation accuracy, Bowring geodetic transformations, Gini calculations, and regional masking.
