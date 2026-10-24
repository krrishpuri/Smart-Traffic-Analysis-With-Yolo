from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")

# Track objects in the video
results = model.track(
    source="data/videos/traffic.mp4",
    show=True,
    tracker="bytetrack.yaml",
    save=True
)

print("Tracking completed!")