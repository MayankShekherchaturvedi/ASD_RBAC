"""
Main build script for the M3 Internal Assessment Animation Video.
Generates voice-over narration, renders 1080p Matplotlib frames per scene,
pipes them directly to FFmpeg, and concatenates all scenes into Derivative_Video.mp4.
"""

import math
import subprocess
from pathlib import Path

from config import FPS, HEIGHT, WIDTH
from narration import generate_all_audio
from scenes import SCENE_RENDERERS


def render_segment_mp4(
    seg_id: str,
    audio_path: Path,
    duration: float,
    out_mp4: Path,
    preview_png: Path,
) -> None:
    num_frames = max(1, int(round(duration * FPS)))
    preview_idx = int(num_frames * 0.85)
    renderer = SCENE_RENDERERS[seg_id]

    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{WIDTH}x{HEIGHT}",
        "-r",
        str(FPS),
        "-i",
        "-",
        "-i",
        str(audio_path),
        "-af",
        "apad",
        "-t",
        f"{duration:.3f}",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "medium",
        "-crf",
        "20",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-ar",
        "44100",
        str(out_mp4),
    ]

    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )

    frame_bytes_len = WIDTH * HEIGHT * 3
    for idx, rgb_bytes in enumerate(renderer(num_frames)):
        assert len(rgb_bytes) == frame_bytes_len, f"Unexpected frame size: {len(rgb_bytes)}"
        proc.stdin.write(rgb_bytes)
        if idx == preview_idx:
            from PIL import Image
            img = Image.frombytes("RGB", (WIDTH, HEIGHT), rgb_bytes)
            img.save(preview_png)

    proc.stdin.close()
    _, stderr = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg failed for {seg_id}:\n{stderr.decode('utf-8', errors='ignore')}")


def main():
    code_dir = Path(__file__).resolve().parent
    project_dir = code_dir.parent
    assets_dir = code_dir / "build_assets"
    audio_dir = assets_dir / "audio"
    seg_dir = assets_dir / "segments"
    preview_dir = assets_dir / "previews"

    seg_dir.mkdir(parents=True, exist_ok=True)
    preview_dir.mkdir(parents=True, exist_ok=True)

    print("1. Generating voice-over narration...")
    audio_items = generate_all_audio(audio_dir)

    print("\n2. Rendering 1080p animation scenes...")
    segment_mp4s = []
    for seg_id, title, audio_path, duration in audio_items:
        out_mp4 = seg_dir / f"{seg_id}.mp4"
        preview_png = preview_dir / f"{seg_id}_preview.png"
        if out_mp4.exists() and out_mp4.stat().st_size > 10000 and preview_png.exists():
            print(f"  Skipping {seg_id} (already rendered).")
        else:
            print(f"  Rendering {seg_id} ({title}) -> {duration:.2f}s ({int(round(duration*FPS))} frames)...")
            render_segment_mp4(seg_id, audio_path, duration, out_mp4, preview_png)
        segment_mp4s.append(out_mp4)

    print("\n3. Concatenating scenes into final Derivative_Video.mp4...")
    concat_file = assets_dir / "concat.txt"
    with concat_file.open("w", encoding="utf-8") as f:
        for mp4 in segment_mp4s:
            f.write(f"file '{mp4.resolve()}'\n")

    final_video = project_dir / "Derivative_Video.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            "-movflags",
            "+faststart",
            str(final_video),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print(f"\nDone! Final video saved to: {final_video}")


if __name__ == "__main__":
    main()
