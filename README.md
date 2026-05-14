# Flood Inundation Analysis (DEM-based)

**Specialized Experiment 4 | Smart Water Lab Series**

## Overview

This experiment analyzes flood inundation using Digital Elevation Model (DEM) data. It implements spatial comparison algorithms to identify flooded areas based on water level, creates visual flood extent maps, and calculates flooded area percentages.

## Requirements

- Python 3.10+
- numpy
- matplotlib
- pillow (for animated GIF)

## Files

| File | Description |
|------|-------------|
| `flood_inundation.py` | Main implementation (all 5 parts + optional extensions) |
| `generate_animation.py` | Script to generate animated GIF |
| `dem_data.npy` | Generated DEM data (100x100 grid) |
| `flood_extent_40m.png` | Flood visualization at 40m water level |
| `flood_extent_50m.png` | Flood visualization at 50m water level |
| `flood_curve.png` | Water level vs flooded percentage plot |
| `flood_comparison.png` | Side-by-side flood extent comparison |
| `flood_animation.gif` | Animated rising water levels (30–75.5m) |
| `prompt_log.md` | Documentation of AI interactions |
| `experiment_report.md` | Full report with self-grading |

## Usage

```bash
python flood_inundation.py
python generate_animation.py
```

## Experiment Structure

1. **DEM Data Preparation** — Generate/load 100x100 DEM (30–80m)
2. **Flood Simulation** — `elevation < water_level` mask + depth calculation
3. **Visualization** — 4-panel plots (DEM, flood extent, depth heatmap, stats)
4. **Dynamic Simulation** — Loop 30–80m, plot flood curve
5. **Physical Validation** — 6 automated checks (all pass)

## Results

- **Validation**: All checks passed
- **Grade**: 100/100 (A)
- **Extensions**: Flood volume, animated GIF, real DEM support, comparison plots
