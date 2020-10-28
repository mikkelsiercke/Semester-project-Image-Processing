import cv2 as cv
import numpy as np

# Define background substraction model
backSubKNN = cv.createBackgroundSubtractorKNN()
backSubMOG2 = cv.createBackgroundSubtractorMOG2()

kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))

backSubGMG = cv.bgsegm.createBackgroundSubtractorGMG()

# Define the camera input
capture = cv.VideoCapture(1)

capture_gray = cv.cvtColor(capture, cv.COLOR_BGR2GRAY)

while True:
    # Set a frame that reads the camera input from capture variable
    ret, frame = capture_gray.read()

    # Define the foreground mask
    # fgMask = backSubKNN.apply(frame)
    fgmask = backSubGMG.apply(frame)

    fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)

    fgmask = cv.blur(fgmask, fgmask, (15, 15))

    # cv.rectangle(frame, (10, 2), (100, 20), (255, 255, 255), -1)
    # cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
    #           cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    cv.imshow('Frame', frame)
    cv.imshow('FG Mask', fgmask)

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break

