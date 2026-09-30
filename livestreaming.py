import cv2
from ultralytics import YOLO
from deepface import DeepFace
import os
import threading
import math

thread_lock = threading.Lock()

model = YOLO('yolo11n.pt')
yolo_detectors = list(range(1,80))
cap = cv2.VideoCapture(0)
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

face_details_cache = {}     # face_id -> "MALE 25"
face_names_cache = {}       # face_id -> "John"
analyzing_ids = set()       # face_ids currently running a background thread
last_analyzed_frame = {}    # face_id -> frame_counter value at last analysis

RUN_INTERVAL = 60
frame_counter = 0

# --- simple centroid tracker: gives each physical face a stable id ---
next_face_id = 0
tracked_faces = {}   # face_id -> (cx, cy) from the previous frame
MAX_DISTANCE = 120    # px — tune to your resolution/how fast people move
current_objects = set()
current_people = []


def get_seen_objects():
    with thread_lock:
        return list(current_objects)


def get_seen_people():
    with thread_lock:
        return list(current_people)

def match_faces(detections):
    """
    Matches this frame's raw detections to last frame's tracked centroids
    by nearest distance, so the same physical face keeps the same id.
    New faces (or ones that moved too far) get a fresh id.
    """
    global next_face_id, tracked_faces

    new_tracked = {}
    results = []
    used_ids = set()

    for (x, y, w, h) in detections:
        cx, cy = x + w / 2, y + h / 2

        best_id, best_dist = None, MAX_DISTANCE
        for fid, (px, py) in tracked_faces.items():
            if fid in used_ids:
                continue
            dist = math.hypot(cx - px, cy - py)
            if dist < best_dist:
                best_dist, best_id = dist, fid

        if best_id is None:
            best_id = next_face_id
            next_face_id += 1

        used_ids.add(best_id)
        new_tracked[best_id] = (cx, cy)
        results.append((best_id, (x, y, w, h)))

    tracked_faces = new_tracked
    return results


def find(face_crop, face_id):
    try:
        dfs = DeepFace.find(face_crop, "faces", enforce_detection=False, silent=True)
        name = "Unknown"
        if len(dfs) > 0 and not dfs[0].empty:
            path = dfs[0]["identity"].iloc[0]
            name = os.path.basename(path).split(".")[0]
        with thread_lock:
            face_names_cache[face_id] = name
    except Exception as e:
        print(e)
        with thread_lock:
            face_names_cache[face_id] = "Unknown"
    print(f"Face done...{face_id}")
    with thread_lock:
        analyzing_ids.discard(face_id)


def profiles(face_crop, face_id):
    try:
        analysis = DeepFace.analyze(
            face_crop, actions=["age", "gender"], enforce_detection=False, silent=True
        )
        face_data = analysis[0] if isinstance(analysis, list) else analysis
        gender = "MALE" if face_data["dominant_gender"] == "Man" else "FEMALE"
        age = int(face_data["age"])
        with thread_lock:
            face_details_cache[face_id] = f"{gender} {age}"
    except Exception as e:
        print(e)
        with thread_lock:
            face_details_cache[face_id] = "Unknown"
    print(f"Profile done...{face_id}")
    find(face_crop, face_id)

    '''
    Below code use only when in face this code is removed
    with thread_lock:
        analyzing_ids.discard(face_id)'''


def run_vision():
    global frame_counter
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame_counter += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detections = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100),
            flags=cv2.CASCADE_SCALE_IMAGE,
        )

        faces = match_faces(detections)
        # print(faces)
        seen_ids = {fid for fid, _ in faces}
        result = model(frame,classes=yolo_detectors,verbose=False)
        # print(seen_ids)
        # drop cached data for ids that left the frame, so they don't linger
        # or get reused on a different face later
        with thread_lock:
            for fid in list(face_names_cache.keys()):
                if fid not in seen_ids:
                    face_names_cache.pop(fid, None)
                    face_details_cache.pop(fid, None)
                    last_analyzed_frame.pop(fid, None)

        for face_id, (x, y, w, h) in faces:
            face_crop = frame[y:y + h, x:x + w]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if face_crop.size == 0:
                continue

            with thread_lock:
                current_name = face_names_cache.get(face_id, "Analyzing...")
                current_text = face_details_cache.get(face_id, "Analyzing...")
                already_running = face_id in analyzing_ids

            due = (frame_counter - last_analyzed_frame.get(face_id, -RUN_INTERVAL)) >= RUN_INTERVAL

            if not already_running and due:
                with thread_lock:
                    analyzing_ids.add(face_id)
                last_analyzed_frame[face_id] = frame_counter
                crop_copy = face_crop.copy()
                threading.Thread(target=find, args=(crop_copy, face_id), daemon=True).start()

            cv2.putText(frame, current_name, (x, y - 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            # cv2.putText(frame, current_text, (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 25, 80), 2)

        cv2.imshow("Sparky Vision", result[0].plot())
        if cv2.waitKey(1) & 0xff == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

def run_vision_web():
    global frame_counter
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame_counter += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detections = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100),
            flags=cv2.CASCADE_SCALE_IMAGE,
        )

        faces = match_faces(detections)
        # print(faces)
        seen_ids = {fid for fid, _ in faces}
        result = model(frame,classes=yolo_detectors,verbose=False)
        # print(seen_ids)
        # drop cached data for ids that left the frame, so they don't linger
        # or get reused on a different face later
        with thread_lock:
            for fid in list(face_names_cache.keys()):
                if fid not in seen_ids:
                    face_names_cache.pop(fid, None)
                    face_details_cache.pop(fid, None)
                    last_analyzed_frame.pop(fid, None)

        for face_id, (x, y, w, h) in faces:
            face_crop = frame[y:y + h, x:x + w]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if face_crop.size == 0:
                continue

            with thread_lock:
                current_name = face_names_cache.get(face_id, "Analyzing...")
                current_text = face_details_cache.get(face_id, "Analyzing...")
                already_running = face_id in analyzing_ids

            due = (frame_counter - last_analyzed_frame.get(face_id, -RUN_INTERVAL)) >= RUN_INTERVAL

            if not already_running and due:
                with thread_lock:
                    analyzing_ids.add(face_id)
                last_analyzed_frame[face_id] = frame_counter
                crop_copy = face_crop.copy()
                threading.Thread(target=find, args=(crop_copy, face_id), daemon=True).start()

            cv2.putText(frame, current_name, (x, y - 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            # cv2.putText(frame, current_text, (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 25, 80), 2)

        _, buffer = cv2.imencode(".jpg", result[0].plot())

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + buffer.tobytes() +
            b"\r\n"
        )

    cap.release()
    cv2.destroyAllWindows()

def start_vision_thread():
    """Call this from another script to run vision detection in the background."""
    t = threading.Thread(target=run_vision, args=(display,), daemon=True)
    t.start()
    return t
if __name__ == "__main__":
    run_vision()
