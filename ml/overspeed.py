import math

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

# Speed limit
SPEED_LIMIT = 50

# Previous position of each vehicle
previous_positions = {}

# Speed of each vehicle
vehicle_speeds = {}

# Calibration factor
PIXELS_PER_METER = 10

# Video FPS
FPS = 30

# Video
video_path = "data/videos/traffic.mp4"

results = model.track(
    source=video_path,
    tracker="bytetrack.yaml",
    stream=True
)

for result in results:

    frame = result.plot()

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

            current_position = (center_x, center_y)

            # Calculate speed
            if track_id in previous_positions:

                previous_position = previous_positions[track_id]

                dx = center_x - previous_position[0]
                dy = center_y - previous_position[1]

                pixel_distance = math.sqrt(
                    dx ** 2 + dy ** 2
                )

                distance_meters = (
                    pixel_distance / PIXELS_PER_METER
                )

                time_seconds = 1 / FPS

                speed_mps = (
                    distance_meters / time_seconds
                )

                speed_kmh = speed_mps * 3.6

                vehicle_speeds[track_id] = speed_kmh

            # Save position
            previous_positions[track_id] = current_position

            # Get speed
            speed = vehicle_speeds.get(track_id, 0)

            # Check overspeed
            if speed > SPEED_LIMIT:

                status = "OVERSPEEDING!"

            else:

                status = "Normal"

            # Display information
            text = (
                f"ID {track_id} "
                f"{speed:.1f} km/h "
                f"{status}"
            )

            cv2.putText(
                frame,
                text,
                (center_x, center_y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 0, 255) if speed > SPEED_LIMIT
                else (0, 255, 0),
                2
            )

    # Display speed limit
    cv2.putText(
        frame,
        f"Speed Limit: {SPEED_LIMIT} km/h",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.imshow(
        "Overspeed Detection",
        frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()