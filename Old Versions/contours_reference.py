import numpy as np
import cv2
import sys

video_path = './images/bg.mp4'
cv2.ocl.setUseOpenCL(False)

version = cv2.__version__.split('.')[0]
print(version)

# read video file
cap = cv2.VideoCapture(video_path)

# check opencv version
if version == '2':
    fgbg = cv2.BackgroundSubtractorMOG2()
if version == '4':
    fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=False)

while (cap.isOpened):

    # if ret is true than no error with cap.isOpened
    ret, frame = cap.read()

    if ret == True:

        # apply background substraction
        fgmask = fgbg.apply(frame)

        # check opencv version
        if version == '2':
            (contours, hierarchy) = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if version == '4':
            (contours, hierarchy) = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # looping for contours
        for c in contours:
            if cv2.contourArea(c) < 500:
                continue

            # get bounding box from contour
            (x, y, w, h) = cv2.boundingRect(c)

            # draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # calc Moments (moment of blob)
            M = cv2.moments(c)

            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            print(cX, cY)

            # draw moment
            cv2.circle(frame, (cX, cY), 5, (255, 0, 255), -1)

        # cv2.imshow('foreground and background', fgmask)
        cv2.imshow('rgb', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()