from ultralytics import YOLO

model = YOLO("yolo11n.pt")

results = model("data/videos/traffic.mp4", show=True)

print("Detection completed!")