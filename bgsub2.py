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

    (contours, hierarchy) = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv.contourArea(c) < 1300:
            continue

        (x, y, w, h) = cv.boundingRect(c)

        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        #M = cv.moments(c)

        #cX = int(M["m10"] / M["m00"])
        #cY = int(M["m10"] / M["m00"])

        #cv.circle(frame, (cX, cY), 5, (255, 0, 255), -1)

    cv.imshow("frame", frame)
    cv.imshow("thresh", thresh)

    key = cv.waitKey(1) & 0xFF

    if key == ord('q'):
        break

capture.release()
cv.destroyAllWindows()

