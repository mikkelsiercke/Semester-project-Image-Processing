import numpy as np
import cv2 as cv
import socket

# Server settings
HOST = '172.20.10.6'  # Raspberry Pi IP-address
PORT = 65432  # Port number

capture = cv.VideoCapture(1)  # Specify video capture port
ret, first = capture.read()  # Read data from video capture port

# Background subtraction calibration reference
first_gray = cv.cvtColor(first, cv.COLOR_BGR2GRAY)
first_gray = cv.GaussianBlur(first_gray, (21, 21), 0)


# Width and height of camera frame
height = first_gray.shape[0]
width = first_gray.shape[1]
print(height)
print(width)


# Threshold settings
threshold_level = 55
threshold_max = 255


# How much distance 1 meter is in pixels
distance_pixels = 230


# Global distance variable - Set to 1000 so bounding boxes is not red on program start
D = 1000


# Global variable for center x and y coordinates
cX = 0
cY = 0

# Distance hit, true or not - in byte format
hit = b''
hit_true = b'true'
hit_false = b'false'


# Drawing position of centroid circle - convert to int, pixels do not have floats
circleY_position = int(height / 2)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # Connect to our defined host and port

    while True:
        centers = []

        ret, frame = capture.read()

        if not ret:
            break

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (21, 21), 0)

        difference = cv.absdiff(gray, first_gray)

        thresh = cv.threshold(difference, threshold_level, threshold_max, cv.THRESH_BINARY)[1]

        # Dilate the threshold source(input array), none in output(output array),
        # iterations = number of times dilation is applied
        thresh = cv.dilate(thresh, None, iterations=2)

        (contours, hierarchy) = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        for c in contours:
            if cv.contourArea(c) < 1300:
                continue

            (x, y, w, h) = cv.boundingRect(c)

            # Change rect color if distance is not held
            if D <= distance_pixels:
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                hit = hit_false
            else:
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                hit = hit_true

            M = cv.moments(c)

            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centers.append([cX, cY])
#            print(cX)

            cv.circle(frame, (cX, cY), 7, (255, 0, 255), -1)

            cv.putText(frame, "ID:", (cX - 20, cY - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        if len(centers) >= 2:
            # Distance y and x, [X][Y]
            dX = centers[0][0] - centers[1][0]
            dY = centers[0][1] - centers[1][1]
            D = np.sqrt(dX * dX + dY * dY)
            # print(D)

        # Display our openCV frames
        cv.imshow("frame", frame)
        cv.imshow("thresh", thresh)

        # Sending the hit data to our socket
        # s.send(hit)
        cxString = bytes(str(cX), encoding='utf8')
        # print(D)
        s.send(cxString)

        # Close program if 'Q' key is pressed
        key = cv.waitKey(1) & 0xFF

        if key == ord('q'):
            break


capture.release()
cv.destroyAllWindows()
