"""
Configuration for the M3 Internal Assessment Animation Video:
"Derivative and Rate of Change: From Secant Slope to Tangent Slope"
"""

# Student & Assessment Metadata (update these before final submission)
STUDENT_NAME = "Mayank Shekhar Chaturvedi"
STUDENT_ID = "E25B070727"
COURSE_NAME = "Linear Algebra and Calculus (M3) • Internal Assessment"
VIDEO_TITLE = "Derivative and Rate of Change"
VIDEO_SUBTITLE = "From Secant Slope to Tangent Slope"
CONCEPT_AREA = "Single-Variable Calculus — Derivative & Rate of Change"

LEARNING_OBJECTIVE = (
    "By the end of this video, the viewer will be able to understand how the "
    "average rate of change (secant slope) transitions into the instantaneous "
    "rate of change (tangent slope) as h approaches 0, and compute f'(2) for f(x) = x^2."
)

# Video Output Settings (1080p 16:9 Landscape)
WIDTH = 1920
HEIGHT = 1080
FPS = 30
DPI = 150
FIGSIZE = (WIDTH / DPI, HEIGHT / DPI)  # (12.8, 7.2) inches

# Visual Palette (High-contrast academic dark theme)
BG_COLOR = "#0F172A"       # Deep slate navy
CARD_BG = "#1E293B"        # Elevated slate card
GRID_COLOR = "#334155"     # Subtle grid lines
TEXT_PRIMARY = "#F8FAFC"   # Crisp white
TEXT_MUTED = "#94A3B8"     # Muted slate gray
ACCENT_BLUE = "#38BDF8"    # Curve f(x) = x^2
ACCENT_AMBER = "#F59E0B"   # Secant line & moving point Q
ACCENT_GREEN = "#10B981"   # Tangent line & final answer
ACCENT_PINK = "#F472B6"    # Fixed point P & highlights
ACCENT_RED = "#EF4444"     # Caution / division by zero highlight
