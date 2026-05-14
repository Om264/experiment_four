import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

dem = np.load(os.path.join(OUTPUT_DIR, "dem_data.npy"))
levels = np.arange(30, 76, 0.5)

fig, ax = plt.subplots(figsize=(8, 6))
fig.subplots_adjust(bottom=0.1)

def update(frame):
    ax.clear()
    level = levels[frame]
    mask = dem < level
    depth = np.maximum(level - dem, 0)
    pct = np.sum(mask) / dem.size * 100
    ax.imshow(dem, cmap="gray", aspect="auto")
    overlay = np.ma.masked_where(~mask, mask)
    ax.imshow(overlay, cmap="Blues", alpha=0.6, aspect="auto")
    ax.set_title(f"Water Level: {level:.1f}m | Flooded: {pct:.1f}%",
                 fontsize=13, fontweight="bold")
    ax.axis("off")

ani = FuncAnimation(fig, update, frames=len(levels), interval=150, repeat=True)
gif_path = os.path.join(OUTPUT_DIR, "flood_animation.gif")
ani.save(gif_path, writer="pillow", dpi=100)
plt.close()
print(f"Saved animation to {gif_path}")
print(f"Frames: {len(levels)}, Levels: {levels[0]:.1f}m to {levels[-1]:.1f}m")
