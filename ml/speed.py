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

# Store previous center position of each vehicle
previous_positions = {}

# Store speed for each vehicle
vehicle_speeds = {}

# Calibration
PIXELS_PER_METER = 10

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

            # Find center of vehicle
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            current_position = (center_x, center_y)

            # Calculate movement
            if track_id in previous_positions:

                previous_position = previous_positions[track_id]

                dx = center_x - previous_position[0]
                dy = center_y - previous_position[1]

                # Pixel distance
                pixel_distance = math.sqrt(
                    dx ** 2 + dy ** 2
                )

                # Convert pixels to meters
                distance_meters = pixel_distance / PIXELS_PER_METER

                # Assume video is 30 FPS
                fps = 30

                # Time between frames
                time_seconds = 1 / fps

                # Speed in meters/second
                speed_mps = distance_meters / time_seconds

                # Convert to km/h
                speed_kmh = speed_mps * 3.6

                vehicle_speeds[track_id] = speed_kmh

            # Save current position
            previous_positions[track_id] = current_position

            # Display vehicle ID and speed
            speed = vehicle_speeds.get(track_id, 0)

            text = f"ID {track_id} {speed:.1f} km/h"

            cv2.putText(
                frame,
                text,
                (center_x, center_y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    cv2.imshow(
        "Vehicle Speed Estimation",
        frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()