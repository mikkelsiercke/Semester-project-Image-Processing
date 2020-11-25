import numpy as np
import cv2 as cv
import time

capture = cv.VideoCapture(1)
ret, first = capture.read()

first_gray = cv.cvtColor(first, cv.COLOR_BGR2GRAY)
first_gray = cv.GaussianBlur(first_gray, (21, 21), 0)

while True:
    ret, frame = capture.read()

    if not ret:
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (21, 21), 0)

    difference = cv.absdiff(gray, first_gray)

    thresh = cv.threshold(difference, 60, 255, cv.THRESH_BINARY)[1]
    thresh = cv.dilate(thresh, None, iterations=2)

    cv.imshow("frame", frame)
    cv.imshow("thresh", thresh)

    key = cv.waitKey(1) & 0xFF

    if key == ord('q'):
        break

capture.release()
cv.destroyAllWindows()

