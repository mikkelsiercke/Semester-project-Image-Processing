import cv2 as cv
import numpy as np

capture = cv.VideoCapture(0)

while True:
    ret, frame = capture.read()

    if not ret:
        break

    kernel_size = 41

    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.GaussianBlur(frame_gray, (kernel_size, kernel_size), 0)

    frame_roi = frame_gray[135:170, 0:400]
    average = np.mean(frame_roi)

    thresh = cv.threshold(frame_gray, average * 0.10, 255, cv.THRESH_BINARY_INV)[1]

    thresh = cv.dilate(thresh, None, iterations=2)

    thresh = thresh[250:360, 0:640]

    (contours, hierarchy) = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv.contourArea(c) < 1300:
            continue

        (x, y, w, h) = cv.boundingRect(c)

    cv.imshow("frame ROI", frame_roi)
    cv.imshow("frame", frame)
    cv.imshow("Thresh", thresh)

    key = cv.waitKey(1) & 0xFF

    if key == ord('q'):
        break