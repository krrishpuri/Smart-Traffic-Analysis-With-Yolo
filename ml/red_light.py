import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")

# Vehicle classes
vehicle_classes = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck"
}

# -----------------------------
# TRAFFIC LIGHT
# -----------------------------

# For now, we simulate RED light
traffic_light = "RED"

# -----------------------------
# STOP LINE
# -----------------------------

# Change this value depending
# on your video
STOP_LINE_Y = 300

# Store previous Y position
previous_positions = {}

# Store vehicles already detected
violations = set()

# Video
video_path = "data/videos/traffic.mp4"

# Track vehicles
results = model.track(
    source=video_path,
    tracker="bytetrack.yaml",
    stream=True
)

for result in results:

    frame = result.plot()

    # Draw stop line
    cv2.line(
        frame,
        (0, STOP_LINE_Y),
        (frame.shape[1], STOP_LINE_Y),
        (0, 0, 255),
        3
    )

    # Display traffic light
    cv2.putText(
        frame,
        f"Traffic Light: {traffic_light}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )

    if result.boxes.id is not None:

        boxes = result.boxes

        track_ids = boxes.id.int().cpu().tolist()
        class_ids = boxes.cls.int().cpu().tolist()
        coordinates = boxes.xyxy.cpu().tolist()

        for track_id, class_id, box in zip(
            track_ids,
            class_ids,
            coordinates
        ):

            # Ignore non-vehicles
            if class_id not in vehicle_classes:
                continue

            x1, y1, x2, y2 = box

            # Vehicle center
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # Previous Y position
            previous_y = previous_positions.get(
                track_id,
                center_y
            )

            # Detect crossing
            crossed_line = (
                previous_y < STOP_LINE_Y
                and center_y >= STOP_LINE_Y
            )

            # Check red-light violation
            if (
                traffic_light == "RED"
                and crossed_line
                and track_id not in violations
            ):

                violations.add(track_id)

                print(
                    f"RED LIGHT VIOLATION "
                    f"- Vehicle ID: {track_id}"
                )

            # Save position
            previous_positions[track_id] = center_y

            # Display violation
            if track_id in violations:

                cv2.putText(
                    frame,
                    "RED LIGHT VIOLATION!",
                    (center_x, center_y - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )

    cv2.imshow(
        "Red Light Violation Detection",
        frame
    )

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()

print("\n========== VIOLATIONS ==========")
print("Total violations:", len(violations))
print("================================")