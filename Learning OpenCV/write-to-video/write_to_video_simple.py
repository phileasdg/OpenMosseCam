import numpy
import cv2

# video feed (in this case I'm just putting one image
frame = cv2.imread(r"C:\Users\phile\OneDrive\Bureau\openCVtest\Erotische_Aufnahme_c1880s.jpg")
frame_height = frame.shape[0]
frame_width = frame.shape[1]

print("frame dim", frame_width, frame_height)

# videoCapture object
video_out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (frame_width, frame_height))
# video_out = cv2.VideoWriter('export path', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, (frame_width, frame_height))

steps = 60
# add frames to video capture
for i in range(steps):
    video_out.write(frame)
    print("step ", i, " out of ", steps)

# release videoCapture object
video_out.release()

# close all the frames (I think there may not be any)
cv2.destroyAllWindows()
