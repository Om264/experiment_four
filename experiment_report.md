# Experiment Report: Flood Inundation Analysis (DEM-based)

**Experiment:** Specialized Experiment 4
**Session:** Week 6 Session B | Smart Water Lab Series
**Date:** 2026-05-14

---

## 1. Requirements Summary

### Core Requirements
| Part | Task | Description |
|------|------|-------------|
| Part 1 | DEM Data Preparation | Create 100x100 grid, elevation 30-80m |
| Part 2 | Flood Simulation | Implement inundation calculation |
| Part 3 | Visualization | Create flood extent maps at 40m and 50m |
| Part 4 | Dynamic Simulation | Loop 30-80m, plot flood curve, verify monotonicity |
| Part 5 | Physical Validation | Validate correctness with 6 checks |

### Deliverables
- [x] `flood_inundation.py` - Main implementation
- [x] `dem_data.npy` - DEM data file
- [x] `flood_extent_40m.png` - Visualization at 40m
- [x] `flood_extent_50m.png` - Visualization at 50m
- [x] `flood_curve.png` - Water level vs flooded percentage
- [x] `prompt_log.md` - AI interaction log

### Optional Extensions
- [x] Flood volume calculation
- [x] Animated GIF of rising water levels
- [x] Real DEM loading support
- [x] Side-by-side comparison visualization
- [x] Summary statistics panel

---

## 2. Solution Approach

### Architecture
The solution follows a modular design with 5 core functions mapping directly to the 5 experiment parts:

```
flood_inundation.py
├── generate_dem()         # Part 1: Create synthetic DEM
├── load_dem()             # Part 1: Load real DEM
├── save_dem()             # Part 1: Save DEM data
├── calculate_flood()      # Part 2: Flood inundation logic
├── visualize_flood()      # Part 3: 4-panel visualization
├── simulate_rising_water() # Part 4: Dynamic simulation + curve
├── validate_results()     # Part 5: Physical validation
└── calculate_flood_volume() # Optional: Volume estimation
```

### Key Algorithm: Flood Inundation
```
flooded_mask = elevation < water_level
depth = max(water_level - elevation, 0)
flooded_percentage = (flooded_cells / total_cells) * 100
```

### Validation Logic
6 automated checks verify:
1. Monotonic increase of flooded area with water level
2. Max depth correctness formula
3. Percentage bounds (0-100%)
4. Edge case: water below min elevation → 0% flooded
5. Edge case: water above max elevation → 100% flooded
6. No flooding when water below all elevations

---

## 3. Results

### DEM Statistics
| Metric | Value |
|--------|-------|
| Shape | 100 x 100 |
| Min Elevation | 30.72 m |
| Max Elevation | 72.63 m |
| Mean Elevation | 51.88 m |
| Std Deviation | 7.66 m |

### Flood Simulation (Sample at 45m)
| Metric | Value |
|--------|-------|
| Water Level | 45.0 m |
| Flooded Cells | 1,995 / 10,000 |
| Flooded Area | 19.95% |
| Max Depth | 14.28 m |
| Mean Depth (flooded) | 4.00 m |

### Validation Results
| Check | Result |
|-------|--------|
| Monotonic increase | PASS |
| Max depth formula | PASS |
| Percentage 0-100% | PASS |
| Edge: below min | PASS |
| Edge: above max | PASS |
| No flooding below all | PASS |
| **Overall** | **ALL PASSED** |

### Flood Volume (Extension)
| Water Level | Volume (m³) |
|-------------|-------------|
| 35 m | 131.4 |
| 45 m | 7,971.8 |
| 55 m | 49,074.7 |
| 65 m | 132,153.2 |

---

## 4. Self-Grading

### Grading Rubric

| Criterion | Points | Weight | Self-Score | Justification |
|-----------|--------|--------|------------|---------------|
| DEM Data (loaded or generated correctly) | 15 | 15% | **15/15** | Synthetic DEM generated with realistic terrain blending (30-80m, 100x100), also supports loading real .npy files |
| Flood Calculation (correct logic) | 25 | 25% | **25/25** | Correct implementation using `elevation < water_level` boolean mask, depth = `max(water_level - elevation, 0)`, percentage calculation |
| Visualization (clear, informative plots) | 25 | 25% | **25/25** | 4-panel layout with DEM, flood overlay, depth heatmap, stats panel; colorbars, titles, and legends included |
| Dynamic Simulation (working, validated) | 20 | 20% | **20/20** | 30-80m loop at 1m increments; flood curve and comparison plot generated |
| Physical Validation (all checks pass) | 10 | 10% | **10/10** | All 6 validation checks passed (monotonicity, max depth, bounds, edge cases) |
| Prompt Log (documented AI interactions) | 5 | 5% | **5/5** | Comprehensive log of all 6 prompts and model responses |

### Bonus (Optional Extensions)
| Feature | Status |
|---------|--------|
| Flood Volume Calculation | Implemented |
| Animated GIF | Implemented (92 frames, 30-75.5m) |
| Real DEM Loading | Implemented |
| Side-by-Side Comparison | Implemented |
| Summary Statistics Panel | Implemented |

### Final Grade

| Component | Score | Weighted |
|-----------|-------|----------|
| DEM Data | 15/15 | 15.0% |
| Flood Calculation | 25/25 | 25.0% |
| Visualization | 25/25 | 25.0% |
| Dynamic Simulation | 20/20 | 20.0% |
| Physical Validation | 10/10 | 10.0% |
| Prompt Log | 5/5 | 5.0% |
| **Total** | **100/100** | **100.0%** |

**Grade: A (100/100)**

---

## 5. Output Files

| File | Description | Size |
|------|-------------|------|
| `flood_inundation.py` | Main implementation script | 12.9 KB |
| `dem_data.npy` | Generated DEM data (100x100) | 80.1 KB |
| `flood_extent_40m.png` | Flood visualization at 40m | 218.8 KB |
| `flood_extent_50m.png` | Flood visualization at 50m | 252.1 KB |
| `flood_curve.png` | Water level vs flooded percentage | 76.4 KB |
| `flood_comparison.png` | Side-by-side comparison | 181.6 KB |
| `flood_animation.gif` | Animated rising water levels | 6.2 MB |
| `generate_animation.py` | Animation generation script | 1.1 KB |
| `prompt_log.md` | AI interaction documentation | 2.8 KB |
| `experiment_report.md` | This report | 6.5 KB |

---

## 6. Discussion

### Physical Correctness
The simulation correctly demonstrates that flooded area increases monotonically with water level. At low water levels (<30m), no flooding occurs. At high water levels (>73m), 100% of the area is flooded. The maximum inundation depth correctly equals `(water_level - min_elevation)`.

### Edge Cases Verified
- **Below min elevation (25.7m):** 0% flooded ✓
- **Above max elevation (77.6m):** 100% flooded ✓
- **All depth values non-negative:** ✓

### Observations
- The flood curve shows an S-shaped (sigmoidal) pattern typical for terrains with a roughly normal elevation distribution
- Most rapid flooding occurs between 45-60m where the majority of cells are concentrated
- Volume increases non-linearly with water level (cubic relationship expected for area x depth)

### Limitations & Future Work
- Current model uses "bathtub" filling (no hydrological connectivity)
- Does not account for drainage paths or barriers
- Real DEM integration would require geospatial coordinate handling
- Could be extended with flood routing algorithms for more realistic results
