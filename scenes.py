"""
Matplotlib 1080p animation scene renderers for:
"Derivative and Rate of Change: From Secant Slope to Tangent Slope"

Each render_* function yields `num_frames` RGB byte buffers (1920x1080x3)
synchronized to the exact duration of its narration audio.
"""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

from config import (
    ACCENT_AMBER,
    ACCENT_BLUE,
    ACCENT_GREEN,
    ACCENT_PINK,
    ACCENT_RED,
    BG_COLOR,
    CARD_BG,
    COURSE_NAME,
    DPI,
    FIGSIZE,
    GRID_COLOR,
    LEARNING_OBJECTIVE,
    STUDENT_ID,
    STUDENT_NAME,
    TEXT_MUTED,
    TEXT_PRIMARY,
    VIDEO_SUBTITLE,
    VIDEO_TITLE,
)

# Configure crisp matplotlib typography
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
        "axes.edgecolor": GRID_COLOR,
        "axes.linewidth": 1.2,
    }
)


def ease_in_out(t: float) -> float:
    """Smooth cubic ease-in-out for t in [0, 1]."""
    t = max(0.0, min(1.0, t))
    return 3 * t * t - 2 * t * t * t


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def new_figure():
    """Create a 1920x1080 figure with a full-bleed dark slate canvas."""
    fig = plt.figure(figsize=FIGSIZE, dpi=DPI, facecolor=BG_COLOR)
    ax = fig.add_axes([0, 0, 1, 1], facecolor=BG_COLOR)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")
    return fig, ax


def fig_to_rgb_bytes(fig) -> bytes:
    """Render matplotlib figure to raw RGB24 bytes (1920x1080x3)."""
    fig.canvas.draw()
    rgba = np.asarray(fig.canvas.buffer_rgba())
    return rgba[:, :, :3].tobytes()


def draw_header(ax, scene_tag: str, title: str):
    """Consistent top header bar across scenes."""
    ax.text(
        0.7,
        8.45,
        scene_tag.upper(),
        color=ACCENT_BLUE,
        fontsize=13,
        fontweight="bold",
        va="center",
    )
    ax.text(
        0.7,
        8.0,
        title,
        color=TEXT_PRIMARY,
        fontsize=24,
        fontweight="bold",
        va="center",
    )
    ax.plot([0.7, 15.3], [7.62, 7.62], color=GRID_COLOR, lw=1.2)


def draw_card(ax, x, y, w, h, edge=GRID_COLOR, lw=1.5, alpha=1.0):
    """Draw a rounded card container."""
    box = patches.FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.08,rounding_size=0.18",
        facecolor=CARD_BG,
        edgecolor=edge,
        linewidth=lw,
        alpha=alpha,
    )
    ax.add_patch(box)
    return box


# ---------------------------------------------------------------------------
# Segment 0: Opening Frame
# ---------------------------------------------------------------------------
def render_opening(num_frames: int):
    for i in range(num_frames):
        p = i / max(1, num_frames - 1)
        fade = ease_in_out(clamp01(p * 3.0))

        fig, ax = new_figure()
        # Decorative subtle parabola in background
        xs = np.linspace(1, 15, 200)
        ys = 0.08 * (xs - 8) ** 2 + 1.2
        ax.plot(xs, ys, color=ACCENT_BLUE, alpha=0.14 * fade, lw=3)

        # Tangent line decoration
        tx = np.linspace(4, 14, 100)
        ty = 0.08 * 4 * (tx - 10) + 1.2 + 0.08 * 4
        ax.plot(tx, ty, color=ACCENT_GREEN, alpha=0.18 * fade, lw=2, ls="--")

        ax.text(
            8.0,
            6.5,
            COURSE_NAME,
            color=ACCENT_BLUE,
            fontsize=16,
            fontweight="bold",
            ha="center",
            alpha=fade,
        )
        ax.text(
            8.0,
            5.3,
            VIDEO_TITLE,
            color=TEXT_PRIMARY,
            fontsize=42,
            fontweight="bold",
            ha="center",
            alpha=fade,
        )
        ax.text(
            8.0,
            4.45,
            VIDEO_SUBTITLE,
            color=ACCENT_AMBER,
            fontsize=24,
            ha="center",
            alpha=fade,
        )

        draw_card(ax, 4.5, 2.0, 7.0, 1.35, edge=ACCENT_BLUE, alpha=fade)
        ax.text(
            8.0,
            2.85,
            f"Presented by: {STUDENT_NAME}",
            color=TEXT_PRIMARY,
            fontsize=18,
            fontweight="bold",
            ha="center",
            alpha=fade,
        )
        ax.text(
            8.0,
            2.32,
            f"Student ID: {STUDENT_ID}",
            color=TEXT_MUTED,
            fontsize=15,
            ha="center",
            alpha=fade,
        )

        yield fig_to_rgb_bytes(fig)
        plt.close(fig)


# ---------------------------------------------------------------------------
# Segment 1: Hook / Context (Moving Car Analogy)
# ---------------------------------------------------------------------------
def render_hook(num_frames: int):
    for i in range(num_frames):
        p = i / max(1, num_frames - 1)
        fig, ax = new_figure()
        draw_header(ax, "Scene 1 • Hook & Context", "How Fast Are You Moving Right Now?")

        # Road visualization at top
        draw_card(ax, 0.7, 4.9, 14.6, 2.3, edge=GRID_COLOR)
        ax.text(1.1, 6.75, r"Distance traveled:  $s(t) = t^2$  (meters)", color=TEXT_PRIMARY, fontsize=18, fontweight="bold")

        # Road line
        ax.plot([1.3, 14.7], [5.45, 5.45], color=TEXT_MUTED, lw=4)
        for mark_t, mx in [(0, 1.5), (2, 4.8), (4, 14.0)]:
            ax.plot([mx, mx], [5.3, 5.6], color=TEXT_PRIMARY, lw=2)
            ax.text(mx, 5.05, f"t = {mark_t}s\n({mark_t**2} m)", color=TEXT_MUTED, fontsize=12, ha="center", va="top")

        # Animated car moving from t=0 to t=4
        car_t = 4.0 * ease_in_out(clamp01(p * 1.15))
        car_x = 1.5 + (car_t ** 2 / 16.0) * (14.0 - 1.5)
        car = patches.FancyBboxPatch(
            (car_x - 0.35, 5.55), 0.7, 0.36,
            boxstyle="round,pad=0.03,rounding_size=0.08",
            facecolor=ACCENT_AMBER, edgecolor=TEXT_PRIMARY, lw=1.5
        )
        ax.add_patch(car)
        ax.text(car_x, 6.12, f"t = {car_t:.1f}s", color=ACCENT_AMBER, fontsize=13, fontweight="bold", ha="center")

        # Left card: Average Speed (appears after p > 0.25)
        a1 = ease_in_out(clamp01((p - 0.22) * 5))
        if a1 > 0.01:
            draw_card(ax, 0.7, 1.0, 6.9, 3.4, edge=ACCENT_AMBER, alpha=a1)
            ax.text(1.1, 3.9, "Average Speed (t = 2s to t = 4s)", color=ACCENT_AMBER, fontsize=17, fontweight="bold", alpha=a1)
            ax.text(
                1.1, 3.1,
                r"$\mathrm{Average\ Speed} = \frac{s(4) - s(2)}{4 - 2} = \frac{16 - 4}{2} = 6\ \mathrm{m/s}$",
                color=TEXT_PRIMARY, fontsize=17, alpha=a1,
            )
            ax.text(
                1.1, 2.0,
                "Uses TWO different moments in time.\nEasy to compute, but only an average!",
                color=TEXT_MUTED, fontsize=14, alpha=a1,
            )

        # Right card: Instantaneous Speed question (appears after p > 0.55)
        a2 = ease_in_out(clamp01((p - 0.55) * 5))
        if a2 > 0.01:
            draw_card(ax, 8.2, 1.0, 7.1, 3.4, edge=ACCENT_GREEN, alpha=a2)
            ax.text(8.6, 3.9, "Instantaneous Speed at t = 2s?", color=ACCENT_GREEN, fontsize=17, fontweight="bold", alpha=a2)
            ax.text(
                8.6, 3.0,
                "What does the speedometer read\nat the EXACT instant  t = 2s ?",
                color=TEXT_PRIMARY, fontsize=16, alpha=a2,
            )
            ax.text(
                8.6, 1.85,
                r"If $\Delta t = 0$,  $\frac{0}{0}$ is undefined!"
                "\nWe need a way to approach  t = 2s  smoothly.",
                color=ACCENT_PINK, fontsize=14, fontweight="bold", alpha=a2,
            )

        yield fig_to_rgb_bytes(fig)
        plt.close(fig)


# ---------------------------------------------------------------------------
# Segment 2: Concept Introduction
# ---------------------------------------------------------------------------
def render_concept(num_frames: int):
    for i in range(num_frames):
        p = i / max(1, num_frames - 1)
        fig, ax = new_figure()
        draw_header(ax, "Scene 2 • Concept Introduction", "Defining Secant Slope & The Derivative")

        # Learning Objective Banner
        a0 = ease_in_out(clamp01(p * 6))
        draw_card(ax, 0.7, 6.05, 14.6, 1.25, edge=ACCENT_BLUE, alpha=a0)
        ax.text(1.0, 6.92, "LEARNING OBJECTIVE", color=ACCENT_BLUE, fontsize=12, fontweight="bold", alpha=a0)
        ax.text(1.0, 6.40, LEARNING_OBJECTIVE, color=TEXT_PRIMARY, fontsize=13.5, alpha=a0)

        # Card 1: Average Rate of Change (Secant Slope)
        a1 = ease_in_out(clamp01((p - 0.25) * 5))
        if a1 > 0.01:
            draw_card(ax, 0.7, 1.2, 7.0, 4.4, edge=ACCENT_AMBER, alpha=a1)
            ax.text(1.1, 5.05, "1. Average Rate of Change", color=ACCENT_AMBER, fontsize=19, fontweight="bold", alpha=a1)
            ax.text(1.1, 4.5, "Notation:  x = starting input,   h = non-zero step", color=TEXT_MUTED, fontsize=13.5, alpha=a1)
            ax.text(
                4.2, 3.35,
                r"$m_{\mathrm{sec}} = \frac{f(x + h) - f(x)}{h}$",
                color=TEXT_PRIMARY, fontsize=24, ha="center", alpha=a1,
            )
            ax.text(
                1.1, 2.0,
                "• Measures change over an interval [x, x + h]\n"
                "• Geometrically: slope of the SECANT line\n"
                "  connecting (x, f(x)) and (x + h, f(x + h))",
                color=TEXT_PRIMARY, fontsize=14, linespacing=1.55, alpha=a1,
            )

        # Card 2: Instantaneous Rate of Change (Derivative)
        a2 = ease_in_out(clamp01((p - 0.55) * 5))
        if a2 > 0.01:
            draw_card(ax, 8.3, 1.2, 7.0, 4.4, edge=ACCENT_GREEN, alpha=a2)
            ax.text(8.7, 5.05, "2. Instantaneous Rate (Derivative)", color=ACCENT_GREEN, fontsize=19, fontweight="bold", alpha=a2)
            ax.text(8.7, 4.5, "Shrink step size  h  closer and closer to 0:", color=TEXT_MUTED, fontsize=13.5, alpha=a2)
            ax.text(
                11.8, 3.35,
                r"$f'(x) = \lim_{h \to 0} \frac{f(x + h) - f(x)}{h}$",
                color=TEXT_PRIMARY, fontsize=24, ha="center", alpha=a2,
            )
            ax.text(
                8.7, 2.0,
                "• Measures exact rate of change AT input x\n"
                "• Geometrically: slope of the TANGENT line\n"
                "  touching the curve at the single point (x, f(x))",
                color=TEXT_PRIMARY, fontsize=14, linespacing=1.55, alpha=a2,
            )

        yield fig_to_rgb_bytes(fig)
        plt.close(fig)


# ---------------------------------------------------------------------------
# Segment 3: Visual Intuition (Secant -> Tangent Animation on f(x) = x^2)
# ---------------------------------------------------------------------------
def render_intuition(num_frames: int):
    # Keyframes for h: stays at 2.0, then shrinks smoothly to 1.0, 0.5, 0.1, 0.005
    h_waypoints = [
        (0.00, 2.0),
        (0.28, 2.0),
        (0.45, 1.0),
        (0.62, 0.5),
        (0.78, 0.1),
        (0.92, 0.002),
        (1.00, 0.002),
    ]

    def interp_h(p: float) -> float:
        for idx in range(len(h_waypoints) - 1):
            t0, h0 = h_waypoints[idx]
            t1, h1 = h_waypoints[idx + 1]
            if t0 <= p <= t1:
                local = ease_in_out((p - t0) / max(1e-6, t1 - t0))
                return h0 + (h1 - h0) * local
        return 0.002

    for i in range(num_frames):
        p = i / max(1, num_frames - 1)
        h = interp_h(p)
        x0, y0 = 2.0, 4.0
        x1 = x0 + h
        y1 = x1 ** 2
        slope = (y1 - y0) / h  # = 4 + h

        fig = plt.figure(figsize=FIGSIZE, dpi=DPI, facecolor=BG_COLOR)
        # Background header axis
        bg = fig.add_axes([0, 0, 1, 1], facecolor=BG_COLOR)
        bg.set_xlim(0, 16)
        bg.set_ylim(0, 9)
        bg.axis("off")
        draw_header(bg, "Scene 3 • Visual Intuition", r"Shrinking $h \to 0$ on $f(x) = x^2$ at $P(2, 4)$")

        # Left Plot Axis
        ax = fig.add_axes([0.07, 0.10, 0.54, 0.72], facecolor=CARD_BG)
        ax.set_xlim(0, 4.6)
        ax.set_ylim(0, 18.5)
        ax.grid(True, color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.6)
        ax.tick_params(colors=TEXT_MUTED, labelsize=12)
        ax.set_xlabel("x", color=TEXT_PRIMARY, fontsize=14, fontweight="bold")
        ax.set_ylabel("f(x)", color=TEXT_PRIMARY, fontsize=14, fontweight="bold")

        # Curve f(x) = x^2
        xs = np.linspace(0, 4.5, 300)
        ax.plot(xs, xs ** 2, color=ACCENT_BLUE, lw=3.2, label=r"$f(x) = x^2$")

        # Target tangent line y = 4x - 4 (fades in strongly as h -> 0)
        tan_alpha = 0.25 + 0.75 * clamp01((0.4 - h) / 0.4)
        tx = np.linspace(0.5, 4.5, 100)
        ax.plot(tx, 4 * tx - 4, color=ACCENT_GREEN, lw=2.8, ls="--" if h > 0.05 else "-", alpha=tan_alpha, label="Tangent line (slope = 4)")

        # Secant line through P and Q
        sx = np.linspace(0.2, 4.5, 100)
        sy = y0 + slope * (sx - x0)
        ax.plot(sx, sy, color=ACCENT_AMBER, lw=2.8, label=f"Secant line (slope = {slope:.2f})")

        # Rise/Run triangle if h > 0.08
        if h > 0.08:
            ax.plot([x0, x1], [y0, y0], color=TEXT_PRIMARY, lw=1.6, ls=":")
            ax.plot([x1, x1], [y0, y1], color=TEXT_PRIMARY, lw=1.6, ls=":")
            ax.text((x0 + x1) / 2, y0 - 0.85, f"h = {h:.2f}", color=TEXT_PRIMARY, fontsize=11, ha="center")
            ax.text(x1 + 0.08, (y0 + y1) / 2, rf"$\Delta y$ = {y1-y0:.2f}", color=TEXT_PRIMARY, fontsize=11, va="center")

        # Points P and Q
        ax.scatter([x0], [y0], color=ACCENT_PINK, s=110, zorder=5)
        ax.text(x0 - 0.35, y0 + 0.6, "P(2, 4)", color=ACCENT_PINK, fontsize=13, fontweight="bold")

        if h > 0.02:
            ax.scatter([x1], [y1], color=ACCENT_AMBER, s=110, zorder=5)
            ax.text(max(0.2, x1 - 0.45), min(17.5, y1 + 0.7), f"Q({x1:.2f}, {y1:.2f})", color=ACCENT_AMBER, fontsize=12, fontweight="bold")

        ax.legend(loc="upper left", facecolor=BG_COLOR, edgecolor=GRID_COLOR, labelcolor=TEXT_PRIMARY, fontsize=11.5)

        # Right Readout Panel
        draw_card(bg, 10.2, 1.0, 5.1, 6.2, edge=ACCENT_AMBER if h > 0.05 else ACCENT_GREEN)
        bg.text(10.55, 6.65, "LIVE SLOPE TRACKER", color=ACCENT_BLUE, fontsize=14, fontweight="bold")

        bg.text(10.55, 5.8, "Step size  h:", color=TEXT_MUTED, fontsize=15)
        bg.text(14.9, 5.8, f"{h:.3f}" if h < 0.05 else f"{h:.2f}", color=ACCENT_AMBER, fontsize=22, fontweight="bold", ha="right")

        bg.text(10.55, 4.9, "Point Q:", color=TEXT_MUTED, fontsize=15)
        bg.text(14.9, 4.9, f"({x1:.2f}, {y1:.2f})", color=TEXT_PRIMARY, fontsize=18, fontweight="bold", ha="right")

        bg.text(10.55, 3.9, "Secant Slope:", color=TEXT_MUTED, fontsize=15)
        bg.text(
            12.75,
            3.15,
            rf"$\frac{{f(2+h)-f(2)}}{{h}} = {slope:.3f}$" if h < 0.05 else rf"$\frac{{f(2+h)-f(2)}}{{h}} = {slope:.2f}$",
            color=ACCENT_GREEN if h <= 0.05 else ACCENT_AMBER,
            fontsize=21,
            ha="center",
        )

        status = (
            "Q has merged into P!\nThe secant line IS the\ntangent line with slope 4."
            if h <= 0.05
            else "As h shrinks toward 0,\nQ slides down the curve\ntoward P(2, 4)."
        )
        bg.text(10.55, 1.75, status, color=TEXT_PRIMARY, fontsize=14, linespacing=1.45)

        yield fig_to_rgb_bytes(fig)
        plt.close(fig)


# ---------------------------------------------------------------------------
# Segment 4: Worked Example (Table + Step-by-Step Algebra)
# ---------------------------------------------------------------------------
def render_example(num_frames: int):
    rows = [
        ("2.0", "4.0", "16.00", "6.00"),
        ("1.0", "3.0", "9.00", "5.00"),
        ("0.5", "2.5", "6.25", "4.50"),
        ("0.1", "2.1", "4.41", "4.10"),
        ("0.01", "2.01", "4.0401", "4.01"),
    ]
    algebra_steps = [
        (0.18, r"$f'(2) = \lim_{h \to 0} \frac{f(2+h) - f(2)}{h}$", TEXT_PRIMARY),
        (0.32, r"$= \lim_{h \to 0} \frac{(2+h)^2 - 4}{h}$", TEXT_PRIMARY),
        (0.46, r"$= \lim_{h \to 0} \frac{(4 + 4h + h^2) - 4}{h}$", ACCENT_BLUE),
        (0.60, r"$= \lim_{h \to 0} \frac{4h + h^2}{h} = \lim_{h \to 0} \frac{h(4 + h)}{h}$", ACCENT_AMBER),
        (0.75, r"$= \lim_{h \to 0} (4 + h) \quad (h \neq 0)$", ACCENT_AMBER),
        (0.86, r"$= 4 + 0 = 4$", ACCENT_GREEN),
    ]

    for i in range(num_frames):
        p = i / max(1, num_frames - 1)
        fig, ax = new_figure()
        draw_header(ax, "Scene 4 • Worked Example", r"Computing $f'(2)$ for $f(x) = x^2$")

        # Left Card: Numerical Table
        draw_card(ax, 0.7, 1.0, 6.2, 6.2, edge=ACCENT_BLUE)
        ax.text(1.05, 6.72, "Numerical Evidence (h → 0)", color=ACCENT_BLUE, fontsize=17, fontweight="bold")

        headers = ["h", "2 + h", "f(2+h)", "Slope"]
        col_x = [1.15, 2.4, 3.85, 5.45]
        for cx, htext in zip(col_x, headers):
            ax.text(cx, 6.05, htext, color=TEXT_MUTED, fontsize=13.5, fontweight="bold")
        ax.plot([1.0, 6.6], [5.8, 5.8], color=GRID_COLOR, lw=1.2)

        for idx, row in enumerate(rows):
            reveal = ease_in_out(clamp01((p - 0.04 * idx) * 6))
            if reveal > 0.01:
                ry = 5.25 - idx * 0.72
                for cx, val in zip(col_x, row):
                    color = ACCENT_AMBER if cx == col_x[-1] else TEXT_PRIMARY
                    ax.text(cx, ry, val, color=color, fontsize=14, fontweight="bold" if cx == col_x[-1] else "normal", alpha=reveal)

        a_lim = ease_in_out(clamp01((p - 0.25) * 5))
        if a_lim > 0.01:
            ax.text(1.1, 1.45, "Slopes approach 4.000...", color=ACCENT_GREEN, fontsize=15, fontweight="bold", alpha=a_lim)

        # Right Card: Algebraic Derivation
        draw_card(ax, 7.3, 1.0, 8.0, 6.2, edge=ACCENT_GREEN)
        ax.text(7.65, 6.72, "Exact Algebraic Derivation", color=ACCENT_GREEN, fontsize=17, fontweight="bold")

        for idx, (thresh, expr, color) in enumerate(algebra_steps):
            alpha = ease_in_out(clamp01((p - thresh) * 7))
            if alpha > 0.01:
                sy = 5.85 - idx * 0.85
                ax.text(7.7, sy, expr, color=color, fontsize=19 if idx < 5 else 23, fontweight="bold" if idx == 5 else "normal", alpha=alpha)

        yield fig_to_rgb_bytes(fig)
        plt.close(fig)


# ---------------------------------------------------------------------------
# Segment 5: Interpretation (Local Linearity + Tangent Equation + Speed)
# ---------------------------------------------------------------------------
def render_interpretation(num_frames: int):
    for i in range(num_frames):
        p = i / max(1, num_frames - 1)
        # Zoom factor smoothly zooms in on (2, 4)
        zoom = 1.0 + 5.5 * ease_in_out(clamp01((p - 0.15) / 0.55))
        half_w = 2.0 / zoom
        half_h = 8.0 / zoom

        fig = plt.figure(figsize=FIGSIZE, dpi=DPI, facecolor=BG_COLOR)
        bg = fig.add_axes([0, 0, 1, 1], facecolor=BG_COLOR)
        bg.set_xlim(0, 16)
        bg.set_ylim(0, 9)
        bg.axis("off")
        draw_header(bg, "Scene 5 • Interpretation", r"What Does $f'(2) = 4$ Mean?")

        # Left Zooming Plot
        ax = fig.add_axes([0.07, 0.12, 0.48, 0.68], facecolor=CARD_BG)
        ax.set_xlim(2.0 - half_w, 2.0 + half_w)
        ax.set_ylim(4.0 - half_h, 4.0 + half_h)
        ax.grid(True, color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.6)
        ax.tick_params(colors=TEXT_MUTED, labelsize=11)
        ax.set_title(f"Local Linearity (Zoom: {zoom:.1f}x)", color=ACCENT_BLUE, fontsize=14, fontweight="bold")

        xs = np.linspace(2.0 - half_w, 2.0 + half_w, 300)
        ax.plot(xs, xs ** 2, color=ACCENT_BLUE, lw=3.2, label=r"$f(x) = x^2$")
        ax.plot(xs, 4 * xs - 4, color=ACCENT_GREEN, lw=2.6, ls="--", label="Tangent: y = 4x - 4")
        ax.scatter([2.0], [4.0], color=ACCENT_PINK, s=110, zorder=5)
        ax.legend(loc="upper left", facecolor=BG_COLOR, edgecolor=GRID_COLOR, labelcolor=TEXT_PRIMARY, fontsize=11)

        # Right Cards: Geometric & Physical meaning
        draw_card(bg, 9.2, 4.25, 6.1, 2.95, edge=ACCENT_GREEN)
        bg.text(9.55, 6.72, "Geometric Meaning", color=ACCENT_GREEN, fontsize=18, fontweight="bold")
        bg.text(
            9.55,
            5.35,
            "• Tangent line at (2, 4) has slope 4:\n"
            r"  $y - 4 = 4(x - 2) \Rightarrow y = 4x - 4$"
            "\n• Local Linearity: Zooming in makes\n  the curve look straight with slope 4.",
            color=TEXT_PRIMARY,
            fontsize=14,
            linespacing=1.55,
            va="center",
        )

        a_phys = ease_in_out(clamp01((p - 0.55) * 5))
        if a_phys > 0.01:
            draw_card(bg, 9.2, 1.05, 6.1, 2.8, edge=ACCENT_AMBER, alpha=a_phys)
            bg.text(9.55, 3.35, "Physical Meaning (Our Car)", color=ACCENT_AMBER, fontsize=18, fontweight="bold", alpha=a_phys)
            bg.text(
                9.55,
                2.15,
                r"• For $s(t) = t^2$,  $s'(2) = 4\ \mathrm{m/s}$."
                "\n• At the exact instant t = 2s,\n  the speedometer reads 4 m/s!",
                color=TEXT_PRIMARY,
                fontsize=14.5,
                linespacing=1.55,
                va="center",
                alpha=a_phys,
            )

        yield fig_to_rgb_bytes(fig)
        plt.close(fig)


# ---------------------------------------------------------------------------
# Segment 6: Summary & Credits
# ---------------------------------------------------------------------------
def render_summary(num_frames: int):
    for i in range(num_frames):
        p = i / max(1, num_frames - 1)
        fade = ease_in_out(clamp01(p * 4.0))

        fig, ax = new_figure()
        draw_header(ax, "Scene 6 • Summary & Credits", "3 Core Takeaways")

        takeaways = [
            ("1. Secant Slope = Average Rate", r"$\frac{f(x+h)-f(x)}{h}$ measures average change across two points.", ACCENT_AMBER),
            ("2. Shrinking h → Tangent Line", r"As $h \to 0$, the secant line rotates into the unique tangent line.", ACCENT_BLUE),
            ("3. Limit = Instantaneous Rate", r"Simplifying before taking $\lim_{h \to 0}$ gives the exact derivative $f'(x)$.", ACCENT_GREEN),
        ]

        for idx, (head, desc, col) in enumerate(takeaways):
            y_pos = 5.65 - idx * 1.45
            draw_card(ax, 0.7, y_pos, 8.6, 1.2, edge=col, alpha=fade)
            ax.text(1.0, y_pos + 0.78, head, color=col, fontsize=16, fontweight="bold", alpha=fade)
            ax.text(1.0, y_pos + 0.30, desc, color=TEXT_PRIMARY, fontsize=13.5, alpha=fade)

        # Credits & AI Disclosure Card
        draw_card(ax, 9.7, 2.75, 5.6, 4.1, edge=GRID_COLOR, alpha=fade)
        ax.text(10.0, 6.35, "Credits & AI Disclosure", color=ACCENT_PINK, fontsize=17, fontweight="bold", alpha=fade)
        ax.text(
            10.0,
            4.55,
            f"Author: {STUDENT_NAME}\n"
            f"Student ID: {STUDENT_ID}\n\n"
            "References:\n"
            "• M3 Calculus Lecture Notes\n"
            "• Stewart, Calculus: Early Transcendentals\n\n"
            "AI Tools Disclosure:\n"
            "• AI assistance used for Python/Matplotlib\n"
            "  animation scripting & edge-tts voice-over.\n"
            "• All math verified independently.",
            color=TEXT_PRIMARY,
            fontsize=12.5,
            linespacing=1.45,
            va="center",
            alpha=fade,
        )

        ax.text(
            8.0,
            1.1,
            "Thank you for watching! Code & Storyboard PDF available in the GitHub repository.",
            color=TEXT_MUTED,
            fontsize=14,
            ha="center",
            alpha=fade,
        )

        yield fig_to_rgb_bytes(fig)
        plt.close(fig)


SCENE_RENDERERS = {
    "00_opening": render_opening,
    "01_hook": render_hook,
    "02_concept": render_concept,
    "03_intuition": render_intuition,
    "04_example": render_example,
    "05_interpretation": render_interpretation,
    "06_summary": render_summary,
}
