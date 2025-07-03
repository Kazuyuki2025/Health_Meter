import cv2
from ultralytics import YOLO
import numpy as np
import argparse
import datetime
from argparse import RawTextHelpFormatter

COLOR = (0,255,0)
VAR_THICKNESS = 20
FONT_SCALE = 2.0
TEXT_THICKNESS = 2
FINISH_COMMAND = "q"

# set now_time
dt_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
# set deta_type
tp = lambda x:list(map(int, x.split(',')))

# Format argment
parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
parser.add_argument('--limit', help='Set numuber of detected people', default=100000)
parser.add_argument('--fps', help='Set FPS', default=20)
parser.add_argument('--outlier', help='Set validation', 1000)
parser.add_argument('--model', help='Set model_data', default='model/yolov8n.pt')
parser.add_argument('--framesize', type=tp, help='Set width and heigh of framesize', default='1920,1080')
parser.add_argument('--input', help='Input video data', default=f'input_data/{dt_now}.mp4')
parser.add_argument('--output', help='Output video data', default=f'output_data/{dt_now}.mp4')
parser.add_argument('--csv', help='Output csv data', default=f'output_data/{dt_now}.csv')

parser.usage = parser.format_help()

# Set argument
args = parser.parse_args()
fps = args.fps
frame_width = args.framesize[0]
frame_height = args.framesize[1]
detect_limit = args.limit
detect_type = int(args.type)
input_file = args.input
output_file = args.output
csv_file = args.csv
model_data = args.model
validation = args.outlier

# Load learning model
model = YOLO(model_data)


# Open camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, fps)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

# Set detected_data array
coordinate = np.array(np.zeros((4, detect_limit), dtype=int)).T.tolist()
velocity = np.array(np.zeros((4, detect_limit), dtype=int)).T.tolist()
pre_velocity = np.array(np.zeros((4, detect_limit), dtype=int)).T.tolist()

# loop of detection
while cap.isOpened():
    success, frame = cap.read()

    if success:

        results = model.track(frame, persist=True, classes=[0], tracker="bytetrack.yaml")

        # Get captured image
        imageWidth = results[0].orig_shape[0]
        imageHeight = results[0].orig_shape[1]
        names = results[0].names
        classes = results[0].boxes.cls
        boxes = results[0].boxes
        annotatedFrame = results[0].plot()

        for box, cls in zip(boxes, classes):
            x1, x2, y1, y2 = [int(i) for i in box.xyxy[0]]
            name = names[int(cls)]
            if box.id is not None:
                ids = int(box.id[0])
            else:
                continue

            velocity[ids][0], velocity[ids][1], velocity[ids][2], velocity[ids][3] = abs(x1-coordinate[ids][0]), abs(x2-coordinate[ids][1]), abs(y1-coordinate[ids][2]), abs(y2-coordinate[ids][3])
            evaluation = int(abs(velocity[ids][0] - pre_velocity[ids][0]) + abs(velocity[ids][1] - pre_velocity[ids][1]) + abs(velocity[ids][2] - pre_velocity[ids][2]) + abs(velocity[ids][3] - pre_velocity[ids][3]))

            # Update cordinate and velocity
            coordinate[ids] = box.xyxy[0]
            print(f"Object: {name} Coordinates: StartX={x1}, StartY={y1}, EndX={x2}, EndY={y2}")

            LINE_START = (x1, y2)
            LINE_FINISH = (x1, y2-evaluation*4)
            ACTIVITY_COORDINATE = (x1+15, y2-10)

            # Write image
            if evaluation < validation:
                cv2.line(annotatedFrame, pt1=LINE_START, pt2=LINE_FINISH, color=COLOR, thickness=VAR_THICKNESS, lineType=cv2.LINE_4)
            cv2.putText(annotatedFrame, f"HUMAN ACTIVITY {evaluation}", ACTIVITY_COORDINATE, cv2.FONT_HERSHEY_PLAIN, FONT_SCALE, COLOR, TEXT_THICKNESS, cv2.LINE_AA)

        cv2.imshow("YOLOv8 Inference", annotatedFrame)

        if cv2.waitKey(1) & 0xFF == ord(FINISH_COMMAND):
            break

cap.release()
cv2.destroyAllWindows()
