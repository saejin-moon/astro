#set page(
  paper: "a4",
  margin: (top: 2.8cm, bottom: 2.8cm, left: 3.2cm, right: 3.2cm),
  header: context {
    if here().page() > 1 [
      #text(size: 8pt, style: "italic", fill: rgb("#64748b"))[
        Who Owns the Sky? $space | space$ The New Scramble for Space
      ]
      #h(1fr)
      #text(size: 8pt, fill: rgb("#94a3b8"))[Antigravity Perspectives]
      #v(-2pt)
      #line(length: 100%, stroke: 0.5pt + rgb("#e2e8f0"))
    ]
  },
  footer: context [
    #text(size: 8pt, fill: rgb("#94a3b8"))[
      Page #here().page()
    ]
  ]
)

#set text(
  font: "DejaVu Serif",
  size: 11pt,
  lang: "en"
)

#set par(
  justify: true,
  leading: 0.85em,
  first-line-indent: 1.5em
)

// Category Kicker
#text(size: 9pt, weight: "bold", fill: rgb("#2563eb"))[
  ESSAY $space | space$ TECHNOLOGY & GEOPOLITICS
]
#v(0.2cm)

// Main Title
#block[
  #set par(leading: 0.4em)
  #text(size: 24pt, weight: "bold", fill: rgb("#0f172a"))[
    Who Owns the Sky? What 30 Days of Satellite Orbits Tell Us About the New Scramble for Space
  ]
]

#v(0.3cm)

// Subhead
#block[
  #set par(leading: 0.5em)
  #text(size: 13pt, style: "italic", fill: rgb("#475569"))[
    We tracked 16,000 objects in orbit over the past month. What we found wasn't an open frontier—it was a high-speed corporate enclosure of the orbital commons.
  ]
]

#v(0.4cm)

// Byline & Date
#grid(
  columns: (auto, 1fr),
  gutter: 12pt,
  align: (left, left),
  [
    #circle(radius: 14pt, fill: rgb("#e2e8f0"))[
      #align(center + horizon)[#text(size: 10pt, weight: "bold", fill: rgb("#475569"))[M]]
    ]
  ],
  [
    #text(size: 9.5pt, weight: "bold", fill: rgb("#1e293b"))[By Moose] \
    #text(size: 8.5pt, fill: rgb("#64748b"))[November 7, 2026 $space bullet space$ 11 min read]
  ]
)

#v(0.6cm)
#line(length: 100%, stroke: 0.5pt + rgb("#e2e8f0"))
#v(0.4cm)

Look up on a clear night away from city lights, and outer space still looks like an infinite, peaceful wilderness. A silent void governed by no king, bordered by no fences, belonging equally to everyone and no one. 

That romantic picture is codified in international law. In 1967, at the height of the Cold War, the world’s nations signed the Outer Space Treaty. Article I proclaimed that outer space was the "province of all mankind." Article II declared that no nation could claim sovereignty over any part of it by occupation, use, or any other means.

It is a beautiful sentiment. It is also completely detached from physical reality.

Over the past month, we pulled tracking ephemeris from CelesTrak for every cataloged object currently circling the Earth—over 16,000 satellites, spent rocket stages, and shards of debris. We fed their orbital elements into an SGP4 astrodynamics engine and simulated their exact ground tracks, second by second, over a 30-day window.

The resulting dataset tells an unmistakable story. Low Earth Orbit (LEO) is no longer an open commons. It is an enclosed industrial zone, dominated by a single commercial actor and configured to serve the wealthiest corners of the globe.

#v(0.3cm)

#rect(
  width: 100%,
  fill: rgb("#f8fafc"),
  stroke: (left: 3pt + rgb("#2563eb")),
  inset: (x: 14pt, y: 10pt)
)[
  #text(style: "italic", size: 10.5pt, fill: rgb("#1e293b"))[
    "A single private American corporation now controls over 88% of all operational satellites in Low Earth Orbit. All the nations of Latin America, Africa, and Southeast Asia combined own less than 0.2%."
  ]
]

#v(0.3cm)

== The Anatomy of an Orbital Monopoly

If you want to understand how concentrated Low Earth Orbit has become, you have to look at the numbers.

There are currently roughly 12,700 operational satellites in Low Earth Orbit (the band between 200 and 2,000 kilometers above the planet). Of those, *88.1% belong to one company: SpaceX's Starlink network*. 

To put that in perspective, economists measure market concentration using the Herfindahl-Hirschman Index (HHI). In standard antitrust law, any industry with an HHI over 2,500 is classified as a dangerous monopoly or oligopoly. The HHI for operational Low Earth Orbit satellites is *7,789.3*. 

#align(center)[
  #image("../output/figures/orbital_inequality_lorenz.png", width: 75%)
  #text(size: 8.5pt, fill: rgb("#64748b"))[*The Sky's Gini Coefficient*: Cumulative share of orbital actors versus satellite assets, showing extreme concentration ($"Gini" = 0.930$).]
]

Next in line is the UK-backed OneWeb, with about 5.1% of active satellites, followed by China's nascent Qianfan constellation at 2.0%. 

And the Global South? All the nations of Africa, Latin America, and Southeast Asia combined hold less than *0.2%* of active LEO satellites. 

This is not simply a commercial lead; it is an enclosure of prime real estate. Satellites do not drift randomly through space. They occupy specific, fuel-efficient altitude bands. Over 80% of all commercial satellites are crammed into a razor-thin shell between 540 and 560 kilometers above our heads. 

When a single company parks thousands of satellites in the exact same orbital corridor, it creates a physical barrier to entry. Every new satellite launched by Nigeria, Brazil, or Indonesia into that altitude must constantly maneuver to avoid colliding with a Starlink satellite, escalating fuel use, mission complexity, and insurance premiums.

== The Physics of Inequality

One of the most persistent marketing narratives of commercial mega-constellations is that they exist to "connect the unconnected"—bringing high-speed internet to remote villages in Kenya, schools in the Andes, or island communities in the South Pacific.

The orbital mechanics tell a much less flattering story.

When a satellite is launched into a circular orbit at an inclination $i$ (for example, Starlink's primary shell is inclined at $53 degree$ relative to the equator), orbital geometry dictates how much time it spends over each latitude band. The mathematical equation for dwell time is:

$ (d t) / (d phi) prop 1 / sqrt(sin^2(i) - sin^2(phi)) $

Because the denominator shrinks as latitude $phi$ approaches the orbital inclination $i$, satellites naturally spend the vast majority of their time lingering near their northern and southern turning points. 

#align(center)[
  #image("../output/figures/latitudinal_dwell_profile.png", width: 80%)
  #text(size: 8.5pt, fill: rgb("#64748b"))[*The Inclination Trap*: Empirical satellite dwell density peaks sharply at $plus.minus 53 degree$, clustering over mid-latitude nations.]
]

For a $53 degree$ constellation, that turning point sits squarely between *45°N and 53°N latitude*. 

Take a look at a globe: that latitude band covers Seattle, London, Paris, Frankfurt, and Tokyo. The satellite constellations overhead were physically engineered to maximize capacity where the money is: high-density corporate and residential subscribers in North America, Western Europe, and East Asia who can easily afford \$500 hardware dishes and \$100 monthly fees.

Equatorial nations, meanwhile, sit in a geometric trough. They receive the fewest satellite passes per unit area, meaning lower throughput and greater vulnerability to network congestion, unless foreign providers build expensive dedicated gateway stations on their soil.

== The Panopticon Overhead

The divide is even starker when you look at Earth observation and reconnaissance satellites.

Today, there are over 500 active satellites whose sole job is to point cameras, infrared sensors, and Synthetic Aperture Radar (SAR) down at the surface of the Earth. Over *85% of these eyes in the sky are owned by the United States, European nations, and China*.

Our 30-day trajectory run tracked every pass made by these observation platforms over the world's 10 major continental regions:

#align(center)[
#table(
  columns: (3.5cm, 2.5cm, 2.5cm, 3.2cm),
  fill: (col, row) => if row == 0 { rgb("#1e293b") } else if calc.even(row) { rgb("#f8fafc") } else { none },
  stroke: 0.5pt + rgb("#cbd5e1"),
  inset: 6pt,
  align: (center + horizon),
  table.header(
    [*Region*], [*Land Area*], [*30-Day Dwell*], [*Pass Density*]
  ),
  [Oceania & Pacific], [8.5 M km²], [195,849 hrs], [23,041 hrs/M km²],
  [Latin America], [20.1 M km²], [408,394 hrs], [20,318 hrs/M km²],
  [Western Europe], [5.4 M km²], [55,773 hrs], [10,328 hrs/M km²],
  [Sub-Saharan Africa], [24.3 M km²], [243,437 hrs], [10,018 hrs/M km²],
  [MENA], [11.1 M km²], [107,672 hrs], [9,700 hrs/M km²],
)
]

#align(center)[
  #image("../output/figures/global_satellite_density_map.png", width: 90%)
  #text(size: 8.5pt, fill: rgb("#64748b"))[*Global Pass Density Heatmap*: Satellite ground-tracks over 30 days, revealing the heavy bands crisscrossing the northern hemisphere.]
]

The result is what political scientists call *asymmetric transparency*. Great powers and Western commercial intelligence firms (Planet Labs, Maxar, BlackSky) can watch the Global South in near-real-time. They can monitor troop movements in the Sahel, count shipping containers in Latin American ports, and assess agricultural yields across South Asia before local governments even know the data exists.

Yet when developing nations face natural disasters—droughts, floods, or illegal mining—they must beg for access to foreign commercial feeds or wait for delayed imagery through international aid charters. During conflicts, those commercial feeds can be abruptly throttled, censored, or geofenced by corporate executives thousands of miles away.

== The Unpaid Bill of Space Debris

There is one more dimension of astropolitical inequity that rarely makes the headlines: who pays the ecological cost of space exploration?

Over the past seven decades, the United States, Russia, and China launched thousands of rockets and conducted destructive anti-satellite (ASAT) missile tests. The 2007 Chinese Fengyun-1C test alone obliterated a weather satellite into 3,500 tracked pieces of shrapnel. A 2009 collision between a dead Russian Cosmos satellite and an active American Iridium satellite spawned 2,000 more. In 2021, Russia blew up its own Cosmos-1408 satellite, spraying debris across the orbit of the International Space Station.

These thousands of high-speed bullets do not discriminate. They will orbit Earth for decades, traveling at 17,500 miles per hour.

When a developing nation like Kenya or Ecuador scrapes together several hundred thousand dollars to build and launch a university research CubeSat, they bear the full, unmitigated risk of colliding with debris generated by Cold War superpowers. The polluters made their profits and established their dominance; the latecomers inherit the minefield.

== Can the Commons Be Saved?

In 1976, eight equatorial countries signed the Bogotá Declaration, claiming that the geostationary orbit directly above their borders was a sovereign natural resource that northern industrialized nations were privatizing. Major powers laughed it off, arguing that the Outer Space Treaty guaranteed "freedom of space."

Fifty years later, that freedom looks an awful lot like the freedom of an industrial cartel to enclose the commons before anyone else can show up.

If we want near-Earth space to remain an engine of human progress rather than a private tollway, we need to treat orbital space like what it actually is: a fragile, shared ecosystem.

That means:
- *Ending the "First-Come, First-Served" Land Grab*: The International Telecommunication Union (ITU) must stop awarding orbital filings to whoever files the paperwork first. We need reserved quotas of orbital shells and frequencies set aside specifically for developing nations and regional space programs.
- *An Orbital Commons Conservation Fee*: Mega-constellations deploying thousands of mass-manufactured satellites should pay an annual fee into an international fund dedicated to cleaning up space debris and providing free orbital tracking to small space agencies.
- *Strict Deorbit Rules*: Any satellite launched into LEO should be legally required to deorbit within 1 to 5 years of mission completion, backed by a mandatory decommissioning bond deposited prior to launch.

Outer space was declared the province of all mankind because the architects of the space age understood what happens when technological superiority goes untamed. If we don’t act now, the sky above us will belong to whoever got there first—and the rest of the world will simply be renting the view.

#v(0.6cm)
#line(length: 100%, stroke: 0.5pt + rgb("#e2e8f0"))
#align(center)[
  #text(size: 8.5pt, fill: rgb("#64748b"))[
    *Antigravity Astropolitics Research Lab* $space | space$ Code, datasets, and reproduction scripts available in `/home/moose/git/astro`.
  ]
]
