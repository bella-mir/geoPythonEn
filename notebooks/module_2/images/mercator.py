"""Generates mercator.png – how the Mercator projection is built, and what it costs.

Left: the cylinder wrapped around the globe, touching it at the equator.
Right: the graticule that results, carrying circles that are all the *same size
on the globe*. They stay circles – that is conformality, the property Mercator
was built for – and they grow towards the poles by exactly 1 / cos(latitude),
which is the area distortion the section goes on to discuss.

Run from this folder:  python mercator.py
"""

import matplotlib.pyplot as plt
import numpy as np

TEAL = "#03A3A6"
TEAL_LIGHT = "#9BD7D8"
GREY = "#5A5A5A"
INK = "#1A1A1A"
POINT = "#C1443C"

CUTOFF = 84.0        # the graticule is drawn to here; the poles never arrive
EQUATOR_RADIUS = 6.5  # radius of the equatorial circle, in degrees of longitude

# one circle per latitude, spread across the map so none of them overlap
CIRCLES = ((-75, -138), (-45, -70), (0, 0), (45, 70), (75, 138))


def mercator_y(lat_degrees):
    """Mercator northing, in the same units as longitude so the aspect is true."""
    lat = np.radians(lat_degrees)
    return np.degrees(np.log(np.tan(np.pi / 4 + lat / 2)))


fig = plt.figure(figsize=(11.6, 4.8))

# ------------------------------------------------- left: the construction
ax = fig.add_subplot(1, 2, 1, projection="3d")

angle = np.linspace(0, 2 * np.pi, 120)
for lat in range(-60, 61, 30):
    phi = np.radians(lat)
    r = np.cos(phi)
    ax.plot(r * np.cos(angle), r * np.sin(angle), np.full_like(angle, np.sin(phi)),
            color=GREY, linewidth=0.5, alpha=0.55)
theta = np.linspace(-np.pi / 2, np.pi / 2, 90)
for lon in range(0, 360, 30):
    lam = np.radians(lon)
    ax.plot(np.cos(theta) * np.cos(lam), np.cos(theta) * np.sin(lam), np.sin(theta),
            color=GREY, linewidth=0.5, alpha=0.55)

# the cylinder, tangent along the equator
height = np.linspace(-1.45, 1.45, 2)
grid_angle, grid_height = np.meshgrid(angle, height)
ax.plot_surface(np.cos(grid_angle), np.sin(grid_angle), grid_height,
                color=TEAL_LIGHT, alpha=0.25, linewidth=0, shade=False)
for end in (-1.45, 1.45):
    ax.plot(np.cos(angle), np.sin(angle), np.full_like(angle, end),
            color=TEAL, linewidth=1.1, alpha=0.8)

# the line of contact
ax.plot(np.cos(angle), np.sin(angle), np.zeros_like(angle),
        color=TEAL, linewidth=2.6, zorder=7)
ax.plot([0, 0], [0, 0], [-1.42, 1.42], color=POINT, linewidth=1.6, zorder=6)

ax.set_xlim(-1.3, 1.3)
ax.set_ylim(-1.3, 1.3)
ax.set_zlim(-1.5, 1.5)
ax.set_box_aspect((1, 1, 1.15))
ax.view_init(elev=14, azim=-64)
ax.axis("off")

# --------------------------------------------------- right: the resulting map
ax = fig.add_subplot(1, 2, 2)

top = mercator_y(CUTOFF)
for lon in range(-180, 181, 30):
    ax.plot([lon, lon], [-top, top], color=GREY, linewidth=0.5, alpha=0.6)
for lat in (-80, -75, -60, -30, 30, 60, 75, 80):
    y = mercator_y(lat)
    ax.plot([-180, 180], [y, y], color=GREY, linewidth=0.5, alpha=0.6)

ax.plot([-180, 180], [0, 0], color=INK, linewidth=1.2, alpha=0.9)
ax.add_patch(plt.Rectangle((-180, -top), 360, 2 * top, facecolor="none",
                           edgecolor=INK, linewidth=1.3))

# circles that are all the same size on the globe
for lat, lon in CIRCLES:
    scale = 1 / np.cos(np.radians(lat))
    radius = EQUATOR_RADIUS * scale
    y = mercator_y(lat)
    ax.add_patch(plt.Circle((lon, y), radius, facecolor=TEAL, alpha=0.30,
                            edgecolor=TEAL, linewidth=1.4, zorder=4))
    ax.annotate(f"{abs(lat)}°  ×{scale:.1f}", xy=(lon, y - radius),
                xytext=(lon, y - radius - 5), ha="center", va="top",
                fontsize=9.5, color=INK, zorder=5)

ax.set_xlim(-195, 195)
ax.set_ylim(-top - 20, top + 6)
ax.set_aspect("equal")
ax.axis("off")

# both titles placed by hand, so the two panels line up
fig.text(0.26, 0.94, "A cylinder touching at the equator",
         ha="center", fontsize=11.5, color=INK)
fig.text(0.74, 0.94, "…and the map it produces",
         ha="center", fontsize=11.5, color=INK)
fig.text(0.5, 0.075,
         "Every circle is the same size on the globe. It stays a circle – that is the "
         "shape-preserving property Mercator was built for –\nbut its area grows by "
         "1 / cos(latitude), which is why the projection cannot be trusted for size.",
         ha="center", va="top", fontsize=9.5, color=GREY)

fig.subplots_adjust(left=0.01, right=0.99, top=0.90, bottom=0.20, wspace=0.02)
fig.savefig("mercator.png", dpi=170, facecolor="white", bbox_inches="tight")
