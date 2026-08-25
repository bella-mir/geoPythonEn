"""Generates webmercator_tiles.png — why the Web Mercator world is a square.

Cutting the map off at ±85.05° of latitude makes its extent identical in x and
y, so the world divides into an exact quadtree of tiles: 1, then 4, then 16.

Run from this folder:  python webmercator_tiles.py
"""

import math

import matplotlib.pyplot as plt

TEAL = "#03A3A6"
TEAL_LIGHT = "#9BD7D8"
GREY = "#5A5A5A"
INK = "#1A1A1A"

CUTOFF = 85.0511287798066   # the latitude at which y equals half the equator
EXTENT = 20037508.342789244  # metres from the centre to the edge, x and y alike


def mercator_y(lat_degrees):
    """Web Mercator northing, scaled so that the world spans -1 to 1."""
    lat = math.radians(lat_degrees)
    return math.log(math.tan(math.pi / 4 + lat / 2)) / math.pi


def mercator_x(lon_degrees):
    return lon_degrees / 180


fig, axes = plt.subplots(1, 3, figsize=(11.4, 4.3))

for zoom, ax in enumerate(axes):
    tiles = 2 ** zoom
    ax.add_patch(plt.Rectangle((-1, -1), 2, 2, facecolor="white",
                               edgecolor=INK, linewidth=1.4, zorder=1))
    # one tile shaded, so that "a tile" is a thing you can point at
    ax.add_patch(plt.Rectangle((-1, 1 - 2 / tiles), 2 / tiles, 2 / tiles,
                               facecolor=TEAL_LIGHT, alpha=0.65, zorder=1.5,
                               edgecolor="none"))

    # graticule: meridians every 30 degrees, parallels every 15
    for lon in range(-150, 180, 30):
        ax.plot([mercator_x(lon)] * 2, [-1, 1], color=GREY,
                linewidth=0.5, alpha=0.5, zorder=2)
    for lat in range(-75, 90, 15):
        y = mercator_y(lat)
        ax.plot([-1, 1], [y, y], color=GREY, linewidth=0.5, alpha=0.5, zorder=2)
    ax.plot([-1, 1], [0, 0], color=GREY, linewidth=1.1, alpha=0.9, zorder=3)

    # the tile grid for this zoom level
    for i in range(1, tiles):
        edge = -1 + 2 * i / tiles
        ax.plot([edge] * 2, [-1, 1], color=TEAL, linewidth=2, zorder=4)
        ax.plot([-1, 1], [edge] * 2, color=TEAL, linewidth=2, zorder=4)

    ax.set_title(f"zoom {zoom} — {tiles ** 2} tile{'s' if tiles > 1 else ''}",
                 fontsize=11, color=INK, pad=10)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect("equal")
    ax.axis("off")

# the cutoff is what makes the extent square, so it is labelled once
axes[0].text(0, 1.09, f"{CUTOFF:.2f}° N", ha="center", va="bottom",
             fontsize=9, color=TEAL)
axes[0].text(0, -1.09, f"{CUTOFF:.2f}° S", ha="center", va="top",
             fontsize=9, color=TEAL)
axes[0].text(-1.1, 0, "equator", ha="right", va="center",
             fontsize=8.5, color=GREY)

fig.tight_layout(pad=1.0)
fig.savefig("webmercator_tiles.png", dpi=180, facecolor="white",
            bbox_inches="tight")
