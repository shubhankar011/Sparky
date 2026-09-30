import cv2
from ultralytics import YOLO
from deepface import DeepFace
import os

model = YOLO('yolo11n.pt')
yolo_detectors = list(range(1, 80))
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def _grab_frame():
    cap = cv2.VideoCapture(0)
    frame = None
    # webcams often return a black/garbage first frame — read a few
    # to let auto-exposure settle before taking the real one
    for _ in range(5):
        ok, frame = cap.read()
        if not ok:
            frame = None
            break
    cap.release()
    return frame


def detect_objects_once():
    frame = _grab_frame()
    if frame is None:
        return []
    result = model(frame, classes=yolo_detectors, verbose=False)
    boxes = result[0].boxes
    if boxes is None or len(boxes) == 0:
        return []
    return list({model.names[int(c)] for c in boxes.cls})


def identify_people_once():
    frame = _grab_frame()
    if frame is None:
        return []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detections = face_detector.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5,
        minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE,
    )
    names = []
    for (x, y, w, h) in detections:
        face_crop = frame[y:y + h, x:x + w]
        if face_crop.size == 0:
            continue
        try:
            dfs = DeepFace.find(face_crop, "f   aces", enforce_detection=False, silent=True)
            name = "Unknown"
            if len(dfs) > 0 and not dfs[0].empty:
                path = dfs[0]["identity"].iloc[0]
                name = os.path.basename(path).split(".")[0]
            names.append(name)
        except Exception as e:
            print(e)
            names.append("Unknown")
    return names