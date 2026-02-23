"""
Traffic Analysis Engine
Handles vehicle detection and all traffic metrics computation.
"""

from __future__ import annotations

import tempfile
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO

# ─────────────────────────────────────────────
CLASS_NAMES = ["bus", "car", "van"]
LARGE_VEHICLES = {"bus", "van"}
SMALL_VEHICLES = {"car"}
CONGESTION_WEIGHTS = {"bus": 3.0, "van": 2.0, "car": 1.0}
COLORS_BGR = {"bus": (34, 87, 255), "car": (243, 150, 33), "van": (80, 175, 76)}
COLORS_HEX = {"bus": "#FF5722", "car": "#2196F3", "van": "#4CAF50"}
# ─────────────────────────────────────────────


def load_model(model_path: str) -> YOLO:
    return YOLO(model_path)


def analyze_frame(
    model: YOLO,
    image: np.ndarray,
    conf: float = 0.4,
    iou: float = 0.5,
) -> dict:
    """
    Run detection on a single BGR numpy frame.
    Returns a dict with counts, density, ratio, congestion, and annotated image.
    """
    results = model.predict(source=image, conf=conf, iou=iou, verbose=False)[0]

    vehicle_counts: dict[str, int] = defaultdict(int)
    detections: list[dict] = []

    if results.boxes is not None:
        for i in range(len(results.boxes)):
            cls_id = int(results.boxes.cls[i].item())
            conf_val = float(results.boxes.conf[i].item())
            xyxy = results.boxes.xyxy[i].cpu().numpy()
            cls_name = CLASS_NAMES[cls_id] if cls_id < len(CLASS_NAMES) else "unknown"
            vehicle_counts[cls_name] += 1
            detections.append({"class": cls_name, "conf": conf_val, "bbox": xyxy})

    analytics = _compute_analytics(vehicle_counts, image)
    annotated = _draw_boxes(image.copy(), detections)

    return {
        **analytics,
        "detections": detections,
        "annotated": annotated,
    }


def _compute_analytics(vehicle_counts: dict, image: np.ndarray) -> dict:
    counts = {
        "bus": vehicle_counts.get("bus", 0),
        "car": vehicle_counts.get("car", 0),
        "van": vehicle_counts.get("van", 0),
        "total": sum(vehicle_counts.values()),
    }

    h, w = image.shape[:2]
    img_area = h * w
    density_score = (counts["total"] / img_area) * 100_000 if img_area > 0 else 0

    if density_score < 0.5:
        density_level, density_color = "Rendah", "#22c55e"
    elif density_score < 1.5:
        density_level, density_color = "Sedang", "#eab308"
    elif density_score < 3.0:
        density_level, density_color = "Tinggi", "#f97316"
    else:
        density_level, density_color = "Sangat Tinggi", "#ef4444"

    large = sum(vehicle_counts.get(v, 0) for v in LARGE_VEHICLES)
    small = sum(vehicle_counts.get(v, 0) for v in SMALL_VEHICLES)
    total = counts["total"]

    if small > 0:
        ratio_val = round(large / small, 2)
    else:
        ratio_val = float("inf") if large > 0 else 0.0

    ratio = {
        "large": large,
        "small": small,
        "ratio": ratio_val,
        "pct_large": round(large / total * 100, 1) if total > 0 else 0,
        "pct_small": round(small / total * 100, 1) if total > 0 else 0,
        "composition": (
            "Dominan Kendaraan Besar"
            if large > small
            else ("Dominan Kendaraan Kecil" if small > large else "Seimbang")
        ),
    }

    weighted = sum(
        vehicle_counts.get(c, 0) * w for c, w in CONGESTION_WEIGHTS.items()
    )
    ci = min(100.0, (weighted / 50) * 100)

    if ci < 20:
        cl, ce, cd = "Lancar", "🟢", "Lalu lintas lancar, tidak ada hambatan"
    elif ci < 40:
        cl, ce, cd = "Ramai Lancar", "🟡", "Ramai namun masih mengalir"
    elif ci < 60:
        cl, ce, cd = "Padat", "🟠", "Mulai ada perlambatan signifikan"
    elif ci < 80:
        cl, ce, cd = "Macet", "🔴", "Kemacetan parah, kecepatan sangat rendah"
    else:
        cl, ce, cd = "Macet Total", "⛔", "Hampir tidak bergerak"

    cong_color_map = {
        "Lancar": "#22c55e",
        "Ramai Lancar": "#eab308",
        "Padat": "#f97316",
        "Macet": "#ef4444",
        "Macet Total": "#7f1d1d",
    }

    return {
        "vehicle_counts": counts,
        "density": {
            "score": round(density_score, 3),
            "level": density_level,
            "color": density_color,
        },
        "ratio": ratio,
        "congestion": {
            "index": round(ci, 1),
            "level": cl,
            "emoji": ce,
            "description": cd,
            "color": cong_color_map.get(cl, "#6b7280"),
        },
    }


def _draw_boxes(image: np.ndarray, detections: list[dict]) -> np.ndarray:
    """Draw bounding boxes on BGR image."""
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    for det in detections:
        cls_name = det["class"]
        conf_val = det["conf"]
        x1, y1, x2, y2 = [int(v) for v in det["bbox"]]
        color = COLORS_BGR.get(cls_name, (200, 200, 200))
        # Box
        cv2.rectangle(img_rgb, (x1, y1), (x2, y2), color, 2)
        # Label background
        label = f"{cls_name} {conf_val:.2f}"
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
        cv2.rectangle(img_rgb, (x1, y1 - th - 6), (x1 + tw + 6, y1), color, -1)
        cv2.putText(
            img_rgb, label, (x1 + 3, y1 - 3),
            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1,
        )
    return img_rgb


def process_video_file(
    model: YOLO,
    video_path: str,
    conf: float = 0.4,
    iou: float = 0.5,
    sample_every: int = 3,
    max_frames=None
) -> tuple[str, list[dict]]:
    """
    Process a video file. Returns (output_path, frame_stats).
    """
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 25
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out_path = tempfile.mktemp(suffix=".mp4")
    writer = cv2.VideoWriter(
        out_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h)
    )

    frame_stats: list[dict] = []
    fc = 0
    last_result = None
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if max_frames is not None and frame_count >= max_frames:break
        
        if fc % sample_every == 0:
            last_result = analyze_frame(model, frame, conf, iou)
            frame_stats.append(
                {
                    "frame": fc,
                    "time_sec": round(fc / fps, 2),
                    "total": last_result["vehicle_counts"]["total"],
                    "bus": last_result["vehicle_counts"]["bus"],
                    "car": last_result["vehicle_counts"]["car"],
                    "van": last_result["vehicle_counts"]["van"],
                    "congestion_index": last_result["congestion"]["index"],
                    "congestion_level": last_result["congestion"]["level"],
                }
            )
        frame_count += 1
        if last_result is not None:
            out_frame = _overlay_video_stats(frame.copy(), last_result)
        else:
            out_frame = frame

        writer.write(cv2.cvtColor(out_frame, cv2.COLOR_RGB2BGR) if last_result else out_frame)
        fc += 1

    cap.release()
    writer.release()
    return out_path, frame_stats


def _overlay_video_stats(frame: np.ndarray, result: dict) -> np.ndarray:
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Draw boxes
    for det in result.get("detections", []):
        cls_name = det["class"]
        x1, y1, x2, y2 = [int(v) for v in det["bbox"]]
        color = COLORS_BGR.get(cls_name, (200, 200, 200))
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

    # HUD overlay
    ov = img.copy()
    cv2.rectangle(ov, (8, 8), (340, 130), (15, 15, 15), -1)
    img = cv2.addWeighted(ov, 0.65, img, 0.35, 0)

    c = result["vehicle_counts"]
    g = result["congestion"]
    cv2.putText(img, f"Bus:{c['bus']}  Car:{c['car']}  Van:{c['van']}",
                (18, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
    cv2.putText(img, f"Total Kendaraan: {c['total']}",
                (18, 68), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 230, 80), 2)
    cv2.putText(img, f"Kemacetan: {g['level']} ({g['index']:.0f}/100)",
                (18, 98), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (80, 255, 140), 2)
    return img
