import numpy as np
import cv2 as cv
from Code.CentroidTracker import CentroidTracker
import time

capture = cv.VideoCapture('pedestrians.mp4')
ret, first = capture.read()

first_gray = cv.cvtColor(first, cv.COLOR_BGR2GRAY)
first_gray = cv.GaussianBlur(first_gray, (21, 21), 0)

height = first_gray.shape[0]
width = first_gray.shape[1]

threshold_level = 60
threshold_max = 255

tracker = CentroidTracker(maxDisappeared=80, maxDistance=90)

# Drawing position of centroid circle - convert to int, pixels do not have floats
circleY_position = int(height / 2)

object_id_list = []

print(height)
print(width)

while True:
    centers = []
    rects = []

    rect_color = (0, 255, 0)

    ret, frame = capture.read()

    if not ret:
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (21, 21), 0)

    difference = cv.absdiff(gray, first_gray)

    thresh = cv.threshold(difference, threshold_level, threshold_max, cv.THRESH_BINARY)[1]
    # Dilate the threshold source(input array), none in output(output array),
    # iterations = number of times dilation isa pplied
    thresh = cv.dilate(thresh, None, iterations=2)

    (contours, hierarchy) = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv.contourArea(c) < 1300:
            continue

        (x, y, w, h) = cv.boundingRect(c)

        #cv.rectangle(frame, (x, y), (x + w, y + h), rect_color, 2)

        M = cv.moments(c)

        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        centers.append([cX, cY])

        #cv.circle(frame, (cX, cY), 7, (255, 0, 255), -1)

        # cv.putText(frame, "ID:", (cX - 20, cY - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        person_box = [w, h, w, h]
        rects.append(person_box)

        if len(centers) >= 2:
            # Distance y and x, [X][Y]
            dX = centers[0][0] - centers[1][0]
            dY = centers[0][1] - centers[1][1]
            D = np.sqrt(dX * dX)
            # print(D)

        # if D <= 1000:
        # (x, y, w, h) = cv.boundingRect(c)
    #
    #

    objects = tracker.update(rects)
    for (objectId, bbox) in objects.items():
        x1, y1, x2, y2 = bbox
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        cX = int((x1 + x2) / 2.0)
        cY = int((y1 + y2) / 2.0)

        if objectId not in object_id_list:
            object_id_list.append(objectId)
            cv.circle(frame, (cX, cY), 7, (255, 0, 255), -1)

        cv.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        text = "ID: {}".format(objectId)
        cv.putText(frame, text, (x1, y1 - 5), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1)

    cv.imshow("frame", frame)
    cv.imshow("thresh", thresh)

    key = cv.waitKey(1) & 0xFF

    if key == ord('q'):
        break

capture.release()
cv.destroyAllWindows()
