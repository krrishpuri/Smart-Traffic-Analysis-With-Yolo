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

# Open video
video_path = "data/videos/traffic.mp4"

results = model.track(
    source=video_path,
    tracker="bytetrack.yaml",
    stream=True
)

for result in results:

    # Count vehicles in current frame
    vehicle_count = 0

    if result.boxes:

        class_ids = result.boxes.cls.int().cpu().tolist()

        for class_id in class_ids:

            if class_id in vehicle_classes:
                vehicle_count += 1

    # Determine traffic density
    if vehicle_count <= 5:
        density = "LOW"
    elif vehicle_count <= 10:
        density = "MEDIUM"
    else:
        density = "HIGH"

    # Get frame
    frame = result.plot()

    # Display vehicle count
    cv2.putText(
        frame,
        f"Vehicles: {vehicle_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Display traffic density
    cv2.putText(
        frame,
        f"Traffic Density: {density}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    # Show video
    cv2.imshow("Smart Traffic Analysis", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()