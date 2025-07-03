import cv2
from ultralytics import YOLO
import numpy as np
import argparse
import csv
import datetime
from argparse import RawTextHelpFormatter
import math

COLOR = (0,255,0)
VAR_THICKNESS = 20
FONT_SCALE = 2.0
TEXT_THICKNESS = 2
FINISH_COMMAND = "q"
OUTLIER = 1000

# set now_time
dt_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
# set deta_type
tp = lambda x:list(map(int, x.split(',')))

# Format argment
parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
parser.add_argument('--type', help='Set demo_type', default=1)
parser.add_argument('--limit', help='Set numuber of detected people', default=100000)
parser.add_argument('--fps', help='Set FPS', default=20)
parser.add_argument('--model', help='Set model_data', default='model/yolov8n.pt')
parser.add_argument('--framesize', type=tp, help='Set width and heigh of framesize', default='1920,1080')
parser.add_argument('--output', help='Output video data', default = False)
parser.add_argument('--csv', help='Output csv data', default = False)
parser.add_argument('--start', help='Set start of frame', type = int, default=2)
parser.add_argument('--end', help='Set end of frame', type = int, default=2)
parser.add_argument('input', help='Input video data', default=f'input_data/{dt_now}.mp4')

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
start_frame = args.start
end_frame = args.end
validation = OUTLIER

# Load learning model
model = YOLO(model_data)

cap = cv2.VideoCapture(input_file)

totalframe = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
if end_frame == 0:
    end_frame = totalframe
if end_frame > totalframe:
    print("Error: end_frame is over totalframe")
    exit()
if start_frame <= 2:
    print("Error: start_frame is over 2")
    exit()

cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("---start---")

# Set detected_data array
coordinate = np.array(np.zeros((4, detect_limit), dtype=int)).T.tolist()
velocity = np.array(np.zeros((4, detect_limit), dtype=int)).T.tolist()
pre_velocity = np.array(np.zeros((4, detect_limit), dtype=int)).T.tolist()
activity_average = np.zeros(detect_limit, dtype=int)

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

if csv_file:
    csv_file = open(csv_file, mode='w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['frame_number', 'activity'])

if output_file:
    fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    writer = cv2.VideoWriter(output_file, fmt, fps, (frame_width, frame_height))

for i in range(frame_count):
        ret, frame = cap.read()
        played_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        if ret:
            results = model.track(frame, verbose=False, persist=True, classes=[0], tracker="bytetrack.yaml")
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

                velocity[ids][0], velocity[ids][1], velocity[ids][2], velocity[ids][3] = \
                abs(x1-coordinate[ids][0]), abs(x2-coordinate[ids][1]), abs(y1-coordinate[ids][2]), abs(y2-coordinate[ids][3])

                match detect_type:
                    case 1:
                        evaluation = abs(velocity[ids][0] - pre_velocity[ids][0]) + abs(velocity[ids][1] - pre_velocity[ids][1]) + abs(velocity[ids][2]\
                                     - pre_velocity[ids][2]) + abs(velocity[ids][3] - pre_velocity[ids][3])

                    case 2:
                        evaluation = abs(velocity[ids][0] - pre_velocity[ids][0]) + abs(velocity[ids][1] - pre_velocity[ids][1]) + abs(velocity[ids][2]\
                                     - pre_velocity[ids][2]) + abs(velocity[ids][3] - pre_velocity[ids][3])

                    case _:
                        print("Please select a specific type")

                coordinate[ids] = box.xyxy[0]
                activity_average[ids] = activity_average[ids] + evaluation
                if played_frame >= start_frame+2:
                    print(f"{played_frame-2}, {evaluation}")

                if output_file:
                    LINE_START = (x1, y2)
                    LINE_FINISH = (x1, int(y2-evaluation*4))
                    ACTIVITY_COORDINATE = (x1+15, y2-10)

                    if played_frame >= start_frame+3:
                        cv2.line(annotatedFrame, pt1=LINE_START, pt2=LINE_FINISH, color=COLOR, thickness=VAR_THICKNESS, lineType=cv2.LINE_4)
                    cv2.putText(annotatedFrame, f"HUMAN ACTIVITY {evaluation}", ACTIVITY_COORDINATE, cv2.FONT_HERSHEY_PLAIN, FONT_SCALE, COLOR, TEXT_THICKNESS, cv2.LINE_AA)
                    writer.write(annotatedFrame)

                if csv_file:
                    csv_writer.writerow([i, evaluation])

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if played_frame-2 >= end_frame:
            break
        cv2.imshow('Frame', annotatedFrame)

if csv_file:
    csv_file.close()
if output_file:
    writer.release()

cv2.destroyAllWindows()
print("---end---")
