"""Generates coordinate_systems.png – the same place, described two ways.

One point in the middle of the Atlantic, at 40° W and 40° N. On the left it is
given in degrees on the globe; on the right, in metres on a flat map. The
projected coordinates are computed with pyproj – the same library GeoPandas
uses under the hood – so the numbers on the figure are real, not illustrative.

Run from this folder:  python coordinate_systems.py
"""

import matplotlib.pyplot as plt
import numpy as np
from pyproj import CRS, Transformer

TEAL = "#03A3A6"
GREY = "#5A5A5A"
INK = "#1A1A1A"
POINT = "#C1443C"

LON, LAT = -40.0, 40.0
PROJECTED = "EPSG:4087"   # WGS 84 / World Equidistant Cylindrical, in metres

transformer = Transformer.from_crs("EPSG:4326", PROJECTED, always_xy=True)
x_m, y_m = transformer.transform(LON, LAT)
projected_name = CRS.from_user_input(PROJECTED).name


def globe_xy(lon, lat, view_lon=-40.0, view_lat=18.0):
    """Orthographic projection – what the globe looks like face on.

    Returns the plotted position and whether the point is on the near side.
    """
    lam, phi = np.radians(lon), np.radians(lat)
    lam0, phi0 = np.radians(view_lon), np.radians(view_lat)
    cos_c = (np.sin(phi0) * np.sin(phi)
             + np.cos(phi0) * np.cos(phi) * np.cos(lam - lam0))
    x = np.cos(phi) * np.sin(lam - lam0)
    y = np.cos(phi0) * np.sin(phi) - np.sin(phi0) * np.cos(phi) * np.cos(lam - lam0)
    return x, y, cos_c >= 0


fig, (left, right) = plt.subplots(1, 2, figsize=(11.0, 4.9))

# ---------------------------------------------------------------- the globe
left.add_patch(plt.Circle((0, 0), 1, facecolor="white",
                          edgecolor=INK, linewidth=1.4, zorder=1))

for lat in range(-80, 81, 20):
    lons = np.linspace(-180, 180, 400)
    gx, gy, visible = globe_xy(lons, np.full_like(lons, float(lat)))
    gx, gy = np.where(visible, gx, np.nan), np.where(visible, gy, np.nan)
    left.plot(gx, gy, color=GREY, linewidth=0.6, alpha=0.6, zorder=2)

for lon in range(-180, 180, 20):
    lats = np.linspace(-90, 90, 400)
    gx, gy, visible = globe_xy(np.full_like(lats, float(lon)), lats)
    gx, gy = np.where(visible, gx, np.nan), np.where(visible, gy, np.nan)
    left.plot(gx, gy, color=GREY, linewidth=0.6, alpha=0.6, zorder=2)

# the equator, heavier, as the origin of latitude
lons = np.linspace(-180, 180, 400)
gx, gy, visible = globe_xy(lons, np.zeros_like(lons))
left.plot(np.where(visible, gx, np.nan), np.where(visible, gy, np.nan),
          color=INK, linewidth=1.2, alpha=0.85, zorder=3)

px, py, _ = globe_xy(LON, LAT)
left.plot([px], [py], "o", color=POINT, markersize=9, zorder=5)
left.annotate(f"{abs(LON):.0f}° W, {LAT:.0f}° N",
              xy=(px, py), xytext=(px - 0.15, py + 0.42),
              fontsize=12, color=POINT, ha="center", fontweight="bold",
              arrowprops=dict(arrowstyle="-", color=POINT, linewidth=1))

left.set_title("Geographic CRS", fontsize=13, color=INK, pad=12)
left.text(0.5, 0.02, "degrees of latitude and longitude\non the ellipsoid",
          transform=left.transAxes, ha="center", va="top",
          fontsize=10, color=GREY)
left.set_xlim(-1.35, 1.35)
left.set_ylim(-1.75, 1.35)

# ------------------------------------------------------------- the flat map
bounds_x, bounds_y = transformer.transform(180, 90)

for lat in range(-80, 81, 20):
    _, gy = transformer.transform(0, lat)
    right.plot([-bounds_x, bounds_x], [gy, gy],
               color=GREY, linewidth=0.6, alpha=0.6, zorder=2)

for lon in range(-180, 181, 20):
    gx, _ = transformer.transform(lon, 0)
    right.plot([gx, gx], [-bounds_y, bounds_y],
               color=GREY, linewidth=0.6, alpha=0.6, zorder=2)

right.add_patch(plt.Rectangle((-bounds_x, -bounds_y), 2 * bounds_x, 2 * bounds_y,
                              facecolor="none", edgecolor=INK,
                              linewidth=1.4, zorder=3))
right.plot([-bounds_x, bounds_x], [0, 0], color=INK,
           linewidth=1.2, alpha=0.85, zorder=3)
right.plot([0, 0], [-bounds_y, bounds_y], color=INK,
           linewidth=1.2, alpha=0.85, zorder=3)

right.plot([x_m], [y_m], "o", color=POINT, markersize=9, zorder=5)
right.annotate(f"x = {x_m:,.0f} m\ny = {y_m:,.0f} m".replace(",", " "),
               xy=(x_m, y_m), xytext=(x_m - 1.1e6, y_m + 6.2e6),
               fontsize=12, color=POINT, ha="center", fontweight="bold",
               arrowprops=dict(arrowstyle="-", color=POINT, linewidth=1))

# the origin the metres are counted from
right.plot([0], [0], "o", color=INK, markersize=4, zorder=5)
right.annotate("origin (0, 0)", xy=(0, 0), xytext=(3.1e6, -6.4e6),
               fontsize=9, color=INK, ha="left", va="center",
               arrowprops=dict(arrowstyle="-", color=INK, linewidth=0.8))

right.set_title("Projected CRS", fontsize=13, color=INK, pad=12)
right.text(0.5, 0.02,
           f"metres on the map plane\n{projected_name} ({PROJECTED})",
           transform=right.transAxes, ha="center", va="top",
           fontsize=10, color=GREY)
right.set_xlim(-bounds_x * 1.06, bounds_x * 1.06)
right.set_ylim(-bounds_y * 3.05, bounds_y * 2.35)

for ax in (left, right):
    ax.set_aspect("equal")
    ax.axis("off")

fig.subplots_adjust(left=0.02, right=0.98, top=0.94, bottom=0.02, wspace=0.05)
fig.savefig("coordinate_systems.png", dpi=170, facecolor="white",
            bbox_inches="tight")
