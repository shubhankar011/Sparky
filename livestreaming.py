import cv2
import numpy as np
import pickle
from deepface import DeepFace
from ultralytics import YOLO


# SETTINGS

PERSON_CONFIDENCE = 0.5
DISTANCE_THRESHOLD = 10

''' How close a new detection must be to
an existing person to be considered
the same person.'''
MATCH_DISTANCE = 120

'''Number of frames before an unseen
person is removed from cache.'''
MAX_MISSING_FRAMES = 15


# LOAD MODELS

print("Loading YOLO...")
yolo = YOLO("yolo11n.pt")

print("Loading face detector...")

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

print("Loading face database...")

with open("faces/face_db.pkl", "rb") as f:
    database = pickle.load(f)

print("Everything loaded.")


# =========================
# CAMERA
# =========================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not open camera.")
    exit()


# PERSON CACHE

people = {}

next_id = 0


# FACE RECOGNITION

def recognize_face(face_crop):

    try:

        result = DeepFace.represent(
            img_path=face_crop,
            model_name="ArcFace",
            detector_backend="skip",
            enforce_detection=False
        )

        embedding = np.array(
            result[0]["embedding"]
        )

        best_name = "Unknown"
        best_distance = float("inf")

        for name, stored_embedding in database.items():

            stored_embedding = np.array(
                stored_embedding
            )

            distance = np.linalg.norm(
                embedding - stored_embedding
            )

            if distance < best_distance:

                best_distance = distance
                best_name = name


        if best_distance < DISTANCE_THRESHOLD:

            confidence = max(
                0,
                100 - best_distance * 5
            )
            
            return best_name, confidence

        return "Unknown", 0


    except Exception as e:

        print("DeepFace error:", e)

        return "Unknown", 0

# MAIN LOOP

while True:

    ret, frame = cap.read()

    if not ret:
        break


    # YOLO

    results = yolo(
        frame,
        verbose=False,
        classes=[0]
    )


    detections = []
    for box in results[0].boxes:
        confidence = float(box.conf[0])
        if confidence < PERSON_CONFIDENCE:
            continue

        x1, y1, x2, y2 = map(
            int,
            box.xyxy[0]
        )

        center = (
            (x1 + x2) // 2,
            (y1 + y2) // 2
        )

        detections.append(
            (x1, y1, x2, y2, center)
        )

    # KEEP TRACK OF PEOPLE

    current_ids = set()

    for x1, y1, x2, y2, center in detections:

        cx, cy = center

        matched_id = None

        smallest_distance = float("inf")

        # FIND EXISTING PERSON
        for pid, data in people.items():

            old_cx, old_cy = data["center"]

            distance = np.sqrt(
                (cx - old_cx) ** 2 +
                (cy - old_cy) ** 2
            )


            if (
                distance < MATCH_DISTANCE
                and distance < smallest_distance
            ):

                smallest_distance = distance
                matched_id = pid


        # NEW PERSON

        if matched_id is None:

            matched_id = next_id
            next_id += 1


            people[matched_id] = {
                "center": center,
                "name": None,
                "confidence": 0,
                "missing": 0,
                "recognized": False
            }


            print(f"\nNEW PERSON DETECTED → ID {matched_id}")

        # UPDATE EXISTING PERSON

        data = people[matched_id]

        data["center"] = center
        data["missing"] = 0

        current_ids.add(matched_id)

        # ONLY RECOGNIZE NEW PEOPLE

        if not data["recognized"]:

            person_crop = frame[
                max(0, y1):min(frame.shape[0], y2),
                max(0, x1):min(frame.shape[1], x2)
            ]


            if person_crop.size > 0:

                gray = cv2.cvtColor(
                    person_crop,
                    cv2.COLOR_BGR2GRAY
                )

                faces = face_detector.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(60, 60)
                )

                if len(faces) > 0:

                    # Largest face
                    fx, fy, fw, fh = max(
                        faces,
                        key=lambda f: f[2] * f[3]
                    )


                    face_crop = person_crop[
                        fy:fy + fh,
                        fx:fx + fw
                    ]


                    print(f"Running DeepFace for ID {matched_id}...")


                    name, confidence = recognize_face(face_crop)


                    data["name"] = name
                    data["confidence"] = confidence

                    # IMPORTANT
                    # Once recognized, LOCK this person.

                    data["recognized"] = True


                    print(f"ID {matched_id} → {name}")

        # DRAW PERSON BOX

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (255, 0, 0),
            2
        )

        # LABEL

        if data["name"] is None:
            label = "Analyzing..."

        elif data["name"] == "Unknown":
            label = "Unknown"

        else:
            label = (
                f"{data['name']} "
                f"{data['confidence']:.0f}%"
            )


        cv2.putText(
            frame,
            label,
            (x1, max(30, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
    # HANDLE PEOPLE WHO LEFT

    for pid in list(people.keys()):

        if pid not in current_ids:

            people[pid]["missing"] += 1


            if people[pid]["missing"] > MAX_MISSING_FRAMES:

                print(f"Person ID {pid} LEFT")

                del people[pid]


    # DISPLAY
    cv2.imshow("Sparky Vision",frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()