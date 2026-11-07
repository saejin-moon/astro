# Astropolitics: Satellite Trajectory & Orbital Inequity Analysis

A quantitative research toolkit using CelesTrak satellite data and 30-day SGP4 orbit propagation to analyze astropolitical inequality, orbital commons enclosure, and surveillance disparities.

---

## Quickstart with `uv`

This project is configured as a native [`uv`](https://docs.astral.sh/uv/) project with dependency resolution and lockfile management via `uv.lock`.

### 1. Synchronize Dependencies
To create the virtual environment and install all locked dependencies:
```bash
uv sync
```

### 2. Run the Full Analysis Pipeline
Execute the end-to-end data ingestion, 30-day vectorized SGP4 propagation, metric computation, and figure generation:
```bash
uv run astro-pipeline
```
*(Or directly via python: `uv run python src/run_pipeline.py`)*

### 3. Run Automated Tests
```bash
uv run pytest
```

### 4. Launch Jupyter Notebook / Lab
Open the interactive research notebook:
```bash
uv run jupyter lab notebooks/astropolitics_analysis.ipynb
```
or
```bash
uv run jupyter notebook notebooks/astropolitics_analysis.ipynb
```

---

## Key Deliverables

* **Executed Research Notebook**: [`notebooks/astropolitics_analysis.ipynb`](notebooks/astropolitics_analysis.ipynb)
* **Astropolitics Policy Report**: [`reports/astropolitics_report.md`](reports/astropolitics_report.md)
* **Static Publication Figures**:
  * `output/figures/world_satellite_activity_heatmap.png` (Full-world activity heatmap)
  * `output/figures/volumetric_orbital_density.png` (The 550 km Wall)
  * `output/figures/temporal_enclosure_velocity.png` (1957–2026 Inflection)
  * `output/figures/geo_longitudinal_sovereignty.png` (Empirical Bogotá Test)
  * `output/figures/climate_vulnerability_paradox.png` (Climate-Surveillance Paradox)
  * `output/figures/atmospheric_deorbit_mass.png` (Mesospheric Alumina Deposition)
  * `output/figures/global_satellite_density_map.png`
  * `output/figures/latitudinal_dwell_profile.png`
  * `output/figures/orbital_inequality_lorenz.png`
  * `output/figures/regional_coverage_comparison.png`
  * `output/figures/mission_cohort_breakdown.png`
* **Interactive Web Visualizations (Plotly HTML)**:
  * `output/interactive/interactive_world_activity_heatmap.html`
  * `output/interactive/interactive_orbital_scatter.html`
  * `output/interactive/interactive_trajectory_map.html`
  * `output/interactive/interactive_revisit_dashboard.html`
* **Typst Publications (Source & Compiled PDFs)**:
  * `documents/research_findings.pdf` (Academic Journal Paper)
  * `documents/policy_memo.pdf` (Executive Policy Briefing)
  * `documents/blog_post.pdf` (Public Long-form Essay)

---

## License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
