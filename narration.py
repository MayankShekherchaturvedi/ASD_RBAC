"""
Narration script and text-to-speech audio generator.
Uses edge-tts for natural voice-over narration (with macOS `say` fallback)
and ffprobe to measure exact segment durations for frame-accurate sync.
"""

import asyncio
import os
import subprocess
from pathlib import Path

VOICE = "en-US-AndrewNeural"

# Each segment has (segment_id, title, narration_text)
SEGMENTS = [
    (
        "00_opening",
        "Opening Frame",
        "Welcome to this M3 Calculus visual explainer on the Derivative and Rate of Change: "
        "how we move from a secant slope to a tangent slope.",
    ),
    (
        "01_hook",
        "Scene 1: Hook and Context",
        "Imagine you are driving a car along a straight highway. Suppose your distance in meters "
        "after t seconds is given by s of t equals t squared. "
        "At t equals 2 seconds, you have traveled 4 meters. At t equals 4 seconds, you are at 16 meters. "
        "Computing your average speed over those 2 seconds is easy: 16 minus 4, divided by 4 minus 2, "
        "gives 6 meters per second. "
        "But if you glance down at your speedometer at the exact instant t equals 2 seconds, "
        "what number does it show? Average speed needs two different times. "
        "How can we measure a rate of change at a single instant?",
    ),
    (
        "02_concept",
        "Scene 2: Concept Introduction",
        "By the end of this video, you will be able to understand how the average rate of change, "
        "which is the slope of a secant line, transitions into the instantaneous rate of change, "
        "the slope of a tangent line, as the step size h approaches zero. "
        "Let us define our notation carefully. For a function f of x, we pick a starting point x "
        "and a nearby point x plus h, where h is a small non-zero step. "
        "The average rate of change on the interval from x to x plus h is the difference quotient: "
        "f of x plus h, minus f of x, all divided by h. "
        "Geometrically, this is the slope of the secant line connecting two points on the graph. "
        "The derivative, written f prime of x, is the limit of this secant slope as h approaches zero.",
    ),
    (
        "03_intuition",
        "Scene 3: Visual Intuition",
        "Let us see why this works visually on the curve f of x equals x squared. "
        "Fix the point P at x equals 2, where f of 2 equals 4. "
        "Now place a second point Q at x equals 2 plus h. "
        "The amber line passing through P and Q is our secant line. "
        "Its slope is rise over run: delta y divided by h. "
        "Watch what happens as we shrink h closer and closer to zero. "
        "At h equals 2, Q is at 4 comma 16, and the secant line is quite steep, with slope 6. "
        "Shrink h to 1: Q slides down to 3 comma 9, and the secant slope drops to 5. "
        "Shrink h to 0.5: the secant line hugs the curve more tightly, with slope 4.5. "
        "At h equals 0.1, Q is almost on top of P, and the slope is 4.1. "
        "As h approaches zero, the secant line rotates smoothly and settles onto one unique line "
        "that just grazes the curve at P: the emerald tangent line.",
    ),
    (
        "04_example",
        "Scene 4: Worked Example",
        "Now let us verify this exact limit with algebra. "
        "On the left, our table of secant slopes for f of x equals x squared at x equals 2 "
        "shows values 6, 5, 4.5, 4.1, and 4.01. Every step gets closer to 4. "
        "Why cannot we just plug in h equals 0 right away? Because that gives 0 divided by 0, which is undefined. "
        "Instead, we simplify the difference quotient first. "
        "Start with f of 2 plus h, minus f of 2, divided by h. "
        "Substitute f of x equals x squared: we get 2 plus h squared, minus 4, over h. "
        "Expand 2 plus h squared to get 4 plus 4 h plus h squared. "
        "Notice that 4 minus 4 cancels out cleanly, leaving 4 h plus h squared, divided by h. "
        "Factor out h from the numerator: h times 4 plus h, over h. "
        "Since h is approaching zero but not equal to zero, we can cancel h, leaving simply 4 plus h. "
        "Now take the limit as h approaches zero: 4 plus 0 equals 4. "
        "So f prime of 2 is exactly 4.",
    ),
    (
        "05_interpretation",
        "Scene 5: Interpretation",
        "What does this number, f prime of 2 equals 4, actually tell us? "
        "Geometrically, 4 is the exact slope of the tangent line at the point 2 comma 4, "
        "whose equation is y equals 4 x minus 4. "
        "If we zoom in closer and closer around the point 2 comma 4, "
        "the curved parabola flattens out and becomes nearly indistinguishable from this straight tangent line. "
        "This property is called local linearity. "
        "And returning to our driving car example: at the exact instant t equals 2 seconds, "
        "the speedometer reads 4 meters per second.",
    ),
    (
        "06_summary",
        "Scene 6: Summary and Credits",
        "Let us recap our three core takeaways. "
        "First, the average rate of change over an interval is the slope of a secant line between two points. "
        "Second, shrinking the horizontal step h toward zero turns the secant line into the tangent line. "
        "Third, simplifying the difference quotient before taking the limit reveals the exact instantaneous rate of change. "
        "Thank you for watching. All code, storyboard PDF, and AI tool disclosures are available in the project repository.",
    ),
]


def get_audio_duration(filepath: Path) -> float:
    """Return exact duration of an audio file in seconds using ffprobe."""
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(filepath),
    ]
    out = subprocess.check_output(cmd, text=True).strip()
    return float(out)


async def _synth_edge_tts(text: str, out_mp3: Path) -> None:
    import edge_tts

    communicate = edge_tts.Communicate(text, VOICE, rate="-4%")
    await communicate.save(str(out_mp3))


def generate_all_audio(audio_dir: Path) -> list[tuple[str, str, Path, float]]:
    """
    Generate voice-over MP3 files for all segments and return
    list of (seg_id, title, audio_path, duration_sec).
    """
    audio_dir.mkdir(parents=True, exist_ok=True)
    results = []

    for seg_id, title, text in SEGMENTS:
        out_mp3 = audio_dir / f"{seg_id}.mp3"
        if not out_mp3.exists():
            try:
                asyncio.run(_synth_edge_tts(text, out_mp3))
            except Exception as exc:
                print(f"[narration] edge-tts failed ({exc}), falling back to macOS `say`...")
                tmp_aiff = audio_dir / f"{seg_id}.aiff"
                subprocess.run(["say", "-o", str(tmp_aiff), text], check=True)
                subprocess.run(
                    ["ffmpeg", "-y", "-i", str(tmp_aiff), "-q:a", "2", str(out_mp3)],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                tmp_aiff.unlink(missing_ok=True)

        dur = get_audio_duration(out_mp3)
        # Add a 0.8s breathing pause at the end of each segment
        padded_dur = dur + 0.8
        print(f"  Audio {seg_id}: {dur:.2f}s (padded to {padded_dur:.2f}s)")
        results.append((seg_id, title, out_mp3, padded_dur))

    return results


if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "build_assets" / "audio"
    items = generate_all_audio(out)
    total = sum(x[3] for x in items)
    print(f"Total narration duration: {total:.2f}s ({total/60:.2f} min)")
