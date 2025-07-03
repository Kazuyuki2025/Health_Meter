import argparse
from argparse import RawTextHelpFormatter
import cv2
import datetime
import os

dt_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
# Format argment
parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
parser.add_argument('--input', help='Input video data', default='input_data/input_video.mp4')
parser.add_argument('--start', help='Set start of frame', type = int, default=0)
parser.add_argument('--end', help='Set end of frame', type = int, default=0)
parser.add_argument('--save', help='Save showed data', action='store_true')

parser.usage = parser.format_help()

# Set argument
args = parser.parse_args()
input_data = args.input
start_frame = args.start
end_frame = args.end
save = args.save
output_data = f'output_video/{dt_now}_cutout.mp4'

cap = cv2.VideoCapture(input_data)

# Set for writing output_data
fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
writer = cv2.VideoWriter(output_data, fmt, fps,  (frame_width, frame_height))

totalframe = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
if end_frame == 0:
    end_frame = totalframe
if end_frame > totalframe:
    print("Error: end_frame is over totalframe")

cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
while cap.isOpened():
    ret, frame = cap.read()
    played_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    if ret:
        print(f"{played_frame} showed")
        key = cv2.waitKey(1) & 0xFF
        if played_frame >= end_frame:
            break
        if key == ord("q"):
            break
        cv2.imshow("cutshow", frame)
        if save:
            writer.write(frame)
    else:
        print("Cap Read Error")

writer.release()

if not save:
    os.remove(output_data)

cap.release()
cv2.destroyAllWindows()
