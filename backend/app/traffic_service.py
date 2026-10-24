
# import threading
# from pathlib import Path

# import cv2
# from ultralytics import YOLO

# PROJECT_ROOT = Path(__file__).resolve().parents[2]
# VIDEO_PATH = PROJECT_ROOT / "data" / "videos" / "traffic.mp4"
# MODEL_PATH = PROJECT_ROOT / "yolo11n.pt"

# VEHICLE_CLASSES = {
#     2: "cars",
#     3: "motorcycles",
#     5: "buses",
#     7: "trucks",
# }

# _lock = threading.Lock()

# _stats = {
#     "vehicles_detected": 0,
#     "cars": 0,
#     "motorcycles": 0,
#     "buses": 0,
#     "trucks": 0,
#     "density": "LOW",
#     "average_speed": None,
#     "violations": 0,
#     "processing": False,
#     "error": None,
# }


# def get_traffic_summary():
#     with _lock:
#         return _stats.copy()


# def process_video():
#     try:
#         if not VIDEO_PATH.exists():
#             raise FileNotFoundError(f"Video not found: {VIDEO_PATH}")

#         model = YOLO(str(MODEL_PATH))
#         seen_vehicles = {}

#         with _lock:
#             _stats["processing"] = True
#             _stats["error"] = None

#         results = model.track(
#             source=str(VIDEO_PATH),
#             stream=True,
#             persist=True,
#             tracker="bytetrack.yaml",
#             verbose=False,
#         )

#         for result in results:
#             frame_counts = {name: 0 for name in VEHICLE_CLASSES.values()}

#             if result.boxes is not None:
#                 boxes = result.boxes
#                 ids = boxes.id

#                 if ids is not None:
#                     track_ids = ids.int().cpu().tolist()
#                     class_ids = boxes.cls.int().cpu().tolist()

#                     for track_id, class_id in zip(track_ids, class_ids):
#                         if class_id not in VEHICLE_CLASSES:
#                             continue

#                         vehicle_type = VEHICLE_CLASSES[class_id]
#                         frame_counts[vehicle_type] += 1
#                         seen_vehicles[track_id] = vehicle_type

#             visible_count = sum(frame_counts.values())

#             if visible_count <= 5:
#                 density = "LOW"
#             elif visible_count <= 10:
#                 density = "MEDIUM"
#             else:
#                 density = "HIGH"

#             counts = {
#                 name: sum(
#                     1 for vehicle_type in seen_vehicles.values()
#                     if vehicle_type == name
#                 )
#                 for name in VEHICLE_CLASSES.values()
#             }

#             with _lock:
#                 _stats.update({
#                     "vehicles_detected": len(seen_vehicles),
#                     **counts,
#                     "density": density,
#                 })

#         # The video has finished processing.
#     except Exception as exc:
#         with _lock:
#             _stats["error"] = str(exc)
#     finally:
#         with _lock:
#             _stats["processing"] = False


# def start_processing():
#     worker = threading.Thread(target=process_video, daemon=True)
#     worker.start()



import threading
from pathlib import Path
from typing import Any

import cv2
from ultralytics import YOLO

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VIDEO_DIR = PROJECT_ROOT / "data" / "videos"
MODEL_PATH = PROJECT_ROOT / "yolo11n.pt"
PERMITTED_VIDEOS = ("traffic.mp4", "highway.mp4")

VEHICLE_CLASSES = {
    2: "cars",
    3: "motorcycles",
    5: "buses",
    7: "trucks",
}

_lock = threading.Lock()
_processing_lock = threading.Lock()
_model_lock = threading.Lock()
_model: YOLO | None = None
_active_video = PERMITTED_VIDEOS[0]
_stream_generation = 0
_active_captures: list[cv2.VideoCapture] = []

_stats = {
    "vehicles_detected": 0,
    "cars": 0,
    "motorcycles": 0,
    "buses": 0,
    "trucks": 0,
    "density": "LOW",
    "average_speed": None,
    "violations": 0,
    "processing": False,
    "error": None,
    "video": _active_video,
}


def get_traffic_summary():
    with _lock:
        return _stats.copy()


def get_available_videos() -> dict[str, Any]:
    videos = [
        {
            "filename": filename,
            "label": Path(filename).stem.replace("_", " ").title(),
        }
        for filename in PERMITTED_VIDEOS
        if (VIDEO_DIR / filename).is_file()
    ]
    with _lock:
        active_video = _active_video
    return {"videos": videos, "active_video": active_video}


def switch_video(filename: str) -> dict[str, str]:
    global _active_video, _stream_generation

    if filename not in PERMITTED_VIDEOS:
        raise ValueError("Video selection is not permitted.")

    video_path = VIDEO_DIR / filename
    if not video_path.is_file():
        raise FileNotFoundError(f"Video not found: {filename}")

    with _lock:
        _active_video = filename
        _stream_generation += 1
        _reset_stats_locked()
        _stats["video"] = filename
        captures = list(_active_captures)

    for capture in captures:
        capture.release()

    return {"filename": filename}


def _reset_stats_locked() -> None:
    for key in (
        "vehicles_detected",
        "cars",
        "motorcycles",
        "buses",
        "trucks",
        "violations",
    ):
        _stats[key] = 0
    _stats["density"] = "LOW"
    _stats["average_speed"] = None
    _stats["error"] = None


def _get_model() -> YOLO:
    global _model

    if _model is None:
        with _model_lock:
            if _model is None:
                if not MODEL_PATH.is_file():
                    raise FileNotFoundError(f"YOLO model not found: {MODEL_PATH}")
                _model = YOLO(str(MODEL_PATH))
    return _model


def generate_video_frames():
    """Generate annotated MJPEG frames for the frontend."""
    cap = None
    _processing_lock.acquire()

    try:
        with _lock:
            video_name = _active_video
            generation = _stream_generation

        video_path = VIDEO_DIR / video_name
        if not video_path.is_file():
            raise FileNotFoundError(f"Video not found: {video_name}")

        model = _get_model()
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise RuntimeError(f"Could not open video: {video_name}")

        seen_vehicles = {}

        with _lock:
            _active_captures.append(cap)
            _stats["processing"] = True
            _stats["error"] = None
            _stats["video"] = video_name

        # Reset tracker state for this video without reloading model weights.
        model.predictor = None

        while True:
            with _lock:
                if generation != _stream_generation or video_name != _active_video:
                    return

            success, frame = cap.read()

            # Replay the video when it reaches the end.
            if not success:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                seen_vehicles.clear()

                with _lock:
                    _reset_stats_locked()
                    _stats["video"] = video_name

                # Reset the tracker for the next playback.
                model.predictor = None
                continue

            results = model.track(
                frame,
                persist=True,
                tracker="bytetrack.yaml",
                verbose=False,
            )

            result = results[0]
            frame_counts = {name: 0 for name in VEHICLE_CLASSES.values()}

            if result.boxes is not None:
                boxes = result.boxes

                if boxes.id is not None:
                    track_ids = boxes.id.int().cpu().tolist()
                    class_ids = boxes.cls.int().cpu().tolist()

                    for track_id, class_id in zip(track_ids, class_ids):
                        if class_id not in VEHICLE_CLASSES:
                            continue

                        vehicle_type = VEHICLE_CLASSES[class_id]
                        frame_counts[vehicle_type] += 1
                        seen_vehicles[track_id] = vehicle_type

            visible_count = sum(frame_counts.values())

            if visible_count <= 5:
                density = "LOW"
            elif visible_count <= 10:
                density = "MEDIUM"
            else:
                density = "HIGH"

            unique_counts = {
                name: sum(
                    1
                    for vehicle_type in seen_vehicles.values()
                    if vehicle_type == name
                )
                for name in VEHICLE_CLASSES.values()
            }

            with _lock:
                _stats.update({
                    "vehicles_detected": len(seen_vehicles),
                    **unique_counts,
                    "density": density,
                    "error": None,
                })

            # Draw YOLO detection boxes and labels.
            annotated_frame = result.plot()

            # Encode the frame as JPEG.
            encoded, buffer = cv2.imencode(".jpg", annotated_frame)

            if not encoded:
                continue

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + buffer.tobytes()
                + b"\r\n"
            )

    except GeneratorExit:
        return
    except Exception as exc:
        with _lock:
            _stats["error"] = str(exc)
        print(f"Video stream error: {exc}")
    finally:
        if cap is not None:
            cap.release()
            with _lock:
                if cap in _active_captures:
                    _active_captures.remove(cap)

        with _lock:
            if not _active_captures:
                _stats["processing"] = False
        _processing_lock.release()
