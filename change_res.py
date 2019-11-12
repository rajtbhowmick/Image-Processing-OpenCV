import cv2

cap = cv2.VideoCapture(0)


def make_1080p():
    cap.set(3, 1920)
    cap.set(4, 1080)
def make_720p():
    cap.set(3, 1280)
    cap.set(4, 720)
def make_480p():
    cap.set(3, 640)
    cap.set(4, 480)
def change_res(width, height):
    cap.set(3, width)
    cap.set(4, height)

def rescale_frame(frame, percent=75):
    scale_percentage = 75
    width = int(frame.shape[1] * scale_percentage/100)
    height = int(frame.shape[0] * scale_percentage/100)
    dim = (width,height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

#make_1080p()
#change_res(768,1366)

while True:
    ret, frame = cap.read()
    frame = rescale_frame(frame, percent=30)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #colorframe = rescale_frame(frame, percent=500)
    cv2.imshow('colorframe', frame)
    cv2.imshow('black and white', gray)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()