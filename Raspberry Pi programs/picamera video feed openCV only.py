import picamera
import picamera.array
import cv2
import numpy as np
import time
import os

# Global camera setting values
camResX, camResY = (640 * 4, 480 * 2)  # PiCamera resolution values
fps = 30
c_num = 1  # PiCamera camera number camera_num options = [0, 1]
s_mode = 'side-by-side'  # PiCamera stereo mode stereo mode options = ['none', 'side-by-side', top-bottom]

# -------------------------------------------------------------------------------------------------------------------- #
# PiCamera and OpenCV setup
# -------------------------------------------------------------------------------------------------------------------- #

camera = picamera.PiCamera(camera_num=c_num, stereo_mode=s_mode, stereo_decimate=False, led_pin=3)

# Important: Camera resolution height must be dividable by 16, and width by 32 TODO: check if this is still true

# Video stream
video = picamera.array.PiRGBArray(camera)
globalFrame = None
frame = None

# videoCapture Object
save_directory = "/home/pi/Desktop/OpenMosseCam/DCIM"
videoFileName = "video " + str(time.ctime()) + ".avi"
fourcc = cv2.VideoWriter_fourcc(*'MPEG')
video_out = cv2.VideoWriter(os.path.join(save_directory, videoFileName), fourcc, fps, (camResX, camResY))

steps = 0
stepcount = 0

for frameBuf in camera.capture_continuous(video, format="bgra", use_video_port=True):

    globalFrame = np.flipud(video.array)
    frame = cv2.resize(globalFrame, (256, 96))

    video.truncate(0)
    cv2.imshow("frame", frame)
    key = cv2.waitKey(1) & 0xFF

    while True:
        # add frames to video capture
        if stepcount < steps:
            stepcount += 1
            video_out.write(globalFrame)
            print("step ", stepcount, " out of ", steps)
#         elif stepcount >= steps:
#             break
#
# # release videoCapture object
# video_out.release()
# # close all the frames (I think there may not be any)
# cv2.destroyAllWindows()
