import cv2
from ultralytics import YOLO

cap = cv2.VideoCapture(0)
model = YOLO("yolo11n.pt")
while True:
    ret,frame = cap.read()
    if not ret:
        print("Error: Can't receive frame.")
        break
    results = model(frame, verbose=False)
    annotated = results[0].plot()
    cv2.imshow('Sparky Vision',annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()