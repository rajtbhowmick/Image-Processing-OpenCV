import numpy as np
import os
import cv2
from utils import image_resize


filename = 'recorded-videos/watermark.avi'
frames_per_second = 6
res = '480p'

def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}


def get_dims(cap, res='720p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]

    change_res(cap, width, height)
    return width, height

VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']



cap = cv2.VideoCapture(0)
#video_writer = cv2.VideoWriter_fourcc(*'MJPG')
#out = cv2.VideoWriter(filename,video_writer,12, get_dims(cap, res))
out = cv2.VideoWriter(filename, get_video_type(filename), frames_per_second, get_dims(cap, res))


img_path = 'images/logos/flag.png'
logo = cv2.imread(img_path, -1)
watermark = image_resize(logo, height=150, width=150)
watermark = cv2.cvtColor(watermark, cv2.COLOR_BGR2BGRA)
#cv2.imshow('watermark', watermark)
print(watermark.shape)
while True:
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    #OVERLAY WITH 4 CHANNELS & ALPHA
    frame_h, frame_w, frame_c = frame.shape
    #print(frame.shape)
    #gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
    #print(gray.shape)
    overlay = np.zeros((frame_h, frame_w, 4), dtype='uint8')
    #overlay[100:250,100:125] = (255,255,0,1)
    #overlay[100:250,150:255] = (0,255,0,1)

    #cv2.imshow('overlay', overlay)
    watermark_h, watermark_w, watermark_c = watermark.shape
    for i in range(0, watermark_h):
        for j in range(0, watermark_w):
            if watermark[i,j][3] != 0:
                #watermark[i,j]
                offset = 10
                h_offset = frame_h - watermark_h - offset
                w_offset = frame_w - watermark_w - offset
                overlay[h_offset + i, w_offset + j] = watermark[i,j]

    cv2.addWeighted(overlay, 0.25, frame, 1.0, 0, frame)



    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    out.write(frame)
    cv2.imshow('frame',frame)
    #cv2.imshow('frame', gray)
    if cv2.waitKey(6) & 0xFF == ord('q'):
        break


cap.release()
out.release()
cv2.destroyAllWindows()