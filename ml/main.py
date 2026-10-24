
import math

import cv2
from ultralytics import YOLO

# ==========================================
# CONFIGURATION
# ==========================================

MODEL_PATH = "yolo11n.pt"
VIDEO_PATH = "data/videos/traffic.mp4"

SPEED_LIMIT = 50
PIXELS_PER_METER = 10  # Demo only; calibrate for real speed
TRAFFIC_LIGHT = "RED"  # Simulated signal, not automatically detected
STOP_LINE_Y = 300      # Adjust to match your video

VEHICLES = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck"
}

# ==========================================
# INITIALIZATION
# ==========================================

model = YOLO(MODEL_PATH)

# Get actual video FPS
video = cv2.VideoCapture(VIDEO_PATH)

if not video.isOpened():
    raise FileNotFoundError(
        f"Could not open video: {VIDEO_PATH}"
    )

FPS = video.get(cv2.CAP_PROP_FPS)
video.release()

if not FPS or FPS <= 0:
    FPS = 30.0

previous_positions = {}
vehicle_speeds = {}
counted_ids = set()
violations = set()

counts = {name: 0 for name in VEHICLES.values()}

frame_number = 0

# ==========================================
# DETECTION + TRACKING
# ==========================================

results = model.track(
    source=VIDEO_PATH,
    tracker="bytetrack.yaml",
    stream=True,
    persist=True,
    verbose=False
)

for result in results:
    frame_number += 1
    frame = result.plot()

    frame_counts = {name: 0 for name in VEHICLES.values()}

    # Draw stop line
    cv2.line(
        frame,
        (0, STOP_LINE_Y),
        (frame.shape[1], STOP_LINE_Y),
        (0, 0, 255),
        2
    )

    if result.boxes is not None and result.boxes.id is not None:
        boxes = result.boxes

        track_ids = boxes.id.int().cpu().tolist()
        class_ids = boxes.cls.int().cpu().tolist()
        coordinates = boxes.xyxy.cpu().tolist()

        for track_id, class_id, box in zip(
            track_ids, class_ids, coordinates
        ):
            # Only process vehicles
            if class_id not in VEHICLES:
                continue

            vehicle_name = VEHICLES[class_id]

            x1, y1, x2, y2 = box

            # Bottom-center point is useful for road contact
            cx = int((x1 + x2) / 2)
            cy = int(y2)

            # Step 3: Count unique tracked vehicles
            if track_id not in counted_ids:
                counted_ids.add(track_id)
                counts[vehicle_name] += 1

            # Step 4: Count vehicles currently visible
            frame_counts[vehicle_name] += 1

            # Get previous position and frame
            previous = previous_positions.get(track_id)

            speed = vehicle_speeds.get(track_id, 0.0)

            if previous is not None:
                prev_x, prev_y, prev_frame = previous

                frame_gap = frame_number - prev_frame

                if frame_gap > 0:
                    pixel_distance = math.hypot(
                        cx - prev_x,
                        cy - prev_y
                    )

                    distance_meters = (
                        pixel_distance / PIXELS_PER_METER
                    )

                    elapsed_seconds = frame_gap / FPS

                    speed_mps = (
                        distance_meters / elapsed_seconds
                    )

                    speed = speed_mps * 3.6
                    vehicle_speeds[track_id] = speed

                # Step 7: Detect crossing from above to below
                crossed_line = (
                    prev_y < STOP_LINE_Y
                    and cy >= STOP_LINE_Y
                )

                if (
                    TRAFFIC_LIGHT == "RED"
                    and crossed_line
                    and track_id not in violations
                ):
                    violations.add(track_id)

                    print(
                        f"RED LIGHT VIOLATION: "
                        f"{vehicle_name} ID {track_id}"
                    )

            # Save current position
            previous_positions[track_id] = (
                cx, cy, frame_number
            )

            # Step 6: Overspeed check
            overspeeding = speed > SPEED_LIMIT

            if overspeeding:
                label = (
                    f"{vehicle_name} ID:{track_id} "
                    f"{speed:.1f} km/h OVERSPEED!"
                )
                color = (0, 0, 255)
            else:
                label = (
                    f"{vehicle_name} ID:{track_id} "
                    f"{speed:.1f} km/h"
                )
                color = (0, 255, 0)

            # Step 1, 2, 5, 6: Detection, tracking, speed
            cv2.putText(
                frame,
                label,
                (max(cx - 80, 5), max(cy - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                color,
                2
            )

            # Show violation label
            if track_id in violations:
                cv2.putText(
                    frame,
                    "RED LIGHT VIOLATION!",
                    (max(cx - 80, 5), max(cy - 35, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    2
                )

    # Step 4: Traffic density
    total_visible = sum(frame_counts.values())

    if total_visible <= 5:
        density = "LOW"
    elif total_visible <= 10:
        density = "MEDIUM"
    else:
        density = "HIGH"

    # Display dashboard overlay
    cv2.putText(
        frame,
        f"Signal: {TRAFFIC_LIGHT}",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2
    )

    cv2.putText(
        frame,
        f"Visible vehicles: {total_visible} | Density: {density}",
        (20, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Unique vehicles: {len(counted_ids)}",
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Violations: {len(violations)}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (0, 0, 255),
        2
    )

    cv2.imshow("Smart Traffic Analysis", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()

# ==========================================
# FINAL REPORT
# ==========================================

print("\n========== TRAFFIC SUMMARY ==========")

for name, count in counts.items():
    print(f"{name.capitalize()}: {count}")

print("Total unique vehicles:", sum(counts.values()))
print("Red-light violations:", len(violations))

overspeed_ids = [
    track_id
    for track_id, speed in vehicle_speeds.items()
    if speed > SPEED_LIMIT
]

print("Overspeeding vehicle IDs:", overspeed_ids)
print("Video FPS:", FPS)

print("=====================================")
