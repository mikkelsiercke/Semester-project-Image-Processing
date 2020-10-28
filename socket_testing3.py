import numpy as np
import cv2 as cv
import time
import socket
import json

# Server settings
HOST = '172.20.10.6' # Raspberry Pi IP-address
PORT = 65432  # Port number

capture = cv.VideoCapture(1)
ret, first = capture.read()

first_gray = cv.cvtColor(first, cv.COLOR_BGR2GRAY)
first_gray = cv.GaussianBlur(first_gray, (21, 21), 0)

height = first_gray.shape[0]
width = first_gray.shape[1]

threshold_level = 50
threshold_max = 255

distance_pixels = 230

personID = 0
currentPerson = []

D = 1000

# Distance hit, true or not - in byte format
hit = ''
hit_true = 'true'
hit_false = 'false'

# Drawing position of centroid circle - convert to int, pixels do not have floats
circleY_position = int(height / 2)

print(height)
print(width)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # Connect to our defined host and port

    while True:
        centers = []
        centersToSend = []

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

            Xcenter = x + int(w / 2)
            centers.append(Xcenter)

            centers.sort()  # sort -> stigende værdier
            print(centers)
            # cv.circle(frame, (Xcenter, y), 7, (255, 0, 255), cv.FILLED)

            if len(centers) == 2:
                if abs(centers[1] - centers[0]) < distance_pixels:
                    centersToSend.append(centers[0])
                    centersToSend.append(centers[1])
                    cv.rectangle(frame, (centers[1], 0), (centers[0], height), (0, 0, 255), 2)
            elif len(centers) >= 3:
                centersToSend.append(centers[2])
                # loop i listen, udregn den absolutte forskel på index og index-1 + index og index+1
                for i in range(1, len(centers) - 1):
                    if abs(centers[i] - centers[i + 1]) < distance_pixels:
                        cv.rectangle(frame, (centers[i], 0), (centers[i + 1], height), (0, 0, 255), 2)
                        # print('ok')
                    if abs(centers[i] - centers[i - 1]) < distance_pixels:
                         cv.rectangle(frame, (centers[i - 1], 0), (centers[i], height), (0, 0, 255), 2)

            #test hvis der er tre elementer
            #if len(centers) == 3:
             #   if abs(centers[2] - centers[1]) < distance_pixels:
              #      centersToSend.append(centers[1])
               #     centersToSend.append(centers[2])
                #if abs(centers[1] - centers[0]) < distance_pixels:
                 #   centersToSend.append(centers[0])
                  #  centersToSend.append(centers[1])



        cv.imshow("frame", frame)
        cv.imshow("thresh", thresh)

        data = json.dumps({"x": centersToSend})
        s.send(data.encode())

        key = cv.waitKey(1) & 0xFF

        if key == ord('q'):
            break

capture.release()
cv.destroyAllWindows()
