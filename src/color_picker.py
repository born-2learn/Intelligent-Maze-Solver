import cv2
import numpy as np


def nothing(x):
    pass


cap = cv2.VideoCapture(1)
cv2.namedWindow('res')
cv2.createTrackbar('r_higher', 'res', 0, 255, nothing)
cv2.createTrackbar('g_higher', 'res', 0, 255, nothing)
cv2.createTrackbar('b_higher', 'res', 0, 255, nothing)
cv2.createTrackbar('r_lower', 'res', 0, 255, nothing)
cv2.createTrackbar('g_lower', 'res', 0, 255, nothing)
cv2.createTrackbar('b_lower', 'res', 0, 255, nothing)

while True:
    ret, frame = cap.read()
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    r_higher = cv2.getTrackbarPos('r_higher', 'res')
    g_higher = cv2.getTrackbarPos('g_higher', 'res')
    b_higher = cv2.getTrackbarPos('b_higher', 'res')
    r_lower = cv2.getTrackbarPos('r_lower', 'res')
    g_lower = cv2.getTrackbarPos('g_lower', 'res')
    b_lower = cv2.getTrackbarPos('b_lower', 'res')

    lower_blue = np.array([b_lower, g_lower, r_lower])  # 100 67 65
    upper_blue = np.array([b_higher, g_higher, r_higher])  # 112 255 255

    mask = cv2.inRange(frame, lower_blue, upper_blue)

    res = cv2.bitwise_and(frame, frame, mask=mask)
    print(r_higher, " ", g_higher, " ", b_higher, " ", r_lower, " ", g_lower, " ", b_lower)

    # kernel=np.ones((15,15),np.float32)/225
    # smoothened=cv2.filter2D(res,-1,kernel)

    # blur=cv2.blur(res,(5,5))

    # Gaussianblur=cv2.GaussianBlur(res,(15,15),0)

    # kernelM=np.ones((5,5),np.uint8)

    # eroded=cv2.erode(mask,kernelM,iterations=1)
    # erode=cv2.bitwise_and(frame,frame,mask=eroded)

    # dilated=cv2.dilate(eroded,kernelM,iterations=1)
    # dilate=cv2.bitwise_and(frame,frame,mask=dilated)

    # closing=cv2.morphologyEx(dilated,cv2.MORPH_CLOSE,kernelM)
    # closed=cv2.bitwise_and(frame,frame,mask=closing)

    ##    cv2.imshow('frame',frame)
    ##    cv2.imshow('mask',mask)
    cv2.imshow('res', res)
    ##    cv2.imshow('smoothened',smoothened)
    ##    cv2.imshow('blur',blur)
    ##    cv2.imshow('Gaussianblur',Gaussianblur)
    # cv2.imshow('eroded',eroded)
    # cv2.imshow('dilated',dilated)
    # cv2.imshow('erode',erode)
    # cv2.imshow('dilate',dilate)
    # cv2.imshow('closing',closing)
    # cv2.imshow('closed',closed)

    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
cap.release()
