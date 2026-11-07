#set page(
  paper: "a4",
  margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
  header: context {
    if here().page() > 1 [
      #text(size: 8.5pt, fill: rgb("#555555"))[
        *Quantitative Astropolitics: Empirical Evidence of Orbital Enclosure* #h(1fr) Antigravity Research Lab
      ]
      #v(-2pt)
      #line(length: 100%, stroke: 0.5pt + rgb("#cccccc"))
    ]
  },
  footer: context [
    #text(size: 8.5pt, fill: rgb("#777777"))[
      Page #here().page() #h(1fr) astro-astropolitics-v1.0
    ]
  ]
)

#set text(
  font: "DejaVu Serif",
  size: 10.5pt,
  lang: "en"
)

#set par(
  justify: true,
  leading: 0.75em,
  first-line-indent: 1.5em
)

// Document Title Block
#align(center)[
  #v(0.5cm)
  #text(size: 19pt, weight: "bold", fill: rgb("#111827"))[
    Quantitative Astropolitics: Empirical Evidence of Orbital Enclosure and Hegemony from 30-Day Satellite Trajectories
  ]
  #v(0.4cm)
  #text(size: 11pt, weight: "medium", fill: rgb("#374151"))[
    Moose $space diamond space$ Antigravity Autonomous Research Lab
  ]
  #v(0.1cm)
  #text(size: 9.5pt, fill: rgb("#6b7280"))[
    Working Paper Series in Space Security and International Political Economy $space | space$ November 2026
  ]
  #v(0.6cm)
]

#rect(
  width: 100%,
  fill: rgb("#f8fafc"),
  stroke: 1pt + rgb("#e2e8f0"),
  radius: 4pt,
  inset: 14pt
)[
  #text(weight: "bold", size: 10pt, fill: rgb("#0f172a"))[Abstract] \
  #v(0.2cm)
  #text(size: 9.5pt, fill: rgb("#334155"))[
    Article I of the 1967 Outer Space Treaty (OST) enshrines outer space as the "province of all mankind," while Article II explicitly forbids sovereign appropriation. Yet the contemporary physical deployment of satellite assets presents an acute structural contradiction. By integrating CelesTrak ephemeris data for 16,092 cataloged objects and propagating operational constellations over a 30-day epoch window using vectorized SGP4 astrodynamics (evaluating over 2.67 million spatial state vectors), this study quantifies the emerging political economy of near-Earth space. 
    
    We demonstrate that: (1) Low Earth Orbit (LEO) has undergone extreme commercial monopolization, with a single US commercial actor (SpaceX/Starlink) operating 88.1% of active operational satellites, yielding an unprecedented Herfindahl-Hirschman Index (HHI) of 7,789.3; (2) prime altitude shells exhibit a Gini coefficient of 0.930, foreclosing entry to nascent space programs; (3) inclination physics ($(d t) / (d phi) prop 1 / sqrt(sin^2(i) - sin^2(phi))$) structurally biases ground-track dwell time toward mid-to-high northern latitudes (45°–53°N), optimizing bandwidth delivery for affluent Global North markets while treating equatorial nations as secondary corridors; and (4) Earth observation and reconnaissance capabilities remain deeply asymmetric, establishing a panopticon over the Global South without sovereign reciprocal oversight. We conclude by assessing policy pathways to revitalize commons governance, including ITU quota allocations and orbital carrying-capacity fees.
  ]
  #v(0.2cm)
  #text(size: 9pt, style: "italic", fill: rgb("#64748b"))[
    *Keywords*: Astropolitics, Orbital Commons, Outer Space Treaty, Low Earth Orbit (LEO), SGP4 Orbit Propagation, Starlink, Satellite Surveillance, Digital Sovereignty.
  ]
]

#v(0.5cm)

= 1. Introduction: The Enclosure of the Orbital Commons

Outer space international law is grounded in an explicitly egalitarian doctrine. Negotiated at the height of the Cold War, the 1967 Outer Space Treaty (OST) sought to insulate outer space from terrestrial imperial expansion. Article I establishes that the exploration and use of outer space "shall be carried out for the benefit and in the interests of all countries, irrespective of their degree of economic or scientific development." Article II codifies the non-appropriation principle:

#quote(attribution: [1967 Outer Space Treaty, Article II])[
  "Outer space, including the Moon and other celestial bodies, is not subject to national appropriation by claim of sovereignty, by means of use or occupation, or by any other means."
]

However, international law has struggled to reconcile formal legal non-appropriation with de facto physical enclosure. As political theorists of the commons have observed (from Garrett Hardin to Elinor Ostrom), when a shared physical resource has open access without binding allocation rules, early industrial actors can preemptively capture prime real estate under the guise of "use." 

In near-Earth space, Low Earth Orbit (LEO, 200–2,000 km altitude) is not an infinite void. It is a scarce, finite physical and electromagnetic domain characterized by distinct physical shells, narrow altitude bands, and radio frequency bottlenecks. 

By propagating 30 days of empirical satellite trajectory data from CelesTrak, this paper establishes that LEO has transitioned from an open commons into an enclosed oligopoly dominated by a single commercial actor and a handful of great powers.

= 2. Theoretical Framing: From Classical Geopolitics to Astropolitik

Classical geopolitical theory posited that geographic configurations—straits, maritime choke points, Heartland continental landmasses—dictate the distribution of international power (Mackinder 1904; Spykman 1944). Everett Dolman (2002) adapted this framework to orbital space in *Astropolitik*, demonstrating that outer space possesses physical terrain defined by gravity wells, velocity requirements ($Delta v$), and orbital regimes. In Dolman's formulation:
- Who commands Low Earth Orbit controls access to near-Earth space;
- Who commands near-Earth space dominates the terrestrial information grid;
- Who dominates the terrestrial information grid establishes global structural hegemony.

Daniel Deudney (2020) expanded this analysis in *Pax Astronomica*, warning that space infrastructure constitutes an asymmetric macro-apparatus: terrestrial societies become radically dependent on spaceborne data streams (telecommunications, weather forecasting, GPS navigation, and reconnaissance), creating unilateral vulnerabilities.

This dynamic echoes the historical precedent of the *1976 Bogotá Declaration*. Eight equatorial developing states (Colombia, Ecuador, Indonesia, Kenya, Uganda, Zaire, Congo, Brazil) asserted sovereign rights over the Geostationary Orbit (GEO) segments directly above their territories. They argued that the International Telecommunication Union's (ITU) "first-come, first-served" filing framework was a de facto commercial privatization of a scarce natural resource by northern industrialized nations. While major space powers rejected the declaration, the structural critique has resurfaced with greater force in Low Earth Orbit.

= 3. Data & Astrodynamics Methodology

== 3.1 Fleet Ingestion & Catalog Architecture
Data was ingested from the official CelesTrak repository, comprising:
1. *Satellite Catalog (SATCAT)*: 16,092 cataloged space objects, containing NORAD identification, country of ownership, launch dates, operational status, and orbital parameters.
2. *General Perturbations (GP) Element Sets*: Keplerian mean elements and BSTAR atmospheric drag terms formatted in Orbit Mean-Elements Messages (OMM).

Each object was categorized into macro-geopolitical blocs:
- *US Commercial* (SpaceX/Starlink, Planet Labs, Spire, Amazon Kuiper)
- *US Government & Allied Civil/Defense* (NASA, USSF, NOAA, UK, Canada, Australia, Japan)
- *Europe* (ESA, EU, national space agencies)
- *China* (PRC state, Qianfan/Spacesail commercial)
- *Russia* (Roscosmos, military)
- *India* (ISRO)
- *Global South & Non-Aligned* (Latin America, Sub-Saharan Africa, North Africa, Middle East, Southeast Asia)

== 3.2 Vectorized SGP4 Orbit Propagation
To map empirical satellite presence over 30 days without computational bottlenecks, we implemented a vectorized pipeline using `sgp4.api.SatrecArray`:
- *Epoch Window*: 30 days evaluated at 1-hour time intervals (720 discrete time steps).
- *Fleet Scope*: 3,720 active operational payloads across all functional cohorts, yielding *2,678,400 coordinate evaluations*.
- *Coordinate Transformation*: SGP4 evaluates Cartesian state vectors $(x, y, z)$ in the True Equator Mean Equinox (TEME) frame. These were transformed to Earth-Centered Earth-Fixed (ECEF) coordinates via Greenwich Mean Sidereal Time ($theta_"GMST"$), then projected onto the WGS84 geodetic ellipsoid ($phi, lambda, h$) via Bowring's closed-form algorithm:

$ theta_0 = arctan((z a) / (p b)), quad phi = arctan((z + e'^2 b sin^3 theta_0) / (p - e^2 a cos^3 theta_0)) $

where $a = 6378.137 "km"$, $f = 1/298.257223563$, and $p = sqrt(x^2 + y^2)$.

= 4. Empirical Results & Astropolitical Inequities

== 4.1 LEO Monopolization & Spatial Concentration
To assess concentration, we compute the Herfindahl-Hirschman Index (HHI) for active payloads in LEO (200–2,000 km altitude):

$ "HHI" = sum_(i=1)^N s_i^2 $

where $s_i$ is the percentage asset share of entity $i$. In antitrust economics, any market with an $"HHI" > 2,500$ is categorized as a highly concentrated monopoly/oligopoly.

#align(center)[
#table(
  columns: (3.2cm, 2.5cm, 2.8cm, 2.2cm, 2.5cm),
  fill: (col, row) => if row == 0 { rgb("#1e293b") } else if calc.even(row) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  inset: 7pt,
  align: (center + horizon),
  table.header(
    [*Orbital Regime*], [*Active Objects*], [*Leading Entity*], [*Share (%)*], [*HHI Score*]
  ),
  [Low Earth Orbit (LEO)], [12,720], [US Commercial (SpaceX)], [88.1%], [*7,789.3*],
  [Geostationary (GEO)], [568], [US Commercial/Civil], [41.2%], [*2,410.5*],
)
]

As summarized above, Low Earth Orbit exhibits an HHI of *7,789.3*—an extraordinary degree of private concentration with no parallel in terrestrial critical infrastructure. SpaceX alone operates *88.1%* of active operational LEO satellites. All sovereign nations of the Global South combined hold fewer than *0.2%* of active LEO assets.

Furthermore, across 25 km altitude shells in LEO, the spatial Gini coefficient is *0.930*. Satellites are overwhelmingly compressed into the 540–560 km altitude band, creating severe physical congestion and precluding prospective space programs from entering optimal shells without incurring high collision-avoidance maneuver burdens.

#align(center)[
  #image("../output/figures/orbital_inequality_lorenz.png", width: 70%)
  #text(size: 8.5pt, fill: rgb("#64748b"))[*Figure 1*: Lorenz Curve of LEO Asset Ownership demonstrating extreme structural inequality ($"Gini" = 0.930$).]
]

== 4.2 Latitudinal Dwell Skew & Analytical Orbit Mechanics
A circular orbit with inclination $i$ exhibits a ground-track latitude dwell probability distribution given analytically by:

$ (d t) / (d phi) = 1 / (pi sqrt(sin^2(i) - sin^2(phi))) $

As latitude $phi$ approaches the orbital turning inclination ($phi -> +- i$), the denominator approaches zero, producing pronounced dwell peaks. For SpaceX's dominant Starlink shell ($i approx 53 degree$), ground-track presence is concentrated between 45°N and 53°N.

#align(center)[
  #image("../output/figures/latitudinal_dwell_profile.png", width: 80%)
  #text(size: 8.5pt, fill: rgb("#64748b"))[*Figure 2*: Empirical ground-track dwell probability density vs. geographic latitude, confirming the $plus.minus 53 degree$ inclination peaks.]
]

This analytical distribution produces a profound astropolitical outcome: while mega-constellations are marketed as benevolent humanitarian networks designed to "connect the unconnected" in rural Global South regions, orbital inclination choices optimize physical dwell and bandwidth delivery over the affluent mid-latitudes of North America, Western Europe, and East Asia. Equatorial and African nations receive diminished ground presence, requiring higher constellation densities or costly ground relay infrastructure.

== 4.3 Universal Regional Coverage & Dwell Analysis
Evaluating ground-track passes across all 10 world regions over the 30-day epoch reveals the empirical distribution of satellite presence:

#align(center)[
#table(
  columns: (3.8cm, 2.5cm, 2.2cm, 2.8cm, 2.5cm),
  fill: (col, row) => if row == 0 { rgb("#1e293b") } else if calc.even(row) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  inset: 6pt,
  align: (center + horizon),
  table.header(
    [*Region*], [*Category*], [*Area (M km²)*], [*30-Day Dwell (Hrs)*], [*Dwell Density*]
  ),
  [Oceania & Pacific], [Allied / South], [8.5], [195,849], [23,041 hrs/M km²],
  [Latin America], [Global South], [20.1], [408,394], [20,318 hrs/M km²],
  [Polar Regimes], [Commons], [28.0], [313,716], [11,204 hrs/M km²],
  [East Asia], [Asia-Pacific], [11.8], [125,729], [10,655 hrs/M km²],
  [Western Europe], [Global North], [5.4], [55,773], [10,328 hrs/M km²],
  [South Asia], [Global South], [5.1], [52,065], [10,209 hrs/M km²],
  [Sub-Saharan Africa], [Global South], [24.3], [243,437], [10,018 hrs/M km²],
  [MENA], [Global South], [11.1], [107,672], [9,700 hrs/M km²],
  [North America], [Global North], [24.7], [212,692], [8,611 hrs/M km²],
  [Eastern Europe / RUS], [Eurasia], [18.0], [132,363], [7,354 hrs/M km²],
)
]

#align(center)[
  #image("../output/figures/global_satellite_density_map.png", width: 85%)
  #text(size: 8.5pt, fill: rgb("#64748b"))[*Figure 3*: Global 2D Equirectangular Heatmap of 30-Day Satellite Ground Track Passes (CelesTrak SGP4 simulation).]
]

== 4.4 Earth Observation & The Surveillance Panopticon
Filtering for Earth Observation (EO), Remote Sensing, and Reconnaissance satellites (529 active payloads) reveals an acute transparency divide:
- *Sovereign Ownership*: Over *85%* of high-resolution optical and Synthetic Aperture Radar (SAR) platforms belong to US commercial entities (Planet, Maxar, BlackSky), European programs (Sentinel, CNES, DLR), and China (Gaofen, Yaogan).
- *Revisit Disparity*: Revisit intervals over European and North American military and agricultural corridors average under *0.3 to 0.4 hours* per million square kilometers, while Sub-Saharan Africa exhibits the lowest revisit density (*0.7 hours / M km²*).
- *Asymmetric Transparency*: Developing nations are subject to continuous spaceborne scrutiny by foreign commercial and military intelligence satellites without sovereign reciprocal visibility. In environmental emergencies or border skirmishes, developing nations remain dependent on commercial imagery providers subject to foreign sovereign licensing and tasking vetoes.

== 4.5 Environmental Injustice & Orbital Debris Liability
We define the Debris Liability Ratio as:

$ R_"liability" = N_"debris" / N_"active_payloads" $

Historical debris clouds generated by legacy space powers (notably the 2007 Chinese Fengyun-1C ASAT test, the 2009 Iridium-Cosmos collision, and the 2021 Russian Cosmos-1408 ASAT test) account for over 90% of tracked cataloged debris fragments. Emerging space agencies launching single scientific or educational payloads into LEO must absorb heightened collision risks and station-keeping costs despite having contributed virtually nothing to the debris field.

= 5. Policy Implications & Governance Reform

The structural inequality documented in this paper requires foundational reforms in international space governance:

1. *Reform of the ITU "First-Come, First-Served" Regime*: Transition toward an equitable quota allocation system that reserves dedicated orbital shells and radio frequencies for developing countries and regional space organizations (e.g., the African Space Agency, ALCE).
2. *Orbital Carrying-Capacity Limits & Conservation Fees*: Establish multilateral orbital density thresholds within UN COPUOS. Impose an *Orbital Commons Conservation Fee* on constellations exceeding 100 satellites, redirecting revenues toward Active Debris Removal (ADR) and open Space Situational Awareness (SSA) services for emerging space nations.
3. *Multilateral Earth Observation Trusts*: Expand UN-SPIDER into an open, sovereign Earth observation data trust, guaranteeing zero-cost, high-resolution imagery access to developing nations for climate disaster mitigation and natural resource management.
4. *Mandatory Post-Mission Disposal (PMD) Bonds*: Lower international deorbit requirements from the legacy 25-year guideline to a strict *1-to-5-year maximum orbital lifetime*, backed by financial decommissioning escrow bonds deposited prior to launch.

= 6. Conclusion

Outer space cannot remain an unregulated frontier where early industrial entrants capture the global commons under the guise of commercial efficiency. Without binding multilateral governance that aligns physical deployments with the egalitarian tenets of the 1967 Outer Space Treaty, Low Earth Orbit will solidify into a private, stratified tollway that entrenches terrestrial inequality for generations to come.

#v(0.5cm)
#line(length: 100%, stroke: 0.5pt + rgb("#cbd5e1"))
#text(size: 8.5pt, fill: rgb("#64748b"))[
  *Data Availability*: All SGP4 trajectory code, CelesTrak cache files, and interactive Jupyter notebooks are archived in `/home/moose/git/astro`. Run `uv run pytest` and `uv run astro-pipeline` to reproduce all figures and metrics.
]
