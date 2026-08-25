"""Generates oblateearth.png – the sphere vs. reference ellipsoid diagram.

Run from this folder:  python oblateearth.py
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse

EQUATORIAL_KM = 6378
POLAR_KM = 6357

# the real flattening (~0.3%) is invisible at this size, so it is exaggerated
a, b = 1.0, 0.9

fig, ax = plt.subplots(figsize=(6.2, 5.6))

ax.add_patch(Ellipse((0, 0), 2 * a, 2 * b, facecolor="#9BD7D8",
                     edgecolor="#03A3A6", linewidth=2, zorder=1))
ax.add_patch(Circle((0, 0), b, facecolor="white", edgecolor="#5A5A5A",
                    linewidth=1.6, linestyle="--", zorder=2))

# axes of the ellipsoid
ax.annotate("", xy=(0, b), xytext=(0, 0), zorder=3,
            arrowprops=dict(arrowstyle="->", color="#1A1A1A", linewidth=1.4))
ax.annotate("", xy=(a, 0), xytext=(0, 0), zorder=3,
            arrowprops=dict(arrowstyle="->", color="#1A1A1A", linewidth=1.4))
ax.text(-0.06, b / 2, f"{POLAR_KM:,} km".replace(",", " "), rotation=90,
        ha="right", va="center", fontsize=11)
ax.text(a / 2, -0.07, f"{EQUATORIAL_KM:,} km".replace(",", " "),
        ha="center", va="top", fontsize=11)

# the difference between the two radii
ax.annotate(f"{EQUATORIAL_KM - POLAR_KM} km", xy=(0.985, 0.18), xytext=(1.28, 0.52),
            fontsize=11, ha="center",
            arrowprops=dict(arrowstyle="-", color="#5A5A5A", linewidth=1))

ax.plot([-a, a], [0, 0], color="#5A5A5A", linewidth=0.8, linestyle=":", zorder=3)
ax.text(-0.78, 0.05, "Equator", fontsize=9, color="#5A5A5A")
ax.text(0, b + 0.05, "N", ha="center", fontsize=12)
ax.text(0, -b - 0.05, "S", ha="center", va="top", fontsize=12)

ax.text(0, -1.22, "Sphere (dashed) vs. reference ellipsoid – flattening exaggerated",
        ha="center", fontsize=9, color="#5A5A5A")

ax.set_xlim(-1.35, 1.6)
ax.set_ylim(-1.3, 1.15)
ax.set_aspect("equal")
ax.axis("off")

fig.savefig("oblateearth.png", dpi=110, bbox_inches="tight", facecolor="white")
