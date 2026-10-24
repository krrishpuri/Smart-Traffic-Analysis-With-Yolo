
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI(
#     title="Smart Traffic Analysis API",
#     description="API for YOLO-based traffic monitoring",
#     version="1.0.0",
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/")
# def home():
#     return {
#         "message": "Smart Traffic Analysis API is running"
#     }


# @app.get("/api/health")
# def health():
#     return {
#         "status": "healthy",
#         "service": "traffic-analysis",
#     }


# @app.get("/api/traffic/summary")
# def traffic_summary():
#     # Temporary sample response.
#     # Next, we'll connect this to actual YOLO results.
#     return {
#         "vehicles_detected": 0,
#         "cars": 0,
#         "motorcycles": 0,
#         "buses": 0,
#         "trucks": 0,
#         "density": "LOW",
#         "average_speed": None,
#         "violations": 0,
#     }



# from contextlib import asynccontextmanager

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from backend.app.traffic_service import (
#     get_traffic_summary,
#     start_processing,
# )


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     start_processing()
#     yield


# app = FastAPI(
#     title="Smart Traffic Analysis API",
#     description="API for YOLO-based traffic monitoring",
#     version="1.0.0",
#     lifespan=lifespan,
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:5173",
#         "http://localhost:5174",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/")
# def home():
#     return {"message": "Smart Traffic Analysis API is running"}


# @app.get("/api/health")
# def health():
#     return {
#         "status": "healthy",
#         "service": "traffic-analysis",
#     }


# @app.get("/api/traffic/summary")
# def traffic_summary():
#     return get_traffic_summary()



from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from backend.app.traffic_service import (
    generate_video_frames,
    get_available_videos,
    get_traffic_summary,
    switch_video,
)

app = FastAPI(
    title="Smart Traffic Analysis API",
    description="API for YOLO-based traffic monitoring",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class VideoSelection(BaseModel):
    filename: str


@app.get("/")
def home():
    return {"message": "Smart Traffic Analysis API is running"}


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "service": "traffic-analysis",
    }


@app.get("/api/traffic/summary")
def traffic_summary():
    return get_traffic_summary()


@app.get("/api/traffic/videos")
def available_videos():
    return get_available_videos()


@app.post("/api/traffic/videos/select")
def select_video(selection: VideoSelection):
    try:
        return switch_video(selection.filename)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/traffic/video-stream")
def video_stream():
    return StreamingResponse(
        generate_video_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers={"Cache-Control": "no-cache"},
    )
