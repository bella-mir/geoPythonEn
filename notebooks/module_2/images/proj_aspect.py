"""Generates proj_aspect.png – the orientation of the developable surface.

The same cylinder wrapped around the same globe three ways: aligned with the
Earth's axis (normal), turned 90 degrees to it (transverse), and set at an
arbitrary angle (oblique). Where the surface touches the globe is where the
map will be least distorted, which is the whole point of choosing an aspect.

Run from this folder:  python proj_aspect.py
"""

import matplotlib.pyplot as plt
import numpy as np

TEAL = "#03A3A6"
TEAL_LIGHT = "#9BD7D8"
GREY = "#5A5A5A"
INK = "#1A1A1A"
AXIS_RED = "#C1443C"

R = 1.0            # globe radius
CYL_HALF = 1.45    # half-height of the cylinder
LINE_OF_CONTACT = 90  # samples along the tangent circle


def rotation(tilt_degrees):
    """Rotate about the y axis, so the cylinder leans in the xz plane."""
    t = np.radians(tilt_degrees)
    return np.array([[np.cos(t), 0, np.sin(t)],
                     [0, 1, 0],
                     [-np.sin(t), 0, np.cos(t)]])


def apply(matrix, x, y, z):
    """Rotate a grid of points, keeping its shape."""
    stacked = np.stack([x.ravel(), y.ravel(), z.ravel()])
    out = matrix @ stacked
    return (out[0].reshape(x.shape),
            out[1].reshape(x.shape),
            out[2].reshape(x.shape))


def draw_globe(ax):
    """A wireframe globe: parallels every 20 degrees, meridians every 20."""
    angle = np.linspace(0, 2 * np.pi, 120)

    for lat in range(-80, 81, 20):
        phi = np.radians(lat)
        r = R * np.cos(phi)
        ax.plot(r * np.cos(angle), r * np.sin(angle),
                np.full_like(angle, R * np.sin(phi)),
                color=GREY, linewidth=0.5, alpha=0.55)

    theta = np.linspace(-np.pi / 2, np.pi / 2, 90)
    for lon in range(0, 360, 20):
        lam = np.radians(lon)
        ax.plot(R * np.cos(theta) * np.cos(lam),
                R * np.cos(theta) * np.sin(lam),
                R * np.sin(theta),
                color=GREY, linewidth=0.5, alpha=0.55)

    # the equator, drawn heavier so the Earth's own orientation stays readable
    ax.plot(R * np.cos(angle), R * np.sin(angle), np.zeros_like(angle),
            color=INK, linewidth=1.2, alpha=0.85)


def draw_axis(ax):
    """The Earth's axis of rotation – the thing an aspect is measured against."""
    ax.plot([0, 0], [0, 0], [-1.42 * R, 1.42 * R],
            color=AXIS_RED, linewidth=1.6, zorder=6)
    ax.text(0, 0, 1.55 * R, "N", color=AXIS_RED, fontsize=10,
            ha="center", va="bottom")


def draw_cylinder(ax, tilt_degrees):
    """A cylinder tangent to the globe, tilted off the polar axis."""
    matrix = rotation(tilt_degrees)

    angle = np.linspace(0, 2 * np.pi, 80)
    height = np.linspace(-CYL_HALF, CYL_HALF, 2)
    grid_angle, grid_height = np.meshgrid(angle, height)

    x = R * np.cos(grid_angle)
    y = R * np.sin(grid_angle)
    z = grid_height
    x, y, z = apply(matrix, x, y, z)
    ax.plot_surface(x, y, z, color=TEAL_LIGHT, alpha=0.28,
                    linewidth=0, shade=False, zorder=2)

    # the rims, so the cylinder reads as a solid rather than a haze
    for end in (-CYL_HALF, CYL_HALF):
        rim = np.stack([R * np.cos(angle), R * np.sin(angle),
                        np.full_like(angle, end)])
        rim = matrix @ rim
        ax.plot(rim[0], rim[1], rim[2], color=TEAL, linewidth=1.1, alpha=0.8)

    # the line of contact: where the cylinder touches the globe
    contact_angle = np.linspace(0, 2 * np.pi, LINE_OF_CONTACT)
    contact = np.stack([R * np.cos(contact_angle), R * np.sin(contact_angle),
                        np.zeros_like(contact_angle)])
    contact = matrix @ contact
    ax.plot(contact[0], contact[1], contact[2],
            color=TEAL, linewidth=2.6, zorder=7)


ASPECTS = [
    ("Normal", 0, "surface axis along the Earth's axis"),
    ("Transverse", 90, "surface axis turned 90° to it"),
    ("Oblique", 40, "surface axis at an arbitrary angle"),
]

fig = plt.figure(figsize=(11.4, 4.4))

for position, (name, tilt, note) in enumerate(ASPECTS, start=1):
    ax = fig.add_subplot(1, 3, position, projection="3d")
    draw_globe(ax)
    draw_cylinder(ax, tilt)
    draw_axis(ax)

    ax.set_title(name, fontsize=12, color=INK, pad=2)
    ax.text2D(0.5, -0.02, note, transform=ax.transAxes, fontsize=9,
              color=GREY, ha="center")

    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_zlim(-1.5, 1.5)
    ax.set_box_aspect((1, 1, 1.15))
    ax.view_init(elev=14, azim=-64)
    ax.axis("off")

fig.text(0.5, 0.045,
         "The heavy teal line is where the surface touches the globe – "
         "the line along which the map is least distorted.",
         ha="center", fontsize=9.5, color=GREY)

fig.subplots_adjust(left=0.01, right=0.99, top=1.0, bottom=0.1, wspace=0.0)
fig.savefig("proj_aspect.png", dpi=170, facecolor="white", bbox_inches="tight")
