
import cv2
from ultralytics import YOLO

SOURCE = 0                      
MODEL = "yolov8n.pt"            
TRACKER = "bytetrack.yaml"      

model = YOLO(MODEL)
cap = cv2.VideoCapture(SOURCE)          

while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
        break

    
    results = model.track(frame, persist=True, tracker=TRACKER, verbose=False)[0]

    
    if results.boxes is not None and results.boxes.id is not None:
        boxes = results.boxes.xyxy.cpu().numpy().astype(int)
        ids = results.boxes.id.cpu().numpy().astype(int)
        classes = results.boxes.cls.cpu().numpy().astype(int)
        confs = results.boxes.conf.cpu().numpy()

        for (x1, y1, x2, y2), tid, c, conf in zip(boxes, ids, classes, confs):
            label = f"ID {tid} {model.names[c]} {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, max(y1 - 8, 15)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    win = "Object Detection & Tracking"
    cv2.imshow(win, frame)
    key = cv2.waitKey(1) & 0xFF
    
    if key in (ord("q"), 27) or cv2.getWindowProperty(win, cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()