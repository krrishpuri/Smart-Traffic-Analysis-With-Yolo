from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")

# Vehicle classes we want
vehicle_classes = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck"
}

# Store IDs we've already counted
counted_ids = set()

# Counters
vehicle_count = {
    "car": 0,
    "motorcycle": 0,
    "bus": 0,
    "truck": 0
}

# Track vehicles
results = model.track(
    source="data/videos/traffic.mp4",
    tracker="bytetrack.yaml",
    show=True,
    stream=True
)

for result in results:

    if result.boxes.id is None:
        continue

    boxes = result.boxes

    # Tracking IDs
    track_ids = boxes.id.int().cpu().tolist()

    # Class IDs
    class_ids = boxes.cls.int().cpu().tolist()

    for track_id, class_id in zip(track_ids, class_ids):

        # Only process vehicles
        if class_id not in vehicle_classes:
            continue

        vehicle_name = vehicle_classes[class_id]

        # Count vehicle only once
        if track_id not in counted_ids:

            counted_ids.add(track_id)

            vehicle_count[vehicle_name] += 1

# Display results
print("\n========== TRAFFIC SUMMARY ==========")

print("Cars:", vehicle_count["car"])
print("Motorcycles:", vehicle_count["motorcycle"])
print("Buses:", vehicle_count["bus"])
print("Trucks:", vehicle_count["truck"])

total = sum(vehicle_count.values())

print("Total Vehicles:", total)

print("====================================")