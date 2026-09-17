import cv2
import os
from deepface import DeepFace as df
import pickle

path = 'faces'
if not os.path.exists(path):
        os.makedirs(path)

name = input("Enter name: ")

cap = cv2.VideoCapture(0)
print("'s' for save 'q' for quit")

while True:
    ret,frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    cv2.imshow('Live Feed', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s') or key == ord('S'):
        img_name = f"{name}.jpg"
        full_path = os.path.join(path, img_name)
        cv2.imwrite(full_path, frame)
        print(f"Saved: {full_path}")
        try:
            result = df.represent(
                img_path=full_path,
                model_name='ArcFace',
                detector_backend='opencv',
                enforce_detection=True
            )
            embedding = result[0]["embedding"]
            print("Face encoding generated!")

            db_path = os.path.join(
                path,
                'face_db.pkl'
            )

            if os.path.exists(db_path):
                with open(db_path, "rb") as file:
                    database = pickle.load(file)

            else:
                database = {}

            database[name] = embedding
            with open(db_path, "wb") as file:
                pickle.dump(database, file)

            print("Face encoding saved.")
            print(f"Database: {db_path}")
        except Exception as e:
            print("Face analysis failed:")
            print(e)
        break
    elif key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
