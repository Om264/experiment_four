import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# Part 1: DEM Data Preparation
# ============================================================
def generate_dem(shape=(100, 100), elev_min=30, elev_max=80, style="terrain"):
    np.random.seed(42)
    if style == "random":
        dem = np.random.uniform(elev_min, elev_max, shape)
    elif style == "slope":
        x = np.linspace(0, 1, shape[1])
        y = np.linspace(0, 1, shape[0])
        xx, yy = np.meshgrid(x, y)
        dem = elev_min + (elev_max - elev_min) * (xx * 0.7 + yy * 0.3)
    else:
        base = np.random.uniform(elev_min, elev_max, shape)
        x = np.linspace(0, 1, shape[1])
        y = np.linspace(0, 1, shape[0])
        xx, yy = np.meshgrid(x, y)
        trend = elev_min + (elev_max - elev_min) * (xx * 0.5 + yy * 0.3)
        dem = 0.6 * trend + 0.4 * base
    return dem

def load_dem(filepath=None, shape=(100, 100), elev_min=30, elev_max=80):
    if filepath and os.path.exists(filepath):
        dem = np.load(filepath)
        print(f"Loaded DEM from {filepath}, shape: {dem.shape}")
    else:
        dem = generate_dem(shape, elev_min, elev_max, style="terrain")
        print(f"Generated synthetic DEM, shape: {dem.shape}")
    return dem

def save_dem(dem, filepath):
    np.save(filepath, dem)
    print(f"DEM saved to {filepath}")

# ============================================================
# Part 2: Flood Simulation
# ============================================================
def calculate_flood(dem, water_level):
    flooded_mask = dem < water_level
    depth_array = np.maximum(water_level - dem, 0)
    total_cells = dem.size
    flooded_cells = np.sum(flooded_mask)
    percentage = (flooded_cells / total_cells) * 100.0
    return flooded_mask, depth_array, percentage

# ============================================================
# Part 3: Visualization
# ============================================================
def setup_plot_style():
    plt.rcParams.update({
        'figure.dpi': 150,
        'font.size': 10,
        'axes.titlesize': 12,
        'axes.labelsize': 10,
    })

def visualize_flood(dem, flooded_mask, depth, water_level, save_path=None):
    setup_plot_style()
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    ax0 = axes[0, 0]
    im0 = ax0.imshow(dem, cmap="terrain", aspect="auto")
    ax0.set_title(f"Original DEM (Elevation)")
    plt.colorbar(im0, ax=ax0, label="Elevation (m)")

    ax1 = axes[0, 1]
    ax1.imshow(dem, cmap="gray", aspect="auto")
    overlay = np.ma.masked_where(~flooded_mask, flooded_mask)
    ax1.imshow(overlay, cmap="Blues", alpha=0.7, aspect="auto",
               vmin=0, vmax=1)
    ax1.set_title(f"Flood Extent at {water_level}m")
    from matplotlib.patches import Patch
    from matplotlib.colors import LinearSegmentedColormap
    ax1.legend(
        handles=[Patch(color="blue", alpha=0.5, label="Flooded")],
        loc="lower right",
    )

    ax2 = axes[1, 0]
    im2 = ax2.imshow(depth, cmap="Blues", aspect="auto", vmin=0)
    ax2.set_title(f"Inundation Depth at {water_level}m")
    plt.colorbar(im2, ax=ax2, label="Depth (m)")

    ax3 = axes[1, 1]
    ax3.axis("off")
    info_text = (
        f"Flood Analysis Summary\n"
        f"{'='*25}\n"
        f"Water Level: {water_level:.1f} m\n"
        f"DEM Min Elev: {dem.min():.1f} m\n"
        f"DEM Max Elev: {dem.max():.1f} m\n"
        f"Flooded Cells: {np.sum(flooded_mask):,}\n"
        f"Total Cells: {dem.size:,}\n"
        f"Flooded Area: {np.sum(flooded_mask) / dem.size * 100:.2f}%\n"
        f"Max Depth: {depth.max():.2f} m\n"
        f"Mean Depth: {depth[depth > 0].mean() if np.any(depth > 0) else 0:.2f} m"
    )
    ax3.text(0.1, 0.95, info_text, transform=ax3.transAxes,
             fontsize=11, verticalalignment="top",
             fontfamily="monospace",
             bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.3))

    plt.suptitle(f"Flood Inundation Analysis - Water Level {water_level}m",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Saved visualization to {save_path}")
    plt.close()

# ============================================================
# Part 4: Dynamic Simulation
# ============================================================
def simulate_rising_water(dem, levels, save_curve_path=None,
                          save_comparison_path=None):
    percentages = []
    depths = []
    flooded_cells_list = []

    for level in levels:
        mask, depth, pct = calculate_flood(dem, level)
        percentages.append(pct)
        depths.append(depth)
        flooded_cells_list.append(np.sum(mask))

    # Water Level vs Flooded Percentage
    setup_plot_style()
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ax1 = axes[0]
    ax1.plot(levels, percentages, "b-o", markersize=3, linewidth=1.5)
    ax1.axvline(x=dem.min(), color="green", linestyle="--",
                alpha=0.7, label=f"Min Elev = {dem.min():.1f}m")
    ax1.axvline(x=dem.max(), color="red", linestyle="--",
                alpha=0.7, label=f"Max Elev = {dem.max():.1f}m")
    ax1.set_xlabel("Water Level (m)")
    ax1.set_ylabel("Flooded Area (%)")
    ax1.set_title("Water Level vs Flooded Percentage")
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=8)

    ax2 = axes[1]
    ax2.plot(levels, flooded_cells_list, "r-s", markersize=3, linewidth=1.5)
    ax2.set_xlabel("Water Level (m)")
    ax2.set_ylabel("Number of Flooded Cells")
    ax2.set_title("Water Level vs Flooded Cell Count")
    ax2.grid(True, alpha=0.3)

    plt.suptitle("Dynamic Flood Simulation Results", fontsize=14,
                 fontweight="bold")
    plt.tight_layout()

    if save_curve_path:
        plt.savefig(save_curve_path, dpi=150, bbox_inches="tight")
        print(f"Saved flood curve to {save_curve_path}")

    # Side-by-side comparison at different water levels
    if save_comparison_path:
        comparison_levels = levels[::max(1, len(levels) // 5)]
        n = len(comparison_levels)
        cols = min(3, n)
        rows = int(np.ceil(n / cols))
        fig2, axes2 = plt.subplots(rows, cols, figsize=(cols * 5, rows * 4))
        axes2 = axes2.flatten() if n > 1 else [axes2]

        for i, level in enumerate(comparison_levels):
            mask, depth, pct = calculate_flood(dem, level)
            ax = axes2[i]
            ax.imshow(dem, cmap="gray", aspect="auto")
            overlay = np.ma.masked_where(~mask, mask)
            ax.imshow(overlay, cmap="Blues", alpha=0.6, aspect="auto")
            ax.set_title(f"WL = {level}m ({pct:.1f}% flooded)",
                         fontsize=9)
            ax.axis("off")

        for j in range(i + 1, len(axes2)):
            axes2[j].axis("off")

        plt.suptitle("Flood Extent at Different Water Levels",
                     fontsize=13, fontweight="bold")
        plt.tight_layout()
        plt.savefig(save_comparison_path, dpi=150, bbox_inches="tight")
        print(f"Saved comparison to {save_comparison_path}")

    plt.close()
    plt.close("all")

    return percentages, depths

def create_flood_animation(dem, levels, save_path, interval=200):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title("Flood Animation")

    def update(frame):
        ax.clear()
        level = levels[frame]
        mask, depth, pct = calculate_flood(dem, level)
        ax.imshow(dem, cmap="gray", aspect="auto")
        overlay = np.ma.masked_where(~mask, mask)
        ax.imshow(overlay, cmap="Blues", alpha=0.6, aspect="auto")
        ax.set_title(f"Water Level: {level}m | Flooded: {pct:.1f}%")
        ax.axis("off")

    ani = FuncAnimation(fig, update, frames=len(levels),
                        interval=interval, repeat=True)
    ani.save(save_path, writer="pillow", dpi=100)
    plt.close()
    print(f"Saved animation to {save_path}")

# ============================================================
# Part 5: Physical Validation
# ============================================================
def validate_results(dem, levels, percentages, depths):
    print("\n" + "=" * 60)
    print("PHYSICAL VALIDATION RESULTS")
    print("=" * 60)

    checks = []

    check1 = all(
        percentages[i] <= percentages[i + 1]
        for i in range(len(percentages) - 1)
    )
    checks.append(("Flooded area increases monotonically with water level",
                   check1))

    max_possible_depth = max(levels) - dem.min()
    actual_max_depth = max(d.max() for d in depths)
    check2 = abs(actual_max_depth - max_possible_depth) < 0.01
    checks.append(
        ("Max depth equals (water_level - min_elevation)", check2)
    )

    check3 = all(0 <= p <= 100 for p in percentages)
    checks.append(("Flooded percentage between 0-100%", check3))

    min_level = dem.min() - 5
    _, _, pct_below = calculate_flood(dem, min_level)
    check4a = pct_below < 0.1
    checks.append(
        (f"Edge case: water below min elev ({min_level}m) -> 0% flooded",
         check4a)
    )

    max_level = dem.max() + 5
    _, _, pct_above = calculate_flood(dem, max_level)
    check4b = abs(pct_above - 100) < 0.1
    checks.append(
        (f"Edge case: water above max elev ({max_level}m) -> 100% flooded",
         check4b)
    )

    _, depth_zero, _ = calculate_flood(dem, dem.min() - 1)
    check5 = depth_zero.max() == 0
    checks.append(("No flooding when water below all elevations", check5))

    all_pass = True
    for desc, result in checks:
        status = "PASS" if result else "FAIL"
        if not result:
            all_pass = False
        print(f"  [{status}] {desc}")

    print("-" * 60)
    print(f"  Overall Validation: {'ALL CHECKS PASSED' if all_pass else 'SOME CHECKS FAILED'}")
    print("=" * 60)

    return checks, all_pass

def calculate_flood_volume(dem, water_level, cell_area_m2=1):
    _, depth, _ = calculate_flood(dem, water_level)
    volume = np.sum(depth) * cell_area_m2
    return volume

# ============================================================
# Main Execution
# ============================================================
def main():
    print("=" * 60)
    print("SPECIALIZED EXPERIMENT 4: FLOOD INUNDATION ANALYSIS")
    print("=" * 60)

    # Part 1: DEM Data Preparation
    print("\n[PART 1] DEM Data Preparation")
    print("-" * 40)
    dem = load_dem()
    dem_path = os.path.join(OUTPUT_DIR, "dem_data.npy")
    save_dem(dem, dem_path)

    print(f"\nDEM Statistics:")
    print(f"  Shape: {dem.shape}")
    print(f"  Min Elevation: {dem.min():.2f} m")
    print(f"  Max Elevation: {dem.max():.2f} m")
    print(f"  Mean Elevation: {dem.mean():.2f} m")
    print(f"  Std Elevation: {dem.std():.2f} m")

    # Part 2: Flood Simulation
    print("\n[PART 2] Flood Simulation")
    print("-" * 40)
    test_level = 45.0
    mask, depth, pct = calculate_flood(dem, test_level)
    print(f"Water Level: {test_level}m")
    print(f"  Flooded cells: {np.sum(mask)} / {dem.size}")
    print(f"  Flooded area: {pct:.2f}%")
    print(f"  Max inundation depth: {depth.max():.2f} m")
    print(f"  Mean depth (flooded areas): {depth[depth > 0].mean():.2f} m")

    # Part 3: Visualization
    print("\n[PART 3] Visualization")
    print("-" * 40)
    vis_40_path = os.path.join(OUTPUT_DIR, "flood_extent_40m.png")
    mask_40, depth_40, pct_40 = calculate_flood(dem, 40)
    visualize_flood(dem, mask_40, depth_40, 40, save_path=vis_40_path)

    vis_50_path = os.path.join(OUTPUT_DIR, "flood_extent_50m.png")
    mask_50, depth_50, pct_50 = calculate_flood(dem, 50)
    visualize_flood(dem, mask_50, depth_50, 50, save_path=vis_50_path)

    # Part 4: Dynamic Simulation
    print("\n[PART 4] Dynamic Simulation")
    print("-" * 40)
    levels = np.arange(30, 81, 1)
    curve_path = os.path.join(OUTPUT_DIR, "flood_curve.png")
    comparison_path = os.path.join(OUTPUT_DIR, "flood_comparison.png")
    percentages, depths = simulate_rising_water(
        dem, levels,
        save_curve_path=curve_path,
        save_comparison_path=comparison_path,
    )

    # Part 5: Physical Validation
    print("\n[PART 5] Physical Validation")
    print("-" * 40)
    checks, all_pass = validate_results(dem, levels, percentages, depths)

    # Volume calculation (optional extension)
    print("\n[OPTIONAL EXTENSION] Flood Volume Calculation")
    print("-" * 40)
    for wl in [35, 45, 55, 65]:
        vol = calculate_flood_volume(dem, wl)
        print(f"  Water Level {wl}m: Volume = {vol:.1f} m3")

    print(f"\n{'=' * 60}")
    print("EXPERIMENT COMPLETE")
    print(f"{'=' * 60}")
    print(f"\nOutput files saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
